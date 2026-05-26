import streamlit as st
import pandas as pd
from Home import supabase
from utils import (
    fetch_player_data,
    get_all_players,
    get_player_seasons,
    get_sorted_seasons,
    get_table_data
)

st.set_page_config(page_title="D-X Seasons", layout="wide", page_icon="https://images.seeklogo.com/logo-png/27/1/d-generation-x-logo-png_seeklogo-275249.png")

st.header("D-Generation X History")
st.write("**Team Captain:** Mike Jang")

tab_season_overview, tab_schedule, tab_player_stats = st.tabs(["Season Overview", "Schedule & Results", "Player Stats"])

with tab_season_overview:
    data_season_overview = get_table_data("dx_by_season")
    df_season_overview = pd.DataFrame(data_season_overview)
    st.dataframe(
        df_season_overview,
        hide_index=True,
        height="content",
        placeholder="",
        column_order=["season","games","wins","losses","ties","win_pct","player_runs","runs_allowed","pythag_win_pct","runs_per_plate_appearance","top_player"],
        column_config={
            "season": st.column_config.Column("Season", pinned=True, help="**Season**"),
            "games": st.column_config.NumberColumn("G", format="%d", help="**Games**"),
            "wins": st.column_config.NumberColumn("W", format="%d", help="**Wins**"),
            "losses": st.column_config.NumberColumn("L", format="%d", help="**Losses**"),
            "ties": st.column_config.NumberColumn("T", format="%d", help="**Ties**"),
            "win_pct": st.column_config.NumberColumn("W-L%", format="%.3f", help="**Win Percentage**"),
            "player_runs": st.column_config.NumberColumn("R", format="%d", help="**Runs Scored**"),
            "runs_allowed": st.column_config.NumberColumn("RA", format="%d", help="**Runs Allowed**"),
            "pythag_win_pct": st.column_config.NumberColumn("pythW-L%", format="%.3f", help="**Pythagorean Win Percentage**  \nExpected win percentage based on run differential  \n=R^2/(R^2+RA^2)"),
            "runs_per_plate_appearance": st.column_config.NumberColumn("RPA", format="%.3f", help="**Runs Per Plate Appearance**"),
            "top_player": st.column_config.Column("Top Player", help="**Top Player**  \nTeam leader for this season in Wins Above Replacement")
        }
    )

with tab_schedule:
    st.write("Coming soon")

with tab_player_stats:
    st.write("Coming soon")
