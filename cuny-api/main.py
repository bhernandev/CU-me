import json
import urllib

BASE_URL = urllib.urlopen("http://107.170.2.38:3000/api/names")

requirements = ["ANT"]

cunydata = json.loads(BASE_URL.read())
print cunydata[1]
