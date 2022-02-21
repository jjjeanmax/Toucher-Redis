import random

from redis_queue import RedisQueue, worker
from redis import Redis

broker = Redis(host="localhost", db=0)
result_backend = Redis(host="localhost", db=1)
redis_queue = RedisQueue(broker, result_backend, "default")


def task(start: int, end: int):
    """definir un task et excecuter de maniere asynchron"""
    return random.randint(start, end)


# Excecuter 10 task
for start, end in zip(range(10), range(100, 1000, 100)):
    redis_queue.enattente(task, start, end)

worker(redis_queue)
