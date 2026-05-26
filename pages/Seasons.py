import streamlit as st
import pandas as pd
from Home import supabase
from utils import (
    fetch_player_data,
    get_all_players,
    get_player_seasons,
    get_sorted_seasons
)

st.set_page_config(page_title="D-X Seasons", layout="wide", page_icon="https://images.seeklogo.com/logo-png/27/1/d-generation-x-logo-png_seeklogo-275249.png")

st.subheader(":green[D-Generation X History]")
