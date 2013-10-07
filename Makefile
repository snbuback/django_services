help:
	@echo
	@echo "Please use 'make <target>' where <target> is one of"
	@echo "	 clean		to clean garbage left by builds and installation"
	@echo "	 compile	to compile .py files (just to check for syntax errors)"
	@echo "	 install	to install"
	@echo "	 build		to build without installing"
	@echo "	 dist		to create egg for distribution"
	@echo "	 publish	to publish the package to PyPI"
	@echo "	 test		to run tests"
	@echo "	 pip		to install some dependecies"
	@echo

clean:
	@echo "Cleaning..."
	@rm -rf build dist *.egg-info *.egg .tox
	@find . -name \*.pyc -delete
	@git clean -xdf

compile: clean
	@echo "Compiling source code..."
	@python -tt -m compileall django_services
	@python -tt -m compileall tests

test: clean
	@python django_services/runtests/runtests.py

pip: # install pip libraries
	@pip install -r requirements.txt
	@pip install -r requirements_test.txt

build:
	@python setup.py build

install:
	@python setup.py install

dist: clean
	@python setup.py sdist

upload: clean
	@python setup.py sdist upload -r pip

increment_version:
	@python -c "import django_services; VERSION = django_services.VERSION.split('.') ; VERSION[2] = str(int(VERSION[2])+1); f = open('django_services/__init__.py', 'w'); f.write('VERSION = \'%s\'\n' % '.'.join(VERSION)); f.close()"

publish: increment_version upload
	@git commit -m 'incremented version' -- django_services/__init__.py
	@git tag v`egrep -o "'.*'" django_services/__init__.py | tr -d \'`
	@git push --tags
	@git push

