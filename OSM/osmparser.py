import xml.etree.cElementTree as ET
import argparse
import os.path
#from more_itertools import unique_everseen
from math import radians, cos, sin, asin, sqrt

def is_valid_file(parser, arg):
   if not os.path.exists(arg):
       parser.error("The file %s does not exist!" % arg)
   else:
       return open(arg, 'r')  # return an open file handle

def is_valid_path(parser, arg):
   if (os.path.exists(arg)):
       return open(arg, 'r+')
   elif (os.access(os.path.dirname(arg), os.W_OK)):
       return open(arg, 'w+')
   else:
       parser.error("The path %s is not valid!" % arg)

parser = argparse.ArgumentParser()
parser.add_argument("-o", "--osm", required=True, metavar="FILE", type=lambda x: is_valid_file(parser, x), help="Absolute Path to OSM File")
parser.add_argument("-n", "--nodes", metavar="FILE", required=True, type=lambda x: is_valid_path(parser, x), help="Absolute Path to output your nodes file")
parser.add_argument("-r", "--relationships", metavar="FILE", required=True, type=lambda x: is_valid_path(parser, x), help="Absolute Path to output your relationships file")
args = parser.parse_args()

def distancia(lon1, lat1, lon2, lat2):
    #Converte de Decimal para Radianos
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # Formula Haversine
    raio_terra = 6371
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    m = raio_terra * c * 1000
    return m
def xmlparse(mapname, restrict=False, excludeway=[], estrada=True):
   context = ET.iterparse(mapname, events=("start", "end"))
   event, root = context.next()
   node = args.nodes
   #node.write(("%s,%s,%s") % ("ID:ID","Lat","Long \n"))
   coords = {}
   def write_node(elem):
       osmid = elem.get("id")
       lat = elem.get("lat")
       lon = elem.get("lon")
       #coords[osmid] = [(lon, lat)]
       node.write(("%s,%s,%s\n") % (osmid, lat, lon))    

   rel = args.relationships
   #rel.write(":START_ID,:END_ID,:TYPE\n")
   def getNodes(nodes):
        for i in range(0,len(nodes)-1):
            #weight = distancia(float(coords[nodes[i]][0][0]),float(coords[nodes[i]][0][1]),float(coords[nodes[i+1]][0][0]),float(coords[nodes[i+1]][0][1]))
            rel.write (("%s,%s,%s\n") % (nodes[i],nodes[i+1],"LINKED_TO"))

   def write_relation(way):
       #for i in waydict:
       attributes = way[0]
       if estrada and 'highway' not in attributes:
           return
       getNodes(list(way[1]))
       if 'oneway' not in attributes and 'highway' in attributes and attributes['highway'] != 'motorway':
           getNodes(list(reversed(way[1])))
       elif 'oneway' in attributes and 'highway' in attributes and attributes['oneway'] != 'yes' and attributes['oneway'] != '-1' and  attributes['highway'] != 'motorway':
           getNodes(list(reversed(way[1])))

   
   def create_relation(elem):
       waydict = {}
       osmid = elem.get("id")
       attribs={}
       refs=[]
       for obj in elem:
           att = obj.attrib
           if "k" in att:
               key = att["k"]
               val = att["v"]
               attribs[key]=val
           if "ref" in att:
               refs.append(att["ref"])
       if restrict is False:
           waydict[osmid] = attribs, refs
       elif restrict in attribs and attribs[restrict] not in excludeway:
           waydict[osmid] = [attribs, refs]
       write_relation(waydict[osmid])

   for event, elem in context:
       if event == "end" and (elem.tag == "node" or elem.tag == "way"):
           if elem.tag == "way":
               create_relation(elem)
           else:
               write_node(elem)
       root.clear()
   
   rel.close()
   node.close()
xmlparse(args.osm)