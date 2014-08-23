# convenience makefile to boostrap & run buildout
# use `make options=-v` to run buildout with extra options

python = python2.7
options = -c travis.cfg

all: docs tests

coverage: htmlcov/index.html

htmlcov/index.html: README.rst src/brasil.gov.paginadestaque/*.py bin/coverage
	@bin/coverage run --source=./src/brasil.gov.paginadestaque/ --branch bin/test
	@bin/coverage html -i
	@touch $@
	@echo "Coverage report was generated at '$@'."

docs: docs/html/index.html

docs/html/index.html: docs/*.rst src/brasil.gov.paginadestaque/*.py src/brasil.gov.paginadestaque/browser/*.py src/brasil.gov.paginadestaque/tests/*.py bin/sphinx-build
	bin/sphinx-build docs docs/html
	@touch $@
	@echo "Documentation was generated at '$@'."

bin/sphinx-build: .installed.cfg
	@touch $@

.installed.cfg: bin/buildout buildout.cfg setup.py
	@mkdir -p buildout-cache/downloads
	bin/buildout $(options)

bin/buildout: bin/python buildout.cfg bootstrap.py
	bin/python bootstrap.py -v 1.7.1
	@touch $@

bin/python:
	virtualenv -p $(python) --no-site-packages .
	@touch $@

tests: .installed.cfg
	@bin/test
	@bin/code-analysis

clean:
	@rm -rf .coverage .installed.cfg .mr.developer.cfg bin docs/html htmlcov parts develop-eggs \
		src/brasil.gov.paginadestaque.egg-info lib include .Python

.PHONY: all docs tests clean
