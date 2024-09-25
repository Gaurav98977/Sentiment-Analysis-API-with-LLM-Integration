from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# Function to process the uploaded file and extract reviews
def process_file(file):
    df = pd.read_excel(file)
    
    # Extracting the 'Review' column
    if 'Review' in df.columns:
        reviews = df['Review'].tolist()
    else:
        return None, "No 'Review' column found in the file."
    
    return reviews, None

# Mock sentiment analysis function
def perform_sentiment_analysis(reviews):
    positive, negative, neutral = 0, 0, 0
    
    # Mock logic for sentiment classification based on keywords
    for review in reviews:
        if any(word in review.lower() for word in ["great", "fantastic", "exceeded"]):
            positive += 1
        elif any(word in review.lower() for word in ["poor", "terrible", "bad"]):
            negative += 1
        else:
            neutral += 1
    
    return {
        "positive": positive,
        "negative": negative,
        "neutral": neutral
    }

# Route to handle file upload and sentiment analysis
@app.route('/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    reviews, error = process_file(file)
    
    if error:
        return jsonify({"error": error}), 400

    # Perform sentiment analysis on the extracted reviews
    sentiment_results = perform_sentiment_analysis(reviews)
    
    return jsonify(sentiment_results)

if __name__ == '__main__':
    app.run(debug=True)
