import functools
import json
import uuid

import redis

QUEUE_KEY = "taskq:queue:default"

_registry: dict[str, "Task"] = {}


def get_redis() -> redis.Redis:
    return redis.Redis(host="localhost", port=6379, decode_responses=True)


class Task:
    def __init__(self, func):
        self.func = func
        self.name = f"{func.__module__}.{func.__qualname__}"
        functools.update_wrapper(self, func)
        _registry[self.name] = self

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    def delay(self, *args, **kwargs) -> str:
        job = {
            "id": str(uuid.uuid4()),
            "task": self.name,
            "args": list(args),
            "kwargs": kwargs,
        }
        payload = json.dumps(job)
        get_redis().lpush(QUEUE_KEY, payload)
        return job["id"]


def task(func):
    return Task(func)