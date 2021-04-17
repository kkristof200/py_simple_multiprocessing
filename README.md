# simple_multiprocessing

![PyPI - package version](https://img.shields.io/pypi/v/simple_multiprocessing?logo=pypi&style=flat-square)
![PyPI - license](https://img.shields.io/pypi/l/simple_multiprocessing?label=package%20license&style=flat-square)
![PyPI - python version](https://img.shields.io/pypi/pyversions/simple_multiprocessing?logo=pypi&style=flat-square)
![PyPI - downloads](https://img.shields.io/pypi/dm/simple_multiprocessing?logo=pypi&style=flat-square)

![GitHub - last commit](https://img.shields.io/github/last-commit/kkristof200/py_simple_multiprocessing?style=flat-square)
![GitHub - commit activity](https://img.shields.io/github/commit-activity/m/kkristof200/py_simple_multiprocessing?style=flat-square)

![GitHub - code size in bytes](https://img.shields.io/github/languages/code-size/kkristof200/py_simple_multiprocessing?style=flat-square)
![GitHub - repo size](https://img.shields.io/github/repo-size/kkristof200/py_simple_multiprocessing?style=flat-square)
![GitHub - lines of code](https://img.shields.io/tokei/lines/github/kkristof200/py_simple_multiprocessing?style=flat-square)

![GitHub - license](https://img.shields.io/github/license/kkristof200/py_simple_multiprocessing?label=repo%20license&style=flat-square)

## Description

Execute multiple async tasks (via multiprocessing.Process, or threading.Thread) as simple as possible.

## Install

~~~~bash
pip install simple_multiprocessing
# or
pip3 install simple_multiprocessing
~~~~

## Usage

~~~~python
from simple_multiprocessing import MultiThread, MultiProcess, Task
import random, time

def test_func(i: int) -> float:
    print('started:', i)

    start = time.time()
    start / i

    if random.random() < 0.5:
        while True:
            time.sleep(0.01)

    res = time.time() - start

    return res

tasks = [Task(test_func, i) for i in range(5)]

# via threading
results_via_threading = MultiThread(tasks).solve(timeout=1)

for i, r in enumerate(results_via_threading):
    print(i, type(r), r)

# via Multiproccess
results_via_multiprocess = MultiProcess(tasks).solve(timeout=1)

for i, r in enumerate(results_via_multiprocess):
    print(i, type(r), r)
~~~~

## Dependencies

[noraise](https://pypi.org/project/noraise), [stopit](https://pypi.org/project/stopit)