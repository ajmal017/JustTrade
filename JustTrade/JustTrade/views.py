from django.shortcuts import render
 
from tasks.models import tradingTask

def landing_view(request):
	return render(request, 'landing.html')
 
 
def index_view(request):
	tasks = tradingTask.objects.all()
	return render(request, 'index.html',  {'tasks': tasks})

