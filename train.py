import tensorflow as tf
from keras import layers, models
import matplotlib.pyplot as plt

# 1. Define Image Parameters
img_height = 100
img_width = 100
batch_size = 32
epochs = 10 # 10 is usually plenty to hit 95%+ on this dataset

# 2. Load the Datasets using tf.keras
train_ds = tf.keras.preprocessing.image_dataset_from_directory(
  'custom_dataset/Training',
  seed=123,
  image_size=(img_height, img_width),
  batch_size=batch_size
)

val_ds = tf.keras.preprocessing.image_dataset_from_directory(
  'custom_dataset/Test',
  seed=123,
  image_size=(img_height, img_width),
  batch_size=batch_size
)

class_names = train_ds.class_names
print(f"Classes being trained: {class_names}")

# 3. Optimize datasets for performance
AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

# 4. Build the CNN Model
num_classes = len(class_names)

model = models.Sequential([
    # Rescaling pixel values from 0-255 to 0-1
    layers.Rescaling(1./255, input_shape=(img_height, img_width, 3)),
    
    layers.Conv2D(16, 3, padding='same', activation='relu'),
    layers.MaxPooling2D(),
    
    layers.Conv2D(32, 3, padding='same', activation='relu'),
    layers.MaxPooling2D(),
    
    layers.Conv2D(64, 3, padding='same', activation='relu'),
    layers.MaxPooling2D(),
    
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    # Softmax ensures the model outputs exactly ONE class prediction
    layers.Dense(num_classes, activation='softmax') 
])

# 5. Compile the Model
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.summary()

# 6. Train the Model
history = model.fit(
  train_ds,
  validation_data=val_ds,
  epochs=epochs
)

# 7. Save the model for later use
model.save('fruit_classifier_model.keras')
print("Model trained and saved successfully!")