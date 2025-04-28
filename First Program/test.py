

import  matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense,Dropout
from tensorflow.keras.optimizers import Adam
house=fetch_california_housing()
x=pd.DataFrame(house.data,columns=house.feature_names)
y=house.target
scaler=StandardScaler()
scaled_x=scaler.fit_transform(x)
x_train,x_test,y_train,y_test=train_test_split(scaled_x,y,test_size=0.2,random_state=42)
model=Sequential([
    Dense(64,activation='relu',input_shape=(x_train.shape[1],)),
    Dropout(0.2),
    Dense(32,activation='relu'),
    Dropout(0.2),
    Dense(16,activation='relu'),
    Dense(1)
])
model.compile(optimizer=Adam(),loss='mean_squared_error')
his=model.fit(x_train,y_train,epochs=200,validation_data=(x_test,y_test),verbose=0)
testing_loss,acc=model.evaluate(x_test,y_test,verbose=0)
print(f'Test mean squared error: {round(testing_loss,4)}')
print(f'Accuracy on test set: {round(acc,4)}')
model.summary()
plt.plot(his.history['loss'],label='Train Loss')
plt.plot(his.history['val_loss'],label='Test Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.grid(True)
plt.show()