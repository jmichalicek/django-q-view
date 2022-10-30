from __future__ import annotations

import json
from typing import Any, Callable

from django.core.serializers.json import DjangoJSONEncoder

import redis
from django_q.brokers.redis_broker import Redis

import logging

logger = logging.getLogger(__name__)

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
        self.queued_key = f'{self.key_prefix}:queued'
        self.executing_key = f'{self.key_prefix}:executing'

    def add_to_queued(self, task: dict[str, Any]) -> None:
        logger.debug('Adding task %s to queued dict', str(task))
        task_data = dict(task)
        task_data['func'] = str(task['func'])
        self.connection.hset(self.queued_key, task['id'], json.dumps(task_data, cls=DjangoJSONEncoder))

    def move_to_executing(self, func: Callable, task: dict[str, Any]) -> None:
        logger.debug('moving task %s to executing dict', str(task))
        task_data = self.connection.hget(self.queued_key, task['id'])
        self.connection.hset(self.executing_key, task['id'], task_data)
        self.connection.hdel(self.queued_key, task['id'])
        logger.debug('Removed task %s from queued dict', str(task))

    def remove_from_backend(self, task: dict[str, Any]) -> None:
        logger.debug('Removing task %s from executing dict', str(task))
        self.connection.hdel(self.executing_key, task['id'])
        logger.debug('Removed task %s from executing dict', str(task))

    def get_queued_tasks(self) -> list[dict[str, Any]]:
        return self.connection.hgetall(self.queued_key)

    def get_executing_tasks(self) -> list[dict[str, Any]]:
        return self.connection.hgetall(self.executing_key)
