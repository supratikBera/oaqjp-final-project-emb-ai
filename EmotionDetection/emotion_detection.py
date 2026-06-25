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