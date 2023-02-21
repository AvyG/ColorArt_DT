import streamlit as st
from utils.functions import *

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
    st.title("Color Relationships in Art and AI-Generated Art")
    st.write("The aim of this project is to explore the relationships between the most prominent colors in man-made and AI-generated works with an specific style or artist"
            )
    
    # n pairs of images from artwork_both_filtered.csv
    n = 1
    image_list = load_image_list(n)

    # Display the images side-by-side
    with st.container():
        col1, col2 = st.columns(2)
        image1 = call_artwork(image_list[0][0]).resize((500,500))
        col1.image(image1, use_column_width=True)
        col2.image(call_artwork(image_list[0][1]), use_column_width=True)


elif add_selectbox == "Exploratory analysis":
    st.title("Color Relationships in Art and AI-Generated Art")
    st.write("changepage"
            )

elif add_selectbox == "Color Analysis":
    st.title("Color Relationships in Art and AI-Generated Art")
    st.write("In this section, we present the color extraction of multiple artworks"
            )