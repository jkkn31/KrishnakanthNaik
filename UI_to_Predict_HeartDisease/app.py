import pandas as pd
import numpy as np
import streamlit as st
import base64
import pickle
import sklearn
import getpass
from PIL import Image


# all other imports
import os
# from streamlit_elements import Elements

###############################################################################

# The code below is for the layout of the page
if "widen" not in st.session_state:
    layout = "centered"
else:
    layout = "wide" if st.session_state.widen else "centered"

st.set_page_config(
    layout=layout,
    page_title='Heart Disease Prediction App',  # String or None. Strings get appended with "• Streamlit".
    page_icon= "images/hi.png",  # String, anything supported by st.image, or None.
)

###############################################################################
# Lets Prepare some data
data = {'18-24':0, '25-29':1,'30-34':2,'35-39':3,'40-44':4,'45-49':5,'50-54':6,'55-59':7,'60-64':8,'65-69':9,'70-74':10,'75-79':11,'80 or older':12}
age_df = pd.DataFrame({'AgeCategory' : data.keys() , 'AgeValue' : data.values() })


###############################################################################
# Define few functions


# bgimage_link = "https://drive.google.com/file/d/1qpO3e_leNXN30DVMkTRo7-LjyxA2lvzY/view?usp=share_link"
# Image from Local
path = os.path.dirname(__file__)
image_file = path+'/images/bh.jpg'

# Image from link
# add_bg_from_local(bgimage_link)

# Model Path
MODEL_PATH = path+"/model/rf_model_to_predict_heartDisease"

def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )

def featuresTransformations_to_df(agecat_key, bmi_key, gender, race, smoking, alcohol, health_key, diabetic, asthma, stroke, skincancer, kidneydisease) -> pd.DataFrame:
    age_dict = {'18-24':0, '25-29':1,'30-34':2,'35-39':3,'40-44':4,'45-49':5,'50-54':6,'55-59':7,'60-64':8,'65-69':9,'70-74':10,'75-79':11,'80 or older':12}
    health_dict = {'Poor':0,'Fair':1,'Good':2,'Very good':3,'Excellent':4}
    bmi_dict = {'UnderWeight':0,'NormalWeight':1,'OverWeight':2,'Obesity Class I':3,'Obesity Class II':4, 'Obesity Class III':5}
    dict = {"Yes": 1, "No": 0}

    agecat = age_dict.get(agecat_key)
    health = health_dict.get(health_key)
    bmi = bmi_dict.get(bmi_key)
    diabetic = 1 if diabetic == "Yes" else 0
    gender = 1 if gender == "Male" else 0
    race = 1 if race == "White" else 0

    stroke = 1 if stroke == "Yes" else 0
    skincancer = 1 if skincancer == "Yes" else 0
    kidneydisease = 1 if kidneydisease == "Yes" else 0
    asthma = 1 if asthma == "Yes" else 0
    smoking = 1 if smoking == "Yes" else 0
    alcohol = 1 if alcohol == "Yes" else 0


    df = pd.DataFrame({
        "AgeCategory": [agecat],
        "Stroke": [stroke],
        "Diabetic_Yes": [diabetic],
        "KidneyDisease": [kidneydisease],
        "Smoking": [smoking],
        "SkinCancer": [skincancer],
        "Is_Male": [gender],
        "BMI": [bmi],
        "Asthma": [asthma],
        "Race_White": [race],
        "AlcoholDrinking": [alcohol],
        "GenHealth": [health]
    })

    return df

###############################################################################
add_bg_from_local(image_file)

st.title("Heart Disease Prediction")
st.subheader("Are you wondering about the condition of your heart? "
             "This app will help you to diagnose it!")



st.subheader("General Information:")
col1, col2, col3 = st.columns(3)

with col1:
    gender = st.selectbox(
    "Gender",
    options = ["Male", "Female"],
    help="Choose your Gender!",
    )

with col2:
    agecat_key = st.selectbox(
        "Age Group",
        options=age_df.AgeCategory.unique().tolist(),
        help="Choose a age group you belong to!",
    )

with col3:
    race = st.selectbox(
        "Race",
        options= ['White', 'Black', 'Asian', 'American Indian/Alaskan Native', 'Hispanic',  'Other'],
        help="Choose your Race!",
    )

    # ['AgeCategory', 'Stroke', 'Diabetic_Yes', 'KidneyDisease', 'Smoking', 'SkinCancer', 'is_Male', 'BMI', 'Asthma',
     # 'Race_White', 'AlcoholDrinking', 'GenHealth']

st.subheader("Habits:")
col4, col5 = st.columns(2)

with col4:
    smoking = st.selectbox(
        "Do you Smoke?",
        options=["Yes", "No"],
        help="Whether you smoke or Not!",
    )

with col5:
    alcohol = st.selectbox(
        "Do you Drink Alcohol?",
        options=["Yes", "No"],
        help="Are you Alcoholic or Not!",
    )

st.subheader("Health Information:")
col6, col7, col8, col12 = st.columns(4)

with col7:
    health_key = st.selectbox(
        "How is your Health?",
        options=[ 'Poor', 'Fair', 'Good', 'Very good', 'Excellent'],
        help="Be Frank about your health condition!",
    )

with col12:
    asthma = st.selectbox(
        "Ever had  Asthma?",
        options= ["Yes", "No"],
        help="(Ever told) (you had) Asthma?",
    )
with col8:
    diabetic = st.selectbox(
        "Are you Diabetic?",
        options= ['Yes', 'No', 'No, borderline diabetes', 'Yes (during pregnancy)'],
        help = "Ever had diabetes?",
    )
with col6:
    bmi_key = st.selectbox(
        "BMI",
        options= ['UnderWeight', 'NormalWeight', 'OverWeight', 'Obesity Class I', "Obesity Class II", "Obesity Class III"],
        help = "Please choose respective BMI category!",
    )

st.subheader("Critical Health Issues:")
col8, col9, col10 = st.columns(3)

with col8:
    stroke = st.selectbox(
        "Ever had a Heart Stroke in the Past?",
        options=["Yes", "No"],
        help="Ever had a stroke in the past atleast once?",
    )

with col9:
    skincancer = st.selectbox(
        "Ever Diagnosed with Skin Caner?",
        options=["Yes", "No"],
        help="(Ever told) Diagnosed with Skin Cancer?",
    )
with col10:
    kidneydisease = st.selectbox(
        "Ever Diagnosed with Kidney Disease?",
        options=["Yes", "No"],
        help="Not including Kidney Stones, Bladder Infection or Incontinence, were you ever told you had Kidney Disease?",
    )

st.write("")
col8, col9, col10 = st.columns(3)

with col8:
    predict = st.button("Predict!")
                # with col2:



log_model = pickle.load(open(MODEL_PATH, "rb"))

if predict:
    # st.expander("Hey Clicked on predict buttion")
    df = featuresTransformations_to_df(agecat_key, bmi_key, gender, race, smoking, alcohol, health_key, diabetic, asthma, stroke, skincancer, kidneydisease)
    prediction = log_model.predict(df)
    prediction_prob = log_model.predict_proba(df)

    # st.write(f"Model Prediction {prediction} and its probability {prediction_prob}")

    if prediction ==0:
        st.write(f"Dr. RandomForest says that you are LESS prone to Heart Disease with a probability of {(100*prediction_prob[0][1]).round(1)}%.")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("![Good](https://media.giphy.com/media/trhFX3qdAPF3GjYPMt/giphy.gif)")

    else:
        st.write(f"Dr. RandomForest says that you are Highly prone to Heart Disease with a probability of {(100*prediction_prob[0][1]).round(1)}%.")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("![Bad](https://media4.giphy.com/media/zaMldSPOkLNu9iYgZ6/giphy.gif?cid=29caca75yzsr24jwjoy2f8ze5azrdqka0mlt7untywajjgme&rid=giphy.gif&ct=g)")
            # Big gif
            # st.markdown("![Alt Text](https://media3.giphy.com/media/2UIeG5bGcwKK3nwAP0/giphy.gif?cid=29caca75i6x91f7yc0c12ghfj8fsm9eic6g4wo1fhs8odx32&rid=giphy.gif&ct=g)")


st.caption(
    "Made with 💓, by Krishnakanth Naik"
)




