__author__ = 'kuddai'
#it is expected that local database is working here
import urllib, json
url = "http://maps.googleapis.com/maps/api/geocode/json?address=googleplex&sensor=false"
response = urllib.urlopen(url)
data = json.loads(response.read())
print data