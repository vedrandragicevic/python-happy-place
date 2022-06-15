import csv
import logging
import sys

logging.basicConfig(
        format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
        stream=sys.stdout,
        level=logging.INFO)
logger = logging.getLogger("query_script")
logger.setLevel(logging.INFO)


def write_results_to_csv(results_data: list):
    """ Writes list of lists to a csv file."""
    with open("output.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(results_data)
    logger.info(f"Finished writing to output.csv file.")
