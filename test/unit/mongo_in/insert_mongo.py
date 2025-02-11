# Classification (U)

"""Program:  insert_mongo.py

    Description:  Unit testing of insert_mongo in mongo_in.py.

    Usage:
        test/unit/mongo_in/insert_mongo.py

    Arguments:

"""

# Libraries and Global Variables

# Standard
import sys
import os
import datetime
import unittest
import mock

# Local
sys.path.append(os.getcwd())
import mongo_in                                 # pylint:disable=E0401,C0413
import version                                  # pylint:disable=E0401,C0413

__version__ = version.__version__


class TimeFormat():                                     # pylint:disable=R0903

    """Class:  TimeFormat

    Description:  Class stub holder for gen_class.TimeFormat class.

    Methods:
        __init__
        get_hack

    """

    def __init__(self):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.delimit = "."
        self.micro = False
        self.thacks = {}
        self.tformats = {
            "ymd": {"format": "%Y%m%d", "del": "", "micro": False}}
        rdtg = datetime.datetime.now()
        msecs = str(rdtg.microsecond // 100)
        ext = ""
        texpr = "ymd"
        tformat = "ymd"
        self.thacks[tformat] = datetime.datetime.strftime(rdtg, texpr) + ext

    def get_hack(self, tformat):

        """Method:  get_hack

        Description:  Stub method holder for TimeFormat.get_hack.

        Arguments:

        """

        return self.thacks[tformat] if tformat in self.thacks else None


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

        self.error_dir = "/dir/path"
        self.dbs = "database_name"
        self.tbl = "table_name"


class Logger():

    """Class:  Logger

    Description:  Class which is a representation of gen_class.Logger class.

    Methods:
        __init__
        log_info
        log_err

    """

    def __init__(self, job_name, job_log, log_type, log_format, log_time):

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
        self.data = {"asOf": "20200306 084503", "entry": "data_line"}

    @mock.patch("mongo_in.gen_libs.write_file",
                mock.Mock(return_value=True))
    @mock.patch("mongo_in.mongo_libs.ins_doc",
                mock.Mock(return_value=(False, "mongo failure")))
    def test_mongo_failed(self):

        """Function:  test_mongo_failed

        Description:  Test with failed Mongo data insertion.

        Arguments:

        """

        self.assertFalse(mongo_in.insert_mongo(
            self.cfg, self.dtg, self.logger, self.data))

    @mock.patch("mongo_in.mongo_libs.ins_doc",
                mock.Mock(return_value=(True, None)))
    def test_mongo_successful(self):

        """Function:  test_mongo_successful

        Description:  Test with successful Mongo data insertion.

        Arguments:

        """

        self.assertTrue(mongo_in.insert_mongo(
            self.cfg, self.dtg, self.logger, self.data))


if __name__ == "__main__":
    unittest.main()
