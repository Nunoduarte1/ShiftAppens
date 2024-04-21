from textblob import TextBlob

# Example text
text = "hp comes to terms with the cloud,hewlett-packard has decided it cannot compete with the likes of amazon and google for one of the hottest new businesses. instead, on the eve of its split into two companies, hp is learning about collaborative technologies, and not just for its customers"

# Perform sentiment analysis
blob = TextBlob(text)
sentiment = blob.sentiment

# Print sentiment
print("Sentiment:", sentiment)