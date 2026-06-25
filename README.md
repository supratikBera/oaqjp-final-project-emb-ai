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

