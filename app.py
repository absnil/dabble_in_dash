import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output

app = dash.Dash()
server = app.server

df = pd.read_csv("stock_data1.csv")

app.layout = html.Div([
    html.H1("Stock Price Analysis", style={"textAlign": "center"}),
            html.Div([
                html.H1("Stocks Open vs Close", 
                        style={'textAlign': 'center'}),
                dcc.Dropdown(id='my-dropdown',
                             options=[{'label': 'Tesla', 'value': 'TSLA'},
                                      {'label': 'Apple','value': 'AAPL'}, 
                                      {'label': 'Facebook', 'value': 'FB'}, 
                                      {'label': 'Amazon','value': 'AMZN'}], 
                             multi=True,value=['AMZN'],
                             style={"display": "block", "margin-left": "auto", 
                                    "margin-right": "auto", "width": "60%"}),
                dcc.Graph(id='highlow')
            ], className="container"),        
])

@app.callback(Output('highlow', 'figure'),
              [Input('my-dropdown', 'value')])
def update_graph(selected_dropdown):
    dropdown = {"TSLA": "Tesla","AAPL": "Apple","FB": "Facebook","AMZN": "Amazon",}
    trace1 = []
    trace2 = []
    for stock in selected_dropdown:
        trace1.append(
          go.Scatter(x=df[df["Symbol"] == stock]["date"],
                     y=df[df["Symbol"] == stock]["Open"],
                     mode='lines', opacity=0.7, 
                     name=f'Open {dropdown[stock]}',textposition='bottom center'))
        trace2.append(
          go.Scatter(x=df[df["Symbol"] == stock]["date"],
                     y=df[df["Symbol"] == stock]["Close"],
                     mode='lines', opacity=0.6,
                     name=f'Close {dropdown[stock]}',textposition='bottom center'))
    traces = [trace1, trace2]
    data = [val for sublist in traces for val in sublist]
    figure = {'data': data,
              'layout': go.Layout(colorway=["#5E0DAC", '#FF4F00', '#375CB1', 
                                            '#FF7400', '#FFF400', '#FF0056'],
            height=600,
            title=f"Open and Close Prices for {', '.join(str(dropdown[i]) for i in selected_dropdown)} Over Time",
            xaxis={"title":"Date",
                   'rangeselector': {'buttons': list([{'count': 1, 'label': '1M', 
                                                       'step': 'month', 
                                                       'stepmode': 'backward'},
                                                      {'count': 6, 'label': '6M', 
                                                       'step': 'month', 
                                                       'stepmode': 'backward'},
                                                      {'step': 'all'}])},
                   'rangeslider': {'visible': True}, 'type': 'date'},
             yaxis={"title":"Price (USD)"})}
    return figure


if __name__ == '__main__':
    app.run_server(debug=True)

#reference:
#https://towardsdatascience.com/interactive-dashboards-for-data-science-51aa038279e5