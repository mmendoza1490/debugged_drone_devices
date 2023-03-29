import logging

LOG_FORMAT = "%(asctime)s %(name)-6s %(levelname)-4s %(message)s"
LOG_FILE_DEBUG = "logs.log"
LOG_FILE_ERROR = "error_log.log"
LOG_FILE_INFO = "debugg_result.log"

def get_logger(log_name=""):
    log = logging.getLogger(log_name)
    log_formatter = logging.Formatter(LOG_FORMAT)

    # File Handler debug
    file_handler_debug = logging.FileHandler(LOG_FILE_DEBUG, mode="a")
    file_handler_debug.setFormatter(log_formatter)
    file_handler_debug.setLevel(logging.DEBUG)
    log.addHandler(file_handler_debug)

    # file handler info
    file_handler_info = logging.FileHandler(LOG_FILE_INFO, mode="a")
    file_handler_info.setFormatter(log_formatter)
    file_handler_info.setLevel(logging.INFO)
    log.addHandler(file_handler_info)


    log.setLevel(logging.DEBUG)

    return log