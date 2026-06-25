# Repository for final project
project name : Final project
# 2a_emotion_detection
import requests

def emotion_detector(text_to_analyze):
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    input_json = { "raw_document": { "text": text_to_analyze } }
    
    # Make the POST request to the API
    response = requests.post(url, headers=headers, json=input_json)
    
    # Return the response as a dictionary
    return response.json()
# 2b_emotion_detection
python3.11
Python 3.11.14 (main, Oct 10 2025, 08:54:03) [GCC 11.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from emotion_detection import emotion_detector
>>> emotion_detector("I love this new technology")
{'emotionPredictions': [{'emotion': {'anger': 0.0132405795, 'disgust': 0.0020517302, 'fear': 0.009090992, 'joy': 0.9699522, 'sadness': 0.054984167}, 'target': '', 'emotionMentions': [{'span': {'begin': 0, 'end': 26, 'text': 'I love this new technology'}, 'emotion': {'anger': 0.0132405795, 'disgust': 0.0020517302, 'fear': 0.009090992, 'joy': 0.9699522, 'sadness': 0.054984167}}]}], 'producerId': {'name': 'Ensemble Aggregated Emotion Workflow', 'version': '0.0.1'}}
# 3a_output_formatting
import requests
import json

def emotion_detector(text_to_analyze):
    # 1. Define the API request parameters
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    input_json = { "raw_document": { "text": text_to_analyze } }
    
    # 2. Make the POST request
    response = requests.post(url, headers=headers, json=input_json)
    
    # 3. Convert the response text into a dictionary using the json library
    formatted_response = json.loads(response.text)
    
    # 4. Extract the required set of emotions
    # (Assuming standard Watson NLP emotion output structure)
    emotions = formatted_response['emotionPredictions'][0]['emotion']
    
    anger_score = emotions.get('anger', 0)
    disgust_score = emotions.get('disgust', 0)
    fear_score = emotions.get('fear', 0)
    joy_score = emotions.get('joy', 0)
    sadness_score = emotions.get('sadness', 0)
    
    # 5. Write the logic to find the dominant emotion
    emotion_scores = {
        'anger': anger_score,
        'disgust': disgust_score,
        'fear': fear_score,
        'joy': joy_score,
        'sadness': sadness_score
    }
    
    # max() looks at the values (using .get) and returns the corresponding key
    dominant_emotion = max(emotion_scores, key=emotion_scores.get)
    
    # 6. Return the final formatted dictionary
    return {
        'anger': anger_score,
        'disgust': disgust_score,
        'fear': fear_score,
        'joy': joy_score,
        'sadness': sadness_score,
        'dominant_emotion': dominant_emotion
    }
# 3b_formatted_output_test
python3.11
Python 3.11.14 (main, Oct 10 2025, 08:54:03) [GCC 11.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from emotion_detection import emotion_detector
>>> emotion_detector("I love this new technology")
{'anger': 0.0132405795, 'disgust': 0.0020517302, 'fear': 0.009090992, 'joy': 0.9699522, 'sadness': 0.054984167, 'dominant_emotion': 'joy'}
# 4b_packaging_test
from EmotionDetection.emotion_detection import emotion_detector
>>> emotion_detector("I hate this technology")
{'anger': 0.66664743, 'disgust': 0.046570558, 'fear': 0.024311474, 'joy': 0.015504743, 'sadness': 0.2439738, 'dominant_emotion': 'anger'}
# 5a_unit_testing
from EmotionDetection.emotion_detection import emotion_detector
import unittest
class TestEmotionDetection(unittest.TestCase):
    def test_emotion_detector(self):
        result_1 = emotion_detector("I am glad this happened")
        self.assertEqual(result_1['dominant_emotion'], 'joy')
        
        # Test case 2: Anger
        result_2 = emotion_detector("I am really mad about this")
        self.assertEqual(result_2['dominant_emotion'], 'anger')
        
        # Test case 3: Disgust
        result_3 = emotion_detector("I feel disgusted just hearing about this")
        self.assertEqual(result_3['dominant_emotion'], 'disgust')
        
        # Test case 4: Sadness
        result_4 = emotion_detector("I am so sad about this")
        self.assertEqual(result_4['dominant_emotion'], 'sadness')
        
        # Test case 5: Fear
        result_5 = emotion_detector("I am really afraid that this will happen")
        self.assertEqual(result_5['dominant_emotion'], 'fear')
if __name__ == '__main__':
    unittest.main()
# 5b_unit_testing_result
    python3.
.
----------------------------------------------------------------------
Ran 1 test in 0.611s

OK
# 6a_server
from flask import Flask, render_template, request 
from EmotionDetection.emotion_detection import emotion_detector
app = Flask(__name__)
@app.route('/emotionDetector')
def detect_emotion():
    """
    Analyzes the text provided in the query parameters and 
    returns a formatted string with the emotion scores.
    """
    # Retrieve the text to analyze from the request arguments
    text_to_analyze = request.args.get('textToAnalyze')
    
    # Pass the text to the imported emotion_detector function
    response = emotion_detector(text_to_analyze)
    
    # Error handling for empty or invalid input (optional but recommended)
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
    Placeholder for the main application route.
    Typically, this renders the index.html template.
    """
    return "Emotion Detector is running. Navigate to /emotionDetector?textToAnalyze=your_text_here"

if __name__ == '__main__':
    # Deploy the application on localhost:5000
    app.run(host='0.0.0.0', port=5000, debug=True)
# 7a_error_handling
import requests
import json

def emotion_detector(text_to_analyze):
    # 1. Define the API request parameters
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    input_json = { "raw_document": { "text": text_to_analyze } }
    
    # 2. Make the POST request
    response = requests.post(url, headers=headers, json=input_json)
    
    # 3. Error Handling: Check for a 400 Bad Request status code
    if response.status_code == 400:
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }
    
    # 4. If the request was successful, parse the JSON response
    formatted_response = json.loads(response.text)
    
    # Extract the required set of emotions
    emotions = formatted_response['emotionPredictions'][0]['emotion']
    
    anger_score = emotions.get('anger', 0)
    disgust_score = emotions.get('disgust', 0)
    fear_score = emotions.get('fear', 0)
    joy_score = emotions.get('joy', 0)
    sadness_score = emotions.get('sadness', 0)
    
    # 5. Write the logic to find the dominant emotion
    emotion_scores = {
        'anger': anger_score,
        'disgust': disgust_score,
        'fear': fear_score,
        'joy': joy_score,
        'sadness': sadness_score
    }
    
    dominant_emotion = max(emotion_scores, key=emotion_scores.get)
    
    # 6. Return the final formatted dictionary
    return {
        'anger': anger_score,
        'disgust': disgust_score,
        'fear': fear_score,
        'joy': joy_score,
        'sadness': sadness_score,
        'dominant_emotion': dominant_emotion
    }
# 8a_server_modified
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



