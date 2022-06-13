import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import os

class_names = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

train_new_model = True

if os.path.exists("handwritten.model"):
    train_new_model = False


def dataset_gathering():
    global mnist, train_images, train_labels, test_images, test_labels
    # pobranie datasetow
    mnist = tf.keras.datasets.mnist
    (train_images, train_labels), (test_images, test_labels) = mnist.load_data()
    train_images = tf.keras.utils.normalize(train_images, axis=1)
    test_images = tf.keras.utils.normalize(test_images, axis=1)


if train_new_model:
    # pobranie datasetów
    dataset_gathering()

    # tworzenie nowej sieci neuronowej
    model = tf.keras.models.Sequential([
        tf.keras.layers.Flatten(input_shape=(28, 28)),
        tf.keras.layers.Dense(1024, activation=tf.nn.relu),
        tf.keras.layers.Dense(1024, activation=tf.nn.relu),
        tf.keras.layers.Dense(1024, activation=tf.nn.relu),
        tf.keras.layers.Dense(1024, activation=tf.nn.relu),
        tf.keras.layers.Dense(10, activation=tf.nn.softmax),
    ])

    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy']
                  )
    model.fit(train_images, train_labels, epochs=20)
    test_loss, test_acc = model.evaluate(test_images, test_labels)
    print(f"Dokładność: {test_acc}")

    # zapisywanie modelu
    model.save("handwritten.model")
else:
    model = tf.keras.models.load_model("handwritten.model")
    dataset_gathering()

predictions = []
img_array = []

image_number = 1
while os.path.isfile(f"digits/digit{format(image_number)}.png"):
    try:
        img = cv.imread(f"digits/digit{format(image_number)}.png")[:, :, 0]
        nazwa_pliku = "digit" + str(image_number) + ".png"
        img = np.invert(np.array([img]))
        prediction = model.predict(img)
        predictions.append(prediction)
        img_array.append(img)
        print(f"Wykryta cyfra w pliku {nazwa_pliku} to prawdopodobnie: {format(np.argmax(prediction))}")
        image_number += 1
    except:
        print("Błąd podczas ładowania obrazu. Przechodzę do kolejnego przypadku...")
        image_number += 1

num_rows = 5
num_columns = 4
plt.figure(figsize=(4*num_columns, 2*num_rows))

for i in range(len(predictions)):
    plt.subplot(num_rows, 2*num_columns, 2*i + 1)
    plt.imshow((img_array[i])[0], cmap=plt.cm.binary)
    plt.colorbar()
    predicted_label = np.argmax(predictions[i])
    plt.xlabel(f"Najprawdopodobniej jest to {predicted_label}")
plt.show()