import twitter
import requests, json

def public_timeline(url=None, auth=None):
	url = url or "https://api.twitter.com/1/statuses/public_timeline.json"
	r = requests.get(url)
	return json.loads(r.content)

if __name__ == '__main__':
	print public_timeline()
