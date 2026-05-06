import streamlit as st
import pandas as pd
from supabase import create_client
import requests
from ics import Calendar
import arrow

# Initialize connection
@st.cache_resource
def init_connection():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase = init_connection()

st.set_page_config(page_title="D-Generation X", page_icon="🥎")

def get_calendar_events(url):
    response = requests.get(url)
    calendar = Calendar(response.text)
    
    events = []
    for event in calendar.events:
        # Convert to local time (Chicago)
        start = arrow.get(event.begin).to('US/Central')
        events.append({
            "Game": event.name,
            "Date": start.format('MMM D'),
            "Time": start.format('h:mm A'),
            "Location": event.location,
            "Raw_Date": start.datetime # For sorting
        })
    
    return pd.DataFrame(events).sort_values("Raw_Date")

# Your "Public Address in iCal format" from Google Settings
ics_url = st.secrets["<iframe src="https://calendar.google.com/calendar/embed?src=0njlfmi13vb164gn4banaovrt5m8rhd9%40import.calendar.google.com&ctz=America%2FChicago" style="border: 0" width="800" height="600" frameborder="0" scrolling="no"></iframe>"]

try:
    df = get_calendar_events(ics_url)
    
    st.subheader("Upcoming Schedule")
    # Display as a clean, flat table
    st.table(df[["Date", "Time", "Game", "Location"]])
    
except Exception as e:
    st.error("Could not sync with the league calendar.")

st.image("https://images.seeklogo.com/logo-png/27/1/d-generation-x-logo-png_seeklogo-275249.png")
