import dash
import dash_core_components as dcc
import dash_html_components as html


def create_dash_app(flask_app):
    dash_app = dash.Dash(__name__, server=flask_app, url_base_pathname="/dash/")

    dash_app.layout = html.Div([html.H1("Hello World")])  # Your Dash components go here

    return dash_app
