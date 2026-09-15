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
st.link_button("QuickScores", "https://www.quickscores.com/Orgs/ResultsDisplay.php?OrgDir=ahpd&LeagueID=1740379")
st.write("")

st.subheader("**September 21**")
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
