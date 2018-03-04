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
from iplot import iplot_data, iplot
import dash_table_experiments as dt

import plotly.plotly as py
import plotly.graph_objs as gobj
import plotly

import pandas as pd


def start_server(song)
    app = dash.Dash()

    DF_SEGMENTS = pd.DataFrame([(segment[0], segment[1], 'P') for segment in song['segments_pulse']] + [(segment[0], segment[1], 'P') for segment in song['segments_sin']])

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
            id='soundwawe',
            figure={
                'data': iplot_data(song['samples'], segments = song['segments_pulse'], segments_1 = song['segments_sin'], skip = 20)
                ,
                'layout': gobj.Layout(
                    xaxis={'title': 'Time'},
                    yaxis={'title': 'Signal level'},
                    margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                    legend={'x': 0, 'y': 1},
                    hovermode='closest'
                )
            }
        )

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
            rows=DF_SEGMENTS.to_dict('records'),

            # optional - sets the order of columns
            #columns=sorted(DF_SEGMENTS.columns),

            row_selectable=True,
            filterable=True,
            sortable=True,
            selected_row_indices=[],
            id='datatable-segments',
            editable=False
        ),
        html.Div(id='selected-indexes'),
        dcc.Graph(
            id='graph-segments'
        )
    ])


    app.run_server(debug=True)