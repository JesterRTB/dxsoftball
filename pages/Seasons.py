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

tab_season_overview, tab_schedule, tab_player_stats = st.tabs(["Season Overview", "Schedule", "Player Stats"])

with tab_season_overview:
    data_season_overview = get_table_data("dx_by_season")
    df_season_overview = pd.DataFrame(data_season_overview)
    st.dataframe(
        df_season_overview,
        hide_index=True,
        height="content",
        column_order=["season","games","wins","losses","ties","win_pct","player_runs","runs_allowed","pythag_win_pct","runs_per_plate_apperance","top_player"]
    )

with tab_schedule:
    st.write("Coming soon")

with tab_player_stats:
    st.write("Coming soon")
