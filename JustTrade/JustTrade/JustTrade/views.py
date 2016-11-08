from django.shortcuts import render


def landing_view(request):
	return render(request, 'landing.html')


def index_view(request):
	return render(request, 'index.html')
