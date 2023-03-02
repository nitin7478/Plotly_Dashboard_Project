import pandas as pd
import plotly.express as px
import dash
import dash_html_components as html
import dash_core_components as dcc


df =  pd.read_csv('airline_data.csv', encoding = "ISO-8859-1")

# Randomly sample 500 data points. Setting the random state to be 42 so that we get same result.
data = df.sample(n=500, random_state=42)
fig = px.pie(data, values='Flights', names='DistanceGroup', title='Distance group proportion by flights')

#create dash application 
app = dash.Dash(__name__)
# Get the layout of the application and adjust it.
# Create an outer division using html.Div and add title to the dashboard using html.H1 component
# Add description about the graph using HTML P (paragraph) component
# Finally, add graph component.

# Get the layout of the application and adjust it.
# Create an outer division using html.Div and add title to the dashboard using html.H1 component
# Add description about the graph using HTML P (paragraph) component
# Finally, add graph component.
app.layout = html.Div(children=[html.H1('Airline Dashboard', style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
                                html.P('Proportion of distance group (250 mile distance interval group) by flights.', style={'textAlign':'center', 'color': '#F57241'}),
                                dcc.Graph(figure=fig),

                    ])
if __name__ =='__main__':
    app.run_server()