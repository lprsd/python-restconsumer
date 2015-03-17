import json
import requests


def json_response(consumer, response):
    return json.loads(response.content)


def append_to_url(base_url, param):
    return "{}{}/".format(base_url, param)


class RestConsumer(object):
    """ Call REST-like endpoints this way:

        >>> consumer = RestConsumer('http://example.com/api/v1/')
        >>> events = consumer.projects.groups[22].events()

        and it will call http://example.com/api/v1/projects/groups/22/events/
    """

    base_url = ''

    _append_json = False
    _append_slash = False
    _requests_kwargs = {}
    _response_wrapper = None

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
        return self._response_wrapper(self, response)

    def post(self, **kwargs):
        response = requests.post(**kwargs)
        return self._response_wrapper(self, response)


class PaginatableResponse(object):
    """ This iterator supports pagination done by Link header.

        Here's how you can use it:

        >>> consumer = RestConsumer('http://example.com/api/v1/',
                                    response_wrapper=PaginatableResponse)
        >>> events = consumer.projects.groups[22].events()
        >>> for event in events:
                print event

        It will iterate through all events on a server,
        downloading next pages automatically when needed.
    """

    def __init__(self, consumer, response):
        self._consumer = consumer
        self._response = response
        self._set_state(response)

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return next(self._content_iterator)
        except StopIteration:
            if self._is_paginatable():
                self._download_next_page()
                return next(self._content_iterator)
            else:
                raise

    def next(self):
        return self.__next__()

    def _set_state(self, response):
        self._response = response
        self._content_iterator = iter(json.loads(response.content))

    def _download_next_page(self):
        self._consumer.base_url = self._response.links['next']['url']
        response = self._consumer()._response
        self._set_state(response)

    # FIXME This guy should be reimplemented according to HTTP Link standart.
    def _is_paginatable(self):
        if 'next' in self._response.links:
            if 'results' in self._response.links['next']:
                if self._response.links['next']['results'] == 'true':
                    return True
            else:
                return True

        return False
