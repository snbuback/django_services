help:
	@echo
	@echo "Please use 'make <target>' where <target> is one of"
	@echo "  clean      to clean garbage left by builds and installation"
	@echo "  compile    to compile .py files (just to check for syntax errors)"
	@echo "  install    to install"
	@echo "  build      to build without installing"
	@echo "  dist       to create egg for distribution"
	@echo "  publish    to publish the package to PyPI"
	@echo "  test       to run tests"
	@echo

clean:
	@echo "Cleaning..."
	@rm -rf build dist *.egg-info *.egg .tox
	@find . -name \*.pyc -delete

compile: clean
	@echo "Compiling source code..."
	@python -tt -m compileall django_services
	@python -tt -m compileall tests

test: clean
	@python django_services/runtests/runtests.py

build:
	@python setup.py build

install:
	@python setup.py install

dist: clean
	@python setup.py sdist

publish: clean
	@python setup.py sdist upload -r pypi

