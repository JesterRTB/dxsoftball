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
    st.subheader(":green[D-Generation X Season Overview & Team Stats]")
    data_season_overview = get_table_data("dx_by_season")
    df_season_overview = pd.DataFrame(data_season_overview)
    tab_overview, tab_team_standard_batting, tab_team_advanced_batting, tab_team_pitching = st.tabs(["Overview", "Team Standard Batting", "Team Advanced Batting", "Team Pitching & Fielding"])
    
    with tab_overview:
        st.dataframe(
            df_season_overview,
            hide_index=True,
            height="content",
            placeholder="",
            column_order=["season","games","wins","losses","ties","win_pct","player_runs","runs_allowed","pythag_win_pct","top_player"],
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
                "top_player": st.column_config.Column("Top Player", help="**Top Player**  \nTeam leader for this season in Wins Above Replacement")
            }
        )

    with tab_team_standard_batting:
        st.dataframe(
            df_season_overview,
            hide_index=True,
            height="content",
            placeholder="",
            column_order=["season","games","at_bats","plate_appearances","hits","singles","doubles","triples","home_runs","total_bases","player_runs","runs_batted_in","walks","strikeouts_batting",
                         "sacrifice_flies","batting_double_plays","batting_triple_plays","batting_average"],
            column_config={
                "season": st.column_config.Column("Season", pinned=True, help="**Season**"),
                "games": st.column_config.NumberColumn("G", format="%d", help="**Games**"),
                "at_bats": st.column_config.NumberColumn("AB", format="%d", help="**At-Bats**"),
                "plate_appearances": st.column_config.NumberColumn("PA", format="%d", help="**Plate Appearances**"),
                "hits": st.column_config.NumberColumn("H", format="%d", help="**Hits**"),
                "singles": st.column_config.NumberColumn("1B", format="%d", help="**Singles**"),
                "doubles": st.column_config.NumberColumn("2B", format="%d", help="**Doubles**"),
                "triples": st.column_config.NumberColumn("3B", format="%d", help="**Triples**"),
                "home_runs": st.column_config.NumberColumn("HR", format="%d", help="**Home Runs**"),
                "total_bases": st.column_config.NumberColumn("TB", format="%d", help="**Total Bases**  \n=1B+2x2B+3x3B+4xHR"),
                "player_runs": st.column_config.NumberColumn("R", format="%d", help="**Runs Scored**"),
                "runs_batted_in": st.column_config.NumberColumn("RBI", format="%d", help="**Runs Batted In**"),
                "walks": st.column_config.NumberColumn("BB", format="%d", help="**Bases on Balls / Walks**"),
                "strikeouts_batting": st.column_config.NumberColumn("SO", format="%d", help="**Strikeouts**  \nIncludes foul outs"),
                "sacrifice_flies": st.column_config.NumberColumn("SF", format="%d", help="**Sacrifice Flies**"),
                "batting_double_plays": st.column_config.NumberColumn("HIDP", format="%d", help="**Hit Into Double Play**"),
                "batting_triple_plays": st.column_config.NumberColumn("HITP", format="%d", help="**Hit Into Triple Play**"),
                "batting_average": st.column_config.NumberColumn("AVG", format="%.3f", help="**Batting Average**")
            }
        )

    with tab_team_advanced_batting:
        st.dataframe(
            df_season_overview,
            hide_index=True,
            height="content",
            placeholder="",
            column_order=["season","runs_per_plate_appearance","games",],
            column_config={
                "season": st.column_config.Column("Season", pinned=True, help="**Season**"),
                "runs_per_plate_appearance": st.column_config.NumberColumn("RPA", format="%.3f", help="**Runs Per Plate Appearance**"),
                "games": st.column_config.NumberColumn("G", format="%d", help="**Games**"),
            }
        )

with tab_schedule:
    st.write("Coming soon")

with tab_player_stats:
    st.write("Coming soon")
