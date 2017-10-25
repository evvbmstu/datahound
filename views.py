import plotly.graph_objs as go

import funnelview


def create_sex_dist(community):
    sex = community.sex_dist(debug=True)
    return [go.Pie(labels=list(sex.keys()), values=list(sex.values()))]


def create_platform_dist(community):
    platform, system = community.platform_dist()
    pie_platform = [go.Pie(
                        labels=list(platform.keys()), values=list(platform.values()),
                        hoverinfo='label+percent', textinfo='value',
                        marker=dict(colors=['#66CDAA', '#EE5C42', '#1874CD']), opacity=0.9)]
    pie_system = [go.Pie(
                        labels=list(system.keys()), values=list(system.values()),
                        hoverinfo='label+percent', textinfo='value',
                        marker=dict(colors=['#8B8386', '#FFE4C4']), opacity=0.9)]
    return pie_platform, pie_system


def create_ages_gist(community):
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


def create_likes_funnel(community):
    funnel = community.likes_funnel(debug=True)

    phase = ["Views", "Likes", 'Reposts']
    values = []

    for each in phase:
        values.append(funnel[each])
    return funnelview.funnel_fig(values, phase)
