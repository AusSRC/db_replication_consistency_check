import configparser
import optparse


def parse_config():
    """Get database credentials from config file into a dictionary.

    """
    args = optparse.OptionParser()
    args.add_option('-c', dest="config", default="./config.ini")
    options, arguments = args.parse_args()
    parser = configparser.ConfigParser()
    parser.read(options.config)

    creds = {}
    for db in parser.sections():
        creds[db] = dict(parser[db])

    return creds