from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import json
from django.views.decorators.csrf import csrf_exempt
import graphdijkstra as graph
import os
from django.conf import settings
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

	print coords[0][0]
	data = {
		'lista' : graph.get_dijkstra_path(float(coords[0][0]),float(coords[0][1]), float(coords[1][0]), float(coords[1][1]))
	}
	return JsonResponse(data)

@csrf_exempt
def download(request):
	#teste inversao
	#minLat = request.POST.get('minLat')
	#minLon = request.POST.get('minLon')
	#maxLat = request.POST.get('maxLat')
	#maxLon = request.POST.get('maxLon')
	#teste inversao
	maxLat = request.POST.get('minLat')
	maxLon = request.POST.get('minLon')
	minLat = request.POST.get('maxLat')
	minLon = request.POST.get('maxLon')
	coordinates.get_bounding_box(minLat,minLon, maxLat, maxLon)
	path = '/var/lib/neo4j/data/bbox.graphml'
	file_path = os.path.join(settings.MEDIA_ROOT, path)
	if os.path.exists(file_path):
			with open(file_path, 'rb') as fh:
					print 'to aqui'
					response = HttpResponse(fh.read(), content_type="application/graphml")
					response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
					return response
