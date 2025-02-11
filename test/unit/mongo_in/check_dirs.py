# Classification (U)

"""Program:  check_dirs.py

    Description:  Unit testing of check_dirs in mongo_in.py.

    Usage:
        test/unit/mongo_in/check_dirs.py

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
import mongo_in
import version

__version__ = version.__version__


class Cfg():

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

        self.error_dir = "/dir_path/error_dir"
        self.archive_dir = "/dir_path/archive_dir"
        self.monitor_dir = "/dir_path/monitor_dir"


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_archive_dir_fail
        test_monitor_dir_fail
        test_error_dir_failure
        test_outfile_failure
        test_log_dir_failure
        test_no_failures

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.cfg = Cfg()
        self.chk = (True, None)
        self.chk5 = (False, "Error_dir failure")
        self.chk9 = (False, "Monitor_dir failure")
        self.chk10 = (False, "Archive_dir failure")
        self.results = dict()
        self.results5 = {"/dir_path/error_dir": "Error_dir failure"}
        self.results9 = {"/dir_path/monitor_dir": "Monitor_dir failure"}
        self.results10 = {"/dir_path/archive_dir": "Archive_dir failure"}

    @mock.patch("mongo_in.gen_libs.chk_crt_dir")
    def test_archive_dir_fail(self, mock_chk):

        """Function:  test_archive_dir_fail

        Description:  Test with failure on raw_archive_dir directory.

        Arguments:

        """

        mock_chk.side_effect = [self.chk, self.chk10, self.chk]

        self.assertEqual(mongo_in.check_dirs(self.cfg), self.results10)

    @mock.patch("mongo_in.gen_libs.chk_crt_dir")
    def test_monitor_dir_fail(self, mock_chk):

        """Function:  test_monitor_dir_fail

        Description:  Test with failure on monitor_dir directory.

        Arguments:

        """

        mock_chk.side_effect = [self.chk, self.chk, self.chk9]

        self.assertEqual(mongo_in.check_dirs(self.cfg), self.results9)

    @mock.patch("mongo_in.gen_libs.chk_crt_dir")
    def test_error_dir_failure(self, mock_chk):

        """Function:  test_error_dir_failure

        Description:  Test with failure on error_dir check.

        Arguments:

        """

        mock_chk.side_effect = [self.chk5, self.chk, self.chk]

        self.assertEqual(mongo_in.check_dirs(self.cfg), self.results5)

    @mock.patch("mongo_in.gen_libs.chk_crt_dir")
    def test_no_failures(self, mock_chk):

        """Function:  test_no_failures

        Description:  Test with no failures on directory checks.

        Arguments:

        """

        mock_chk.side_effect = [self.chk, self.chk, self.chk]

        self.assertEqual(mongo_in.check_dirs(self.cfg), self.results)


if __name__ == "__main__":
    unittest.main()
