from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.layouts import row, column
from bokeh.models import Select

zip_codes = ['11385', '10039', '11230', '11249', '10040', '11434', '11368',\
       '10304', '10014', '11422', '11101', '11418', '11217', '10037',\
       '11432', '11377', '11234', '11218', '11414', '10472', '10454',\
       '10036', '11236', '11419', '11206', '11102', '10001', '11203',\
       '11367', '11232', '10029', '11228', '11423', '11226', '10459',\
       '11238', '11355', '11364', '11360', '11357', '10003', '10453',\
       '11361', '11213', '10463', '10467', '10473', '11204', '11222',\
       '10027', '11210', '10466', '10016', '11220', '11233', '11201',\
       '11417', '11435', '11415', '10314', '11105', '10025', '10282',\
       '10469', '11354', '10065', '11209', '10452', '11004', '11214',\
       '11369', '11221', '11429', '10032', '11421', '11427', '11378',\
       '11211', '11370', '10031', '10038', '11420', '10457', '11237',\
       '11208', '10303', '10033', '11373', '11216', '11411', '10462',\
       '10024', '10011', '11223', '11104', '10002', '10468', '11374',\
       '11225', '11372', '10022', '11362', '11229', '10017', '11207',\
       '11379', '10044', '11219', '11366', '11365', '10301', '11413',\
       '11412', '10019', '10009', '10306', '11103', '10458', '11106',\
       '10305', '10023', '10012', '10010', '11231', '11205', '10075',\
       '11001', '10013', '11212', '10312', '11375', '11433', '10465',\
       '11358', '10451', '10471', '10461', '10456', '11692', '11215',\
       '10460', '11694', '10021', '10035', '10128', '10004', '10168',\
       '11416', '11224', '10028', '11239', '11691', '10309', '10308',\
       '10034', '11235', '11426', '10475', '10455', '11693', '11428',\
       '10310', '11436', '10302', '11356', '10470', '10474', '10026',\
       '11109', '10464', '11363', '10018', '10030', '10005', '10007',\
       '10280', '10307', '10006', '11430', '11040', '10020', '10169',\
       '10121', '10041', '10111', '11697', '10069', '10162', '10281',\
       '10120', '10123', '10278', '10105', '10045', '10106', '10103',\
       '10165', '11005', '10000', '10122', '10118', '10173', '11359',\
       '10177', '10178', '12345', '10171', '10119', '10172', '10279',\
       '11695', '11371', '10151', '11242', '10154', '10152', '10271',\
       '10110', '10155', '10170', '10166', '10158', '10179', '11251',\
       '10055', '10112', '11241', '10107', '10176', '10115', '10174',\
       '00083', '10153', '10048', '10167', '10175', '07114', '20005',\
       '08542']

line_chart = figure(plot_width=1000, plot_height=400, x_axis_type="datetime",
                    title="Google Stock Prices from 2005 - 2013")

line_chart.line(
                x="date", y="open",
                line_width=0.5, line_color="dodgerblue",
                legend_label = "open",
                source=google_df
                )

line_chart.xaxis.axis_label = 'Time'
line_chart.yaxis.axis_label = 'Price ($)'

line_chart.legend.location = "top_left"

### Widgets Code Starts ################################
drop_zipcode1 = Select(title="X-Axis-Dim",
                    options=iris.feature_names,
                    value=iris.feature_names[0],
                    width=225)

drop_zipcode2 = Select(title="Y-Axis-Dim",
                    options=iris.feature_names,
                    value=iris.feature_names[1],
                    width=225)


##### Code to Update Charts as Per Widget  State Starts #####################

def update_line_chart(attrname, old, new):
    '''
        Code to update Line Chart as Per Check Box Selection
    '''
    line_chart = figure(plot_width=1000, plot_height=400, x_axis_type="datetime",
                        title="Google Stock Prices from 2005 - 2013")

    for option in checkbox_grp.active:
        line_chart.line(
                x="date", y=checkbox_options[option],
                line_width=0.5, line_color=price_color_map[checkbox_options[option]],
                legend_label=checkbox_options[option],
                source=google_df
            )

    line_chart.xaxis.axis_label = 'Time'
    line_chart.yaxis.axis_label = 'Price ($)'

    line_chart.legend.location = "top_left"

    layout_with_widgets.children[0].children[1] = line_chart

#### Registering Widget Attribute Change with Methods Code Starts ############# 
drop_zipcode1.on_change("active", update_line_chart)
drop_zipcode2.on_change("active", update_line_chart)

####### Widgets Layout #################
layout_with_widgets = column(line_chart)

############ Creating Dashboard ################
curdoc().add_root(layout_with_widgets)