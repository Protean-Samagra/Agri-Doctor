from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os
import tensorflow as tf
import numpy as np
from PIL import Image
import requests
import json

from flask_swagger_ui import get_swaggerui_blueprint
from flask_restful import Resource, Api

app = Flask(__name__)

# Configure Swagger UI
SWAGGER_URL = '/swagger'
API_URL = 'http://127.0.0.1:5000/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Sample API"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@app.route('/swagger.json')
def swagger():
    with open('swagger.json', 'r') as f:
        return jsonify(json.load(f))

# CITY 
city_url = "http://dataservice.accuweather.com/locations/v1/cities/search"
params2 = {
    'apikey': "2KKl77kWEt4A4Uejje97IC6ENw9fDs3G",
    'q': 'Bangalore'
}

@app.route('/city', methods=['GET'])
def getcity():
    global location_key
    response = requests.get(city_url, params=params2)  # Making GET request to weather API with given params
    if response.status_code == 200: #If it's successful in getting the data from API
        data = response.json() #Converting json response to list data structure
        location_key = data[0]["Key"]
    else: 
        return "Unsuccessful in hitting API"
    return jsonify([{"Location key" : location_key}])

# WEATHER  
params = {
    'apikey': "2KKl77kWEt4A4Uejje97IC6ENw9fDs3G",
}

@app.route('/weather', methods=['GET'])
def getweather():
    global weather_prompt
    weather_url = "http://dataservice.accuweather.com/currentconditions/v1/" + str(location_key )
    response = requests.get(weather_url, params=params)  # Making GET request to weather API with given params
    if response.status_code == 200: #If it's successful in getting the data from API
        data = response.json() #Converting json response to list data structure
        weatherText = data[0]["WeatherText"]
        temperature = data[0]["Temperature"]["Metric"]["Value"]
        temp_unit = data[0]["Temperature"]["Metric"]["Unit"]
        weather_prompt = str(weatherText)+" with "+str(temperature)+str(temp_unit)
    else: 
        return "Unsuccessful in hitting API"
    return jsonify([{"Data":data}])

# MACHINE LEARNING 
url = "http://localhost:11434/api/generate"
headers = {
    'Content-Type':'application/json',
}
CORS(app) 

@app.route('/processing', methods=['POST'])
def loadmodel():
    if request.method == 'POST':
        f = request.files['file']
        lang = request.form['language']
        print(lang)

        filename = secure_filename(f.filename)
        file_path = os.path.join(os.getcwd(), filename)
        f.save(file_path)

        def preprocess_image(image_path, target_size):
            img = Image.open(image_path).resize(target_size)  # Resize to match model's input shape
            img_array = np.array(img).astype('float32') / 255.0  # Normalize to [0, 1] range
            img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
            return img_array

        disease_detection_target_size = (224, 224)  # Resize to match model's input shape
        img_array_for_disease = preprocess_image(file_path, disease_detection_target_size)
        disease_detection_model = tf.keras.models.load_model(r'C:/Users/ITBS/Desktop/disease_detection.keras')
        
        disease_predictions = disease_detection_model.predict(img_array_for_disease)
        disease_class_index = np.argmax(disease_predictions, axis=1)[0]
        disease_class_names = ['Corn_blight', 'Corn_common_rust', 'Corn_gray_leaf_spot', 'Corn_healthy', 
                            'Potato_Early_Blight', 'Potato_Healthy', 'Potato_Late_Blight', 
                            'Rice_BrownSpot', 'Rice_Healthy', 'Rice_Hispa', 'Rice_LeafBlast', 
                            'Tomato_bacterial_spot', 'Tomato_early_blight', 'Tomato_healthy', 
                            'Tomato_late_blight', 'Tomato_leaf_miner', 'Tomato_spotted_wilt_virus', 
                            'Wheat_Brown_Rust', 'Wheat_Healthy', 'Wheat_Yellow_Rust']
        predicted_disease = disease_class_names[disease_class_index]
        crop_type, disease_type = predicted_disease.split('_')

        if not lang:
            lang = "English"
        prompt = "Imagine you are a plant pathologist. I am a farmer with "+crop_type+" crop which has "+disease_type+" disease. Produce a professional report of bullet points including 1. Fertilizer cure for the disease 2. Chemical cure for the disease 3. Organics cure for the disease 4. General practises based on weather of the place I am at which is "+weather_prompt+" to increase yield. Give your answer in "+lang+" language."
        print("Prompt: ",prompt)

        data = {
            "model":"gemma2:2b",
            "prompt":prompt,
            "stream":False
        }
        
        response = requests.post(url, headers = headers, data=json.dumps(data))

        if response.status_code == 200:
            response = response.text
            data = json.loads(response)
            actual_response = data['response']
            return actual_response
        else:
            print("Error:",response.text)
        return jsonify({"Reponse": actual_response})
    print(actual_response)

if __name__ == '__main__':
    app.run(port=5000)
