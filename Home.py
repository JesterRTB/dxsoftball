import streamlit as st
import pandas as pd
import requests
import json
from ics import Calendar
import arrow

def get_league_schedule(target_url):
    # Convert webcal:// to https:// if needed
    if target_url.startswith("webcal://"):
        target_url = target_url.replace("webcal://", "https://", 1)
        
    # Route through the allorigins proxy to bypass Cloudflare IP blocking
    proxy_url = f"https://api.allorigins.win/get?url={requests.utils.quote(target_url)}"
    
    response = requests.get(proxy_url)
    response.raise_for_status()
    
    # Parse the raw text contents out of the proxy's JSON response
    data = response.json()
    raw_ics_text = data.get("contents", "")
    
    # Safety check
    if raw_ics_text.strip().startswith("<"):
        raise ValueError("The proxy returned HTML instead of calendar data.")

    calendar = Calendar(raw_ics_text)
    
    events = []
    for event in calendar.events:
        # QuickScores uses UTC; convert to Chicago local time
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
    # Pass your original QuickScores link (webcal:// or https://) directly from secrets
    ical_link = st.secrets["CALENDAR_URL"]
    df = get_league_schedule(ical_link)
    
    st.dataframe(
        df[["Date", "Time", "Opponent", "Field"]],
        hide_index=True,
        use_container_width=True
    )

except Exception as e:
    st.error(f"Error details: {e}")
