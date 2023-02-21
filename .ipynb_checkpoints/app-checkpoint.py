import pandas as pd
import streamlit as st
import time
from data import *

# Set page title
st.set_page_config( page_title='FrostByte', 
                    page_icon='🎨', 
                    layout='wide')


# Title, Tabs, Sidebar 

st.title("KU Leuven Datathon 2023")

tab_home, tab_explore, tab_analysis, tab_aboutus = st.tabs(["Home", "Exploratory Analysis", "Color Analysis", "About Us"])

col1, col2, col3 = st.sidebar.columns([1,8,1])
with col1:
    st.write("")
with col2:
    st.image('logo.png',  use_column_width=True)
with col3:
    st.write("")

st.sidebar.markdown("We are Master's students at KU Leuven studying Statistics and Data Science. Learn more about us in About Us", unsafe_allow_html=True)              
st.sidebar.info("This project is created for KU Leuven's Datathon 2023. Our work can be found on [Github](https://github.com/AvyG/ColorArt_DT). More information about the Datathon can be found [here](https://kul-datathon-jobfair.netlify.app/#Datathon)", icon="🎨")



# Home tab

with tab_home:
    # Home Page
    st.title("AI-rtist vs. Aritst")
    st.markdown("What does influence the color palettes of AI-rtist and artist? Is there difference between artworks generated by an AI-rtist and artist? We explore image data consisting of both AI-generated artworks and original artworks to answer these questions by focusing on colors.", unsafe_allow_html=True)

    
    # n pairs of images from artwork_both_filtered.csv
    n = 1
    image_list = load_image_list(n)

    # Display the images side-by-side
    with st.container():
        col1, col2 = st.columns(2)
        col1.image(call_artwork(image_list[0][0]), use_column_width=True)
        col2.image(call_artwork(image_list[0][1]), use_column_width=True)


# About Us tab

with tab_aboutus:
    st.header("About Us")
    st.markdown('''### Meet the members of Team FrostByte''', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4, gap="medium")
    with col1:
        st.image('memoji_seorin.png',  use_column_width=False)
        st.markdown ("Seorin Kim \n> seorin.kim@student.kuleuven.be")
    with col2:
        st.image('logo.png',  use_column_width=True)
        st.markdown ("Seorin Kim \n> seorin.kim@student.kuleuven.be")
    with col3:
        st.image('logo.png',  use_column_width=True)
        st.markdown ("Seorin Kim \n> seorin.kim@student.kuleuven.be")
    with col4:
        st.image('logo.png',  use_column_width=True)
        st.markdown ("Seorin Kim \n> seorin.kim@student.kuleuven.be")
                
    
    
    
    