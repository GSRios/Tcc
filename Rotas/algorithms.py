from py2neo import Graph,authenticate
import ast
import json


def get_dijkstra(minLat, minLon, maxLat, maxLon):
    # set up authentication parameters
    authenticate("localhost:7474", "neo4j", "tccneo4j2017")
    # connect to authenticated graph database
    graph = Graph("http://localhost:7474/db/data/")
    query = 'MATCH (start:Node) MATCH (end:Node), p = shortestPath((start)-[*..1000000]-(end)) WHERE start.Long = \'%s\' and start.Lat = \'%s\'and end.Long = \'%s\' and end.Lat = \'%s\' RETURN p' % (minLon, minLat, maxLon, maxLat)
    print query
    ret = graph.run(query)
    ast.literal_eval(json.dumps(ret.data()))
    return ast.literal_eval(json.dumps(ret.data()))
