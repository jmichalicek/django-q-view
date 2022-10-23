from django_q_view.views import QueueData
from django.urls import path

app_name = "django_q_view"
urlpatterns = [
    # this may eventually be queue/<queue_name>/
    # or broker/<broker_identifier>/queues/<queue_name>/
    # if a clean way of supporting multiple brokers and queues can be worked out
    path("queue/", QueueData.as_view(), name="queue-data"),
]
