from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import joblib

# Load trained model and scaler
model = load_model("lstm_forecasting_model.h5")
scaler = joblib.load("scaler.pkl")  # Load the saved scaler

# Initialize FastAPI app
app = FastAPI()

# Request model
class ForecastRequest(BaseModel):
    commodity: str
    market: str
    forecast_days: int

@app.post("/forecast/")
def forecast_prices(request: ForecastRequest):
    """
    API endpoint to forecast future retail prices for a commodity and market.
    """
    commodity, market, forecast_days = request.commodity, request.market, request.forecast_days

    # Load dataset
    data = pd.read_csv("merged_data.csv", parse_dates=["Date"])

    # Filter data for the selected commodity and market
    filtered_data = data[(data["Commodity"] == commodity) & (data["Market"] == market)]
    if filtered_data.empty:
        return {"error": f"No data available for {commodity} in {market}"}

    # Select features used in training
    selected_features = [
        "Retail", "Wholesale_log", "Supply_Volume_log",
        "Retail_Lag1", "Retail_Lag7", "Retail_Rolling3",
        "Wholesale_Rolling3", "Month_sin", "Month_cos"
    ]

    filtered_data = filtered_data[selected_features].dropna()
    data_scaled = scaler.transform(filtered_data)

    # Define sequence length
    seq_length = 14
    current_input = data_scaled[-seq_length:].reshape(1, seq_length, data_scaled.shape[1])

    predictions = []
    for _ in range(forecast_days):
        next_day_scaled = model.predict(current_input, verbose=0)

        # Expand predicted price to match feature count
        next_day_scaled_expanded = np.zeros((1, data_scaled.shape[1]))
        next_day_scaled_expanded[0, 0] = next_day_scaled[0, 0]  # Assign predicted price

        # Inverse transform to original price scale
        next_day_price = scaler.inverse_transform(next_day_scaled_expanded)[0, 0]
        predictions.append(next_day_price)

        # Update input sequence
        next_input = np.vstack((current_input[0, 1:], next_day_scaled_expanded))
        current_input = next_input.reshape(1, seq_length, data_scaled.shape[1])

    # Generate future dates
    future_dates = pd.date_range(start=data["Date"].max() + pd.Timedelta(days=1), periods=forecast_days)
    forecast_result = [{"date": str(future_dates[i]), "predicted_price": predictions[i]} for i in range(forecast_days)]

    return {"commodity": commodity, "market": market, "forecast": forecast_result}


# start api
# uvicorn app:app --host 0.0.0.0 --port 8000 --reload

# url
# http://127.0.0.1:8000/docs
