import streamlit as st
import requests

API_URL = ""

st.title("Insurance Premium Catergory Predictor")
st.markdown("Enter you details below:")


#Input Fields

age = st.number_input("Age" , min_value=1 , max_value=119 , value=30)
weight = st.number_input("Weight(kg)" , min_value=1.0 , max_values=0.5 , value=1.7)
height = st.number_input("Height (m)" , min_value=0.5 , max_values=2.5 , value= 1.7)
income_lpa = st.number("Annual Income(LPA)" , min_value=0.1 , value= 10.0)
smoker = st.selectbox("Are you a smoker?" , options = [True , False])
city = st.text_input("City" , value="Mumbai")
occupation = st.selectbox(
    "Occupation",
    ['retired' , 'freelance' , 'student' , 'government' , 'business_owner' , 'unwmployed' , 'private_job']   
)


if st.button("Predict Premium Category"):
    input_data = {
        "age" : age,
        "weight" : weight, 
        "height" : height,
        "income_lpa": income_lpa,
        "smoker" : smoker,
        "city" : city,
        "occupation" : occupation
    }

