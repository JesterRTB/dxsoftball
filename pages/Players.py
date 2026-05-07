import streamlit as st
import pandas as pd
from Home import supabase

st.set_page_config(page_title="D-X Player Search", layout="wide", page_icon="🥎")

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
    width=300,
    placeholder="Select a player",
    label_visibility="collapsed"
)

if selected_player:
    df = fetch_player_data(selected_player)
    
    # Create a total row for all columns
    total_row = df.sum(numeric_only=True).to_frame().T
    total_row['season'] = "Total"
    total_row['batting_average'] = total_row['hits']/total_row['at_bats']
    total_row['on_base_percentage'] = (total_row['hits']+total_row['walks'])/total_row['plate_appearances']
    total_row['slugging_percentage'] = total_row['total_bases']/total_row['at_bats']
    total_row['on_base_plus_slugging'] = total_row['on_base_percentage']+total_row['slugging_percentage']
    total_ops_points = (df['ops_plus']*df['plate_appearances']).sum()
    #total_woba_points = (df['woba']*df['plate_appearances']).sum()
    total_wrc_points = (df['wrc_plus']*df['plate_appearances']).sum()
    total_pa = df['plate_appearances'].sum()
    total_row['wrc_plus'] = total_wrc_points/total_pa
    
    # Give the index a name like 'Career Total'
    total_row.index = ['Total']
    
    # Append it to the original DataFrame
    df_with_total = pd.concat([df, total_row])

    # 1. Define the styling function
    def highlight_total_row(row):
        # Check if the 'season' column for this row is exactly "Total"
        if row['season'] == "Total":
            # Apply a subtle gray tint with 20% opacity
            return ['background-color: rgba(128, 128, 128, 0.2)'] * len(row)
        else:
            # Return empty strings (no style) for other rows
            return [''] * len(row)
    
    styled_df = df_with_total.style.apply(highlight_total_row, axis=1)
    st.set_page_config(page_title=f"{selected_player}", layout="wide", page_icon="🥎")
    
    if not df.empty:
        # Displaying the high-level profile info
        st.header(f"{selected_player}")
        st.markdown(
            f"""**Position:** {df['position_long'].iloc[0]}  
            **DX Debut:** {df['dx_debut'].iloc[0]}"""
        )
        tab_stats, tab_game_log = st.tabs(["Stats", "Game Log"])
        with tab_stats:
            st.subheader(":green[Overview]")
            st.dataframe(
                styled_df,
                height="content",
                hide_index=True,
                placeholder="",
                column_order=[
                    "season","games_batting","plate_appearances","runs","home_runs","runs_batted_in","batting_average","on_base_percentage","slugging_percentage",
                    "on_base_plus_slugging","wrc_plus","wraa","defensive_run_value","wins_above_replacement"
                ],
                column_config={
                    "season": st.column_config.Column("Season", help="**Season**"),
                    "games_batting": st.column_config.NumberColumn("G", format="%d", help="**Games**"),
                    "plate_appearances": st.column_config.NumberColumn("PA", format="%d", help="**Plate Appearances**"),
                    "runs": st.column_config.NumberColumn("R", format="%d", help="**Runs Scored**"),
                    "home_runs": st.column_config.NumberColumn("HR", format="%d", help="**Home Runs**"),
                    "runs_batted_in": st.column_config.NumberColumn("RBI", format="%d", help="**Runs Batted In**"),
                    "batting_average": st.column_config.NumberColumn("AVG", format="%.3f", help="**Batting Average**"),
                    "on_base_percentage": st.column_config.NumberColumn("OBP", format="%.3f", help="**On-Base Percentage**"),
                    "slugging_percentage": st.column_config.NumberColumn("SLG", format="%.3f", help="**Slugging Percentage**"),
                    "on_base_plus_slugging": st.column_config.NumberColumn("OPS", format="%.3f", help="**On-Base Plus Slugging**"),
                    "wrc_plus": st.column_config.NumberColumn("WRC+", format="%.0f", help="**Adjusted Weighted Runs Created**"),
                    "wraa": st.column_config.NumberColumn("Bat", format="%.1f", help="**Batting Run Value**"),
                    "defensive_run_value": st.column_config.NumberColumn("Def", format="%.1f", help="**Defensive Run Value**"),
                    "wins_above_replacement": st.column_config.NumberColumn("WAR", format="%.1f", help="**Wins Above Replacement**")
                }
            )

        with tab_game_log:
            st.markdown("Coming soon")
            
    else:
        st.warning("No player found with that name.")
