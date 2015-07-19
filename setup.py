import os

from setuptools import setup, find_packages

install_requires = [
    'requests',
]

setup(
    name='python-restconsumer',
    version='1.1.2',
    description='RESTful API generic client with sweet interface.',
    long_description='See README.rst',
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    author='murchik',
    author_email='mixturchik@gmail.com',
    url='https://github.com/moorchegue/python-restconsumer',
    keywords='rest api generic client',
    packages=find_packages(),
    py_modules=['restconsumer'],
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
)
