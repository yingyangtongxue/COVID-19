import os
from click import style
import pandas as pd
import json

import dash
import dash_bootstrap_components as dbc
import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, ClientsideFunction
import plotly.graph_objects as go

clean_folder = os.getcwd()
clean_folder += os.sep + "datasets"+ os.sep + "clean"

df_states = pd.read_csv(os.path.join(clean_folder,"states_result.csv"))
df_brazil = pd.read_csv(os.path.join(clean_folder,"brazil_result.csv"))

json_brazil = json.load(open("geojson"+ os.sep +"brazil_geo.json","r"))

df_data = df_states[df_states["estado"]=="SP"]

# =====================================================================
#Initialize Dash
df_states_ = df_states[df_states["data"]=="2020-05-13"]

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

fig = px.choropleth_mapbox(df_states_, locations="estado", color="casosNovos",
                            center={"lat": -16.95, "lon": -47.78}, zoom=4,
                            geojson=json_brazil, color_continuous_scale="Redor", opacity=0.4, 
                            hover_data={"casosAcumulado": True, "casosNovos": True,"obitosNovos": True,"estado": True})

fig.update_layout(
    paper_bgcolor="#242424",
    autosize=True,
    margin=go.Margin(l=0,r=0,t=0,b=0),
    showlegend=False,
    mapbox_style="carto-darkmatter"
) #Map

fig2 = go.Figure(layout={"template": "plotly_dark"})
fig2.add_trace(go.Scatter(x=df_data["data"],y=df_data["casosAcumulado"]))
fig2.update_layout(
    paper_bgcolor="#242424",
    plot_bgcolor="#242424",
    autosize=True,
    margin=dict(l=10,r=10,t=10,b=10)
) #line graph
# =====================================================================
#Layout

app.layout = dbc.Container(
    dbc.Row([
        dbc.Col([

            html.Div([
                html.H1("COVID-19"),
                html.H5("Pandemic Evolution"), 
                dbc.Button("Brazil", color="light", id="location-button", size="lg")
            ], style={}),

            html.P("Enter date", style={"margin-top": "40px"}),

            html.Div(id="div-test", children = [
                dcc.DatePickerSingle(
                    id="date-picker",
                    min_date_allowed=df_brazil["data"].min(),
                    max_date_allowed=df_brazil["data"].max(),
                    initial_visible_month=df_brazil["data"].min(),
                    date = df_brazil["data"].max(),
                    display_format = "MMMM DD, YYYY",
                    style={"border": "0px solid black"}
                )
            ]),

        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Span("Recovered cases"), 
                        html.H3(style={"color": "#adfc92"}, id="recovered-cases-text"),
                        html.Span("Active cases"), 
                        html.H5(id="active-cases-text")
                    ])
                ])
            ]),
        ]),    

            dcc.Graph(id="line-graph", figure=fig2)
        ]),

        dbc.Col([
            dcc.Graph(id="choropleth-map", figure=fig)
        ])     

    ])
)

if __name__== "__main__": 
    app.run_server(debug=True)
