import logging
import sys
from pythonjsonlogger import jsonlogger


logger = logging.getLogger("logging_script")

logHandler = logging.StreamHandler(stream=sys.stdout)
formatter = jsonlogger.JsonFormatter(
    '%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(lineno)d:\t %(funcName)s: %(message)s ')
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)
