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
        return self.__class__(base_url=new_base,
                              append_json=self.append_json,
                              append_slash=self.append_slash)
    
    def __getitem__(self,key):
        return self.__getattr__(key)

    def __call__(self, **kwargs):
        if not self.append_slash:
            self.base_url = self.base_url[:-1]
        if self.append_json:
            self.base_url = "%s%s" % (self.base_url,'.json')
        print "Calling %s" % self.base_url
        return self.get(self.base_url,**kwargs)

    def get(self,url,**kwargs):
        r = requests.get(url,**kwargs)
        return json.loads(r.content)

    def post(self,**kwargs):
        r = requests.post(**kwargs)
        return json.loads(r.content)
