import json

import pytest

import taskq.app as app
from conftest import TEST_QUEUE
from taskq import task


@task
def add(a, b):
    """Add two numbers."""
    return a + b


def test_direct_call_still_works():
    assert add(2, 3) == 5


def test_wrapper_keeps_function_metadata():
    assert add.__name__ == "add"
    assert add.__doc__ == "Add two numbers."


def test_task_is_registered():
    assert app._registry[add.name] is add


def test_delay_pushes_json_job(redis_client, monkeypatch):
    monkeypatch.setattr(app, "QUEUE_KEY", TEST_QUEUE)
    job_id = add.delay(2, b=3)

    job = json.loads(redis_client.rpop(TEST_QUEUE))
    assert job == {"id": job_id, "task": add.name, "args": [2], "kwargs": {"b": 3}}


def test_delay_rejects_non_json_args(redis_client, monkeypatch):
    monkeypatch.setattr(app, "QUEUE_KEY", TEST_QUEUE)
    with pytest.raises(TypeError):
        add.delay({1, 2}, 3)
    assert redis_client.llen(TEST_QUEUE) == 0