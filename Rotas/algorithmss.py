from math import radians,cos,sin,atan2,sqrt,degrees,asin
from py2neo import Graph,authenticate
import networkx as nx
from subprocess import call
from coordinates import get_bounding_box


file = '/var/lib/neo4j/data/bbox.graphml' 

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


def nearest_node(G,lat,lon):
    menor = 9999
    for i in G.nodes():
        dist_node = distancia(lat, lon, G.node[i]['Lat'], G.node[i]['Long'])
        if(float(dist_node) < float(menor)):
            menor = dist_node
            menor_node = i
    return menor_node

def get_dijikstra_path(minLat, minLon ,maxLat, maxLon):
    get_bounding_box(maxLat, maxLon, minLat, minLon)
    G = nx.read_graphml(file)
    return_list = []
    start_node = nearest_node(G,minLat, minLon)
    end_node = nearest_node(G,maxLat, maxLon)
    SP = nx.dijkstra_path(G,start_node, end_node, weight='Weight')
    for i in SP:
        return_list.append([float(G.node[i]['Lat']),float(G.node[i]['Long'])])
        #return_list.append({float(nodeAux[1]), float(nodeAux[0])})
    return return_list


def get_a_start(minLat, minLon ,maxLat, maxLon):    
    get_bounding_box(maxLat, maxLon, minLat, minLon)
    G = nx.read_graphml(file)
    return_list = []
    start_node = nearest_node(G,minLat, minLon)
    end_node = nearest_node(G,maxLat, maxLon)
    SP = nx.astar_path(G,start_node, end_node, weight='Weight')
    for i in SP:
        return_list.append([float(G.node[i]['Lat']),float(G.node[i]['Long'])])
        #return_list.append({float(nodeAux[1]), float(nodeAux[0])})
    return return_list

