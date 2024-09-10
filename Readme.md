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
