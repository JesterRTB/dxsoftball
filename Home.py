import streamlit as st
import pandas as pd
import requests
from ics import Calendar
import arrow
from utils import (
    supabase
)

st.set_page_config(page_title="D-Generation X Schedule", page_icon="https://images.seeklogo.com/logo-png/27/1/d-generation-x-logo-png_seeklogo-275249.png")

st.subheader(":green[D-Generation X Schedule]")

@st.cache_data(ttl=3600)  # Caches the schedule for 1 hour so it loads lightning fast
def get_league_schedule(url):
    response = requests.get(url)
    response.raise_for_status()

    calendar = Calendar(response.text)
    
    events = []
    for event in calendar.events:
        # QuickScores times are typically UTC; convert to Chicago local time
        start_time = arrow.get(event.begin).to('US/Central')
        
        events.append({
            "Date": start_time.format('ddd, MMM D'),
            "Time": start_time.format('h:mm A'),
            "Opponent": event.name.replace("Softball - ", ""), # Clean up event title prefix
            "Field": event.location if event.location else "TBD",
            "Unix": start_time.timestamp() # Helper column for accurate chronological sorting
        })
    
    # Return sorted by game time
    return pd.DataFrame(events).sort_values("Unix")

try:
    calendar_url = st.secrets["CALENDAR_URL"]
    df_schedule = get_league_schedule(calendar_url)
    
    st.dataframe(
        df_schedule[["Date", "Time", "Opponent", "Field"]],
        hide_index=True,
        use_container_width=True
    )

except Exception as e:
    st.error(f"Error loading schedule: {e}")
