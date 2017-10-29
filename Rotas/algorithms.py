from py2neo import Graph,authenticate


def get_dijkstra(minLat, minLon, maxLat, maxLon):
    # set up authentication parameters
    authenticate("localhost:7474", "neo4j", "tccneo4j2017")
    # connect to authenticated graph database
    graph = Graph("http://localhost:7474/db/data/")
    query = 'MATCH (from:Node) WHERE from.Lat = \'%s\' AND from.Long = \'%s\'MATCH (to:Node) WHERE to.Lat = \'%s\' AND to.Long = \'%s\'CALL apoc.algo.dijkstra(from, to, \'LINKED_TO\', \'Weight\') yield path as path, weight as weight RETURN path, weight' % (minLat, maxLat, minLon, maxLon)
    ret = graph.run(query)
    return ret
    