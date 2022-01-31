import yfinance as yf

stock_symbol="TATASTEEL.NS"
yf_stk=yf.Ticker(stock_symbol)

df=yf.download(stock_symbol, start="2021-01-02")



import pandas_ta as ta
import yfinance as yf
import plotly.graph_objects as go


# Get the data
stock_symbol="TATASTEEL.NS"
df = yf.Ticker(stock_symbol).history(period='12mo')[['Open', 'Close', 'High', 'Low', 'Volume']]
# df=yf.download(stock_symbol, start="2021-01-02")

# Add the indicators

df['TP'] = (df['Close'] + df['Low'] + df['High'])/3
df['std'] = df['TP'].rolling(20).std(ddof=0)
df['MA-TP'] = df['TP'].rolling(20).mean()
df['BOLU'] = df['MA-TP'] + 2*df['std']
df['BOLD'] = df['MA-TP'] - 2*df['std']
print(df)


WINDOW = 30
df['sma'] = df['Close'].rolling(WINDOW).mean()
df['std'] = df['Close'].rolling(WINDOW).std(ddof = 0)

fig = go.Figure(data=[
    go.Candlestick(x = df.index,
                             open = df['Open'],
                             high = df['High'],
                             low = df['Low'],
                             close = df['Close'], showlegend=False,
                             name = 'candlestick'),
])

# Moving Average
fig.add_trace(go.Scatter(x = df.index,
                         y = df['sma'],
                         line_color = 'black',
                         name = 'sma')
)
                        
# Upper Bound
fig.add_trace(go.Scatter(x = df.index,
                         y = df['sma'] + (df['std'] * 2),
                         line_color = 'gray',
                         line = {'dash': 'dash'},
                         name = 'upper band',
                         opacity = 0.5)
)

# Lower Bound fill in between with parameter 'fill': 'tonexty'
fig.add_trace(go.Scatter(x = df.index,
                         y = df['sma'] - (df['std'] * 2),
                         line_color = 'gray',
                         line = {'dash': 'dash'},
                         fill = 'tonexty',
                         name = 'lower band',
                         opacity = 0.5)
)

# Make it pretty
layout = go.Layout(
    plot_bgcolor='#efefef',
    # Font Families
    font_family='Monospace',
    font_color='#000000',
    font_size=20,
    xaxis=dict(
        rangeslider=dict(
            visible=False
        ))
)
fig.update_layout(layout)

fig.show()

