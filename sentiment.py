from textblob import TextBlob

def analyze_sentiment(text: str) -> dict:
    """Return dict with polarity score and label."""
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0.1:
        label = "Positive"
    elif polarity < -0.1:
        label = "Negative"
    else:
        label = "Neutral"
    return {"polarity": polarity, "label": label}
