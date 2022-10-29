from __future__ import annotations

from typing import Any, Callable

import redis
from django_q.brokers.redis_broker import Redis


# start with redis. then build out. will default to using
# whatever broker is configured but should probably have option
# to use something else.
class RedisBackend:
    """
    Store queue task stats in redis
    """
    # TODO: move this elsewhere

    def __init__(self, broker: Redis):
        # may change to just taking connection directly
        self.broker = broker
        self.connection: redis.Redis | redis.StrictRedis = broker.get_connection()

        # TODO: make this configurable
        self.key_prefix = 'django_q_view'

    def add_to_queued(self, task: dict[str, Any]):
        task_data = dict(task)
        task_data['func'] = str(task['func'])
        self.connection.hset(f'{self.key_prefix}:queued'. task['id'], task_data)

    def move_to_executing(self, func: Callable, task: dict[str, Any]):
        task_data = self.connection.hget(f'{self.key_prefix}:queued', task['id'])
        self.connection.hset(f'{self.key_prefix}:executing'. task['id'], task_data)

    def remove_from_backend(self, task: dict[str, Any]):
        self.connection.hdel(f'{self.key_prefix}:executing'. task['id'])
