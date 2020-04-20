from django.shortcuts import render, get_object_or_404
from  django.http import HttpResponse
from  .models import Task

# Create your views here.
def index(request):
    latest_tasks_list = Task.objects.order_by('-pub_date')[:5]
    context = {'latest_tasks_list' : latest_tasks_list}
    return render(request, 'daytasks/index.html', context)

def detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    return render(request, 'daytasks/detail.html', {'task': task})