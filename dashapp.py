import dash
import dash_core_components as dcc
import dash_html_components as html

import community as cm
from views import CreatorViews as crtr
import views


def create_dash_app(comm_name="pentestit", debug=True):
    if debug:
            print("Just start app.")
    app = dash.Dash()
    pb = cm.Community(comm_name)
    if debug:
        print("We got info of community")

    pb.display()

    if debug:
        print("Okey, we got some data. Start to visualize...")
    sex_pie = crtr.pie_chart(pb.sex_dist(), ['#F08080', '#6495ED',  '#B22222'], 'Sex')

    funnel = views.likes_funnel(pb)

    plat_data = pb.platform_dist()

    platform_pie = crtr.pie_chart(plat_data[0], ['#66CDAA', '#EE5C42', '#1874CD'], 'Platform')
    system_pie = crtr.pie_chart(plat_data[1], ['#8B8386', '#FFE4C4'], 'System')

    fig_sex_age = views.ages_gist(pb)

    app.layout = html.Div(children=[
        html.H1(children='Hello Dash'),

        html.Div(children='''
            Dash: A web application framework for Python.
        '''),

        dcc.Graph(id='Sex', figure={'data': sex_pie}),

        dcc.Graph(id='Likes funnel', figure={'data': funnel[0], 'layout': funnel[1]}),

        dcc.Graph(id='Plaform', figure={'data': platform_pie}),

        dcc.Graph(id='System', figure={'data': system_pie}),

        dcc.Graph(id='Ages', figure={'data': fig_sex_age})

    ])

    if debug:
        print("We draw this awesome graph, bro. Check it.")

    app.run_server(debug=True)


if __name__ == '__main__':
    create_dash_app()
