# -*- coding: utf-8 -*-
import base64
import dash
import dash_core_components as dcc
import dash_html_components as html
import matplotlib.pyplot as plt
from frontend.iplot import iplot_data
import dash_table_experiments as dt
import plotly.graph_objs as gobj
import pandas as pd
import numpy as np


def start_server(song, debug=False):
    app = dash.Dash()

    if len(song['segments_pulse']) + len(song['segments_sin']) > 0:
        DF_SEGMENTS = pd.DataFrame(columns=['start', 'end', 'type'],
                                   data=[(segment[0], segment[1], 'P') for segment in song['segments_pulse']] +
                                        [(segment[0], segment[1], 'S') for segment in song['segments_sin']])
    else:
        DF_SEGMENTS = pd.DataFrame([1, 2])

    if len(song['info_sin']) > 0:
        DF_SEGMENTS_SIN = pd.DataFrame(song['info_sin'], columns=[
            'start', 'end', 'n_periods', 'sine_freq',
            'am_time_mean', 'am_amplitude_mean'])
    else:
        DF_SEGMENTS_SIN = pd.DataFrame([1, 2])
    if len(song['info_pulse']) > 0:
        DF_SEGMENTS_PULSE = pd.DataFrame(song['info_pulse'], columns=[
            'start', 'end', 'number_of_pulses', 'song_duration',
            'max_amps_mean', 'max_amps_std',
            'widths_mean', 'widths_std',
            'energies_mean', 'energies_std'])
    else:
        DF_SEGMENTS_PULSE = pd.DataFrame([1, 2])

    image_filename = 'specgram.png'
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.specgram(song['samples'], NFFT=512, Fs=song['rate'])
    fig.savefig(image_filename, dpi=100, bbox_inches='tight')
    with open(image_filename, 'rb') as fl:
        encoded_specgram_image = base64.b64encode(fl.read())

    image_filename = 'fft.png'
    fig, ax = plt.subplots(figsize=(8, 6))
    fourier = np.fft.fftshift(np.fft.fft(song['samples'], n=len(song['samples'])))
    fourier = fourier[int(len(fourier) * 0.45):int(len(fourier) * 0.55)]
    ax.plot([x.real for x in fourier])
    fig.savefig(image_filename, dpi=100, bbox_inches='tight')
    with open(image_filename, 'rb') as fl:
        encoded_fft_image = base64.b64encode(fl.read())

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
        ***
        '''.replace('  ', ''), className='container',
                     containerProps={'style': {
                         'left': '10px',
                         'display': 'inline',
                     }}),

        dcc.Graph(
            id='soundwawe',
            figure={
                'data': iplot_data(song['samples'], segments=song['segments_pulse'],
                                   segments_1=song['segments_sin'], skip=20)
                ,
                'layout': gobj.Layout(
                    xaxis={'title': 'Time'},
                    yaxis={'title': 'Signal level'},
                    margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                    legend={'x': 0, 'y': 1},
                    hovermode='closest'
                )
            }
        ),

        html.Img(
            src="data:image/png;base64,{}".format(encoded_specgram_image.decode()),
        ),

        html.Img(
            src="data:image/png;base64,{}".format(encoded_fft_image.decode()),
        ),
        dcc.Markdown('''
        ##### Segmentation results
        ***
        '''.replace('  ', ''), className='container',
                     containerProps={'style': {
                         'left': '10px',
                         'display': 'inline',
                     }}),

        # generate_table(df)
        dt.DataTable(
            rows=DF_SEGMENTS.to_dict('records'),
            row_selectable=True,
            filterable=True,
            sortable=True,
            selected_row_indices=[],
            id='datatable-segments',
            editable=False
        ),
        dcc.Markdown('''
        ##### Pulse wawes:
        ***
        '''.replace('  ', ''), className='container',
                     containerProps={'style': {
                         'left': '10px',
                         'display': 'inline',
                     }}),
        dt.DataTable(
            rows=DF_SEGMENTS_PULSE.to_dict('records_pulse'),
            row_selectable=True,
            filterable=True,
            sortable=True,
            selected_row_indices=[],
            id='datatable-segments_pulse',
            editable=False
        ),
        dcc.Markdown('''
        ##### Sine wawes:
        ***
        '''.replace('  ', ''), className='container',
                     containerProps={'style': {
                         'left': '10px',
                         'display': 'inline',
                     }}),
        dt.DataTable(
            rows=DF_SEGMENTS_SIN.to_dict('records_sine'),
            row_selectable=True,
            filterable=True,
            sortable=True,
            selected_row_indices=[],
            id='datatable-segments_sine',
            editable=False
        ),

    ])

    app.run_server(debug=debug)  # for internet server host='0.0.0.0'
