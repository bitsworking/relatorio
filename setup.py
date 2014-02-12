import os
import re
from setuptools import setup, find_packages

def get_version():
    init = open(os.path.join(os.path.dirname(__file__), 'relatorio',
                             '__init__.py')).read()
    return re.search(r"""__version__ = '([0-9.]*)'""", init).group(1)

setup(
    name="relatorio",
    url="http://code.google.com/p/python-relatorio/",
    author="Nicolas Evrard",
    author_email="nicolas.evrard@b2ck.com",
    maintainer="Cedric Krier",
    maintainer_email="cedric.krier@b2ck.com",
    description="A templating library able to output odt and pdf files",
    long_description="""
relatorio
=========

A templating library which provides a way to easily output all kind of
different files (odt, ods, png, svg, ...). Adding support for more filetype is
easy: you just have to create a plugin for this.

relatorio also provides a report repository allowing you to link python objects
and report together, find reports by mimetypes/name/python objects.
    """,
    license="GPL License",
    version=get_version(),
    packages=find_packages(exclude=['examples']),
    package_data={
        'relatorio.tests': ['*.jpg', '*.odt', '*.png', 'templates/*.tmpl'],
        },
    install_requires=[
        "Genshi >= 0.5",
        "lxml >= 2.0"
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing",
    ],
    test_suite="nose.collector",
    tests_require=[
        "nose",
    ],
    use_2to3=True)
