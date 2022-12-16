import pandas as pd
# import numpy as np
# import plotly.express as px
# import plotly.graph_objects as go
import streamlit as st
# import matplotlib.pyplot as plt

import time
import datetime
from datetime import datetime, timedelta, date, time
import getpass
from PIL import Image


# pd.set_option('max_columns', None)
# pd.set_option('max_rows', None)

# st.set_page_config(  # Alternate names: setup_page, page, layout
#     layout="wide",  # Can be "centered" or "wide". In the future also "dashboard", etc.
#     initial_sidebar_state="auto",  # Can be "auto", "expanded", "collapsed"
#     page_title='LCE Monintoring Dashboard',  # String or None. Strings get appended with "• Streamlit".
#     page_icon=None,  # String, anything supported by st.image, or None.
# )

# st.sidebar.image(image, use_column_width=False)


st.set_page_config(
        page_title="Heart Disease Prediction App",
        # page_icon="images/heart-fav.png"
    )

st.title("Heart Disease Prediction")
st.subheader("Are you wondering about the condition of your heart? "
             "This app will help you to diagnose it!")

col1, col2 = st.columns([1, 3])


st.sidebar.title('Diagonose Heart Disease')

race = st.sidebar.selectbox("Race", options=["White", "Asian", "Others"])
# sex = st.sidebar.selectbox("Sex", options=(sex for sex in heart.Sex.unique()))
# age_cat = st.sidebar.selectbox("Age category",
#                                options=(age_cat for age_cat in heart.AgeCategory.unique()))
# bmi_cat = st.sidebar.selectbox("BMI category",
#                                options=(bmi_cat for bmi_cat in heart.BMICategory.unique()))
# sleep_time = st.sidebar.number_input("How many hours on average do you sleep?", 0, 24, 7)
# gen_health = st.sidebar.selectbox("How can you define your general health?",
#                                   options=(gen_health for gen_health in heart.GenHealth.unique()))
# phys_health = st.sidebar.number_input("For how many days during the past 30 days was"
#                                       " your physical health not good?", 0, 30, 0)
# ment_health = st.sidebar.number_input("For how many days during the past 30 days was"
#                                               " your mental health not good?", 0, 30, 0)

