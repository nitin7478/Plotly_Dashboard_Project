import pandas as pd
import yfinance as yd
import numpy as np
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import datetime as dt
import yfinance as yf
from datetime import timedelta
from datetime import date
from logger import logging
import plotly.graph_objects as go
from sklearn.preprocessing import StandardScaler, MinMaxScaler


external_stylesheets = [
    {
        "href": (
            "https://fonts.googleapis.com/css2?"
            "family=Lato:wght@400;700&display=swap"
        ),
        "rel": "stylesheet",
    },
]
app = Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Stock Prices"

# fig = px.line(x=data['Date'], y=data['Close'], title= 'Stock Price Chart', labels= dict(x='Date', y='Close'))
# fig1 = px.bar(x=data['Date'], y=data['Volume'], title= 'Stock Volume Chart', labels= dict(x='Date', y='Volume'))
stocks_list = ['ITC.NS', 'SBIN.NS', 'HDFC.NS']

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children="📈", className="header-emoji"),
                html.H1(
                    children="Stock Prices", className="header-title"
                ),
                html.P(
                    children=(
                        "Analyze the behavior of stocks"
                        " by its prices and volumes"
                        " in 2023"
                    ),
                    className="header-description",
                ),
            ],
            className="header",

        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Stock", className="menu-title"),
                        dcc.Dropdown(
                            id="stock_filter",
                            options=[
                                {"label": (stock.split('.')[0] if stock is not None else stock),
                                 "value": stock} for stock in stocks_list

                            ],
                            placeholder="Select stock",
                            clearable=False,
                            className="dropdown",
                            searchable=False,
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(
                            children="Date Range", className="menu-title"
                        ),
                        dcc.DatePickerRange(
                            id="date-range",
                            min_date_allowed=date(1990, 1, 1),
                            max_date_allowed=date.today() - timedelta(days=1),
                            initial_visible_month=date.today() - timedelta(days=1),
                            end_date_placeholder_text="End Date",
                            number_of_months_shown=3
                        ),
                    ]
                ),
            ],
            className="menu",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="price-chart",
                        config={"displayModeBar": False},

                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
        html.Div(
            children=html.Div([
                dcc.Graph(id="graph"),
            ],
                className = "card",                 
        ),

            className="wrapper",
        ),
        html.Div(
            children=html.Div([
                dcc.Graph(id="graph1"),
            ],
                className = "card",                 
        ),

            className="wrapper",
        ),

    ],
)


@app.callback(
    Output("price-chart", "figure"),
    Output("graph", "figure"),
    Output("graph1","figure"),
    Input("stock_filter", "value"),
    Input("date-range", "start_date"),
    Input("date-range", "end_date"),
)
def update_charts(value, start_date, end_date):
    start_date_object = ""
    end_date_object = ""
    if start_date is not None:
        start_date_object = date.fromisoformat(start_date)
    if end_date is not None:
        end_date_object = date.fromisoformat(end_date)
        
    data, scaled_data = download_data(value, start_date_object, end_date_object)
    object1 = yf.Ticker(value)
    
    
    
    price_chart_figure = {
        "data": [
            {
                "x": data.index.get_level_values('Date'),
                "y": data["Close"],
                "type": "lines",
                "hovertemplate": "$%{y:.2f}<extra></extra> %{x}",
            },
        ],
        "layout": {
            "title": {
                "text": f"Line chart of {value.split('.')[0] if value is not None else value }",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"tickprefix": "$", "fixedrange": True},
            "colorway": ["#17B897"],
        },
    }
    fig = go.Figure(data=[go.Candlestick(x=data.index.get_level_values('Date'),
                                         open=data['Open'],
                                         high=data['High'],
                                         low=data['Low'],
                                         close=data['Close'])])

    fig.update_layout(
        title = f"Candlestick Chart of {value.split('.')[0] if value is not None else value }",   
    )
    fig.update_xaxes(patch = dict(object1.splits))
    
    fig1 = px.line(x=data['Date'], y=scaled_data['Close','Volume'], title= 'Price-Volume Relation', labels= dict(x='Date', y=['Close','Volume']))
    return price_chart_figure, fig , fig1


def download_data(value, start, end):
    start = start
    end = end
    data = yf.download(str(value), start=start, end=end)
    scaler = MinMaxScaler(feature_range=(0,100))
    x = data[['Close','Volume']].reset_index(drop =True)
    scaled_data = scaler.fit_transform(x)
    df1 = pd.DataFrame(scaled_data)
    df1.index = data.index
    return data, df1


if __name__ == "__main__":
    app.run_server(debug=True)
