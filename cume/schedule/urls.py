from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^schedule/', views.schedule, name="schedule"),
    url(r'^logout/', views.logoutUser, name="logout"),
    url(r'^class_add/', views.class_add, name="class_add"),
    url(r'^class_delete/', views.class_delete, name="class_delete"),
]
