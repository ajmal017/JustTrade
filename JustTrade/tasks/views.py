from django.shortcuts import get_object_or_404, render
from .models import tradingTask
from scripts import main
import json
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

    param = request.POST

    if len(param) == 0:
        try:

            param = json.loads(request.body)

        except:

            pass

    tasks = tradingTask.objects.all()

    return render(request,'pick_strategy.html',{'tasks':tasks})
