import requests, json

class RestConsumer(object):

	def __init__(self,base_url,append_json=False,**kwargs):
		self.base_url = base_url
		self.uriparts = []
		self.append_json = append_json
		self.kwargs = kwargs

	def __getattr__(self,k):
		if k=='spc':
			return self.spc
		if not k[0] == '_':
			self.uriparts.append(k)
		else:
			if k[1:3]=='in':
				self.uriparts.append(k[3:])
			elif k[1:3] == 'uh':
				self.uriparts.append(k.replace('_','-'))
		return self

	def spc(self,k):
		self.uriparts.append(k)
		return self

	def __call__(self, **kwargs):
		uri_constructed = '/'.join(self.uriparts)
		self.uriparts = []
		self.uri_constructed = "%s%s"%(uri_constructed,'.json') if self.append_json else uri_constructed
		self.url = '/'.join([self.base_url,self.uri_constructed])
		return self.get(self.url,**kwargs)

	def get(self,url,**kwargs):
		print url
		r = requests.get(url,**kwargs)
		return json.loads(r.content)

	def post(self,**kwargs):
		r = requests.post(**kwargs)
		return json.loads(r.content)

if __name__=='__main__':
	from pprint import pprint
	t = RestConsumer(base_url='https://api.twitter.com/1',append_json=True)
	public_timeline = t.statuses.public_timeline()
	pprint(public_timeline)

	g = RestConsumer(base_url='https://api.github.com')
	repos = g.users.kennethreitz.repos()
	pprint(repos)

	s = RestConsumer(base_url='http://api.stackoverflow.com/1.1')
	sr = s.users.spc('55562').questions.unanswered()
	pprint(sr)

	sr2 = s.tags.python.spc('top-answerers').spc('all-time')()
	pprint(sr2)