import logging
import multiprocessing
import pickle
import time
import uuid
from typing import Any, Callable

from redis import Redis

logging.basicConfig(level=logging.INFO)


class SimpleTask:
    def __init__(self, func: Callable, *args: Any, **kwargs: Any):
        self.id = str(uuid.uuid4())
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def process_task(self):
        return self.func(*self.args, **self.kwargs)


class RedisQueue:
    def __init__(self, broker: Redis, resultat_backend: Redis, nom_queue: str):
        self.broker = broker
        self.resultat_backend = resultat_backend
        self.nom_queue = nom_queue

    def enattente(self, func: Callable, *args, **kwargs):
        # convertion en Task
        task = SimpleTask(func, *args, **kwargs)
        serializer_task = pickle.dumps(task, protocol=pickle.HIGHEST_PROTOCOL)

        # append le Task dans redis dans une list
        self.broker.rpush(self.nom_queue, serializer_task)
        return task.id

    def enexcecution(self):
        # obtenir le Task de Redis
        serializer_task = self.broker.lpop(self.nom_queue)
        try:
            task = pickle.loads(serializer_task)
            logging.info(f"Task ID: {task.id}, Args: {task.args}, Kwargs: {task.kwargs}")

            # excecution du task
            resultat = task.process_task()

            # enregistrer le resultat dans redis key:value
            self.resultat_backend.set(f"{task.id}", resultat)
            logging.info("Fin du Task")

        except TypeError as e:
            logging.info(e)

    def get_length(self):
        return self.broker.llen(self.nom_queue)


def worker(queue: RedisQueue, max_worker: int = 4):
    "imiter celery"

    def _excecuter_task(queue):
        if queue.get_length() > 0:
            queue.enexcecution()
        else:
            logging.info("Pas de Task en attente")

    processes = []
    logging.info(f"Excecution des Tasks avec {max_worker} processes!")
    while queue.get_length() != 0:
        for _ in range(max_worker):
            p = multiprocessing.Process(target=_excecuter_task, args=(queue,))
            processes.append(p)
            p.start()
            time.sleep(5)
        for p in processes:
            p.join()
