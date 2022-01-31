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
moving_averages = ta.Strategy(
    name="moving indicators",
    ta=[
        {"kind": "sma", "length": 10},
        {"kind": "ema", "length": 5},
    ]
)

# Disable multiprocessing, calculate averages
df.ta.cores = 0  # optional, but requires if __name__ == "__main__" syntax if not set to 0
df.ta.strategy(moving_averages)

# Create the Plot
fig1 = go.Figure(data=[
    go.Candlestick(
        x=df.index,
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        increasing_line_color='#248f24',
        decreasing_line_color='black',
        showlegend=False,
    ),
])

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
fig1.update_layout(layout)

# # Display (in browser by default)
# fig.show()

# Add the SMA 10
fig1.add_trace(
    go.Scatter(
        x=df.index,
        y=df['SMA_10'],
        line=dict(color='#ff9900', width=2),
        name='SMA_10'
    )
)
# Add the EMA 5
fig1.add_trace(
    go.Scatter(
        x=df.index,
        y=df['EMA_5'],
        line=dict(color='#006699', width=2),
        name='EMA_5'
    )
)

fig1.show()