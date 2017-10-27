from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import json
from django.views.decorators.csrf import csrf_exempt
import graphdijkstra as graph
import coordinates

def index(request):
  return render(request, "index.html")

@csrf_exempt
def teste(request):

	coordView = json.loads(request.POST.get('coordinate'))
	coords = []
	try:
		for idx, x in enumerate(coordView):
			coords.append(coordinates.get_coordinate_from_address(x, idx)) 			
	except ValueError as error:
		return JsonResponse(data={'message': error.message}, status=500)

	print coords
	data = {
		'lista' : graph.get_dijkstra_path(float(coords[0][0]),float(coords[0][1]), float(coords[1][0]), float(coords[1][1]))
	}
	return JsonResponse(data)