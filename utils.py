from Home import supabase

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
    
    return sorted(seasons, key=sort_key)

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
