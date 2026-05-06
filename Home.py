import streamlit as st
import pandas as pd
from supabase import create_client

# Initialize connection
@st.cache_resource
def init_connection():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase = init_connection()

st.image("https://images.seeklogo.com/logo-png/27/1/d-generation-x-logo-png_seeklogo-275249.png")
