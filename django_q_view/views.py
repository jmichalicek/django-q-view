from __future__ import annotations

from typing import Any

from django.conf import settings
from django.utils import timezone
from django.views.generic import TemplateView

from django_q import VERSION, models
from django_q.brokers import Broker, get_broker
from django_q.conf import Conf
from django_q.status import Stat


class DjangoQBrokerData(TemplateView):
    """
    Data and stats for a broker
    """
    template_name = "django_q_view/q_view.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        broker: Broker = self.get_broker()
        clusters: list[dict[str, Any]] = self.get_broker_cluster_info(broker=broker)
        return super().get_context_data(broker=broker, queue_name=Conf.PREFIX, clusters=clusters, **kwargs)

    def get_broker(self) -> Broker:
        return get_broker()

    def get_broker_cluster_info(self, broker: Broker) -> list[dict[str, Any]]:
        stats: list[Stat] = Stat.get_all(broker=broker)
        clusters: list(dict[str, Any]) = []
        # get the broker host/ip/etc from broker.connection?
        for cluster_stats in stats:
            # for each instance of manage.py qcluster on the same queue there will be a Stat object here
            stats_dict = {
                "cluster_id": cluster_stats.cluster_id,
                "status": cluster_stats.status,
                "host": cluster_stats.host,
                "pid": cluster_stats.pid,
                #"uptime": cluster_stats.uptime(),  this is just seconds as a float
                "queue_size": cluster_stats.task_q_size,
                "total_results": cluster_stats.done_q_size,
                "uptime": timezone.now() - cluster_stats.tob,  # uptime as a timedelta
                "worker_count": len(cluster_stats.workers),
                # goes on the broker"lock_size":
            }
            clusters.append(stats_dict)

        return clusters
