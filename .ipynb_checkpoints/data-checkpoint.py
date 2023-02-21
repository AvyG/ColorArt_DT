import csv
import io
import pathlib as p
import random
import requests
from PIL import Image

# Find current directory
file_path = p.Path(__file__).parent

# Useful files
p_filtered_artwork = p.PurePath.joinpath(file_path, 'artwork_both_filtered.csv')

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

def call_artwork(url):
    response = requests.get(url)
    image = Image.open(io.BytesIO(response.content))
    return image