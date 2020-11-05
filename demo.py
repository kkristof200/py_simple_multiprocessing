from simple_multiprocessing import MultiProcess, Task
import random, time

def test(i: int) -> float:
    print('started:', i)
    start = time.time()

    if random.random() < 0.5:
        while True:
            time.sleep(0.01)

    return time.time() - start

tasks = [Task(test, i) for i in range(5)]
results = MultiProcess(tasks).solve(timeout=1)

[print(i, type(r), r) for i, r in enumerate(results)]