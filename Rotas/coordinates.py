# coding=utf-8
from urllib2 import urlopen
import json

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