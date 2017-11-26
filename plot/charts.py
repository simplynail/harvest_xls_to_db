# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 20:01:52 2017

@author: pawel
"""
from bokeh.plotting import figure

from bokeh.charts import Bar, Scatter
from bokeh.charts import output_file, show, save
from bokeh.embed import components
from bokeh.models.ranges import FactorRange

#from bokeh.models import HoverTool

bokeh_js_str = '''
    <link href="http://cdn.pydata.org/bokeh/release/bokeh-0.12.0.min.css" rel="stylesheet" type="text/css">
    <script src="http://cdn.pydata.org/bokeh/release/bokeh-0.12.0.min.js"></script>'''
bokeh_js_widget_str = '''<link
    href="http://cdn.pydata.org/bokeh/release/bokeh-widgets-0.12.0.min.css" rel="stylesheet" type="text/css">
    <script src="http://cdn.pydata.org/bokeh/release/bokeh-widgets-0.12.0.min.js"></script>'''

def generate_random_project_data(rows_no):
    import random
    versions = ['1.6','2.0','2.1','2.2']

    selects = []
    for a in range(rows_no):
        month = '%2d'%random.randrange(1,12)
        year = random.randrange(2010,2016)
        version = random.choice(versions)
        number = random.randrange(210000,250000,10)
        date = '%d-%s'%(year,month)
        values = random.randrange(1,100)
        item = {'version':version,'number':number,'date':date,'values':values}
        selects.append(item)
    return selects

def rename_filter_columns(selects, mask_dict):
    # mask = {'version':'HVAC_version','date':'Date','number':'Number'}

    data = []
    for entity in selects:
        item = dict()
        for key, value in mask.items():
            #getattr        
            item[value] = entity[key]
        data.append(item)
    return data

def aggregate(group,series,data_dict):
    cat=set()
    for item in data_dict: cat.add(item[group])
    cat = list(cat)
    
    xs=set()
    for item in data: xs.add(item[series])
        
    uxs = {}
    for item in xs: uxs[item] = 0
    
    sums = {}
    for c in cat:
        current_dict = uxs
        for item in data:
            if item[group] == c: current_dict[item[series]] += 1
        sums[c] = current_dict
    return sums

def create_tooltips(param_dict):
    '''
    creates a list for proper configuring the HoverTool/tooltips
    '''
    tooltips = []
    for value in param_dict['tooltips']:      
#        if value in param_dict['x']:
#            code = '$x'
#        else:
#            code = '@%s' % value
        code = '@%s' % value
        param = (value,code)
        tooltips.append(param)
    #tooltips.append(('y','$y'))
    #print(tooltips)
    return tooltips
   
def do_output(p,mode,output_path=''):
    if mode == 'object':
        return p
    elif mode == 'embed':
        script, div = components(p)
        return [script, div]
    else:
        output_file(output_path)
        if mode == 'show':
            show(p)
        elif mode =='save':
            save(p)
            return True

def sort_axis(data,key,reverse=False,continous=True):
    '''
    returns list of strings to be used as axis label ticks
    data - list of dicts with all the data rows
    key - str(): 'key' to take out the values from each item of list to use as axis range
    reverse - True/False if to sort in reverse order
    continous - True/False - for 'number like' values - if only use the values in rows or to create mid-values in range of min/max value
    '''
    values = [value[key] for value in data]  
    values = list(set(values))
    if 'date' in key and continous:
        from itertools import product
        temp = [[] for item in values[0].split('-')]
        for i in values:
            temp[0].append(int(i.split('-')[0]))
        if len(temp) >= 2:
            temp[1].extend([1,12])
        if len(temp) >= 3:
            temp[2].extend([1,31])
        for no,grp in enumerate(temp):
            temp[no]=['%02d'%i for i in range(min(grp),max(grp)+1)]
        temp = list(product(*temp))
        for no,item in enumerate(temp):
            temp[no] = '-'.join(item)            
        values = temp
    elif continous:
        try:
            temp=[]
            for item in values:
                temp.append(int(item))
            values = ['%02d'%i for i in range(min(temp),max(temp)+1)]
        except:
            pass
    values.sort(reverse=reverse)    
    return FactorRange(factors=values)

def to_date(data,formatting='%Y-%m-%d'):
    '''
    converts string to datetime object
    '''
    import time
    for item in data:
        for key,value in item.items():
            if 'date' in key:
                item[key] = time.strptime(value,formatting)   

def rows_to_columns(data):
    output = dict()
    for key in data[0].keys():
        output[key] = []
    for row in data:
        for key,value in row.items():
            output[key].append(value)
    return output
        
def plt_barchart_grupped(data,param_dict,mode='object',output_path=None):
    '''
    data: rows = list of dicts(): keywords with neat naming straight to put in charts
    param_dict: dictionary with settings as follows:
    {'x':'name of column to put on x axis',
     'y':'name of column to put in y axis',
     'agg':'name of aggregate function: 'sum'/'count' /etc',
     'color':'name of name of column to create siloses by/to apply aggr funct',
     'tooltips':['list() of strings with column names to put in tooltip cloud']}
    mode: 'object'/'save'/'show'/'embed' - either returns plot object / saves to path + returns True / saves to path and shows plot
    output_path: string with html ext to save chart to. If None then emmbed is returned
    returns: True(saved to file) or emmbed data code
    '''
    # tooltips=[
        # ("Date", "$x"),
        # ("version", "@HVAC_version")]


    # p = Bar(data, label='Date', values='HVAC_version', agg='count', group='HVAC_version',
            # title="Median MPG by YR, grouped by ORIGIN", legend='bottom_right', bar_width=3.0,
            # plot_width=1000, plot_height=400, tooltips = tooltips)
    # p.legend.background_fill_alpha = 0.8

    # output_file("bar.html")

    # show(p)
    #to_date(data,'%Y-%m-01')    
    tooltips = create_tooltips(param_dict)
    
    title = "{} of {} by {}, grouped by {}".format(param_dict['agg'], param_dict['y'].upper(), param_dict['x'].upper(), param_dict['color'].upper())
    
    p = Bar(data=data, label=param_dict['x'], values=param_dict['y'], agg=param_dict['agg'], group=param_dict['color'],
            title=title, legend='bottom_right', bar_width=3.0,
            plot_width=1000, plot_height=600, tooltips = tooltips)
            #legend_sort_field = param_dict['group'])
    p.legend.background_fill_alpha = 0.8
    
    if type(data[0][param_dict['x']]) == str:
        x_rng = sort_axis(data,param_dict['x'],False,True)        
        p.x_range = x_rng

    if type(data[0][param_dict['y']]) == str:
        y_rng = sort_axis(data,param_dict['y'],False,True)        
        p.y_range = y_rng
    
    return do_output(p,mode,output_path)
        
        
def plt_scatter1(data,param_dict,mode='object',output_path=None):
    #to_date(data,'%Y-%m-01')    
    tooltips = create_tooltips(param_dict)
    
    title = "{} by {} (dot colors show {})".format(param_dict['y'].upper(), param_dict['x'].upper(), param_dict['color'].upper())
    
    try:
        color = param_dict['color']
    except KeyError:
        color = 'red'
    
#    p = figure(tooltips=tooltips)
#    p.scatter(data=data, x=param_dict['x'], y=param_dict['y'], color=color, title=title,
#            xlabel=param_dict['x'], ylabel=param_dict['y'],
#            plot_width=1000, plot_height=600, tooltips = tooltips,
#            legend_sort_field = 'color',
#            legend_sort_direction = 'ascending')
    p = Scatter(data=data, x=param_dict['x'], y=param_dict['y'], color=color, title=title,
            xlabel=param_dict['x'], ylabel=param_dict['y'],
            plot_width=1000, plot_height=600, tooltips = tooltips,
            legend_sort_field = 'color',
            legend_sort_direction = 'ascending')
    p.legend.background_fill_alpha = 0.8
    
    try:
        p.radius = param_dict['size']
    except KeyError:
        try:
            p.marker=param_dict['color']
        except KeyError:
            pass
    
    if type(data[0][param_dict['x']]) == str:
        x_rng = sort_axis(data,param_dict['x'],False,True)        
        p.x_range = x_rng

    if type(data[0][param_dict['y']]) == str:
        y_rng = sort_axis(data,param_dict['y'],False,True)        
        p.y_range = y_rng
        
    return do_output(p,mode,output_path)
    
def plt_scatter3(data,param_dict,mode='object',output_path=None):
    #to_date(data,'%Y-%m-01')    
    tooltips = create_tooltips(param_dict)
    
    title = "{} by {} (dot colors show {})".format(param_dict['y'].upper(), param_dict['x'].upper(), param_dict['color'].upper())
    
    try:
        color = param_dict['color']
    except KeyError:
        color = 'red'
    
    try:
        p = Scatter(data=data, x=param_dict['x'], y=param_dict['y'], color=color, title=title,
        xlabel=param_dict['x'], ylabel=param_dict['y'],
        plot_width=1000, plot_height=600, tooltips = tooltips,
        legend_sort_field = 'color', legend_sort_direction = 'ascending',
        size = param_dict['size'])

    except KeyError:
        try:
            p = Scatter(data=data, x=param_dict['x'], y=param_dict['y'], color=color, title=title,
            xlabel=param_dict['x'], ylabel=param_dict['y'],
            plot_width=1000, plot_height=600, tooltips = tooltips,
            legend_sort_field = 'color', legend_sort_direction = 'ascending',
            marker = param_dict['color'])
        except KeyError:
            p = Scatter(data=data, x=param_dict['x'], y=param_dict['y'], color=color, title=title,
            xlabel=param_dict['x'], ylabel=param_dict['y'],
            plot_width=1000, plot_height=600, tooltips = tooltips,
            legend_sort_field = 'color', legend_sort_direction = 'ascending')
    
    p.legend.background_fill_alpha = 0.8
    
    if type(data[0][param_dict['x']]) == str:
        x_rng = sort_axis(data,param_dict['x'],False,True)        
        p.x_range = x_rng

    if type(data[0][param_dict['y']]) == str:
        y_rng = sort_axis(data,param_dict['y'],False,True)        
        p.y_range = y_rng
        
    return do_output(p,mode,output_path)
    
if __name__ == '__main__':
    #groupped = aggregate('HVAC_version','Date',data)
    
    data = generate_random_project_data(30)
    
    sett={'x':'date',
          'y':'version',
          'agg':'version',
          'group':'version',
          'tooltips':['date','version']}
    #plt_barchart_grupped(data,sett,'bar.html')
    plt_scatter1(data,sett,'show','scatter.html')