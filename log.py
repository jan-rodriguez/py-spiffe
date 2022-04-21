import logging
import sys

log = logging.getLogger()

def set_up_logging():
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    # create formatter
    formatter = logging.Formatter('%(asctime)s[%(levelname)s](%(filename)s:%(lineno)s) %(message)s', datefmt='%H:%M:%S')

    # Info logging
    ch_info = logging.StreamHandler(sys.stdout)
    ch_info.setLevel(logging.DEBUG)
    # Don't allow anything above info
    ch_info.addFilter(lambda record: record.levelno <= logging.INFO)
    ch_info.setFormatter(formatter)

    # Error/warning logging
    ch_err = logging.StreamHandler()
    ch_err.setLevel(logging.WARNING)
    ch_err.setFormatter(formatter)

    # Add the different handlers
    root_logger.addHandler(ch_info)
    root_logger.addHandler(ch_err)
