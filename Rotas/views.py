from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

def index(request):
  return render(request, "index.html")

def teste(request):
	user = request.GET.get('user')
	data = {
		'is_run' : user *2;
	}
	return JsonResponse(data)