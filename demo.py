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