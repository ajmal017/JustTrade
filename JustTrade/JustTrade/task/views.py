from django.shortcuts import get_object_or_404, render
from .models import tradingTask
from script import main
# Create your views here.


def Trade(request,strategy_id):
    param = request.POST

    if len(param) == 0:
        param = json.loads(request.body)


    task = get_object_or_404(tradingTask,pk = strategy_id)

    # need to fix
    main(task.real_time_index,task.symbol,task.strategy)
    # need to fix
    return render(request, 'polls/detail.html', {'question': question})


def show_tasks(request):

    param = request.POST

    if len(param) == 0:
        param = json.loads(request.body)

    tasks = tradingTask.objects.all()

    return render(request,'template/pick_strategy.html',tasks)
