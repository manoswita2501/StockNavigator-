import streamlit as st
import pandas as pd
import yfinance as yf
import datetime
from datetime import date
from plotly import graph_objs as go
from prophet import Prophet
from prophet.plot import plot_plotly
import time
from streamlit_option_menu import option_menu

# Set up the Streamlit page configuration
st.set_page_config(layout="wide", initial_sidebar_state="expanded", page_title="StockNavigator", page_icon=":chart_with_upwards_trend:")

# Add custom meta tags and styling
def add_meta_tag():
    meta_tag = """
        <head>
            <meta name="google-site-verification" content="QBiAoAo1GAkCBe1QoWq-dQ1RjtPHeFPyzkqJqsrqW-s" />
            <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700&display=swap" />
        </head>
    """
    st.markdown(meta_tag, unsafe_allow_html=True)

add_meta_tag()

# CSS for custom styling
st.markdown("""
    <style>
    body {
        font-family: 'Roboto', sans-serif;
        background-color: #f4f4f9;
    }
    .sidebar .sidebar-content {
        background-image: linear-gradient(#0a3d62,#0a3d62);
        color: white;
    }
    .big-font {
        font-size: 24px !important;
        color: #0a3d62;
    }
    .medium-font {
        font-size: 18px !important;
    }
    .small-font {
        font-size: 14px !important;
    }
    .stButton>button {
        background-color: #0a3d62;
        color: white;
        border: none;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 12px;
    }
    .stButton>button:hover {
        background-color: #0a3d62;
        color: #ffffff;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar Section Starts Here
today = date.today()  # today's date
st.sidebar.image("Images/logo.png", width=300, use_column_width=False)  # logo
st.sidebar.write('''# StockNavigator''')

with st.sidebar: 
    selected = option_menu(
        "Utilities", 
        ["Stock Performance Comparison", "Real-Time Stock Price", "Stock Prediction", 'About'], 
        icons=['bar-chart', 'bar-chart', 'bar-chart', 'info-circle'],
        menu_icon="cast",
        default_index=0,
    )

start = st.sidebar.date_input('Start', datetime.date(2021, 1, 1))  # start date input
end = st.sidebar.date_input('End', datetime.date.today())  # end date input
# Sidebar Section Ends Here

# Read CSV file
stock_df = pd.read_csv("StockNavigationData.csv")

# Function to show info about stock terms
def show_info(term, description):
    st.info(f"**{term}:** {description}")

# Stock Performance Comparison Section Starts Here
if selected == 'Stock Performance Comparison':
    st.markdown("<h2 class='big-font'>Stock Performance Comparison</h2>", unsafe_allow_html=True)
    st.write("Compare the performance of multiple stocks over a specified period.")
    st.info("**Relative Return:** The return of an asset compared to a benchmark or another asset.")
    st.info("**Closing Price:** The price of a stock at the end of the trading day.")
    st.info("**Volume:** The total number of shares traded during the trading day.")

    tickers = stock_df["Company Name"]
    dropdown = st.multiselect('Pick your assets', tickers, help="Select multiple assets to compare their performance.")

    with st.spinner('Loading...'):
        time.sleep(3)

    dict_csv = pd.read_csv('StockNavigationData.csv', header=None, index_col=0).to_dict()[1]
    symb_list = [dict_csv.get(i) for i in dropdown]

    def relativeret(df):
        rel = df.pct_change()
        cumret = (1 + rel).cumprod() - 1
        return cumret.fillna(0)

    if dropdown:
        df = relativeret(yf.download(symb_list, start, end))['Adj Close']
        raw_df = relativeret(yf.download(symb_list, start, end))
        raw_df.reset_index(inplace=True)

        closingPrice = yf.download(symb_list, start, end)['Adj Close']
        volume = yf.download(symb_list, start, end)['Volume']

        st.subheader(f'Raw Data for {", ".join(dropdown)}')
        st.dataframe(raw_df.style.set_properties(**{'text-align': 'left'}))

        chart_types = ('Line Chart', 'Area Chart', 'Bar Chart')
        dropdown1 = st.selectbox('Pick your chart', chart_types, help="Select the type of chart to visualize the data.")

        with st.spinner('Loading...'):
            time.sleep(3)

        st.subheader(f'Relative Returns for {", ".join(dropdown)}')

        if dropdown1 == 'Line Chart':
            st.line_chart(df)
            st.write(f"### Closing Price of {', '.join(dropdown)}")
            st.line_chart(closingPrice)
            st.write(f"### Volume of {', '.join(dropdown)}")
            st.line_chart(volume)

        elif dropdown1 == 'Area Chart':
            st.area_chart(df)
            st.write(f"### Closing Price of {', '.join(dropdown)}")
            st.area_chart(closingPrice)
            st.write(f"### Volume of {', '.join(dropdown)}")
            st.area_chart(volume)

        elif dropdown1 == 'Bar Chart':
            st.bar_chart(df)
            st.write(f"### Closing Price of {', '.join(dropdown)}")
            st.bar_chart(closingPrice)
            st.write(f"### Volume of {', '.join(dropdown)}")
            st.bar_chart(volume)

    else:
        st.warning('Please select at least one asset to compare.')
# Stock Performance Comparison Section Ends Here
    
# Real-Time Stock Price Section Starts Here
elif selected == 'Real-Time Stock Price':
    st.markdown("<h2 class='big-font'>Real-Time Stock Price</h2>", unsafe_allow_html=True)
    st.write("View the real-time stock price of a selected company. Real-time data is continuously updated during market hours.")
    st.info("**Candlestick Chart:** A type of financial chart used to describe price movements of a security, derivative, or currency.")
    st.info("**Line Chart:** A type of chart which displays information as a series of data points called 'markers' connected by straight line segments.")
    st.info("**Open:** The price at which a stock first trades upon the opening of an exchange on a trading day.")
    st.info("**Close:** The final price at which a stock is traded on a given trading day.")
    st.info("**High:** The highest price at which a stock traded during a period.")
    st.info("**Low:** The lowest price at which a stock traded during a period.")

    tickers = stock_df["Company Name"]
    company = st.selectbox('Pick a Company', tickers, help="Select a company to view its real-time stock price.")

    with st.spinner('Loading...'):
        time.sleep(3)

    dict_csv = pd.read_csv('StockNavigationData.csv', header=None, index_col=0).to_dict()[1]
    symb_list = [dict_csv.get(company)]

    if "button_clicked" not in st.session_state:
        st.session_state.button_clicked = False

    def callback():
        st.session_state.button_clicked = True

    if st.button("Search", on_click=callback) or st.session_state.button_clicked:
        if company:
            data = yf.download(symb_list, start=start, end=end)
            data.reset_index(inplace=True)
            st.subheader(f'Raw Data of {company}')
            st.dataframe(data.style.set_properties(**{'text-align': 'left'}))

            def plot_raw_data():
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name="stock_open"))
                fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="stock_close"))
                fig.layout.update(title_text=f'Line Chart of {company}', xaxis_rangeslider_visible=True)
                st.plotly_chart(fig)

            def plot_candle_data():
                fig = go.Figure()
                fig.add_trace(go.Candlestick(x=data['Date'], open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'], name='market data'))
                fig.update_layout(title=f'Candlestick Chart of {company}', yaxis_title='Stock Price', xaxis_title='Date')
                st.plotly_chart(fig)

            chart_types = ('Candle Stick', 'Line Chart')
            dropdown1 = st.selectbox('Pick your chart', chart_types, help="Select the type of chart to visualize the data.")
            
            with st.spinner('Loading...'):
                time.sleep(3)
                
            if dropdown1 == 'Candle Stick':
                plot_candle_data()
            elif dropdown1 == 'Line Chart':
                plot_raw_data()
        else:
            st.warning("Click Search to view the company's stock price.")
# Real-Time Stock Price Section Ends Here

# Stock Price Prediction Section Starts Here
elif selected == 'Stock Prediction':
    st.markdown("<h2 class='big-font'>Stock Prediction</h2>", unsafe_allow_html=True)
    st.write("Predict the future stock price of a selected company using the Prophet model. The forecast will be displayed for the next year.")
    st.info("**Prophet Model:** A forecasting procedure implemented in R and Python. It is used to predict time series data based on an additive model where non-linear trends are fit with yearly, weekly, and daily seasonality, plus holiday effects.")
    st.info("**Date:** The specific day when the stock data was recorded.")
    st.info("**Close:** The final price at which a stock is traded on a given trading day.")
    st.info("**Forecast Components:** The individual contributing elements (trend, weekly, yearly) that make up the forecast.")
    
    tickers = stock_df["Company Name"]
    company = st.selectbox('Pick a Company', tickers, help="Select a company to predict its future stock price.")

    with st.spinner('Loading...'):
        time.sleep(3)

    dict_csv = pd.read_csv('StockNavigationData.csv', header=None, index_col=0).to_dict()[1]
    symb_list = [dict_csv.get(company)]

    if company:
        data = yf.download(symb_list, start=start, end=end)
        data.reset_index(inplace=True)
        st.subheader(f'Raw Data of {company}')
        st.dataframe(data.style.set_properties(**{'text-align': 'left'}))

        df_train = data[['Date', 'Close']]
        df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

        m = Prophet()
        m.fit(df_train)
        future = m.make_future_dataframe(periods=365)
        forecast = m.predict(future)

        st.subheader(f'Forecast data of {company}')
        st.write(forecast.tail())

        st.write('Forecast data')
        fig1 = plot_plotly(m, forecast)
        st.plotly_chart(fig1)

        st.write("Forecast components")
        fig2 = m.plot_components(forecast)
        st.write(fig2)
    else:
        st.warning("Please select a company to predict its stock price.")
# Stock Price Prediction Section Ends Here

# About Section Starts Here
elif selected == 'About':
    st.markdown("<h2 class='big-font'>About</h2>", unsafe_allow_html=True)
    st.markdown('''
        <p class="medium-font">
        StockNavigator is your ultimate destination for monitoring stock performance, obtaining real-time stock prices, and predicting future stock prices using cutting-edge technology like the Facebook Prophet Model for Stock Price Prediction. Developed using Streamlit, an open-source app framework in Python, StockNavigator enables easy creation of web apps tailored for Data Science and Machine Learning.
        <br><br>
        This financial project has been developed by <strong>Manoswita Bose</strong>, a student pursuing MCA at CHRIST (Deemed-to-be University), Bengaluru. Manoswita is a self-proclaimed code struggler and habitual procrastinator who would rather be scribbling secret stories in her notebook during her spare hours. Writing in the third person is a personal pet peeve, yet here we are. Manoswita's diverse skill set is matched only by her ability to laugh at herself – an invaluable trait in the ever-evolving landscape of digital creativity.
        <br><br>
        Streamlit's user-friendly interface and powerful capabilities have made it possible to develop StockNavigator efficiently, providing a robust platform for both novice investors and seasoned traders to make informed decisions. Hope this application meets your needs. Enjoy exploring StockNavigator!
        <br><br>
        </p>
    ''', unsafe_allow_html=True)
# About Section Ends Here
