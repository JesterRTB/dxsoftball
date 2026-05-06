import streamlit as st
import pandas as pd
from Home import supabase

st.set_page_config(page_title="D-X Player Search", page_icon="🥎")

def fetch_player_data(player_name):
    # 'get_player_profile' is the name of the SQL function
    # The dictionary keys must match the parameter names in your SQL function
    response = supabase.rpc("get_player_profile", {"target_player": player_name}).execute()
    
    # Convert the JSON response directly into a DataFrame
    return pd.DataFrame(response.data)

st.title("Player Search")

# A simple text input for the search
player_search = st.text_input("Enter Player Name", placeholder="e.g. Jason Jester")

if player_search:
    df = fetch_player_data(player_search)
    
    if not df.empty:
        # Displaying the high-level profile info
        col1, col2 = st.columns(2)
        col1.metric("Primary Position", df['position_long'].iloc[0])
        col2.metric("DX Debut", df['dx_debut'].iloc[0])
        
        st.write("### Seasonal Stats")
        st.dataframe(df.drop(columns=['player', 'dx_debut', 'position_long']), hide_index=True)
    else:
        st.warning("No player found with that name.")
