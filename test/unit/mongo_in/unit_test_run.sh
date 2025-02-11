#!/bin/bash
# Unit testing program for the mongo_in.py module.
# This will run all the units tests for this program.
# Will need to run this from the base directory where the module file
#   is located at.

echo ""
echo "Unit test:  mongo_in.py"
/usr/bin/python ./test/unit/mongo_in/check_dirs.py
/usr/bin/python ./test/unit/mongo_in/help_message.py
/usr/bin/python ./test/unit/mongo_in/insert_data.py
/usr/bin/python ./test/unit/mongo_in/insert_mongo.py
/usr/bin/python ./test/unit/mongo_in/is_base64.py
/usr/bin/python ./test/unit/mongo_in/main.py
/usr/bin/python ./test/unit/mongo_in/process_insert.py
/usr/bin/python ./test/unit/mongo_in/run_program.py
