from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^search/$', views.search, name='search'),
    url(r'^poll_state/', views.poll_state, name="poll_state"),
]
