import csv
from math import radians, cos, sin, asin, sqrt

file = "/var/lib/neo4j/data/joined.csv"
final_rel = "/var/lib/neo4j/data/final_rel.csv"

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

with open(file, 'r') as file, open(final_rel,'w') as out:
    reader = csv.reader(file, delimiter=',')
    out.write(":START_ID,Weight,:END_ID,:TYPE\n")
    for row in reader:
        weight = distancia(float(row[3]),float(row[2]),float(row[7]),float(row[6]))
        out.write(("%s,%.2f,%s,%s\n") % (row[0],float(weight),row[4],"LINKED_TO"))