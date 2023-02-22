import cv2
import io
import requests
import pandas as pd
import numpy as np
import pathlib as p
from PIL import Image

# Find app parent directory
app_path = p.Path(__file__).parents[1]

# Save path to data folder
tosave_path = p.PurePath.joinpath(app_path, 'data', 'full_artwork_filtered.csv')

# Create the dataset 
# (run if full_artwork_both_filter.csv is not present)

def generate_dataset():

    # Recall the necessary provided dataset
    artists = pd.read_parquet("https://kuleuven-datathon-2023.s3.eu-central-1.amazonaws.com/data/Artist.parquet.gzip")
    generated = pd.read_parquet('https://kuleuven-datathon-2023.s3.eu-central-1.amazonaws.com/data/Generated.parquet.gzip')
    artworks = pd.read_parquet('https://kuleuven-datathon-2023.s3.eu-central-1.amazonaws.com/data/Artwork.parquet.gzip')
    movement = pd.read_parquet('https://kuleuven-datathon-2023.s3.eu-central-1.amazonaws.com/data/Movement.parquet.gzip')
    artmov = pd.read_csv('https://kuleuven-datathon-2023.s3.eu-central-1.amazonaws.com/data/ArtistMovements.csv')
    
    # Extract the url as a string in a separated column
    generated['strurl'] = str(generated.url)

    # Extract the artist and the painting from the prompt given to the ai
    art_pattern = '(A painting of)(.*?)(in the style of)(.*?)(.png)'
    art = generated.url.str.extract(art_pattern)
    art = art[[1,3]]

    # Making a common column due to its absence
    generated['num'] = 1
    art.loc[:,'num'] = 1

    # Concatenate the two dataframes
    generated_info = pd.concat([generated, art], axis=1)
    generated_info.rename(columns = {1:'topic_AI', 3:'artist_AI'}, inplace = True)
    generated_info.drop(['num', 'strurl'], inplace=True, axis=1)
    
    # Merge with "artworks" data
    artworks_full = pd.merge(artworks, generated_info, left_on='id', right_on='source_artwork')
    artworks_full.rename(columns = {'url_x':'url_wiki', 'url_y':'url_AI', 'id':'artwork_id', 'name':'title_og'}, inplace = True)

    artists.rename(columns = {'id': 'artist', 'url': 'wiki_artist'}, inplace =True)
    df = pd.merge(artworks_full, artists, on = 'artist')
    df.rename(columns= {'summary_x': 'summary_artwork', 'summary_y':'summary_artist'}, inplace = True)
    
    """ Problematic onces
    Louvre = Musée du Louvre, Paris = Musée du Louvre = Louvre Museum = The Louvre
    Royal Museums of Fine Arts of Belgium = Royal Museum of Fine Arts of Belgium
    Museum of Popular Art of Constanța (page does not exist)
    National Gallery (London) = National Gallery, London = National Gallery #National Galllery of Art is in Washington D.C., USA
    Metropolitan Museum of Art = The Metropolitan Museum of Art
    Uffizi Gallery = Uffizi
    Santa Maria Gloriosa dei Frari = Basilica di Santa Maria Gloriosa dei Frari
    Smithsonian Museum of American Art = Smithsonian American Art Museum
    J. Paul Getty Museum = The J. Paul Getty Museum
    Galleria nazionale di Parma = Galleria Nazionale di Parma
"""

    # Note: checked online what appears to be the official name of the locations.
    df.loc[df.location.str.contains('Louvre', case=False) == True, 'location'] = "Musée du Louvre"
    df = df.replace({'location': {'Metropolitan Museum of Art': 'The Metropolitan Museum of Art', 
                                  'Royal Museum of Fine Arts of Belgium': 'Royal Museums of Fine Arts of Belgium',
                                  'National Gallery': 'National Gallery, London', 
                                  'National Gallery (London)': 'National Gallery, London',
                                  'Museum of Popular Art of Constanța (page does not exist)': 'Museum of Popular Art of Constanța',
                                  'Uffizi': 'Uffizi Gallery',
                                  'Santa Maria Gloriosa dei Frari': 'Basilica di Santa Maria Gloriosa dei Frari',
                                  'Smithsonian Museum of American Art': 'Smithsonian American Art Museum',
                                  'The J. Paul Getty Museum': 'J. Paul Getty Museum',
                                  'Galleria nazionale di Parma': 'Galleria Nazionale di Parma'
                                 }})
    
    # Merge the table with the "movement" data
    # For this first we need to merge with the "artistmovement" data
    # Then we can merge the table with the "movement" data to have the movement name and description for each artwork 
    merged_table = pd.merge(df, artmov, left_on = 'artist', right_on='artist_id')
    df = pd.merge(merged_table, movement,  left_on='movement_id', right_on='id')
    
    df.rename(columns= {'name_x': 'artist_name', 'name_y':'movement_name','description':'movement_description','title_og':'title_artwork'}, inplace = True)
    
    # But some artworks belong to more than one movement
    # This transform the movements of those artworks to a list
    grouped = df.groupby("artwork_id")["movement_name"].apply(list).reset_index()
    df.drop("movement_name", axis=1, inplace=True)
    df = pd.merge(df, grouped, on="artwork_id", how="left")
    df.drop_duplicates(subset=["artwork_id"], inplace=True)

    #This checks for AI artwork that are black
    i=1
    for url in df.url_AI:
        response = requests.get(url)
        img = Image.open(io.BytesIO(response.content))
        image = np.asarray(img)
        gray_version = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        if cv2.countNonZero(gray_version) == 0:
            drop = df[df['url_AI'] == url].index
            df.drop(drop, inplace=True)
            i+=1
        else:
            print(f"\r{i}", 'checked image', end='', flush=True)
            i+=1
            #print(f"\r{df[df['url_AI'] == url].index.item()}", 'colored image', end='', flush=True)
    
    df.to_csv(tosave_path, index=False)