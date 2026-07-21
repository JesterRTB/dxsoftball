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

st.set_page_config(page_title="D-Generation X", page_icon="https://images.seeklogo.com/logo-png/27/1/d-generation-x-logo-png_seeklogo-275249.png")

# 1. Fetch and Parse
def get_league_schedule(url):
    # 1. Convert webcal:// protocol to https://
    if url.startswith("webcal://"):
        url = url.replace("webcal://", "https://", 1)
        
    # 2. Add Accept and User-Agent headers to satisfy QuickScores
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/calendar, text/html, application/xhtml+xml, application/xml;q=0.9, */*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9"
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    # 3. Safety check for HTML error responses
    if response.text.strip().startswith("<"):
        raise ValueError("QuickScores returned a web page instead of iCal data.")

    calendar = Calendar(response.text)
    
    events = []
    for event in calendar.events:
        start_time = arrow.get(event.begin).to('US/Central')
        
        events.append({
            "Date": start_time.format('ddd, MMM D'),
            "Time": start_time.format('h:mm A'),
            "Opponent": event.name.replace("Softball - ", ""),
            "Field": event.location if event.location else "TBD",
            "Unix": start_time.timestamp()
        })
    
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
