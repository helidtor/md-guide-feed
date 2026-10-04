"""Download the public YGOPRODeck card-facts cache used by build/validation."""
import json,pathlib,urllib.request
url='https://db.ygoprodeck.com/api/v7/cardinfo.php'
req=urllib.request.Request(url,headers={'User-Agent':'MDGuideFeed/1.0'})
raw=urllib.request.urlopen(req,timeout=60).read()
data=json.loads(raw)
assert data.get('data')
pathlib.Path(__file__).with_name('cardinfo.json').write_bytes(raw)
print(f'Cached {len(data["data"])} cards from YGOPRODeck API v7.')
