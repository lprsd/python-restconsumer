import requests, json

class RestConsumer(object):

    def __init__(self,base_url,append_json=False,**kwargs):
        self.base_url = base_url
        self.uriparts = kwargs.pop('uriparts',[])
        self.append_json = append_json
        for k,v in kwargs.items():
            setattr(self,k,v)

    def __getattr__(self,key):
        self.uriparts.append(key)
        return self.__class__(**self.__dict__)        

    def spc(self,key):
        return self.__getattr__(key)

    def __getitem__(self,key):
        return self.__getattr__(key)

    def __call__(self, **kwargs):
        uri_constructed = '/'.join(self.uriparts)
        self.uriparts = []
        self.uri_constructed = "%s%s"%(uri_constructed,'.json') if self.append_json else uri_constructed
        self.url = '/'.join([self.base_url,self.uri_constructed])
        return self.get(self.url,**kwargs)

    def get(self,url,**kwargs):
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
    sr = s.users['55562'].questions.unanswered()
    pprint(sr)

    sr2 = s.tags.python['top-answerers']['all-time']
    pprint(sr2())