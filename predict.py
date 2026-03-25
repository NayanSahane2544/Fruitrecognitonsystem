import tensorflow as tf
import numpy as np
from keras.preprocessing import image
import os

# 1. Define your classes in ALPHABETICAL order
# TensorFlow's image_dataset_from_directory sorts folders alphabetically by default
class_names = ['Almond','Ananas','Apple','Banana','Grape','Guava', 'Mango','Orange','Pomegranate','Strawberry','Walnut','Watermelon']

# 2. Load the trained model
print("Loading model...")
model = tf.keras.models.load_model('fruit_classifier_model.keras')
print("Model loaded successfully!\n")

def predict_fruit(img_path):
    if not os.path.exists(img_path):
        print(f"Error: Could not find image at {img_path}")
        return

    # 3. Load and preprocess the image
    # Target size MUST match the exact size used during training (100x100)
    img = image.load_img(img_path, target_size=(100, 100))
    
    # Convert the image to a mathematical array of pixels
    img_array = image.img_to_array(img)
    
    # Add a "batch" dimension. 
    # Even though we are predicting one image, the model expects a batch (e.g., [1, 100, 100, 3])
    img_array = np.expand_dims(img_array, axis=0)

    # 4. Make the prediction
    # This outputs an array of probabilities, e.g., [[0.02, 0.95, 0.03]]
    predictions = model.predict(img_array, verbose=0)
    
    # 5. Interpret the results
    # np.argmax finds the index of the highest probability
    predicted_index = np.argmax(predictions[0]) 
    confidence = np.max(predictions[0]) * 100
    predicted_class = class_names[predicted_index]

    print("-" * 30)
    print(f"Image: {os.path.basename(img_path)}")
    print(f"Prediction: {predicted_class}")
    print(f"Confidence: {confidence:.2f}%")
    print("-" * 30)

# --- Test it out! ---
# Provide the path to a test image here
test_image_path = r"F:\Fruits\fruits-360_100x100\fruits-360\Training\Pomegranate 1\19_100.jpg"

predict_fruit(test_image_path)