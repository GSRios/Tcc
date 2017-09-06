from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

def index(request):
  return render(request, "index.html")

def teste(request):
	user = request.GET.get('user')
	data = {
		'lon' : user.split(",")[0],
		'lat' : user.split(",")[1]
	}
	return JsonResponse(data)