# Classification (U)

"""Program:  data_conversion.py

    Description:  Unit testing of data_conversion in mongo_in.py.

    Usage:
        test/unit/mongo_in/data_conversion.py

    Arguments:

"""

# Libraries and Global Variables

# Standard
import sys
import os
import unittest

# Local
sys.path.append(os.getcwd())
import mongo_in                                 # pylint:disable=E0401,C0413
import version                                  # pylint:disable=E0401,C0413

__version__ = version.__version__


class Logger():                                         # pylint:disable=R0903

    """Class:  Logger

    Description:  Class which is a representation of gen_class.Logger class.

    Methods:
        __init__
        log_err

    """

    def __init__(                               # pylint:disable=R0913,R0917
            self, job_name, job_log, log_type, log_format, log_time):

        """Method:  __init__

        Description:  Initialization instance of the class.

        Arguments:

        """

        self.job_name = job_name
        self.job_log = job_log
        self.log_type = log_type
        self.log_format = log_format
        self.log_time = log_time
        self.data = None

    def log_err(self, data):

        """Method:  log_err

        Description:  log_err method.

        Arguments:

        """

        self.data = data


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_string_quoted
        test_dict_string_quoted
        test_dict_success
        test_dict_failure

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.logger = Logger("Name", "Name", "INFO", "%(asctime)s%(message)s",
                             "%m-%d-%YT%H:%M:%SZ|")
        base = os.getcwd()
        self.in_file = os.path.join(
            base, "test/unit/mongo_in/testfiles/test_process_insert.json")
        self.in_file2 = os.path.join(
            base, "test/unit/mongo_in/testfiles/test_process_insert2.json")
        self.in_file3 = os.path.join(
            base, "test/unit/mongo_in/testfiles/test_process_insert3.json")
        self.in_file4 = os.path.join(
            base, "test/unit/mongo_in/testfiles/test_process_insert4.json")
        self.in_file5 = os.path.join(
            base, "test/unit/mongo_in/testfiles/test_process_insert5.json")
        self.results = None
        self.results2 = {"docid": "90349823749", "command": "eucom"}
        self.results3 = "This is testing of a string1"
        self.results4 = '{"docid": "90349823749", "command": "eucom"}'

    def test_string_quoted(self):

        """Function:  test_string_quoted

        Description:  Test with string in a file is string quoted.

        Arguments:

        """

        with open(self.in_file5, mode="r", encoding="UTF-8") as fhdr:
            data = fhdr.read()

        self.assertEqual(
            mongo_in.data_conversion(data, self.logger), self.results3)

    def test_dict_string_quoted(self):

        """Function:  test_dict_string_quoted

        Description:  Test with dictionary in a file is string quoted.

        Arguments:

        """

        with open(self.in_file4, mode="r", encoding="UTF-8") as fhdr:
            data = fhdr.read()

        self.assertEqual(
            mongo_in.data_conversion(data, self.logger), self.results4)

    def test_dict_success(self):

        """Function:  test_dict_success

        Description:  Test with conversion to dictionary successful.

        Arguments:

        """

        with open(self.in_file3, mode="r", encoding="UTF-8") as fhdr:
            data = fhdr.read()

        self.assertEqual(
            mongo_in.data_conversion(data, self.logger), self.results2)

    def test_dict_failure(self):

        """Function:  test_dict_failure

        Description:  Test with conversion to dictionary failure.

        Arguments:

        """

        with open(self.in_file2, mode="r", encoding="UTF-8") as fhdr:
            data = fhdr.read()

        self.assertEqual(
            mongo_in.data_conversion(data, self.logger), self.results)


if __name__ == "__main__":
    unittest.main()
