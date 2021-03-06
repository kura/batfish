SHELL := /bin/bash
.PHONY: clean coverage deps deps-docs deps-test docs flake8 install pypi rtd test tox uninstall

clean:
	find . -name "*.pyc" -delete

coverage: deps-test
	coverage run --source=batfish runtests.py

deps:
	pip install -r requirements.txt

deps-docs:
	pip install -r requirements-docs.txt

deps-test:
	pip install -r requirements-test.txt

docs: deps-docs
	sphinx-build -b html docs/source docs/build

flake8:
	pip install flake8
	flake8 batfish

install:
	python setup.py install

pypi: rtd
	pip install -r requirements-pypi.txt
	python setup.py register
	python setup.py sdist bdist_wheel
	twine upload dist/*

rtd:
	curl -X POST https://readthedocs.org/build/batfish

test:
	nosetests --processes=$(shell grep -c ^processor /proc/cpuinfo 2>/dev/null || sysctl -n hw.ncpu) --with-progressive

tox: deps deps-test
	pip install detox
	detox

uninstall:
	pip uninstall batfish
