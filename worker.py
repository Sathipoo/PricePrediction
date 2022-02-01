
import Rams_class as base




tata=base.BaseClass("TATASTEEL.NS")


apple=base.BaseClass("AAPL")
amazon=base.BaseClass("AMZN")


>>> fig1=tata.plot_basic(False)
>>> 
>>> tata.plot_sma(fig1,"SMA_10")

# or with custom period

pointer=base.BaseClass(symbol,'6mo')

# to get the entire OHLS data of 12 months 
pointer.df

pointer.df

# pointer.plot_basic()

pointer.get_sma(10)
pointer.get_rsi(10)
