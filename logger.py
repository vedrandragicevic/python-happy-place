""" Default logger setup with custom format. """
import logging
import sys

logging.basicConfig(
        format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s (%(filename)s:%(lineno)d)',
        stream=sys.stdout,
        level=logging.INFO)
logger = logging.getLogger("lambda_script")
logger.setLevel(logging.INFO)
