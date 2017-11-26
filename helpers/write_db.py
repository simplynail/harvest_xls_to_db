# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 10:33:17 2016

@author: pawel.cwiek
"""

import os
import sqlite3
from time import strftime
import re


def dump_stats(subs):
    db_path = r"\\global.arup.com\europe\Warsaw\Transfer\PCw\_other\log\mef"
    if not os.path.exists(db_path):
        #print('not existing', db_path)
        return None

    db_existed = os.path.exists(os.path.join(db_path,'db.sqlite'))
    conn = sqlite3.connect(os.path.join(db_path,'db.sqlite'))
    c = conn.cursor()

    if not db_existed:
        # create table
        table_name = 'MasterExcelFile_log'

        # 'field_name': 'field_type'
        # valid field_type: INT, REAL, TEXT, BLOB, NULL (can add NOT NULL at the end)
        # wtihout ID PRIMARY KEY
        # valid
        columns = {'date':'TEXT',
                      'file_count':'INTEGER',
                      'who':'TEXT',
                      'project':'TEXT'}

        columns_str = ', '.join(('{} {}'.format(cn, ct) for cn, ct in columns.items()))
        c.execute('CREATE TABLE {tn} (ID INTEGER PRIMARY KEY, {cns})'.format(tn=table_name, cns=columns_str))

    now = strftime('%Y-%m-%d_%H%M%S')

    usr_str = os.path.expanduser('~')
    usr_re = re.search( r'[a-z]*\.[a-z]*', usr_str, re.I|re.M)
    usr_str = usr_re.group()

    proj_str = subs[0]
    proj_re = re.search(r'00.\d{6,}', proj_str, re.I|re.M)
    if proj_re != None: proj_str = proj_re.group()[3:]
    #print('takie: ', subs[0])
    #print(proj_str)

    c.execute('INSERT INTO MasterExcelFile_log(date,file_count,who,project) values (?,?,?,?)', (now,len(subs),usr_str,proj_str))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    dump_stats('',[r'J:\237000\237423-00 Railway line no. 202'])