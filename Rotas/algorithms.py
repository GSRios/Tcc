from neo4j.v1 import GraphDatabase, basic_auth


def get_dijkstra(minLat, minLon, maxLat, maxLon):
    
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth("neo4j", "tccneo4j2017"))
    session = driver.session()
    ret = []
    query = 'MATCH (start:Node) MATCH (end:Node),p = shortestPath((start)-[*..]-(end)) WHERE start.Long = \'%s\' and start.Lat = \'%s\' and end.Long = \'%s\' and end.Lat = \'%s\' with nodes(p) as no RETURN no' %(minLon, minLat, maxLon,maxLat)
    #query = 'MATCH (start:Node) MATCH (end:Node),p = shortestPath((start)-[*..1000000]-(end)) WHERE start.Long = \'-43.5398174\' and start.Lat = \'-22.8088785\' and end.Long = \'-43.5398146\' and end.Lat = \'-22.8087\' RETURN p AS PATH'
    result = session.run(query)
    for record in result:
        for i in record['no']:
            ret.append([float(i['Long']), float(i['Lat'])])
    return ret
