# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile
import numpy as np
from pylab import rcParams
import wave
from iplot import iplot_data
import dash_table_experiments as dt

import plotly.plotly as py
import plotly.graph_objs as gobj
import plotly

import pandas as pd

df = pd.read_csv(
    'https://gist.githubusercontent.com/chriddyp/'
    'c78bf172206ce24f77d6363a2d754b59/raw/'
    'c353e8ef842413cae56ae3920b8fd78468aa4cb2/'
    'usa-agricultural-exports-2011.csv')

data_dir = '../soundAnalysis/data/22-03-~1/22-03-16-agn-n/'
file_name = data_dir + '22-03-16-agn-12.wav'
file_segments = data_dir + '22-03-16-agn-12.6'


def parse_segments(file_name):
    with open(file_name, 'r') as fl:
        return [(int(data[1]), int(data[2]), data[0]) 
                for data in map(lambda s: s.strip().split(), fl)]

def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

# TEST
#---------------------

DF_WALMART = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/1962_2006_walmart_store_openings.csv')

DF_GAPMINDER = pd.read_csv(
    'https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv'
)
DF_GAPMINDER = DF_GAPMINDER[DF_GAPMINDER['year'] == 2007]
DF_GAPMINDER.loc[0:20]

DF_SIMPLE = pd.DataFrame({
    'x': ['A', 'B', 'C', 'D', 'E', 'F'],
    'y': [4, 3, 1, 2, 3, 6],
    'z': ['a', 'b', 'c', 'a', 'b', 'c']
})

ROWS = [
    {'a': 'AA', 'b': 1},
    {'a': 'AB', 'b': 2},
    {'a': 'BB', 'b': 3},
    {'a': 'BC', 'b': 4},
    {'a': 'CC', 'b': 5},
    {'a': 'CD', 'b': 6}
]



#---------------------
sample_rate, d_samples = wavfile.read(file_name)
segments = parse_segments(file_segments)

app = dash.Dash()

app.css.append_css({
    'external_url': (
        'https://cdn.rawgit.com/chriddyp/0247653a7c52feb4c48437e1c1837f75'
        '/raw/a68333b876edaf62df2efa7bac0e9b3613258851/dash.css'
    )
})
app.layout = html.Div(children=[

    dcc.Markdown('''
    ## Analysis of Drosophila sound production
    ##### Good vibrations — BioHack 2018, Saint-Petersburg

    Five years since the end of the Great Recession,
    the economy has finally regained the nine million jobs it lost.
    But not all industries recovered equally.
    Each line below shows how the number of jobs has changed for
    a particular industry over the past 10 years.
    Scroll down to see how the recession reshaped the nation’s job market,
    industry by industry.
    > This interactive report is a rendition of a
    > [New York Times original](https://www.nytimes.com/interactive/2014/06/05/upshot/how-the-recession-reshaped-the-economy-in-255-charts.html).
    > This app demonstrates how to build high-quality, interactive
    > reports using the Dash framework in Python.
    ***
    '''.replace('  ', ''), className='container',
    containerProps={'style': {
                    'left': '10px',
                    'display': 'inline',
                }}),

    dcc.Graph(
        id='HELLO THERE',
        figure={
            'data': iplot_data(d_samples, skip = 20)
            ,
            'layout': gobj.Layout(
                xaxis={'title': 'GDP Per Capita'},
                yaxis={'title': 'Life Expectancy'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }
    ),
    dcc.Markdown('''
    ##### Table example
    ***
    '''.replace('  ', ''), className='container',
    containerProps={'style': {
                    'left': '10px',
                    'display': 'inline',
                }}),



    #generate_table(df)
    dt.DataTable(
        rows=DF_GAPMINDER.to_dict('records'),

        # optional - sets the order of columns
        columns=sorted(DF_GAPMINDER.columns),

        row_selectable=True,
        filterable=True,
        sortable=True,
        selected_row_indices=[],
        id='datatable-gapminder'
    ),
    html.Div(id='selected-indexes'),
    dcc.Graph(
        id='graph-gapminder'
    )
])


#---------


@app.callback(
    Output('datatable-gapminder', 'selected_row_indices'),
    [Input('graph-gapminder', 'clickData')],
    [State('datatable-gapminder', 'selected_row_indices')])
def update_selected_row_indices(clickData, selected_row_indices):
    if clickData:
        for point in clickData['points']:
            if point['pointNumber'] in selected_row_indices:
                selected_row_indices.remove(point['pointNumber'])
            else:
                selected_row_indices.append(point['pointNumber'])
    return selected_row_indices


@app.callback(
    Output('graph-gapminder', 'figure'),
    [Input('datatable-gapminder', 'rows'),
     Input('datatable-gapminder', 'selected_row_indices')])
def update_figure(rows, selected_row_indices):
    dff = pd.DataFrame(rows)
    fig = plotly.tools.make_subplots(
        rows=3, cols=1,
        subplot_titles=('Life Expectancy', 'GDP Per Capita', 'Population',),
        shared_xaxes=True)
    marker = {'color': ['#0074D9']*len(dff)}
    for i in (selected_row_indices or []):
        marker['color'][i] = '#FF851B'
    fig.append_trace({
        'x': dff['country'],
        'y': dff['lifeExp'],
        'type': 'bar',
        'marker': marker
    }, 1, 1)
    fig.append_trace({
        'x': dff['country'],
        'y': dff['gdpPercap'],
        'type': 'bar',
        'marker': marker
    }, 2, 1)
    fig.append_trace({
        'x': dff['country'],
        'y': dff['pop'],
        'type': 'bar',
        'marker': marker
    }, 3, 1)
    fig['layout']['showlegend'] = False
    fig['layout']['height'] = 800
    fig['layout']['margin'] = {
        'l': 40,
        'r': 10,
        't': 60,
        'b': 200
    }
    fig['layout']['yaxis3']['type'] = 'log'
    return fig

#------------------


if __name__ == '__main__':
    app.run_server(debug=True)