import logging
import csv

from filefunctions import os_functions

def to_csv(path, rows, mode='w'):

    with open(path, mode=mode) as csvfile:

        if rows == []:
            return

        mywriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL, dialect='excel', lineterminator='\n')
        non_valid_names = 0

        for item in rows:
            row = list()
            row.append(item)
            try:
                mywriter.writerow(row)
            except:
                non_valid_names += 1
                continue
        if non_valid_names > 0:
            logging.info("couldn't write lines to csv: %d" % non_valid_names)

    return

def line_from_csv_folder(dir_path):
    for file in os_functions.find_files(dir_path,['csv']):
        with open(file, mode='r') as csvfile:
            logging.info("file opened to get rows from: %s" % file)
            reader = csv.reader(csvfile,delimiter=',', quoting=csv.QUOTE_MINIMAL, dialect='excel', lineterminator='\n')
            for row in reader:
                logging.debug("row returned: %s" % row)
                yield row
