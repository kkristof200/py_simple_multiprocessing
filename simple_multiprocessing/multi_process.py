# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import Optional, Callable, List
from multiprocessing import Process, SimpleQueue
import sys

# Local
from .task import Task

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# --------------------------------------------------------- class: MultiProcess ---------------------------------------------------------- #

class MultiProcess:

    # ------------------------------------------------------------- Init ------------------------------------------------------------- #

    def __init__(
        self,
        tasks: List[Optional[Task]] = []
    ):
        """Creates a new multiproceess object

        Args:
            tasks (List[Optional[Task]], optional): Tasks to innit with. More can be added later. Defaults to [].
        """
        self.tasks = tasks


    # -------------------------------------------------------- Public methods -------------------------------------------------------- #

    def solve(self, timeout: Optional[float] = None, max_concurent_processes: Optional[int] = None) -> List[any]:
        """Solves all added tasks in parallel

        Args:
            timeout (Optional[float], optional): Timeout to use for tasks wich do not have a timeout speciified yet. Defaults to None.
            max_concurent_processes (Optional[int], optional): Maximum comcurent processes to execute at a time.

        Returns:
            List[any]: Result or exception for each task (exception will not be thrown, but returned)
        """        
        queue = SimpleQueue()
        processes = []
        taks_id = 0
        null_task_ids = []

        for task in self.tasks:
            if task:
                task.timeout = task.timeout or timeout
                p = Process(target=self.__solve_task, args=(task, taks_id, queue,))
                processes.append(p)
            else:
                null_task_ids.append(taks_id)

            taks_id += 1

        active_processes = []
        finished_processes = []
        max_concurent_processes = max_concurent_processes if max_concurent_processes and max_concurent_processes > 0 else sys.maxsize

        while True:
            while len(active_processes) < max_concurent_processes and len(processes) > 0:
                process = processes.pop(0)
                process.start()
                active_processes.append(process)

            if len(active_processes) == 0:
                break

            while True:
                finished_process_pos = None

                for i, process in enumerate(active_processes):
                    process.join(timeout=0)

                    if not process.is_alive():
                        finished_process_pos = i
                        process.join()

                        break

                if finished_process_pos is not None:
                    finished_process = active_processes.pop(finished_process_pos)
                    finished_processes.append(finished_process)

                    break

        results = [queue.get() for _ in finished_processes]

        for taks_id in null_task_ids:
            results.append((taks_id, None))

        sorted_results = sorted(results, key=lambda tup: tup[0])

        return [r_tup[1] for r_tup in sorted_results]


    # ------------------------------------------------------- Private methods -------------------------------------------------------- #

    def __solve_task(self, task: Task, id: int, queue: SimpleQueue) -> None:
        try:
            result = task.execute()
        except Exception as e:
            result = e

        queue.put((id, result))


# ---------------------------------------------------------------------------------------------------------------------------------------- #