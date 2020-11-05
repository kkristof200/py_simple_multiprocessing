# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import Optional, Callable

# Pip
import stopit

# Local
from .constants import TIME_OUT_ERROR

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ------------------------------------------------------------- class: Task -------------------------------------------------------------- #

class Task:

    # ------------------------------------------------------------- Init ------------------------------------------------------------- #

    def __init__(
        self,
        target: Callable,
        *args,
        timeout: Optional[float] = None,
        **kwargs
    ):
        """Creates a new Task object

        Args:
            target (Callable): Function to call
            timeout (Optional[float], optional): Timeout of the task. Defaults to None.

        *args: Args to call the target with.
        **kwargs: Kwargs to call the target with.
        """
        self.target = target
        self.args = args
        self.kwargs = kwargs
        self.timeout = timeout


    # -------------------------------------------------------- Public methods -------------------------------------------------------- #

    def execute(self, timeout: Optional[float] = None) -> any:
        """Calls target with the given params

        Args:
            timeout (Optional[float], optional): Timeout of the task.
                                                 Only needed, if you want to override the timeout given at init.
                                                 Defaults to None.

        Returns:
            any: Return value of target
        
        Throws:
            TIME_OUT_ERROR - if task is not finished befor the given timeout ends
        """

        return self.__execute_with_timeout(timeout=self.timeout or timeout)


    # ------------------------------------------------------- Private methods -------------------------------------------------------- #

    @stopit.threading_timeoutable(default=TIME_OUT_ERROR, timeout_param='timeout')
    def __execute_with_timeout(self, timeout: Optional[float] = None) -> any:
        return self.target(*self.args, **self.kwargs)


# ---------------------------------------------------------------------------------------------------------------------------------------- #