import cv2 as cv
# Tensorflow
import tensorflow as tf
# Biblioteki pomocniczne
import numpy as np
import matplotlib.pyplot as plt
import os

class_names = np.arange(10)

mnist = tf.keras.datasets.mnist
(train_images, train_labels), (test_images, test_labels) = mnist.load_data()

# normalizacja do 1
train_images = tf.keras.utils.normalize(train_images, axis=1)
test_images = tf.keras.utils.normalize(test_images, axis=1)

# tworzenie nowej sieci neuronowej
model = tf.keras.models.Sequential([
    tf.keras.layers.Flatten(input_shape=(28, 28)),
    tf.keras.layers.Dense(64, activation='tanh'),
    tf.keras.layers.Dense(128, activation='sigmoid'),
    tf.keras.layers.Dense(len(class_names), activation=tf.nn.softmax)
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
model.summary()
model.fit(train_images, train_labels, epochs=40)
test_loss, test_acc = model.evaluate(test_images, test_labels)
print(f"Dokładność: {test_acc}")

modelOutputPath = 'trained_model'
model.save(modelOutputPath, save_format='tf')

predictions = []
img_array = []

image_number = 1
while os.path.isfile(f'digits/digit{format(image_number)}.png'):
    try:
        img = cv.imread(f'digits/digit{format(image_number)}.png')[:, :, 0]
        img = np.invert(np.array([img]))
        prediction = model.predict(img)
        predictions.append(prediction)
        img_array.append(img)
        print(f"The number is probably a {format(np.argmax(prediction))}")
        #plt.imshow(img[0], cmap=plt.cm.binary)
        #plt.show()
        image_number += 1
    except:
        print("Error reading image! Proceeding with next image...")
        image_number += 1

num_rows = 5
num_cols = 4
plt.figure(figsize=(2*2*num_cols, 2*num_rows))

for i in range(len(predictions)):
    plt.subplot(num_rows, 2*num_cols, 2*i+1)
    plt.imshow((img_array[i])[0], cmap=plt.cm.binary)
    plt.colorbar()
    predicted_label = np.argmax(predictions[i])
    plt.xlabel(f"Najprawdopodobniej jest to {predicted_label}")
plt.show()
plt.savefig("exported.png")
