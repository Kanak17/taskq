import json

from conftest import TEST_QUEUE


def test_json_job_round_trips(redis_client):
    job = {"task": "add", "args": [2, 3], "kwargs": {}}
    redis_client.lpush(TEST_QUEUE, json.dumps(job))

    assert redis_client.llen(TEST_QUEUE) == 1
    raw = redis_client.rpop(TEST_QUEUE)
    assert json.loads(raw) == job
    assert redis_client.rpop(TEST_QUEUE) is None