from __future__ import annotations

import json
from typing import Any, TypedDict

from django.conf import settings
from django.utils import timezone
from django.views.generic import TemplateView

from django_q import VERSION, models
from django_q.brokers import Broker, get_broker
from django_q.conf import Conf
from django_q.humanhash import humanize
from django_q.status import Stat

from django_q_view import backends
from django_q_view.backends import RedisBackend


class QueueData(TemplateView):
    """
    Stats about a single queue on a broker
    """

    template_name = "django_q_view/q_view.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        broker: Broker = self.get_broker()
        queue_data: dict[str, Any] = self.get_broker_cluster_info(broker=broker)
        queued_tasks = self.get_queue_tasks(broker)
        executing_tasks = self.get_executing_tasks(broker)
        return super().get_context_data(
            broker=broker,
            queue_name=Conf.PREFIX,
            queue_data=queue_data,
            queued_tasks=queued_tasks,
            executing_tasks=executing_tasks,
            **kwargs,
        )

    def get_broker(self) -> Broker:
        return get_broker()

    def get_broker_cluster_info(self, broker: Broker) -> dict[str, Any]:
        stats: list[Stat] = Stat.get_all(broker=broker)
        clusters: list[dict[str, Any]] = []
        # get the broker host/ip/etc from broker.connection?
        data = {
            "total_results": 0,
            "queue_size": 0,
            "cluster_count": 0,
            "clusters": [],
        }
        for cluster_stats in stats:
            # for each instance of manage.py qcluster on the same queue there will be a Stat object here
            stats_dict = {
                "cluster_id": cluster_stats.cluster_id,
                "cluster_name": humanize(cluster_stats.cluster_id.hex),
                "status": cluster_stats.status,
                "host": cluster_stats.host,
                "pid": cluster_stats.pid,
                # "uptime": cluster_stats.uptime(),  this is just seconds as a float
                "queue_size": cluster_stats.task_q_size,
                "total_results": cluster_stats.done_q_size,
                "uptime": timezone.now() - cluster_stats.tob,  # uptime as a timedelta
                "worker_count": len(cluster_stats.workers),
                # goes on the broker"lock_size":
            }
            clusters.append(stats_dict)
            data["queue_size"] += stats_dict["queue_size"]
            data["total_results"] += stats_dict["total_results"]

        data["clusters"] = clusters
        data["cluster_count"] = len(data["clusters"])

        return data

    def get_queue_tasks(self, broker: Broker) -> dict[str, Any]:
        backend = RedisBackend(broker=broker)
        tasks = {}
        for k, v in backend.get_queued_tasks().items():
            tasks[k] = json.loads(v)
        return tasks

    def get_executing_tasks(self, broker: Broker) -> dict[str, Any]:
        backend = RedisBackend(broker=broker)
        tasks = {}
        for k, v in backend.get_executing_tasks().items():
            tasks[k.decode('utf-8')] = json.loads(v)
        return tasks
