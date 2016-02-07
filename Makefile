readme:
	pandoc -o README.rst README.md

upload: readme
	python3 setup.py sdist upload

test:
	python3 setup.py test

all: readme