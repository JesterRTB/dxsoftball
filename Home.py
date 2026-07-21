import streamlit as st
import pandas as pd
import requests
from ics import Calendar
import arrow

st.set_page_config(
    page_title="D-Generation X", 
    page_icon="https://images.seeklogo.com/logo-png/27/1/d-generation-x-logo-png_seeklogo-275249.png",
    layout="wide"
)

st.subheader(":green[D-Generation X Schedule]")

st.info("Awaiting playoff schedule...", width=250)
