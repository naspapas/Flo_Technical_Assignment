import csv
import logging
import sys

def file_input(file):
    try:
        with open(file, 'r') as file:
            sequential_read = csv.reader(file)
            for row in sequential_read:
                yield row
    except FileNotFoundError:
        logging.error(f"{file} cannot be found. Are you sure file path is correct?")
        sys.exit(1)