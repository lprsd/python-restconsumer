import requests, json

def append_to_url(base_url,param):
    return "%s%s/" % (base_url,param)


class RestConsumer(object):

    def __init__(self,base_url,append_json=False,append_slash=False):
        self.base_url = base_url if base_url[-1] == '/' else "%s%s" % (base_url,"/")
        self.append_json = append_json
        self.append_slash = append_slash

    def __getattr__(self,key):
        new_base = append_to_url(self.base_url,key)
        return self.__class__(base_url=new_base,append_json=self.append_json)

    def __getitem__(self,key):
        return self.__getattr__(key)

    def __call__(self, **kwargs):
        if not self.append_slash:
            self.base_url = self.base_url[:-1]
        if self.append_json:
            self.base_url = "%s%s" % (self.base_url[:-1],'.json')
        print "Calling %s" % self.base_url
        return self.get(self.base_url,**kwargs)

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

    st2 = RestConsumer(base_url='http://api.stackoverflow.com/1.1')
    sr2 = st2.tags.python['top-answerers']['all-time']
    pprint(sr2())
    