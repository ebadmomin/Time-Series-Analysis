import streamlit as st
import pandas as pd
import yfinance as yf
import pandas_datareader.data as web
import datetime
import numpy as np
import CAPM_functions

st.set_page_config(
    page_title='CAPM Return',
    page_icon='chart_with_upwards_trend',
    layout='wide',
)

st.title('Capital Asset Pricing Model (CAPM)')

# User inputs
col1, col2 = st.columns([1, 1])
with col1:
    stock_list = st.multiselect("Choose 4 Stocks",
                                ["TSLA", "AAPL", "NFLX", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA", "META"],
                                default=["AAPL", "MSFT"])
with col2:
    year = st.number_input("Number of years", 1, 10)

# Dates
end = datetime.datetime.today()
start = datetime.datetime(end.year - int(year), end.month, end.day)

# Load S&P 500 data
try:
    SP500 = web.DataReader('SP500', 'fred', start, end)
    st.success("S&P 500 data loaded successfully!")
except Exception as e:
    st.error(f"Error loading S&P 500 data: {e}")

# Load stock data
stocks_df = pd.DataFrame()
for stock in stock_list:
    data = yf.download(stock, start=start, end=end)
    stocks_df[stock] = data['Close']

stocks_df.reset_index(inplace=True)
SP500.reset_index(inplace=True)
SP500.columns = ['Date', 'SP500']

# Format and merge dates
stocks_df['Date'] = pd.to_datetime(stocks_df['Date'])
stocks_df['Date'] = stocks_df['Date'].apply(lambda x: str(x)[:10])
stocks_df['Date'] = pd.to_datetime(stocks_df['Date'])
stocks_df = pd.merge(stocks_df, SP500, on='Date', how='inner')

# Display head and tail
col1, col2 = st.columns([1, 1])
with col1:
    st.subheader("Dataframe Head")
    st.dataframe(stocks_df.head(), use_container_width=True)
with col2:
    st.subheader("Dataframe Tail")
    st.dataframe(stocks_df.tail(), use_container_width=True)

col1, col2 = st.columns([1, 1])
with col1:
    st.markdown("Price of all the Stocks")
    st.plotly_chart(CAPM_functions.interactive_plot(stocks_df), use_container_width=True)
with col2:
    CAPM_functions.normalize(stocks_df)
    st.markdown("Price of all the Stocks (After Normalization)")
    st.plotly_chart(CAPM_functions.interactive_plot(CAPM_functions.normalize(stocks_df)))

stocks_daily_returns = CAPM_functions.daily_returns(stocks_df)

beta = {}
alpha = {}

for i in stocks_daily_returns.columns:
    if i != 'Date' and i != 'SP500':
        b, a = CAPM_functions.calculate_beta(stocks_daily_returns, i)
        beta[i] = b
        alpha[i] = a
print(beta, alpha)

beta_df = pd.DataFrame(columns = ['Stock', 'Beta Values'])
beta_df['Stock'] = beta.keys()
beta_df['Beta Values'] = [str(round(i,2)) for i in beta.values()]

with col1:
    st.markdown("Calculated Beta Values")
    st.dataframe(beta_df, use_container_width=True)

rf = 0
rm = stocks_daily_returns['SP500'].mean() * 252

return_df = pd.DataFrame()
return_value = []
for stock, value in beta.items():
    return_value.append(str(round(rf+(value*(rf-rm)),2)))
return_df['Stock'] = stock_list
return_df['Return Value'] = return_value

with col2:
    st.markdown("Calculated Return Using CAPM")
    st.dataframe(return_df, use_container_width=True)