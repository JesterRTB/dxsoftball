import streamlit as st
import pandas as pd
from Home import supabase

st.set_page_config(page_title="D-X Player Search", page_icon="🥎")

def get_all_players():
    # Fetch just the player names from the primary_positions table
    response = supabase.table("primary_positions").select("player").execute()
    # Extract names into a sorted list
    player_list = sorted([row['player'] for row in response.data])
    return player_list
    
def fetch_player_data(player_name):
    # 'get_player_profile' is the name of the SQL function
    # The dictionary keys must match the parameter names in your SQL function
    response = supabase.rpc("get_player_profile", {"target_player": player_name}).execute()
    
    # Convert the JSON response directly into a DataFrame
    return pd.DataFrame(response.data)

# Fetch the list for the selectbox
players = get_all_players()

# Add a placeholder or "Select a Player" at the top
selected_player = st.selectbox(
    "Select a player", 
    options=players,
    index=None,
    placeholder="Select a player",
    label_visibility="collapsed"
)

if selected_player:
    df = fetch_player_data(selected_player)
    
    if not df.empty:
        # Displaying the high-level profile info
        st.header(f"{selected_player}")
        st.markdown(
            f"""**Position:** {df['position_long'].iloc[0]}  
            **DX Debut:** {df['dx_debut'].iloc[0]}"""
        )
        tab_stats, tab_game_log = st.tabs(["Stats", "Game Log"])
        with tab_stas:
            st.subheader(":green[Overview]")
            st.dataframe(
                df,
                height="content",
                hide_index=True,
                placeholder="",
                column_order=(
                    "season",
                    "wins_above_replacement",
                    "games_batting",
                    "plate_appearances",
                    "runs",
                    "home_runs",
                    "runs_batted_in",
                    "batting_average",
                    "on_base_percentage",
                    "slugging_percentage",
                    "on_base_plus_slugging"
                )
            )
    else:
        st.warning("No player found with that name.")
