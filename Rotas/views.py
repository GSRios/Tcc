from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import json
from django.views.decorators.csrf import csrf_exempt

def index(request):
  return render(request, "index.html")

@csrf_exempt
def teste(request):
	user = json.loads(request.POST.get('user'))
	data = {
		'lista' : user
	}
	return JsonResponse(data)