# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import Optional, Callable
import time

# Pip
import stopit
from noraise import noraise

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
        timout_function: Optional[Callable] = None,
        **kwargs
    ):
        """Creates a new Task object

        Args:
            target (Callable): Function to call
            timeout (Optional[float], optional): Timeout of the task. Defaults to None.
            timout_function (Optional[Callable], optional): Timeout functiion to use the task. Accepted values are 'stopit.ThreadingTimeout' annd 'stopit.SignalTimeout', Defaults to None (Will be chosen automatically).

        *args: Args to call the target with.
        **kwargs: Kwargs to call the target with.
        """
        self.target = target
        self.args = args
        self.kwargs = kwargs
        self.timeout = timeout
        self.timout_function = timout_function


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

    def __execute_with_timeout(self, timeout: Optional[float] = None) -> any:
        try:
            if self.timout_function:
                with stopit.ThreadingTimeout(timeout, swallow_exc=False):
                    @noraise(return_exception=True)
                    def __execute(target: Callable, *args, **kwargs):
                        return target(*args, **kwargs)

                    return __execute(self.target, *self.args, **self.kwargs)
            else:
                return self.target(*self.args, **self.kwargs)
        except stopit.TimeoutException:
            raise TIME_OUT_ERROR


# ---------------------------------------------------------------------------------------------------------------------------------------- #