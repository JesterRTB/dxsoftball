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
    
    leaderboard_response = supabase.rpc("get_leaderboard", {
        "start_season": start_season, 
        "end_season": end_season
    }).execute()
    
    df = pd.DataFrame(leaderboard_response.data)

    # Calculations
    df['strikeout_percentage'] = df['strikeout_percentage']*100
    df['walk_percentage'] = df['walk_percentage']*100
    df['extra_base_hit_percentage'] = df['extra_base_hits']/df['plate_appearances']*100
    df['range_factor'] = (df['putouts']+df['assists'])/df['innings_defense']*7
    df['fielding_run_value_with_adjustment'] = df['fielding_run_value']+df['designated_hitter_adjustment']
    df['runs_above_replacement'] = df['wraa']+df['defensive_run_value']+df['replacement_runs']
    
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
        
        with tab_standard_batting:
            df = df.sort_values(by="batting_average", ascending=False)
            st.dataframe(
                df,
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

        with tab_advanced_batting:
            df = df.sort_values(by="wrc_plus", ascending=False)
            st.dataframe(
                df,
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
                    "wrc_plus": st.column_config.NumberColumn("wRC+", format="%.0f", help="**Adjusted Weighted Runs Created Plus**")
                }
            )

        with tab_pitching:
            pitching_df = df[df['games_pitching'] > 0].copy()
            pitching_df = pitching_df.sort_values(by="innings_pitched", ascending=False)
            if not pitching_df.empty:
                st.dataframe(
                    pitching_df,
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
            
        with tab_fielding:
            fielding_df = df[(df['innings_defense'] > 0) | (df['innings_designated_hitter'] > 0)].copy()
            fielding_df = fielding_df.sort_values(by="innings_defense", ascending=False)
            df = df.sort_values(by="innings_defense", ascending=False)
            if not fielding_df.empty:
                st.dataframe(
                    fielding_df,
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

        with tab_value:
            df = df.sort_values(by="wins_above_replacement", ascending=False)
            st.dataframe(
                df,
                height="content",
                hide_index=True,
                placeholder="",
                column_order=["player","wraa","pitching_run_value","fielding_run_value","designated_hitter_adjustment","defensive_run_value","replacement_runs","runs_above_replacement","wins_above_replacement"],
                column_config={
                    "player": st.column_config.Column("Player", help="**Player**"),
                    "wraa": st.column_config.NumberColumn("Batting", format="%.1f", help="**Batting Run Value**"),
                    "pitching_run_value": st.column_config.NumberColumn("Pitching", format="%.1f", help="**Pitching Run Value**"),
                    "fielding_run_value": st.column_config.NumberColumn("Fielding", format="%.1f", help="**Raw Fielding Run Value**"),
                    "designated_hitter_adjustment": st.column_config.NumberColumn("Positional", format="%.1f", help="**Designated Hitter Adjustment**  \nSitting players accrue negative run value as if they were on the field and didn't make any plays.  \nTo balance the team average to zero, an equal amount of positive run value is distributed equally amongst the players in the field."),
                    "defensive_run_value": st.column_config.NumberColumn("Defense", format="%.1f", help="**Defensive Run Value**  \nPitching+Fielding+Positional"),
                    "replacement_runs": st.column_config.NumberColumn("Replacement", format="%.1f", help="**Replacement Run Value**  \nRuns credited to players based on playing time (plate appearances) and team performance (runs scored vs. runs allowed)"),
                    "runs_above_replacement": st.column_config.NumberColumn("RAR", format="%.1f", help="**Runs Above Replacement**  \nBatting+Defense+Replacement"),
                    "wins_above_replacement": st.column_config.NumberColumn("WAR", format="%.1f", help="**Wins Above Replacement**  \nRAR/RPW  \nRPW = Runs Per Win: Value varies by season but is typically in the low-mid 20s")
                }
            )
