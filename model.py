from tensorflow.keras.models import load_model

model = load_model(r"C:\Users\HP\Downloads\plant_disease_model.keras", compile=False)

print("Model loaded successfully ✅")
model.summary()
