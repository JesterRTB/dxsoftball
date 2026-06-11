import streamlit as st
import pandas as pd
from Home import supabase
from utils import (
    create_row_highlighter,
    fetch_player_data,
    format_baseball_innings,
    get_all_players,
    get_player_seasons
)

# Set page configuration
st.set_page_config(page_title="D-X Player Search", layout="wide", page_icon="https://images.seeklogo.com/logo-png/27/1/d-generation-x-logo-png_seeklogo-275249.png")

# Fetch the list for the selectbox
players = get_all_players()
team_captain = "Mike Jang"
dx_logo = "https://images.seeklogo.com/logo-png/27/1/d-generation-x-logo-png_seeklogo-275249.png"

# Default search to team captain
default_index = players.index(team_captain) if team_captain in players else 0

selected_player = st.selectbox(
    "Select a player", 
    options=players,
    index=default_index,
    width=300,
    placeholder="Select a player",
    label_visibility="collapsed"
)

if selected_player:
    df = fetch_player_data(selected_player)
    avatar_url = df["avatar_url"].iloc[0] if "avatar_url" in df.columns else None
    if not avatar_url or pd.isna(avatar_url) or str(avatar_url).strip() in ["", "-", "None"]:
        avatar_url = dx_logo

    # Pull the jersey values from the dataframe first row safely
    jersey_name = df["jersey_name"].iloc[0] if "jersey_name" in df.columns else None
    jersey_number = df["jersey_number"].iloc[0] if "jersey_number" in df.columns else None
    
    # Check if BOTH jersey values exist and are valid before drawing the badge
    has_jersey_data = (
        pd.notna(jersey_name) and str(jersey_name).strip() not in ["", "-", "None"] and
        pd.notna(jersey_number) and str(jersey_number).strip() not in ["", "-", "None"]
    )
    
    captain_message = ":green[**TEAM CAPTAIN**]  \n" if selected_player == team_captain else ""

    exclude_seasons = ["Summer 2023", "Fall 2023", "Summer 2024", "Fall 2024"]
    excluded_games_count = df.loc[df['season'].isin(exclude_seasons), 'games_batting'].sum()

    # Calculations
    df['strikeout_percentage'] = df['strikeout_percentage'] * 100
    df['walk_percentage'] = df['walk_percentage'] * 100
    df['extra_base_hit_percentage'] = df['extra_base_hits'] / df['plate_appearances'] * 100
    df['range_factor'] = (df['putouts'] + df['assists']) / df['innings_defense'] * 7
    df['fielding_run_value_with_adjustment'] = df['fielding_run_value'] + df['designated_hitter_adjustment']
    df['runs_above_replacement'] = df['wraa'] + df['defensive_run_value'] + df['replacement_runs']
    df['games_fielding'] = df['games_batting']
    df['innings_pitcher'] = df['innings_pitched']
    df['pitching_run_value_per'] = df['pitching_run_value']
    
    # Create a total row for all columns
    total_row = df.sum(numeric_only=True).to_frame().T
    total_row['season'] = "Total"
    total_row['games_fielding'] = total_row['games_batting'] - excluded_games_count
    total_row['batting_average'] = total_row['hits'] / total_row['at_bats']
    total_row['on_base_percentage'] = (total_row['hits'] + total_row['walks']) / total_row['plate_appearances']
    total_row['slugging_percentage'] = total_row['total_bases'] / total_row['at_bats']
    total_row['on_base_plus_slugging'] = total_row['on_base_percentage'] + total_row['slugging_percentage']
    
    total_ops_points = (df['ops_plus'] * df['plate_appearances']).sum()
    total_woba_points = (df['woba'] * df['plate_appearances']).sum()
    total_wrc_points = (df['wrc_plus'] * df['plate_appearances']).sum()
    total_pa = df['plate_appearances'].sum()
    
    total_row['ops_plus'] = total_ops_points / total_pa
    total_row['woba'] = total_woba_points / total_pa
    total_row['wrc_plus'] = total_wrc_points / total_pa
    total_row['strikeout_percentage'] = total_row['strikeouts_batting'] / total_pa * 100
    total_row['walk_percentage'] = total_row['walks'] / total_pa * 100
    total_row['isolated_power'] = total_row['slugging_percentage'] - total_row['batting_average']
    total_row['batting_average_balls_in_play'] = (total_row['hits'] - total_row['home_runs']) / (total_row['at_bats'] - total_row['strikeouts_batting'] - total_row['home_runs'] + total_row['sacrifice_flies'])
    total_row['extra_base_hit_percentage'] = total_row['extra_base_hits'] / total_pa * 100
    total_row['runs_allowed_per_seven'] = total_row['runs_allowed'] / total_row['innings_pitched'] * 7
    total_row['strikeouts_per_seven'] = total_row['strikeouts_pitching'] / total_row['innings_pitched'] * 7
    total_row['range_factor'] = (total_row['putouts'] + total_row['assists']) / total_row['innings_defense'] * 7

    # Create a "Per 10 Games" row for all columns
    per_10_row = total_row.copy()
    per_10_row['season'] = "10 Game Avg"
    
    total_games = float(total_row['games_batting'].values[0])
    for col in per_10_row.columns:
        if col not in ['player','season']:
            per_10_row[col] = (per_10_row[col] / total_games) * 10 if total_games > 0 else 0

    # Alt "Per 10 Games" calculations
    per_10_row['batting_average'] = total_row['hits'] / total_row['at_bats']
    per_10_row['on_base_percentage'] = (total_row['hits'] + total_row['walks']) / total_row['plate_appearances']
    per_10_row['slugging_percentage'] = total_row['total_bases'] / total_row['at_bats']
    per_10_row['on_base_plus_slugging'] = total_row['on_base_percentage'] + total_row['slugging_percentage']
    per_10_row['wrc_plus'] = total_wrc_points / total_pa
    per_10_row['strikeout_percentage'] = total_row['strikeouts_batting'] / total_pa * 100
    per_10_row['walk_percentage'] = total_row['walks'] / total_pa * 100
    per_10_row['extra_base_hit_percentage'] = total_row['extra_base_hits'] / total_pa * 100
    per_10_row['ops_plus'] = total_ops_points / total_pa
    per_10_row['isolated_power'] = total_row['slugging_percentage'] - total_row['batting_average']
    per_10_row['batting_average_balls_in_play'] = (total_row['hits'] - total_row['home_runs']) / (total_row['at_bats'] - total_row['strikeouts_batting'] - total_row['home_runs'] + total_row['sacrifice_flies'])
    per_10_row['woba'] = total_woba_points / total_pa
    
    # Isolate scalar checking flags to handle legacy cohorts safely
    g_pitching = float(total_row['games_pitching'].values[0]) if 'games_pitching' in total_row.columns else 0
    g_fielding = float(total_row['games_fielding'].values[0]) if 'games_fielding' in total_row.columns else 0
    inn_pitched = float(total_row['innings_pitched'].values[0]) if 'innings_pitched' in total_row.columns else 0
    inn_defense = float(total_row['innings_defense'].values[0]) if 'innings_defense' in total_row.columns else 0

    per_10_row['games_pitching'] = 10 if g_pitching > 0 else 0
    per_10_row['games_fielding'] = 10 if g_fielding > 0 else 0

    # --- FORTIFIED LEGACY CALCULATIONS ---
    per_10_row['innings_pitched'] = (total_row['innings_pitched'] / g_pitching * 10) if g_pitching > 0 else 0
    per_10_row['runs_allowed'] = (total_row['runs_allowed'] / g_pitching * 10) if g_pitching > 0 else 0
    per_10_row['strikeouts_pitching'] = (total_row['strikeouts_pitching'] / g_pitching * 10) if g_pitching > 0 else 0
    per_10_row['runs_allowed_per_seven'] = (total_row['runs_allowed'] / inn_pitched * 7) if inn_pitched > 0 else 0
    per_10_row['strikeouts_per_seven'] = (total_row['strikeouts_pitching'] / inn_pitched * 7) if inn_pitched > 0 else 0
    per_10_row['out_credit_pitching'] = (total_row['out_credit_pitching'] / g_pitching * 10) if g_pitching > 0 else 0
    per_10_row['pitching_run_value'] = (total_row['pitching_run_value'] / g_pitching * 10) if g_pitching > 0 else 0
    
    per_10_row['defensive_run_value'] = (total_row['defensive_run_value'] / g_fielding * 10) if g_fielding > 0 else 0
    per_10_row['innings_defense'] = (total_row['innings_defense'] / g_fielding * 10) if g_fielding > 0 else 0
    per_10_row['innings_pitcher'] = (total_row['innings_pitcher'] / g_fielding * 10) if g_fielding > 0 else 0
    per_10_row['innings_catcher'] = (total_row['innings_catcher'] / g_fielding * 10) if g_fielding > 0 else 0
    per_10_row['innings_first_base'] = (total_row['innings_first_base'] / g_fielding * 10) if g_fielding > 0 else 0
    per_10_row['innings_second_base'] = (total_row['innings_second_base'] / g_fielding * 10) if g_fielding > 0 else 0
    per_10_row['innings_third_base'] = (total_row['innings_third_base'] / g_fielding * 10) if g_fielding > 0 else 0
    per_10_row['innings_shortstop'] = (total_row['innings_shortstop'] / g_fielding * 10) if g_fielding > 0 else 0
    per_10_row['innings_left_field'] = (total_row['innings_left_field'] / g_fielding * 10) if g_fielding > 0 else 0
    per_10_row['innings_left_center_field'] = (total_row['innings_left_center_field'] / g_fielding * 10) if g_fielding > 0 else 0
    per_10_row['innings_right_center_field'] = (total_row['innings_right_center_field'] / g_fielding * 10) if g_fielding > 0 else 0
    per_10_row['innings_right_field'] = (total_row['innings_right_field'] / g_fielding * 10) if g_fielding > 0 else 0
    per_10_row['innings_designated_hitter'] = (total_row['innings_designated_hitter'] / g_fielding * 10) if g_fielding > 0 else 0
    per_10_row['putouts'] = (total_row['putouts'] / g_fielding * 10) if g_fielding > 0 else 0
    per_10_row['assists'] = (total_row['assists'] / g_fielding * 10) if g_fielding > 0 else 0
    per_10_row['fielding_double_plays'] = (total_row['fielding_double_plays'] / g_fielding * 10) if g_fielding > 0 else 0
    per_10_row['out_credit_fielding'] = (total_row['out_credit_fielding'] / g_fielding * 10) if g_fielding > 0 else 0
    per_10_row['fielding_run_value'] = (total_row['fielding_run_value'] / g_fielding * 10) if g_fielding > 0 else 0
    per_10_row['designated_hitter_adjustment'] = (total_row['designated_hitter_adjustment'] / g_fielding * 10) if g_fielding > 0 else 0
    per_10_row['fielding_run_value_with_adjustment'] = (total_row['fielding_run_value_with_adjustment'] / g_fielding * 10) if g_fielding > 0 else 0
    per_10_row['range_factor'] = ((total_row['putouts'] + total_row['assists']) / inn_defense * 7) if inn_defense > 0 else 0
    per_10_row['pitching_run_value_per'] = (total_row['pitching_run_value'] / g_fielding * 10) if g_pitching > 0 else 0
    
    # Give the index unified names
    total_row.index = ['Total']
    per_10_row.index = ['10 Game Avg']
    
    # Combine safely using ignore_index
    df_with_total = pd.concat([df, total_row])
    df_with_avg = pd.concat([df_with_total, per_10_row], ignore_index=True)

    # Pitching dataframe branches off here
    pitching_mask = (df_with_avg['games_pitching'] > 0) | (df_with_avg['season'] == "Total")
    pitching_display_df = df_with_avg[pitching_mask]
    
    has_pitched = False
    if "Total" in pitching_display_df['season'].values:
        has_pitched = pitching_display_df.loc[pitching_display_df['season'] == 'Total', 'games_pitching'].values[0] > 0

    # Fielding dataframe branches off here
    fielding_mask = (~df_with_avg['season'].isin(exclude_seasons)) | (df_with_avg['season'] == "Total")
    fielding_display_df = df_with_avg[fielding_mask]
    
    has_fielding = False
    if "Total" in fielding_display_df['season'].values:
        has_fielding = fielding_display_df.loc[fielding_display_df['season'] == 'Total', 'innings_defense'].values[0] > 0
    
    # Styling pipelines using your shared utility closures
    styled_df = (
        df_with_avg.style
        .apply(create_row_highlighter(target_column="season", target_value="Total"), axis=1)
        .apply(create_row_highlighter(target_column="season", target_value="10 Game Avg"), axis=1)
    )
    
    styled_pitching_df = (
        pitching_display_df.style
        .apply(create_row_highlighter(target_column="season", target_value="Total"), axis=1)
        .apply(create_row_highlighter(target_column="season", target_value="10 Game Avg"), axis=1)
        .format({"innings_pitched": format_baseball_innings})
    )
    
    styled_fielding_df = (
        fielding_display_df.style
        .apply(create_row_highlighter(target_column="season", target_value="Total"), axis=1)
        .apply(create_row_highlighter(target_column="season", target_value="10 Game Avg"), axis=1)
        .format({
            "innings_pitcher": format_baseball_innings,
            "innings_defense": format_baseball_innings,
            "innings_catcher": format_baseball_innings,
            "innings_first_base": format_baseball_innings,
            "innings_second_base": format_baseball_innings,
            "innings_third_base": format_baseball_innings,
            "innings_shortstop": format_baseball_innings,
            "innings_left_field": format_baseball_innings,
            "innings_left_center_field": format_baseball_innings,
            "innings_right_center_field": format_baseball_innings,
            "innings_right_field": format_baseball_innings,
            "innings_designated_hitter": format_baseball_innings
        })
    )
    
    if not df.empty:
        # Reset page configuration
        st.set_page_config(page_title=f"{selected_player} D-X Profile & Stats", layout="wide", page_icon="https://images.seeklogo.com/logo-png/27/1/d-generation-x-logo-png_seeklogo-275249.png")

        col_image, col_bio = st.columns([0.2, 0.8], gap="medium")
        with col_image:
            st.image(avatar_url)

        with col_bio:
            st.header(f"{selected_player}")
            st.markdown(
                f"""{captain_message}**Position:** {df['position_long'].iloc[0]}  
                **DX Debut:** {df['dx_debut'].iloc[0]}"""
            )

            if has_jersey_data:
                # Flattened strings to prevent parse breaks
                box_style = "background-color: #111111; border: 2px solid #00FF00; border-radius: 8px; width: 160px; height: 100px; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; font-family: 'Arial Black', Impact, sans-serif;"
                name_style = "color: #FFFFFF; font-size: 12px; text-transform: uppercase; letter-spacing: 1px; padding: 0 4px; white-space: nowrap; width: 150px;"
                num_style = "color: #00FF00; font-size: 42px; line-height: 44px; margin-top: -2px;"
            
                # Assemble the HTML string
                jersey_badge_html = f'<div style="{box_style}"><div style="{name_style}">{jersey_name}</div><div style="{num_style}">{jersey_number}</div></div>'
                
                # Render the badge
                st.markdown(jersey_badge_html, unsafe_allow_html=True)
    
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
                    "season": st.column_config.Column("Season", pinned=True),
                    "games_batting": st.column_config.NumberColumn("G", format="%d"),
                    "plate_appearances": st.column_config.NumberColumn("PA", format="%d"),
                    "runs": st.column_config.NumberColumn("R", format="%d"),
                    "home_runs": st.column_config.NumberColumn("HR", format="%d"),
                    "runs_batted_in": st.column_config.NumberColumn("RBI", format="%d"),
                    "batting_average": st.column_config.NumberColumn("AVG", format="%.3f"),
                    "on_base_percentage": st.column_config.NumberColumn("OBP", format="%.3f"),
                    "slugging_percentage": st.column_config.NumberColumn("SLG", format="%.3f"),
                    "on_base_plus_slugging": st.column_config.NumberColumn("OPS", format="%.3f"),
                    "wrc_plus": st.column_config.NumberColumn("wRC+", format="%.0f"),
                    "wraa": st.column_config.NumberColumn("Bat", format="%.1f"),
                    "defensive_run_value": st.column_config.NumberColumn("Def", format="%.1f"),
                    "wins_above_replacement": st.column_config.NumberColumn("WAR", format="%.1f")
                }
            )

            st.write("")
            st.subheader(":green[Standard Batting]")
            st.dataframe(
                styled_df,
                height="content",
                hide_index=True,
                placeholder="",
                column_order=[
                    "season","games_batting","at_bats","plate_appearances","hits","singles","doubles","triples","home_runs","total_bases","runs","runs_batted_in",
                    "walks","strikeouts_batting","sacrifice_flies","batting_double_plays","batting_triple_plays","batting_average"
                ],
                column_config={
                    "season": st.column_config.Column("Season", pinned=True),
                    "games_batting": st.column_config.NumberColumn("G", format="%d"),
                    "at_bats": st.column_config.NumberColumn("AB", format="%d"),
                    "plate_appearances": st.column_config.NumberColumn("PA", format="%d"),
                    "hits": st.column_config.NumberColumn("H", format="%d"),
                    "singles": st.column_config.NumberColumn("1B", format="%d"),
                    "doubles": st.column_config.NumberColumn("2B", format="%d"),
                    "triples": st.column_config.NumberColumn("3B", format="%d"),
                    "home_runs": st.column_config.NumberColumn("HR", format="%d"),
                    "total_bases": st.column_config.NumberColumn("TB", format="%d"),
                    "runs": st.column_config.NumberColumn("R", format="%d"),
                    "runs_batted_in": st.column_config.NumberColumn("RBI", format="%d"),
                    "walks": st.column_config.NumberColumn("BB", format="%d"),
                    "strikeouts_batting": st.column_config.NumberColumn("SO", format="%d"),
                    "sacrifice_flies": st.column_config.NumberColumn("SF", format="%d"),
                    "batting_double_plays": st.column_config.NumberColumn("HIDP", format="%d"),
                    "batting_triple_plays": st.column_config.NumberColumn("HITP", format="%d"),
                    "batting_average": st.column_config.NumberColumn("AVG", format="%.3f")
                }
            )

            st.write("")
            st.subheader(":green[Advanced Batting]")
            st.dataframe(
                styled_df,
                height="content",
                hide_index=True,
                placeholder="",
                column_order=[
                    "season","plate_appearances","walk_percentage","strikeout_percentage","extra_base_hit_percentage","batting_average","on_base_percentage","slugging_percentage",
                    "on_base_plus_slugging","ops_plus","isolated_power","batting_average_balls_in_play","wrc","wraa","woba","wrc_plus"
                ],
                column_config={
                    "season": st.column_config.Column("Season", pinned=True),
                    "plate_appearances": st.column_config.NumberColumn("PA", format="%d"),
                    "walk_percentage": st.column_config.NumberColumn("BB%", format="%.1f%%"),
                    "strikeout_percentage": st.column_config.NumberColumn("K%", format="%.1f%%"),
                    "extra_base_hit_percentage": st.column_config.NumberColumn("XBH%", format="%.1f%%"),
                    "batting_average": st.column_config.NumberColumn("AVG", format="%.3f"),
                    "on_base_percentage": st.column_config.NumberColumn("OBP", format="%.3f"),
                    "slugging_percentage": st.column_config.NumberColumn("SLG", format="%.3f"),
                    "on_base_plus_slugging": st.column_config.NumberColumn("OPS", format="%.3f"),
                    "ops_plus": st.column_config.NumberColumn("OPS+", format="%.0f"),
                    "isolated_power": st.column_config.NumberColumn("ISO", format="%.3f"),
                    "batting_average_balls_in_play": st.column_config.NumberColumn("BABIP", format="%.3f"),
                    "wrc": st.column_config.NumberColumn("wRC", format="%.0f"),
                    "wraa": st.column_config.NumberColumn("wRAA", format="%.1f"),
                    "woba": st.column_config.NumberColumn("wOBA", format="%.3f"),
                    "wrc_plus": st.column_config.NumberColumn("wRC+", format="%.0f")
                }
            )

            if has_pitched:
                st.write("")
                st.subheader(":green[Pitching]", help="Pitching stats tracked since Summer 2025")
                st.dataframe(
                    styled_pitching_df,
                    height="content",
                    hide_index=True,
                    placeholder="",
                    column_order=["season","games_pitching","innings_pitched","runs_allowed","strikeouts_pitching","runs_allowed_per_seven","strikeouts_per_seven","out_credit_pitching","pitching_run_value"],
                    column_config={
                        "season": st.column_config.Column("Season", pinned=True),
                        "games_pitching": st.column_config.NumberColumn("G", format="%d"),
                        "innings_pitched": st.column_config.NumberColumn("IP"),
                        "runs_allowed": st.column_config.NumberColumn("RA", format="%d"),
                        "strikeouts_pitching": st.column_config.NumberColumn("K", format="%d"),
                        "runs_allowed_per_seven": st.column_config.NumberColumn("RA7", format="%.2f"),
                        "strikeouts_per_seven": st.column_config.NumberColumn("K/7", format="%.2f"),
                        "out_credit_pitching": st.column_config.NumberColumn("PC", format="%.1f"),
                        "pitching_run_value": st.column_config.NumberColumn("PRV", format="%.1f", help="**Pitching Run Value**")
                    }
                )
                
            if has_fielding:
                st.write("")
                st.subheader(":green[Fielding]", help="Fielding stats tracked since Summer 2025")
                st.dataframe(
                    styled_fielding_df,
                    height="content",
                    hide_index=True,
                    placeholder="",
                    column_order=[
                        "season","games_fielding","innings_defense","innings_pitcher","innings_catcher","innings_first_base","innings_second_base","innings_third_base","innings_shortstop","innings_left_field",
                        "innings_left_center_field","innings_right_center_field","innings_right_field","innings_designated_hitter","putouts","assists","fielding_double_plays","range_factor","out_credit_fielding",
                        "fielding_run_value"
                    ],
                    column_config={
                        "season": st.column_config.Column("Season", pinned=True, help="**Season**"),
                        "games_fielding": st.column_config.NumberColumn("G", format="%d", help="**Defensive Games Played**  \nPitching and fielding stats tracked since Summer 2025"),
                        "innings_defense": st.column_config.NumberColumn("Inn", help="**Defensive Innings Played**"),
                        "innings_pitcher": st.column_config.NumberColumn("P", help="**Innings Played as Pitcher**"),
                        "innings_catcher": st.column_config.NumberColumn("C", help="**Innings Played as Catcher**"),
                        "innings_first_base": st.column_config.NumberColumn("1B", help="**Innings Played as First Baseman**"),
                        "innings_second_base": st.column_config.NumberColumn("2B", help="**Innings Played as Second Baseman**"),
                        "innings_third_base": st.column_config.NumberColumn("3B", help="**Innings Played as Third Baseman**"),
                        "innings_shortstop": st.column_config.NumberColumn("SS", help="**Innings Played as Shortstop**"),
                        "innings_left_field": st.column_config.NumberColumn("LF", help="**Innings Played as Leftfielder**"),
                        "innings_left_center_field": st.column_config.NumberColumn("LC", help="**Innings Played as Left Centerfielder**"),
                        "innings_right_center_field": st.column_config.NumberColumn("RC", help="**Innings Played as Right Centerfielder**"),
                        "innings_right_field": st.column_config.NumberColumn("RF", help="**Innings Played as Rightfielder**"),
                        "innings_designated_hitter": st.column_config.NumberColumn("DH", help="**Innings Played as Designated Hitter**"),
                        "putouts": st.column_config.NumberColumn("PO", format="%d"),
                        "assists": st.column_config.NumberColumn("A", format="%d"),
                        "fielding_double_plays": st.column_config.NumberColumn("DP", format="%d"),
                        "range_factor": st.column_config.NumberColumn("RF/7", format="%.2f"),
                        "out_credit_fielding": st.column_config.NumberColumn("FC", format="%.1f"),
                        "fielding_run_value": st.column_config.NumberColumn("FRV", format="%.1f", help="**Fielding Run Value**  \nCompared to the team average given an equal amount of defensive innings played")
                    }
                )

            st.write("")
            st.subheader(":green[Value]")
            st.dataframe(
                styled_df,
                height="content",
                hide_index=True,
                placeholder="",
                column_order=["season","wraa","pitching_run_value_per","fielding_run_value","designated_hitter_adjustment","defensive_run_value","replacement_runs","runs_above_replacement","wins_above_replacement"],
                column_config={
                    "season": st.column_config.Column("Season", pinned=True),
                    "wraa": st.column_config.NumberColumn("Batting", format="%.1f"),
                    "pitching_run_value_per": st.column_config.NumberColumn("Pitching", format="%.1f"),
                    "fielding_run_value": st.column_config.NumberColumn("Fielding", format="%.1f"),
                    "designated_hitter_adjustment": st.column_config.NumberColumn("Positional", format="%.1f", help="**Positional Adjustment**"),
                    "defensive_run_value": st.column_config.NumberColumn("Defense", format="%.1f", help="**Defensive Run Value**  \n=Pitching+Fielding+Positional"),
                    "replacement_runs": st.column_config.NumberColumn("Replacement", format="%.1f"),
                    "runs_above_replacement": st.column_config.NumberColumn("RAR", format="%.1f", help="**Runs Above Replacement**  \n=Batting+Defense+Replacement"),
                    "wins_above_replacement": st.column_config.NumberColumn("WAR", format="%.1f")
                }
            )

        with tab_game_log:
            player_seasons = get_player_seasons(selected_player)
            selected_player_season = st.selectbox(
                "Select a season", 
                options=player_seasons,
                index=0,
                width=300,
                placeholder="Select a season",
                label_visibility="collapsed"
            )

            res_game_log = supabase.rpc("get_player_game_log", {
                "target_player": selected_player,
                "target_season": selected_player_season
            }).execute()

            game_log_df = pd.DataFrame(res_game_log.data)

            tab_gl_batting, tab_gl_fielding, tab_gl_pitching = st.tabs(["Batting","Fielding","Piching"])

            with tab_gl_batting:
                st.dataframe(
                    game_log_df,
                    height="content",
                    hide_index=True,
                    placeholder="",
                    column_order=[
                        "date","opponent","bat_order","plate_appearances","hits","doubles","triples","home_runs","runs","runs_batted_in","walks",
                        "strikeouts_batting","batting_average","on_base_percentage","slugging_percentage","on_base_plus_slugging",
                        "total_bases","sacrifice_flies","batting_double_plays","wrc","wrc_plus"
                    ],
                    column_config={
                        "date": st.column_config.Column("Date", pinned=True),
                        "opponent": st.column_config.Column("Opponent"),
                        "bat_order": st.column_config.NumberColumn("BO", alignment="left", format="%.0f"),
                        "plate_appearances": st.column_config.NumberColumn("PA", format="%d"),
                        "hits": st.column_config.NumberColumn("H", format="%d"),
                        "doubles": st.column_config.NumberColumn("2B", format="%d"),
                        "triples": st.column_config.NumberColumn("3B", format="%d"),
                        "home_runs": st.column_config.NumberColumn("HR", format="%d"),
                        "runs": st.column_config.NumberColumn("R", format="%d"),
                        "runs_batted_in": st.column_config.NumberColumn("RBI", format="%d"),
                        "walks": st.column_config.NumberColumn("BB", format="%d"),
                        "strikeouts_batting": st.column_config.NumberColumn("SO", format="%d"),
                        "batting_average": st.column_config.NumberColumn("AVG", format="%.3f"),
                        "on_base_percentage": st.column_config.NumberColumn("OBP", format="%.3f"),
                        "slugging_percentage": st.column_config.NumberColumn("SLG", format="%.3f"),
                        "on_base_plus_slugging": st.column_config.NumberColumn("OPS", format="%.3f"),
                        "total_bases": st.column_config.NumberColumn("TB", format="%d"),
                        "sacrifice_flies": st.column_config.NumberColumn("SF", format="%d"),
                        "batting_double_plays": st.column_config.NumberColumn("HIDP", format="%d"),
                        "wrc": st.column_config.NumberColumn("wRC", format="%.0f"),
                        "wrc_plus": st.column_config.NumberColumn("wRC+", format="%.0f")
                    }
                )

            with tab_gl_fielding:
                st.dataframe(
                    game_log_df,
                    height="content",
                    hide_index=True,
                    placeholder="",
                    column_order=[
                        "date","opponent","position_played","innings_defense","putouts","assists","fielding_double_plays","out_credit_fielding"
                    ],
                    column_config={
                        "date": st.column_config.Column("Date", pinned=True),
                        "opponent": st.column_config.Column("Opponent"),
                        "position_played": st.column_config.Column("Pos"),
                        "innings_defense": st.column_config.NumberColumn("Inn", format="%.1f"),
                        "putouts": st.column_config.NumberColumn("PO", format="%d"),
                        "assists": st.column_config.NumberColumn("A", format="%d"),
                        "fielding_double_plays": st.column_config.NumberColumn("DP", format="%d"),
                        "out_credit_fielding": st.column_config.NumberColumn("FC", format="%.1f")
                    }
                )

            with tab_gl_pitching:
                st.write("Pitching Stats coming soon")
            
    else:
        st.warning("No player found with that name.")
