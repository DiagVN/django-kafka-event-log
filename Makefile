package:
	python setup.py sdist

package_wheel:
	python setup.py bdist_wheel

clean:
	rm -rf dist/*

dev:
	poetry install
