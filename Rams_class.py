import pandas_ta as ta
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots



class BaseClass:
    def __init__(self,symbol,period='12mo') :
        self.symbol=symbol
        self.period=period
        self.df=self.get_history()
        # print(dir(ta))

    def get_history(self):
        stock_symbol=self.symbol
        stock_period=self.period
        df = yf.Ticker(stock_symbol).history(period=stock_period)[['Open', 'Close', 'High', 'Low', 'Volume']]
        return(df)

# Strategies

    def get_sma(self,sma_window):
        moving_averages = ta.Strategy(
            name="moving indicators",
            ta=[
                {"kind": "sma", "length": sma_window},
            ]
        )
        self.df.ta.strategy(moving_averages)

        # self.df.ta.sma(close=self.df['Close'], length=sma_window, append=True, signal_indicators=True)

        return (self.df)

    def get_ema(self,ema_window):
        moving_averages = ta.Strategy(
            name="moving indicators",
            ta=[
                {"kind": "ema", "length": ema_window},
            ]
        )
        self.df.ta.strategy(moving_averages)
        return (self.df)

    def get_rsi(self,rsi_length):
        df=self.df
        df.ta.rsi(close=df['Close'], length=rsi_length, append=True, signal_indicators=True)
        return(df)

    def get_all(self):
        df=self.df
        # Create your own Custom Strategy
        CustomStrategy = ta.Strategy(
            name="Momo and Volatility",
            description="SMA 50,200, BBANDS, RSI, MACD and Volume SMA 20",
            ta=[
                {"kind": "sma", "length": 50},
                {"kind": "sma", "length": 200},
                {"kind": "bbands", "length": 20},
                {"kind": "rsi"},
                {"kind": "macd", "fast": 8, "slow": 21},
                {"kind": "sma", "close": "volume", "length": 20, "prefix": "VOLUME"},
            ]
        )
        df.ta.strategy(CustomStrategy)
        return (df)



    def plot_basic(self,bool_val=True):
        df=self.df
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

        if(bool_val):
            fig1.show()
        return(fig1)

    def plot_sma(self,fig1,col_name,bool_val=True):
        df=self.df
        fig1.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df[col_name],
                    line=dict(color='#ff9900', width=2),
                    name=col_name
                        )
            )
        if(bool_val):
            fig1.show()
        return(fig1)

    def plot_ema(self,fig1,col_name,bool_val=True):
        df=self.df
        fig1.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df[col_name],
                    line=dict(color='#006699', width=2),
                    name=col_name
                )
            )
        if(bool_val):
            fig1.show()
        return(fig1)
        
    
    def plot_rsi(self,col_name,bool_val=True):
        # Create Figure
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, row_width=[0.25, 0.75])

        df=self.df
        # Create Candlestick chart for price data
        fig.add_trace(go.Candlestick(
            x=df.index,
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            increasing_line_color='#ff9900',
            decreasing_line_color='black',
            showlegend=True
        ), row=1, col=1)



        # Make RSI Plot
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df[col_name],
            line=dict(color='#ff9900', width=2),
            name=col_name,
            showlegend=True,
        ), row=2, col=1
        )


        # Add upper/lower bounds
        fig.update_yaxes(range=[-10, 110], row=2, col=1)
        fig.add_hline(y=0, col=1, row=2, line_color="#666", line_width=2)
        fig.add_hline(y=100, col=1, row=2, line_color="#666", line_width=2)


        # Add overbought/oversold
        fig.add_hline(y=30, col=1, row=2, line_color='#336699', line_width=2, line_dash='dash')
        fig.add_hline(y=70, col=1, row=2, line_color='#336699', line_width=2, line_dash='dash')


        # Customize font, colors, hide range slider
        layout = go.Layout(
            plot_bgcolor='#efefef',
            # Font Families
            font_family='Monospace',
            font_color='#000000',
            font_size=20,
            xaxis=dict(
                rangeslider=dict(
                    visible=False
                )
            )
        )
        # update and display
        fig.update_layout(layout)
        if(bool_val):
            fig.show()
        return(fig)
    
    def plot_bollinger(self,WINDOW):
        df=self.df
        df['sma_boll'] = df['Close'].rolling(WINDOW).mean()
        df['std_boll'] = df['Close'].rolling(WINDOW).std(ddof = 0)
        # Create subplots with 2 rows; top for candlestick price, and bottom for bar volume
        fig = make_subplots(rows = 2, cols = 1, shared_xaxes = True, subplot_titles = ('Company', 'Volume'), vertical_spacing = 0.1, row_width = [0.2, 0.7])

        # ----------------
        # Candlestick Plot
        fig.add_trace(go.Candlestick(x = df.index,
                                    open = df['Open'],
                                    high = df['High'],
                                    low = df['Low'],
                                    close = df['Close'], showlegend=False,
                                    name = 'candlestick'),
                    row = 1, col = 1)

        # Moving Average
        fig.add_trace(go.Scatter(x = df.index,
                                y = df['sma_boll'],
                                line_color = 'black',
                                name = 'sma'),
                    row = 1, col = 1)

        # Upper Bound
        fig.add_trace(go.Scatter(x = df.index,
                                y = df['sma_boll'] + (df['std_boll'] * 2),
                                line_color = 'gray',
                                line = {'dash': 'dash'},
                                name = 'upper band',
                                opacity = 0.5),
                    row = 1, col = 1)

        # Lower Bound fill in between with parameter 'fill': 'tonexty'
        fig.add_trace(go.Scatter(x = df.index,
                                y = df['sma_boll'] - (df['std_boll'] * 2),
                                line_color = 'gray',
                                line = {'dash': 'dash'},
                                fill = 'tonexty',
                                name = 'lower band',
                                opacity = 0.5),
                    row = 1, col = 1)


        # ----------------
        # Volume Plot
        fig.add_trace(go.Bar(x = df.index, y = df['Volume'], showlegend=False), 
                    row = 2, col = 1)

        # Remove range slider; (short time frame)
        fig.update(layout_xaxis_rangeslider_visible=False)

        # Stock data has gaps in dates, specifically in weekends and holidays
        # create a list of dates that are NOT included from start to end
        # date_gaps = [date for date in pd.date_range(start = '2020-12-21', end = '2021-05-14') if date not in df.index.values]

        # # Update Xaxes 
        # fig.update_xaxes(rangebreaks = [dict(values = date_gaps)])

        fig.show()
