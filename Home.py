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

@st.cache_data(ttl=3600)
def get_league_schedule(url):
    # Fetch from Supabase Storage
    response = requests.get(url)
    response.raise_for_status()

    calendar = Calendar(response.text)
    
    events = []
    for event in calendar.events:
        # Convert UTC game times to Chicago local time
        start_time = arrow.get(event.begin).to('US/Central')
        
        # Clean up event name to isolate Opponent name
        opponent_name = event.name if event.name else "TBD"
        opponent_name = opponent_name.replace("Softball - ", "").replace("Softball ", "").strip()
        
        events.append({
            "Date": start_time.format('ddd, MMM D'),
            "Time": start_time.format('h:mm A'),
            "Opponent": opponent_name,
            "Field": event.location if event.location else "TBD",
            "Unix": start_time.timestamp()
        })
    
    if not events:
        return pd.DataFrame(columns=["Date", "Time", "Opponent", "Field"])

    # Convert to DataFrame and sort chronologically by Unix timestamp
    df = pd.DataFrame(events).sort_values("Unix")
    return df[["Date", "Time", "Opponent", "Field"]]

try:
    calendar_url = st.secrets["CALENDAR_URL"]
    df_schedule = get_league_schedule(calendar_url)
    
    if not df_schedule.empty:
        st.dataframe(
            df_schedule,
            hide_index=True,
            use_container_width=True
        )
    else:
        st.info("No upcoming games found in the schedule.")

except Exception as e:
    st.error(f"Error loading schedule: {e}")
