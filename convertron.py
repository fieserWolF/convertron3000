#!/usr/bin/env python3

"""
Convertron3000 Commodore 64 graphics converter
Copyright (C) 2024 fieserWolF / Abyss-Connection

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

For futher questions, please contact me at
http://csdb.dk/scener/?id=3623
or
wolf@abyss-connection.de

For Python3, The Python Imaging Library (PIL), Numpy, Tcl/Tk and other used source licenses see file "LICENSE_OTHERS".
"""



import os
import sys
import hitherdither
import struct
from PIL import ImageTk, ImageEnhance, ImageFilter, ImageDraw
import PIL.Image as PilImage    #we need another name, as it collides with tkinter.Image otherwise
from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
import json
import argparse

#from tkinter import ttk
#ttk.Style().theme_use('clam')


#global constants
def _global_constants():
        return None

#BGCOLOR="#ff0000"
BGCOLOR="#d9d9d9"


PROGNAME = 'CONVERTRON3000';
C64_CHAR_HEIGHT=25  #200/8
C64_CHAR_WIDTH=40   #320/8

FILENAME_JSON_PRE = '/tmp/color_clashes.json'
FILENAME_CLASH_IMAGE_PRE = '/tmp/color_clashes.png'

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)
    
RES_VERSION = resource_path('resources/version.txt')
RES_GFX_ICON = resource_path('resources/icon.png')
RES_GFX_ABOUT = resource_path('resources/about.png')
RES_DOC_ABOUT = resource_path('resources/about.txt')

VERSION = open(RES_VERSION, encoding="utf_8").read().rstrip()


_padx = 2
_pady = 2
_bd = 4

KOALA_WIDTH = 160
KOALA_HEIGHT = 200
HIRES_WIDTH = 320
HIRES_HEIGHT = 200


PALETTEDATA_PEPTO = (
    0, 0, 0,		# 0 black
    255, 255, 255,	# 1 white
    104, 55, 43,	# 2 red
    112, 164, 178,	# 3 cyan
    111,  61, 134,	# 4 purple
     88, 141,  67,	# 5 green
     53,  40, 121,	# 6 blue
    184, 199, 111,	# 7 yellow
    111,  79,  37,	# 8 orange
     67,  57,   0,	# 9 brown
    154, 103,  89,	# a pink
     68,  68,  68,	# b dark gray
    108, 108, 108,	# c gray
    154, 210, 132,	# d light green
    108,  94, 181,	# e light blue
    149, 149, 149,	# f light gray
)


PALETTEDATA_VIEW64 = (
    0,   0,   0,	# 0 black
    250, 250, 250,	# 1 white
    127,  39,  52,	# 2 red
    111, 192, 180,	# 3 cyan
    135,  60, 149,	# 4 purple
     86, 156,  73,	# 5 green
     62,  62, 142,	# 6 blue
    187, 187, 106,	# 7 yellow
    134,  61,  39,	# 8 orange
     85,  44,   0,	# 9 brown
    174,  86,  99,	# a pink
     78,  78,  78,	# b dark gray
    117, 117, 117,	# c gray
    148, 218, 135,	# d light green
    117, 117, 197,	# e light blue
    156, 156, 156	# f light gray
)

PALETTEDATA_VICE = (
    0,   0,   0,	# 0 black
    255, 255, 255,	# 1 white
    146,  74,  64,	# 2 red
    132, 197, 204,	# 3 cyan
    147,  81, 182,	# 4 purple
    114, 177,  75,	# 5 green
     72,  58, 170,	# 6 blue
    213, 223, 124,	# 7 yellow
    153, 105,  45,	# 8 orange
    103,  82,   0,	# 9 brown
    193, 129, 120,	# a pink
     92,  92,  92,	# b dark gray
    151, 151, 151,	# c gray
    179, 236, 145,	# d light green
    135, 139, 221,	# e light blue
    200, 200, 200	# f light gray
)

PALETTEDATA_COLODORE = (
    0,   0,   0,	# 0 black
    255, 255, 255,	# 1 white
    129,  51, 56,	# 2 red
    117, 206, 200,	# 3 cyan
    142,  60, 151,	# 4 purple
    86, 172,  77,	# 5 green
    46,  44, 155,	# 6 blue
    237, 241, 113,	# 7 yellow
    142,  80,  41,	# 8 orange
    85,  56,   0,	# 9 brown
    196, 108, 113,	# a pink
    74,  74,  74,	# b dark gray
    123, 123, 123,	# c gray
    169, 255, 159,	# d light green
    112, 109, 235,	# e light blue
    178, 178, 178	# f light gray
)

#gradients from project one:
GRADIENT_PURPLE_COLORS = 6
GRADIENT_PURPLE_SCEME = (
    0x00,
    0x06,
    0x04,
    0x0a,
    0x07,
    0x01
)

GRADIENT_BROWN_COLORS = 7
GRADIENT_BROWN_SCEME = (
    0x00,
    0x09,
    0x02,
    0x08,
    0x0a,
    0x07,
    0x01
)

GRADIENT_GRAY_COLORS = 5
GRADIENT_GRAY_SCEME = (
    0x00,
    0x0b,
    0x0c,
    0x0f,
    0x01
)

GRADIENT_GREEN_COLORS = 6
GRADIENT_GREEN_SCEME = (
    0x00,
    0x09,
    0x05,
    0x03,
    0x0d,
    0x01
)

GRADIENT_BLUE_COLORS = 6
GRADIENT_BLUE_SCEME = (
    0x00,
    0x0b,
    0x0e,
    0x03,
    0x0d,
    0x01
)

GRADIENT_GREEN2_COLORS = 6
GRADIENT_GREEN2_SCEME = (
    0x00,
    0x09,
    0x05,
    0x03,
    0x0d,
    0x0f
)



"""
you need 15 values for each color
apart from the color to be replaced, each of the 16 c64 colors has to be in each table
colors near to the original come first, then the worse alternatives, in the end the worst alternative color
"""
REPLACEMENT_TABLE = (
    (	11,	6,	2,	5,	9,	12,	8,	4,	10,	7,	14,	13,	3,	15,	1),#00 black    
    (	15,	3,	13,	14,	7,	10,	7,	8,	12,	9,	5,	2,	6,	11,	0),#01 white
    (	8,	9,	10,	0,	4,	11,	6,	5,	12,	7,	14,	13,	3,	15,	1),#02 red
    (	14,	13,	15,	10,	12,	7,	1,	6,	5,	8,	2,	9,	4,	11,	0),#03 cyan
    (	6,	8,	10,	2,	9,	11,	12,	13,	14,	7,	5,	0,	3,	15,	1),#04 purple
    (	13,	3,	11,	12,	6,	2,	9,	0,	4,	8,	10,	14,	7,	15,	1),#05 green
    (	14,	4,	0,	2,	9,	5,	3,	11,	12,	8,	10,	7,	13,	15,	1),#06 blue
    (	1,	13,	3,	15,	14,	10,	8,	12,	11,	4,	5,	6,	2,	9,	0),#07 yellow
    (	2,	9,	10,	7,	15,	13,	14,	3,	1,	4,	5,	6,	11,	12,	0),#08 light brown
    (	2,	8,	10,	11,	0,	6,	5,	12,	4,	7,	14,	13,	3,	15,	1),#09 brown
    (	8,	7,	2,	9,	15,	12,	11,	6,	5,	4,	0,	10,	14,	15,	1),#10 light-red
    (	12,	0,	15,	2,	9,	8,	6,	5,	4,	10,	7,	14,	13,	3,	1),#11 dark-gray
    (	11,	15,	0,	2,	9,	8,	6,	5,	4,	10,	7,	14,	13,	3,	1),#12 gray
    (	3,	5,	7,	15,	14,	10,	12,	11,	8,	1,	4,	9,	2,	6,	0),#13 light-green
    (	3,	6,	1,	13,	15,	10,	8,	4,	7,	12,	5,	2,	11,	9,	0),#14 light-blue
    (	1,	12,	11,	7,	13,	14,	4,	10,	8,	9,	5,	2,	6,	3,	0) #15 light-gray
)

CURSOR_HAND = 'hand2'

#CONFIG_FILENAME = "convertron3000.ini"  #"c:\\convertron3000.ini"





"""
ERROR_DIFFUSION = (
    'Floyd-Steinberg',
    'Jarvis-Judice-Ninke',
    'Stucki',
    'Burkes',
    'Sierra3',
    'Sierra2',
    'Sierra-2-4A',
    'Stevenson-Arce',
    'Atkinson'
)
"""


#global variables
def _global_variables():
        return None
        
root = Tk()

user_filename_open = "none"
user_filename_save = "none"
user_filename_save_clash_json = "none"
user_filename_save_clash_image = "none"

user_start_address = StringVar()
user_start_address_checkbutton = IntVar()
user_sharpness = IntVar()
user_treshold = IntVar()
user_color_saturation = IntVar()
user_brightness = IntVar()
user_contrast = IntVar()
user_modes = StringVar()
user_outputformat = StringVar()
user_palette = StringVar()
user_filename_open_textvariable = StringVar()
convertbutton_text = StringVar()

user_effects_blur = IntVar()
user_effects_detail = IntVar()
user_effects_enhance = IntVar()
user_effects_enhance_more = IntVar()
user_effects_smooth = IntVar()
user_effects_smooth_more = IntVar()
user_effects_sharpen = IntVar()
user_effects_showClashes = IntVar()

user_gradient_sceme = StringVar()
user_dithering = StringVar()
user_backgroundcolor = IntVar()
user_backgroundcolor.set(99)


#defaults
user_outputformat.set("koala")
user_modes.set("colors")
user_palette.set("pepto")
user_gradient_sceme.set("purple")
user_filename_open_textvariable.set("none")
convertbutton_text.set("convert\nAlt+C")
user_dithering.set("none")
#user_dithering.set("bayer")


textbox = Text()
label_original_image = Label()
label_preview_image = Label()
label_koala_image = Label()
image_original = PilImage.new("RGB", (320, 200), "black")
image_preview = PilImage.new("RGB", (320, 200), "black")
image_koala = PilImage.new("RGBA", (320, 200), "black")
image_preview_convert = PilImage.new("RGB", (160, 200), "black")

koala_bitmap=[None]*8000
koala_col12=[None]*1000
koala_col3=[None]*1000
koala_bg=0

koala_colorindex_data = [0] * KOALA_WIDTH*KOALA_HEIGHT
hires_colorindex_data = [0] * HIRES_WIDTH*HIRES_HEIGHT

#initialize empty 320x200 data
image_result_koala = PilImage.new("P", (KOALA_WIDTH, KOALA_HEIGHT))
image_result_hires = PilImage.new("P", (HIRES_WIDTH, HIRES_HEIGHT))

image_clashes = PilImage.new("P", (KOALA_WIDTH, KOALA_HEIGHT))
#image_clashes_koala = PilImage.new("P", (KOALA_WIDTH, KOALA_HEIGHT))
#image_clashes_hires = PilImage.new("P", (HIRES_WIDTH, HIRES_HEIGHT))


scale_modifier_list=[]
scale_modifier_list_default=[]

user_custom_gradient_sceme = [0] * 16
user_custom_gradient_sceme_size = 0

color_clash_chars_xy = []

args = 0


#hitherdither
def convert_to_hitherdither_palette (
    palette_rgb
) :
    pal = []
    cnt = 0
    for value in palette_rgb :
        if (cnt == 0 ) : r = value
        if (cnt == 1 ) : g = value
        if (cnt == 2 ) :
            b = value
            rgb = (r * 256 * 256) + (g * 256) + b
            pal.append(rgb)
            cnt = -1
        cnt += 1
    return pal

hitherdither_palette = hitherdither.palette.Palette(convert_to_hitherdither_palette(PALETTEDATA_PEPTO))  #do to
hitherdither_tres_value=256/8    #play around with tresholds
hitherdither_tresholds = [hitherdither_tres_value, hitherdither_tres_value, hitherdither_tres_value]
hitherdither_order=8  #2,4,8,16,32,64,128









#https://docs.python.org/2.7/library/configparser.html#examples
def config_read(
    filename
) :
    global user_custom_gradient_sceme
    global user_custom_gradient_sceme_size

    with open(filename, "r") as f:
        config = json.load(f)
    
    user_custom_gradient_sceme_size = int(config['size'])

    for a in range(0,len(user_custom_gradient_sceme)) :
        user_custom_gradient_sceme[a] = int(config['color'+str(a)])




def gen_matrix( e ):
#https://github.com/justmao945/lab/tree/master/halftoning/ordered-dithering
  ''' Generating new matrix.
      @param e The width and height of the matrix is 2^e.
      @return New 2x2 to 2^e x 2^e matrix list.
  '''
  if e < 1: return None
  m_list = [ [[1,2],[3,0]] ]
  _b = m_list[0]
  for n in range(1, e):
    m = m_list[ n - 1 ]
    m_list.append( [
      [4*i+_b[0][0] for i in m[0]] + [4*i+_b[0][1] for i in m[0]],
      [4*i+_b[0][0] for i in m[1]] + [4*i+_b[0][1] for i in m[1]],
      [4*i+_b[1][0] for i in m[0]] + [4*i+_b[1][1] for i in m[0]],
      [4*i+_b[1][0] for i in m[1]] + [4*i+_b[1][1] for i in m[1]],
    ] )
  return m_list


"""
def ordered_dithering( pixel, size, matrix ):
#https://github.com/justmao945/lab/tree/master/halftoning/ordered-dithering
    #Dithering on a single channel.
    #@param pixel PIL PixelAccess object.
    #@param size A tuple to represent the size of pixel.
    #@param matrix Must be NxN, and N == 2^e where e>=1

    X, Y = size
    N = len(matrix)

    T = [[255*(matrix[x][y]+0.5)/N/N for x in range(N)] for y in range(N)]
    for y in range(0, Y):
        for x in range(0, X):
#            pixel[x,y] = 255 if pixel[x,y] > T[x%N][y%N] else 0
            if pixel[x,y] > T[x%N][y%N] :
                pixel[x,y] = 255
            else :
                pixel[x,y] = 0
"""








def image_quantize_c64_colors(image):
    pal_image= PilImage.new("P", (1,1))
    

    switcher_palette = {
        'pepto': PALETTEDATA_PEPTO,
        'view64': PALETTEDATA_VIEW64,
        'vice': PALETTEDATA_VICE,
        'colodore': PALETTEDATA_COLODORE,
    }
    my_palettedata = switcher_palette.get(user_palette.get(), PALETTEDATA_PEPTO)
    
    hitherdither_tresholds = [256/user_treshold.get(), 256/user_treshold.get(), 256/user_treshold.get()]

    #https://github.com/justmao945/lab/tree/master/halftoning/ordered-dithering
    if (user_dithering.get() == 'bayer') :
        hitherdither_palette = hitherdither.palette.Palette(convert_to_hitherdither_palette(my_palettedata))
        image = hitherdither.ordered.bayer.bayer_dithering(image, hitherdither_palette, hitherdither_tresholds, order=hitherdither_order)
    if (user_dithering.get() == 'yliluomas1') :
        hitherdither_palette = hitherdither.palette.Palette(convert_to_hitherdither_palette(my_palettedata))
        image = hitherdither.ordered.yliluoma.yliluomas_1_ordered_dithering(image, hitherdither_palette, order=hitherdither_order)
    if (user_dithering.get() == 'line') :
        hitherdither_palette = hitherdither.palette.Palette(convert_to_hitherdither_palette(my_palettedata))
        my_width, my_height = image.size
        image = image.resize((my_width*2,my_height), resample=PilImage.NEAREST)
        image = hitherdither.ordered.bayer.bayer_dithering(image, hitherdither_palette, hitherdither_tresholds, order=hitherdither_order)
        image = image.resize((my_width,my_height), resample=PilImage.NEAREST)
    if (user_dithering.get() == 'dots') :
        hitherdither_palette = hitherdither.palette.Palette(convert_to_hitherdither_palette(my_palettedata))
        image = hitherdither.ordered.cluster.cluster_dot_dithering(image, hitherdither_palette, hitherdither_tresholds, order=hitherdither_order)

    if (user_dithering.get() == 'floyd-steinberg') :
        pal_image.putpalette(
            (my_palettedata)
            +(0,0,0)*(256-16)
        )
        quantisized_image = image.im.convert("P",1,pal_image.im)
        image = image._new(quantisized_image)

    if (user_dithering.get() == 'none') :
        pal_image.putpalette(
            (my_palettedata)
            +(0,0,0)*(256-16)
        )
        quantisized_image = image.im.convert("P",0,pal_image.im)
        image = image._new(quantisized_image)

    return image



def image_quantize_paletted_brightness(image):

    switcher_gradient_sceme = {
        'purple': GRADIENT_PURPLE_SCEME,
        'brown': GRADIENT_BROWN_SCEME,
        'gray': GRADIENT_GRAY_SCEME,
        'green': GRADIENT_GREEN_SCEME,
        'blue': GRADIENT_BLUE_SCEME,
        'green2': GRADIENT_GREEN2_SCEME,
        'custom': user_custom_gradient_sceme,
    }
    gradient_sceme = switcher_gradient_sceme.get(user_gradient_sceme.get(), GRADIENT_PURPLE_SCEME)

    switcher_gradient_colors = {
        'purple': GRADIENT_PURPLE_COLORS,
        'brown': GRADIENT_BROWN_COLORS,
        'gray': GRADIENT_GRAY_COLORS,
        'green': GRADIENT_GREEN_COLORS,
        'blue': GRADIENT_BLUE_COLORS,
        'green2': GRADIENT_GREEN2_COLORS,
        'custom': user_custom_gradient_sceme_size,
    }
    gradient_colors = switcher_gradient_colors.get(user_gradient_sceme.get(), GRADIENT_PURPLE_COLORS)


    #prepare grayscale palette
    my_palettedata = []

    for a in range (0,gradient_colors) :
        for rgb in range (0,3) :
            my_palettedata.append(
                int(round(
                    (255/(gradient_colors-1))*a
                ))
            )
    #fill the rest of the palette with 0
    for a in range (gradient_colors*3,256*3) :
            my_palettedata.append(0)

    hitherdither_tresholds = [256/user_treshold.get(), 256/user_treshold.get(), 256/user_treshold.get()]


    #quantisize image to grayscale with given grayscale palette holding (gradient_colors) number of colors
    if (user_dithering.get() == 'bayer') :
        hitherdither_palette = hitherdither.palette.Palette(convert_to_hitherdither_palette(my_palettedata))
        image = hitherdither.ordered.bayer.bayer_dithering(image, hitherdither_palette, hitherdither_tresholds, order=hitherdither_order)
    if (user_dithering.get() == 'yliluomas1') :
        hitherdither_palette = hitherdither.palette.Palette(convert_to_hitherdither_palette(my_palettedata))
        image = hitherdither.ordered.yliluoma.yliluomas_1_ordered_dithering(image, hitherdither_palette, order=hitherdither_order)
    if (user_dithering.get() == 'line') :
        hitherdither_palette = hitherdither.palette.Palette(convert_to_hitherdither_palette(my_palettedata))
        my_width, my_height = image.size
        image = image.resize((my_width*2,my_height), resample=PilImage.NEAREST)
        image = hitherdither.ordered.bayer.bayer_dithering(image, hitherdither_palette, hitherdither_tresholds, order=hitherdither_order)
        image = image.resize((my_width,my_height), resample=PilImage.NEAREST)
    if (user_dithering.get() == 'dots') :
        hitherdither_palette = hitherdither.palette.Palette(convert_to_hitherdither_palette(my_palettedata))
        image = hitherdither.ordered.cluster.cluster_dot_dithering(image, hitherdither_palette, hitherdither_tresholds, order=hitherdither_order)

    if (user_dithering.get() == 'floyd-steinberg') :
        pal_image= PilImage.new("P", (1,1))
        pal_image.putpalette(my_palettedata)
        quantisized_image = image.im.convert("P",1,pal_image.im)
        image = image._new(quantisized_image)

    if (user_dithering.get() == 'none') :
        pal_image= PilImage.new("P", (1,1))
        pal_image.putpalette(my_palettedata)
        quantisized_image = image.im.convert("P",0,pal_image.im)
        image = image._new(quantisized_image)



    #make new palette with gradient sceme
    rgb_palettedata = []
    for a in range (0,gradient_colors):
        rgb_palettedata.extend(koala_colorindex_to_rgb(gradient_sceme[a]))
    #fill the rest of the palette
    for a in range (gradient_colors*3,256*3) :
        rgb_palettedata.append(0)
    #apply new color gradient to grayscale image
    image.putpalette(rgb_palettedata)


    return image




def koala_index_to_colorindex(
    index,  #0..3
    x,
    y
) :
    location = (y*C64_CHAR_WIDTH)+x
        
    switcher = {
        0 : koala_bg,    #=koala_bg;	// pixel not set = $d021 colour
        1 : koala_col12[location] >> 4,   #=koala_col12[(y*C64_CHAR_WIDTH)+x] SHR 4;
        2 : koala_col12[location] & 0b00001111,    #=koala_col12[(y*C64_CHAR_WIDTH)+x] and %00001111;
        3 : koala_col3[location] & 0b00001111    #=koala_col3[(y*C64_CHAR_WIDTH)+x] and %00001111;
    }
    return switcher.get(index,0)




def hires_index_to_colorindex(
    index,  #0..1
    x,
    y
) :
    location = (y*C64_CHAR_WIDTH)+x
        
    switcher = {
        0 : koala_col12[location] & 0b00001111,    #=koala_col12[(y*C64_CHAR_WIDTH)+x] and %00001111;
        1 : koala_col12[location] >> 4,   #=koala_col12[(y*C64_CHAR_WIDTH)+x] SHR 4;
    }
    return switcher.get(index,0)



def koala_colorindex_to_rgb(
    index
):
    switcher_palette = {
        'pepto': PALETTEDATA_PEPTO,
        'view64': PALETTEDATA_VIEW64,
        'vice': PALETTEDATA_VICE,
        'colodore': PALETTEDATA_COLODORE,
    }
    my_palette = switcher_palette.get(user_palette.get(), PALETTEDATA_PEPTO)

    return_palette = []
    return_palette.append(my_palette[(index*3)+0])
    return_palette.append(my_palette[(index*3)+1])
    return_palette.append(my_palette[(index*3)+2])

    return return_palette




def koala_to_image(
):
    global koala_colorindex_data

    SHR_PRE = [
        6,
        4,
        2,
        0
    ]

    for y in range(0, C64_CHAR_HEIGHT):
        for x in range(0, C64_CHAR_WIDTH):
            pos = ((y*C64_CHAR_WIDTH)+x)*8
            this_block = koala_bitmap[ pos:pos+8]   #this_block holds 8 bytes
        #    print(this_block)

            for row in range(0, 8):
                this_row = this_block[row]
                
                for column in range(0, 4):
                    iy = y*8    +row
                    ix = x*4    +column

                    #normal data
                    koalaindex = (this_row >> SHR_PRE[column]) & 0b00000011 #result should be 0..3
                    koala_colorindex_data[iy*KOALA_WIDTH+ix] = koala_index_to_colorindex(koalaindex,x,y)









def hires_to_image(
):
    global koala_colorindex_data

    #constants
    SHR_PRE = [
        7,
        6,
        5,
        4,
        3,
        2,
        1,
        0
    ]

    for y in range(0, C64_CHAR_HEIGHT):
        for x in range(0, C64_CHAR_WIDTH):
            pos = ((y*C64_CHAR_WIDTH)+x)*8
            this_block = koala_bitmap[ pos:pos+8]   #this_block holds 8 bytes

            for row in range(0, 8):
                this_row = this_block[row]
                
                for column in range(0, 8):
                    my_index = (this_row >> SHR_PRE[column]) & 0b00000001 #result should be 0..1

                    iy = y*8    +row
                    ix = x*8    +column

                    hires_colorindex_data[iy*HIRES_WIDTH+ix] = hires_index_to_colorindex(my_index,x,y)


 
 
 
 

def convert_to_koala_find_replace_color(
    palette,#:array of palette_type_extra,
    replace_this
):
    # find the next better color of the 4 most used ones (color table)
    found=False;
    return_value=0
    for a in range (0,15):  #should be 0,16
        for b in range (0,4):
            if (
                (found == False) &
                (REPLACEMENT_TABLE[replace_this][a] == palette[b][0])
            ):
                return_value = palette[b][0]
                found = True
#                print('solution found: %d -> %d' %(replace_this, palette[b][0]))

    if (found == False) :
        print( 'Error in the color replacement table: ')

        print( '4 mostly used colors: ')
        #for a in range (0,4) : print ("%d " % palette[a].color),
        for a in range (0,4) : print ("%d " % palette[a][0]),
        print

        print ( 'Replacement table for color %d: '% replace_this)
        print( REPLACEMENT_TABLE[replace_this] )
        print

        return_value = palette[1][0];
        print('Dirty fix: Replacing %d with most used color %d.' % (replace_this,palette[1][0]));

    return return_value

 

def convert_to_koala_replace_colors(
    block,
    color,
    solution
):
#    print('Replacing %d -> %d in ' % (color, solution))
    for a in range (0,8) :
        for b in range (0,4) :
            if (block[a][b] == color):
#                print('block[%d,%d] ' % (a,b)),
                block[a][b] = solution
    #    print

    
    
    
def convert_to_koala_sort_palette(
    palette
):    
    #normal bubble sort, sort colors: mostly used first, least used last
    for a in range(0,16):
        for b in range(0,16):
            if (a==b) : continue
            if (palette[a][1] > palette[b][1]):
                palette[b], palette[a] = palette[a].copy(), palette[b].copy() 




def convert_to_koala_find_best_background_color(
    bmp_bitmap
) :
    """
    sets background color ($d021) to the most used color in the original image
    """    
    #my_palette = numpy.zeros((16,2), dtype=numpy.uint8)    #32 bytes 
    my_palette = [ [0] *2 for i in range(16) ]    #32 bytes 
    
    #init
    for y in range (0,16) : my_palette[y][0] = y    #color
    for y in range (0,16) : my_palette[y][1] = 0    #amount

    for y in range (0,200) :
        for x in range (0,160) :
            my_palette[bmp_bitmap[y][x]][1] += 1  #amount

    convert_to_koala_sort_palette(my_palette)
        
    return my_palette[0][0] #color



def write_color_clashes_to_json_file(
    filename_out,
    my_data
) :
    
    if ( len(my_data) > 0 ) :
        # write file
        print ('    Opening json-file "%s" for writing...' % filename_out, end='')
        try:
            file_out = open(filename_out , "w")
        except IOError as err:
            print("I/O error: {0}".format(err))
            sys.exit(1)

        json_data = {}

        #info
        my_item = {}
        my_item['program'] = PROGNAME
        my_item['version'] = VERSION
        my_item['clashes amount'] = len(my_data)
        json_data['info'] = my_item


        #Color clashes
        clash_array = []
        number = 0
        for c in my_data :
            #posx
            my_item = {}
            my_item['number'] = number
            my_item['x'] = c[0]
            my_item['y'] = c[1]
            my_item['colors used'] = c[2]
            used_colors = []
            for r in c[3] :
                used_colors.append(r)
            my_item['colors'] = used_colors
            clash_array.append( my_item )
            number += 1
        json_data['clashes'] = clash_array

        #write to file
        json.dump(json_data, file_out, indent=4)
        file_out.close()
        print("done.")

    return None


def show_color_clashes_on_console(
    my_data
) :
    if ( len(my_data) > 0 ) :
        n=1
        print('Color clashes:')
        for c in my_data :
            print('%3d: '%(n),end='')
            print('x:%2d, y:%2d, %d colors used, colors: ' %(c[0], c[1], c[2]), end='')
            for r in c[3] :
                print('%2d, '%r , end='')
            print()
            n+=1
        print('---end---')

        """
        unique_list = [list(x) for x in set(tuple(x) for x in color_clash_chars_xy)]
        color_clash_chars_xy = unique_list
        n=1
        print('unique list (should not contain duplicates):')
        for c in color_clash_chars_xy :
            print('%d: '%(n),end='')
            print(c)
            n+=1
        print('---end---')
        """




def convert_to_koala(
) :
    """
    converts a palettes image mode "P" to a koala
    also checks color clashes
    * reads: image_preview_convert
    * sets: koala_bitmap, koala_col12, koala_col3 and koala_bg
    """
    global textbox
    global koala_bitmap, koala_col12, koala_col3, koala_bg
    global color_clash_chars_xy
    
    textbox.delete('1.0', END)      #clear textbox

    block = [ [0] * 4 for i in range(8)]    #32 bytes
    bitmap = [[ [0] * 8 for i in range(40)] for i in range(25)]    #8000 bytes
    screen = [ [0] * 40 for i in range(25)]    #1000 bytes
    colram = [ [0] * 40 for i in range(25)]    #1000 bytes
    palette = [ [0] * 2 for i in range(16)]    #32 bytes   palette[x][0]=color palette  /  [x][1]=amount
    
    user_koala_bg_color = user_backgroundcolor.get()

    textbox.insert(END,"procedure \"convert_to_koala\": working...\n")
    
    root.update()


    #fill bmp_bitmap with image_preview 160x200 data
    bmp_bitmap = [ [0] * 160 for i in range(200) ]
    my_list = list(image_preview_convert.getdata()) #image is in "P" mode
    for y in range(0,200) :
        for x in range(0,160) :
            bmp_bitmap[y][x] = my_list[(y*160)+x]


    #converting to koala: begin...
    color_clash_counter = 0
    color_clash_chars_counter = 0
    background_color = 0
    

    #background color
    if (user_koala_bg_color!=99) :  #99 = automatic
        background_color = user_koala_bg_color
    else:
        background_color = convert_to_koala_find_best_background_color(bmp_bitmap);
    textbox.insert(END,"Background Color = %d\n" % background_color)



    #main loop
    color_clash_chars_xy = []
    for y in range (0,25):
        for x in range (0,40):


            #fill block with values
            for c in range (0,8):
                for d in range (0,4):
                    block[c][d] = bmp_bitmap[y*8+c][x*4+d]
            
            # count all colors in this block: make palette
            # clear palette
            for c in range (0,16):
                palette[c][0]=c  #palette[c].color
                palette[c][1]=0	# clear amount palette[c].amount

            # fill palette amount values
            for c in range (0,8):
                for d in range (0,4):
                    palette[block[c][d]][1] += 1 # increase the color-counter (palette.amount) for block[c][d]
            
            palette[background_color][1] = 99   # palette.amount BACKGROUND_COLOR always has to be in the palette
            convert_to_koala_sort_palette(palette)
#            print("sorted:")
#            print(palette)
            
            used_colors_count = 0
            used_colors_colors = []
            for c in range (0,16):
                if (palette[c][1] > 0): #palette[c].amount
                    used_colors_count += 1  #this color has already been used (amount > 0)
                    used_colors_colors.append(palette[c][0])    #store color number of used color

            if (used_colors_count > 4) :    #this character has more than 4 colors -> fix this color clash
                color_clash_chars_counter += 1
                my_coords = []
                my_coords.append(x)
                my_coords.append(y)
                my_coords.append(used_colors_count)
                my_coords.append(used_colors_colors)
                color_clash_chars_xy.append(my_coords)
                #print("x: %d, y: %d"%(x,y))
                #print(palette)
                #print("")


                for c in range (4,16):  #find a solution for fourth, fifth, sixth... color if it is used
                    if (palette[c][1]>0):   #palette[c].amount
                        color_clash_counter += 1
                        solution = convert_to_koala_find_replace_color(palette, palette[c][0])    #palette.color

                        # now really replace the colors in block[c,d]
                        convert_to_koala_replace_colors(block, palette[c][0], solution)  #palette.color

            # store colors
            screen[y][x] = palette[1][0]  #palette.color
            screen[y][x] = (screen[y][x] << 4) | palette[2][0]  #palette.color
            colram[y][x] = palette[3][0]  #palette.color


            # convert bitmap data
            for c in range (0,8):
                for d in range (0,4):
                    if (block[c][d] == background_color) :
                        block[c][d] = 0
                        continue       	# %00
                    if (block[c][d] == palette[1][0]) : #palette.color
                        block[c][d] = 1
                        continue        # %01
                    if (block[c][d] == palette[2][0]) : #palette.color
                        block[c][d] = 2
                        continue        # %10
                    if (block[c][d] == palette[3][0]) : #palette.color
                        block[c][d] = 3
                        continue;       # %11

                    # we should never reach here
                    textbox.insert(END,'Convert error in char[%d,%d]:\n'%(y,x))
                    textbox.insert(END,'Color %d in block[%d,%d] not found!\n'% (block[c][d], c, d))
                    textbox.insert(END,'Block row %d, column %d (convert bitmap data)\n' % (c,d))
                    textbox.insert(END,"\n")
                    return None # halt(1);

            # store bitmap data
            for c in range (0,8) :
                bitmap[y][x][c] = block[c][0]
                bitmap[y][x][c] = (bitmap[y][x][c] << 2) | block[c][1]
                bitmap[y][x][c] = (bitmap[y][x][c] << 2) | block[c][2]
                bitmap[y][x][c] = (bitmap[y][x][c] << 2) | block[c][3]

    textbox.insert(END,'Fixed %d color clashes in %d character blocks.\n'% (color_clash_counter, color_clash_chars_counter));

    if (args.debug_clashes) :
        show_color_clashes_on_console(color_clash_chars_xy)


    #convert to our format used in koala_to_image
    for y in range (0,25) :
        for x in range (0,40) :
            for c in range (0,8) : koala_bitmap[((y*40)+x)*8 +c] = bitmap[y][x][c]
            koala_col12[(y*40)+x] = screen[y][x]
            koala_col3[(y*40)+x] = colram[y][x]
    koala_bg = background_color
    



 
 

def convert_to_hires_find_replace_color(
    palette,#:array of palette_type_extra,
    replace_this
):
    # find the next better color of the 4 most used ones (color table)
    found=False;
    return_value=0
    for a in range (0,15):  #should be 0,16
        for b in range (0,2):
            if (
                (found == False) &
                (REPLACEMENT_TABLE[replace_this][a] == palette[b][0])
            ):
                return_value = palette[b][0]
                found = True
                #print('solution found: %d -> %d' %(replace_this, palette[b][0]))

    if (found == False) :
        print( 'Error in the color replacement table: ')

        print( '2 mostly used colors: ')
        for a in range (0,2) : print ("%d " % palette[a].color),
        print

        print ( 'Replacement table for color %d: '% replace_this)
        for a in range (0,16) : print( "%d " % REPLACEMENT_TABLE[replace_this][a]),
        print

        return_value = palette[1][0];
        print('Dirty fix: Replacing %d with most used color %d.' % (replace_this,palette[1][0]));

    return return_value

 

def convert_to_hires_replace_colors(
    block,
    color,
    solution
):
#    print('Replacing %d -> %d in ' % (color, solution))
    for a in range (0,8) :
        for b in range (0,8) :
            if (block[a][b] == color):
#                print('block[%d,%d] ' % (a,b)),
                block[a][b] = solution
    #    print

    
    




def convert_to_hires(
) :
    """
    converts a palettes image mode "P" to a hires
    also checks color clashes
    * reads: image_preview_convert
    * sets: koala_bitmap, koala_col12
    """
    global textbox
    global koala_bitmap, koala_col12
    global color_clash_chars_xy

    textbox.delete('1.0', END)      #clear textbox

    block = [ [0] * 8 for i in range(8)]    #8*8 = 64 bytes
    bitmap = [[ [0] * 8 for i in range(40)] for i in range(25)]    #25*40*8 = 8000 bytes
    screen = [ [0] * 40 for i in range(25)]    #25*40 = 1000 bytes
    palette = [ [0] * 2 for i in range(16)]    #16*2 = 32 bytes   palette[x][0]=color palette  /  [x][1]=amount
 
    
    textbox.insert(END,"procedure \"convert_to_hires\": working...\n")
    
    root.update()


    #fill bmp_bitmap with image_preview_convert data
    bmp_bitmap = [ [0] * HIRES_WIDTH for i in range(HIRES_HEIGHT)]   #200*320 = 64000 bytes
    my_list = list(image_preview_convert.getdata()) #image is in "P" mode
    for y in range(0,HIRES_HEIGHT) :
        for x in range(0,HIRES_WIDTH) :
            bmp_bitmap[y][x] = my_list[(y*HIRES_WIDTH)+x]




    #converting to hires: begin...
    color_clash_counter = 0
    color_clash_chars_counter = 0
    color_clash_chars_xy = []

    #main loop
    for y in range (0,25):
        for x in range (0,40):


            #fill block with values
            for c in range (0,8):
                for d in range (0,8):
                    block[c][d] = bmp_bitmap[y*8+c][x*8+d]
            
            # count all colors in this block: make palette
            for c in range (0,16):
                palette[c][1]=0	# clear amount palette[c].amount
                palette[c][0]=c  #palette[c].color

            for c in range (0,8):
                for d in range (0,8):
                    palette[block[c][d]][1] += 1 # palette.amount
            
            convert_to_koala_sort_palette(palette)



            used_colors_count = 0
            used_colors_colors = []
            for c in range (0,16):
                if (palette[c][1] > 0): #palette[c].amount
                    used_colors_count += 1  #this color has already been used (amount > 0)
                    used_colors_colors.append(palette[c][0])    #store color number of used color

            if (used_colors_count > 2) :    #this character has more than 2 colors -> fix this color clash
                color_clash_chars_counter += 1
                my_coords = []
                my_coords.append(x)
                my_coords.append(y)
                my_coords.append(used_colors_count)
                my_coords.append(used_colors_colors)
                color_clash_chars_xy.append(my_coords)

                for c in range (2,16):  #color[0] and color[1] of the palette are used mostly, keep them. replace the others (2..15)
                    if (palette[c][1]>0):   #palette[c].amount
                        color_clash_counter += 1
                        solution = convert_to_hires_find_replace_color(palette, palette[c][0])    #palette.color

                        # now really replace the colors in block[c,d]
                        convert_to_hires_replace_colors(block, palette[c][0], solution)  #palette.color

            # store colors
            screen[y][x] = palette[1][0]  #palette.color
            screen[y][x] = (screen[y][x] << 4) | palette[0][0]  #palette.color


            # convert bitmap data
            for c in range (0,8):
                for d in range (0,8):
                    if (block[c][d] == palette[0][0]) : #palette.color
                        block[c][d] = 0
                        continue        # %00
                    if (block[c][d] == palette[1][0]) : #palette.color
                        block[c][d] = 1
                        continue        # %01

                    # we should never reach here
                    textbox.insert(END,'Convert error in char[%d,%d]:\n'%(y,x))
                    textbox.insert(END,'Color %d in block[%d,%d] not found!\n'% (block[c][d], c, d))
                    textbox.insert(END,'Block row %d, column %d (convert bitmap data)\n' % (c,d))
                    textbox.insert(END,"\n")
                    return None # halt(1);


            # store bitmap data
            for c in range (0,8) :
                bitmap[y][x][c] = block[c][0]
                bitmap[y][x][c] = (bitmap[y][x][c] << 1) | block[c][1]
                bitmap[y][x][c] = (bitmap[y][x][c] << 1) | block[c][2]
                bitmap[y][x][c] = (bitmap[y][x][c] << 1) | block[c][3]
                bitmap[y][x][c] = (bitmap[y][x][c] << 1) | block[c][4]
                bitmap[y][x][c] = (bitmap[y][x][c] << 1) | block[c][5]
                bitmap[y][x][c] = (bitmap[y][x][c] << 1) | block[c][6]
                bitmap[y][x][c] = (bitmap[y][x][c] << 1) | block[c][7]

    textbox.insert(END,'Fixed %d color clashes in %d character blocks.\n'% (color_clash_counter, color_clash_chars_counter));

    if (args.debug_clashes) :
        show_color_clashes_on_console(color_clash_chars_xy)


    #convert to our format used in hires_to_image
    for y in range (0,25) :
        for x in range (0,40) :
            for c in range (0,8) : koala_bitmap[((y*40)+x)*8 +c] = bitmap[y][x][c]
            koala_col12[(y*40)+x] = screen[y][x]
    





def image_preview_create_effects(
    my_image
) :
    """creates the preview image 160x200 object"""

#Hue-Saturation-Lightness
#contrast

#http://pillow.readthedocs.io/en/3.4.x/reference/ImageFilter.html
    if (user_effects_blur.get() == 1) :
        my_image = my_image.filter(ImageFilter.BLUR)
    if (user_effects_detail.get() == 1) :
        my_image = my_image.filter(ImageFilter.DETAIL)
    if (user_effects_enhance.get() == 1) :
        my_image = my_image.filter(ImageFilter.EDGE_ENHANCE)
    if (user_effects_enhance_more.get() == 1) :
        my_image = my_image.filter(ImageFilter.EDGE_ENHANCE_MORE)
    if (user_effects_smooth.get() == 1) :
        my_image = my_image.filter(ImageFilter.SMOOTH)
    if (user_effects_smooth_more.get() == 1) :
        my_image = my_image.filter(ImageFilter.SMOOTH_MORE)
    if (user_effects_sharpen.get() == 1) :
        my_image = my_image.filter(ImageFilter.SHARPEN)
  
    fineness = 50.0
  
#http://pillow.readthedocs.io/en/3.1.x/reference/ImageEnhance.html
#sharpness
    enhancer = ImageEnhance.Sharpness(my_image)
    factor = int(user_sharpness.get()) / fineness
    my_image = enhancer.enhance(factor)

#color balance
    enhancer = ImageEnhance.Color(my_image)
    factor = int(user_color_saturation.get()) / fineness
    my_image = enhancer.enhance(factor)

#color brightness
    enhancer = ImageEnhance.Brightness(my_image)
    factor = int(user_brightness.get()) / fineness
    my_image = enhancer.enhance(factor)

#color contrast
    enhancer = ImageEnhance.Contrast(my_image)
    factor = int(user_contrast.get()) / fineness
    my_image = enhancer.enhance(factor)
  
    return my_image





def action_convert():
    global image_koala

    convertbutton_text.set("busy...")

    switcher_palette = {
        'pepto': PALETTEDATA_PEPTO,
        'view64': PALETTEDATA_VIEW64,
        'vice': PALETTEDATA_VICE,
        'colodore': PALETTEDATA_COLODORE,
    }
    my_palettedata = switcher_palette.get(user_palette.get(), PALETTEDATA_PEPTO)



    if (user_outputformat.get()=='koala') :
        convert_to_koala()    #reads: image_preview_convert sets koala_bitmap, koala_col12, koala_col3 and koala_bg
        koala_to_image()    #prepares koala_colorindex_data

        image_result_koala.putpalette(my_palettedata)
        image_result_koala.putdata(koala_colorindex_data)

        image_koala = image_result_koala.resize((320,200), resample=PilImage.NEAREST).convert("RGBA")
       
        
    if (user_outputformat.get()=='hires') :
        convert_to_hires()    #reads: image_preview_convert sets koala_bitmap, koala_col12
        hires_to_image()    #prepares koala_colorindex_data

        image_result_hires.putpalette(my_palettedata)
        image_result_hires.putdata(hires_colorindex_data)
        image_koala = image_result_hires.convert("RGBA")

    image_koala_new = show_color_clashes()
    image_koalaTk = ImageTk.PhotoImage(image_koala_new)
    label_koala_image.configure(image=image_koalaTk)
    label_koala_image.image = image_koalaTk # keep a reference!


#    image_koalaTk = ImageTk.PhotoImage(image_koala)
#    label_koala_image.configure(image=image_koalaTk)
#    label_koala_image.image = image_koalaTk # keep a reference!

    convertbutton_text.set("convert\nAlt+C")


def show_color_clashes():
    global image_clashes
    if (len(color_clash_chars_xy) == 0): return image_koala
    image_markers = PilImage.new("RGBA", (320,200), (0,0,0,0))
    img1 = ImageDraw.Draw(image_markers)
    for i in color_clash_chars_xy:
        img1.rectangle(
            [
                (i[0]*8, i[1]*8),           # start: x,y
                (i[0]+1)*8, (i[1]+1)*8      # end: x,y
            ],
            fill=(255,255,0,128),
            outline=(255,0,0,128)
        )
    
    image_koala_new = image_koala
    if (user_effects_showClashes.get() == 1) :
        image_koala_new = PilImage.alpha_composite(image_koala, image_markers)
        
        image_clashes = image_koala_new

        #print ('    Opening image-file "%s" for writing...' % args.clashes_image)
        #image_koala_new.save(args.clashes_image)
        #write_color_clashes_to_json_file(args.clashes_json,color_clash_chars_xy)
        #textbox.insert(END,'See files "%s" and "%s" for details.\n'% (args.clashes_json, args.clashes_image));

    return image_koala_new




def action_image_refresh():
    global image_preview
    global image_preview_convert
    global image_koala
    
    #prepare image_preview_convert (this image will be converted later)
    if (user_modes.get() == "palette") :
        #make grayscale
        enhancer = ImageEnhance.Color(image_original)
        image_grayscale = enhancer.enhance(0)
        image_preview_convert = image_preview_create_effects(image_grayscale)   #apply effects
        if (user_outputformat.get() == "koala") :
            image_preview_convert = image_preview_convert.resize((160,200), resample=PilImage.NEAREST)
        image_preview_convert = image_quantize_paletted_brightness(image_preview_convert)   #quantisize to selected gradient
        image_preview_convert = image_preview_convert.convert("RGB")
        image_preview_convert = image_quantize_c64_colors(image_preview_convert)    #map to 16 colors using normal c64 palette
    else:
        image_preview_convert = image_preview_create_effects(image_original)
        if (user_outputformat.get() == "koala") :
            image_preview_convert = image_preview_convert.resize((160,200), resample=PilImage.NEAREST)
        image_preview_convert = image_quantize_c64_colors(image_preview_convert)

    #prepare image_preview (this image will only be seen in preview window)
    if (user_outputformat.get() == "koala") :
        image_preview = image_preview_convert.resize((320,200), resample=PilImage.NEAREST)
    if (user_outputformat.get() == "hires") :
        image_preview = image_preview_convert
        
    #image_preview = image_preview.convert("RGBA")
        
    image_previewTk = ImageTk.PhotoImage(image_preview)
    label_preview_image.configure(image=image_previewTk)
    label_preview_image.image = image_previewTk # keep a reference!

    #converting every time the image is refreshed: takes a lot of time and cpu power
    #action_convert()

    image_koala_new = show_color_clashes()
    image_koalaTk = ImageTk.PhotoImage(image_koala_new)
    label_koala_image.configure(image=image_koalaTk)
    label_koala_image.image = image_koalaTk # keep a reference!





	
	

def action_preview_scale(
    scale_value
):
    action_image_refresh()



def create_empty_images():
    global label_original_image
    global image_original
    global image_originalTk
    image_original = PilImage.new("RGB",(320,200), "BLACK")
    image_originalTk = ImageTk.PhotoImage(image_original)
    label_original_image.configure(image=image_originalTk)
    label_original_image.image = image_original # keep a reference!

    global label_koala_image
    global image_koala
    global image_koalaTk
    image_koala = PilImage.new("RGB",(320,200), "BLACK")
    image_koalaTk = ImageTk.PhotoImage(image_koala)
    label_koala_image.configure(image=image_koalaTk)
    label_koala_image.image = image_koala # keep a reference!

    action_image_refresh()  #this will also create a preview image from the original image



def load_image(
	filename
):
	global label_original_image
	global image_original
	global image_originalTk
#	print("opening image \"%s\"..."%filename)
	image_original = PilImage.open(filename)
	image_original = image_original.resize((320,200), resample=PilImage.NEAREST)
	image_original = image_original.convert("RGB")
	image_originalTk = ImageTk.PhotoImage(image_original)
	label_original_image.configure(image=image_originalTk)
	label_original_image.image = image_original # keep a reference!
	action_image_refresh()



def action_OpenGradient():
    textbox.delete('1.0', END)      #clear textbox

    ftypes = [('gradient', '*.json')]
    filename = askopenfilename(filetypes = ftypes)
    if not filename : return None

    textbox.insert(END,"Reading custom gradient from file \"%s\"...\n"%filename)
    config_read(filename)

    textbox.insert(END,"%d colors read.\n"%user_custom_gradient_sceme_size)

#    for a in range(0,16) :
#        textbox.insert(END,"color %d: %d\n"%(a,user_custom_gradient_sceme[a]))

    action_image_refresh()    








def action_OpenFile():
    global user_filename_open
    user_filename_open = ""
    
    ftypes = [('Image Files', '*.tif *.jpg *.png *.bmp *.gif')]
    user_filename_open = askopenfilename(filetypes = ftypes)
    if not user_filename_open : return None
    
    loadFile(user_filename_open)



def loadFile(user_filename_open):
    global user_filename_open_textvariable

    user_filename_open_textvariable.set("\"..."+user_filename_open[-30:]+"\"")
    load_image(user_filename_open)
#    action_convert()    



def action_SaveFile():
    global user_filename_save
    user_filename_save = ""

    global textbox
    textbox.delete('1.0', END)      #clear textbox

    try:
        var_start_address = int (user_start_address.get(),16)
    except ValueError:
        var_start_address = 0
    var_start_address_checkbutton = user_start_address_checkbutton.get()
    sanity_check = TRUE

#sanity checks
    if (
        (var_start_address > 0xffff) &
        (var_start_address_checkbutton)
    ) :
        textbox.insert(END, "*** error: Start address has to be 0-65535 (2bytes).\n")
        sanity_check = FALSE


    if (user_outputformat.get() == "koala") :
        ftypes = [('koala', '*.koa')]
    if (user_outputformat.get() == "hires") :
        ftypes = [('hires', '*.hir')]
    user_filename_save = asksaveasfilename(filetypes = ftypes)

    if not user_filename_save : return None

    action_convert()

    #open file for writing...
    file_out = open(user_filename_save , "wb")

    out_buffer = []
    
    #start address
    if var_start_address_checkbutton :
        i=var_start_address & 0xff  #low
        out_buffer.append(i)
        i=var_start_address >> 8    #high
        out_buffer.append(i)
    
    #koala data
    for i in range(0,8000) : out_buffer.append(int(koala_bitmap[i]))
    for i in koala_col12 : out_buffer.append(i)
    if (user_outputformat.get() == "koala") :
        for i in koala_col3 : out_buffer.append(i)
        out_buffer.append(int(koala_bg))

    #write stuff...
    file_out.write(bytearray(out_buffer))
    file_out.close()



def action_SaveFile_clash_json():
    global user_filename_save_clash_json
    #user_filename_save_clash_json = args.clashes_json

    global textbox
    textbox.delete('1.0', END)      #clear textbox

    user_filename_save_clash_json = asksaveasfilename(filetypes = [('json', '*.json')])

    if not user_filename_save_clash_json : return None

    #write_color_clashes_to_json_file(args.clashes_json,color_clash_chars_xy)
    write_color_clashes_to_json_file(user_filename_save_clash_json,color_clash_chars_xy)



def action_SaveFile_clash_image():
    global user_filename_save_clash_image
    user_filename_save_clash_image = ""

    global textbox
    textbox.delete('1.0', END)      #clear textbox

    user_filename_save_clash_image = asksaveasfilename(filetypes = [('image', '*.png')])

    if not user_filename_save_clash_image : return None

    image_clashes.save(user_filename_save_clash_image)
    
    return None





def action_reset_modifiers():
    global scale_modifier_list
    for a in range(0,len(scale_modifier_list)):
        scale_modifier_list[a].set( scale_modifier_list_default[a])



def create_drop_down_menu (
	root
) :
    menu = Menu(root)
    root.config(menu=menu)

    filemenu = Menu(menu)

    filemenu.add_command(label="open image...", command=action_OpenFile, underline=0, accelerator="Alt+O")
    filemenu.add_command(label="save image...", command=action_SaveFile, underline=0, accelerator="Alt+S")
    filemenu.add_separator()
    filemenu.add_command(label="save color-clash image...", command=action_SaveFile_clash_image, underline=5, accelerator="Alt+C")
    filemenu.add_command(label="save color-clash json...", command=action_SaveFile_clash_json, underline=17, accelerator="Alt+J")
    filemenu.add_separator()
    filemenu.add_command(label="open custom gradient...", command=action_OpenGradient, underline=5, accelerator="Alt+G")
#    filemenu.add_command(label="save custom gradient...", command=action_SaveGradient, underline=5, accelerator="Alt+H")
    filemenu.add_separator()
    filemenu.add_command(label="about...", command=create_gui_about, underline=0, accelerator="Alt+A")
    filemenu.add_separator()
    filemenu.add_command(label="quit", command=root.quit, underline=0, accelerator="Alt+Q")

    #add all menus
    menu.add_cascade(label="menu", menu=filemenu)




def create_gui_settings_modifiers (
	root,
    _row,
    _column
) :
    global scale_modifier_list, scale_modifier_list_default

#scales modifiers
    frame_border = Frame(
        root,
        bg=BGCOLOR,
        bd=_bd,
    )
    frame_border.grid(
        row=_row,
        column=_column
    )
    frame_inner = Frame(
        frame_border,
        bg=BGCOLOR,
        bd=1,
        padx = _padx,
        pady = _pady,
        relief=RAISED
        )
    frame_inner.grid()
    frame_inner.grid_columnconfigure(0, weight=1)
    frame_inner.grid_rowconfigure(0, weight=1)

    _row=0
    label = Label(
        frame_inner,
        bg=BGCOLOR,
        text="modifiers",
        wraplength=100,
        anchor='c',
        justify='left',
        fg="#000088"
    )
    label.grid(
        row=_row,
        column=0,
        sticky=W+E
    )

    MODIFIERS = [
        #text, variable, row, column
        ("saturation", user_color_saturation, 1,0, 1,100),
        ("brightness", user_brightness, 2,0, 1,100),
        ("contrast", user_contrast, 3,0, 1,100),
        ("sharpness", user_sharpness, 4,0, 1,100),
        ("dithering treshold", user_treshold, 5,0, 2,20),
    ]

    scale_modifier_list=[]
    scale_modifier_list_default=[]
    for text, var, my_row, my_column, low, high in MODIFIERS:
        scale_modifier = Scale(
            frame_inner,
            bg=BGCOLOR,
            from_=low,
            to=high,
            orient=HORIZONTAL,
            variable=var,
            label=text,
            length=200,
            cursor=CURSOR_HAND,
            command=action_preview_scale
        )
        scale_modifier.grid(
            row=my_row,
            column=my_column,
            sticky='w'
        )
        #set default value
        scale_modifier.set(high/2)
        scale_modifier_list.append(scale_modifier)
        scale_modifier_list_default.append(high/2)
        
#        last_row = my_row
 
    button_reset = Button(
        frame_inner,
        bg=BGCOLOR,
        text = "reset",
        command=action_reset_modifiers,
        cursor=CURSOR_HAND,
    )
    button_reset.grid(
        row=my_row+1,
        column=0,
        sticky="w"
    )
           
        

def create_gui_settings_effects (
	root,
    _row,
    _column
) :
#effects checkbuttons
    frame_border = Frame(
        root,
        bg=BGCOLOR,
        bd=_bd,
    )
    frame_border.grid(
        row=_row,
        column=_column
    )
    frame_inner = Frame(
        frame_border,
        bg=BGCOLOR,
        bd=1,
        padx = _padx,
        pady = _pady,
        relief=RAISED
        )
    frame_inner.grid()
    frame_inner.grid_columnconfigure(0, weight=1)
    frame_inner.grid_rowconfigure(0, weight=1)
    
    _row = 0
    label = Label(
        frame_inner,
        bg=BGCOLOR,
        text="options",
        wraplength=100,
        anchor='c',
        justify='left',
        fg="#000088"
    )
    label.grid(
        row=_row,
        column=0,
        sticky=W+E,
        columnspan=2
    )
    EFFECTS = [
        #text, variable, row, column
        ("blur",					user_effects_blur,						1,0),
        ("detail",					user_effects_detail, 					2,0),
        ("enhance",					user_effects_enhance, 					3,0),
        ("enhance_more",			user_effects_enhance_more, 				4,0),
        ("smooth",					user_effects_smooth, 					1,1),
        ("smooth_more",				user_effects_smooth_more,				2,1),
        ("sharpen",					user_effects_sharpen,					3,1),
        ("show clashes",			user_effects_showClashes,				4,1),
 
    ]
    for text,var, my_row, my_column in EFFECTS:
        checkbutton_effects = Checkbutton(
            frame_inner,
            bg=BGCOLOR,
            text=text,
            variable=var,
            cursor=CURSOR_HAND,
            command=action_image_refresh
        )
        checkbutton_effects.grid(
            row=my_row,
            column=my_column,
            sticky=W
        )




def create_gui_settings_outputformat (
	root,
    _row,
    _column
) :
#mode radiobuttons
#http://effbot.org/tkinterbook/radiobutton.htm
    frame_border = Frame(
        root,
        bg=BGCOLOR,
        bd=_bd,
    )
    frame_border.grid(
        row=_row,
        column=_column
    )
    frame_inner = Frame(
        frame_border,
        bg=BGCOLOR,
        bd=1,
        padx = _padx,
        pady = _pady,
        relief=RAISED
        )
    frame_inner.grid()
    frame_inner.grid_columnconfigure(0, weight=1)
    frame_inner.grid_rowconfigure(0, weight=1)

    label = Label(
        frame_inner,
        bg=BGCOLOR,
        text="output format",
        wraplength=100,
        anchor="c",
        justify='left',
        fg="#000088"
    )
    label.grid(
        row=0,
        column=0,
        sticky=W+E,
        columnspan=2
    )
    MODES = [
            ("koala", "koala",1,0),
            ("hires", "hires",1,1),
    ]

    for text, mode, row, column in MODES:
        radiobutton_user_mode = Radiobutton(
            frame_inner,
            bg=BGCOLOR,
            text = text,
            value = mode,
            indicatoron=0,
            variable=user_outputformat,
            cursor=CURSOR_HAND,
            command=action_image_refresh
        )
        radiobutton_user_mode.grid(
            row=row,
            column=column,
            sticky=W+E
        )




def create_gui_settings_mode (
	root,
    _row,
    _column
) :
#mode radiobuttons
#http://effbot.org/tkinterbook/radiobutton.htm
    frame_border = Frame(
        root,
        bg=BGCOLOR,
        bd=_bd,
    )
    frame_border.grid(
        row=_row,
        column=_column
    )
    frame_inner = Frame(
        frame_border,
        bg=BGCOLOR,
        bd=1,
        padx = _padx,
        pady = _pady,
        relief=RAISED
        )
    frame_inner.grid()
    frame_inner.grid_columnconfigure(0, weight=1)
    frame_inner.grid_rowconfigure(0, weight=1)

    _row = 0
    label = Label(
        frame_inner,
        bg=BGCOLOR,
        text="mode",
        wraplength=100,
        anchor="c",
        justify='left',
        fg="#000088"
    )
    label.grid(
        row=_row,
        column=1,
        sticky=W+E
    )
    MODES = [
            ("keep colors", "colors"),
            ("brightness palette", "palette"),
    ]

    for text, mode in MODES:
        radiobutton_user_mode = Radiobutton(
            frame_inner,
            bg=BGCOLOR,
            text = text,
            value = mode,
            indicatoron=0,
            variable=user_modes,
            cursor=CURSOR_HAND,
            command=action_image_refresh
        )
        _row += 1
        radiobutton_user_mode.grid(
            row=_row,
            column=1,
            sticky=W+E
        )




def create_gui_backgroundcolor (
	root,
    _row,
    _column
) :
    frame_border = Frame(
        root,
        bg=BGCOLOR,
        bd=_bd,
    )
    frame_border.grid(
        row=_row,
        column=_column
    )
    frame_inner = Frame(
        frame_border,
        bg=BGCOLOR,
        bd=1,
        padx = _padx,
        pady = _pady,
        relief=RAISED
        )
    frame_inner.grid()
    frame_inner.grid_columnconfigure(0, weight=1)
    frame_inner.grid_rowconfigure(0, weight=1)

    _row = 0
    label = Label(
        frame_inner,
        bg=BGCOLOR,
        text="convert background $d021",
        anchor="c",
        justify='left',
        fg="#000088"
    )
    label.grid(
        row=_row,
        column=1,
        sticky=W+E,
        columnspan=8
    )

    MODES = [
            ("black", 		 0, 0,0),	#text,value,row,column
            ("white",		 1, 0,1),
            ("red",			 2, 0,2),
            ("cyan",		 3, 0,3),
            ("purple",		 4, 0,4),
            ("green",		 5, 0,5),
            ("blue",		 6, 0,6),
            ("yellow",		 7, 0,7),
            ("orange",		 8, 1,0),
            ("brown",		 9, 1,1),
            ("light red",	10, 1,2),
            ("dark gray",	11, 1,3),
            ("gray", 		12, 1,4),
            ("light green",	13, 1,5),
            ("light blue",	14, 1,6),
            ("light gray",	15, 1,7),
    ]

    for text, value, my_row, my_column in MODES:
        mycolor = '#%02x%02x%02x' % (
            PALETTEDATA_PEPTO[(value*3)+0],
            PALETTEDATA_PEPTO[(value*3)+1],
            PALETTEDATA_PEPTO[(value*3)+2]
        )
        radiobutton_user_value = Radiobutton(
            frame_inner,
            value = value,
            width=2,
            indicatoron=0,
            variable=user_backgroundcolor,
            background=mycolor,
            activebackground=mycolor,
            selectcolor=mycolor,
            cursor=CURSOR_HAND,
            bd=4,
            relief=GROOVE,
            offrelief=RAISED,
            #command=action_convert
        )
        radiobutton_user_value.grid(
            row=2+my_row,
            column=my_column,
            sticky=W+E
        )

    radiobutton_automatic = Radiobutton(
        frame_inner,
        bg=BGCOLOR,
        value = 99,
        text="auto",
        indicatoron=0,
        variable=user_backgroundcolor,
        cursor=CURSOR_HAND
        #command=action_convert
    )
    radiobutton_automatic.grid(
        row=1,
        column=0,
        sticky=W+E,
        columnspan=8
    )



def create_gui_palette_brightness_mode (
	root,
    _row,
    _column
) :
    frame_border = Frame(
        root,
        bg=BGCOLOR,
        bd=_bd,
    )
    frame_border.grid(
        row=_row,
        column=_column
    )
    frame_inner = Frame(
        frame_border,
        bg=BGCOLOR,
        bd=1,
        padx = _padx,
        pady = _pady,
        relief=RAISED
        )
    frame_inner.grid()
    frame_inner.grid_columnconfigure(0, weight=1)
    frame_inner.grid_rowconfigure(0, weight=1)

    label = Label(
        frame_inner,
        bg=BGCOLOR,
        text="brightness palette",
        wraplength=100,
        anchor="c",
        justify='left',
        fg="#000088"
    )
    label.grid(
        row=0,
        column=0,
        sticky=W+E,
        columnspan=4
    )

    MODES = [
            ("purple", "purple", 1,0),
            ("brown", "brown", 2,0),
            ("gray", "gray", 1,1),
            ("green", "green", 2,1),
            ("blue", "blue", 1,2),
            ("green2", "green2", 2,2),
            ("custom", "custom", 1,3),
    ]

    for text, mode, row, column in MODES:
        radiobutton_user_mode = Radiobutton(
            frame_inner,
            bg=BGCOLOR,
            text = text,
            value = mode,
            indicatoron=0,
            variable=user_gradient_sceme,
            command=action_image_refresh,
            cursor=CURSOR_HAND
        )
        radiobutton_user_mode.grid(
            row=row,
            column=column,
            sticky=W+E
        )



def create_gui_dithering (
	root,
    _row,
    _column
) :
    frame_border = Frame(
        root,
        bg=BGCOLOR,
        bd=_bd,
    )
    frame_border.grid(
        row=_row,
        column=_column
    )
    frame_inner = Frame(
        frame_border,
        bg=BGCOLOR,
        bd=1,
        padx = _padx,
        pady = _pady,
        relief=RAISED
        )
    frame_inner.grid()
    frame_inner.grid_columnconfigure(0, weight=1)
    frame_inner.grid_rowconfigure(0, weight=1)

    label = Label(
        frame_inner,
        bg=BGCOLOR,
        text="dithering",
        wraplength=100,
        anchor="c",
        justify='left',
        fg="#000088"
    )
    label.grid(
        row=0,
        column=0,
        sticky=W+E,
        columnspan=2
    )

    MODES = [
            ("none", "none", 1 ,0),
            ("floyd-steinberg", "floyd-steinberg", 2 ,0),
            ("bayer ordered", "bayer", 3 ,0),
            ("line", "line", 1 ,1),
            ("dots", "dots", 2 ,1),
            ("yliluomas1", "yliluomas1", 3 ,1),
    ]

    for text, mode, row, column in MODES:
        radiobutton_user_mode = Radiobutton(
            frame_inner,
            bg=BGCOLOR,
            text = text,
            value = mode,
            indicatoron=0,
            variable=user_dithering,
            command=action_image_refresh,
            cursor=CURSOR_HAND
        )
        radiobutton_user_mode.grid(
            row=row,
            column=column,
            sticky=W+E
        )




def create_gui_settings_palette (
	root,
    _row,
    _column
) :
#palette radiobuttons
#http://effbot.org/tkinterbook/radiobutton.htm
    frame_border = Frame(
        root,
        bg=BGCOLOR,
        bd=_bd,
    )
    frame_border.grid(
        row=_row,
        column=_column
    )
    frame_inner = Frame(
        frame_border,
        bg=BGCOLOR,
        bd=1,
        padx = _padx,
        pady = _pady,
        relief=RAISED
        )
    frame_inner.grid()
    frame_inner.grid_columnconfigure(0, weight=1)
    frame_inner.grid_rowconfigure(0, weight=1)

    label = Label(
        frame_inner,
        bg=BGCOLOR,
        text="palette",
        wraplength=100,
        anchor='c',
        justify='left',
        fg="#000088"
    )
    label.grid(
        row=0,
        column=0,
        sticky=W+E,
        columnspan=2
    )
    MODES = [
            ("colodore", "colodore",1,0),
            ("pepto", "pepto",2,0),
            ("view64", "view64",1,1),
            ("vice", "vice",2,1),
        ]

    for text, mode, row, column in MODES:
        radiobutton_user_mode = Radiobutton(
            frame_inner,
            bg=BGCOLOR,
            text = text,
            value = mode,
            indicatoron=0,
            variable=user_palette,
            cursor=CURSOR_HAND,
            command=action_image_refresh
        )
        radiobutton_user_mode.grid(
            row=row,
            column=column,
            sticky=W+E
        )




def create_gui_settings_startaddress (
	root,
    _row,
    _column
) :
    frame_border = Frame(
        root,
        bg=BGCOLOR,
        bd=_bd,
    )
    frame_border.grid(
        row=_row,
        column=_column
    )
    frame_inner = Frame(
        frame_border,
        bg=BGCOLOR,
        bd=1,
        padx = _padx,
        pady = _pady,
        relief=RAISED
        )
    frame_inner.grid()
    frame_inner.grid_columnconfigure(0, weight=1)
    frame_inner.grid_rowconfigure(0, weight=1)
    
    label_start_address_title = Label(
        frame_inner,
        bg=BGCOLOR,
        text="start address in hex:",
        anchor='c',
        fg="#000088"
    )
    checkbutton_start_address = Checkbutton(
        frame_inner,
        bg=BGCOLOR,
        variable = user_start_address_checkbutton
        )
    label_start_address = Label(
        frame_inner,
        bg=BGCOLOR,
        text="values $0-$ffff $",
        anchor='c'
    )
    entry_start_address= Entry(
        frame_inner,
        bg=BGCOLOR,
        width=8,
        textvariable = user_start_address
    )
    #placement in grid layout
    label_start_address_title.grid(
        row=0,
        column=0,
        sticky=W+E,
        columnspan=3
    )
    checkbutton_start_address.grid(
        row=1,
        column=0,
        sticky=W
    )
    label_start_address.grid(
        row=1,
        column=1,
        sticky=W+E
    )
    entry_start_address.grid(
        row=1,
        column=2,
        sticky=E
    )
    user_start_address.set("6000")
    user_start_address_checkbutton.set(1)






def create_gui_filename (
	root,
    _row,
    _column
) :
    
    frame_border = Frame(
        root,
        bg=BGCOLOR,
        bd=_bd,
    )
    frame_border.grid(
        row=_row,
        column=_column
    )
    frame_inner = Frame(
        frame_border,
        bg=BGCOLOR,
        bd=1,
        padx = _padx,
        pady = _pady,
        relief=RAISED
        )
    frame_inner.grid()
    frame_inner.grid_columnconfigure(0, weight=1)
    frame_inner.grid_rowconfigure(0, weight=1)
    
    label_title = Label(
        frame_inner,
        bg=BGCOLOR,
        text="image",
        anchor='c',
        fg="#000088"
    )
    label_filename = Label(
        frame_inner,
        bg=BGCOLOR,
        textvariable = user_filename_open_textvariable,
        anchor='c'
    )
    #placement in grid layout
    label_title.grid(
        row=0,
        column=0,
        sticky=W+E
    )
    label_filename.grid(
        row=1,
        column=0,
        sticky=W+E
    )






def create_gui_about (
) :
    TEXT_HEIGHT=30

    def close_window():
        global about_window
        global about_window_open
        
        if (about_window_open == True) :
            about_window.destroy()
            about_window_open = False

    def close_window_key(self):
        close_window()

    def keyboard_up(event):
        msg.yview_scroll(-1,"units")

    def keyboard_down(event):
        msg.yview_scroll(1,"units")

    def keyboard_pageup(event):
        msg.yview_scroll(TEXT_HEIGHT,"units")

    def keyboard_pagedown(event):
        msg.yview_scroll(TEXT_HEIGHT*-1,"units")


    _padx = 10
    _pady = 10
    
	#http://effbot.org/tkinterbook/toplevel.htm
    about_window = Toplevel(
        bd=10
    )
    about_window.title("About")
    about_window.configure(background=BGCOLOR)

    frame_left = Frame( about_window)
    frame_right = Frame( about_window)

    #http://effbot.org/tkinterbook/message.htm
    #text
    msg = Text(
        frame_right,
#        bd=10,
        relief=FLAT,
        width=80,
        height=30
    )

    #scrollbar
    msg_scrollBar = Scrollbar(
        frame_right,
        bg=BGCOLOR
    )
    msg_scrollBar.config(command=msg.yview)
    msg.insert(END, open(RES_DOC_ABOUT, encoding="utf_8").read())
    msg.config(yscrollcommand=msg_scrollBar.set)
    msg.config(state=DISABLED)

    #label with image
    #http://effbot.org/tkinterbook/photoimage.htm
    #image = Image.open("wolf.jpg")
    #photo = ImageTk.PhotoImage(image)
    photo = PhotoImage(file=RES_GFX_ABOUT)
    label_image = Label(
        frame_left,
        bg=BGCOLOR,
#        bd=10,
        image=photo,
        padx=_padx,
        pady=_pady
    )
    label_image.image = photo # keep a reference!

    #button
    button = Button(
        frame_left,
        bg=BGCOLOR,
        text="OK",
        command=about_window.destroy,
        padx=_padx,
        pady=_pady
    )




    #placement in grid
    frame_left.grid(
        row=0,
        column=0,
        sticky=W
    )
    frame_right.grid(
        row=0,
        column=1,
        sticky=W
    )
    
    label_image.grid(
        row=0,
        column=0,
        sticky=W
    )
    button.grid(
        row=1,
        column=0,
        sticky=W+E
    )

    msg.grid(
        row=0,
        column=0,
        sticky=W
    )
    msg_scrollBar.grid(
        row=0,
        column=1,
        sticky=N+S
    )

    about_window.bind('<Up>', keyboard_up) 
    about_window.bind('<Down>', keyboard_down) 
    about_window.bind('<Next>', keyboard_pageup) 
    about_window.bind('<Prior>', keyboard_pagedown) 




	

def create_gui_action_buttons (
	root,
    _row,
    _column
) :
    frame_border = Frame(
        root,
        bg=BGCOLOR,
        bd=_bd,
    )
    frame_border.grid(
        row=_row,
        column=_column
    )
    frame_inner = Frame(
        frame_border,
        bg=BGCOLOR,
        bd=1,
        padx = _padx,
        pady = _pady,
        relief=RAISED
        )
    frame_inner.grid()
    frame_inner.grid_columnconfigure(0, weight=1)
    frame_inner.grid_rowconfigure(0, weight=1)
    
    button_convert = Button(
        frame_inner,
        bg=BGCOLOR,
        textvariable = convertbutton_text,
        width=7,
        height=3,
        command=action_convert,
        cursor=CURSOR_HAND
    )
    #placement in grid layout
    button_convert.grid(
        row=0,
        column=0,
        sticky=W+E
    )






def create_gui_text (
    root,
    _row,
    _column
) :
    #creation of elements
    global textbox

    frame_border = Frame(
        root,
        bg=BGCOLOR,
        bd=_bd,
    )
    frame_border.grid(
        row=_row,
        column=_column
    )
    frame_inner = Frame(
        frame_border,
        bg=BGCOLOR,
        bd=1,
        padx = _padx,
        pady = _pady,
        relief=RAISED
        )
    frame_inner.grid()
    frame_inner.grid_columnconfigure(0, weight=1)
    frame_inner.grid_rowconfigure(0, weight=1)

    label_textbox_text = Label(
		frame_inner,
        bg=BGCOLOR,
		text="converter output",
        fg="#000088"
	)
    textbox = Text(
        frame_inner,
        height=10,
        width=40
    )

    #placement in grid layout
    label_textbox_text.grid(
        row=0,
        column=0,
        sticky=W+E
    )
    textbox.grid(
        row=1,
        column=0,
        sticky=W+E
    )







def create_gui_image_original (
	root,
    _row,
    _column
) :
    global label_original_image
    
    frame_border = Frame(
        root,
        bg=BGCOLOR,
        bd=_bd,
    )
    frame_border.grid(
        row=_row,
        column=_column
    )
    frame_inner = Frame(
        frame_border,
        bg=BGCOLOR,
        bd=1,
        padx = _padx,
        pady = _pady,
        relief=RAISED
        )
    frame_inner.grid()
    frame_inner.grid_columnconfigure(0, weight=1)
    frame_inner.grid_rowconfigure(0, weight=1)
    
    #creation of elements
    label_original_text = Label(
		frame_inner,
        bg=BGCOLOR,
		text="original",
        fg="#000088"
	)
    label_original_image = Label(
        frame_inner,
        bg=BGCOLOR
    )
	
    #placement in grid layout
    label_original_text.grid(
        row=0,
        column=0,
        sticky=W+E
    )
    label_original_image.grid(
        row=1,
        column=0,
        sticky=W+E
    )



def create_gui_image_preview (
	root,
    _row,
    _column
) :
    global label_preview_image
    
    frame_border = Frame(
        root,
        bg=BGCOLOR,
        bd=_bd,
    )
    frame_border.grid(
        row=_row,
        column=_column
    )
    frame_inner = Frame(
        frame_border,
        bg=BGCOLOR,
        bd=1,
        padx = _padx,
        pady = _pady,
        relief=RAISED
        )
    frame_inner.grid()
    frame_inner.grid_columnconfigure(0, weight=1)
    frame_inner.grid_rowconfigure(0, weight=1)
    
    #creation of elements
    label_preview_text = Label(
		frame_inner,
        bg=BGCOLOR,
		text="preview",
        fg="#000088"
	)
    label_preview_image = Label(
        frame_inner,
        bg=BGCOLOR
    )
	
    #placement in grid layout
    label_preview_text.grid(
        row=0,
        column=0,
        sticky=W+E
    )
    label_preview_image.grid(
        row=1,
        column=0,
        sticky=W+E
    )




def create_gui_image_koala (
	root,
    _row,
    _column
) :
    global label_koala_image
    
    frame_border = Frame(
        root,
        bg=BGCOLOR,
        bd=_bd,
    )
    frame_border.grid(
        row=_row,
        column=_column
    )
    frame_inner = Frame(
        frame_border,
        bg=BGCOLOR,
        bd=1,
        padx = _padx,
        pady = _pady,
        relief=RAISED
        )
    frame_inner.grid()
    frame_inner.grid_columnconfigure(0, weight=1)
    frame_inner.grid_rowconfigure(0, weight=1)
    
    #creation of elements
    label_koala_text = Label(
		frame_inner,
        bg=BGCOLOR,
		text="output",
        fg="#000088"
	)
    label_koala_image = Label(
        frame_inner,
        bg=BGCOLOR
    )
	
    #placement in grid layout
    label_koala_text.grid(
        row=0,
        column=0,
        sticky=W+E
    )
    label_koala_image.grid(
        row=1,
        column=0,
        sticky=W+E
    )





#keyboard shortcuts
def keyboard_quit(self):
    root.quit()
def keyboard_OpenFile(self):
    action_OpenFile()
def keyboard_SaveFile(self):
    action_SaveFile()
def keyboard_About(self):
    create_gui_about()
def keyboard_Convert(self):
    action_convert()
def keyboard_OpenGradient(self):
    action_OpenGradient()




def _main_procedure() :
    global args
    print("%s %s *** by fieserWolF"% (PROGNAME, VERSION))

    #https://docs.python.org/3/library/argparse.html
    parser = argparse.ArgumentParser(
        description='This program reads an image-file, lets the user adjust settings and converts it to a C64 koala or hires image.',
        epilog='Example: '+sys.argv[0]+' -i image.png -c /tmp/clashes.json -d'
    )
    parser.add_argument('-i', '--image', dest='input_image', help='image file)')
    #parser.add_argument('-c', '--clashes', dest='clashes_json', help='filename of report containing all color-clashes (in json-format (default="'+FILENAME_JSON_PRE+'")', default=FILENAME_JSON_PRE)
    #parser.add_argument('-o', '--output', dest='clashes_image', help='filename of color-clash image (default="'+FILENAME_CLASH_IMAGE_PRE+'")', default=FILENAME_CLASH_IMAGE_PRE)
    parser.add_argument('-d', '--debug', dest='debug_clashes', help='show color-clashes on consule', action='store_true')
    args = parser.parse_args()

    _start_gui()

    if (args.input_image) :
        loadFile(args.input_image)

    mainloop()

    
def _start_gui() :
    #main procedure
    title_string = PROGNAME+" "+VERSION
    root.title(title_string)
    #print("%s %s *** by WolF"% (PROGNAME, VERSION))

    root.configure(background=BGCOLOR)
    root.iconphoto(False, PhotoImage(file=RES_GFX_ICON))


    root.grid_columnconfigure(0, weight=10)
    root.grid_rowconfigure(0, weight=10)


    frame_left = Frame(root, bg=BGCOLOR)
    frame_left.grid(
        row=0,
        column=0,
        sticky=N
    )
    frame_left.grid_columnconfigure(0, weight=1)
    frame_left.grid_rowconfigure(0, weight=1)

    frame_middle = Frame(root, bg=BGCOLOR)
    frame_middle.grid(
        row=0,
        column=1,
        sticky=N
    )
    frame_middle.grid_columnconfigure(0, weight=1)
    frame_middle.grid_rowconfigure(0, weight=1)

    frame_right = Frame(root, bg=BGCOLOR)
    frame_right.grid(
        row=0,
        column=2,
        sticky=N
    )
    frame_right.grid_columnconfigure(0, weight=1)
    frame_right.grid_rowconfigure(0, weight=1)


    create_drop_down_menu(
        root
    )


    #frame_left elements
    create_gui_settings_outputformat(
        frame_left,
        0,  #row
        0   #column
    )
    create_gui_settings_modifiers(
        frame_left,
        1,  #row
        0   #column
    )

    create_gui_action_buttons (
        frame_left,
        2,  #row
        0   #column
    )

    create_gui_settings_effects(
        frame_left,
        3,  #row
        0   #column
    )
    create_gui_settings_palette(
        frame_left,
        4,  #row
        0   #column
    )




    #frame_middle elements
    create_gui_image_koala(
        frame_middle,
        0,  #row
        0   #column
    )
    create_gui_image_preview(
        frame_middle,
        1,  #row
        0   #column
    )
    create_gui_image_original(
        frame_middle,
        2,  #row
        0   #column
    )


    #frame_right elements
    create_gui_filename(
        frame_right,
        0,  #row
        0   #column
    )
    create_gui_settings_mode(
        frame_right,
        1,  #row
        0   #column
    )
    create_gui_palette_brightness_mode(
        frame_right,
        2,  #row
        0   #column
    )
    create_gui_dithering(
        frame_right,
        3,  #row
        0   #column
    )
    create_gui_backgroundcolor(
        frame_right,
        4,  #row
        0   #column
    )
    create_gui_settings_startaddress(
        frame_right,
        5,  #row
        0   #column
    )
    create_gui_text(
        frame_right,
        6,  #row
        0   #column
    )

            
    root.bind_all("<Alt-q>", keyboard_quit)
    root.bind_all("<Alt-o>", keyboard_OpenFile)
    root.bind_all("<Alt-s>", keyboard_SaveFile)
    root.bind_all("<Alt-a>", keyboard_About)
    root.bind_all("<Alt-c>", keyboard_Convert)
    root.bind_all("<Alt-g>", keyboard_OpenGradient)
    #root.bind_all("<Alt-h>", keyboard_SaveGradient)

    create_empty_images()
    
    



if __name__ == '__main__':
    _main_procedure()
