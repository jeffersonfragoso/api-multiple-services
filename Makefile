SERVICES_DIR:=./services
GENERATE_NUMBERS_DIR:=${SERVICES_DIR}/generate_numbers
GENERATE_NUMBERS_SOURCE:=${GENERATE_NUMBERS_DIR}/src
PUBLISH_NUMBERS_DIR:=${SERVICES_DIR}/publish_numbers
PUBLISH_NUMBERS_SOURCE:=${PUBLISH_NUMBERS_DIR}/src
API_DIR:=${SERVICES_DIR}/api
API_SOURCE:=${API_DIR}/src

.PHONY: generate-numbers-lint generate-numbers-tests publish-numbers-lint publish-numbers-test api-lint api-tests lint tests clean

generate-numbers-lint:
	PYTHONPATH=${GENERATE_NUMBERS_SOURCE} pylint ${GENERATE_NUMBERS_SOURCE}/service

generate-numbers-tests:
	PYTHONPATH=${GENERATE_NUMBERS_SOURCE} python3 -m unittest discover -b -s ${GENERATE_NUMBERS_SOURCE}/tests

publish-numbers-lint:
	PYTHONPATH=${PUBLISH_NUMBERS_SOURCE} pylint ${PUBLISH_NUMBERS_SOURCE}/service

publish-numbers-tests:
	PYTHONPATH=${PUBLISH_NUMBERS_SOURCE} python3 -m unittest discover -b -s ${PUBLISH_NUMBERS_SOURCE}/tests

api-lint:
	PYTHONPATH=${API_SOURCE} pylint ${API_SOURCE}/api --rcfile=${API_SOURCE}/api/.pylintrc

api-tests:
	PYTHONPATH=${API_SOURCE} python3 -m unittest discover -b -s ${API_SOURCE}/tests

lint: generate-numbers-lint publish-numbers-lint api-lint

tests: generate-numbers-tests publish-numbers-tests api-tests

clean:
	rm -rf ${DOC_DIR}/build ${DOC_DIR}/_*
	find ${SRC_DIR} | grep -E "(__pycache__|\.pyc|\.pyo)" | xargs rm -rf