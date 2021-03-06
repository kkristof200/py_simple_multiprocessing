# ------------------------------------------------------------ Imports ----------------------------------------------------------- #

# System
from multiprocessing import Process

# Local
from ._multi_task import _MultiTask

# -------------------------------------------------------------------------------------------------------------------------------- #



# ------------------------------------------------------ class: MultiProcess ----------------------------------------------------- #

class MultiProcess(_MultiTask):

    def _proc_cls(self) -> type:
        return Process


# -------------------------------------------------------------------------------------------------------------------------------- #