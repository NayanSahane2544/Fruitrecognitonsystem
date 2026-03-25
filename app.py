import tensorflow as tf
import numpy as np
import cv2
import json
import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
# Allow React to communicate with Flask
CORS(app) 

# LOAD MODEL
model = tf.keras.models.load_model("fruit_classifier_model.keras")

# LOAD CLASS NAMES
with open("class_names.json") as f:
    class_names = json.load(f)

# 1. EXPANDED DESCRIPTIONS
descriptions = {
    "Almond": "Almonds are highly nutritious tree nuts native to the Middle East and South Asia. They are packed with healthy fats, antioxidants, vitamins, and minerals. Regular consumption is linked to lower blood sugar levels, reduced blood pressure, and lower cholesterol levels.",
    "Ananas": "Pineapples are tropical fruits known for their vibrant sweet and tart flavor. They are exceptionally rich in vitamin C and manganese, and they contain bromelain, a unique digestive enzyme that helps break down proteins and reduce inflammation.",
    "Apple": "Apples are one of the most popular and widely cultivated fruits globally. They are an excellent source of dietary fiber, particularly pectin, and are rich in antioxidants like quercetin, which promote heart health and regulate blood sugar.",
    "Banana": "Bananas are elongated, edible fruits packed with potassium, vitamin B6, and carbohydrates. They are an excellent source of quick, natural energy, making them a staple in athletic diets and vital for maintaining healthy blood pressure.",
    "Grapes": "Grapes are botanic berries that grow on woody vines. They are packed with water and powerful antioxidants, including resveratrol, which is widely studied for its anti-aging properties and benefits to cardiovascular health.",
    "Guava": "Guava is a tropical fruit characterized by its green skin and pink or white fleshy interior. It is an absolute powerhouse of Vitamin C—containing four times more than an orange—and is highly beneficial for immune system support and digestion.",
    "Mango": "Often hailed as the 'King of Fruits', mangoes are luscious stone fruits with a rich, sweet flavor profile. They are incredibly high in Vitamin A, folate, and digestive enzymes, promoting eye health and supporting a strong immune system.",
    "Orange": "Oranges are a globally beloved citrus fruit known for their refreshing juice and tangy flavor. They are primarily recognized for their high Vitamin C content, which aids in collagen production, skin health, and iron absorption.",
    "Pomegranate": "Pomegranates are unique fruits containing hundreds of jewel-like, edible seeds called arils. They are categorized as a superfood due to their massive concentration of punicalagins, which are extremely potent antioxidants that fight inflammation.",
    "Strawberry": "Strawberries are bright red, juicy, and sweet aggregate fruits. They are an excellent source of vitamin C, manganese, and various plant compounds that have been linked to improved heart health and blood sugar control.",
    "Walnut": "Walnuts are edible seeds prized for their brain-like shape and exceptional nutritional profile. They are the only nut that contains a significant amount of plant-based Omega-3 fatty acids, which are critical for brain health and reducing inflammation.",
    "Watermelon": "Watermelon is a refreshing, large trailing vine fruit comprising over 92% water. It is an incredible source of hydration and contains high levels of lycopene, an antioxidant linked to decreased risk of chronic diseases."
}

# 2. SCIENTIFIC NAMES
scientific_names = {
    "Almond": "Prunus dulcis", "Ananas": "Ananas comosus", "Apple": "Malus domestica",
    "Banana": "Musa spp.", "Grapes": "Vitis vinifera", "Guava": "Psidium guajava",
    "Mango": "Mangifera indica", "Orange": "Citrus × sinensis", "Pomegranate": "Punica granatum",
    "Strawberry": "Fragaria × ananassa", "Walnut": "Juglans regia", "Watermelon": "Citrullus lanatus"
}

# 3. CALORIES
calories = {
    "Almond": "~579 kcal per 100g", "Ananas": "~50 kcal per 100g", "Apple": "~52 kcal per 100g",
    "Banana": "~89 kcal per 100g", "Grapes": "~69 kcal per 100g", "Guava": "~68 kcal per 100g",
    "Mango": "~60 kcal per 100g", "Orange": "~47 kcal per 100g", "Pomegranate": "~83 kcal per 100g",
    "Strawberry": "~32 kcal per 100g", "Walnut": "~654 kcal per 100g", "Watermelon": "~30 kcal per 100g"
}

# 4. MACRONUTRIENTS FOR PIE CHART
macros = {
    "Almond": [{"name": "Carbs", "value": 15}, {"name": "Protein", "value": 13}, {"name": "Fat", "value": 72}],
    "Ananas": [{"name": "Carbs", "value": 95}, {"name": "Protein", "value": 3}, {"name": "Fat", "value": 2}],
    "Apple": [{"name": "Carbs", "value": 95}, {"name": "Protein", "value": 2}, {"name": "Fat", "value": 3}],
    "Banana": [{"name": "Carbs", "value": 93}, {"name": "Protein", "value": 4}, {"name": "Fat", "value": 3}],
    "Grapes": [{"name": "Carbs", "value": 94}, {"name": "Protein", "value": 4}, {"name": "Fat", "value": 2}],
    "Guava": [{"name": "Carbs", "value": 73}, {"name": "Protein", "value": 12}, {"name": "Fat", "value": 15}],
    "Mango": [{"name": "Carbs", "value": 94}, {"name": "Protein", "value": 4}, {"name": "Fat", "value": 2}],
    "Orange": [{"name": "Carbs", "value": 91}, {"name": "Protein", "value": 7}, {"name": "Fat", "value": 2}],
    "Pomegranate": [{"name": "Carbs", "value": 85}, {"name": "Protein", "value": 10}, {"name": "Fat", "value": 5}],
    "Strawberry": [{"name": "Carbs", "value": 85}, {"name": "Protein", "value": 7}, {"name": "Fat", "value": 8}],
    "Walnut": [{"name": "Carbs", "value": 14}, {"name": "Protein", "value": 15}, {"name": "Fat", "value": 71}],
    "Watermelon": [{"name": "Carbs", "value": 89}, {"name": "Protein", "value": 7}, {"name": "Fat", "value": 4}]
}

# 5. CULTIVATION BY INDIAN STATE FOR BAR CHART
cultivation = {
    "Almond": [{"state": "Jammu & Kashmir", "percent": 85}, {"state": "Himachal Pradesh", "percent": 15}],
    "Ananas": [{"state": "Kerala", "percent": 35}, {"state": "Assam", "percent": 25}, {"state": "Meghalaya", "percent": 15}],
    "Apple": [{"state": "Jammu & Kashmir", "percent": 70}, {"state": "Himachal Pradesh", "percent": 25}, {"state": "Uttarakhand", "percent": 5}],
    "Banana": [{"state": "Tamil Nadu", "percent": 30}, {"state": "Maharashtra", "percent": 25}, {"state": "Gujarat", "percent": 20}],
    "Grapes": [{"state": "Maharashtra", "percent": 70}, {"state": "Karnataka", "percent": 20}, {"state": "Tamil Nadu", "percent": 5}],
    "Guava": [{"state": "Uttar Pradesh", "percent": 45}, {"state": "Bihar", "percent": 15}, {"state": "Maharashtra", "percent": 10}],
    "Mango": [{"state": "Uttar Pradesh", "percent": 23}, {"state": "Andhra Pradesh", "percent": 15}, {"state": "Maharashtra", "percent": 10}],
    "Orange": [{"state": "Maharashtra", "percent": 40}, {"state": "Madhya Pradesh", "percent": 25}, {"state": "Punjab", "percent": 15}],
    "Pomegranate": [{"state": "Maharashtra", "percent": 65}, {"state": "Karnataka", "percent": 15}, {"state": "Gujarat", "percent": 10}],
    "Strawberry": [{"state": "Maharashtra", "percent": 80}, {"state": "Himachal Pradesh", "percent": 10}, {"state": "Uttarakhand", "percent": 5}],
    "Walnut": [{"state": "Jammu & Kashmir", "percent": 90}, {"state": "Uttarakhand", "percent": 5}, {"state": "Himachal Pradesh", "percent": 5}],
    "Watermelon": [{"state": "UP", "percent": 35}, {"state": "Karnataka", "percent": 20}, {"state": "Andhra Pradesh", "percent": 15}]
}

# 6. DISH DATA (Pointing to your LOCAL folder)
dish_data = {
    "Almond": [
        {"name": "Badam Milk", "url": "http://127.0.0.1:5000/static/dishes/badammilk.jpeg"},
        {"name": "Almond Cookies", "url": "http://127.0.0.1:5000/static/dishes/almondcookies.jpeg"},
        {"name": "Marzipan", "url": "http://127.0.0.1:5000/static/dishes/marzipan.jpeg"}
    ],
    "Ananas": [
        {"name": "Pineapple Pastry", "url": "http://127.0.0.1:5000/static/dishes/pineapplepastry.jpeg"},
        {"name": "Pina Colada", "url": "http://127.0.0.1:5000/static/dishes/pinacolada.jpeg"},
        {"name": "Pineapple Rice", "url": "http://127.0.0.1:5000/static/dishes/pineapplerice.jpeg"}
    ],
    "Apple": [
        {"name": "Apple Pie", "url": "http://127.0.0.1:5000/static/dishes/applepie.jpeg"},
        {"name": "Apple Cider", "url": "http://127.0.0.1:5000/static/dishes/applecider.jpeg"},
        {"name": "Apple Halwa", "url": "http://127.0.0.1:5000/static/dishes/applehalwa.jpeg"}
    ],
    "Banana": [
        {"name": "Banana Bread", "url": "http://127.0.0.1:5000/static/dishes/bananabread.jpeg"},
        {"name": "Banana Chips", "url": "http://127.0.0.1:5000/static/dishes/bananachip.jpeg"},
        {"name": "Pancakes", "url": "http://127.0.0.1:5000/static/dishes/bananapancakes.jpeg"}
    ],
    "Grapes": [
        {"name": "Raisins", "url": "http://127.0.0.1:5000/static/dishes/raisins.jpeg"},
        {"name": "Grape Wine", "url": "http://127.0.0.1:5000/static/dishes/grapewine.jpeg"},
        {"name": "Grape Pickle (Marwadi)", "url": "http://127.0.0.1:5000/static/dishes/grapepickle.jpeg"}
    ],
    "Guava": [
        {"name": "Guava Jelly", "url": "http://127.0.0.1:5000/static/dishes/guavajelly.jpeg"},
        {"name": "Guava Chaat", "url": "http://127.0.0.1:5000/static/dishes/guavachaat.jpeg"},
        {"name": "Guava Juice", "url": "http://127.0.0.1:5000/static/dishes/guavajuice.jpeg"}
    ],
    "Mango": [
        {"name": "Aam Ras", "url": "http://127.0.0.1:5000/static/dishes/aamras.jpeg"},
        {"name": "Mango Lassi", "url": "http://127.0.0.1:5000/static/dishes/mangolassi.jpeg"},
        {"name": "Sticky Rice", "url": "http://127.0.0.1:5000/static/dishes/stickyrice.jpeg"}
    ],
    "Orange": [
        {"name": "Orange Juice", "url": "http://127.0.0.1:5000/static/dishes/orangejuice.jpeg"},
        {"name": "Marmalade", "url": "http://127.0.0.1:5000/static/dishes/marmalade.jpeg"},
        {"name": "Orange Chicken", "url": "http://127.0.0.1:5000/static/dishes/orangechicken.jpeg"}
    ],
    "Pomegranate": [
        {"name": "Pomegranate Raita", "url": "http://127.0.0.1:5000/static/dishes/pomegranateraita.jpeg"},
        {"name": "Pomegranate Salad ", "url": "http://127.0.0.1:5000/static/dishes/pomegranatesalad.jpeg"},
        {"name": "Molasses", "url": "http://127.0.0.1:5000/static/dishes/molasses.jpeg"}
    ],
    "Strawberry": [
        {"name": "Shortcake", "url": "http://127.0.0.1:5000/static/dishes/shortcake.jpeg"},
        {"name": "Strawberry Jam", "url": "http://127.0.0.1:5000/static/dishes/strawberryjam.jpeg"},
        {"name": "Smoothie", "url": "http://127.0.0.1:5000/static/dishes/smoothie.jpeg"}
    ],
    "Walnut": [
        {"name": "Walnut Barfi", "url": "http://127.0.0.1:5000/static/dishes/walnutbarfi.jpeg"},
        {"name": "Walnut Ladoo", "url": "http://127.0.0.1:5000/static/dishes/walnutladoo.jpeg"},
        {"name": "Walnut Chikki", "url": "http://127.0.0.1:5000/static/dishes/walnutchikki.jpeg"}
    ],
    "Watermelon": [
        {"name": "Watermelon Juice", "url": "http://127.0.0.1:5000/static/dishes/watermelonjuice.jpeg"},
        {"name": "Watermelon Rice", "url": "http://127.0.0.1:5000/static/dishes/watermelonrice.jpeg"},
        {"name": "Sorbet", "url": "http://127.0.0.1:5000/static/dishes/sorbet.jpeg"}
    ]
}

@app.route("/predict", methods=["POST"])
def predict():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files["image"]
    os.makedirs("static/uploads", exist_ok=True)
    filepath = os.path.join("static/uploads", file.filename)
    file.save(filepath)

    # PREPROCESS
    img = cv2.imread(filepath)
    if img is None:
        return jsonify({"error": "Error loading image."}), 400

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (100, 100))
    img = np.expand_dims(img, axis=0)

    # PREDICT
    pred = model.predict(img)[0]
    class_id = np.argmax(pred)
    fruit = class_names[class_id]

    # SEND EVERYTHING TO REACT
    return jsonify({
        "success": True,
        "fruit": fruit,
        "scientific_name": scientific_names.get(fruit, "Unknown species"),
        "confidence": float(pred[class_id] * 100),
        "description": descriptions.get(fruit, "A delicious fruit."),
        "calories": calories.get(fruit, "Data not found."),
        "macros": macros.get(fruit, []),
        "cultivation": cultivation.get(fruit, []),
        "dish_images": dish_data.get(fruit, [])
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)