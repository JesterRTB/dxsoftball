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
all_seasons = get_sorted_seasons()

tab_season_overview, tab_schedule, tab_player_stats = st.tabs(["Season Overview", "Schedule & Results", "Player Stats"])

with tab_season_overview:
    st.subheader(":green[D-Generation X Season Overview & Team Stats]")
    data_season_overview = get_table_data("dx_by_season")
    df_season_overview = pd.DataFrame(data_season_overview)

    # Calculations
    df_season_overview['strikeout_percentage'] = df_season_overview['strikeout_percentage']*100
    df_season_overview['walk_percentage'] = df_season_overview['walk_percentage']*100
    df_season_overview['extra_base_hit_percentage'] = df_season_overview['extra_base_hits']/df_season_overview['plate_appearances']*100
    df_season_overview['ra7'] = df_season_overview['runs_allowed']/df_season_overview['innings_pitched']*7
    df_season_overview['k7'] = df_season_overview['strikeouts_pitching']/df_season_overview['innings_pitched']*7
    
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
            column_order=["season","games","plate_appearances","runs_per_plate_appearance","walk_percentage","strikeout_percentage","extra_base_hit_percentage","batting_average","on_base_percentage",
                          "slugging_percentage","on_base_plus_slugging","isolated_power","batting_average_balls_in_play","team_calculated_war"],
            column_config={
                "season": st.column_config.Column("Season", pinned=True, help="**Season**"),
                "games": st.column_config.NumberColumn("G", format="%d", help="**Games**"),
                "plate_appearances": st.column_config.NumberColumn("PA", format="%d", help="**Plate Appearances**"),
                "runs_per_plate_appearance": st.column_config.NumberColumn("RPA", format="%.3f", help="**Runs Per Plate Appearance**"),
                "walk_percentage": st.column_config.NumberColumn("BB%", format="%.1f%%", help="**Walk Percentage**  \n=BB/PA"),
                "strikeout_percentage": st.column_config.NumberColumn("K%", format="%.1f%%", help="**Strikeout Percentage**  \n=SO/PA"),
                "extra_base_hit_percentage": st.column_config.NumberColumn("XBH%", format="%.1f%%", help="**Extra-Base Hit Percentage**  \n=(2B+3B+HR)/PA"),
                "batting_average": st.column_config.NumberColumn("AVG", format="%.3f", help="**Batting Average**  \n=H/AB"),
                "on_base_percentage": st.column_config.NumberColumn("OBP", format="%.3f", help="**On-Base Percentage**  \n=(H+BB)/PA"),
                "slugging_percentage": st.column_config.NumberColumn("SLG", format="%.3f", help="**Slugging Percentage**  \n=TB/AB"),
                "on_base_plus_slugging": st.column_config.NumberColumn("OPS", format="%.3f", help="**On-Base Plus Slugging Percentage**  \n=OBP+SLG"),
                "isolated_power": st.column_config.NumberColumn("ISO", format="%.3f", help="**Isolated Power**  \nSLG-AVG"),
                "batting_average_balls_in_play": st.column_config.NumberColumn("BABIP", format="%.3f", help="**Batting Average on Balls In Play**  \n(H-HR)/(AB-K-HR+SF)"),
                "team_calculated_war": st.column_config.NumberColumn("WAR", format="%.1f", help="**Wins Above Replacement**")
            }
        )

    with tab_team_pitching:
        st.dataframe(
            df_season_overview,
            hide_index=True,
            height="content",
            placeholder="",
            column_order=["season","games","innings_pitched","runs_allowed","strikeouts_pitching","ra7","k7","out_credit_pitching",
                          "putouts","assists","fielding_double_plays","out_credit_fielding"],
            column_config={
                "season": st.column_config.Column("Season", pinned=True, help="**Season**"),
                "games": st.column_config.NumberColumn("G", format="%d", help="**Games**"),
                "innings_pitched": st.column_config.NumberColumn("IP", format="%.1f", help="**Innings Pitched**"),
                "runs_allowed": st.column_config.NumberColumn("RA", format="%d", help="**Runs Allowed**"),
                "strikeouts_pitching": st.column_config.NumberColumn("K", format="%d", help="**Strikeouts**"),
                "ra7": st.column_config.NumberColumn("RA7", format="%.2f", help="**Runs Allowed per Seven Innings**  \n=RA/IPx7"),
                "k7": st.column_config.NumberColumn("K/7", format="%.2f", help="**Strikeouts per Seven Innings**  \n=K/IPx7"),
                "out_credit_pitching": st.column_config.NumberColumn("PC", format="%.1f", help="**Pitching Out Credit**  \nPitchers receive 0.1 for every out and an additional 0.9 for strikeouts"),
                "putouts": st.column_config.NumberColumn("PO", format="%d", help="**Putouts**"),
                "assists": st.column_config.NumberColumn("A", format="%d", help="**Assists**"),
                "fielding_double_plays": st.column_config.NumberColumn("DP", format="%d", help="**Double Plays**"),
                "out_credit_fielding": st.column_config.NumberColumn("FC", format="%.1f", help="**Fielding Out Credit**  \nPitchers receive 0.1 for all outs. The remaining 0.9 is split between all fielders who touch the ball leading to an out")
            }
        )

with tab_schedule:
    st.subheader(":green[D-Generation X Game-by-Game Schedule]")
    schedule_season = st.selectbox(
        "Select a season",
        all_seasons,
        index=0,
        label_visibility="collapsed",
        width=300
    )

    schedule_response = supabase.rpc("get_season_schedule", {
        "target_season": schedule_season 
    }).execute()

    df_schedule = pd.DataFrame(schedule_response.data)

    st.dataframe(
        df_schedule,
        height="content",
        hide_index=True,
        placeholder="",
        column_order=["game_id","game_date","game_time","opponent","win_loss","dx_score","opp_score","innings","player_of_the_game"],
        column_config={
            "game_id": st.column_config.NumberColumn("G#", format="%d", pinned=True, help="**Game Number**"),
            "game_date": st.column_config.DateColumn("Date", format="M/D/YY", help="**Game Date**"),
            "game_time": st.column_config.TimeColumn("Time", format="h:mm A", help="**Game Time**"),
            "opponent": st.column_config.Column("Opponent", help="**Opponent**"),
            "win_loss": st.column_config.Column("W-L", help="**Result**"),
            "dx_score": st.column_config.NumberColumn("R", format="%d", help="**Runs Scored**"),
            "opp_score": st.column_config.NumberColumn("RA", format="%d", help="**Runs Allowed**"),
            "innings": st.column_config.NumberColumn("Inn", format="%d", help="**Innings**"),
            "player_of_the_game": st.column_config.Column("Player of the Game", help="**Player of the Game**  \nPlayer with highest calculated run value for this game"),
        }
    )

with tab_player_stats:
    st.write("Coming soon")
