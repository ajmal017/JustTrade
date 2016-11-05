from django.shortcuts import render
from .models import tradingTask
from script import main
# Create your views here.


def Trade(request):
	param = request.POST

	if len(param) == 0:
        param = json.loads(request.body)


    tasks = tradingTask.objects.all()

    for task in tasks:
    	if task.is_active:
    		main(task.real_time_index,task.symbol,task.strategy)



