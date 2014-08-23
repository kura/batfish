import re
from setuptools import (find_packages, setup)
import sys


desc = "A DigitalOcean shell and CLI interface"
long_desc = open('README.rst').read() + "\n\n" + open('CHANGES.rst').read()
long_desc = re.sub(r":[a-z]*:`", "`", long_desc)

exec(open('batfish/__init__.py').read())

entry_points = {
    'console_scripts': [
        'batfish = batfish.cli:cli',
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
      install_requires=['requests', ],
      requires=['requests', ],
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
