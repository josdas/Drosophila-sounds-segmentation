# -*- coding: utf-8 -*-
import base64
import dash
import dash_core_components as dcc
import dash_html_components as html
import matplotlib.pyplot as plt
from iplot import iplot_data
import dash_table_experiments as dt
import plotly.graph_objs as gobj
import pandas as pd


def start_server(song):
    app = dash.Dash()

    DF_SEGMENTS = pd.DataFrame(columns=['start', 'end', 'type'],
                               data=[(segment[0], segment[1], 'P') for segment in song['segments_pulse']] +
                                    [(segment[0], segment[1], 'S') for segment in song['segments_sin']])

    print(len(song['info_sin']))
    print(len(song['info_pulse']))

    DF_SEGMENTS_SIN = pd.DataFrame(song['info_sin'])[[
        'start', 'end', 'n_periods', 'song_duration', 'sine_freq',
        'am_time_mean', 'am_amplitude_mean'
    ]]

    DF_SEGMENTS_PULSE = pd.DataFrame(song['info_pulse'])[[
        'start', 'end', 'number_of_pulses', 'song_duration',
        'max_amps_mean', 'max_amps_std',
        'widths_mean', 'widths_std',
        'energies_mean', 'energies_std']]

    # Pxx, freqs, bins, im = plt.specgram(song['samples'], NFFT=512, Fs=song['rate'])
    # image_filename = 'spectre.png'
    # im.write_png(image_filename)

    # with open(image_filename, 'rb') as fl:
    #    encoded_image = base64.b64encode(fl.read())

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
                'data': iplot_data(song['samples'], segments=song['segments_pulse'], segments_1=song['segments_sin'],
                                   skip=20)
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
        ##### Pulse wawes detalised
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
        ##### Sine wawes detalised
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
        )

    ])

    app.run_server(debug=True)
