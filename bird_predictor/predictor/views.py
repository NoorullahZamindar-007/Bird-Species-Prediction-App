from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import tensorflow as tf
import numpy as np
from PIL import Image
import os

# Load model
model = tf.keras.models.load_model('bird_species.h5')

# Replace these with your real class labels
class_names = [
    'AMERICAN GOLDFINCH',
    'BARN OWL',
    'CARMINE BEE-EATER',
    'DOWNY WOODPECKER',
    'EMPEROR PENGUIN',
    'FLAMINGO'
]



def preprocess_image(image_path):
    img = Image.open(image_path).convert("RGB")
    img = img.resize((224, 224))
    img_array = np.array(img) / 255.0
    return np.expand_dims(img_array, axis=0)
    


def index(request):
    prediction = None
    image_url = None

    if request.method == 'POST' and request.FILES.get('bird_image'):
        image_file = request.FILES['bird_image']
        fs = FileSystemStorage()
        filename = fs.save(image_file.name, image_file)
        image_url = fs.url(filename)
        image_path = os.path.join(fs.location, filename)

        image = preprocess_image(image_path)
        pred = model.predict(image)
        prediction = class_names[np.argmax(pred)]

    return render(request, 'predictor/index.html', {
        'prediction': prediction,
        'image_url': image_url
    })
