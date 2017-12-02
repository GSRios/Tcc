#!/bin/bash
START="$(date +%s)"

echo "Stopping Neo4j service..."
systemctl stop neo4j

echo "Deleting current database..."
rm -rf /var/lib/neo4j/data/databases/graph.db/*
chmod 777 -R /var/lib/neo4j/data/databases/graph.db/

echo "Generating nodes and relationships files..."
python ibmxml.py -o /var/lib/neo4j/data/rio-de-janeiro_brazil.osm --nodes /var/lib/neo4j/data/ts-no.csv --relationships /var/lib/neo4j/data/ts-rel.csv

echo "Sorting nodes file..."
sort -t , -k 1,1 ts-no.csv > sorted_no.csv

echo "Sorting relationships file..."
sort -u ts-rel.csv > sorted_rel.csv

echo "Spliting relationships file..."
awk -F"," '{print $1}' sorted_rel.csv > start_rel.csv
awk -F"," '{print $2}' sorted_rel.csv > end_rel.csv

echo "Adding index to relationships files..."
awk -F',' -v OFS=',' 'NR == 1 {$0;}{print (NR), $0}' start_rel.csv > indexed_start_rel.csv
awk -F',' -v OFS=',' 'NR == 1 {$0;}{print (NR), $0}' end_rel.csv > indexed_end_rel.csv

echo "Sorting relationships files on Node ID..."
sort -t , -k 2,2 indexed_start_rel.csv > sorted_start.csv
sort -t , -k 2,2 indexed_end_rel.csv > sorted_end.csv

echo "Joining relationships to nodes file..."
join -t , -1 2 -2 1 sorted_start.csv sorted_no.csv > final_start.csv
join -t , -1 2 -2 1 sorted_end.csv sorted_no.csv > final_end.csv

echo "Adding header to nodes file..."
sed -i $'1 i\\\nID:ID,Lat,Long' sorted_no.csv

echo "Sorting relationships files on Index..."
sort -t , -k 2,2 final_start.csv > sorted_final_start.csv
sort -t , -k 2,2 final_end.csv > sorted_final_end.csv

echo "Pasting files together..."
paste -d "," sorted_final_start.csv sorted_final_end.csv > joined.csv

echo "Calculating weight..."
python calcWeight.py

echo "Importing to Neo4j database..."
/usr/share/neo4j/bin/neo4j-import --into /var/lib/neo4j/data/databases/graph.db --nodes:Node /var/lib/neo4j/data/sorted_no.csv --relationships /var/lib/neo4j/data/final_rel.csv
chmod 777 -R /var/lib/neo4j/data/databases/graph.db/

echo "Removing temp files..."
rm -f sorted_rel.csv start_rel.csv end_rel.csv indexed_start_rel.csv indexed_end_rel.csv sorted_start.csv sorted_end.csv final_start.csv final_end.csv sorted_final_start.csv sorted_final_end.csv joined.csv ts-no.csv ts-rel.csv sorted_no.csv final_rel.csv

echo "Starting Neo4j Service..."
systemctl start neo4j

END="$(date +%s)"

RUNTIME="$((END-START))"

echo "Done in ${RUNTIME} seconds"
