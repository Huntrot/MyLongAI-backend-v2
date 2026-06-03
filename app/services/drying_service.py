import joblib
import pandas as pd

from app.core.config import settings

drying_model = joblib.load(settings.DRYING_MODEL_PATH)

def predict_drying_time(avg_temperature: float, avg_humidity: float):
    df = pd.DataFrame([{
        "avg_temperature": avg_temperature,
        "avg_humidity": avg_humidity
    }])

    prediction = drying_model.predict(df)

    return {
        "message": "Drying time predicted successfully",
        "input": {
            "avg_temperature": avg_temperature,
            "avg_humidity": avg_humidity
        },
        "predicted_drying_time": float(prediction[0])
    }