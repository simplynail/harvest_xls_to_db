# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 20:01:52 2017

@author: pawel
"""
import random
from math import pi

from bokeh.plotting import figure
from bokeh.colors import RGB
from bokeh.models import HoverTool

import plot.charts as chrts
        
def plt_scatter2(data,param_dict,mode='object',output_path=None):
    #to_date(data,'%Y-%m-01')    
    tooltips = [HoverTool(tooltips=chrts.create_tooltips(param_dict)),'pan','box_select','wheel_zoom','crosshair','save','reset']
    
    title = "{} by {} (dot colors show {})".format(param_dict['y'].upper(), param_dict['x'].upper(), param_dict['color'].upper())
    
#    size_range = (2,10)
#    v_range = [item[param_dict['size']] for item in data]
#    v_range = (min(v_range),max(v_range))
#    print(v_range)
    
#    p = figure(plot_width=1000, plot_height=600, tools = [tooltips],title=title)
 #              xlabel=param_dict['x'], ylabel=param_dict['y'],
 #           legend_sort_field = 'color',
 #           legend_sort_direction = 'ascending')
    if type(data[0][param_dict['x']]) == str:
        x_rng = chrts.sort_axis(data,param_dict['x'],False,True)        
        #p.x_range = x_rng

    if type(data[0][param_dict['y']]) == str:
        y_rng = chrts.sort_axis(data,param_dict['y'],False,True)        
        #p.y_range = y_rng
        
    p = figure(plot_width=1000, plot_height=600, tools = tooltips, active_scroll="wheel_zoom", title=title,
                x_range=x_rng, y_range=y_rng)
#    xs = []
#    ys = []
#    colors = []
#    sizes = []
#    for row in data:
#        xs.append(row[param_dict['x']])
#        ys.append(row[param_dict['y']])
#        random.seed(row[param_dict['color']])
#        color = (random.randint(0,255),random.randint(0,255),random.randint(0,255),0.7)
#        colors.append(color)
#        row['color'] = color
#        size = size_range[0] + (size_range[1] - size_range[0]) * row[param_dict['size']] * v_range[0]/v_range[1]
#        sizes.append(size)
#        row['size'] = size
    source = chrts.rows_to_columns(data)
    
#    source['size'] = []
#    for value in source[param_dict['size']]:
#        size = size_range[0] + (size_range[1] - size_range[0]) * value * v_range[0]/v_range[1]
#        source['size'].append(size)
#    print(source['size'])
#    
    source['color'] = []
    for value in source[param_dict['color']]:
        random.seed(value)
        color = RGB(random.randint(0,255),random.randint(0,255),random.randint(0,255))
        source['color'].append(color)
    #print(source['color'])
    
    try:
        sum(source[param_dict['size']])
        size = param_dict['size']
    except:
        size=10
        
    p.scatter(param_dict['x'],param_dict['y'],size=size,
              fill_color='color',fill_alpha=0.7,line_color=None,source=source)
              # not working now in bokeh - legend = param_dict['color'])
    #p.scatter(data=data, x=param_dict['x'], y=param_dict['y'], color=color)
#    p = Scatter(data=data, x=param_dict['x'], y=param_dict['y'], color=color, title=title,
#            xlabel=param_dict['x'], ylabel=param_dict['y'],
#            plot_width=1000, plot_height=600, tooltips = tooltips,
#            legend_sort_field = 'color',
#            legend_sort_direction = 'ascending')
    #p.legend.background_fill_alpha = 0.8
    p.xaxis.major_label_orientation = pi/4
    
    return chrts.do_output(p,mode,output_path)
    
if __name__ == '__main__':
    #groupped = aggregate('HVAC_version','Date',data)
    
    data = chrts.generate_random_project_data(30)
    
    sett={'x':'date',
          'y':'version',
          'agg':'version',
          'group':'version',
          'tooltips':['date','version']}
    #plt_barchart_grupped(data,sett,'bar.html')
    plt_scatter2(data,sett,'show','scatter.html')