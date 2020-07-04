SERVICES_DIR:=./services
GENERATE_NUMBERS_DIR:=${SERVICES_DIR}/generate_numbers
GENERATE_NUMBERS_SOURCE:=${GENERATE_NUMBERS_DIR}/src

generate-numbers-lint:
	PYTHONPATH=${GENERATE_NUMBERS_SOURCE} pylint ${GENERATE_NUMBERS_SOURCE}/service

generate-numbers-tests:
	PYTHONPATH=${GENERATE_NUMBERS_SOURCE} python3 -m unittest discover -b -s ${GENERATE_NUMBERS_SOURCE}/tests

clean:
	rm -rf ${DOC_DIR}/build ${DOC_DIR}/_*
	find ${SRC_DIR} | grep -E "(__pycache__|\.pyc|\.pyo)" | xargs rm -rf