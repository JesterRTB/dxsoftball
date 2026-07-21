import streamlit as st
import pandas as pd
import requests
from ics import Calendar
import arrow
from utils import (
    supabase
)

st.set_page_config(page_title="D-Generation X", page_icon="https://images.seeklogo.com/logo-png/27/1/d-generation-x-logo-png_seeklogo-275249.png")

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
    ical_link = st.secrets["CALENDAR_URL"]
    df = get_league_schedule(ical_link)
    # Display the upcoming games in a clean table
    # We drop the 'Unix' column so the user doesn't see it
    st.table(
        df[["Date", "Time", "Opponent", "Field"]],
        hide_index=True
    )

except Exception as e:
    st.error(f"Error details: {e}") # This will show the actual technical error
    st.info("Make sure 'requests', 'ics', and 'arrow' are in your requirements.txt!")
