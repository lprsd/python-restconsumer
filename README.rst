RestConsumer: Generic REST API consumer. 
-----------------------------------------------------------------------

RestConsumer is a generic python wrapper for consuming JSON REST APIs. It is built with python-requests, some magic and good intentions. This is the first alpha release; pull requests are welcome.

Rationale:

    All modern REST API services already have an hierarchical meaningful url structure and return the response content in JSON format. Custom API wrappers for each service would necessitate the developer consuming the API, to refer to the documentation of the wrapper as well as the service itself. (Do I call the twitter.public_timeline() or twitter.get_public_timeline() of this particular library; what about it's pagination option?)

    This package is an attempt to exploit the meaningful url structure and use some python magic to make it developer friendly to create a thin wrapper, on using which the developer would be enabled to consume REST API by looking at the service documentation alone. 

    Examples below highlight it's purpose and use.

For Github API v3:  From the documentation, `/users/:user/repos/` returns all the user's repos.

::

	# Instantiate the consumer with the api end point
	>>> github = RestConsumer(base_url='https://api.github.com/')

	# use the consumer to query for the repos.
	>>> github.users.kennethreitz.repos() -- Returns all the repos of the user kennethreitz.

	Internally, requests.get(url='https://api.github.com/users/kennethreitz/repos') is called and the content is returned in a python dict.

For Stackoverflow: http://api.stackoverflow.com/1.1/users/55562/questions/unanswered returns unanswered questions for user with id 55562

::

	>>> stack = RestConsumer(base_url='http://api.stackoverflow.com/1.1')

	# When there are special characters, that can't be used as python methods, wrap in the 'spc' method.
	>>> s.users.spc('55562').questions.unanswered()

	# All the top answerers of the tag python can be obtained from: http://api.stackoverflow.com/1.1/tags/python/top-answerers/all-time
	s.tags.python.spc('top-answerers').spc('all-time')()

For Twitter:

::

	# Initialize twitter from it's end point. All twitter api calls need '.json' appended.
	t = RestConsumer(base_url='http://api.twitter.com/1',append_json=True)

	# From the twitter documentation, /statuses/public_timeline provides all public timeline data
	t.statuses.public_timeline()

	# Similarly, /user_timeline?screen_name=becomingGuru provides the timeline of the given user
	t.statuses.user_timeline.get(screen_name='becomingGuru')

	# Since get is the default, you can skip that and just do:
	t.statuses.user_timeline(screen_name='becomingGuru')

	# Since twitter also allows (undocumented) /user_timeline/becomingGuru, you can do:
	t.statuses.user_timeline.becomingGuru() -- Which is equivallent to t.statuses.user_timeline.becomingGuru.get()

This is all you need to know about this package. That's the whole point.
Spend your time reading through the documentation of the REST API that you are trying to consume rather than another class wrapper built around it.
You get a dictionary of the received JSON. Wrapping those in classes is hardly pythonic or transparent, nor does it allow you to store it in a database without enough changes. Might as well deal with the received data directly.

Credits: API has been inspired by http://mike.verdone.ca/twitter/, since 3 years: http://weblog.becomingguru.com/2009/05/awesome-python-twitter-library-see.html
While that one is twitter only, this is intended as a generic wrapper. With requests in the scene doing all the hard work, this is simple.


TODO:

* Returning mutated self is not a good idea. Return new objects.
* Enable oAuth
* Enable all parameters taken by requests. Lazy content fetch, with header only, ...
* Provide services.py, that provides various classes, that document end points of various services, so developer can import bing and get going.
* Enable bash auto completion of different services by including various uri's
* Include headers etc as params in the response given.
* Explore wrapping response into ServiceClasses that behave like dict, list and other
* Add more services, freebase, wikipedia