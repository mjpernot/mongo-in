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
        or import into a Mongo database.

    Usage:
        mongo_in.py -c cfg_file -d path
            {-I -b db_name -t coll_name -a name -f {path/file | path/file*} |
             -M -b db_name -t coll_name -a name -f {path/file | path/file*} |
             [-p path}
            [-v | -h]

    Arguments:
        -c cfg_file => Mongo configuration file.  Required arg.
        -d dir path => Config directory path.  Required arg.

        -I => Insert JSON document into database.
            -b db_name => Database Name.
            -t coll_name => Collection Name.
            -f file(s) => JSON document to be inserted.  Requires absolute
                path.
            -a name => Authentication Database Name.  Required for accounts
                not in database (-b option).

        -M => Import JSON file into database.
            -b db_name => Database Name.
            -t coll_name => Collection Name.
            -f file(s) => JSON document to be inserted.  Requires absolute
                path.
            -a name => Authentication Database Name.  Required for accounts
                not in database (-b option).

        -p => Path to Mongo binaries.  Only required if the user
            running the program does not have the Mongo binaries in their path.
        -v => Display version of this program.
        -h => Help and usage message.

        NOTE 1:  -v and/or -h overrides all other options.
        NOTE 2:  -I and -M are XOR options.

    Notes:
        Mongo configuration file format (config/mongo.py.TEMPLATE).  The
            configuration file format is for connecting to a Mongo database or
            replica set for monitoring.  A second configuration file can also
            be used to connect to a Mongo database or replica set to insert the
            results of the performance monitoring into.

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
        mongo_in.py -c mongo -d config -b GMI -t FAC -f /tmp/ins_doc -M
        mongo_in.py -c mongo -d config -b GMI -t FAC -f /tmp/ins_doc -I

":"""
# Python program follows


# Libraries and Global Variables

# Standard
import sys

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


def insert_data(args, **kwargs):

    """Function:  insert_data

    Description:  Insert data into the Mongo database.

    Arguments:
        (input) args -> ArgParser class instance
        (input) kwargs:
            opt_arg -> Contains list of optional arguments for command line
            opt_rep -> Contains list of replaceable arguments for command line

    """

    # Process files
    for fname in args.get_val("-f"):

        with open(fname, mode="r", encoding="UTF-8") as fhdlr:
            data = fhdlr.readline()

            if not isinstance(data, dict):
### Try to convert it here or exit?

            state, msg = mongo_libs.ins_doc(
                mongo, args.get_val("-b"), args.get_val("-t"), data)
STOPPED HERE


def run_program(args, func_dict, **kwargs):

    """Function:  run_program

    Description:  Controls flow of the program.

    Arguments:
        (input) args -> ArgParser class instance
        (input) func_dict -> Dictionary list of functions and options
        (input) kwargs:
            opt_arg -> Contains list of optional arguments for command line
            opt_rep -> Contains list of replaceable arguments for command line

    """

    func_dict = dict(func_dict)

    # Intersect args_array & func_dict to determine which functions to call
    for func in set(args.get_args_keys()) & set(func_dict.keys()):
### Need a status return???
        status = func_dict[func](args, **kwargs)


def main():

    """Function:  main

    Description:  Initializes program-wide used variables and processes command
        line arguments and values.

    Variables:
        dir_perms_chk -> contains directories and their octal permissions
        file_perm_chk -> file check options with their perms in octal
        func_dict -> dictionary list for the function calls or other options
        opt_arg_list-> contains list of optional arguments for command line
        opt_arg_rep -> contains list of replaceable arguments for command line
        opt_multi_list -> contains the options that will have multiple values
        opt_req_list -> contains the options that are required for the program
        opt_val_list -> contains options which require values
        opt_xor_dict -> contains options which are XOR with its values

    Arguments:
        (input) argv -> Arguments from the command line

    """

    dir_perms_chk = {"-d": 5, "-p": 5}
    file_perm_chk = {"-f": 6}
    func_dict = {"-I": insert_data, "-M": import_data}
    opt_arg_list = {
        "-a": "--authenticationDatabase=", "-b": "--db=",
        "-t": "--collection="}
    opt_arg_rep = {"-f": "--file="}
    opt_multi_list = ["-f"]
    opt_req_list = ["-b", "-c", "-d", "-t", "-f"]
    opt_val_list = ["-a", "-b", "-c", "-d", "-f", "-p", "-t"]
    opt_xor_dict = {"-I": ["-M"], "-M": ["-I"]}

    # Process argument list from command line
    args = gen_class.ArgParser(
        sys.argv, opt_val=opt_val_list, multi_val=opt_multi_list)

    if args.arg_parse2()                                            \
       and not gen_libs.help_func(args, __version__, help_message)  \
       and args.arg_require(opt_req=opt_req_list)                   \
       and args.arg_dir_chk(dir_perms_chk=dir_perms_chk)            \
       and args.arg_xor_dict(opt_xor_val=opt_xor_dict)              \
       and args.arg_file_chk(file_perm_chk=file_perm_chk):

        try:
            proglock = gen_class.ProgramLock(
                sys.argv, args.get_val("-y", def_val=""))
            run_program(
                args, func_dict, opt_arg=opt_arg_list, opt_rep=opt_arg_rep)
            del proglock

        except gen_class.SingleInstanceException:
            print(f'WARNING:  lock in place for mongo_in with id of:'
                  f'{args.get_val("-y", def_val="")}')


if __name__ == "__main__":
    sys.exit(main())
