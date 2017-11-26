# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 16:39:38 2017

@author: pawel.cwiek
"""
import os
import logging
import copy

logging.basicConfig(level=logging.INFO)

import xlrd

#import alchemyModels as models
from . import workbook_version_mappings as wb_maps
from . import write_csv

dump_not_found_files = r'H:\backUp_pcwiek\prywante\Programming\projects\scan_hvac_workbooks\example_data\files_not_found_version_not_checked.csv'

def check_version(file_path):
    try:
        wb = xlrd.open_workbook(file_path)
        
        # aString is less efficient (but ensures read-only access)
        #aString = open(file_path,'rb').read()
        #wb = xlrd.open_workbook(file_contents=aString)

    except FileNotFoundError:
        logging.info("coundn't find/open file to determine version/if is HVAC sh: %s" % file_path)
        write_csv.to_csv(dump_not_found_files,[file_path],mode='a')
        return None

    version = 'unrecognised'
    # determine workbook version
    try:
        sh = wb.sheet_names()
        sheet_names = ['Design Criteria','AHUs','FANs','HVAC']
        # check if file is actually HVAC spreadsheet
        counter = 0
        for item in sheet_names:
            if item not in sh:
                counter += 1
        if counter >= 2: 
            # if two sheets are missing then it's not HVAC sheet
            return None
        elif counter == 1:
            # if one sheet is missing then it's 'unrecognised'
            return version
        
        # some file created approx 2010-02-16 
        if 'Design Criteria_pol' not in sh:
            return 'older_than_16'    

        # 2.2 - no Architectural Data sheet
        if 'Architectural Data' not in sh:
            version = '2.2'

            sh = wb.sheet_by_name('HVAC')
            cell = sh.cell(13, 91)
            if not cell is xlrd.empty_cell:
                if cell.value == 'WSKAŹNIKOWE STRATY CIEPŁA PRZY UWZGLĘDNIENIU     ZYSKÓW CIEPŁA':
                    return version
            return 'custom ' + version

        # 2.1 - added Minimalna ilosc powietrza swiezego w design criteria

        sh = wb.sheet_by_name('Design Criteria')
        cell = sh.cell(10, 8)
        if not cell is xlrd.empty_cell:
            if cell.value == 'm3/hr':
                version = '2.1'

                sh = wb.sheet_by_name('HVAC')
                cell = sh.cell(13, 77)
                if not cell is xlrd.empty_cell:
                    if cell.value == 'WSKAŹNIKOWE STRATY CIEPŁA PRZY UWZGLĘDNIENIU     ZYSKÓW CIEPŁA':
                        return version
                return 'custom ' + version

        # 2.0 - added PROJEKTOWA ILOŚĆ POWIETRZA TRANSFEROWANEGO in HVAC
        sh = wb.sheet_by_name('HVAC')
        cell = sh.cell(13,16)
        if not cell is xlrd.empty_cell:
            if cell.value == 'PROJEKTOWA ILOŚĆ POWIETRZA TRANSFEROWANEGO':
                version = '2.0'

                sh = wb.sheet_by_name('HVAC')
                cell = sh.cell(13, 77)
                if not cell is xlrd.empty_cell:
                    if cell.value == 'WSKAŹNIKOWE STRATY CIEPŁA PRZY UWZGLĘDNIENIU     ZYSKÓW CIEPŁA':
                        return version
                return 'custom ' + version

        # 1.6 - last option remaining
        sh = wb.sheet_by_name('HVAC')
        cell = sh.cell(13,16)
        if not cell is xlrd.empty_cell:
            if cell.value == 'RODZAJ SYSTEMU WENTYLACJI NAWIEWNEJ' or cell.value == 'TYPE OF SUPPLY VENT SYSTEM':
                return '1.6'

                sh = wb.sheet_by_name('HVAC')
                cell = sh.cell(13, 70)
                if not cell is xlrd.empty_cell:
                    if cell.value == 'WSKAŹNIKOWE STRATY CIEPŁA PRZY UWZGLĘDNIENIU     ZYSKÓW CIEPŁA' or cell.value == 'TOTAL SPECIFIC HEAT LOSSES SUMMARY INCL. WINTER HEAT GAINS':
                        return version
                return 'custom ' + version
    except IndexError:
        version = 'unrecognised'
    return version

def find_mapper(version):
    if version == '1.6':
        mapper = wb_maps.ver16
    elif version == '2.0':
        mapper = wb_maps.ver20
    elif version == '2.1':
        mapper = wb_maps.ver21
    elif version == '2.2':
        mapper = wb_maps.ver22
    else:
        mapper = None

    return mapper

def mapper_to_sheet_and_fields(mapper):

    for key in mapper.keys():
        if key == 'room_types':
            yield (key, 'Design Criteria',mapper[key])
        elif key == 'rooms':
            yield (key, 'HVAC',mapper[key])
        elif key == 'ahus':
            yield (key, 'AHUs',mapper[key])
        elif key == 'fans':
            yield (key,'FANs',mapper[key])

def parse_xls(file_path,version):
#    classes = [models.RoomType, models.Room, models.Ahu, models.Fan]
    mapper = find_mapper(version)
    result_tables = dict()
    logging.debug('parsing %s \n with map: %r' % (file_path, version))

    if mapper == None:
        logging.warning('no map found for version: %r' % version)
        return None

    try:
        wb = xlrd.open_workbook(file_path)

    except FileNotFoundError:
        logging.warning("coundn't find/open file to parse project HVAC data: %s" % file_path)
        return None
        
    for table_name, sh, attrs in mapper_to_sheet_and_fields(mapper):
        try:
            sh = wb.sheet_by_name(sh)
            row = attrs['name'][0]
            table_data = []
        
            while True:
                # check if main attr is present or skip row as being empty
                col = attrs['name'][1]
                if table_name == 'rooms':
                    col = attrs['number'][1]
                cell = sh.cell(row, col)
                if cell is not xlrd.empty_cell:
                    if cell.value != '':
                        # copy dict to write values to
                        row_data = attrs.copy()
                        logging.debug('row_data["name"]: %r'% cell.value)
                        for attr, xy in row_data.items():
    #                        logging.debug('attr, xy: %r, %r' % (attr, xy))
                            # if value is None in map then attribute date is not present in excel version so can skip it
                            if row_data[attr] == None:
    #                            logging.debug('row_data[attr] == None')
                                continue
                            # making value empty to process further
                            row_data[attr] = None
                            # most values are tuples in map - making it all lists
                            if type(xy) != type(list()):
                                xy=[xy]
                            # if values in map were lists in map and have 'add' as first item then logic is to add all values referenced by tuples
                            logging.debug('attr [xy]: %r - %r'% (attr,xy))
                            if xy[0] == 'add':
                                # if adding then have to make value 0 and remove 'add' to proces only tuples
                                xy.pop(0)
    #                            logging.debug('xy after pop("add"): %r'% xy)
                                row_data[attr] = 0
                                for item in xy:
                                    col = item[1]
                                    cell = sh.cell(row,col)
                                    if cell is not xlrd.empty_cell and type(cell.value) != type(str()):
                                        row_data[attr] += cell.value
    #                                    logging.debug('adding steps for %r %r: %r \n cell value: %r' % (row_data['name'],xlrd.cellname(row,col),row_data[attr],cell.value))
                            else:
                            # if cells are not to be added then they will be altered and the last non-empty value will be applied
                                for item in xy:
                                    col = item[1]
                                    cell = sh.cell(row,col)
                                    if cell is not xlrd.empty_cell and cell.value != '':
                                        row_data[attr] = cell.value
                            if row_data[attr] == '' or row_data[attr] == ' ':
                                row_data[attr] = None
                            # converting data to string for database purposes
                            # if row_data[attr] != None:
                                # if attr in to_string:
                                    # row_data[attr] = str(row_data[attr])
                            if row_data[attr] in ['n/a','na','N/A','NA','-']:
                                row_data[attr] = None
                            logging.debug('attribute value taken from %r: %r' % (xlrd.cellname(row,col),row_data[attr]))
                        #logging.debug('entity created from xl row: %r' % row_data)
                        # adding row representing dictionary to list of all rows in this sheet
                        table_data.append(row_data)
                row += 1
                if "2.2" in version and row > 59 and table_name == 'room_types':
                    result_tables[table_name] = table_data
                    break
        except IndexError:
            # if last line in this sheet was reached then the error (which one?) is rised
            # so can then continue with next sheet
            logging.info('# rows recognised for table "%s": %r' % (table_name, len(table_data)))
            result_tables[table_name] = table_data
            continue
        except:
            logging.info('Current xl parsing state of file: %r' % file_path)
            logging.info("sheet: %r , column: %r \n row value in dict: %r , current cell value: %r=%r " % (table_name,attr,row_data[attr],xlrd.cellname(row,col),cell.value))
            raise
#        setattr(mycls,attr,attrs[attr])
#        print(getattr(mycls,attr))
#        result_classes.append(copy.deepcopy(mycls))
#
    return result_tables

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    import pprint
    pp = pprint.PrettyPrinter(indent=2)
    #    cwd = os.getcwd()

    #pp.pprint(files)

    path = r'H:\backUp_pcwiek\prywante\Programming\projects\scan_hvac_workbooks\example_data\real_project\1.6 Airport City Gdansk Calcs MKe 16-12-14 ACG HVAC - ver.D.xls'
    version = '1.6'

#    path = r'H:\backUp_pcwiek\prywante\Programming\projects\scan_hvac_workbooks\example_data\real_project\2.0 Hotel Twarda 2016-03-31_PBa_ HVAC_ver 2.0.xlsm'
#    version = '2.0'
#
#    path = r'H:\backUp_pcwiek\prywante\Programming\projects\scan_hvac_workbooks\example_data\real_project\2.1 Willa Konstancin ArupCalcs MPo 16-11-29 HVAC_Konstancin.xlsm'
#    version = '2.1'
#
#    path = r'H:\backUp_pcwiek\prywante\Programming\projects\scan_hvac_workbooks\example_data\real_project\2.2 WM2W Bilans_HVAC_C07_PWo 2017-01-09.xlsm'
#    version = '2.2'

    parse_xls(path,version)
