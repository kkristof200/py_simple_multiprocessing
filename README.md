# simple_multiprocessing

![python_version](https://img.shields.io/static/v1?label=Python&message=3.5%20|%203.6%20|%203.7&color=blue) [![PyPI downloads/month](https://img.shields.io/pypi/dm/simple_multiprocessing?logo=pypi&logoColor=white)](https://pypi.python.org/pypi/simple_multiprocessing)

## Description

execute multiple async tasks (via multiprocessing.Process, or threadingThread) as simple as possible

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

def test(i: int) -> float:
    print('started:', i)
    start = time.time()
    start / i

    if random.random() < 0.5:
        while True:
            time.sleep(0.01)

    res = time.time() - start
    return res#time.time() - start

tasks = [Task(test, i) for i in range(5)]

[print(i, type(r), r) for i, r in enumerate(MultiThread(tasks).solve(timeout=1))]
[print(i, type(r), r) for i, r in enumerate(MultiProcess(tasks).solve(timeout=1))]
~~~~