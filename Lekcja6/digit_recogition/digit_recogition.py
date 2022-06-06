import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import os

class_names = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

train_new_model = True

if os.path.exists("handwritten.model"):
    train_new_model = False

print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))

def dataset_gathering():
    global mnist, x_train, y_train, x_test, y_test
    # pobranie datasetów
    mnist = tf.keras.datasets.mnist
    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    # normalizacja do 1
    x_train = tf.keras.utils.normalize(x_train, axis=1)
    x_test = tf.keras.utils.normalize(x_test, axis=1)


if train_new_model:
    # pobranie datasetów
    dataset_gathering()

    #tworzenie nowej sieci neuronowej
    model = tf.keras.models.Sequential([
        tf.keras.layers.Flatten(input_shape=(28, 28)),
        tf.keras.layers.Dense(256, activation=tf.nn.relu),
        tf.keras.layers.Dense(256, activation=tf.nn.relu),
        tf.keras.layers.Dense(10, activation=tf.nn.softmax)
    ])

    #kompilacja modelu
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    model.fit(x_train, y_train, epochs=40)
    test_loss, test_acc = model.evaluate(x_test, y_test)
    print(f"Dokładność: {test_acc}")

    #zapisanie modelu
    model.save('handwritten.model')
else:
    model = tf.keras.models.load_model('handwritten.model')
    dataset_gathering()

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
