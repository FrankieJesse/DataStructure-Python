'''
@author : Frankie
'''
import logging.handlers
class FinalLogger:
    logger = None
    levels = {
        'n' : logging.NOTSET,
        'd' : logging.DEBUG,
        'i' : logging.INFO,
        'w' : logging.WARN,
        'e' : logging.ERROR,
        'c' : logging.CRITICAL
    }
    log_level = 'd'
    log_file = 'frankie.log'
    log_max_bytes = 10 * 1024 * 1024
    log_backup_count = 5

    @staticmethod
    def getLogger():
        if FinalLogger.logger is not None:
            return FinalLogger.logger
        FinalLogger.logger = logging.Logger("logger.FinalLogger")
        log_file_handler = logging.handlers.RotatingFileHandler(filename = FinalLogger.log_file,
                                                           maxBytes = FinalLogger.log_max_bytes,
                                                           backupCount = FinalLogger.log_max_bytes)
        log_console_handler = logging.StreamHandler()
        log_fmt = logging.Formatter("[%(levelname)s][%(funcName)s][%(asctime)s]%(message)s")
        log_file_handler.setFormatter(log_fmt)
        log_console_handler.setFormatter(log_fmt)
        # FinalLogger.logger.addHandler(log_file_handler)
        FinalLogger.logger.addHandler(log_console_handler)
        FinalLogger.logger.setLevel(FinalLogger.levels.get(FinalLogger.log_level))
        return FinalLogger.logger
