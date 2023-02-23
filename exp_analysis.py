import pandas as pd
import pathlib as p
import streamlit as st
from utils.functions import *

# Find app parent directory
app_path = p.Path(__file__).parent

# Useful path and files
data_path = p.PurePath.joinpath(app_path, 'data')
datafile_path = p.PurePath.joinpath(app_path,'data','full_artwork_filtered.csv')

def create_exppage():

    # Load data
    data = pd.read_csv(datafile_path)

    # Create a replica for cosmetic purpuses
    display_data = data
    display_data.rename(columns = {'title_og':'title_artwork','name':'artist_name'}, inplace=True)

    new_order = ['artwork_id','title_artwork','summary_artwork',
                 'year','medium','location','rating',
                 'artist','picture','caption',
                 'artist_name', 'summary_artist', 'artist_movements','description_movements',
                 'bithplace','deathplace','birthdate','deathdate','cause_of_death',
                 'source_artwork','topic_AI','artist_AI',
                 'url_wiki','wiki_artist','image_url','url_AI','url_picture']

    #display_data = display_data.reindex(columns=new_order)

    st.header("Input table")
    st.markdown("This is the data we use to based or research")
    st.dataframe(display_data)

    st.header("Query by Artist")
    
    artwork_counts = data['artist_name'].value_counts().to_frame().reset_index()
    artwork_counts.columns = ['Artist Name', 'Artwork Count']

    list_artist = ["Vincent Van Gogh", "Sandro Botticelli", "Frida Kahlo" ] 

    with st.container():
        artist = st.selectbox("Select Artist",
                             list_artist)

        artist_data = data.loc[data['artist_name'] == artist]

        movement_lists = artist_data['artist_movements'].tolist()
        store_clean = []
        for mov_string in movement_lists:
            clean_str = mov_string.replace('[','').replace(']','').replace('\'','')
            store_clean.extend(clean_str.split(','))
        movement_str = ', '.join(list(set(store_clean)))

        info_dict = {
                'Artworks': [artwork_counts.loc[artwork_counts['Artist Name'] == artist].values[0][1]],
                'Movements': [movement_str]
            }
        summary = artist_data['summary_artist'].values[0]

        col1, col2 = st.columns(2)
        with col1:
            st.subheader('Information available')
            st.table(pd.DataFrame.from_dict(info_dict, orient='index', columns=['']))
            st.text_area("**Summary of the Artist**", summary, height=300)

        with col2:
            st.subheader('Portrait')
            subcol1, subcol2, subcol3 = st.columns([1,5,1])
            if type(artist_data['picture'].values[0]) == int or float:
                image = call_image('noportrait.png').resize((500,500))
                subcol2.image(image, width=250)
            else:
                st.write('future portrait')
            st.subheader('Gallery')
            subcol4, subcol5, subcol6 = st.columns(3)


