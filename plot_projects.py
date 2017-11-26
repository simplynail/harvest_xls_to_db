# -*- coding: utf-8 -*-
"""
Created on Sat Jan 21 15:33:36 2017

@author: pawel
"""
from operator import itemgetter

from pony import orm
from bokeh.io import output_file, show
from bokeh.layouts import layout
from jinja2 import Environment, PackageLoader, select_autoescape

import dbpony.pony_models as models
from dbpony.pony_setup import *
import plot.charts as charts
import plot.plot as plt

html_env = Environment(
    loader=PackageLoader('plot', 'html_templates'),
    autoescape=select_autoescape(['html']))

def all_projects_chart(path):
    data = []    
    with orm.db_session():
        projects = models.Project.select(lambda p: r'\old' not in p.path)
        for p in projects:        
            data.append(p.to_dict(only=['name','number','spreadsheet_version','date_modified','path']))
    raw_data = sorted(data,key=itemgetter('number', 'date_modified'))
    for item in data:
        #print(item['date_modified'])
        item['path'] = item['path'].split('\\')[-1]
        item['day'] = item['date_modified'][-2:]
        item['date_modified'] = item['date_modified'][:-3]
    
    params1 = {'x':'date_modified',
     'y':'spreadsheet_version',
     'agg':'count',
     'color':'spreadsheet_version',
     'tooltips':['spreadsheet_version','date_modified']}
    
    params2 = {'x':'date_modified',
     'y':'day',
     'color':'spreadsheet_version',
     'size':'number',
     'tooltips':['spreadsheet_version','date_modified','day','name','path']}
    
    bar = charts.plt_barchart_grupped(data,params1,'embed')
    scatter = plt.plt_scatter2(data,params2,'embed')
    
    bokeh_out = [bar,scatter]    
    #widgets = [[bar],[scatter]]
    #l = layout(widgets, sizing_mode='stretch_both')
    #bokeh_out = charts.do_output(l,'embed')
    #output_file(path)
    #show(l)
    
    html_template = html_env.get_template('projects.html')
    html = html_template.render(title='title', projects=raw_data, dates = ['2012-11','2012-12'],plots = bokeh_out)
    with open(path,'w') as file:
        file.write(html)
    
if __name__ == '__main__':
    all_projects_chart('projects.html')
    
    data = charts.generate_random_project_data(20)
    #print(data)
    sett={'x':'date',
      'y':'version',
      'size':'values',
      'color':'version',
      'tooltips':['date','version','values']}

    #plt.plt_scatter2(data,sett,'show','scatter2.html')
    #charts.plt_scatter3(data,sett,'show','scatter2.html')