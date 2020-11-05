# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import Optional, Callable, List
from multiprocessing import Process, SimpleQueue

# Local
from .task import Task

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# --------------------------------------------------------- class: MultiProcess ---------------------------------------------------------- #

class MultiProcess:

    # ------------------------------------------------------------- Init ------------------------------------------------------------- #

    def __init__(
        self,
        tasks: List[Task] = []
    ):
        """Creates a new multiproceess object

        Args:
            tasks (List[Task], optional): Tasks to innit with. More can be added later. Defaults to [].
        """    
        self.tasks = tasks


    # -------------------------------------------------------- Public methods -------------------------------------------------------- #

    def solve(self, timeout: Optional[float] = None) -> List[any]:
        """Solves all added tasks in parallel

        Args:
            timeout (Optional[float], optional): Timeout to use for tasks wich do not have a timeout speciified yet. Defaults to None.

        Returns:
            List[any]: Result or exception for each task (exception will not be thrown, but returned)
        """        
        queue = SimpleQueue()
        processes = []
        taks_id = 0

        for task in self.tasks:
            task.timeout = task.timeout or timeout
            p = Process(target=self.__solve_task, args=(task, taks_id, queue,))
            p.start()
            processes.append(p)
            taks_id += 1
        
        for p in processes:
            p.join()

        results = [queue.get() for _ in processes]
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