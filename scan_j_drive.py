import os
import logging

from os_functions import find_files
from write_csv import to_csv


def search_j_drive(path):
    if path == 'J':
        path = r'J:\\'
    extensions = ['xls','xlsm']
    possible_files = find_files(path,extensions)

    my_path = r'H:\backUp_pcwiek\prywante\Programming\projects\scan_hvac_workbooks\example_data\found_xl'
    filename = path.split(os.sep)[-1] + '.csv'

    csv_file = os.path.join(my_path,filename)
    logging.info('found %d files in %s' % (len(possible_files), path))

    to_csv(csv_file,possible_files)
    if len(possible_files) > 0:
        logging.info('they were written to: %s' % filename)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    import pprint
    pp = pprint.PrettyPrinter(indent=2)

    #search_j_drive(r'J:\119000')

    #search_j_drive(r'J:\123000')
    #search_j_drive(r'J:\124000')

    #search_j_drive(r'J:\253000')
    #search_j_drive(r'J:\252000')
    #search_j_drive(r'J:\251000')
    #search_j_drive(r'J:\250000')

    #search_j_drive(r'J:\249000')
    #search_j_drive(r'J:\248000')
    #search_j_drive(r'J:\247000')
    #search_j_drive(r'J:\246000')
    #search_j_drive(r'J:\245000')
    #search_j_drive(r'J:\243000')
    #search_j_drive(r'J:\242000')
    #search_j_drive(r'J:\241000')
    #search_j_drive(r'J:\240000')

#    search_j_drive(r'J:\239000')
#    search_j_drive(r'J:\238000')
#    search_j_drive(r'J:\237000')
#    search_j_drive(r'J:\236000')
#    search_j_drive(r'J:\235000')
#    search_j_drive(r'J:\234000')
#    search_j_drive(r'J:\233000')
#    search_j_drive(r'J:\232000')
#    search_j_drive(r'J:\231000')
#    search_j_drive(r'J:\230000')

#    search_j_drive(r'J:\229000')
#    search_j_drive(r'J:\228000')
#    search_j_drive(r'J:\227000')
#    search_j_drive(r'J:\226000')
#    search_j_drive(r'J:\225000')
#    search_j_drive(r'J:\224000')
#    search_j_drive(r'J:\223000')
#    search_j_drive(r'J:\222000')
#    search_j_drive(r'J:\221000')
#    search_j_drive(r'J:\220000')

#    search_j_drive(r'J:\219000')
#    search_j_drive(r'J:\218000')
#    search_j_drive(r'J:\217000')
#    search_j_drive(r'J:\216000')
#    search_j_drive(r'J:\215000')
#    search_j_drive(r'J:\214000')
#    search_j_drive(r'J:\213000')
#    search_j_drive(r'J:\212000')
#    search_j_drive(r'J:\211000')

#    search_j_drive(r'J:\200000')


    #search_j_drive(r'H:\backUp_pcwiek\prywante\Programming\projects\scan_hvac_workbooks\example_data\references\found_xl')

    #    cwd = os.getcwd()
#    cwd = r'H:\backUp_pcwiek\prywante\Programming\projects\scan_hvac_workbooks\example_data\references'
#    os.chdir(cwd)
#
#    extensions = ['xls','xlsm']
#    files = find_files(cwd,extensions)
    #pp.pprint(files)