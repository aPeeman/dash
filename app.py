import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import yfinance as yf
import plotly.graph_objs as go
import datetime

# 创建Dash应用
app = dash.Dash(__name__)

# 获取苹果股票数据
def get_stock_data(ticker):
    end = datetime.datetime.now()
    start = end - datetime.timedelta(days=365)
    df = yf.download(ticker, start=start, end=end)
    return df

# 应用布局
app.layout = html.Div(children=[
    html.H1(children='Apple Stock Price Dashboard'),

    dcc.DatePickerRange(
        id='date-picker-range',
        start_date=(datetime.datetime.now() - datetime.timedelta(days=365)).date(),
        end_date=datetime.datetime.now().date()
    ),

    dcc.Graph(
        id='stock-graph'
    )
])

# 回调函数更新图表
@app.callback(
    Output('stock-graph', 'figure'),
    [Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')]
)
def update_graph(start_date, end_date):
    df = yf.download('AAPL', start=start_date, end=end_date)

    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=df.index,
                                 open=df['Open'],
                                 high=df['High'],
                                 low=df['Low'],
                                 close=df['Close'],
                                 name='Apple Stock'))
    fig.update_layout(title='Apple Stock Price',
                      yaxis_title='Stock Price (USD)',
                      xaxis_title='Date')

    return fig

# 运行应用
if __name__ == '__main__':
    app.run_server(debug=True)
