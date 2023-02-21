import pandas as pd
import streamlit as st
import time
from data import *

# Set page title
st.set_page_config( page_title='Art-IA color study', 
                    page_icon=':bar_chart:', 
                    layout='wide')

# Side bar (Menu bar)
with st.sidebar:
    add_selectbox = st.selectbox(
        "Menu",
        ("Home", "Exploratory analysis", "Color analysis")
    )


if add_selectbox == "Home":
    # Home Page
    st.title("Color Relatioships in Art and AI-generated Art")
    st.write("The aim of this project is to explore the relationships "+
            "between the most prominent colors in man-made and "+
            "AI-generated works with an specific style or artist"
            )
    
    # n pairs of images from artwork_both_filtered.csv
    n = 1
    image_list = load_image_list(n)

    # Display the images side-by-side
    with st.container():
        col1, col2 = st.columns(2)
        col1.image(call_artwork(image_list[0][0]), use_column_width=True)
        col2.image(call_artwork(image_list[0][1]), use_column_width=True)


elif add_selectbox == "Exploratory analysis":
    st.write("changepage"
         )