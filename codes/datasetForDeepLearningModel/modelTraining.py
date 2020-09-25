import tensorflow as tf
import numpy as np
from tensorflow.keras import layers
from tensorflow.keras.layers import Dropout
import sys

def main(machineNum):

	X = np.load(f"trainDataForMachine_{machineNum}_trainX.npy");
	Y = np.load(f"trainDataForMachine_{machineNum}_trainY.npy");

	trainX = X[:3000];
	trainY = Y[:3000];
	testX = X[3000:];
	testY = Y[3000:];

	model = tf.keras.Sequential();
	model.add(layers.Dense(408, activation='relu', input_dim=41, kernel_initializer='he_normal'));
	model.add(Dropout(0.1));
	model.add(layers.Dense(408, activation='relu', kernel_initializer='he_normal'));
	model.add(Dropout(0.1));
	model.add(layers.Dense(408, activation='relu', kernel_initializer='he_normal'));
	model.add(Dropout(0.1));
	model.add(layers.Dense(408, activation='relu', kernel_initializer='he_normal'));
	model.add(Dropout(0.1));
	model.add(layers.Dense(408, activation='relu', kernel_initializer='he_normal'));
	model.add(Dropout(0.1));
	model.add(layers.Dense(408, activation='relu', kernel_initializer='he_normal'));
	model.add(Dropout(0.1));
	model.add(layers.Dense(1));

	model.compile(optimizer='adam',loss='mean_squared_error',metrics=['mse']);

	hist = model.fit(trainX, trainY, batch_size=300, epochs=20, validation_data=(testX, testY));

	np.save(f"machine_{machineNum}_loss.npy",hist.history['loss']);
	np.save(f"machine_{machineNum}_validationLoss.npy", hist.history['val_loss']);

	model.save(f"machine_{machineNum}_Weights.h5");

if __name__ == '__main__':
	main(int(sys.argv[1]));