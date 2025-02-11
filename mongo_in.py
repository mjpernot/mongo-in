#!/usr/bin/python
# Classification (U)

# Shell commands follow
# Next line is bilingual: it starts a comment in Python & is a no-op in shell
""":"

# Find a suitable python interpreter (can adapt for specific needs)
# NOTE: Ignore this section if passing the -h option to the program.
#   This code must be included in the program's initial docstring.
for cmd in python3.12 python3.9 ; do
   command -v > /dev/null $cmd && exec $cmd $0 "$@"
done

echo "OMG Python not found, exiting...."

exit 2

# Previous line is bilingual: it ends a comment in Python & is a no-op in shell
# Shell commands end here

   Program:  mongo_in.py

    Description:  Program to take an external JSON document (file) and insert
        into a Mongo database.

    Usage:
        mongo_in.py -c cfg_file -d path -I [-v | -h]

    Arguments:
        -c cfg_file => Mongo configuration file.
        -d dir path => Config directory path.
        -I => Insert file with JSON documents into database.

        -v => Display version of this program.
        -h => Help and usage message.

        NOTE 1:  -v and/or -h overrides all other options.

    Notes:
        Mongo configuration file format (config/mongo.py.TEMPLATE).  The
            configuration file format is for connecting to a Mongo database or
            replica set.

        # Name of Mongo database for data insertion
        dbs = "DATABASE"
        # Name of Mongo collection
        tbl = "COLLECTION"
        # Logger directory for the storage of logs.
        log_dir = "BASE_PATH/log/"
        # Logger file name.
        log_file = "mongo_in.log"
        # Directory path to where error files are saved to.
        error_dir = "BASE_PATH/insert_error"
        # Directory where to monitor for new files to insert into Mongodb.
        monitor_dir = "MONITOR_DIR_PATH"
        # Regular expression for search for Insert/Mongodb file names.
        file_regex = "_mongo.json"
        # Directory path to where Mongo inserted files are saved to.
        archive_dir = "BASE_PATH/archive"

        There are two ways to connect methods:  single Mongo database or a
        Mongo replica set.

        Single database connection:

        # Single Configuration file for Mongo Database Server.
        user = "USER"
        japd = "PSWORD"
        host = "IP_ADDRESS"
        name = "HOSTNAME"
        port = 27017
        conf_file = None
        auth = True
        auth_db = "admin"
        auth_mech = "SCRAM-SHA-1"

        Replica Set connection:  Same format as above, but with these
            additional entries at the end of the configuration file.  By
            default all these entries are set to None to represent not
            connecting to a replica set.

        repset = "REPLICA_SET_NAME"
        repset_hosts = "HOST1:PORT, HOST2:PORT, HOST3:PORT, [...]"
        db_auth = "AUTHENTICATION_DATABASE"

        If Mongo is set to use TLS or SSL connections, then one or more of
            the following entries will need to be completed to connect
            using TLS or SSL protocols.
            Note:  Read the configuration file to determine which entries
                will need to be set.

            SSL:
                auth_type = None
                ssl_client_ca = None
                ssl_client_key = None
                ssl_client_cert = None
                ssl_client_phrase = None
            TLS:
                auth_type = None
                tls_ca_certs = None
                tls_certkey = None
                tls_certkey_phrase = None

        Note:  FIPS Environment for Mongo.
          If operating in a FIPS 104-2 environment, this package will
          require at least a minimum of pymongo==3.8.0 or better.  It will
          also require a manual change to the auth.py module in the pymongo
          package.  See below for changes to auth.py.

        - Locate the auth.py file python installed packages on the system
            in the pymongo package directory.
        - Edit the file and locate the "_password_digest" function.
        - In the "_password_digest" function there is an line that should
            match: "md5hash = hashlib.md5()".  Change it to
            "md5hash = hashlib.md5(usedforsecurity=False)".
        - Lastly, it will require the Mongo configuration file entry
            auth_mech to be set to: SCRAM-SHA-1 or SCRAM-SHA-256.

        Configuration modules -> Name is runtime dependent as it can be used to
            connect to different databases with different names.

    Example:
        mongo_in.py -c mongo -d config -I

":"""
# Python program follows


# Libraries and Global Variables

# Standard
import sys
import os
import ast
import base64
import binascii

try:
    import simplejson as json
except ImportError:
    import json

# Local
try:
    from .lib import gen_libs
    from .lib import gen_class
    from .mongo_lib import mongo_libs
    from .mongo_lib import mongo_class
    from . import version

except (ValueError, ImportError) as err:
    import lib.gen_libs as gen_libs                     # pylint:disable=R0402
    import lib.gen_class as gen_class                   # pylint:disable=R0402
    import mongo_lib.mongo_libs as mongo_libs           # pylint:disable=R0402
    import mongo_lib.mongo_class as mongo_class         # pylint:disable=R0402
    import version

__version__ = version.__version__

# Global


def help_message():

    """Function:  help_message

    Description:  Displays the program's docstring which is the help and usage
        message when -h option is selected.

    Arguments:

    """

    print(__doc__)


def insert_mongo(cfg, dtg, log, data):

    """Function:  insert_mongo

    Description:  Insert JSON document into Mongo database.

    Arguments:
        (input) cfg -> Configuration setup
        (input) dtg -> Datatime class instance
        (input) log -> Log class instance
        (input) line_json -> JSON document
        (output) status -> True|False - Successful insertion into Mongo

    """

    log.log_info("insert_mongo:  Inserting data into Mongo.")
    status = True
    m_status = mongo_libs.ins_doc(cfg, cfg.dbs, cfg.tbl, data)

    if not m_status[0]:
        log.log_err("insert_mongo:  Insertion into Mongo failed.")
        log.log_err(f"Mongo error message:  {m_status[1]}")
        fname = os.path.join(
            cfg.error_dir, "mongo_insert_failed." + dtg.get_hack("ymd"))
        gen_libs.write_file(fname=fname, mode="a", data=data)
        status = False

    return status


def is_base64(data):

    """Function:  is_base64

    Description:  Determines if the data is base64 encoded.

    Arguments:
        (input) data -> Data string to be checked
        (output) status -> True|False - Is base64 encoded

    """

    try:
        status = True if base64.b64encode(
            base64.b64decode(data))[1:70].decode() == data[1:70] else False

    except TypeError:
        status = False

    except binascii.Error:
        status = False

    return status


def process_insert(cfg, dtg, log, fname):

    """Function:  process_insert

    Description:  Process the insert file and send to a database.

    Arguments:
        (input) cfg -> Configuration setup
        (input) dtg -> Datatime class instance
        (input) log -> Log class instance
        (input) fname -> Insert file name
        (output) status -> True|False - File has successfully processed

    """

    log.log_info("process_insert:  Converting data to JSON.")

    with open(fname, mode="r", encoding="UTF-8") as fhdr:
        data = fhdr.read()

    # Check the first 70 chars in case the encoded is split into multiple lines
    if is_base64(data):
        line_json = ast.literal_eval(base64.b64decode(data).decode())

    else:
        try:
            line_json = json.loads(data)

        except ValueError:
            line_json = data

    if isinstance(line_json, dict):
        status = insert_mongo(cfg, dtg, log, line_json)

    else:
        log.log_err("process_insert: Data failed to convert to JSON.")
        status = False

    return status


def insert_data(args, cfg, dtg, log):

    """Function:  insert_data

    Description:  Insert data into the Mongo database.

    Arguments:
        (input) args -> ArgParser class instance
        (input) cfg -> Configuration setup
        (input) dtg -> Datatime class instance
        (input) log -> Log class instance

    """

    log.log_info("insert_data:  Searching for new files.")
    status = True
    insert_list = gen_libs.filename_search(
        cfg.monitor_dir, cfg.file_regex, add_path=True)
    log.log_info("insert_data:  Processing files to insert.")

    for fname in insert_list:
        log.log_info(f"insert_data:  Processing file: {fname}")
        status = status & process_insert(cfg, dtg, log, fname)
        log.log_info("insert_data:  Post-processing of files.")
        gen_libs.mv_file(fname, cfg.monitor_dir, cfg.archive_dir)

    if not status and cfg.to_addr:
        mail = gen_class.setup_mail(cfg.to_addr, subj=cfg.subj)


def check_dirs(args, cfg):

    """Function:  check_dirs

    Description:  Validate the directories in the configuration file.

    Arguments:
        (input) args -> ArgParser class instance
        (input) cfg -> Configuration setup
        (output) msg_dict -> Dictionary of any error messages detected

    """

    msg_dict = dict()
    status, msg = gen_libs.chk_crt_dir(
        cfg.error_dir, write=True, create=True, no_print=True)

    if not status:
        msg_dict[cfg.error_dir] = msg

    status, msg = gen_libs.chk_crt_dir(
        cfg.archive_dir, write=True, create=True, no_print=True)

    if not status:
        msg_dict[cfg.archive_dir] = msg

    status, msg = gen_libs.chk_crt_dir(
        cfg.monitor_dir, write=True, no_print=True)

    if not status:
        msg_dict[cfg.monitor_dir] = msg

    return msg_dict
    

def run_program(args, func_dict):

    """Function:  run_program

    Description:  Controls flow of the program.

    Arguments:
        (input) args -> ArgParser class instance
        (input) func_dict -> Dictionary list of functions and options

    """

    func_dict = dict(func_dict)
    dtg = gen_class.TimeFormat()
    dtg.create_hack("ymd")
    cfg = gen_libs.load_module(args.get_val("-c"), args.get_val("-d"))
    status, err_msg = gen_libs.chk_crt_dir(
        cfg.log_dir, write=True, create=True, no_print=True)
    log_file = os.path.join(
        cfg.log_dir, cfg.log_file + "." + dtg.get_hack("ymd"))

    if status:
        log = gen_class.Logger(
            log_file, log_file, "INFO",
            "%(asctime)s %(levelname)s %(message)s", "%Y-%m-%dT%H:%M:%SZ")
        log.log_info("Program initialization.")
        msg_dict = check_dirs(args, cfg)

        if msg_dict:
            log.log_err("Validation of configuration directories failed")
            log.log_err(f"Message: {msg_dict}")

        else:
            # Intersect args_array & func_dict to determine function calls
            for func in set(args.get_args_keys()) & set(func_dict.keys()):
                func_dict[func](args, cfg, dtg, log)

    else:
        print("Error: Logger Directory Check Failure")
        print(f"Error Message: {err_msg}")


def main():

    """Function:  main

    Description:  Initializes program-wide used variables and processes command
        line arguments and values.

    Variables:
        dir_perms_chk -> contains directories and their octal permissions
        func_dict -> dictionary list for the function calls or other options
        opt_multi_list -> contains the options that will have multiple values
        opt_req_list -> contains the options that are required for the program
        opt_val_list -> contains options which require values

    Arguments:
        (input) argv -> Arguments from the command line

    """

    dir_perms_chk = {"-d": 5, "-I": 7}
    func_dict = {"-I": insert_data}
    opt_req_list = ["-c", "-d", "-I"]
    opt_val_list = ["-c", "-d", "-I"]

    # Process argument list from command line
    args = gen_class.ArgParser(sys.argv, opt_val=opt_val_list)

    if args.arg_parse2()                                            \
       and not gen_libs.help_func(args, __version__, help_message)  \
       and args.arg_require(opt_req=opt_req_list)                   \
       and args.arg_dir_chk(dir_perms_chk=dir_perms_chk):

        try:
            proglock = gen_class.ProgramLock(
                sys.argv, args.get_val("-y", def_val=""))
            run_program(args, func_dict)
            del proglock

        except gen_class.SingleInstanceException:
            print(f'WARNING:  lock in place for mongo_in with id of:'
                  f'{args.get_val("-y", def_val="")}')


if __name__ == "__main__":
    sys.exit(main())
