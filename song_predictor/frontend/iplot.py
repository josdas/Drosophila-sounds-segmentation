from plotly import graph_objs
import plotly

plotly.offline.init_notebook_mode()

BASE_LINE = dict(
    color='rgb(22, 96, 167)',
    width=1,
)

SEGMENT_LINE = dict(
    color='rgb(200, 20, 02)',
    width=3,
)
SEGMENT_LINE_1 = dict(
    color='rgb(200, 200, 02)',
    width=3,
)


def get_colored(x, segments):
    segments = list(sorted(segments, key=lambda x: x[0]))
    colors = [False] * len(x)
    j = 0
    for ind, i in enumerate(x):
        while j < len(segments) and segments[j][1] < i:
            j += 1
        if j < len(segments) and segments[j][0] <= i <= segments[j][1]:
            colors[ind] = True
    return colors


def iplot_data(y, x=None, segments=None, segments_1=None, skip=1):
    if not x:
        x = list(range(len(y)))[::skip]
    if not segments:
        segments = []
    if not segments_1:
        segments_1 = []
    y = y[::skip]

    colors = get_colored(x, segments)
    colors_1 = get_colored(x, segments_1)

    traces = []
    left = 0

    # end symbol
    colors.append(None)
    colors_1.append(None)

    for i in range(len(x) + 1):
        if i > 0 and (colors[i] != colors[i - 1] or colors_1[i] != colors_1[i - 1]):
            color = BASE_LINE
            text = 'noise'
            if colors[i - 1] or colors_1[i - 1]:
                color = SEGMENT_LINE_1 if colors_1[i - 1] else SEGMENT_LINE
                text = 'sin' if colors_1[i - 1] else 'pulse'
            trace = graph_objs.Scatter(
                y=y[left:i],
                x=x[left:i],
                line=color,
                text=text
            )
            traces.append(trace)
            left = i - 1

    data = graph_objs.Data(traces)
    return data


def iplot(y, x=None, segments=None, segments_1=None, skip=1):
    return plotly.offline.iplot(iplot_data(y, x, segments, segments_1, skip))
