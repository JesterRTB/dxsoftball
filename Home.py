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

st.write(
    """**Alabama Slammers @ D-Generation X**  
    Monday, Aug 24 
    8:40 PM  
    Melas #1"""
)

st.write(
    """**Got Errorrs @ D-Generation X**  
    Monday, Aug 24  
    9:45 PM  
    Melas #1"""
)

st.divider()

st.write(
    """**D-Generation X @ Draft Picks**  
    Monday, Aug 31  
    6:30 PM  
    Melas #3"""
)

st.write(
    """**G.O.A.T.S. @ D-Generation X**  
    Monday, Aug 31  
    7:35 PM  
    Melas #2"""
)

st.divider()

st.write(
    """**Labor Day**  
    Monday, Sep 7"""
)

st.divider()

st.write(
    """**D-Generation X @ Get Wrecked**  
    Monday, Sep 14  
    8:40 PM  
    Melas #2"""
)

st.write(
    """**D-Generation X @ Blue Steel**  
    Monday, Sep 14  
    9:45 PM  
    Melas #2"""
)

st.divider()

st.write(
    """**D-Generation X @ Got Errorrs**  
    Monday, Sep 21  
    6:30 PM  
    Melas #2"""
)

st.write(
    """**D-Generation X @ Village Idiots**  
    Monday, Sep 21  
    7:35 PM  
    Melas #1"""
)
