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

    # Calculations
    df['strikeout_percentage'] = df['strikeout_percentage']*100
    df['walk_percentage'] = df['walk_percentage']*100
    df['extra_base_hit_percentage'] = df['extra_base_hits']/df['plate_appearances']*100
    df['range_factor'] = (df['putouts']+df['assists'])/df['innings_defense']*7
    df['fielding_run_value_with_adjustment'] = df['fielding_run_value']+df['designated_hitter_adjustment']
    df['runs_above_replacement'] = df['wraa']+df['defensive_run_value']+df['replacement_runs']
    
    # Create a total row for all columns
    total_row = df.sum(numeric_only=True).to_frame().T
    total_row['season'] = "Total"
    total_row['batting_average'] = total_row['hits']/total_row['at_bats']
    total_row['on_base_percentage'] = (total_row['hits']+total_row['walks'])/total_row['plate_appearances']
    total_row['slugging_percentage'] = total_row['total_bases']/total_row['at_bats']
    total_row['on_base_plus_slugging'] = total_row['on_base_percentage']+total_row['slugging_percentage']
    total_ops_points = (df['ops_plus']*df['plate_appearances']).sum()
    total_woba_points = (df['woba']*df['plate_appearances']).sum()
    total_wrc_points = (df['wrc_plus']*df['plate_appearances']).sum()
    total_pa = df['plate_appearances'].sum()
    total_row['ops_plus'] = total_ops_points/total_pa
    total_row['woba'] = total_woba_points/total_pa
    total_row['wrc_plus'] = total_wrc_points/total_pa
    total_row['strikeout_percentage'] = total_row['strikeouts_batting']/total_pa*100
    total_row['walk_percentage'] = total_row['walks']/total_pa*100
    total_row['isolated_power'] = total_row['slugging_percentage']-total_row['batting_average']
    total_row['batting_average_balls_in_play'] = (total_row['hits']-total_row['home_runs'])/(total_row['at_bats']-total_row['strikeouts_batting']-total_row['home_runs']+total_row['sacrifice_flies'])
    total_row['extra_base_hit_percentage'] = total_row['extra_base_hits']/total_pa*100
    total_row['runs_allowed_per_seven'] = total_row['runs_allowed']/total_row['innings_pitched']*7
    total_row['strikeouts_per_seven'] = total_row['strikeouts_pitching']/total_row['innings_pitched']*7
    total_row['range_factor'] = (total_row['putouts']+total_row['assists'])/total_row['innings_defense']*7
    
    # Give the index a name like 'Career Total'
    total_row.index = ['Total']
    
    # Append it to the original DataFrame
    df_with_total = pd.concat([df, total_row])

    # Pitching dataframe branches off here
    pitching_mask = (df_with_total['games_pitching'] > 0) | (df_with_total['season'] == "Total")
    pitching_display_df = df_with_total[pitching_mask]
    has_pitched = pitching_display_df.loc[pitching_display_df['season'] == 'Total', 'games_pitching'].values[0] > 0

    # Fielding dataframe branchse off here
    exclude_seasons = ["Summer 2023", "Fall 2023", "Summer 2024", "Fall 2024"]
    fielding_mask = (~df_with_total['season'].isin(exclude_seasons)) | (df_with_total['season'] == "Total")
    fielding_display_df = df_with_total[fielding_mask]
    has_fielding = fielding_display_df.loc[fielding_display_df['season'] == 'Total', 'innings_defense'].values[0] > 0

    # 1. Define the styling function
    def highlight_total_row(row):
        # Check if the 'season' column for this row is exactly "Total"
        if row['season'] == "Total":
            # Apply a subtle gray tint with 20% opacity
            return ['background-color: rgba(128, 128, 128, 0.2); font-weight: bold;'] * len(row)
        else:
            # Return empty strings (no style) for other rows
            return [''] * len(row)
    
    styled_df = df_with_total.style.apply(highlight_total_row, axis=1)
    styled_pitching_df = pitching_display_df.style.apply(highlight_total_row, axis=1)
    styled_fielding_df = fielding_display_df.style.apply(highlight_total_row, axis=1)
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
            # Overview / Quick Stats / Dashboard
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
                    "season": st.column_config.Column("Season", pinned=True, help="**Season**"),
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

            # Standard Batting Stats
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
                    "season": st.column_config.Column("Season", pinned=True, help="**Season**"),
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

            # Advanced Batting Stats
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
                    "season": st.column_config.Column("Season", pinned=True, help="**Season**"),
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

            # Pitching Stats only visible if player has ever pitched
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
                        "season": st.column_config.Column("Season", pinned=True, help="**Season**"),
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
                
            st.write("")
            st.subheader(":green[Fielding]", help="Fielding stats tracked since Summer 2025")
            st.dataframe(
                styled_fielding_df,
                height="content",
                hide_index=True,
                placeholder="",
                column_order=[
                    "season","games_batting","innings_defense","innings_pitched","innings_catcher","innings_first_base","innings_second_base","innings_third_base","innings_shortstop","innings_left_field",
                    "innings_left_center_field","innings_right_center_field","innings_right_field","innings_designated_hitter","putouts","assists","fielding_double_plays","range_factor","out_credit_fielding",
                    "fielding_run_value","designated_hitter_adjustment","fielding_run_value_with_adjustment"
                ],
                column_config={
                    "season": st.column_config.Column("Season", pinned=True, help="**Season**"),
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

            st.write("")
            st.subheader(":green[Value]")
            st.dataframe(
                styled_df,
                height="content",
                hide_index=True,
                placeholder="",
                column_order=["season","wraa","pitching_run_value","fielding_run_value","designated_hitter_adjustment","defensive_run_value","replacement_runs","runs_above_replacement","wins_above_replacement"],
                column_config={
                    "season": st.column_config.Column("Season", pinned=True, help="**Season**"),
                    "wraa": st.column_config.NumberColumn("Batting", format="%.1f", help="**Batting Run Value**"),
                    "pitching_run_value": st.column_config.NumberColumn("Pitching", format="%.1f", help="**Pitching Run Value**"),
                    "fielding_run_value": st.column_config.NumberColumn("Fielding", format="%.1f", help="**Raw Fielding Run Value**"),
                    "designated_hitter_adjustment": st.column_config.NumberColumn("Positional", format="%.1f", help="**Designated Hitter Adjustment**  \nSitting players accrue negative run value as if they were on the field and didn't make any plays.  \nTo balance the team average to zero, an equal amount of positive run value is distributed equally amongst the players in the field."),
                    "defensive_run_value": st.column_config.NumberColumn("Defense", format="%.1f", help="**Defensive Run Value**  \nPitching+Fielding+Positional"),
                    "replacement_runs": st.column_config.NumberColumn("Replacement", format="%.1f", help="**Replacement Run Value**  \nRuns credited to players based on playing time (plate appearances) and team success (runs scored vs. runs allowed)"),
                    "runs_above_replacement": st.column_config.NumberColumn("RAR", format="%.1f", help="**Runs Above Replacement**  \nBatting+Defense+Replacement"),
                    "wins_above_replacement": st.column_config.NumberColumn("WAR", format="%.1f", help="**Wins Above Replacement**  \nRAR/RPW  \nRPW = Runs Per Win: Value varies by season but is typically in the low-mid 20s")
                }
            )

        with tab_game_log:
            st.markdown("Coming soon")
            
    else:
        st.warning("No player found with that name.")
