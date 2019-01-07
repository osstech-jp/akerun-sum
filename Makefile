PYTHON		= python3
VENV		= venv
ACTIVATE	= . ./${VENV}/bin/activate

.PHONY: usage
usage:
	@echo 'Usage: ${MAKE} TARGET'
	@echo ''
	@echo 'Targets:'
	@echo '  init       init directory for develop'
	@echo '  test       run test script'
	@echo '  clean      remove cache file'

.PHONY: init
init:
	${MAKE} ${VENV}

${VENV}:
	${PYTHON} -m venv ${VENV}
	${ACTIVATE} && pip install --upgrade pip setuptools
	${ACTIVATE} && pip install -r requirements.txt

.PHONY: test
test: ${VENV}
	${ACTIVATE} && ./test.sh

.PHONY: clean
clean:
	rm -rf ${VENV}
