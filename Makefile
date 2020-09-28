PYTHON		= python3
VENV		= venv
ACTIVATE	= . ./${VENV}/bin/activate

TARGET          = testpypi

.PHONY: usage
usage:
	@echo 'Usage: ${MAKE} TARGET'
	@echo ''
	@echo 'Targets:'
	@echo '  init       init directory for develop'
	@echo '  test       run test script'
	@echo '  build      build wheel package'
	@echo '  upload     upload ${TARGET}'
	@echo '    TARGET=pypi'
	@echo '  clean      remove cache file'

.PHONY: init
init:
	${MAKE} ${VENV}

${VENV}:
	${PYTHON} -m venv ${VENV}
	${ACTIVATE} && pip install --upgrade pip setuptools wheel
	${ACTIVATE} && pip install -r requirements.txt

.PHONY: test
test: ${VENV}
	${ACTIVATE} && ./test.sh

.PHONY: build
build:
	rm -rf dist build *.egg-info
	${MAKE} init
	${ACTIVATE} && python setup.py bdist_wheel sdist --format=gztar,zip
	${ACTIVATE} && twine check dist/*

.PHONY: upload
upload:
	${MAKE} build
	${ACTIVATE} && twine upload --repository ${TARGET} dist/*.tar.gz dist/*.whl dist/*.zip


.PHONY: clean
clean:
	rm -rf ${VENV}
	rm -f log output.csv
	rm -rf build dist akerun_sum.egg-info
