from flask import Flask, render_template, request 
from EmotionDetection.emotion_detection import emotion_detector
# Initialize the Flask application
app = Flask(__name__)


@app.route('/emotionDetector')
def detect_emotion():
    """
    Endpoint that receives text via query parameters and returns 
    a formatted string detailing the emotion scores and dominant emotion.
    """
    # Retrieve the text to analyze from the request arguments
    text_to_analyze = request.args.get('textToAnalyze')

    # Pass the text to the imported emotion_detector function
    response = emotion_detector(text_to_analyze)

    # Error handling for empty or invalid input
    if response['dominant_emotion'] is None:
        return "Invalid text! Please try again."

    # Format the output string exactly as requested by the customer
    formatted_response = (
        f"For the given statement, the system response is "
        f"'anger': {response['anger']}, "
        f"'disgust': {response['disgust']}, "
        f"'fear': {response['fear']}, "
        f"'joy': {response['joy']} and "
        f"'sadness': {response['sadness']}. "
        f"The dominant emotion is {response['dominant_emotion']}."
    )

    return formatted_response


@app.route('/')
def render_index_page():
    """
    Main application route that returns a simple running status.
    """
    return "Emotion Detector is running. Navigate to /emotionDetector"


if __name__ == '__main__':
    # Deploy the application on localhost:5000
    app.run(host='0.0.0.0', port=5000, debug=True)