import csv
import io
import pathlib as p
import random
import requests
from PIL import Image

# Find current directory
app_path = p.Path(__file__).parents[1]

# Useful path and files
data_path = p.PurePath.joinpath(app_path, 'data')
images_path = p.PurePath.joinpath(app_path, 'images')

p_filtered_artwork = p.PurePath.joinpath(data_path, 'artwork_both_filtered.csv')

# This function creates returns one list of n elements that half
# are the artworks url and the other half are AI works to display
def load_image_list(n):
    table = []
    with io.open(p_filtered_artwork, 'r', encoding="Windows-1254", errors='replace') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            table.append((row[5],row[13]))
    random_elements = random.sample(table, n)
    return random_elements

def call_image(image_file):
    p_image = p.PurePath.joinpath(images_path, image_file)
    image = Image.open(p_image)
    return image

def call_artwork(url):
    response = requests.get(url)
    image = Image.open(io.BytesIO(response.content))
    return image