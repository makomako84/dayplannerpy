from django.urls import path
from . import  views

urlpatterns = [
    # /daytasks/
    path('', views.index, name='index'),
    # /daytasks/n/
    path('<int:task_id>/', views.detail,name='detail')
]