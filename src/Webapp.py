import streamlit as st
import requests
from datetime import datetime
import subprocess
import time

def start_fastapi_server():
    process = subprocess.Popen(["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"])
    time.sleep(2)  # Give the server a couple of seconds to start
    return process

# Start the FastAPI server when the Streamlit app starts, if not already running
if 'fastapi_process' not in st.session_state:
    st.session_state.fastapi_process = start_fastapi_server()

# Apply custom CSS for beautification and background color change
st.markdown(
    """
    <style>
    .stApp {
     /* ##ffbf00 */
        background-color: #f7f7f7 ;  /* Amber background for the entire app */
        color: #333333;  /* Darker text color for contrast */
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        font-size: 16px;
        margin: 0 auto; /* Center the button */
        display: block; /* Required to center the button */
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .stNumberInput label, .stDateInput label, .stTimeInput label {
        color: blue;  /* Blue color for labels */
        font-weight: bold;  /* Make the label bold */
        text-align: center;  /* Center align the labels */
        display: block;
        width: 100%;
        margin-top: 5px;
    }
    .stNumberInput.col3 label {
        margin-top: -60px;  /* Adjust this value as needed to align with other columns */
    }
    .stWarning {
        background-color: #b38f00;
        padding: 10px;
        border-radius: 10px;
        font-size: 14px;
        color: red;  /* Red text for the warning message */
        font-weight: bold;
    }
    .stSuccess {
        background-color: #dff0d8;
        padding: 10px;
        border-radius: 10px;
        font-size: 14px;
        color: #333333;  /* Dark text for contrast */
    }
    .prediction-card {
        background-color: #333333;
        color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
        margin-top: 20px;
        text-align: center;
        width: 50%; /* Adjust the width as needed */
        margin-left: auto;
        margin-right: auto;
    }
    .prediction-title {
        font-size: 20px;
        font-weight: bold;
        color: #FFD700;  /* Gold color for the title */
    }
    .prediction-details {
        font-size: 16px;
        color: white;
    }
    .prediction-value {
        font-size: 24px;
        font-weight: bold;
        color: #00FF00;  /* Bright green for the prediction value */
    }
    h1 { 
        color: #b36200;  /* Gold color for the title */
        font-size: 2.5em;
        text-align: center;
    }
    h2 {
        color: #333333;  /* Dark text color for contrast */
        font-size: 1.75em;
        margin-bottom: 20px;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and Header
st.markdown("<h1>Solar Irradiance 🌞 Prediction App</h1>", unsafe_allow_html=True)
st.markdown("<h2>Input Parameters</h2>", unsafe_allow_html=True)

# Arranging st.number_input, st.date_input, and st.time_input components in horizontal lines using columns
col1, col2, col3, col4 = st.columns(4)
with col1:
    date = st.date_input("📅 Select the Date", datetime.now())
    sun_flag = st.number_input('☀️ Avg Sun Flag', min_value=0, max_value=10, value=8)
    Avg_Total_Cloud_Cover = st.number_input('🌥️ Avg Cloud Cover [%]', min_value=0.0, value=0.96)

with col2:
    time = st.time_input("⏰ Select the Time", datetime.now().time())
    datetime_input = datetime.combine(date, time).isoformat()
    blue_red_min = st.number_input('🌈 Avg Blue/Red_min', min_value=0.0, value=0.96)
    Avg_BRBG_Total_Cloud_Cover = st.number_input('☁️ Avg Blue/Red_Total Cloud Cover', min_value=0.0, value=0.96)

with col3:
    zenith_angle = st.number_input('🌅 Avg Zenith Angle [degrees]', min_value=0.0, max_value=180.0, value=85.0)
    opaque_cloud_cover = st.number_input('☁️ Avg Opaque Cloud Cover [%]', min_value=0.0, max_value=100.0, value=10.0)
    Avg_Global_CMP22_vent_cor = st.number_input('🌍 Avg CMP22 Vent Correlation', min_value=0.0, value=0.96)

with col4:
    Avg_Azimuth_Angle_degrees = st.number_input('🧭 Avg Azimuthal Angle', min_value=0.0, value=0.96)
    Avg_Tower_Dew_Point_Temp_deg_C = st.number_input('💧 Avg Dew Point Temp [°C]', min_value=0.0, value=0.96)
    Avg_Albedo_CMP11 = st.number_input('❄️ Avg Albedo', min_value=0.0, value=0.96)


st.write("")

# Predict button
if st.button('🔍 Predict Solar Irradiance'):
    prediction_data = {
        "DATETIME": datetime_input,
        "Avg_Zenith_Angle_degrees": zenith_angle,
        "Avg_Sun_Flag": sun_flag,
        "Avg_Opaque_Cloud_Cover": opaque_cloud_cover,
        "Avg_Blue_Red_min": blue_red_min,
        "Avg_Global_CMP22_vent_cor": Avg_Global_CMP22_vent_cor,
        "Avg_BRBG_Total_Cloud_Cover": Avg_BRBG_Total_Cloud_Cover,
        "Avg_Azimuth_Angle_degrees": Avg_Azimuth_Angle_degrees,
        "Avg_Albedo_CMP11": Avg_Albedo_CMP11,
        "Avg_Tower_Dew_Point_Temp_deg_C": Avg_Tower_Dew_Point_Temp_deg_C,
        "Avg_Total_Cloud_Cover": Avg_Total_Cloud_Cover
    }

    url = 'http://localhost:8000/predict/'

    response = requests.post(url, json=prediction_data)

    # Display the prediction result in a beautified manner
    if response.status_code != 200:
        st.error(f"Failed to fetch data: {response.text}")
    else:
        prediction = response.json()
        prediction_details = prediction["predictions"][0]

        # Parse and format the datetime string
        formatted_datetime = datetime.strptime(prediction_details['ds'], "%Y-%m-%dT%H:%M:%S.%f").strftime("%B %d, %Y %H:%M:%S")

        st.markdown(
            f"""
            <div class="prediction-card">
                <div class="prediction-title">Solar Irradiance Prediction</div>
                <div class="prediction-details"><b>Date/Time:</b> {formatted_datetime}</div>
                <div class="prediction-details"><b>Predicted Irradiance:</b> <span class="prediction-value">{prediction_details['yhat']:.2f} W/m²</span></div>
                <div class="prediction-details"><b>Prediction Interval:</b> {prediction_details['yhat_lower']:.2f} W/m² - {prediction_details['yhat_upper']:.2f} W/m²</div>
            </div>
            """,
            unsafe_allow_html=True
        )

# Space before the server stop section
st.write("")
st.write("")

# Warning and stop server section
st.markdown('<div class="stWarning">⚠️ Please stop the FastAPI server only if you are sure no more prediction requests need to be sent. Once your predictions are complete, you can stop the server to free up resources.</div>', unsafe_allow_html=True)    

# Stop FastAPI server when Streamlit app is stopped
def stop_fastapi_server(process):
    process.terminate()
    process.wait()

st.write("")
st.write("")     

if st.button("🛑 Stop FastAPI Server"):
    if 'fastapi_process' in st.session_state and st.session_state.fastapi_process:
        stop_fastapi_server(st.session_state.fastapi_process)
        st.markdown('<div class="stSuccess">FastAPI server stopped successfully.</div>', unsafe_allow_html=True)
