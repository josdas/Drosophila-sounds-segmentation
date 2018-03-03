# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile
import numpy as np
from pylab import rcParams
import warnings
import wave

import plotly.plotly as py
import plotly.graph_objs as gobj
import plotly

data_dir = '../soundAnalysis/data/22-03-~1/22-03-16-agn-n/'
file_name = data_dir + '22-03-16-agn-12.wav'
file_segments = data_dir + '22-03-16-agn-12.6'

BASE_LINE = dict(
    color = ('rgb(22, 96, 167)'),
    width = 2,
)

SEGMENT_LINE = dict(
    color = ('rgb(200, 20, 02)'),
    width = 3,
)

BACKGROUND = 'rgb(230, 230, 230)'

COLORSCALE = [ [0, "rgb(244,236,21)"], [0.3, "rgb(249,210,41)"], [0.4, "rgb(134,191,118)"],
                [0.5, "rgb(37,180,167)"], [0.65, "rgb(17,123,215)"], [1, "rgb(54,50,153)"] ]

def iplot(y, x=None, segments=None, skip=1):
    if not x:
        x = list(range(len(y)))[::skip]
    if not segments:
        segments = []
    y = y[::skip]
    
    colors = [any(seg[0] <= i <= seg[1] for seg in segments) for i in x]
    
    traces = []
    l = 0
    
    # end symbol
    colors.append(None) 
    
    for i in range(len(x)+1):
        if i > 0 and colors[i] != colors[i-1]:
            trace = gobj.Scatter(
                y=y[l:i],
                x=x[l:i],
                line=SEGMENT_LINE if colors[i-1] else BASE_LINE
            )
            traces.append(trace)
            l = i-1
        
            
    data = gobj.Data(traces)
    return plotly.offline.iplot(data)

def parse_segments(file_name):
    with open(file_name, 'r') as fl:
        return [(int(data[1]), int(data[2]), data[0]) 
                for data in map(lambda s: s.strip().split(), fl)]

sample_rate, d_samples = wavfile.read(file_name)
segments = parse_segments(file_segments)

y = d_samples
print(d_samples)
x = None
segments=segments
skip=100

if not x:
    x = list(range(len(y)))[::skip]
if not segments:
    segments = []
y = y[::skip]
    
colors = [any(seg[0] <= i <= seg[1] for seg in segments) for i in x]
    
traces = []
l = 0
    
# end symbol
colors.append(None) 
    
for i in range(len(x)+1):
    if i > 0 and colors[i] != colors[i-1]:
        trace = gobj.Scatter(
            y=y[l:i],
            x=x[l:i],
            line=SEGMENT_LINE if colors[i-1] else BASE_LINE
        )
        traces.append(trace)
        l = i-1

print(trace)
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
            'data': gobj.Data(traces)
            ,
            'layout': gobj.Layout(
                xaxis={'title': 'GDP Per Capita'},
                yaxis={'title': 'Life Expectancy'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }
    )
])


if __name__ == '__main__':
    app.run_server(debug=True)