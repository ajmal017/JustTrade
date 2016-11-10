import json
from django.shortcuts import get_object_or_404, render
from .models import tradingTask,tradeLog
from scripts import main
import json
import subprocess
from django.http import HttpRequest



# Create your views here.


# Page 2 View Controller
def Trade(request,pk):
    #if request.is_ajax:

    task = get_object_or_404(tradingTask,pk = pk)

    subprocess.Popen(['python', 'manage.py', 'runscript', 'main'])
    
       
    #else:
    #    return HttpRequest(status=400)


# Page 3 View Controller
def present_trading(request,strategy_id):

    task = get_object_or_404(tradingTask,pk = strategy_id)
    logs = tradeLog.objects.filter(trade_task = task)


    return logs[0:5]


def show_tasks(request):
    tasks = tradingTask.objects.all()

    return render(request, 'tasks/task_list.html', {'tasks': tasks})

