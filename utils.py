import pandas as pd
from Home import supabase

def create_row_highlighter(target_column, target_value, bg_color="rgba(128, 128, 128, 0.2)", bold=True):
    """
    Generates a dynamic row highlighting function for pandas Styler.
    """
    style_string = f"background-color: {bg_color};"
    if bold:
        style_string += " font-weight: bold;"

    def highlight_row(row):
        # Dynamically check the column and value you specified
        if row[target_column] == target_value:
            return [style_string] * len(row)
        return [''] * len(row)
        
    return highlight_row

def fetch_player_data(player_name):
    # 'get_player_profile' is the name of the SQL function
    # The dictionary keys must match the parameter names in your SQL function
    response = supabase.rpc("get_player_profile", {"target_player": player_name}).execute()
    
    # Convert the JSON response directly into a DataFrame
    return pd.DataFrame(response.data)

# Inside utils.py

# Inside utils.py

def format_baseball_innings(val):
    """
    Converts a raw cumulative float into standard baseball notation (.1 or .2).
    Returns "-" if the value is 0, NaN, or None.
    """
    import pandas as pd
    import math
    
    # --- UPDATED FALLBACK CHECK ---
    if pd.isna(val) or val == 0:
        return "-"
        
    # 1. Break the raw number into its whole and decimal parts
    whole_part = math.floor(val)
    decimal_part = round(val - whole_part, 2)
    
    # 2. Convert everything to total outs (thirds of an inning)
    if decimal_part >= 0.3:
        # If data was entered as raw literal decimals (e.g., .7 for 7 outs)
        literal_outs = round(decimal_part * 10)
        total_outs = (whole_part * 3) + literal_outs
    else:
        # Standard fractional calculation (e.g., 57.6667 -> 57 and 2 outs)
        total_outs = round(val * 3)
        
    # 3. Reconstruct the standard baseball string notation
    final_innings = total_outs // 3
    leftover_outs = total_outs % 3
    
    if leftover_outs == 0:
        return f"{final_innings}"
        
    return f"{final_innings}.{leftover_outs}"

def get_all_players():
    # Fetch just the player names from the primary_positions table
    response = supabase.table("primary_positions").select("player").execute()
    # Extract names into a sorted list
    player_list = sorted([row['player'] for row in response.data])
    return player_list

def get_sorted_seasons():
    # Fetch unique seasons from your guts or stats table
    response = supabase.table("guts").select("season").execute()
    seasons = list(set([row['season'] for row in response.data]))
    
    # Custom sorting logic: Year first, then Season order
    season_order = {"Spring": 1, "Summer": 2, "Fall": 3, "Winter": 4}
    
    def sort_key(s):
        parts = s.split() # e.g., ["Summer", "2023"]
        return (int(parts[1]), season_order.get(parts[0], 5))
    
    # Setting reverse=True flips the output to Newest -> Oldest safely
    return sorted(seasons, key=sort_key, reverse=True)

def get_player_seasons(player_name):
    # 1. Query the stats view instead of the guts table
    # We filter by player to only get seasons they actually played
    response = supabase.table("player_season_stats") \
        .select("season") \
        .eq("player", player_name) \
        .execute()
    
    # 2. Extract unique seasons from the response
    seasons = list(set([row['season'] for row in response.data]))
    
    if not seasons:
        return []

    # 3. Use your existing custom sorting logic
    season_order = {"Spring": 1, "Summer": 2, "Fall": 3, "Winter": 4}
    
    def sort_key(s):
        parts = s.split() # e.g., ["Summer", "2023"]
        # Handle cases where season name might be malformed
        try:
            year = int(parts[1])
            period = season_order.get(parts[0], 5)
            return (year, period)
        except (IndexError, ValueError):
            return (0, 0)
    
    # 4. Return sorted list (Most recent first usually feels better for game logs)
    return sorted(seasons, key=sort_key, reverse=True)

def get_table_data(table_name):
    # .select("*") grabs all columns; change to specific columns if preferred
    response = supabase.table(table_name).select("*").execute()
    
    # Extract the raw list of dictionaries from the response object
    return response.data
