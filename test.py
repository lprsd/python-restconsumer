class SO(object):

    def __init__(self,**kwargs):
        self.base_url = kwargs.pop('base_url',[]) or 'http://api.stackoverflow.com/1.1'
        self.uriparts = kwargs.pop('uriparts',[])
        for k,v in kwargs.items():
            setattr(self,k,v)

    def __getattr__(self,key):
        self.uriparts.append(key)
        return self.__class__(**self.__dict__)        

    def __getitem__(self,key):
        return self.__getattr__(key)

    def __call__(self,**kwargs):
        call_url = "%s/%s"%(self.base_url,"/".join(self.uriparts))
        self.uriparts = []
        return call_url

if __name__ == '__main__':
    print SO().abc.mno.ghi.jkl()
    print SO().abc.mno['ghi'].jkl()
    user1 = SO().users['55562']
    print user1.questions.unanswered()
    print user1.questions.answered()