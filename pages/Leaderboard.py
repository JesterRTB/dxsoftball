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
        value=(all_seasons[-1], all_seasons[-1]) 
    )

    try:
        leaderboard_response = supabase.rpc("get_leaderboard", {
            "start_season": start_season, 
            "end_season": end_season
        }).execute()
    
        df = pd.DataFrame(leaderboard_response.data)

    except Exception as e:
        st.error("Postgres Error Detected!")
        # This will print the specific reason (e.g., "invalid input syntax for integer")
        if hasattr(e, 'details'):
            st.write(f"**Details:** {e.details}")
        if hasattr(e, 'message'):
            st.write(f"**Message:** {e.message}")
        st.stop() # Stop execution so it doesn't crash later

    tab_overview, tab_standard_batting, tab_advanced_batting, tab_pitching, tab_fielding, tab_value = st.tabs(["Overview", "Standard Batting", "Advanced Batting", "Pitching", "Fielding", "Value"])

    with tab_overview:
        df = df.sort_values(by="wins_above_replacement", ascending=False)
        st.dataframe(
                df,
                height="content",
                hide_index=True,
                placeholder="",
                column_order=[
                    "player","games_batting","plate_appearances","runs","home_runs","runs_batted_in","batting_average","on_base_percentage","slugging_percentage",
                    "on_base_plus_slugging","wrc_plus","wraa","defensive_run_value","wins_above_replacement"
                ],
                column_config={
                    "player": st.column_config.Column("Player", help="**Player**"),
                    "games_batting": st.column_config.NumberColumn("G", format="%d", help="**Games**"),
                    "plate_appearances": st.column_config.NumberColumn("PA", format="%d", help="**Plate Appearances**"),
                    "runs": st.column_config.NumberColumn("R", format="%d", help="**Runs Scored**"),
                    "home_runs": st.column_config.NumberColumn("HR", format="%d", help="**Home Runs**"),
                    "runs_batted_in": st.column_config.NumberColumn("RBI", format="%d", help="**Runs Batted In**"),
                    "batting_average": st.column_config.NumberColumn("AVG", format="%.3f", help="**Batting Average**  \nH/AB"),
                    "on_base_percentage": st.column_config.NumberColumn("OBP", format="%.3f", help="**On-Base Percentage**  \n(H+BB)/PA"),
                    "slugging_percentage": st.column_config.NumberColumn("SLG", format="%.3f", help="**Slugging Percentage**  \nTB/AB"),
                    "on_base_plus_slugging": st.column_config.NumberColumn("OPS", format="%.3f", help="**On-Base Plus Slugging**  \nOBP+SLG"),
                    "wrc_plus": st.column_config.NumberColumn("wRC+", format="%.0f", help="**Adjusted Weighted Runs Created Plus**"),
                    "wraa": st.column_config.NumberColumn("Bat", format="%.1f", help="**Batting Run Value**"),
                    "defensive_run_value": st.column_config.NumberColumn("Def", format="%.1f", help="**Defensive Run Value**"),
                    "wins_above_replacement": st.column_config.NumberColumn("WAR", format="%.1f", help="**Wins Above Replacement**")
                }
            )
