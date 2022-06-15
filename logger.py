""" Default logger setup """
import logging
import sys

logging.basicConfig(
        format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
        stream=sys.stdout,
        level=logging.INFO)
logger = logging.getLogger("query_script")
logger.setLevel(logging.INFO)
