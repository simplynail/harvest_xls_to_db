import os
import logging

import write_csv
import xl_functions

def filter_correct_hvac_files(path,csv_dest):
    counter = 0

    for file in write_csv.line_from_csv_folder(path):
        # shouldnt do this way but just to make things faster...
        file = file[0]
        logging.debug('filename retuned from csv row: \n %s' % (file))
        if 'Mechanical' not in file or '~' in file:
            logging.debug('file discarded as potencially not HVAC (not in Mechanical)')
            continue
        logging.debug('version being checked')
        version = xl_functions.check_version(file)
        if version != None:
            logging.debug('This is proper HVAC spreadsheet.\n Version: %s' % version)
            counter +=1
            write_csv.to_csv(csv_dest,[file],mode='a')

    logging.info('No. of correct hvac files written to %s: \n %d' % (csv_dest,counter))


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    import pprint
    pp = pprint.PrettyPrinter(indent=2)

    my_path = r'H:\backUp_pcwiek\prywante\Programming\projects\scan_hvac_workbooks\example_data\found_xl'
    dump_to = r'H:\backUp_pcwiek\prywante\Programming\projects\scan_hvac_workbooks\example_data\proper_hvac_files\filtered_hvac_files.csv'

    filter_correct_hvac_files(my_path,dump_to)

    #pp.pprint(files)