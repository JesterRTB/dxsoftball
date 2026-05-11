import streamlit as st
import pandas as pd
from Home import supabase

st.set_page_config(page_title="D-X Leaderboard", layout="wide", page_icon="https://images.seeklogo.com/logo-png/27/1/d-generation-x-logo-png_seeklogo-275249.png")

st.subheader(":green[D-Generation X Leaders]")

def get_sorted_seasons():
    # Fetch unique seasons from your guts or stats table
    response = supabase.table("guts").select("season").execute()
    seasons = list(set([row['season'] for row in response.data]))
    
    # Custom sorting logic: Year first, then Season order
    season_order = {"Spring": 1, "Summer": 2, "Fall": 3, "Winter": 4}
    
    def sort_key(s):
        parts = s.split() # e.g., ["Summer", "2023"]
        return (int(parts[1]), season_order.get(parts[0], 5))
    
    return sorted(seasons, key=sort_key)

# --- 2. Implementation ---
all_seasons = get_sorted_seasons()

if all_seasons:
    # Use select_slider to pick a RANGE (tuple)
    # The 'value' parameter sets the default start/end
    start_season, end_season = st.select_slider(
        "Select Season Range",
        options=all_seasons,
        value=(all_seasons[0], all_seasons[-1]) 
    )
    
    st.write(f"Showing Leaderboard from **{start_season}** to **{end_season}**")

    # --- 3. Call your SQL function ---
    # leaderboard_df = supabase.rpc("get_leaderboard", {
    #     "start_season": start_season, 
    #     "end_season": end_season
    # }).execute()
