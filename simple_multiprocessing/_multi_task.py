# ------------------------------------------------------------ Imports ----------------------------------------------------------- #

# System
from abc import abstractmethod
from typing import Optional, Callable, List
from threading import Thread, Lock
from multiprocessing import Manager
import sys

# Pip
import stopit

# Local
from .models.task import Task

# -------------------------------------------------------------------------------------------------------------------------------- #



# ------------------------------------------------------- class: _MultiTask ------------------------------------------------------ #

class _MultiTask:

    # --------------------------------------------------------- Init --------------------------------------------------------- #

    def __init__(
        self,
        tasks: List[Optional[Task]] = []
    ):
        """Creates a new _MultiTask object

        Args:
            tasks (List[Optional[Task]], optional): Tasks to innit with. More can be added later. Defaults to [].
        """
        self.tasks = tasks
        self.__lock = Lock()


    # -------------------------------------------------- Abstract properties ------------------------------------------------- #

    @abstractmethod
    def _proc_cls(self) -> type:
        pass


    # ---------------------------------------------------- Public methods ---------------------------------------------------- #

    def solve(
        self,
        timeout: Optional[float] = None,
        max_concurent_processes: Optional[int] = None,
        print_task_exception: bool = False,
        return_task_exception: bool = True,
        return_value_on_exception: Optional[any] = None
    ) -> List[any]:
        """Solves all added tasks in parallel

        KwArgs:
            timeout (Optional[float], optional):                 Timeout to use for tasks wich do not have a timeout
                                                                 speciified yet. Defaults to None.
            max_concurent_processes (Optional[int], optional):   Maximum comcurent processes to execute at a time
                                                                 (Thread or multiprocess.Process).
            print_task_exception (bool, optional):               If True, prints stacktrace. Defaults to True.
            return_task_exception (bool, optional):              If True, returns caught exception. Defaults to False.
            return_value_on_exception (Optional[any], optional): What to return upon caught exception if 'return_exception'
                                                                 is False. Defaults to None.

        Returns:
            List[any]: Result or exception for each task (exception will not be thrown, but returned)
        """

        proc_cls = self._proc_cls()
        is_threaded = proc_cls == Thread
        self.__results = [0 for _ in range(len(self.tasks))]

        if not is_threaded:
            self.__results = Manager().list([0 for _ in range(len(self.tasks))])

        processes = []
        null_task_ids = []
        taks_id = 0

        for task in self.tasks:
            if task:
                task.timeout = task.timeout or timeout
                task.timout_function = task.timout_function or stopit.ThreadingTimeout if is_threaded else stopit.SignalTimeout
                processes.append(proc_cls(target=self.__solve_task, args=(task, taks_id, print_task_exception, return_task_exception, return_value_on_exception)))
            else:
                null_task_ids.append(taks_id)

            taks_id += 1

        active_processes = []
        finished_processes = []
        max_concurent_processes = max_concurent_processes if max_concurent_processes and max_concurent_processes > 0 else sys.maxsize

        while True:
            while len(active_processes) < max_concurent_processes and len(processes) > 0:
                p = processes.pop(0)
                p.start()
                active_processes.append(p)

            if len(active_processes) == 0:
                break

            while True:
                finished_process_pos = None

                for i, p in enumerate(active_processes):
                    p.join(timeout=0)

                    if not p.is_alive():
                        finished_process_pos = i
                        p.join()

                        break

                if finished_process_pos is not None:
                    finished_process = active_processes.pop(finished_process_pos)
                    finished_processes.append(finished_process)

                    break

        for taks_id in null_task_ids:
            self.__results[taks_id] = None

        return  self.__results

    # Alias
    execute = solve

    @classmethod
    def solve_cls(
        cls,
        tasks: List[Optional[Task]],
        timeout: Optional[float] = None,
        max_concurent_processes: Optional[int] = None
    ) -> List[any]:
        """Solves all added tasks in parallel

        Args:
            tasks (List[Optional[Task]]): Tasks to innit with. More can be added later.
        
        KwArgs:
            timeout (Optional[float], optional):                 Timeout to use for tasks wich do not have a timeout
                                                                 speciified yet. Defaults to None.
            max_concurent_processes (Optional[int], optional):   Maximum comcurent processes to execute at a time
                                                                 (Thread or multiprocess.Process).
            print_task_exception (bool, optional):               If True, prints stacktrace. Defaults to True.
            return_task_exception (bool, optional):              If True, returns caught exception. Defaults to False.
            return_value_on_exception (Optional[any], optional): What to return upon caught exception if 'return_exception'
                                                                 is False. Defaults to None.

        Returns:
            List[any]: Result or exception for each task (exception will not be thrown, but returned)
        """
        return cls(tasks).solve(timeout=timeout, max_concurent_processes=max_concurent_processes)

    # Alias
    execute_cls = solve_cls


    # ---------------------------------------------------- Private methods --------------------------------------------------- #

    def __solve_task(
        self,
        task: Task,
        id: int,
        print_task_exception: bool,
        return_task_exception: bool,
        return_value_on_exception: Optional[any]
    ) -> None:
        try:
            res = task.execute(
                print_exception=print_task_exception,
                return_exception=return_task_exception,
                return_value_on_exception=return_value_on_exception
            )
        except Exception as e:
            res = e

        self.__lock.acquire()
        try:
            self.__results[id] = res
        finally:
            self.__lock.release()


# -------------------------------------------------------------------------------------------------------------------------------- #