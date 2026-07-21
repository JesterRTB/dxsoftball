import streamlit as st
import pandas as pd
from supabase import create_client
import requests
from ics import Calendar
import arrow
from curl_cffi import requests

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
    if url.startswith("webcal://"):
        url = url.replace("webcal://", "https://", 1)

    # impersonate="chrome" sends Chrome's exact TLS fingerprint to bypass Cloudflare
    response = requests.get(url, impersonate="chrome")
    response.raise_for_status()

    if response.text.strip().startswith("<"):
        raise ValueError(f"Received HTML snippet:\n\n{response.text[:500]}")

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
