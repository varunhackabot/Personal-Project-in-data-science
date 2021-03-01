# -*- coding: utf-8 -*-
"""Tuberculosis Detection Using Python

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZL9gJSAKV944hQ52NlQ4RF0BCW4PcJx4
"""

from keras.preprocessing.image import ImageDataGenerator

# Commented out IPython magic to ensure Python compatibility.
from keras import backend as K
from keras.preprocessing.image import ImageDataGenerator,load_img, img_to_array
from keras.models import Sequential, Model
from keras.layers import Conv2D, MaxPooling2D,GlobalAveragePooling2D
from keras.layers import Activation, Dropout, BatchNormalization, Flatten, Dense, AvgPool2D,MaxPool2D
from keras.models import Sequential, Model
from keras.applications.vgg16 import VGG16, preprocess_input
from keras.optimizers import Adam, SGD, RMSprop

import tensorflow as tf
import os
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
# %matplotlib inline

from tqdm  import tqdm
from keras import backend as K
from sklearn.metrics     import accuracy_score, roc_auc_score
from keras.layers        import Dense, Dropout, Flatten, BatchNormalization, GlobalMaxPooling2D
from keras.models        import Sequential, Model, load_model
from keras.callbacks     import ModelCheckpoint,ReduceLROnPlateau, CSVLogger
from keras.activations   import elu
from keras.engine        import Layer, InputSpec
from keras.applications  import MobileNetV2
from keras.optimizers    import Adam
from keras.preprocessing import image
from sklearn.linear_model      import LogisticRegression
from sklearn.model_selection   import train_test_split
from keras.preprocessing.image import ImageDataGenerator

!wget  http://openi.nlm.nih.gov/imgs/collections/ChinaSet_AllFiles.zip
!unzip ChinaSet_AllFiles.zip

!wget http://openi.nlm.nih.gov/imgs/collections/NLM-MontgomeryCXRSet.zip
!unzip NLM-MontgomeryCXRSet.zip

AUG_IMAGES_WANTED = 1000 
IMG_HEIGHT = 90
IMG_WIDTH = 90

shen_list = os.listdir('ChinaSet_AllFiles/CXR_png')
mont_list = os.listdir('MontgomerySet/CXR_png')

df_shen = pd.DataFrame(shen_list, columns=['image_id'])
df_mont = pd.DataFrame(mont_list, columns=['image_id'])

df_shen = df_shen[df_shen['image_id'] != 'Thumbs.db']
df_mont = df_mont[df_mont['image_id'] != 'Thumbs.db']

df_shen.reset_index(inplace=True, drop=True)
df_mont.reset_index(inplace=True, drop=True)

print(df_shen.shape)
print(df_mont.shape)

def target_point(x):
    target = int(x[-5])
    if target == 0:
        return 'Normal'
    if target == 1:
        return 'Tuberculosis'

df_shen['target'] = df_shen['image_id'].apply(target_point)

df_mont['target'] = df_mont['image_id'].apply(target_point)

from sklearn.utils import shuffle
df_mont['target'].value_counts()
df_data = pd.concat([df_shen, df_mont], axis=0).reset_index(drop=True)
df_data = shuffle(df_data)
df_data.shape

df_data['labels'] = df_data['target'].map({'Normal':0, 'Tuberculosis':1})

y = df_data['labels']
df_train, df_val = train_test_split(df_data, test_size=0.15, random_state=101, stratify=y)
print(df_train.shape)
print(df_val.shape)
df_train['target'].value_counts()
df_val['target'].value_counts()

base_dir = 'base_dir2'
os.mkdir(base_dir)

train_dir = os.path.join(base_dir, 'train_dir')
os.mkdir(train_dir)
val_dir = os.path.join(base_dir, 'val_dir')
os.mkdir(val_dir)
normal = os.path.join(train_dir, 'Normal')
os.mkdir(normal)
Tb = os.path.join(train_dir, 'Tuberculosis')
os.mkdir(Tb)
normal = os.path.join(val_dir, 'Normal')
os.mkdir(normal)
Tb = os.path.join(val_dir, 'Tuberculosis')
os.mkdir(Tb)

# Commented out IPython magic to ensure Python compatibility.

from numpy.random import seed
seed(101)


import pandas as pd
import numpy as np

import tensorflow

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Conv2D, MaxPooling2D, Flatten
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.metrics import categorical_crossentropy
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Model
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint
from tensorflow.keras.metrics import binary_accuracy

import os
import cv2

import imageio
import skimage
import skimage.io
import skimage.transform

from sklearn.utils import shuffle
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
import itertools
import shutil
import matplotlib.pyplot as plt
# %matplotlib inline

file_name = list(train_dir)
def read_image_sizes(file_name):
    image = skimage.io.imread(IMAGE_PATH + file_name)
    return list(image.shape)

df_data.set_index('image_id', inplace=True)

f_1 = os.listdir('ChinaSet_AllFiles/CXR_png')
f_2 = os.listdir('MontgomerySet/CXR_png')
train_list = list(df_train['image_id'])
val_list = list(df_val['image_id'])
for x in train_list:
    fname = x
    label = df_data.loc[x,'target']
    if fname in f_1:
        src = os.path.join('ChinaSet_AllFiles/CXR_png', fname)
        dst = os.path.join(train_dir, label, fname)        
        x = cv2.imread(src)
        x = cv2.resize(x, (IMAGE_HEIGHT, IMAGE_WIDTH))
        cv2.imwrite(dst, x)
    if fname in f_2:
        src = os.path.join('MontgomerySet/CXR_png', fname)
        dst = os.path.join(train_dir, label, fname)
        x = cv2.imread(src)
        x = cv2.resize(x, (IMAGE_HEIGHT, IMAGE_WIDTH))
        cv2.imwrite(dst, x)
for x in val_list:
    fname = x
    label = df_data.loc[x,'target']
    if fname in f_1:
        src = os.path.join('ChinaSet_AllFiles/CXR_png', fname)
        dst = os.path.join(val_dir, label, fname)
        x = cv2.imread(src)
        x = cv2.resize(x, (IMAGE_HEIGHT, IMAGE_WIDTH))
        cv2.imwrite(dst, x)
    if fname in f_2:
        src = os.path.join('MontgomerySet/CXR_png', fname)
        dst = os.path.join(val_dir, label, fname)
        x = cv2.imread(src)
        x = cv2.resize(x, (IMAGE_HEIGHT, IMAGE_WIDTH))
        cv2.imwrite(dst, x)

print(len(os.listdir('base_dir2/train_dir/Normal')))
print(len(os.listdir('base_dir2/train_dir/Tuberculosis')))

print(len(os.listdir('base_dir2/val_dir/Normal')))
print(len(os.listdir('base_dir2/val_dir/Tuberculosis')))

c_list = ['Normal','Tuberculosis']
for item in c_list:
    aug_dir = 'aug_dir2'
    os.mkdir(aug_dir)
    img_dir = os.path.join(aug_dir, 'img_dir')
    os.mkdir(img_dir)
    img_class = item
    img_list = os.listdir('base_dir2/train_dir/' + img_class)
    for fname in img_list:
            src = os.path.join('base_dir2/train_dir/' + img_class, fname)
            dst = os.path.join(img_dir, fname)
            shutil.copyfile(src, dst)
    path = aug_dir
    save_path = 'base_dir2/train_dir/' + img_class
    datagen = ImageDataGenerator(
        rotation_range=10,
        width_shift_range=0.1,
        height_shift_range=0.1,
        zoom_range=0.1,
        horizontal_flip=True,
        fill_mode='nearest')
    batch_size = 50
    aug_datagen = datagen.flow_from_directory(path,
                                           save_to_dir=save_path,
                                           save_format='png',
                                                    target_size=(IMAGE_HEIGHT,IMAGE_WIDTH),
                                                    batch_size=batch_size)
    num_files = len(os.listdir(img_dir))
    num_batches = int(np.ceil((NUM_AUG_IMAGES_WANTED-num_files)/batch_size))
    for i in range(0,num_batches):
        imgs, labels = next(aug_datagen)
    shutil.rmtree('aug_dir2')

print(len(os.listdir('base_dir2/train_dir/Normal')))
print(len(os.listdir('base_dir2/train_dir/Tuberculosis')))

train_path = 'base_dir2/train_dir'
valid_path = 'base_dir2/val_dir'
num_train_samples = len(df_train)
num_val_samples = len(df_val)
train_batch_size = 10
val_batch_size = 10
train_steps = np.ceil(num_train_samples / train_batch_size)
val_steps = np.ceil(num_val_samples / val_batch_size)
datagen = ImageDataGenerator(rescale=1.0/255)
train_gen = datagen.flow_from_directory(train_path,
                                        target_size=(IMAGE_HEIGHT,IMAGE_WIDTH),
                                        batch_size=train_batch_size,
                                        class_mode='categorical')
val_gen = datagen.flow_from_directory(valid_path,
                                        target_size=(IMAGE_HEIGHT,IMAGE_WIDTH),
                                        batch_size=val_batch_size,
                                        class_mode='categorical')
test_gen = datagen.flow_from_directory(valid_path,
                                        target_size=(IMAGE_HEIGHT,IMAGE_WIDTH),
                                        batch_size=val_batch_size,
                                        class_mode='categorical',
                                        shuffle=False)

kernel_size = (3,3)
pool_size= (2,2)
first_filters = 32
second_filters = 64
third_filters = 128
dropout_conv = 0.3
dropout_dense = 0.3
model = Sequential()
model.add(Conv2D(first_filters, kernel_size, activation = 'relu', 
                 input_shape = (IMAGE_HEIGHT, IMAGE_WIDTH, 3)))
model.add(Conv2D(first_filters, kernel_size, activation = 'relu'))
model.add(Conv2D(first_filters, kernel_size, activation = 'relu'))
model.add(MaxPooling2D(pool_size = pool_size)) 
model.add(Dropout(dropout_conv))
model.add(Conv2D(second_filters, kernel_size, activation ='relu'))
model.add(Conv2D(second_filters, kernel_size, activation ='relu'))
model.add(Conv2D(second_filters, kernel_size, activation ='relu'))
model.add(MaxPooling2D(pool_size = pool_size))
model.add(Dropout(dropout_conv))
model.add(Conv2D(third_filters, kernel_size, activation ='relu'))
model.add(Conv2D(third_filters, kernel_size, activation ='relu'))
model.add(Conv2D(third_filters, kernel_size, activation ='relu'))
model.add(MaxPooling2D(pool_size = pool_size))
model.add(Dropout(dropout_conv))
model.add(Flatten())
model.add(Dense(256, activation = "relu"))
model.add(Dropout(dropout_dense))
model.add(Dense(2, activation = "softmax"))
model.summary()

model.compile(Adam(lr=0.0001), loss='binary_crossentropy', 
              metrics=['accuracy'])

filepath = "model.h5"
checkpoint = ModelCheckpoint(filepath, monitor='val_acc', verbose=1, 
                             save_best_only=True, mode='max')

reduce_lr = ReduceLROnPlateau(monitor='val_acc', factor=0.5, patience=2, 
                                   verbose=1, mode='max', min_lr=0.00001)
                              
                              
callbacks_list = [checkpoint, reduce_lr]

history = model.fit_generator(train_gen, steps_per_epoch=train_steps, 
                            validation_data=val_gen,
                            validation_steps=val_steps,
                            epochs=100, verbose=1,
                           callbacks=callbacks_list)

model.metrics_names

val_loss, val_acc = \
model.evaluate_generator(test_gen, 
                        steps=val_steps)

print('val_loss:', val_loss)
print('val_acc:', val_acc)

