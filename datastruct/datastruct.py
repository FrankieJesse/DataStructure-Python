__author__ = 'Frankie'
# from datastruct import Stack
import operator
import string

import datastruct.stack
from datastruct.logger import FinalLogger
from datastruct.stack import Stack




def data_struct():
    logger = FinalLogger.getLogger()
    logger.info("data_struct begin")
    datastruct.stack.stack_test()
    logger.info("data_struct end")
