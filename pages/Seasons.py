import streamlit as st
import pandas as pd
from Home import supabase
from utils import (
    create_row_highlighter,
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

st.divider()
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

st.divider()
st.subheader(":green[D-Generation X Records by Season]")
schedule_season = st.selectbox(
        "Select a season",
        all_seasons,
        index=0,
        label_visibility="collapsed",
        width=300
    )

tab_schedule, tab_box_scores, tab_player_stats = st.tabs(["Schedule & Results", "Box Scores", "Player Stats"])

with tab_schedule:
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

with tab_box_scores:
    # Format game date for selectbox
    df_schedule['formatted_date'] = pd.to_datetime(df_schedule['game_date']).dt.strftime('%-m/%-d/%y')

    # Build a helper dictionary mapping game_id -> "game_id. game_date vs opponent"
    game_options_map = {
        row['game_id']: f"G#{row['game_id']} - {row['formatted_date']} vs {row['opponent']}"
        for _, row in df_schedule.iterrows()
    }

    # Create the detailed Game Selectbox
    selected_game_id = st.selectbox(
        "Select a game to view box score",
        options=list(game_options_map.keys()),
        format_func=lambda x: game_options_map[x],
        index=len(game_options_map)-1,
        label_visibility="collapsed",
        width=400,
        key="game_id_selector"
    )

    # Query and Render Box Score
    box_response = supabase.rpc("get_box_score", {
        "target_season": schedule_season,
        "target_game_id": int(selected_game_id)
    }).execute()

    # Declare df
    df_box = pd.DataFrame(box_response.data)

    # Declare total row
    total_row_box = pd.DataFrame(index=[0], columns=df_box.columns)

    # Compute numeric sums
    numeric_sums = df_box.sum(numeric_only=True)
    for col in numeric_sums.index:
        total_row_box[col] = numeric_sums[col]

    # Fill non-numeric cells with empty string
    total_row_box = total_row_box.fillna("")

    # Create new columns for total row
    total_row_box['player'] = "Total"
    total_row_box['player_position'] = ""
    total_row_box['batting_average'] = total_row_box['hits']/total_row_box['at_bats']
    total_row_box['on_base_plus_slugging'] = (total_row_box['hits']+total_row_box['walks'])/total_row_box['plate_appearances'] + total_row_box['total_bases']/total_row_box['at_bats']
    total_box_woba_points = (df_box['woba']*df_box['plate_appearances']).sum()
    total_row_box['woba'] = total_box_woba_points/total_row_box['plate_appearances']

    # Append total row to df
    df_box_with_total = pd.concat([df_box, total_row_box], ignore_index=True)

    # Style the total row
    styled_df_box = df_box_with_total.style.apply(
        create_row_highlighter(target_column="player", target_value="Total"),
        axis=1
    )

    # 1. Isolate game-level metadata from the first row of your box score data
    game_meta = df_box.iloc[0]
    
    # Determine team names based on who is Home and Away
    if game_meta["side"] == "Away":
        away_team = "D-Generation X"
        home_team = str(game_meta["opponent"])
    else:
        away_team = str(game_meta["opponent"])
        home_team = "D-Generation X"

    # 2. Dynamically gather scores for played innings (filtering out any unplayed/null innings)
    num_innings = int(game_meta["innings"])
    
    # Cap standard tracking loop at a maximum of 9 or the actual extra-inning length
    loop_innings = max(9, num_innings)
    
    line_score_data = []
    for team_prefix, team_name, total_key in [("away_", away_team, "opp_score" if game_meta["side"] == "Home" else "dx_score"), 
                                              ("home_", home_team, "dx_score" if game_meta["side"] == "Home" else "opp_score")]:
        
        row_dict = {"Team": team_name}
        
        # Build individual inning scores
        for i in range(1, loop_innings + 1):
            score_val = game_meta.get(f"{team_prefix}{i}_score")
            
            # If the inning wasn't played, leave it clean/blank. 
            # Handle the bottom of the 9th walk-off exception ("X") safely if values are null.
            if pd.isna(score_val) or score_val == "" or i > num_innings:
                row_dict[str(i)] = "-" if i <= num_innings else ""
            else:
                row_dict[str(i)] = str(int(score_val))
                
        # Append the final calculated game total column
        row_dict["R"] = int(game_meta[total_key])
        line_score_data.append(row_dict)

    df_line_score = pd.DataFrame(line_score_data)

    # 3. Render the Scoreboard Header UI Grid
    st.write("### 🔢 Linescore")
    
    # Establish scannable column layouts for the grid columns
    linescore_orders = ["Team"] + [str(i) for i in range(1, loop_innings + 1)] + ["R"]
    linescore_config = {str(i): st.column_config.Column(width="small", alignment="center") for i in range(1, loop_innings + 1)}
    linescore_config["Team"] = st.column_config.Column(pinned=True, width="medium")
    linescore_config["R"] = st.column_config.NumberColumn("R", format="%d", width="small", alignment="center", pinned=False)

    st.dataframe(
        df_line_score,
        column_order=linescore_orders,
        column_config=linescore_config,
        hide_index=True,
        height=110, # Keeps the vertical box tightly packed
        use_container_width=False
    )
    
    st.caption(f"📍 **Ballpark:** {game_meta['ballpark']} — {game_meta['city']}, {game_meta['state']}")
    st.divider()

    tab_box_score_batting, tab_box_score_pitching = st.tabs(["Batting", "Pitching & Fielding"])

    with tab_box_score_batting:
        st.dataframe(
            styled_df_box,
            height="content",
            hide_index=True,
            placeholder="",
            column_order=[
                "player","player_position","runs","at_bats","hits","doubles","triples","home_runs","runs_batted_in","walks","strikeouts_batting","sacrifice_flies",
                "batting_double_plays","batting_average","on_base_plus_slugging","woba"
            ],
            column_config={
                "player": st.column_config.Column("Player", help="**Player**"),
                "player_position": st.column_config.Column("Pos", help="**Position(s) Played**"),
                "runs": st.column_config.NumberColumn("R", format="%d", help="**Runs Scored**"),
                "at_bats": st.column_config.NumberColumn("AB", format="%d", help="**At-Bats**"),
                "hits": st.column_config.NumberColumn("H", format="%d", help="**Hits**"),
                "doubles": st.column_config.NumberColumn("2B", format="%d", help="**Doubles**"),
                "triples": st.column_config.NumberColumn("3B", format="%d", help="**Triples**"),
                "home_runs": st.column_config.NumberColumn("HR", format="%d", help="**Home Runs**"),
                "runs_batted_in": st.column_config.NumberColumn("RBI", format="%d", help="**Runs Batted In**"),
                "walks": st.column_config.NumberColumn("BB", format="%d", help="**Bases on Balls / Walks**"),
                "strikeouts_batting": st.column_config.NumberColumn("SO", format="%d", help="**Strikeouts**  \nIncludes foul outs"),
                "sacrifice_flies": st.column_config.NumberColumn("SF", format="%d", help="**Sacrifice Flies**"),
                "batting_double_plays": st.column_config.NumberColumn("HIDP", format="%d", help="**Hit Into Double Plays**"),
                "batting_average": st.column_config.NumberColumn("AVG", format="%.3f", help="**Batting Average**  \nH/AB"),
                "on_base_plus_slugging": st.column_config.NumberColumn("OPS", format="%.3f", help="**On-Base Plus Slugging**  \nOBP+SLG"),
                "woba": st.column_config.NumberColumn("wOBA", format="%.3f", help="**Weighted On-Base Average**")
            }
        )

    with tab_box_score_pitching:
        st.dataframe(
            styled_df_box,
            height="content",
            hide_index=True,
            placeholder="",
            column_order=[
                "player","player_position","innings_pitched","runs_allowed","strikeouts_pitching",
                "innings_defense","putouts","assists","fielding_double_plays"
            ],
            column_config={
                "player": st.column_config.Column("Player", help="**Player**"),
                "player_position": st.column_config.Column("Pos", help="**Position(s) Played**"),
                "innings_pitched": st.column_config.NumberColumn("IP", format="%.1f", help="**Innings Pitched**"),
                "runs_allowed": st.column_config.NumberColumn("RA", format="%d", help="**Runs Allowed**"),
                "strikeouts_pitching": st.column_config.NumberColumn("K", format="%d", help="**Strikeouts**"),
                "innings_defense": st.column_config.NumberColumn("Inn", format="%.1f", help="**Defensive Innings Played**"),
                "putouts": st.column_config.NumberColumn("PO", format="%d", help="**Putouts**"),
                "assists": st.column_config.NumberColumn("A", format="%d", help="**Assists**"),
                "fielding_double_plays": st.column_config.NumberColumn("DP", format="%d", help="**Double Plays Turned**"),
            }
        )

with tab_player_stats:
    stats_response = supabase.rpc("get_leaderboard", {
        "start_season": schedule_season, 
        "end_season": schedule_season
    }).execute()
    
    df_stats = pd.DataFrame(stats_response.data)

    # Calculations
    df_stats['strikeout_percentage'] = df_stats['strikeout_percentage']*100
    df_stats['walk_percentage'] = df_stats['walk_percentage']*100
    df_stats['extra_base_hit_percentage'] = df_stats['extra_base_hits']/df_stats['plate_appearances']*100
    df_stats['range_factor'] = (df_stats['putouts']+df_stats['assists'])/df_stats['innings_defense']*7
    df_stats['fielding_run_value_with_adjustment'] = df_stats['fielding_run_value']+df_stats['designated_hitter_adjustment']
    df_stats['runs_above_replacement'] = df_stats['wraa']+df_stats['defensive_run_value']+df_stats['replacement_runs']

    tab_stats_overview, tab_stats_standard_batting, tab_stats_advanced_batting, tab_stats_pitching, tab_stats_fielding, tab_stats_value = st.tabs(["Overview", "Standard Batting", "Advanced Batting", "Pitching", "Fielding", "Value"])

    with tab_stats_overview:
        df_stats = df_stats.sort_values(by="wins_above_replacement", ascending=False)
        st.dataframe(
                df_stats,
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
                    "wrc_plus": st.column_config.NumberColumn("wRC+", format="%.0f", help="**Adjusted Weighted Runs Created Plus** \nWeighted Runs Created represented as a rate statistic and adjusted to the team's overall offensive performance  \n100 is team-average, higher is better"),
                    "wraa": st.column_config.NumberColumn("Bat", format="%.1f", help="**Batting Run Value**  \nCompared to the team average given an equal amount of plate appearances"),
                    "defensive_run_value": st.column_config.NumberColumn("Def", format="%.1f", help="**Defensive Run Value**  \nCompared to the team average given an equal amount of defensive innings  \nAlso includes DH Adjustment"),
                    "wins_above_replacement": st.column_config.NumberColumn("WAR", format="%.1f", help="**Wins Above Replacement**")
                }
            )
        
        with tab_stats_standard_batting:
            df_stats = df_stats.sort_values(by="batting_average", ascending=False)
            st.dataframe(
                df_stats,
                height="content",
                hide_index=True,
                placeholder="",
                column_order=[
                    "player","games_batting","at_bats","plate_appearances","hits","singles","doubles","triples","home_runs","total_bases","runs","runs_batted_in",
                    "walks","strikeouts_batting","sacrifice_flies","batting_double_plays","batting_triple_plays","batting_average"
                ],
                column_config={
                    "player": st.column_config.Column("Player", help="**Player**"),
                    "games_batting": st.column_config.NumberColumn("G", format="%d", help="**Games**"),
                    "at_bats": st.column_config.NumberColumn("AB", format="%d", help="**At-Bats**"),
                    "plate_appearances": st.column_config.NumberColumn("PA", format="%d", help="**Plate Appearances**"),
                    "hits": st.column_config.NumberColumn("H", format="%d", help="**Hits**"),
                    "singles": st.column_config.NumberColumn("1B", format="%d", help="**Singles**"),
                    "doubles": st.column_config.NumberColumn("2B", format="%d", help="**Doubles**"),
                    "triples": st.column_config.NumberColumn("3B", format="%d", help="**Triples**"),
                    "home_runs": st.column_config.NumberColumn("HR", format="%d", help="**Home Runs**"),
                    "total_bases": st.column_config.NumberColumn("TB", format="%d", help="**Total Bases**"),
                    "runs": st.column_config.NumberColumn("R", format="%d", help="**Runs Scored**"),
                    "runs_batted_in": st.column_config.NumberColumn("RBI", format="%d", help="**Runs Batted In**"),
                    "walks": st.column_config.NumberColumn("BB", format="%d", help="**Bases on Balls / Walks**"),
                    "strikeouts_batting": st.column_config.NumberColumn("SO", format="%d", help="**Strikeouts**  \nIncludes foul outs"),
                    "sacrifice_flies": st.column_config.NumberColumn("SF", format="%d", help="**Sacrifice Flies**"),
                    "batting_double_plays": st.column_config.NumberColumn("HIDP", format="%d", help="**Hit Into Double Plays**"),
                    "batting_triple_plays": st.column_config.NumberColumn("HITP", format="%d", help="**Hit Into Triple Plays**"),
                    "batting_average": st.column_config.NumberColumn("AVG", format="%.3f", help="**Batting Average**  \nH/AB")
                }
            )

        with tab_stats_advanced_batting:
            df_stats = df_stats.sort_values(by="wrc_plus", ascending=False)
            st.dataframe(
                df_stats,
                height="content",
                hide_index=True,
                placeholder="",
                column_order=[
                    "player","plate_appearances","walk_percentage","strikeout_percentage","extra_base_hit_percentage","batting_average","on_base_percentage","slugging_percentage",
                    "on_base_plus_slugging","ops_plus","isolated_power","batting_average_balls_in_play","wrc","wraa","woba","wrc_plus"
                ],
                column_config={
                    "player": st.column_config.Column("Player", help="**Player**"),
                    "plate_appearances": st.column_config.NumberColumn("PA", format="%d", help="**Plate Appearances**"),
                    "walk_percentage": st.column_config.NumberColumn("BB%", format="%.1f%%", help="**Walk Percentage**  \nBB/PA"),
                    "strikeout_percentage": st.column_config.NumberColumn("K%", format="%.1f%%", help="**Strikeout Percentage**  \nK/PA  \nIncludes foul outs"),
                    "extra_base_hit_percentage": st.column_config.NumberColumn("XBH%", format="%.1f%%", help="**Extra-Base Hit Percentage**  \n(2B+3B+HR)/PA"),
                    "batting_average": st.column_config.NumberColumn("AVG", format="%.3f", help="**Batting Average**  \nH/AB"),
                    "on_base_percentage": st.column_config.NumberColumn("OBP", format="%.3f", help="**On-Base Percentage**  \n(H+BB)/PA"),
                    "slugging_percentage": st.column_config.NumberColumn("SLG", format="%.3f", help="**Slugging Percentage**  \nTB/AB"),
                    "on_base_plus_slugging": st.column_config.NumberColumn("OPS", format="%.3f", help="**On-Base Plus Slugging**  \nOBP+SLG"),
                    "ops_plus": st.column_config.NumberColumn("OPS+", format="%.0f", help="**Adjusted On-Base Plus Slugging Plus**  \n100*((OBP/tmOBP)+(SLG/tmSLG)-1)"),
                    "isolated_power": st.column_config.NumberColumn("ISO", format="%.3f", help="**Isolated Power**  \nSLG-AVG"),
                    "batting_average_balls_in_play": st.column_config.NumberColumn("BABIP", format="%.3f", help="**Batting Average on Balls In Play**  \n(H-HR)/(AB-K-HR+SF)"),
                    "wrc": st.column_config.NumberColumn("wRC", format="%.0f", help="**Weighted Runs Created**"),
                    "wraa": st.column_config.NumberColumn("wRAA", format="%.1f", help="**Weighted Runs Above Average**"),
                    "woba": st.column_config.NumberColumn("wOBA", format="%.3f", help="**Weighted On-Base Average**"),
                    "wrc_plus": st.column_config.NumberColumn("wRC+", format="%.0f", help="**Adjusted Weighted Runs Created Plus**  \nWeighted Runs Created represented as a rate statistic and adjusted to the team's overall offensive performance  \n100 is team-average, higher is better")
                }
            )

        with tab_stats_pitching:
            pitching_df_stats = df_stats[df_stats['games_pitching'] > 0].copy()
            pitching_df_stats = pitching_df_stats.sort_values(by="out_credit_pitching", ascending=False)
            if not pitching_df_stats.empty:
                st.dataframe(
                    pitching_df_stats,
                    height="content",
                    hide_index=True,
                    placeholder="",
                    column_order=["player","games_pitching","innings_pitched","runs_allowed","strikeouts_pitching","runs_allowed_per_seven","strikeouts_per_seven","out_credit_pitching","pitching_run_value"],
                    column_config={
                        "player": st.column_config.Column("Player", help="**Player**"),
                        "games_pitching": st.column_config.NumberColumn("G", format="%d", help="**Games Pitched**"),
                        "innings_pitched": st.column_config.NumberColumn("IP", format="%.1f", help="**Innings Pitched**"),
                        "runs_allowed": st.column_config.NumberColumn("RA", format="%d", help="**Runs Allowed**"),
                        "strikeouts_pitching": st.column_config.NumberColumn("K", format="%d", help="**Strikeouts**  \nIncludes foul outs"),
                        "runs_allowed_per_seven": st.column_config.NumberColumn("RA7", format="%.2f", help="**Runs Allowed Per Seven Innings**"),
                        "strikeouts_per_seven": st.column_config.NumberColumn("K/7", format="%.2f", help="**Strikeouts Per Seven Innings**  \nIncludes foul outs"),
                        "out_credit_pitching": st.column_config.NumberColumn("PC", format="%.1f", help="**Pitching Out Credit**  \nPitchers receive 0.1 for all outs and an additional 0.9 for strikeouts"),
                        "pitching_run_value": st.column_config.NumberColumn("PRV", format="%.1f", help="**Pitching Run Value**")
                    }
                )

            else:
                st.info("Pitching stats were not tracked before Summer 2025")
            
        with tab_stats_fielding:
            fielding_df_stats = df_stats[(df_stats['innings_defense'] > 0) | (df_stats['innings_designated_hitter'] > 0)].copy()
            fielding_df_stats = fielding_df_stats.sort_values(by="out_credit_fielding", ascending=False)
            df_stats = df_stats.sort_values(by="innings_defense", ascending=False)
            if not fielding_df_stats.empty:
                st.dataframe(
                    fielding_df_stats,
                    height="content",
                    hide_index=True,
                    placeholder="",
                    column_order=[
                        "player","games_batting","innings_defense","innings_pitched","innings_catcher","innings_first_base","innings_second_base","innings_third_base","innings_shortstop","innings_left_field",
                        "innings_left_center_field","innings_right_center_field","innings_right_field","innings_designated_hitter","putouts","assists","fielding_double_plays","range_factor","out_credit_fielding",
                        "fielding_run_value","designated_hitter_adjustment","fielding_run_value_with_adjustment"
                    ],
                    column_config={
                        "player": st.column_config.Column("Player", help="**Player**"),
                        "games_batting": st.column_config.NumberColumn("G", format="%d", help="**Games Played**"),
                        "innings_defense": st.column_config.NumberColumn("Inn", format="%.1f", help="**Defensive Innings Played as Pitcher**"),
                        "innings_pitched": st.column_config.NumberColumn("P", format="%.1f", help="**Innings Pitched**"),
                        "innings_catcher": st.column_config.NumberColumn("C", format="%.1f", help="**Innings Played as Catcher**"),
                        "innings_first_base": st.column_config.NumberColumn("1B", format="%.1f", help="**Innings Played as First Baseman**"),
                        "innings_second_base": st.column_config.NumberColumn("2B", format="%.1f", help="**Innings Played as Second Baseman**"),
                        "innings_third_base": st.column_config.NumberColumn("3B", format="%.1f", help="**Innings Played as Third Baseman**"),
                        "innings_shortstop": st.column_config.NumberColumn("SS", format="%.1f", help="**Innings Played as Shortstop**"),
                        "innings_left_field": st.column_config.NumberColumn("LF", format="%.1f", help="**Innings Played as Leftfielder**"),
                        "innings_left_center_field": st.column_config.NumberColumn("LC", format="%.1f", help="**Innings Played as Left Centerfielder**"),
                        "innings_right_center_field": st.column_config.NumberColumn("RC", format="%.1f", help="**Innings Played as Right Centerfielder**"),
                        "innings_right_field": st.column_config.NumberColumn("RF", format="%.1f", help="**Innings Played as Rightfielder**"),
                        "innings_designated_hitter": st.column_config.NumberColumn("DH", format="%.1f", help="**Innings Played as Designated Hitter**"),
                        "putouts": st.column_config.NumberColumn("PO", format="%d", help="**Putouts**"),
                        "assists": st.column_config.NumberColumn("A", format="%d", help="**Assists**"),
                        "fielding_double_plays": st.column_config.NumberColumn("DP", format="%d", help="**Double Plays Turned**"),
                        "range_factor": st.column_config.NumberColumn("RF/7", format="%.2f", help="**Range Factor Per Seven Innings**  \n(PO+A)/Inn*7"),
                        "out_credit_fielding": st.column_config.NumberColumn("FC", format="%.1f", help="**Fielding Out Credit**  \nPitchers receive 0.1 for all outs. The remaining 0.9 is split evenly between all fielders  \nwho touch the ball leading to an out"),
                        "fielding_run_value": st.column_config.NumberColumn("rawFRV", format="%.1f", help="**Raw Fielding Run Value**"),
                        "designated_hitter_adjustment": st.column_config.NumberColumn("DHA", format="%.1f", help="**Designated Hitter Adjustment**  \nSitting players accrue negative run value as if they were on the field and didn't make any plays.  \nTo balance the team average to zero, an equal amount of positive run value is distributed equally amongst the players in the field."),
                        "fielding_run_value_with_adjustment": st.column_config.NumberColumn("adjFRV", format="%.1f", help="**Adjusted Fielding Run Value**")
                    }
                )

            else:
                st.info("Fielding stats were not tracked before Summer 2025")

        with tab_stats_value:
            df_stats = df_stats.sort_values(by="wins_above_replacement", ascending=False)
            st.dataframe(
                df_stats,
                height="content",
                hide_index=True,
                placeholder="",
                column_order=["player","wraa","pitching_run_value","fielding_run_value","designated_hitter_adjustment","defensive_run_value","replacement_runs","runs_above_replacement","wins_above_replacement"],
                column_config={
                    "player": st.column_config.Column("Player", help="**Player**"),
                    "wraa": st.column_config.NumberColumn("Batting", format="%.1f", help="**Batting Run Value** \nCompared to the team average given an equal amount of plate appearances"),
                    "pitching_run_value": st.column_config.NumberColumn("Pitching", format="%.1f", help="**Pitching Run Value**"),
                    "fielding_run_value": st.column_config.NumberColumn("Fielding", format="%.1f", help="**Raw Fielding Run Value**  \nCompared to the team average given an equal amount of defensive innings"),
                    "designated_hitter_adjustment": st.column_config.NumberColumn("Positional", format="%.1f", help="**Designated Hitter Adjustment**  \nSitting players accrue negative run value as if they were on the field and didn't make any plays.  \nTo balance the team average to zero, an equal amount of positive run value is distributed equally amongst the players in the field."),
                    "defensive_run_value": st.column_config.NumberColumn("Defense", format="%.1f", help="**Defensive Run Value**  \nPitching+Fielding+Positional"),
                    "replacement_runs": st.column_config.NumberColumn("Replacement", format="%.1f", help="**Replacement Run Value**  \nRuns credited to players based on playing time (plate appearances) and team performance (runs scored vs. runs allowed)"),
                    "runs_above_replacement": st.column_config.NumberColumn("RAR", format="%.1f", help="**Runs Above Replacement**  \nBatting+Defense+Replacement"),
                    "wins_above_replacement": st.column_config.NumberColumn("WAR", format="%.1f", help="**Wins Above Replacement**  \nRAR/RPW  \nRPW = Runs Per Win: Value varies by season but is typically in the low-mid 20s")
                }
            )
