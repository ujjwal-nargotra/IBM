# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site_dropdown',
                                options=[
                                {'label': 'All Sites', 'value': 'ALL'},
                                {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                {'label':'KSC LC-39A', 'value':'KSC LC-39A'},
                                {'label':'VAFB SLC-4E', 'value':'VAFB SLC-4E'}
                                ],
                                value='ALL',
                                placeholder="Select Launch Site",
                                searchable=True
                                ),
                                
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload_slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0',
                                                1000: '1000',
                                                2000: '2000',
                                                3000: '3000', 
                                                4000 : '4000',
                                                5000: '5000', 
                                                6000: '6000', 
                                                7000: '7000',
                                                8000 : '8000',
                                                9000 : '9000', 
                                                10000: '10000'},
                                                value=[min_payload, max_payload]), 
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success_payload_scatter_chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site_dropdown', component_property='value'))
def get_pie_chart(site_dropdown):
    filtered_df = spacex_df
    if site_dropdown == 'ALL':
        fig = px.pie(filtered_df, values='class', 
        names='Launch Site', 
        title='Total Success Launches by Sites')
        return fig
    else:
        new_df = filtered_df[filtered_df['Launch Site'] == site_dropdown]
        mean_succ = new_df['class'].mean()*100
        values = [mean_succ, 100-mean_succ]
        fig = go.Figure(data=go.Pie(labels = [0,1],
        values = values))     
        fig.update_layout(title_text = 'Total Success Launches for Site {}'.format(site_dropdown))   
        # return the outcomes piechart for a selected site
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success_payload_scatter_chart', component_property='figure'),
            [Input(component_id='site_dropdown', component_property='value'),
            Input(component_id="payload_slider", component_property="value")])

def get_scatter_chart(site_dropdown, payload_slider):
    dff = spacex_df
    if site_dropdown == 'ALL':
        fig = px.scatter(dff, x='Payload Mass (kg)', y='class', color='Booster Version Category')
        return fig
    else:
        new_df = dff[dff['Launch Site'] == site_dropdown]
        fig = px.scatter(new_df, x='Payload Mass (kg)', y='class', color = 'Booster Version Category')
        return fig


# Run the app
if __name__ == '__main__':
    app.run_server()