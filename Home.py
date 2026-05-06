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

# 1. Fetch and Parse
def get_league_schedule(url):
    # Fetch the raw calendar data
    response = requests.get(url)
    calendar = Calendar(response.text)
    
    events = []
    for event in calendar.events:
        # QuickScores usually provides UTC; convert to Chicago time
        start_time = arrow.get(event.begin).to('US/Central')
        
        events.append({
            "Date": start_time.format('ddd, MMM D'),
            "Time": start_time.format('h:mm A'),
            "Opponent": event.name.replace("Softball - ", ""), # Clean up the text
            "Field": event.location if event.location else "TBD",
            "Unix": start_time.timestamp() # For sorting
        })
    
    # Return as a DataFrame sorted by time
    return pd.DataFrame(events).sort_values("Unix")

st.subheader(":green[D-Generation X Schedule]")

try:
    ical_link = st.secrets["TEAM_CALENDAR_URL"]
    df = get_league_schedule(ical_link)
    
    # Display the upcoming games in a clean table
    # We drop the 'Unix' column so the user doesn't see it
    st.table(df[["Date", "Time", "Opponent", "Field"]])

except Exception as e:
    st.error("Wait... something went wrong with the calendar sync.")
    st.info("Make sure 'requests', 'ics', and 'arrow' are in your requirements.txt!")
