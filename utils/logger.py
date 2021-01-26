import logging
import datetime
# Source: https://medium.com/lsc-psd/python%E3%81%AE%E3%83%AD%E3%82%B0%E5%87%BA%E5%8A%9B%E3%83%81%E3%83%BC%E3%83%88%E3%82%B7%E3%83%BC%E3%83%88-%E3%81%99%E3%81%90%E3%81%AB%E4%BD%BF%E3%81%88%E3%82%8B%E3%82%BD%E3%83%BC%E3%82%B9%E3%82%B3%E3%83%BC%E3%83%89%E4%BB%98-4f2ed1449674
# [in] log_folder:  str The directory to output a log file.
# [in] log_level:   str Logging level (DEBUG or INFO)
# [out] logger:     logger instance
def setup_logger(log_folder, log_level_str, modname=__name__):
    dt = datetime.datetime.now()
    filename = '{}.log'.format(dt.strftime('%Y%m%d_%H%M'))

    log_level = getattr(logging, log_level_str.upper(), None)

    logger = logging.getLogger(modname)
    logger.setLevel(log_level)

    sh = logging.StreamHandler()
    sh.setLevel(log_level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    sh.setFormatter(formatter)
    logger.addHandler(sh)

    fh = logging.FileHandler(filename) #fh = file handler
    fh.setLevel(log_level)
    fh_formatter = logging.Formatter('%(asctime)s - %(filename)s - %(name)s - %(lineno)d - %(levelname)s - %(message)s')
    fh.setFormatter(fh_formatter)
    logger.addHandler(fh)

    return logger