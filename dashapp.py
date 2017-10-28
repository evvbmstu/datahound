import dash
import dash_core_components as dcc
import dash_html_components as html

import community as cm
import views as vws


class CommunityAnalysisApp:
    def __init__(self, name="pentestit", debug=True, start=False):
        self.debug = debug
        self.community_name = name
        if start:
            self.start()

    def start(self):
        if self.debug:
                print("Just start app.")
        app = dash.Dash()
        pb = cm.Community(self.community_name)
        if self.debug:
            print("We got info of community")

        pb.display()

        if self.debug:
            print("Okey, we got some data. Start to visualize...")
        sex_pie = vws.pie_chart(pb.sex_dist(), ['#F08080', '#6495ED',  '#B22222'], 'Sex')

        funnel = vws.funnel(["Views", "Likes", 'Reposts'], pb.likes_funnel(debug=True))

        plat_data, sys_data = pb.platform_dist()

        platform_pie = vws.pie_chart(plat_data, ['#66CDAA', '#EE5C42', '#1874CD', '#B22222'], 'Platform')
        system_pie = vws.pie_chart(sys_data, ['#8B8386', '#FFE4C4'], 'System')

        ages_female, xbins_female, ages_male, xbins_male, ukn = pb.age_dict()

        gist_female = vws.histogram(ages_female, xbins_female, '#FFD7E9', 'Female')
        gist_male = vws.histogram(ages_male, xbins_male, '#6495ED', 'Male')

        max_age = max(xbins_female['end'], xbins_male['end'])
        step = xbins_female['size']
        labels = ['{0}'.format(a) for a in range(0, max_age + step, step)]
        values = [a for a in range(0, max_age + step, step)]

        lay = vws.layout('Sex/Age', labels, values, 'Age ({0} Uknown)'.format(ukn), 'Percent')

        fig_sex_age = vws.store_2_fig(gist_female, gist_male, lay)

        app.layout = html.Div(children=[
            html.H1(children='Analisys of {0}'.format(self.community_name)),

            dcc.Graph(id='Sex', figure={'data': sex_pie}),

            dcc.Graph(id='Likes funnel', figure={'data': funnel[0], 'layout': funnel[1]}),

            dcc.Graph(id='Plaform', figure={'data': platform_pie}),

            dcc.Graph(id='System', figure={'data': system_pie}),

            dcc.Graph(id='Ages', figure={'data': fig_sex_age})

        ])

        if self.debug:
            print("We draw this awesome graph, bro. Check it.")

        app.run_server(debug=True)


if __name__ == '__main__':
    nya = CommunityAnalysisApp(start=True)

