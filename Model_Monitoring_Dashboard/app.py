import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import matplotlib.pyplot as plt

import time
import datetime
from datetime import datetime, timedelta, date, time
import getpass
from PIL import Image


pd.set_option('max_columns', None)
pd.set_option('max_rows', None)

st.set_page_config(  # Alternate names: setup_page, page, layout
    layout="wide",  # Can be "centered" or "wide". In the future also "dashboard", etc.
    initial_sidebar_state="auto",  # Can be "auto", "expanded", "collapsed"
    page_title='LCE Monintoring Dashboard',  # String or None. Strings get appended with "• Streamlit".
    page_icon=None,  # String, anything supported by st.image, or None.
)

image = Image.open('../images/tvs-logo.png')

st.sidebar.image(image, use_column_width=False)
st.sidebar.title('LCE Monitoring Dashboard')

# -------------------------------------------------------------------------------------
# Input Method
# -------------------------------------------------------------------------------------

# Select Monitoring Dashboard type
task = st.sidebar.selectbox(
    'Select',
    ['Model Monitoring','System Monitoring','Data Monitoring'])
st.title(f'LCE - {task}')


# Select start and end date

from datetime import datetime

mtd = datetime.today().replace(day=1)
today = datetime.now()
previous_day = datetime.now() + timedelta(days=-7)
past_90 = datetime.now() + timedelta(days=-30)


# -------------------------------------------------------------------------------------
# output Method
# -------------------------------------------------------------------------------------

if task == 'Data Monitoring':

    def dm_feature_prep(df, model_name):
        c1 = px.line(df, x="Scored_at", y=["Hot %","Warm %",  "Cold %"])
        c1.update_layout(title=model_name, title_font_size=25, title_x=0.5)
        return c1

    task = st.sidebar.selectbox('Select', ['Month till date', 'Past 30 days'])

    x1 = pd.read_csv("../data/hw_m1.csv")
    x1['Model'] = 'Model_1'
    x2 = pd.read_csv("../data/hw_m2.csv")
    x2['Model'] = 'Model_2'

    x3 = pd.read_csv("../data/hw_m3.csv")
    x3['Model'] = 'Model_3'

    x4 = pd.read_csv("../data/hw_m1.csv")
    x4['Model'] = 'Model_4'

    temp_df = pd.concat([x1, x2, x3, x4])

    # temp_df = pd.read_csv("../data/hw_dist.csv")
    temp_df.columns = ['Scored_at', "Hot %", "Warm %", "Cold %", "Model"]
    temp_df.Scored_at = pd.to_datetime(temp_df.Scored_at)

    if task == 'Past 30 days':
        today = datetime.now()
        previous_day = datetime.now() + timedelta(days=-30)
        df = temp_df[(temp_df.Scored_at >= pd.to_datetime(previous_day)) & (temp_df.Scored_at <= pd.to_datetime(today))].copy()

        col1, col2 = st.columns(2)
        col3, col4 = st.columns(2)

        with col1:
            chart = dm_feature_prep(df[df.Model== 'Model_1'], 'Model_1')
            st.plotly_chart(chart, use_container_width=True)
        with col2:
            chart = dm_feature_prep(df[df.Model=="Model_2" ], 'Model_2')
            st.plotly_chart(chart, use_container_width=True)
        with col3:
            chart = dm_feature_prep(df[df.Model=="Model_3" ], 'Model_3')
            st.plotly_chart(chart, use_container_width=True)
        with col4:
            chart = dm_feature_prep(df[df.Model== "Model_4"], 'Model_4')
            st.plotly_chart(chart, use_container_width=True)

    elif task == 'Month till date':
        today = datetime.now()
        previous_day = datetime.today().replace(day=1)
        df = temp_df[(temp_df.Scored_at >= pd.to_datetime(previous_day)) & (temp_df.Scored_at <= pd.to_datetime(today))].copy()

        col1, col2 = st.columns(2)
        col3, col4 = st.columns(2)

        with col1:
            chart = dm_feature_prep(df[df.Model== "Model_1"].drop('Model', axis=1), 'Model_1')
            st.plotly_chart(chart, use_container_width=True)
        with col2:
            chart = dm_feature_prep(df[df.Model== "Model_2"].drop('Model', axis=1), 'Model_2')
            st.plotly_chart(chart, use_container_width=True)
        with col3:
            chart = dm_feature_prep(df[df.Model== "Model_3"].drop('Model', axis=1), 'Model_3')
            st.plotly_chart(chart, use_container_width=True)
        with col4:
            chart = dm_feature_prep(df[df.Model== "Model_4"].drop('Model', axis=1), 'Model_4')
            st.plotly_chart(chart, use_container_width=True)


elif task == 'Model Monitoring':
    start_date = st.sidebar.date_input('Start date', previous_day)
    end_date = st.sidebar.date_input('End date', today)


    m1 = pd.read_csv("../data/model_1_mm.csv")
    m2 = pd.read_csv("../data/model_2_mm.csv")
    m3 = pd.read_csv("../data/model_3_mm.csv")
    m4 = pd.read_csv("../data/model_1_mm.csv")
    m1['Model'] = 'Model_1'
    m2['Model'] = 'Model_2'
    m3['Model'] = 'Model_3'
    m4['Model'] = 'Model_4'

    temp_df = pd.concat([m1, m2, m3, m4])
    temp_df.columns = ['computed_on', 'F2 Score', 'KS Decile', 'Conversion Abnormality Detected', 'Recall Score', 'Model']
    temp_df.computed_on = pd.to_datetime(temp_df.computed_on).dt.date
    temp_df = temp_df[(temp_df.computed_on >= pd.to_datetime(start_date)) & (temp_df.computed_on <= pd.to_datetime(end_date))].copy()

    fig_f2_score = px.line(temp_df, x="computed_on", y="F2 Score", color='Model')
    fig_f2_score.update_layout(title='F2 score', title_font_size=25, title_x=0.5)

    fig_recall_score = px.line(temp_df, x="computed_on", y="Recall Score", color='Model')
    fig_recall_score.update_layout(title='Recall score', title_font_size=25, title_x=0.5)

    fig_conv_abn = px.line(temp_df,x="computed_on",y="Conversion Abnormality Detected",color='Model')
    fig_conv_abn.update_layout(title='Conversion Abnormality Detected', title_font_size=25, title_x=0.5)

    fig_ks_decile = px.line(temp_df, x="computed_on", y="KS Decile", color='Model')
    fig_ks_decile.update_layout(title='KS Decile', title_font_size=25, title_x=0.5)

    col1, col2, = st.columns(2)
    col3, col4 = st.columns(2)

    with col1:
        st.plotly_chart(fig_f2_score,use_container_width=True)
    with col2:
        st.plotly_chart(fig_recall_score,use_container_width=True)
    with col3:
        st.plotly_chart(fig_conv_abn,use_container_width=True)
    with col4:
        st.plotly_chart(fig_ks_decile,use_container_width=True)


elif task == 'System Monitoring':
    last_30 = datetime.now() + timedelta(days=-30)
    start_date = st.sidebar.date_input('Start date', last_30)
    end_date = st.sidebar.date_input('End date', today)
    st.subheader('Inference - Pipelines')

    # Job API Table
    inference_pipeline = pd.read_csv("../data/job_api_status.csv")
    inference_pipeline.columns = ['run_name', 'run_date', 'run_state', 'run_trigger']
    inference_pipeline = inference_pipeline[inference_pipeline.run_trigger=='SCHEDULED']
    inference_pipeline.run_date = pd.to_datetime(inference_pipeline.run_date).dt.date
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)
    col5, col6 = st.columns(2)

    def common_chart_def(df, start_date, end_date, model_name):
        temp_df = inference_pipeline[((inference_pipeline.run_date) >= pd.to_datetime(start_date)) & (
                    (inference_pipeline.run_date) <= pd.to_datetime(end_date)) & (
                                                 inference_pipeline.run_name == model_name)].copy()
        v_count = temp_df.run_state.value_counts()
        v_count = pd.DataFrame({'type': v_count.index, 'run_rate': v_count.values})
        fig = px.pie(v_count, values='run_rate', names='type')
        fig.update_layout(title=f'{model_name}', title_font_size=25, title_x=0.5)

        st.plotly_chart(fig, use_container_width=True)
        if st.button(f'{model_name} - Pipeline Failures'):
            st.write(temp_df[temp_df.run_state == 'FAILED'])


    with col1:
        common_chart_def(inference_pipeline, start_date, end_date, 'Model_1')

    with col2:
        common_chart_def(inference_pipeline, start_date, end_date, 'Model_2')

    with col3:
        common_chart_def(inference_pipeline, start_date, end_date, 'Model_3')

    with col4:
        common_chart_def(inference_pipeline, start_date, end_date, 'Model_4')


