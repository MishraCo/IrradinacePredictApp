from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException
from typing import List, Optional
from pydantic import BaseModel
from mangum import Mangum

import pandas as pd

import os
import pickle

import logging


# Create an instance of the FastAPI class
app = FastAPI()

model_path = os.path.join(os.path.dirname(__file__), '..', 'Models', 'Prophetbest_model.pkl')
model_path = os.path.abspath(model_path)  # Resolves to absolute path

# Load your model
with open(model_path, 'rb') as f:
    model = pickle.load(f)


class PredictionRequest(BaseModel):
    DATETIME: str
    Avg_Zenith_Angle_degrees: float
    Avg_Sun_Flag: int
    Avg_Opaque_Cloud_Cover: float
    Avg_Blue_Red_min: float
    Avg_Global_CMP22_vent_cor: float  # This is your target
    Avg_BRBG_Total_Cloud_Cover: float
    Avg_Azimuth_Angle_degrees: float
    Avg_Albedo_CMP11: float
    Avg_Tower_Dew_Point_Temp_deg_C: float
    Avg_Total_Cloud_Cover: float

def prepare_data_for_prophet(df, datetime_col_name='DATETIME'):
    """
    Prepare the DataFrame for Prophet model predictions.
    
    Parameters:
    - df (DataFrame): The original DataFrame.
    - datetime_col_name (str): The name of the column in df that contains datetime information.

    Returns:
    - DataFrame: A DataFrame formatted for Prophet, with 'ds' as the datetime column.
    """
    try:
        # Format datetime in the required format
        df['ds'] = pd.to_datetime(df['DATETIME'])
        #df['ds'] = df['ds'].strftime('%Y-%m-%d %H:%M:%S')
        # Drop the original 'DATETIME' column and any other irrelevant columns
        df.drop(['DATETIME'], axis=1, inplace=True)
        # Ensure that data is sorted by 'ds'
        df.sort_values('ds', inplace=True)
        return df
    except KeyError:
        raise KeyError(f"Column {datetime_col_name} does not exist in DataFrame.")
    except Exception as e:
        raise Exception(f"An error occurred while preparing data for Prophet: {str(e)}")
    
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@app.get("/")
async def root():
    return {"Note": "Hello Dear User, please jump to /predict/ to view the predictions! "}

# Example usage in your FastAPI endpoint
@app.post("/predict/")
async def predict(request: PredictionRequest):
    try:
        print("Shweta, let's make an frontend app to predict Solar Irradiance.")
        data_dict = request.model_dump()
        df = pd.DataFrame([data_dict])
        
        # Preprocess DataFrame for Prophet
        df = prepare_data_for_prophet(df, datetime_col_name='DATETIME')
        
        # Assume the Prophet model expects other columns as well and they are set up correctly
        predictions = model.predict(df)
        predicted_values = predictions[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]

        response = jsonable_encoder(predicted_values.to_dict(orient='records'))
        return {"predictions": response}
    except Exception as e:
        return {"error": str(e)}
    

handler = Mangum(app)
