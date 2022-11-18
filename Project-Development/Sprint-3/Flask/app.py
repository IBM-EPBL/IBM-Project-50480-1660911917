from flask import Flask, render_template, request
from keras.models import load_model
from keras.preprocessing.image import image_utils
from os import path, environ
from requests import get
import numpy as np

API_KEY = environ.get("API_KEY")
API_HOST = environ.get("API_HOST")

app = Flask(__name__)
model = load_model('./model.h5')
url = "https://calorieninjas.p.rapidapi.com/v1/nutrition"
headers = {
	"X-RapidAPI-Key": API_KEY,
	"X-RapidAPI-Host": API_HOST
}
print("\nModel loaded\n")

def save_image(file):
    root_path = path.dirname(__file__)
    file_path = path.join(root_path, 'uploads', file.filename)
    file.save(file_path)

    print(f"\nFILE SAVED: {file.filename} at {file_path}\n")
    return file_path

def predict(file_path):
    # preprocessing the image
    file = image_utils.load_img(file_path, target_size=(64,64))
    file = image_utils.img_to_array(file)
    x = np.expand_dims(file, axis=0)

    # classifying the image
    prediction = model.predict(x)[0]
    max_index = np.where(prediction == np.amax(prediction))[0]
    labels = ["Apple", 'Banana', 'Orange', 'Pineapple', 'Watermelon']

    print(f"""
PREDICTIONS: 
 - {labels[0]} = {prediction[0]}
 - {labels[1]} = {prediction[1]}
 - {labels[2]} = {prediction[2]}
 - {labels[3]} = {prediction[3]}
 - {labels[4]} = {prediction[4]}
    """)

    predicted_label = labels[max_index[0]]

    print(f"PREDICTION RESULT: {predicted_label}\n")
    return predicted_label

def get_nutrition_value(fruit):
    response = get(url, headers=headers, params={"query": fruit})
    data = response.json()
    items = data.get('items', [])
    item = items[0] if len(items) > 0 else None

    print(f"\nRESPONSE: {item}\n")
    return item

@app.route('/')
def home_route():
    return render_template('index.html')

@app.route('/api/predict', methods=["POST"])
def predict_route():
    if request.method != "POST":
        return render_template('index.html')

    file = request.files["file"]
    file_path = save_image(file)
    prediction = predict(file_path)

    nutrition = get_nutrition_value(prediction)

    return {"label": prediction, 'nutrition': nutrition}