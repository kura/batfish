# -*- coding: utf-8 -*-

# (The MIT License)
#
# Copyright (c) 2014 Kura
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the 'Software'), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import re
from setuptools import (find_packages, setup)
import sys


desc = "A DigitalOcean shell, API and CLI interface"
long_desc = open('README.rst').read() + "\n\n" + open('CHANGES.rst').read()
long_desc = re.sub(r":[a-z]*:`", "`", long_desc)

exec(open('batfish/__about__.py').read())

entry_points = {
    'console_scripts': [
        'batfish = batfish.cli:cli',
        'batfish-cli = batfish.cli:cli',
        'batfish-console = batfish.console:shell',
    ]
}

setup(name=__title__,
      version=__version__,
      url=__url__,
      author=__author__,
      author_email=__email__,
      maintainer=__author__,
      maintainer_email=__email__,
      description=desc,
      long_description=long_desc,
      license=__license__,
      platforms=['linux'],
      packages=find_packages(exclude=["*.tests"]),
      install_requires=['requests', 'click', ],
      requires=['requests', 'click', ],
      provides=[__title__, ],
      keywords=['digital', 'ocean', 'shell', 'cli'],
      entry_points=entry_points,
      classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Archiving :: Packaging',
      ],
      zip_safe=True,
      )
