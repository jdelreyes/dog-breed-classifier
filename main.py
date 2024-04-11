# -*- coding: utf-8 -*-
"""main.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1MGl5fr4RBDjmeFaCDfmft8cDEFSM-n-h
"""

import os, shutil

import keras
from keras.constraints import max_norm

import matplotlib.pyplot as plt
import tensorflow as tf

# google colab
# from google.colab import drive
# drive.mount('/content/drive')

# original_data_dir = '/content/drive/MyDrive/Colab Notebooks/dog-breed-classifier/dog-breeds'
# base_dir = '/content/drive/MyDrive/Colab Notebooks/dog-breed-classifier/load-data'

# local
original_data_dir = './dog-breeds'
base_dir = './load-data'

train_dir = os.path.join(base_dir, 'train')
validation_dir = os.path.join(base_dir, 'validation')
test_dir = os.path.join(base_dir, 'test')

os.mkdir(base_dir)
os.mkdir(train_dir)
os.mkdir(validation_dir)
os.mkdir(test_dir)

dog_breed_dir_list = os.listdir(original_data_dir)
dog_breeds = {}

for dog_breed_dir in dog_breed_dir_list:
    DIR = os.path.join(original_data_dir, dog_breed_dir)

    size = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
    dog_breeds[dog_breed_dir] = {'size': size}

for dog_breed in dog_breeds:
    TEN_PERCENT = round(dog_breeds[dog_breed]['size'] * 0.1)
    EIGHTY_PERCENT = round(dog_breeds[dog_breed]['size'] * 0.8)

    validation_size = TEN_PERCENT
    test_size = TEN_PERCENT + TEN_PERCENT
    training_size = TEN_PERCENT + TEN_PERCENT + EIGHTY_PERCENT

    dog_breed_validation_dir = os.path.join(validation_dir, dog_breed)
    dog_breed_test_dir = os.path.join(test_dir, dog_breed)
    dog_breed_train_dir = os.path.join(train_dir, dog_breed)

    os.mkdir(dog_breed_validation_dir)
    os.mkdir(dog_breed_test_dir)
    os.mkdir(dog_breed_train_dir)

    for x in ['{}.jpg'.format(i) for i in range(1, validation_size)]:
        src = os.path.join(original_data_dir, dog_breed, x)
        dst = os.path.join(dog_breed_validation_dir, x)
        shutil.copyfile(src, dst)

    for x in ['{}.jpg'.format(i) for i in range(validation_size, test_size)]:
        src = os.path.join(original_data_dir, dog_breed, x)
        dst = os.path.join(dog_breed_test_dir, x)
        shutil.copyfile(src, dst)

    for x in ['{}.jpg'.format(i) for i in range(test_size, training_size)]:
        src = os.path.join(original_data_dir, dog_breed, x)
        dst = os.path.join(dog_breed_train_dir, x)
        shutil.copyfile(src, dst)

model = keras.Sequential([
    keras.layers.Conv2D(32, (3, 3), padding='same', activation='relu', kernel_constraint=max_norm(3),
                        input_shape=(150, 150, 3)),
    keras.layers.MaxPooling2D((2, 2)),
    keras.layers.Conv2D(64, (3, 3), padding='same', activation='relu', kernel_constraint=max_norm(3)),
    keras.layers.MaxPooling2D((2, 2)),
    keras.layers.Conv2D(128, (3, 3), padding='same', activation='relu', kernel_constraint=max_norm(3)),
    keras.layers.MaxPooling2D((2, 2)),
    keras.layers.Conv2D(256, (3, 3), padding='same', activation='relu', kernel_constraint=max_norm(3)),
    keras.layers.MaxPooling2D((2, 2)),
    keras.layers.Flatten(),
    keras.layers.Dense(512, activation='relu'),
    keras.layers.Dropout(0.5),
    keras.layers.Dense(256, activation='relu'),
    keras.layers.Dropout(0.5),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(17, activation='softmax')
])

model.compile(optimizer="adam", loss='categorical_crossentropy', metrics=['accuracy'])

model.summary()

train_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
    rescale=1./255,
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

test_datagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(150, 150),
    batch_size=256,
    class_mode='categorical'
)

validation_generator = test_datagen.flow_from_directory(
    validation_dir,
    target_size=(150, 150),
    batch_size=256,
    class_mode='categorical'
)

test_generator = test_datagen.flow_from_directory(
    test_dir,
    target_size=(150, 150),
    batch_size=256,
    class_mode='categorical'
)

history = model.fit(
    train_generator,
    steps_per_epoch=256,
    epochs=50,
    validation_data=validation_generator,
    validation_steps=256,
    verbose=1
)

test_loss, test_accuracy = model.evaluate(test_generator)

test_accuracy

# Define a function to plot the results
def result_plotting():
    plt.figure(figsize=[8, 6])
    plt.plot(history.history['accuracy'], 'blue', linewidth=3.0)
    plt.plot(history.history['val_accuracy'], 'red', ls='--', linewidth=3.0)
    plt.legend(['Training Accuracy', 'Validation Accuracy'], fontsize=18, loc='lower right')
    plt.xlabel('Epochs', fontsize=16)
    plt.ylabel('Accuracy', fontsize=16)
    plt.title('Accuracy Curves', fontsize=16)

result_plotting()

