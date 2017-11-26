# -*- coding: utf-8 -*-
"""
Created on Wed Jan 11 15:00:58 2017

@author: pawel.cwiek
"""
import os
import logging
import copy
import time

from pony import orm

from . import pony_models as models
from filefunctions import os_functions
from filefunctions import xl_functions
from filefunctions import workbook_version_mappings as mappings

from pony_setup import *

class BreakIt(Exception): pass

def change_type(class_def, attr_name, value):
    attr_type = getattr(class_def,attr_name).py_type.__name__
    if attr_type == 'str':
        try:
            if value is not None:
                value = str(value)
        except:
            return value
    elif attr_type in ['Decimal','float']:
        try:
            value = value.replace(',','.')
            value = float(value)
        except:
            return value
    
    return value

def write_parse_error(project_id,message):   
    with orm.db_session():
        project = models.Project[project_id] 
        project.debug = message
        project.show = False
    return None

def create_project(file_path, overwrite=False):
    '''
    checks if file is valid HVAC spreadsheet file
    and if so saves Project data into database
    '''
    with orm.db_session():
        project = models.Project.get(path = file_path)
    
        if project == None:
            project = models.Project(path = file_path)
        elif overwrite == False:
            return None
    
        version = xl_functions.check_version(file_path)
        project.spreadsheet_version = version
        project.debug = None
        project.number, project.name = os_functions.get_proj_no_and_name(file_path)
        project.date_modified = os_functions.get_date_modified(file_path)  
        
        if version == None:
            return None
        
        version_map = 'ver' + version.replace('.','')
        if version_map in dir(mappings):
            project.xl_mapping_present = True

def parse_project_data(project_id,old=False):
    '''
    get rest of project data from excel file
    based on Project instance
    '''
    with orm.db_session():

        project = models.Project[project_id]
    
        xl_path = project.path
        version = project.spreadsheet_version
        detail_classes = [models.RoomType, models.Room, models.Ahu, models.Fan]
    
        if project.xl_mapping_present == False:
            logging.info('No mapping available for %s\n file:\n %s'%(version, xl_path))
            return None
        
        # parse files that are in 'old' folders?
        if r'\old' in xl_path.lower():
            project.reparse = False
        
        if project.reparse == False:
            logging.info('Reparse flag False for file:\n %s'%(xl_path))
            return None
    
        xl_path = project.path
        tables_data = xl_functions.parse_xls(xl_path,version)
        if tables_data == None:
            return None
        detail_entities = []

        for cls_template in detail_classes:
            # select data for current class template
            data = tables_data[cls_template._table_]

            #iterate over each row found in xl for current class template
            for row in data:
                entity = None
                key=None
                selected = []
                
                # set column name that is unique for current sheet
                if cls_template._table_ != 'rooms':
                    key = 'name'
                    val = change_type(cls_template,key,row[key])
                    #selected = list(cls_template.select(lambda c: c.name == val))
                    entity = orm.select(c for c in cls_template if c.name == val and c.project.id == project_id).get()
                else:
                    key = 'number'
                    val = change_type(cls_template,key,row[key])
                    #selected = list(cls_template.select(lambda c: c.number == val))
                    entity = orm.select(c for c in cls_template if c.number == val and c.project.id == project_id).get()
                
                # find if current row is already present in DB (based on unique column)
                #selected = list(cls_template.select(lambda c: getattr(c, key) == row[key]))
                

                #entity = cls_template.filter(getattr(cls_template,key)==row[key]).one_or_none()
                try:
                    if entity is None:
                        attr = key
                        required = dict()
                        required[key] = change_type(cls_template,key,row[key])
                        entity = cls_template(project = project, **required)
                
                    for attr,value in row.items():
                        value = change_type(cls_template,attr,value)
                        setattr(entity,attr,value)
                except:
                    orm.rollback()
                    message = 'error parsing xl details: ver:%r , sh|row: %r | %r, col: %r' % (version,cls_template._table_,row[key],attr)
                    logging.info('current file: %s \n %r' % (xl_path,message))
                    
                    return write_parse_error(project_id, message)
                
                #logging.debug('class entity created for %r: %r' % (row[key],entity))
                detail_entities.append(entity)
                #session.add(entity)
    
            logging.info('# of class entities created/updated: %r\n' % (len(detail_entities)))
            
            modified = os_functions.get_date_modified(xl_path)
            project.date_modified = modified
            project.date_parsed = time.strftime('%Y-%m-%d')
            project.debug = None
            project.reparse = False
            project.show = True
    
        return None

def relationship_room_to_room_type():
    with orm.db_session():
        rooms = orm.select(r for r in models.Room)
        try:
            for r in rooms:
            # TODO - not finding all room_types
                room_type = orm.select(rt for rt in models.RoomType if rt.name == r.room_type_name and rt.project == r.project).get()
                if room_type is not None:
                    r.room_type = room_type
                else:
                    logging.info('No room_type found for %r: \n room name: %r - %r (room_type_name: %r)' % (r.project.path, r.number, r.name, r.room_type_name))
        except Exception as e:
            logging.info('Current file: %s: \n room name: %r - %r (room_type_name: %r)' % (r.project.path, r.number, r.name, r.room_type_name))
            r.project.debug = e
            
            
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    import os
    cwd = r'H:\backUp_pcwiek\prywante\Programming\projects\scan_hvac_workbooks'
    os.chdir(path)
    #create_project(r'H:\backUp_pcwiek\prywante\Programming\projects\scan_hvac_workbooks\example_data\real_project\1.6 Airport City Gdansk Calcs MKe 16-12-14 ACG HVAC - ver.D.xls')
    #describe_projects()
    #relationship_room_to_room_type()
    #session = Session()
    #szef = session.query(models.Room).filter_by(id=28).first()
    #test_change_type()
    pass

