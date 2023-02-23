import csv
import io
import pathlib as p
import random
import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.image as mpimg
from PIL import Image, ImageColor
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import cv2
import extcolors
from colormap import rgb2hex
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000
from colormath import color_diff_matrix


# Find parent directory
file_path = p.Path(__file__).parents[1]

# Useful path and files
data_path = p.PurePath.joinpath(file_path, 'data')
images_path = p.PurePath.joinpath(file_path, 'images')

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


def get_artwork(url):
    response = requests.get(url)
    image = Image.open(io.BytesIO(response.content))
    return image


###################################
#  Color Analysis
###################################

# below functions were based on 
# https://towardsdatascience.com/image-color-extraction-with-python-in-4-steps-8d9370d9216e
def color_to_df(input):
    colors_pre_list = str(input).replace('([(','').split(', (')[0:-1]
    df_rgb = [i.split('), ')[0] + ')' for i in colors_pre_list]
    df_percent = [i.split('), ')[1].replace(')','') for i in colors_pre_list]
    
    #convert RGB to HEX code
    df_color_up = [rgb2hex(int(i.split(", ")[0].replace("(","")),
                          int(i.split(", ")[1]),
                          int(i.split(", ")[2].replace(")",""))) for i in df_rgb]
    
    df = pd.DataFrame(zip(df_color_up, df_percent), columns = ['c_code','occurence'])
    return df


def plot_extraction(image_url, tolerance=24, limit=10, zoom=2, crop=False):
    # background
    bg = 'bg.png'
    fig, ax = plt.subplots(figsize=(30,20),dpi=10)
    fig.set_facecolor('white')
    plt.savefig(bg)
    plt.close(fig)
    
    # save image under name "image.jpg" (possible resizing could be added here)
    # this will write over any images previoulsy saved by this function to save space
    im = get_artwork(image_url)
    if crop:
        width, height = im.size
        # Calculate the cropping dimensions
        crop_box = (0, height /10, width, 9* height /10)
        # Crop the image
        im = im.crop(crop_box)

    img_url = "image.jpg"
    im.save(img_url)
    
    # create dataframe of colors and occurences
    colors_x = extcolors.extract_from_path(img_url, tolerance = tolerance, limit = limit+1)
    df_color = color_to_df(colors_x)
    
    # annotate text
    list_color = list(df_color['c_code'])
    list_precent = [int(i) for i in list(df_color['occurence'])]
    text_c = [c + ' ' + str(round(p*100/sum(list_precent),1)) +'%' 
              if round(p*100/sum(list_precent),1) >= 5 else "" for c, p in zip(list_color, list_precent)]
    fig, (ax1) = plt.subplots(1, figsize=(40,30), dpi = 10)
    
    # donut plot
    wedges, text = ax1.pie(list_precent,
                           labels= text_c,
                           labeldistance= 1.05,
                           colors = list_color,
                           textprops={'fontsize': 80, 'color':'black'})
    plt.setp(wedges, width=0.3)

    # add image in the center of donut plot
    img = mpimg.imread(img_url)
    imagebox = OffsetImage(img, zoom=zoom)
    ab = AnnotationBbox(imagebox, (0, 0))
    ax1.add_artist(ab)
    
    bg = plt.imread('bg.png')
    plt.imshow(bg)       
    plt.tight_layout()
    return fig

def color_to_df_perc(input):
    colors_pre_list = str(input).replace('([(','').split(', (')[0:-1]
    df_rgb = [i.split('), ')[0] + ')' for i in colors_pre_list]
    df_percent = [i.split('), ')[1].replace(')','') for i in colors_pre_list]
    
    #convert RGB to HEX code
    df_color_up = [rgb2hex(int(i.split(", ")[0].replace("(","")),
                          int(i.split(", ")[1]),
                          int(i.split(", ")[2].replace(")",""))) for i in df_rgb]
    
    # convert occurence to percentage
    list_precent = [int(i) for i in list(df_percent)]
    df_percent_conv = [i/sum(list_precent) for i in list_precent]

    df = pd.DataFrame(zip(df_color_up, df_percent_conv), columns = ['c_code','percentage'])
    return df

def extract_colors(image_url, tolerance=24, limit=10, crop=False):   
    # save image under name "image.jpg"
    # this will write over any images previoulsy saved by this function to save space
    im = get_artwork(image_url)
    if crop:
        width, height = im.size
        # Calculate the cropping dimensions
        crop_box = (0, height /10, width, 9* height /10)
        # Crop the image
        im = im.crop(crop_box)
        
    img_url = "image.png"
    im.save(img_url)
    
    #create dataframe
    colors_x = extcolors.extract_from_path(img_url, tolerance = tolerance, limit = limit+1)
    df_color = color_to_df_perc(colors_x)
    return df_color


# The below functions were copied from ``colormath`` and updated since they used deprecated functions.
def delta_e_cie2000(color1, color2, Kl=1, Kc=1, Kh=1):
    """
    Calculates the Delta E (CIE2000) of two colors.
    """
    color1_vector = _get_lab_color1_vector(color1)
    color2_matrix = _get_lab_color2_matrix(color2)
    delta_e = color_diff_matrix.delta_e_cie2000(
        color1_vector, color2_matrix, Kl=Kl, Kc=Kc, Kh=Kh)[0]
    return delta_e

def _get_lab_color1_vector(color):
    """
    Converts an LabColor into a NumPy vector.

    :param LabColor color:
    :rtype: numpy.ndarray
    """
    if not color.__class__.__name__ == 'LabColor':
        raise ValueError(
            "Delta E functions can only be used with two LabColor objects.")
    return np.array([color.lab_l, color.lab_a, color.lab_b])

def _get_lab_color2_matrix(color):
    """
    Converts an LabColor into a NumPy matrix.

    :param LabColor color:
    :rtype: numpy.ndarray
    """
    if not color.__class__.__name__ == 'LabColor':
        raise ValueError(
            "Delta E functions can only be used with two LabColor objects.")
    return np.array([(color.lab_l, color.lab_a, color.lab_b)])

# based on https://dev.to/tejeshreddy/color-difference-between-2-colours-using-python-182b
def color_diff(hex1, hex2):
    # covert HEX to RGB
    col1_rgb = ImageColor.getcolor(hex1, "RGB")
    col2_rgb = ImageColor.getcolor(hex2, "RGB")
    
    # convert to sRGB
    color1_srgb = sRGBColor(*col1_rgb, is_upscaled=True)
    color2_srgb = sRGBColor(*col2_rgb, is_upscaled=True)
    
    # convert from RGB to Lab Color Space
    color1_lab = convert_color(color1_srgb, LabColor)
    color2_lab = convert_color(color2_srgb, LabColor)
    
    # find the color difference
    delta_e = delta_e_cie2000(color1_lab, color2_lab)
    return delta_e

def dissimilarity_paintings(image_url_1, image_url_2, nb_colors, crop1=False, crop2=False, weighted=True):
    # extract colors as hex
    colors_1 = extract_colors(image_url_1, limit=nb_colors, crop=crop1)
    colors_2 = extract_colors(image_url_2, limit=nb_colors, crop=crop2)
    
    # matrix to store the pairwise color differences
    diff_mat = np.zeros((nb_colors,nb_colors))
    # calculate the color differences
    for i in range(nb_colors):
        for j in range(nb_colors):
            if weighted:
                # weigh the color difference by the product of the occurence percentages
                p1 = colors_1.loc[i]["percentage"]
                p2 = colors_2.loc[j]["percentage"]
            else:
                p1 = 1
                p2 = 1
            diff_mat[i][j] = p1 * p2 * color_diff(colors_1.loc[i]["c_code"], colors_2.loc[j]["c_code"])
    
    # the dissimilarity between the two paintings is the average of diff_matrix
    dissim = np.mean(diff_mat)
    return dissim