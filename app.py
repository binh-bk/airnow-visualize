import datetime
from urllib.request import urlopen
import json
import pandas as pd 
import dash 
import dash_core_components as dcc 
import dash_bootstrap_components as dbc
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
app = dash.Dash(
	__name__, 
	external_stylesheets=[dbc.themes.BOOTSTRAP],
	meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}])
# app.config["suppress_callback_exceptions"] = True

server = app.server


dfraw = pd.DataFrame() # empty DataFrame

def get_json():
	url = 'https://www.dosairnowdata.org/dos/AllPostsHistorical.json'
	r = urlopen(url)
	if r.status !=200:
		print('Site is not available')
	text = r.read()
	json_ = json.loads(text.decode())
	sites = list(json_.keys())
	return sites, json_

sites, json_ = get_json()
def generate_header():
	return html.Div(
		children=[
			html.Img(
				src=app.get_asset_url("favicon.png"), 
				style={
				'width': 30, 
				'height': 30,
				'pading': '2px 2px'
				}),
			html.H2(
				"A Dash App visualizing Airnow.gov data",
				style={
					'padding': '5px 5px',
					'margin': '0px 0px',
					'text': 'center',
					'color': 'blue',
					}
				)],
		style={
			'width': '100%',
			'padding': '2px 2px',
			'display': 'flex',
			'flex-direction': 'row-reverse',
			'flex-wrap': 'wrap',
			'align-items': 'center',
			},
		)
def generate_footer():
	return html.Div(
		children=[
			html.Img(
				src=app.get_asset_url("favicon.png"), 
				style={
				'width': 30, 
				'height': 30,
				'pading': '2px 2px'
				}),
			html.H2(
				"A Dash App visualizing Airnow.gov data",
				style={
					'padding': '5px 5px',
					'margin': '0px 0px',
					'text': 'center',
					'color': 'blue',
					}
				)],
		style={
			'width': '100%',
			'padding': '2px 2px',
			'display': 'flex',
			'flex-direction': 'row-reverse',
			'flex-wrap': 'wrap',
			'align-items': 'center',
			},
		)
def airnow_select():
	return html.Div([
		html.H3('Inputs'),
		dcc.Dropdown(
		id='select_site',
		options=[{'label': i, 'value': i} for i in sites],
		value='Hanoi',
		),
		dcc.RadioItems(id='select_file'),
		html.H5('File info'),
		html.Link(
			id='target_file', 
			children=[html.P('Link')],
			href='#'),
		html.Hr(),
		html.Label('Quality Tags'),
	    dcc.Checklist(
	    	id='quality-tags',
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
		html.Hr(),
		html.Div(id='specs-pandas'),
		html.Button(id='submit-button-state', n_clicks=0, children='CHART',
			style={
				'color': 'crimson',
			}),
		],
		style={
		'width': '100%',
		})

def generate_input():
	return 	html.Div(
		children=[
			airnow_select(),
			# generate_tab(head_str='First-First Tab'),
			],
		style={
			'width': '50%',
			'height': '90%',
			'border': 'solid white 1px',
			'display': 'flex',
			'align-items': 'flex-start',
			'flex-direction': 'column',
			'padding': '2px 2px',
		})

def summary_tab():
	return html.Div(
		children=[
			dcc.Graph(id='hist-graph'),
			dcc.Graph(id='pie-graph'),
			],
		style={
			# 'width': '80%',
			# 'height': '60%',
			'border': 'solid white 2px',
			'display': 'flex',
			'align-items': 'flex-start',
			})
def graph_tab():
	return html.Div(
		children=[
			dcc.Graph(id='pandas-graphic'),
			dcc.Graph(id='pandas-graphic-daily'),
			],
		style={
			# 'width': '80%',
			# 'height': '40%',
			'border': 'solid white 2px',
			'display': 'flex',
			'align-items': 'flex-start',
		})


def generate_tab(head_str='Example Tab', class_=None):
	return 	html.Div(
		# className='container',
		children=[
			html.H2(head_str),
			html.Img(
				src=app.get_asset_url("favicon.png"), 
				style={'width': 60, 'height': 60}
				),
		 	html.H2("A Dash App visualizing Airnow.gov data"),
		 	html.P(children="The app is under developing, and the layout is not in place. Just yet!\
		 					The app is under developing, and the layout is not in place. Just yet!\
		 					The app is under developing, and the layout is not in place. Just yet!\
		 					The app is under developing, and the layout is not in place. Just yet!, and to make the like abit longer"),
			],)



app.layout = html.Div(
	id='big-app-container',
	children=[
		generate_header(),
		html.Div(
			style={
			'width': '100%',
			'border': 'solid white 2px',
			'margin': '2px 2px',
			}),
		html.Div([
			generate_input(),
			html.Div(
				id='main-display',
				children=[
					summary_tab(),
					graph_tab(),
					],
				style={
					# 'heigh': '960px',
					'display': 'flex',
					'flex-direction': 'column',
					}),
			],
			style={
				'display': 'flex',
				'flex-direction': 'row',
				}

			),
		html.Div(
			id='hl-near-bottom',
			style={
				'width': '100%',
				'border': 'solid red 2px',
				'margin': '2px 2px',
				'display': 'flex',
				'flex-direction': 'row',
				}),
		generate_footer(),
		],
	style={
		'border': 'solid white 1px',
		}
	)


# children=[
# 	html.Div(
# 		className='container',
# 		children=[
# 			html.Img(src=app.get_asset_url("favicon.png"), 
# 				style={'width': 60, 'height': 'auto'}
# 				),
# 		 	html.H2("A Dash App visualizing Airnow.gov data"),
# 		 	html.P(children="The app is under developing, and the layout is not in place. Just yet!")
# 			]),
# 			html.Div(
# 				className='columns',
# 				children=[
# 				generate_tab(head_str='Second Tab'),
# 				generate_tab(head_str='Third Tab'),
# 				]),
# 			html.Hr(),
# 			html.Hr(),
# 			generate_tab(head_str='Fourth Tab')
# ],

# html.Div([

# 	html.Hr(),
# 	html.Div([
# 		html.H3('Inputs'),
# 		dcc.Dropdown(
# 		id='select_site',
# 		# n_clicks=0,
# 		options=[{'label': i, 'value': i} for i in sites],
# 		value='Hanoi',
# 		),
# 		dcc.RadioItems(id='select_file'),
# 		html.Hr(),
# 		# html.Div(id='target_file', children='csvfile', title='Link'),
# 		# html.Hr(),
# 		html.Label('Quality Tags'),
# 	    dcc.Checklist(id='quality-tags',
# 	    	options= [
# 	            {'label': 'Valid', 'value': 'Valid'},
# 	        ],
# 	        value=['Valid'],
# 	    ),
# 	    html.Hr(),
# 	    html.Label('Select Date Range'),
# 		dcc.DatePickerRange(
# 			id='date-picker',
# 			min_date_allowed = datetime.date(2015,1,1),
# 			max_date_allowed = datetime.date(2020,7,30),
# 			initial_visible_month=datetime.date(2020, 3, 1),
# 			start_date = datetime.date(2019,1,1),
# 			end_date = datetime.date(2020,1,1),
# 			display_format='MMM Do, YYYY',
# 			),
# 		# html.Div(
# 		# 	id='output-date-picker'),
# 		html.Hr(),
# 		# html.Div(id='specs-pandas'),
# 		html.Button(id='submit-button-state', n_clicks=0, children='CHART',
# 			style={
# 				'color': 'crimson',
# 			}),
# 		html.Hr(),
# 		]),
# 	html.Div([
# 		dcc.Graph(id='pandas-graphic'),
# 		html.Hr(),
# 		dcc.Graph(id='pandas-graphic-daily')
# 		]),
# 	],
# 	style={
# 	'backgroundColor': '#1e2130', 
# 	'color': 'white'},)

@app.callback(
	Output(component_id='select_file', component_property='options'),
	[Input(component_id='select_site', component_property='value')]
	)
def select_file(selected_city):
	files = json_[selected_city]['monitors'][0]['files']
	tmp = list(files.keys())
	return [{'label': i, 'value': i} for i in tmp]

@app.callback(
	[Output(component_id='target_file', component_property='href'),
	Output(component_id='target_file', component_property='children'),
	],
	[Input(component_id='select_site', component_property='value'),
	Input(component_id='select_file', component_property='value'),
	])
def select_csv(selected_city, target_csv):
	if selected_city is None or target_csv is None:
		return '#', 'File Unavailable'
	output = json_[selected_city]['monitors'][0]['files'][target_csv]
	return output, output[-10:]

@app.callback(
	[Output('date-picker', 'start_date'),
	Output('date-picker', 'end_date'),
	Output('quality-tags', 'options')],
	[Input('target_file', 'href')]
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

# @app.callback(
#     Output('specs-pandas', 'children'),
#     [Input('target_file', 'href'),
#     Input('date-picker', 'start_date'),
#     Input('date-picker', 'end_date')])
# def display_info(target_file, start_date, end_date):
# 	if any([target_file, start_date, end_date]) is None:
# 		return 'Waiting for the input'
# 	info = f'start: {start_date}, end: {end_date} with file {target_file}'
# 	print(info)
# 	return info
		# dcc.Graph(id='hist-graph'),
		# 	dcc.Graph(id='pie-graph'),

@app.callback(
    [Output('pandas-graphic', 'figure'),
    Output('pandas-graphic-daily', 'figure'),
	Output('hist-graph', 'figure'),
	Output('pie-graph', 'figure'),
	],
    [Input('submit-button-state', 'n_clicks')],
    [State('target_file', 'href'),
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
	df = df[df['QC Name'].isin(value)][['Raw Conc.', 'AQI Category']]
	df = df[(df.index >= start) & (df.index <= end)]
	df2 = df.resample('1D').mean()
	fig = px.line(df, y='Raw Conc.', title='Raw PM2.5 Conc.')
	fig_daily = px.line(df2, y='Raw Conc.', title='Daily PM2.5 Conc.')
	dist = px.histogram(df, x='Raw Conc.')
	dfp = df.groupby('AQI Category').count()
	colormap = {'Good': 'green',
				'Moderate': 'yellow',
				'Unhealthy for Sensitive Groups': 'orange',
				'Unhealthy': 'red',
				'Very Unhealthy': 'purple',
				'Hazardous': 'maroon'}
	pie = px.pie(
		dfp, values= 'Raw Conc.', 
		names=dfp.index,
		color_discrete_map=colormap)
	print(dfp)
	return fig, fig_daily, dist, pie

if __name__ == '__main__':
	app.run_server(debug=True)


