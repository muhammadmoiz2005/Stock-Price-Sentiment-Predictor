import streamlit as st
import pandas as pd
import time
from pathlib import Path

from data_ingest import get_latest_price, get_historical_klines
from sentiment import analyze_sentiment
from model_predict import predict_from_row
from chatbot import ask_chatbot
from utils import log_event

st.set_page_config(page_title='Stock Price & Sentiment Predictor', layout='wide')
st.title('📈 Stock Price & Sentiment Predictor')

tabs = st.tabs(['Dashboard','Predict & Train','Chatbot','Logs'])

# -------- Dashboard --------
with tabs[0]:
    col1, col2 = st.columns([2,1])
    with col1:
        st.subheader('Live Price & Historical Chart')
        symbol = st.selectbox('Symbol', ['BTCUSDT'])
        run_stream = st.checkbox('Start Live Stream', value=False)
        placeholder = st.empty()
        chart_placeholder = st.empty()

        # Load historical (or synthetic) for chart
        hist = get_historical_klines(symbol=symbol, interval='1m', limit=300)
        hist = hist.set_index('timestamp')
        chart = chart_placeholder.line_chart(hist['close'])

        if run_stream:
            st.info('Streaming live prices every 5s (if Biybit API Keys are set).')
            try:
                while run_stream:
                    price = get_latest_price(symbol)
                    if price is not None:
                        placeholder.metric(label=f'{symbol} Price (USD)', value=f'${price:,.2f}')
                        # append to dataframe for chart
                        new_row = pd.DataFrame({'close':[price]}, index=[pd.to_datetime(pd.Timestamp.utcnow())])
                        hist = pd.concat([hist, new_row]).iloc[-300:]
                        chart.add_rows(new_row)
                        log_event('STREAM', f'{symbol} {price}')
                    else:
                        placeholder.info('Live client available; showing historical/sample data.')
                    time.sleep(5)
            except Exception as e:
                st.error(f'Error in streaming loop: {e}')
    with col2:
        st.subheader('Sentiment Scanner')
        txt = st.text_area('Paste tweet or news text to analyze:')
        if st.button('Analyze Sentiment'):
            if txt.strip():
                out = analyze_sentiment(txt)
                st.write(out)
                log_event('SENTIMENT', str(out))
            else:
                st.warning('Enter text first.')

# -------- Predict & Train --------
with tabs[1]:
    st.subheader('Train model on historical data')
    if st.button('Train Model (uses data/historical.csv)'):
        from model_train import train_and_save
        try:
            train_and_save()
            st.success('Model trained and saved to models/price_predictor.pkl')
            log_event('MODEL', 'trained')
        except Exception as e:
            st.error(f'Training failed: {e}')
            log_event('ERROR', f'train_failed: {e}')

    st.divider()
    st.subheader('Predict latest direction (demo)')
    if st.button('Predict Using Last Row'):
        try:
            df = get_historical_klines(limit=30)
            df_feat = pd.read_csv('data/historical.csv', parse_dates=['timestamp']) if Path('data/historical.csv').exists() else df
            # prepare features similar to training
            df_feat['return'] = df_feat['close'].pct_change()
            df_feat['ma_3'] = df_feat['close'].rolling(3).mean()
            df_feat['ma_10'] = df_feat['close'].rolling(10).mean()
            df_feat['vol_3'] = df_feat['volume'].rolling(3).mean()
            row = df_feat.dropna().iloc[-1]
            pred = predict_from_row(row)
            st.write('Prediction:', pred)
            log_event('PREDICT', str(pred))
        except Exception as e:
            st.error(f'Prediction failed: {e}')
            log_event('ERROR', f'predict_failed: {e}')

# -------- Chatbot --------
with tabs[2]:
    st.subheader('AI Market Chatbot')
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = None
    user_input = st.text_input('Ask the market assistant a question:')
    if st.button('Send'):
        if user_input.strip():
            reply, st.session_state.chat_history = ask_chatbot(user_input, history=st.session_state.chat_history)
            st.markdown('**Assistant:** ' + reply)
            log_event('CHAT', user_input)
        else:
            st.warning('Write something first.')

# -------- Logs --------
with tabs[3]:
    st.subheader('Recent System Logs')
    import csv
    try:
        df = pd.read_csv('logs/system_logs.csv')
        st.dataframe(df.tail(200))
    except Exception:
        st.info('No logs yet.')
