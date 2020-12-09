from simple_multiprocessing import MultiThread, MultiProcess, Task
import random, time

def test(i: int) -> float:
    print('started:', i)
    start = time.time()

    if random.random() < 0.5:
        while True:
            time.sleep(0.01)

    res = time.time() - start
    return res#time.time() - start

tasks = [Task(test, i) for i in range(5)]

[print(i, type(r), r) for i, r in enumerate(MultiThread(tasks).solve(timeout=1))]
[print(i, type(r), r) for i, r in enumerate(MultiProcess(tasks).solve(timeout=1))]