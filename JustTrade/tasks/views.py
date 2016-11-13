from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect

from .models import tradingTask, tradeLog
from scripts import main

import subprocess
from multiprocessing import Pool

import json


# Page 2 View Controller
def task_detail_view(request, pk):
	task = get_object_or_404(tradingTask, pk=pk)
	if task.is_active:
		subprocess.Popen(['python', 'manage.py', 'runscript', 'main', '--script-args=1'])
	return render(request, 'detail.html', {'task': task})


def task_switch_api(request, pk):
	task = get_object_or_404(tradingTask, pk=pk)
	if task.is_active:
		task.is_active = False
		task.save()
	else:
		task.is_active = True
		task.save()

	return HttpResponseRedirect('/task/trade/' + pk)


# for NLP Trading
def IBM_trade_view(request, pk):
	task = get_object_or_404(tradingTask, pk=pk)
	symbol_to_name = {'GOOG': 'Google', 'APPL': 'Apple', "TSLA": 'Tesla', 'BABA': 'Alibaba'}
	name = symbol_to_name[task.symbol.name]
	urls, result = main.Execute(pk, realtimeindex=False, NPL=True, symbol_list=[name])
	return render(request, '', {"task": task, "urls": urls, "result": result})


# Page 3 View Controller
def task_log_api(request, pk):
	task = get_object_or_404(tradingTask, pk=pk)
	logs = tradeLog.objects.filter(trade_task=task).order_by('-log_time')[0:11]
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
	return render(request, 'backtest.html', {'task': task})


def backtest_api(request, pk):
	result = main.Execute(pk, realtimeindex=False, waiting_time=0)
	subset = result[['equity_curve']]
	a = subset.to_records(index=True)
	tuples = [[x[0].strftime("%Y-%m-%d %H:%M:%S"), x[1]] for x in a]
	json_return = []
	json_return.append({'equity_curve': tuples})
	return HttpResponse(json_return, content_type='application/json')
