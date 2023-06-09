import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense,Conv2D,MaxPooling2D,Flatten
from keras.callbacks import ModelCheckpoint
from sklearn.model_selection import train_test_split
import numpy as np
import os

dir_path = os.path.abspath('data')

# Load the extracted facial features and labels from the previous program
# Load X and y from the saved numpy arrays
X = np.load(os.path.join(dir_path, 'X.npy'), allow_pickle=True)
y = np.load(os.path.join(dir_path, 'y.npy'), allow_pickle=True)
X = X.reshape(X.shape[0], 128)
# Split the data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=True)

# Check for and convert any list elements in X_train and y_train
for i in range(len(X_train)):
    if type(X_train[i]) == list:
        try:
            X_train[i] = np.array(X_train[i]).astype('float32')
        except Exception as e:
            print(f"Error converting X_train element {i} to numpy array: {e}")

for i in range(len(y_train)):
    if type(y_train[i]) == list:
        try:
            y_train[i] = np.array(y_train[i]).astype('float32')
        except Exception as e:
            print(f"Error converting y_train element {i} to numpy array: {e}")

# Print shape and data type of X_train and y_train
print("X_train shape:", X_train.shape)
print("X_train data type:", X_train.dtype)
print("y_train shape:", y_train.shape)
print("y_train data type:", y_train.dtype)
np.save(os.path.join(dir_path, 'X_train.npy'), X_train)
np.save(os.path.join(dir_path, 'y_train.npy'), y_train)


# Define the model architecture
def create_face_recognition_model():
    model = Sequential()
    # Convolutional layers
    model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 3)))
    model.add(MaxPooling2D((2, 2)))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D((2, 2)))
    model.add(Conv2D(128, (3, 3), activation='relu'))
    model.add(MaxPooling2D((2, 2)))
    # Flatten layer
    model.add(Flatten())
    # Dense layers
    model.add(Dense(256, activation='relu'))
    model.add(Dense(128, activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(16, activation='relu'))
    model.add(Dense(8, activation='relu'))
    # Output layer
    model.add(Dense(1, activation='sigmoid'))
    return model


# Create the face recognition model
face_recognition_model = create_face_recognition_model()

# Compile the model
face_recognition_model.compile(optimizer='adam', loss= 'binary_crossentropy', metrics=['accuracy'])
checkpoint = ModelCheckpoint(os.path.join(dir_path, 'best_model.h5'),monitor='val_loss',mode='min',save_best_only=True,verbose=1)
history = face_recognition_model.fit(X_train, y_train,epochs=50,batch_size=32,validation_data=(X_val, y_val),callbacks=[checkpoint])

val_loss, val_acc = face_recognition_model.evaluate(X_val, y_val, batch_size=32)

print("Validation Loss:", val_loss)
print("Validation Accuracy:", val_acc)

# Load the best model
best_model = tf.keras.models.load_model('best_model.h5')
best_model.save('my_model.h5')

X_test = np.load(os.path.join(dir_path, 'X.npy'), allow_pickle=True)
y_test = np.load(os.path.join(dir_path, 'y.npy'), allow_pickle=True)

# Save the test data
np.save(os.path.join(dir_path, 'X_test.npy'), X_test)
np.save(os.path.join(dir_path, 'y_test.npy'), y_test)
