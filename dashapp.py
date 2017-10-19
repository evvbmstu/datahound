import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import community as cm
import funnelview
print("Just start app.")
app = dash.Dash()
pb = cm.Community("knndev")
data = pb.sex_dist(debug="True")
print("We got all members sex")
funnel = pb.likes_funnel(debug=True)
print(" Okay, we got data for plot lieks funnel")
phase = ["Views", "Likes", 'Reposts']
values = []
for each in phase:
    values.append(funnel[each])
dl = funnelview.funnel_fig(values, phase)
pb.display()
print("Okey, we got some data. Start to visualize...")

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [go.Pie(labels = list(data.keys()), values = list(data.values()))]
        }
    ),

    dcc.Graph(
        id='example_funnel',
        figure={
            'data': dl[0],
            'layout': dl[1]
        }
    )
])
print("We draw this awesome graph, bro. Check it.")

if __name__ == '__main__':
    app.run_server(debug=True)
