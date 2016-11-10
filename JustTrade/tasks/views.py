import json
from django.shortcuts import get_object_or_404, render
from django.http import HttpRequest

from .models import tradingTask
from scripts import main
# Create your views here.


def Trade(request,strategy_id):
    if request.is_ajax:

        task = get_object_or_404(tradingTask,pk = strategy_id)

        # need to fix
        main(task.real_time_index,task.symbol,task.strategy)
       
    else:
        return HttpRequest(status=400)


def present_trading(request):

    return


def show_tasks(request):
    tasks = tradingTask.objects.all()
    return render(request, 'tasks/task_list.html', {'tasks': tasks})
