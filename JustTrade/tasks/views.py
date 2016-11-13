from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse

from .models import tradingTask, tradeLog
from scripts import main

import subprocess
from multiprocessing import Pool

import json

# Page 2 View Controller
def trade(request, pk):
	task = get_object_or_404(tradingTask, pk=pk)
	subprocess.Popen(['python', 'manage.py', 'runscript', 'main', '--script-args=1'])

	return render(request, 'detail.html', {'task': task})


def backtest(request, pk):
	task = get_object_or_404(tradingTask, pk=pk)
	result = main.Execute(pk, realtimeindex=False)
	subset = result[['datetime', 'equity_curve', 'total']]
	tuples = [tuple(x) for x in subset.values]
	return render(request, '', {'task': task, 'tuples': tuples})


# Page 3 View Controller
def present_trading(request, pk):
	task = get_object_or_404(tradingTask, pk=pk)
	logs = tradeLog.objects.filter(trade_task=task).reverse()[0:10]
	json_return = []

	for log in logs:
		json_return.append({'log_time': log.log_time.strftime("%Y-%m-%d %H:%M:%S"),
		                    'trade_task': log.trade_task.pk,
		                    'log_type': log.log_type,
		                    'log_info': json.loads(log.log_info)})
	json_return = json.dumps(json_return)

	return HttpResponse(json_return, content_type='application/json')


# backtest view
def backtest_view(request, pk):
	task = get_object_or_404(tradingTask, pk=pk)
	subprocess.Popen(['python', 'manage.py', 'runscript', 'main', '--script-args=1'])

	return render(request, 'backtest.html', {'task': task})

# all tasks listed in index page
# def show_tasks(request):
#     tasks = tradingTask.objects.all()
#
#     return render(request, 'index.html', {'tasks': tasks})
