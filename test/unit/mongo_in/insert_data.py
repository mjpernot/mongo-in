# Classification (U)

"""Program:  insert_data.py

    Description:  Unit testing of insert_data in mongo_in.py.

    Usage:
        test/unit/mongo_in/insert_data.py

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
import lib.gen_class as gen_class           # pylint:disable=E0401,C0413,R0402
import version                                  # pylint:disable=E0401,C0413

__version__ = version.__version__


class Mail():

    """Class:  Mail

    Description:  Class stub holder for gen_class.Mail class.

    Methods:
        __init__
        add_2_msg
        send_mail

    """

    def __init__(self):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.data = None

    def add_2_msg(self, data):

        """Method:  add_2_msg

        Description:  Stub method holder for Mail.add_2_msg.

        Arguments:

        """

        self.data = data

        return True

    def send_mail(self):

        """Method:  send_mail

        Description:  Stub method holder for Mail.send_mail.

        Arguments:

        """

        return True


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

        self.file_regex = "*mongo.json"
        self.monitor_dir = "/dir_path/monitor_dir"
        self.error_dir = "/dir/path/error_dir"
        self.archive_dir = "/dir/path/archive_dir"
        self.to_addr = "Address"
        self.subj = "Subject"


class Cfg2():                                           # pylint:disable=R0903

    """Class:  Cfg2

    Description:  Class which is a representation of a cfg module.

    Methods:
        __init__

    """

    def __init__(self):

        """Method:  __init__

        Description:  Initialization instance of the Cfg class.

        Arguments:

        """

        self.file_regex = "*mongo.json"
        self.monitor_dir = "/dir_path/monitor_dir"
        self.error_dir = "/dir/path/error_dir"
        self.archive_dir = "/dir/path/archive_dir"
        self.to_addr = None
        self.subj = None


class ArgParser():                                      # pylint:disable=R0903

    """Class:  ArgParser

    Description:  Class stub holder for gen_class.ArgParser class.

    Methods:
        __init__
        arg_exist

    """

    def __init__(self):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.args_array = {
            "-c": "mysql_cfg", "-d": "config", "-e": "to_addr",
            "-o": "outfile", "-n": "indentation",
            "-i": "database:table", "-w": "a", "-p": False}

    def arg_exist(self, arg):

        """Method:  arg_exist

        Description:  Method stub holder for gen_class.ArgParser.arg_exist.

        Arguments:

        """

        return arg in self.args_array


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_with_remove_file
        test_with_archive_file
        test_with_fail_insert_no_mail
        test_with_fail_insert_mail
        test_with_multiple_files
        test_with_single_file
        test_with_no_files

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.args = ArgParser()
        self.cfg = Cfg()
        self.cfg2 = Cfg2()
        self.mail = Mail()
        self.dtg = gen_class.TimeFormat()
        self.dtg.create_time()
        self.insert_list = []
        self.insert_list2 = ["/path/file1"]
        self.insert_list3 = ["/path/file1", "/path/file2"]

    @mock.patch("mongo_in.os.remove", mock.Mock(return_value=True))
    @mock.patch("mongo_in.process_insert", mock.Mock(return_value=True))
    @mock.patch("mongo_in.gen_libs.filename_search")
    @mock.patch("mongo_in.gen_class.Logger")
    def test_with_remove_file(self, mock_log, mock_search):

        """Function:  test_with_remove_file

        Description:  Test with removing the file after insert.

        Arguments:

        """

        self.args.args_array["-r"] = True

        mock_log.return_value = True
        mock_search.return_value = self.insert_list2

        self.assertFalse(
            mongo_in.insert_data(self.cfg, self.dtg, mock_log, self.args))

    @mock.patch("mongo_in.gen_libs.mv_file", mock.Mock(return_value=True))
    @mock.patch("mongo_in.process_insert", mock.Mock(return_value=True))
    @mock.patch("mongo_in.gen_libs.filename_search")
    @mock.patch("mongo_in.gen_class.Logger")
    def test_with_archive_file(self, mock_log, mock_search):

        """Function:  test_with_archive_file

        Description:  Test with archiving the file after insert.

        Arguments:

        """

        mock_log.return_value = True
        mock_search.return_value = self.insert_list2

        self.assertFalse(
            mongo_in.insert_data(self.cfg, self.dtg, mock_log, self.args))

    @mock.patch("mongo_in.gen_libs.mv_file", mock.Mock(return_value=True))
    @mock.patch("mongo_in.process_insert", mock.Mock(return_value=False))
    @mock.patch("mongo_in.gen_class.setup_mail")
    @mock.patch("mongo_in.gen_libs.filename_search")
    @mock.patch("mongo_in.gen_class.Logger")
    def test_with_fail_insert_no_mail(self, mock_log, mock_search, mock_mail):

        """Function:  test_with_fail_insert_no_mail

        Description:  Test with failed insert of file but no mail.

        Arguments:

        """

        mock_log.return_value = True
        mock_search.return_value = self.insert_list2
        mock_mail.return_value = self.mail

        self.assertFalse(
            mongo_in.insert_data(self.cfg2, self.dtg, mock_log, self.args))

    @mock.patch("mongo_in.gen_libs.mv_file", mock.Mock(return_value=True))
    @mock.patch("mongo_in.process_insert", mock.Mock(return_value=False))
    @mock.patch("mongo_in.gen_class.setup_mail")
    @mock.patch("mongo_in.gen_libs.filename_search")
    @mock.patch("mongo_in.gen_class.Logger")
    def test_with_fail_insert_mail(self, mock_log, mock_search, mock_mail):

        """Function:  test_with_fail_insert_mail

        Description:  Test with failed insert of file and mail.

        Arguments:

        """

        mock_log.return_value = True
        mock_search.return_value = self.insert_list2
        mock_mail.return_value = self.mail

        self.assertFalse(
            mongo_in.insert_data(self.cfg, self.dtg, mock_log, self.args))

    @mock.patch("mongo_in.gen_libs.mv_file", mock.Mock(return_value=True))
    @mock.patch("mongo_in.process_insert", mock.Mock(return_value=True))
    @mock.patch("mongo_in.gen_libs.filename_search")
    @mock.patch("mongo_in.gen_class.Logger")
    def test_with_multiple_files(self, mock_log, mock_search):

        """Function:  test_with_multiple_files

        Description:  Test with multiple files detected during search.

        Arguments:

        """

        mock_log.return_value = True
        mock_search.return_value = self.insert_list3

        self.assertFalse(
            mongo_in.insert_data(self.cfg, self.dtg, mock_log, self.args))

    @mock.patch("mongo_in.gen_libs.mv_file", mock.Mock(return_value=True))
    @mock.patch("mongo_in.process_insert", mock.Mock(return_value=True))
    @mock.patch("mongo_in.gen_libs.filename_search")
    @mock.patch("mongo_in.gen_class.Logger")
    def test_with_single_file(self, mock_log, mock_search):

        """Function:  test_with_single_file

        Description:  Test with single file detected during search.

        Arguments:

        """

        mock_log.return_value = True
        mock_search.return_value = self.insert_list2

        self.assertFalse(
            mongo_in.insert_data(self.cfg, self.dtg, mock_log, self.args))

    @mock.patch("mongo_in.gen_libs.filename_search")
    @mock.patch("mongo_in.gen_class.Logger")
    def test_with_no_files(self, mock_log, mock_search):

        """Function:  test_with_no_files

        Description:  Test with no files detected during search.

        Arguments:

        """

        mock_log.return_value = True
        mock_search.return_value = self.insert_list

        self.assertFalse(
            mongo_in.insert_data(self.cfg, self.dtg, mock_log, self.args))


if __name__ == "__main__":
    unittest.main()
