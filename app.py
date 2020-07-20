import datetime
from urllib.request import urlopen
import json
import pandas as pd 
import dash 
import dash_core_components as dcc 
import dash_html_components as html 
from dash.dependencies import Input, Output, State
import plotly.express as px 
import plotly.io as pio
from datetime import datetime as dt
import re
import numpy as np
from dateutil import parser
import os

pio.templates.default = "plotly_dark"
# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(
	__name__, 
	# external_stylesheets=external_stylesheets,
	 meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}])
app.config["suppress_callback_exceptions"] = True

server = app.server

url = 'https://www.dosairnowdata.org/dos/AllPostsHistorical.json'
r = urlopen(url)

if r.status !=200:
	print('Site is not available')
text = r.read()
json_ = json.loads(text.decode())
sites = list(json_.keys())
dfraw = pd.DataFrame()

app.layout = html.Div([
	html.Div([
	 	html.Img(id="logo", src=app.get_asset_url("favicon.png"), style={'width': 100, 'height': 'auto'}),
	 	html.H2("A Dash App visualizing Airnow.Gov data"),

		]),
	html.Hr(),
	html.Div([
		html.H3('Inputs'),
		dcc.Dropdown(
		id='select_site',
		# n_clicks=0,
		options=[{'label': i, 'value': i} for i in sites],
		value='Hanoi',
		),
		dcc.RadioItems(id='select_file'),
		html.Hr(),
		html.Div(id='target_file', children='csvfile', title='Link'),
		html.Hr(),
		html.Label('Quality Tags'),
	    dcc.Checklist(id='quality-tags',
	    	options= [
	            {'label': 'Valid', 'value': 'Valid'},
	        ],
	        value=['Valid'],
	    ),

	    html.Label('Select Date Range'),
		dcc.DatePickerRange(
			id='date-picker',
			min_date_allowed = datetime.date(2015,1,1),
			max_date_allowed = datetime.date(2020,7,30),
			initial_visible_month=datetime.date(2020, 3, 1),
			start_date = datetime.date(2019,1,1),
			end_date = datetime.date(2020,1,1),
			display_format='MMM Do, YYYY',
			),
		html.Div(
			id='output-date-picker'),
		html.Hr(),
		html.Div(id='specs-pandas'),
		html.Button(id='submit-button-state', n_clicks=0, children='CHART',
			style={
				'color': 'crimson',
			}),
		html.Hr(),
		]),
	html.Div([
		dcc.Graph(id='pandas-graphic'),
		html.Hr(),
		dcc.Graph(id='pandas-graphic-daily')
		]),
	],
	style={
	'backgroundColor': '#1e2130', 
	'color': 'white'},)

@app.callback(
	Output(component_id='select_file', component_property='options'),
	[Input(component_id='select_site', component_property='value')]
	)
def select_file(selected_city):
	files = json_[selected_city]['monitors'][0]['files']
	tmp = list(files.keys())
	return [{'label': i, 'value': i} for i in tmp]

@app.callback(
	Output(component_id='target_file', component_property='children'),
	[Input(component_id='select_site', component_property='value'),
	Input(component_id='select_file', component_property='value'),
	])
def select_csv(selected_city, target_csv):
	if selected_city is None or target_csv is None:
		return "No file selected"
	output = json_[selected_city]['monitors'][0]['files'][target_csv]
	return '{}'.format(output)

@app.callback(
	[Output('date-picker', 'start_date'),
	Output('date-picker', 'end_date'),
	Output('quality-tags', 'options')],
	[Input('target_file', 'children')]
	)
def update_option(target_file):
	global dfraw
	file = target_file.split('/')[-1]
	print(f'Filename {file}')
	if file not in os.listdir('csv/'):
		dfraw = pd.read_csv(target_file, parse_dates=['Date (LT)'],
                index_col=['Date (LT)'])
		dfraw.to_csv(f'csv/{file}')
	else:
		print('read file from local drive')
		dfraw = pd.read_csv(f'csv/{file}', parse_dates=['Date (LT)'],
                index_col=['Date (LT)'])
	tags = list(dfraw['QC Name'].unique())
	options = [{'label': i, 'value': i} for i in tags]

	return dfraw.index[0], dfraw.index[-1], options


@app.callback(
    Output('output-date-picker', 'children'),
    [Input('date-picker', 'start_date'),
    Input('date-picker', 'end_date')])
def update_output(start_date, end_date):
    string_prefix = 'You have selected: '
    if start_date is not None:
        start_date = dt.strptime(re.split('T| ', start_date)[0], '%Y-%m-%d')
        start_date_string = start_date.strftime('%B %d, %Y')
        string_prefix = string_prefix + 'Start Date: ' + start_date_string + ' | '
    if end_date is not None:
        end_date = dt.strptime(re.split('T| ', end_date)[0], '%Y-%m-%d')
        end_date_string = end_date.strftime('%B %d, %Y')
        string_prefix = string_prefix + 'End Date: ' + end_date_string
    if len(string_prefix) == len('You have selected: '):
        return 'Select a date to see it displayed here'
    else:
        return string_prefix

@app.callback(
    Output('specs-pandas', 'children'),
    [Input('target_file', 'children'),
    Input('date-picker', 'start_date'),
    Input('date-picker', 'end_date')])
def display_info(target_file, start_date, end_date):
	if any([target_file, start_date, end_date]) is None:
		return 'Waiting for the input'
	return f'start: {start_date}, end: {end_date} with file {target_file}'


@app.callback(
    [Output('pandas-graphic', 'figure'),
    Output('pandas-graphic-daily', 'figure')],
    [Input('submit-button-state', 'n_clicks')],
    [State('target_file', 'children'),
    State('date-picker', 'start_date'),
    State('date-picker', 'end_date'),
    State('quality-tags', 'value')])
def display_graph(n_clicks, target_file, start_date, end_date, value):
	if any([target_file, start_date, end_date]) is None:
		return 'Waiting for the input'
	start = parser.parse(start_date)
	end = parser.parse(end_date)
	global dfraw
	df = dfraw.copy(deep=True)
	df = df[df['QC Name'].isin(value)][['Raw Conc.']]
	df = df[(df.index >= start) & (df.index <= end)]
	df2 = df.resample('1D').mean()
	fig = px.line(x=df.index, y=df[df.columns[0]])
	fig_daily = px.line(x=df2.index, y=df2[df2.columns[0]])
	return fig, fig_daily


# @app.callback(
#     [Output('pandas-graphic', 'figure'),
#     Output('pandas-graphic-daily', 'figure')],
#     [Input('target_file', 'children'),
#     Input('date-picker', 'start_date'),
#     Input('date-picker', 'end_date'),
#     Input('quality-tags', 'value')])
# def aqi_segments(target_file, start_date, end_date, value):
# 	if any([target_file, start_date, end_date]) is None:
# 		return 'Waiting for the input'
# 	start = parser.parse(start_date)
# 	end = parser.parse(end_date)
# 	global dfraw
# 	df = dfraw.copy(deep=True)
	
# 	df = df[df['QC Name'].isin(value)][['Raw Conc.']]
# 	# df.index = pd.to_datetime(df.index)
	
# 	print(df.head(3))
# 	print(f'start {start} type {type(start)}, end: {end}')

# 	df = df[(df.index >= start) & (df.index <= end)]
# 	df2 = df.resample('1D').mean()

# 	print(f'filtered: {len(df)}')
# 	print('-'*40)
# 	print(df.head())
# 	fig = px.line(x=df.index, y=df[df.columns[0]])
# 	fig_daily = px.line(x=df2.index, y=df2[df2.columns[0]])

# 	return fig, fig_daily

if __name__ == '__main__':
	app.run_server(debug=True)


