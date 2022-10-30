from __future__ import annotations

from typing import Any, Callable

from django.dispatch import receiver

from django_q.brokers import get_broker
from django_q.signals import post_execute, pre_enqueue, pre_execute

from django_q_view.backends import RedisBackend


@receiver(pre_enqueue, sender="django_q", dispatch_uid="django_q_view_handle_pre_enqueue")
def handle_pre_enqueue(sender: str, task: dict[str, Any], **kwargs):
    broker = task.get("broker", get_broker())
    # TODO: logic to get the correct back end when the others are implemented
    backend = RedisBackend(broker=broker)
    backend.add_to_queued(task)


@receiver(pre_execute, sender="django_q", dispatch_uid="django_q_view_handle_pre_execute")
def handle_pre_execute(sender: str, func: Callable, task: dict[str, Any], **kwargs):
    broker = task.get("broker", get_broker())
    # TODO: logic to get the correct back end when the others are implemented
    backend = RedisBackend(broker=broker)
    backend.move_to_executing(func, task)


@receiver(post_execute, sender="django_q", dispatch_uid="django_q_view_handle_post_execute")
def handle_post_execute(sender: str, task: dict[str, Any], **kwargs):
    broker = task.get("broker", get_broker())
    # TODO: logic to get the correct back end when the others are implemented
    backend = RedisBackend(broker=broker)
    backend.remove_from_backend(task)
