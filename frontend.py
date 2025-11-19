import streamlit as st
import requests

API_URL = ""

st.title("Insurance Premium Catergory Predictor")
st.markdown("Enter you details below:")


#Input Fields

age = st.number_input("Age" , min_value=1 , max_value=119 , value=30)