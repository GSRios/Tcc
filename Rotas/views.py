from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import json
from django.views.decorators.csrf import csrf_exempt
import graphdijkstra as graph

def index(request):
  return render(request, "index.html")

@csrf_exempt
def teste(request):

	coord = json.loads(request.POST.get('coordinate'))	
	data = {
		'lista' : graph.get_dijkstra_path(float(coord[0].split(",")[0]),float(coord[0].split(",")[1]), float(coord[1].split(",")[0]), float(coord[1].split(",")[1]))
	}
	return JsonResponse(data)