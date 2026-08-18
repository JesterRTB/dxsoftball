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

st.subheader(":green[D-Generation X Upcoming Schedule]")
st.write("")

st.write("**August 24**")
st.write(
    """**Alabama Slammers @ :green[D-Generation X]**  
    8:40 PM  
    Melas #1"""
)
st.write(
    """**Got Errorrs @ :green[D-Generation X]**  
    9:45 PM  
    Melas #1"""
)

st.divider()

st.write("**August 31**")
st.write(
    """**:green[D-Generation X] @ Draft Picks**  
    6:30 PM  
    Melas #3"""
)
st.write(
    """**G.O.A.T.S. @ :green[D-Generation X]**  
    7:35 PM  
    Melas #2"""
)

st.divider()

st.write("**September 7**")
st.write(
    """**Labor Day**"""
)

st.divider()

st.write("**September 14**")
st.write(
    """**:green[D-Generation X] @ Get Wrecked**  
    8:40 PM  
    Melas #2"""
)
st.write(
    """**:green[D-Generation X] @ Blue Steel**  
    9:45 PM  
    Melas #2"""
)

st.divider()

st.write("**September 21**")
st.write(
    """**:green[D-Generation X] @ Got Errorrs**  
    6:30 PM  
    Melas #2"""
)
st.write(
    """**:green[D-Generation X] @ Village Idiots**  
    7:35 PM  
    Melas #1"""
)
