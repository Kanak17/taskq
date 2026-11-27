import pytest
import redis

TEST_QUEUE = "taskq:test:queue"


@pytest.fixture
def redis_client():
    client = redis.Redis(host="localhost", port=6379, decode_responses=True)
    try:
        client.ping()
    except redis.ConnectionError:
        pytest.skip("Redis is not running on localhost:6379")
    client.delete(TEST_QUEUE)
    yield client
    client.delete(TEST_QUEUE)
    client.close()