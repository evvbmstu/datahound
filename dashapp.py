import dash
import dash_core_components as dcc
import dash_html_components as html

import community as cm
import views


def create_dash_app(comm_name="rhymes", debug=True):
    if debug:
            print("Just start app.")
    app = dash.Dash()
    pb = cm.Community(comm_name)
    if debug:
        print("We got info of community")

    pb.display()

    if debug:
        print("Okey, we got some data. Start to visualize...")
    sex_dist = views.create_sex_dist(pb)
    funnel = views.create_likes_funnel(pb)
    platform_dist, system_dist = views.create_platform_dist(pb)
    fig_sex_age = views.create_ages_gist(pb)

    app.layout = html.Div(children=[
        html.H1(children='Hello Dash'),

        html.Div(children='''
            Dash: A web application framework for Python.
        '''),

        dcc.Graph(id='Sex', figure={'data': sex_dist}),

        dcc.Graph(id='Likes funnel', figure={'data': funnel[0], 'layout': funnel[1]}),

        dcc.Graph(id='Plaform', figure={'data': platform_dist}),

        dcc.Graph(id='System', figure={'data': system_dist}),

        dcc.Graph(id='Ages', figure={'data': fig_sex_age})

    ])

    if debug:
        print("We draw this awesome graph, bro. Check it.")

    app.run_server(debug=True)


def create_sex_dist(community):
    sex = community.sex_dist(debug=True)
    return [go.Pie(labels=list(sex.keys()), values=list(sex.values()))]


def create_platform_dist(community):
    platform, system = community.platform_dist()
    pie_platform = [go.Pie(labels=list(platform.keys()), values=list(platform.values()),
                           hoverinfo='label+percent', textinfo='value',
                           marker=dict(colors=['#66CDAA', '#EE5C42', '#1874CD']), opacity=0.9)]
    pie_system = [go.Pie(labels=list(system.keys()), values=list(system.values()),
                         hoverinfo='label+percent', textinfo='value',
                         marker=dict(colors=['#8B8386', '#FFE4C4']), opacity=0.9)]

    return pie_platform, pie_system


def create_ages_gist(community):
    ages_female, xbins_female, ages_male, xbins_male, ukn = community.age_dict()
    gist_female = go.Histogram(x=ages_female, histnorm='percent', xbins=xbins_female,
                               marker=dict(color='#FFD7E9', ), name='Female',
                               opacity=0.75)
    gist_male = go.Histogram(x=ages_male, histnorm='percent', xbins=xbins_male,
                             marker=dict(color='#6495ED', ), name='Male',
                             opacity=0.75)

    max_age = max(xbins_female['end'], xbins_male['end'])
    step = xbins_female['size']
    layout = go.Layout(title="Sex/Age",
                       xaxis=dict(rangemode='tozero', showticklabels=True,
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

if __name__ == '__main__':
    create_dash_app()
