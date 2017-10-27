import dash
import dash_core_components as dcc
import dash_html_components as html

import community as cm
import views


def create_dash_app(comm_name="bmstuinformer", debug=True):
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
    ad_ratio = views.create_ad_ratio(pb)

    app.layout = html.Div(children=[
        html.H1(children='Hello Dash'),

        html.Div(children='''
            Dash: A web application framework for Python.
        '''),

        dcc.Graph(id='Sex', figure={'data': sex_dist}),

        dcc.Graph(id='Likes funnel', figure={'data': funnel[0], 'layout': funnel[1]}),

        dcc.Graph(id='Plaform', figure={'data': platform_dist}),

        dcc.Graph(id='System', figure={'data': system_dist}),

        dcc.Graph(id='Ages', figure={'data': fig_sex_age}),

        dcc.Graph(id='Ad', figure={'data': ad_ratio})

    ])

    if debug:
        print("We draw this awesome graph, bro. Check it.")

    app.run_server(debug=False)


if __name__ == '__main__':
    create_dash_app()
