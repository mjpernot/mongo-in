# Classification (U)

"""Program:  process_insert.py

    Description:  Unit testing of process_insert in mongo_in.py.

    Usage:
        test/unit/mongo_in/process_insert.py

    Arguments:

"""

# Libraries and Global Variables

# Standard
import sys
import os
import unittest
import mock

# Local
sys.path.append(os.getcwd())
import mongo_in                                 # pylint:disable=E0401,C0413
import version                                  # pylint:disable=E0401,C0413

__version__ = version.__version__


class Cfg():                                            # pylint:disable=R0903

    """Class:  Cfg

    Description:  Class which is a representation of a cfg module.

    Methods:
        __init__

    """

    def __init__(self):

        """Method:  __init__

        Description:  Initialization instance of the Cfg class.

        Arguments:

        """

        self.mconfig = "mongo"


class TimeFormat():                                     # pylint:disable=R0903

    """Class:  TimeFormat

    Description:  Class which is a representation of a TimeFormat module.

    Methods:
        __init__

    """

    def __init__(self):

        """Method:  __init__

        Description:  Initialization instance of the TimeFormat class.

        Arguments:

        """

        self.dtg = "DTG"


class Logger():

    """Class:  Logger

    Description:  Class which is a representation of gen_class.Logger class.

    Methods:
        __init__
        log_info
        log_err

    """

    def __init__(                                       # pylint:disable=R0913
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

    def log_info(self, data):

        """Method:  log_info

        Description:  log_info method.

        Arguments:

        """

        self.data = data

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
        test_mongo_failed
        test_mongo_successful
        test_string_quoted
        test_dict_string_quoted
        test_json_success
        test_json_failure
        test_with_encoded_data

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.cfg = Cfg()
        self.dtg = TimeFormat()
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

    @mock.patch("mongo_in.insert_mongo", mock.Mock(return_value=False))
    def test_mongo_failed(self):

        """Function:  test_mongo_failed

        Description:  Test with failed Mongo data insertion.

        Arguments:

        """

        self.assertFalse(
            mongo_in.process_insert(
                self.cfg, self.dtg, self.logger, self.in_file))

    @mock.patch("mongo_in.insert_mongo", mock.Mock(return_value=True))
    def test_mongo_successful(self):

        """Function:  test_mongo_successful

        Description:  Test with successful Mongo data insertion.

        Arguments:

        """

        self.assertTrue(
            mongo_in.process_insert(
                self.cfg, self.dtg, self.logger, self.in_file))

    @mock.patch("mongo_in.insert_mongo", mock.Mock(return_value=True))
    def test_string_quoted(self):

        """Function:  test_string_quoted

        Description:  Test with string in a file is string quoted.

        Arguments:

        """

        self.assertFalse(
            mongo_in.process_insert(
                self.cfg, self.dtg, self.logger, self.in_file5))

    @mock.patch("mongo_in.insert_mongo", mock.Mock(return_value=True))
    def test_dict_string_quoted(self):

        """Function:  test_dict_string_quoted

        Description:  Test with dictionary in a file is string quoted.

        Arguments:

        """

        self.assertTrue(
            mongo_in.process_insert(
                self.cfg, self.dtg, self.logger, self.in_file4))

    @mock.patch("mongo_in.insert_mongo", mock.Mock(return_value=True))
    def test_json_success(self):

        """Function:  test_json_success

        Description:  Test with conversion to JSON successful.

        Arguments:

        """

        self.assertTrue(
            mongo_in.process_insert(
                self.cfg, self.dtg, self.logger, self.in_file3))

    def test_json_failure(self):

        """Function:  test_json_failure

        Description:  Test with conversion to JSON failure.

        Arguments:

        """

        self.assertFalse(
            mongo_in.process_insert(
                self.cfg, self.dtg, self.logger, self.in_file2))

    @mock.patch("mongo_in.insert_mongo", mock.Mock(return_value=True))
    def test_with_encoded_data(self):

        """Function:  test_with_encoded_data

        Description:  Test with encoded data in the file.

        Arguments:

        """

        self.assertTrue(
            mongo_in.process_insert(
                self.cfg, self.dtg, self.logger, self.in_file))


if __name__ == "__main__":
    unittest.main()
