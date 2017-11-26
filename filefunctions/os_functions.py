# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 16:01:14 2016

@author: pawel.cwiek
"""
import os
import logging
import re
import time

def find_files(dir_path,extensions):
    # returns list of filepaths including only xml files (with subfolders)
    ok_files = []
    for dirpath, diro, files in os.walk(dir_path):
        for file in files:
            if file.split('.')[-1] in extensions:
                file = os.path.join(dirpath,file)
                ok_files.append(file)
    return ok_files


def get_proj_no_and_name(path):
    proj_re = re.search(r'00.\d{6,}-\d{2,}[\s\w]{1,}', path, re.I|re.M)
    if proj_re != None:
        logging.info('project name recognised: %s' % proj_re.group()[3:])
        name_and_number = proj_re.group()[3:].split('-')
        number = name_and_number[0]
        name = name_and_number[1][3:]
        return (number,name)
    return (None,None)

def get_date_modified(path):
    date = os.path.getmtime(path)
    date = time.localtime(date)

    date = time.strftime('%Y-%m-%d',date)
    return date

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    import write_csv
    import pprint
    pp = pprint.PrettyPrinter(indent=2)

    #    cwd = os.getcwd()
#    cwd = r'H:\backUp_pcwiek\prywante\Programming\projects\scan_hvac_workbooks\example_data\references'
#    os.chdir(cwd)
#
#    extensions = ['xls','xlsm']
#    files = find_files(cwd,extensions)
    #pp.pprint(files)
