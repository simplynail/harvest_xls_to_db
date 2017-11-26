# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 16:01:14 2016

@author: pawel.cwiek
"""
import logging
import concurrent.futures as ccfu

from pony import orm

from helpers import simple_timeit as stimeit
from filefunctions import write_csv
from dbpony import pony_functions
from dbpony import pony_models as models

def workers_no():
    from multiprocessing import cpu_count
    try:
        workers = cpu_count()
    except NotImplementedError:
        workers = 1
    return workers

def create_projects_from_csv(dir_path):
    import csv

    for row in write_csv.line_from_csv_folder(dir_path):
        pony_functions.create_project(row[0])
   
def cct_create_projects_from_csv(dir_path):
    import csv
    
    pool = ccfu.ThreadPoolExecutor(workers_no())

    for row in write_csv.line_from_csv_folder(dir_path):
        pool.submit(pony_functions.create_project,(row[0]))
    
    #ccfu.wait(timeout=None, return_when=ccfu.FIRST_EXCEPTION)
    pool.shutdown(wait=True)
    return True       
 
def describe_projects(old=False):
    
    with orm.db_session():   
        projects = orm.select(p.id for p in models.Project)[:]
    
    for project_id in projects:
        pony_functions.parse_project_data(project_id,old)
    
    return True 
    
def cct_describe_projects(old=False):
    
    with orm.db_session():    
        projects = orm.select(p.id for p in models.Project)[:]
    
    workers = workers_no()
    print(workers)
    pool = ccfu.ThreadPoolExecutor(workers)
    
    for project_id in projects:
        pool.submit(pony_functions.parse_project_data,(project_id,old))
    
    #ccfu.wait(timeout=None, return_when=ccfu.FIRST_EXCEPTION)
    pool.shutdown(wait=True)
    return True
    
def do_all(csv_dir,cct = True,old=False):
    if cct:
        if cct_create_projects_from_csv(csv_dir):
            finished = cct_describe_projects(old)
    else:
        if create_projects_from_csv(csv_dir):
            finished = describe_projects(old)
    print(finished)
    if finished:
        pony_functions.relationship_room_to_room_type()
    
    return True
    
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    import pprint
    import profile
    
    pp = pprint.PrettyPrinter(indent=2)
    #    cwd = os.getcwd()
#    cwd = r'H:\backUp_pcwiek\prywante\Programming\projects\scan_hvac_workbooks\example_data\references'
#    os.chdir(cwd)

    csv_dir = r'H:\backUp_pcwiek\prywante\Programming\projects\scan_hvac_workbooks\example_data\proper_hvac_files'
    #profile.run('cc_create_projects_from_csv(csv_dir)')
    
    #with stimeit.profile('do_all cct: '):
        #do_all(csv_dir)
    with stimeit.profile('describe_projects'):
        pony_functions.relationship_room_to_room_type()
    #pony_functions.relationship_room_to_room_type()
    #describe_projects()
    #cct_describe_projects() # took 580s with ThreadPoolExecutor
    #ccp_describe_projects() # ProcessPoolExecutor got stuck - probobly db lock?




