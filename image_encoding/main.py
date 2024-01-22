import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

# Define the directory for the training and validation sets
train_dir = 'trainset'
valid_dir = 'validset'

# Define the image size and batch size
image_size = (224, 224)
batch_size = 32

# Create an instance of the ImageDataGenerator class for loading and preprocessing images in the training set
train_datagen = ImageDataGenerator(
    rescale=1./255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True
)

# Load the training set using the flow_from_directory method
train_generator = train_datagen.flow_from_directory(
    directory=train_dir,
    target_size=image_size,
    batch_size=batch_size,
    class_mode='categorical',
    shuffle=True
)

# Create an instance of the ImageDataGenerator class for loading and preprocessing images in the validation set
valid_datagen = ImageDataGenerator(rescale=1./255)

# Load the validation set using the flow_from_directory method
valid_generator = valid_datagen.flow_from_directory(
    directory=valid_dir,
    target_size=image_size,
    batch_size=batch_size,
    class_mode='categorical',
    shuffle=True
)

# Define the architecture of the model
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)),
    MaxPooling2D((2, 2)),
    Dropout(0.2),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Dropout(0.2),
    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Dropout(0.2),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(6, activation='softmax')
])

# Compile the model
model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# Train the model on the training set and validate it on the validation set
history = model.fit(
    train_generator,
    steps_per_epoch=train_generator.samples//batch_size,
    validation_data=valid_generator,
    validation_steps=valid_generator.samples//batch_size,
    epochs=10
)

# Save the trained model to a file
model.save('product_classifier.h5')
