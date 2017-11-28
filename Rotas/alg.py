#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from math import radians,cos,sin,atan2,sqrt,degrees,asin
from py2neo import Graph,authenticate
import networkx as nx
from subprocess import call
from coordinates import get_bounding_box

def distancia(lon1, lat1, lon2, lat2):
    #Converte de Decimal para Radianos
    lon1, lat1, lon2, lat2 = map(radians, [float(lon1), float(lat1), float(lon2), float(lat2)])
    # Formula Haversine
    raio_terra = 6371
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    m = raio_terra * c * 1000
    return m  
def getBoundingBox(pLatitude, pLongitude, pDistanceInMeters):
        boundingBox = []
        latRadian = radians(pLatitude)
        degLatKm = 110.574235
        degLongKm = 110.572833 * cos(latRadian)
        deltaLat = pDistanceInMeters / 1000.0 / degLatKm
        deltaLong = pDistanceInMeters / 1000.0 / degLongKm
        minLat = pLatitude - deltaLat
        minLong = pLongitude - deltaLong
        maxLat = pLatitude + deltaLat
        maxLong = pLongitude + deltaLong
        boundingBox.append(minLat)
        boundingBox.append(minLong)
        boundingBox.append(maxLat)
        boundingBox.append(maxLong)
        return boundingBox
def midPoint(lat1,lon1,lat2,lon2):
        dLon = radians(lon2 - lon1)
        mid = []
        #convert to radians
        lat1 = radians(lat1)
        lat2 = radians(lat2)
        lon1 = radians(lon1)
        Bx = cos(lat2) * cos(dLon)
        By = cos(lat2) * sin(dLon)
        lat3 = atan2(sin(lat1) + sin(lat2), sqrt((cos(lat1) + Bx) * (cos(lat1) + Bx) + By * By))
        lon3 = lon1 + atan2(By, cos(lat1) + Bx)
        mid.append(degrees(lat3))
        mid.append(degrees(lon3))
        return mid

file = '/var/lib/neo4j/data/bbox.graphml'
def nearest_node(G,lat,lon):
    menor = 9999
    menor_node = 0 
    for i in G.nodes():
        dist_node = distancia(lat, lon, G.node[i]['Lat'], G.node[i]['Long'])
        if(float(dist_node) < float(menor)):
            menor = dist_node
            menor_node = i
    return menor_node


def get_dijkstra_path(minLat, minLon ,maxLat, maxLon):
    mid = midPoint(minLat,minLon,maxLat,maxLon)
    bbox = getBoundingBox(mid[0],mid[1],10000)
    get_bounding_box(bbox[2],bbox[3],bbox[0],bbox[1])
    G = nx.read_graphml(file)
    start_node = nearest_node(G,minLat,minLon)
    end_node = nearest_node(G,maxLat,maxLon)
    return_list = []
    SP = nx.dijkstra_path(G,start_node, end_node, weight='Weight')
    for i in SP:
        return_list.append([float(G.node[i]['Long']),float(G.node[i]['Lat'])])
        #return_list.append({float(nodeAux[1]), float(nodeAux[0])})
    return return_list

def get_astar_path(minLat, minLon ,maxLat, maxLon):
    mid = midPoint(minLat,minLon,maxLat,maxLon)
    bbox = getBoundingBox(mid[0],mid[1],10000)
    get_bounding_box(bbox[2],bbox[3],bbox[0],bbox[1])
    G = nx.read_graphml(file)
    start_node = nearest_node(G,minLat,minLon)
    end_node = nearest_node(G,maxLat,maxLon)
    return_list = []
    SP = nx.astar_path(G,start_node, end_node, weight='Weight')
    for i in SP:
        return_list.append([float(G.node[i]['Long']),float(G.node[i]['Lat'])])
        #return_list.append({float(nodeAux[1]), float(nodeAux[0])})
    return return_list
