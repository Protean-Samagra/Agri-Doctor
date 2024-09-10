# Agri Doctor: Agronomy Advice API

This project involves developing robust APIs for an Agronomy application called **Agri Doctor** that leverages AI and Machine Learning on historical data to offer personalized agricultural advice and predictive analytics. The APIs enable features such as disease prediction, fertilizer recommendations and nutrition advice to increase crop yield, with multilingual support for all Indian regional languages.

## Project Description

The **Agri Doctor** API suite is designed to support Indian farmers by providing tailored agricultural recommendations using public data and AI/ML models. It aims to assist with disease prediction, seed/fertilizer recommendations, nutrition advice, and yield improvement insights to help farmers make data-driven decisions for better crop health and descreased losses.

Key Features:
- **Crop Prediction API**: Predicts crop type from the image uploaded by the farmer.
- **Disease Prediction API**: Predicts crop disease from the crop type and image uploaded by the farmer.
- **Personalized Agri-Advice API**: Tailored recommendations based on crop type, crop disease and current weather conditions.

## Prerequisites

Before running the project, ensure you have the following tools installed:

- **Python 3.8+**: Required to run the Flask application.
- **Ollama**: [Install Ollama](https://github.com/ollama/ollama) for advice generation.
- **Postman**: [Download Postman](https://www.postman.com/downloads/) for testing API endpoints.
- **Swagger UI**: Swagger is already integrated into the project for API documentation. Access it after running the Flask app at:
  ```
  http://127.0.0.1:5000/swagger
  ```

## Installation

### Steps
1. Clone the repository:
   ```
   git clone https://github.com/Protean-Samagra/Agri-Doctor
   cd your-project-folder
   ```

2. Install the required dependencies:
   ```
   pip install flask_restful
   pip install flask_swagger_ui
   ```

3. Update the necessary URLs in the code:
   - **Swagger UI URL**: 
     ```python
     API_URL = 'http://127.0.0.1:5000/swagger.json'  # Localhost example
     ```
   - **Weather API Key**: Update your `apikey` in `params`:
     ```python
     params2 = {'apikey': 'your_weather_api_key'}
     params = {'apikey': 'your_weather_api_key'}
     ```
   - **Machine Learning API URL**: Update the URL for the ML service:
     ```python
     url = "http://localhost:11434/api/generate"  # Update if necessary
     ```
## Methodology

1. Setting up the Flask Application:
- Start by creating a Flask app, which acts as a web server to handle different HTTP requests.
- Set up Swagger UI to provide interactive documentation for your API using Flask-RESTful and flask_swagger_ui.

2. City API:
- The /city endpoint hits an external weather service API (AccuWeather) to retrieve information about the city (in this case, 'Bangalore').
- The city_url points to the API for fetching city data based on the provided city name.
- You pass an API key and the city name as parameters (params2), then extract the location_key from the response JSON, which is necessary for retrieving weather information.

3. Weather API:
- The /weather endpoint uses the location_key from the city API to form the resource URL for the weather API.
- It hits the AccuWeather API again, using location_key to get real-time weather data, including conditions such as weather type, temperature, and units.
- This weather data is converted from JSON to string format and stored in the weather_prompt variable. This prompt will be passed later for further processing.

4. Machine Learning Model Integration:
- The /processing endpoint allows the user to upload an image file, representing the crop, along with a language preference.
- The uploaded image is processed using preprocess_image, which resizes and normalizes the image to make it suitable for the ML model.
- A pre-trained TensorFlow model (loaded from your local machine) is used to predict the crop's disease based on the image.
- The model predicts the disease by outputting a class index that maps to a list of diseases (disease_class_names). The predicted class is split into crop_type and disease_type.

5. Creating a Prompt:
- The weather_prompt (containing the weather information), along with the predicted crop_type and disease_type, is used to generate a prompt.
- The prompt is designed to simulate asking a plant pathologist for advice, which includes recommendations for fertilizer, chemicals, organic treatments, and practices tailored to the weather conditions.

6. Passing the Prompt to Ollama:
- You send this generated prompt to an AI model running on the Ollama server via a POST request.
- You can use various models. In english the best response is observed by "llama3.1". For Indic languages- "qwen2:1.5b".
- The response from the model contains the professional advice based on the crop and disease condition, which is returned to the user.

## Usage

1. Start the Flask application:
   ```
   flask run
   ```
2. Test the APIs on Postman
   - Create a get api: To hit the City search API: https://developer.accuweather.com/accuweather-locations-api/apis/get/locations/v1/cities/search
       - Example url: http://127.0.0.1:5000/city
   - Create a get api: To hit the Current conditions API: https://developer.accuweather.com/accuweather-current-conditions-api/apis/get/currentconditions/v1/%7BlocationKey%7D
       - Example url: http://127.0.0.1:5000/weather
   - Create a post api: To hit the Machine learning model and Ollama
        - Example url: http://127.0.0.1:5000/processing
        - Key: file; Value: <image file>
        - Key: language; Value: <Language, eg: Hindi, English>
     
2. Access the Swagger UI for API documentation at:
   ```
   http://127.0.0.1:5000/swagger
   ```

## Ollama Setup

1. Install Ollama by following the instructions [here](https://github.com/ollama/ollama).

2. Pull the model required:
   ```
   ollama pull qwen2:1.5b
   ```
3. If the port is busy, set a different port:
   ```
   set OLLAMA_HOST=127.0.0.1:11435
   ```
4. Start the Ollama server:
   ```
   ollama serve
   ```

5. Ensure the Flask application points to the correct Ollama server port:
   ```python
   url = "http://localhost:11434/api/generate"
   ```
