#!/bin/bash
# Unit test code coverage for pulled_search.py module.
# This will run the Python code coverage module against all unit test modules.
# This will show the amount of code that was tested and which lines of code
#   that was skipped during the test.

coverage erase

echo ""
echo "Running unit test modules in conjunction with coverage"
coverage run -a --source=mongo_in test/unit/mongo_in/check_dirs.py
coverage run -a --source=mongo_in test/unit/mongo_in/help_message.py
coverage run -a --source=mongo_in test/unit/mongo_in/insert_data.py
coverage run -a --source=mongo_in test/unit/mongo_in/insert_mongo.py
coverage run -a --source=mongo_in test/unit/mongo_in/is_base64.py
coverage run -a --source=mongo_in test/unit/mongo_in/main.py
coverage run -a --source=mongo_in test/unit/mongo_in/process_insert.py
coverage run -a --source=mongo_in test/unit/mongo_in/run_program.py
echo ""
echo "Producing code coverage report"
coverage combine
coverage report -m
