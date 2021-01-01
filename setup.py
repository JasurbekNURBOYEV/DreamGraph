from setuptools import setup

description = """
**The Python module for Telegraph API.**

DreamGraph is built to make it easy to use Telegraph API which is presented by pupular Messaging platform Telegram.
The module is licensed under GNU GPL license and it is open-source.

Docs: http://dreamgraph.ml

Module is only compatible with Python 3.

"""
__version__ = '1.1.5'


setup(
    name='dreamgraph',
    packages=['dreamgraph'],
    version=__version__,
    long_description=description,
    description='The Python module for Telegraph API',
    author='Jasur Nurboev',
    author_email='bluestacks6523@gmail.com',
    url='https://github.com/JasurbekNURBOYEV/DreamGraph',
    download_url=f'https://github.com/JasurbekNURBOYEV/DreamGraph/archive/{__version__}.tar.gz',
    keywords=['telegraph', 'telegraph-api', 'python-module', 'dreamgraph'],
    classifiers=[],
    install_requires=['requests'],
)
