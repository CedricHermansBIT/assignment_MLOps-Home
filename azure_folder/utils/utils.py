import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Activation
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.layers import Input, Dense, Dropout

import numpy as np
import pandas as pd
import os

from typing import List



BATCH_SIZE = 32
MAX_EPOCHS = 100
PATIENCE = 11
INITIAL_LEARNING_RATE = 0.01
DROPOUTRATE = 0.0
ACTIVATION_HIDDEN = 'relu' # activatiefunctie van de hidden layer neuronen
ACTIVATION_OUTPUT = 'sigmoid'# activatie van de output layer neuronen
INITIALIZER = 'RandomUniform' # type van kernel intializer
model_name = 'gene-cnn-test'



def buildModel(inputShape: int, classes: int) -> Sequential:
    model = Sequential()
    model.add(Dense(20, input_dim=inputShape, kernel_initializer=INITIALIZER,activation=ACTIVATION_HIDDEN))
    model.add(Dropout(DROPOUTRATE))
    model.add(Dense(20, kernel_initializer=INITIALIZER,activation=ACTIVATION_HIDDEN))
    model.add(Dropout(DROPOUTRATE))
    model.add(Dense(20, kernel_initializer=INITIALIZER,activation=ACTIVATION_HIDDEN))
    model.add(Dropout(DROPOUTRATE))
    model.add(Dense(20, kernel_initializer=INITIALIZER,activation=ACTIVATION_HIDDEN))
    model.add(Dropout(DROPOUTRATE))
    model.add(Dense(classes, kernel_initializer=INITIALIZER,activation=ACTIVATION_OUTPUT))


    # return the constructed network architecture
    return model

# model = buildModel((64, 64, 3), len(LABELS))