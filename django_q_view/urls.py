from django_q_view.views import DjangoQBrokerData
from django.urls import path

app_name = "django_q_view"
urlpatterns = [
    path("broker/", DjangoQBrokerData.as_view(), name="broker"),
]
