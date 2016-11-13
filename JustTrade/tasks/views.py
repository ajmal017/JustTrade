import json
from django.shortcuts import get_object_or_404, render
from .models import tradingTask,tradeLog
from scripts import main
import json
import subprocess
from django.http import HttpRequest,JsonResponse
from multiprocessing import Pool
from scripts import main


# Create your views here.


# Page 2 View Controller
def trade(request,pk):
    #if request.is_ajax:

    task = get_object_or_404(tradingTask,pk=pk)
    subprocess.Popen(['python', 'manage.py', 'runscript', 'main','--script-args=1'])

    return render(request, 'detail.html', {'task': task})


def backtest(request,pk):
	task = get_object_or_404(tradingTask,pk=pk)
	result = main.Execute(pk,realtimeindex = False)
	subset = result[['datetime', 'equity_curve', 'total']]
	tuples = [tuple(x) for x in subset.values]
	return render(request,'',{'task' = task,'tuples':tuples})


# Page 3 View Controller
def present_trading(request,pk):

    task = get_object_or_404(tradingTask,pk = pk)
    logs = tradeLog.objects.filter(trade_task = task)
    
    return JsonResponse({'logs':[logs[0].log_type,logs[0].log_info]})


def show_tasks(request):
    tasks = tradingTask.objects.all()

    return render(request, 'tasks/task_list.html', {'tasks': tasks})

