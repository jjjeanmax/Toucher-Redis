import logging
import multiprocessing
import pickle
import time

from redis.client import Redis

from FIFO.redis_queue import RedisQueue


class Lifo(RedisQueue):
    def __init__(self, broker: Redis, resultat_backend: Redis, nom_queue: str):
        super().__init__(broker, resultat_backend, nom_queue)

    def enexcecution(self):
        rk = 'lifo'
        # Obtenir le Task de Redis (dernier venue premier sorti -->rpop)
        serializer_task = self.broker.rpop(self.nom_queue)
        try:
            task = pickle.loads(serializer_task)
            logging.info(f"Task ID: {task.id}, Args: {task.args}, Kwargs: {task.kwargs}")

            # excecution du task
            resultat = task.process_task()

            # enregistrer le resultat dans redis key:value
            self.resultat_backend.set(f"{rk}_{task.id}", resultat)
            logging.info("Fin du Task")

        except TypeError as e:
            logging.info(e)


def worker_lifo(queue: Lifo, max_worker: int = 4):
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
            # Pour le parallelisme
            p = multiprocessing.Process(target=_excecuter_task, args=(queue,))
            processes.append(p)
            p.start()
            time.sleep(5)
        for p in processes:
            p.join()
