# Stock Price & Sentiment Predictor

## 1. Introduction
The **Stock Price & Sentiment Predictor** is a Python-based platform that analyzes historical stock/crypto data and performs sentiment analysis on related news or social media posts. The system helps users understand market trends and make informed predictions.

## 2. Objectives
- Analyze historical stock/crypto data.
- Perform sentiment analysis on news or social media content.
- Predict short-term price trends using ML models.
- Provide an interactive and visual dashboard for better understanding.

## 3. Features Implemented
- Historical data visualization from `historical.csv`.
- Sentiment analysis using TextBlob / Transformer-based models.
- Simple ML predictive model RandomForestClassifier.
- Streamlit frontend dashboard for interactive visualization.
- Modular backend for easy updates.

## 4. Tech Stack & Tools
- **Python 3.x**
- **Streamlit** (Frontend dashboard)
- **Pandas & NumPy** (Data processing)
- **Scikit-learn** (Machine Learning)
- **TextBlob / Transformers** (Sentiment analysis)
- **Matplotlib & Seaborn** (Visualization)
- **Bybit API / ccxt** (Realtime data, optional)
- **Logging** for monitoring predictions

## 5. System Architecture / Flow Diagram
```
[Historical.csv] ---> [Data Preprocessing] ---> [Sentiment Analysis] ---> [ML Model Prediction] ---> [Streamlit Dashboard]
[Optional: Bybit API] ---> [Realtime Data Fetching] ---> [Dashboard Update]
```

## 6. Installation & Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) Add Bybit API keys in `.env` for realtime data:
```text
API_KEY=your_api_key
API_SECRET=your_api_secret
```

## 7. How to Use (User Guide)
1. Run the Streamlit app:
```bash
streamlit run app.py
```

2. Open the local URL in your browser (usually `http://localhost:8501`).

3. Enter the **stock/crypto symbol** to view:
- Historical price graph
- Sentiment analysis
- ML predictions
- Volume & trend visualizations

**Note:** Without Bybit API keys, **real-time data will not appear**.

## 8. Project Implementation Steps
1. Load historical data from `historical.csv`.
2. Preprocess data (cleaning, missing values, timestamp adjustments).
3. Perform sentiment analysis on textual content.
4. Train simple ML models for prediction.
5. Integrate modules into Streamlit dashboard.
6. (Optional) Fetch realtime data using Bybit API and update dashboard.

## 9. Model Details & Performance
- **Models Used:** Random Forest, Logistic Regression
- **Features:** Open, High, Low, Close, Volume, Sentiment Score
- **Performance:** Accuracy up to ~88% on historical dataset

## 10. Screenshots
*Add your screenshots here showing:*
- Dashboard main interface
- Historical graphs
- Sentiment analysis results
- Prediction outputs

## 11. Achievements / Completed Work
- Fully functional dashboard with historical data visualization.
- Sentiment analysis integration.
- Predictive ML model working.
- Modular Python backend for scalability.

## 12. Challenges Faced & Solutions
- **Challenge:** Historical data had missing timestamps → **Solution:** Cleaned and adjusted timestamps.
- **Challenge:** Very large volume numbers in CSV → **Solution:** Converted to readable format (6–7 digit).
- **Challenge:** Real-time API integration optional → **Solution:** Made API integration optional via keys.

## 13. Future Enhancements
- Integrate **multi-exchange support** for more data.
- Use advanced ML/DL models (LSTM, Transformers) for better prediction.
- Add alerts & notifications for significant price changes.
- Deploy on **Streamlit Cloud / Heroku** for live access.

## 14. Conclusion
The **Stock Price & Sentiment Predictor** is a modular, interactive, and scalable system for analyzing stock/crypto trends and public sentiment. It provides a solid foundation for building advanced predictive analytics tools in trading.

