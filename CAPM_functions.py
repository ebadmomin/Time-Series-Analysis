import plotly.graph_objects as go
import numpy as np

# Function to create an interactive plot using Plotly
def interactive_plot(df):
    fig = go.Figure()
    for col in df.columns[1:]:
        fig.add_trace(go.Scatter(x=df['Date'], y=df[col], mode='lines', name=col))

    fig.update_layout(
        width=800,
        height=500,
        margin=dict(l=20, r=20, t=50, b=20),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        title="Stock Prices Over Time",
        xaxis_title="Date",
        yaxis_title="Price"
    )
    return fig


# Function to normalize the prices of the stocks based on the initial price
def normalize(df_2):
    df = df_2.copy()
    for i in df.columns[1:]:
        df[i] = df[i] / df[i][0]
    return df

# Function to calculate daily returns
def daily_returns(df_2):
    df_daily_returns = df_2.copy()
    for i in df_daily_returns.columns[1:]:
        for j in range(1, len(df_daily_returns)):
            df_daily_returns[i][j] = ((df_daily_returns[i][j] - df_daily_returns[i][j-1]) / df_daily_returns[i][j-1]) * 100
        df_daily_returns[i][0] = 0  # Set the first day return as 0
    return df_daily_returns


# Function to calculate beta
def calculate_beta(stocks_daily_returns, stock):
    rm = stocks_daily_returns['SP500'].mean()*252

    b,a = np.polyfit(stocks_daily_returns['SP500'], stocks_daily_returns[stock], 1)
    return b, a

