import plotly.graph_objs as go

import funnelview


def pie_chart(data, colors, name):
    return [go.Pie(labels=list(data.keys()), values=list(data.values()),
                   hoverinfo='label+percent', textinfo='value',
                   marker=dict(colors=colors), name=name, opacity=0.9)]


def histogram(data, xbins, colors, name):
    return go.Histogram(x=data, histnorm='percent', xbins=xbins,
                        marker=dict(color=colors, ), name=name,
                        opacity=0.75)


def layout(name, xtext, xvals, xname, yname):
    return go.Layout(title=name, xaxis=dict(rangemode='tozero', showticklabels=True,
                                            ticktext=xtext, tickvals=xvals, title=xname),
                     yaxis=dict(title=yname))


def store_2_fig(first, second, layout):
    return go.Figure(data=[first, second], layout=layout)


def funnel(phase, data):
    values = []

    for each in phase:
        values.append(data[each])
    return funnelview.funnel_fig(values, phase)
