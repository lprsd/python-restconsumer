import json
import requests


def json_response(response):
    return json.loads(response.content)


def append_to_url(base_url, param):
    return "{}{}/".format(base_url, param)


class RestConsumer(object):
    """ Call REST-like endpoints this way:

        >>> consumer = RestConsumer('http://example.com/api/v1/')
        >>> response = consumer.projects.groups[22].events()

        and it will call http://example.com/api/v1/projects/groups/22/events/
    """

    base_url = ''

    _append_json = False
    _append_slash = False
    _requests_kwargs = {}

    def __init__(self, base_url, append_json=False, append_slash=False, response_wrapper=json_response, requests_kwargs={}):
        self.base_url = base_url if base_url[-1] == '/' else "{}{}".format(base_url, "/")
        self._append_json = append_json
        self._append_slash = append_slash
        self._response_wrapper = response_wrapper
        self._requests_kwargs = requests_kwargs

    def __getattr__(self, key):
        new_base = append_to_url(self.base_url, key)
        return self.__class__(base_url=new_base,
                              append_json=self._append_json,
                              append_slash=self._append_slash,
                              response_wrapper=self._response_wrapper,
                              requests_kwargs=self._requests_kwargs)

    def __getitem__(self, key):
        return self.__getattr__(key)

    def __call__(self, **kwargs):
        if not self._append_slash:
            self.base_url = self.base_url[:-1]
        if self._append_json:
            self.base_url = "{}{}".format(self.base_url, '.json')
        if self._requests_kwargs:
            kwargs.update(self._requests_kwargs)
        return self.get(self.base_url, **kwargs)

    def get(self, url, **kwargs):
        response = requests.get(url, **kwargs)
        return self._response_wrapper(response)

    def post(self, **kwargs):
        response = requests.post(**kwargs)
        return self._response_wrapper(response)
