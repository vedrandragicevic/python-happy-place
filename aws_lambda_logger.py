""" Logger setup with custom format for AWS Lambda. """
import logging
import sys


logger = logging.getLogger()
handler = logger.handlers[0]
handler.setFormatter(logging.Formatter('%(asctime)s.%(msecs)03d %(levelname)s %(module)s:%(lineno)d - %(funcName)s: %(message)s'))
logger.setLevel(logging.INFO)
