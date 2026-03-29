import streamlit as st 
import joblib
import numpy as np 
import pandas as pd 

base_path = r"D:\Projects\salary-predictor\global-salary-predictor"

# Load the saved model and encoders
try:
    model = joblib.load(r"D:\Projects\salary-predictor\global-salary-predictor\salary_model.pkl")
    le_region = joblib.load(r"D:\Projects\salary-predictor\global-salary-predictor\le_region.pkl")
    le_income = joblib.load(r"D:\Projects\salary-predictor\global-salary-predictor\le_income.pkl")
    le_continent = joblib.load(r"D:\Projects\salary-predictor\global-salary-predictor\le_continent.pkl")
    st.success("Model loaded successfully!")
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

# Load country data
salary_df = pd.read_csv(r"D:\Projects\salary-predictor\global-salary-predictor\salary_data.csv")
meta_df = pd.read_csv(r"D:\Projects\salary-predictor\global-salary-predictor\EdStatsCountry.csv")
meta_df = meta_df[['Short Name', 'Region', 'Income Group']].dropna()

# Page title and description 
st.title ('Global Salary Predictor')
st.write('Estimate average annual salaries across 197 countries based on region and income group.')
st.info('High income OECD countries average $53,000/year vs Low income countries at $6,500/year - an 8x gap. This tool helps visualise that disparity')

# Input dropdowns 
st.subheader('Select a country profile')
st.write('**Option 1: Select by country name**')
country_list = ['-- Select a country --'] + sorted(salary_df['country_name'].tolist())
country_choice = st.selectbox('Country', country_list)
st.write('**Option 2: Select manually**')

region = st.selectbox('Region', le_region.classes_.tolist())
income =  st.selectbox('Income Group', le_income.classes_.tolist())
continent = st.selectbox('Continent', le_continent.classes_.tolist())


if country_choice != '-- Select a country --':
    match = meta_df[meta_df['Short Name'] == country_choice]
    if not match.empty:
        region = match.iloc[0]['Region']
        income = match.iloc[0]['Income Group']
        st.info(f'Auto-filled - Region: {region} | Income Group: {income}')

st.caption('Data source: SalaryExplorer (221 countries) merged with World Bank EdStats metadata')

# Predict button
if st.button('Predict Salary'):
    region_enc = le_region.transform([region])[0]
    income_enc = le_income.transform([income])[0]
    continent_enc = le_continent.transform([continent])[0]

    input_df = pd.DataFrame(
        [[region_enc, income_enc, continent_enc]],
        columns=['region_enc', 'income_enc', 'continent_enc']
    )

    prediction = model.predict(input_df)[0]

    st.success(f'Estimated Average Annual Salary: ${prediction:,.0f} USD')
    st.write(f'This is approximately ${prediction/12:,.0f} USD per month.')
    st.write('For reference: Switzerland averages USD 135,000/year. Zambia averages USD 3000/year.')