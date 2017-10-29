# coding=utf-8
from urllib2 import urlopen
import json
from py2neo import Graph,authenticate
import call

url = "http://nominatim.openstreetmap.org/search?format=json&limit=1&q="
def get_coordinate_from_address(address, count):
    listr = []
    address = str(address).replace(' ', "+")
    ret = urlopen(('%s%s') % (url, address))
    listr= json.loads(ret.read())
    print len(listr) < 1
    if len(listr) < 1:
        print 'passei aqui'
        raise ValueError(('Os dados do endereco %d estão incorretos') %(count+1))

    return (listr[0]['lon'], listr[0]['lat'])



def get_bounding_box(minLat, minLon, maxLat, maxLon):
    # set up authentication parameters
    authenticate("localhost:7474", "neo4j", "tccneo4j2017")
    # connect to authenticated graph database
    graph = Graph("http://localhost:7474/db/data/")    
    file = '/var/lib/neo4j/data/bbox.graphml'
    query = 'call apoc.export.graphml.query("match (n:Node)-[r:LINKED_TO]->() where (n.Lat >= \'%s\' AND n.Lat <= \'%s\') AND (n.Long >= \'%s\' AND n.Long <= \'%s\') return n,r","%s",{})' % (minLat, maxLat, minLon, maxLon,file)
    graph.run(query)
    #Fixes the graphml file adding label keys to Nodes and Edges
    insert_node_label = "sed -i '/<graphml xmlns/ a\<key id=\"labels\" for=\"node\" attr.name=\"labels\" attr.type=\"string\"\/>' %s" % (file)
    insert_edge_label = "sed -i '/<graphml xmlns/ a\<key id=\"label\" for=\"edge\" attr.name=\"label\" attr.type=\"string\"\/>' %s" % (file)
    call(insert_node_label, shell=True)
    call(insert_edge_label, shell=True)