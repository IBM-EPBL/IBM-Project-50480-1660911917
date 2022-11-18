from flask import Flask, render_template, request
from keras.models import load_model
from keras.preprocessing import image
import numpy as np
from os import path

app = Flask(__name__)
model = load_model('./model.h5')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/predict', methods=["POST"])
def predict():
    if request.method != "POST":
        return render_template('index.html')

    # getting the image and saving it locally
    file = request.files["file"]
    filename = file.filename
    root_path = path.dirname(__file__)
    file_path = path.join(root_path, 'uploads', filename)
    file.save(file_path)

    # preprocessing the image
    file = image.image_utils.load_img(file_path, target_size=(64,64))
    x = image.image_utils.img_to_array(file)
    x = np.expand_dims(x, axis=0)

    # classifying the image
    prediction = np.argmax(model.predict(x), axis=1)
    index = ["Apple", 'Banana', 'Orange', 'Pineapple', 'Watermelon']

    prediction_label = index[prediction[0]]

    print(f"""
        FILENAME: {filename}
        PREDICTIONS: {list(map(lambda x: f"{index[x]} = {x}", prediction))}
        OUTPUT: {prediction_label}
    """)
    return {"label": prediction_label}