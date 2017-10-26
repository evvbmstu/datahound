import plotly.graph_objs as go

import funnelview


class CreatorViews:
    @staticmethod
    def pie_chart(data, colors, name):
        return [go.Pie(labels=list(data.keys()), values=list(data.values()),
                       hoverinfo='label+percent', textinfo='value',
                       marker=dict(colors=colors), name=name, opacity=0.9)]

    @staticmethod
    def histogram(data, xbins, colors, name):
        return go.Histogram(x=data, histnorm='percent', xbins=xbins,
                            marker=dict(color=colors, ), name=name,
                            opacity=0.75)

    @staticmethod
    def _store_2_fig(first, second):
        pass




def ages_gist(community):
    ages_female, xbins_female, ages_male, xbins_male, ukn = community.age_dict()
    gist_female = go.Histogram(
                            x=ages_female, histnorm='percent', xbins=xbins_female,
                            marker=dict(color='#FFD7E9', ), name='Female',
                            opacity=0.75)
    gist_male = go.Histogram(
                            x=ages_male, histnorm='percent', xbins=xbins_male,
                            marker=dict(color='#6495ED', ), name='Male',
                            opacity=0.75)

    max_age = max(xbins_female['end'], xbins_male['end'])
    step = xbins_female['size']
    layout = go.Layout(
                        title="Sex/Age",
                        xaxis=dict(
                                rangemode='tozero', showticklabels=True,
                                ticktext=['{0}'.format(a) for a in range(0, max_age + step, step)],
                                tickvals=[a for a in range(0, max_age + step, step)],
                                title='Age ({0} Uknown)'.format(ukn)),
                        yaxis=dict(title='Percent'))
    return go.Figure(data=[gist_female, gist_male], layout=layout)


def likes_funnel(community):
    funnel = community.likes_funnel(debug=True)

    phase = ["Views", "Likes", 'Reposts']
    values = []

    for each in phase:
        values.append(funnel[each])
    return funnelview.funnel_fig(values, phase)
