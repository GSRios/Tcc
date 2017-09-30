"""Defines a function that parses a Networkx graph and produces a Cypher query to store the graph in a Neo4j graph database
Athanasios Anastasiou 28/07/2013
"""

import random

#Simple character lists
letDCT = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
numDCT = "0123456789"

def getRndTag(someLen, dct=letDCT):
    """Returns some random string of length someLen composed of the characters in the dct string"""
    return "".join([dct[random.randint(0,len(dct)-1)] for i in range(0,someLen)])
    
def graph2Cypher(aGraph):
    """Generates a Cypher query from a Networkx Graph"""
    nodeStatements = {}
    edgeStatements = []
    
    #Partially generate the node representations
    for aNode in G.nodes(data = True):
        #Generate a node identifier for Cypher
        varName = getRndTag(2)+getRndTag(2,dct=numDCT)
        #Append the node's ID attribute so that the node-ID information used by Networkx is preserved.
        nodeItems = [("ID","%s" % aNode[0])]
        nodeItems.extend(aNode[1].items())
        #Create the key-value representation of the node's attributes taking care to add quotes when the value is of type string        
        nodeAttributes = "{%s}" % ",".join(map(lambda x:"%s:%s" %(x[0],x[1]) if not type(x[1])==str else "%s:'%s'" %(x[0],x[1]) ,nodeItems))
        #Store it to a dictionary indexed by the node-id.
        nodeStatements[aNode[0]] = [varName, "(%s %s)" % (varName, nodeAttributes)]
        
    #Generate the relationship representations
    for anEdge in G.edges(data = True):
        edgeItems = anEdge[2].items()
        edgeAttributes = ""
        if len(edgeItems)>0:
            edgeAttributes = "{%s}" % ",".join(map(lambda x:"%s:%s" %(x[0],x[1]) if not type(x[1])==str else "%s:'%s'" %(x[0],x[1]) ,edgeItems))
        #NOTE: Declare the links by their Cypher node-identifier rather than their Networkx node identifier
        edgeStatements.append("(%s)-[:LINKED_TO %s]->(%s)" % (nodeStatements[anEdge[0]][0], edgeAttributes, nodeStatements[anEdge[1]][0]))
        
    #Put both definitions together and return the create statement.
    return "create %s,%s;\n" % (",".join(map(lambda x:x[1][1],nodeStatements.items())),",".join(edgeStatements))