#!/usr/bin/env python

"""
Convertron3000 Commodore 64 graphics converter
Copyright (C) 2017 fieserWolF / Abyss-Connection

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

For Python2.7, The Python Imaging Library (PIL), Numpy, Tcl/Tk and other used source licenses see file "LICENSE_OTHERS".
"""

#to do
##########
#https://github.com/justmao945/lab/tree/master/halftoning/ordered-dithering
#ordered-dithering
#the big problem is: you cannot specify a palette to map to!
#so the results are not optimal... (to do)
#
#ordered dithering: too high values in ordered dithering modes. If you lower those values down it would look better. Probably adding a slider to control strenght of ordered dithering would be good feature.




about_graphic = """
R0lGODdhZABkAOf/AAABACAjNy0lOSYqNywqNyksQDMsQDIwPTQ0RzA2RDo0STY3PzE3Tzo3RT42
RSw7SzE7Rig+TSw+RzM+SS5ASitBUDBCTDs/TEI9TDlAUT5ASD8/VDJETi9FVDRGUC5FdjJIVz5E
YTZIUjRKWTNKXkVFWzpJWUhHVUdIUDpJbThLYDJNYUJJWzpMVjZNXD1MXD9NXjlPXjVQZEZNVDFO
ijxPZDhQak9LWjxPbjdSZjxSYTRUbUlObFBNYz1TYzFVgUBTaTpVaU1RXlZQWkRSgCdbgz9WcThW
h0lTd0FXZz1YbThZckRXbEJXeTtZelhUallVZUNadUdacEFccEpZdVRYZjlcoT9feUdeeUJff0Zg
dEBdqFJcfUVdnFxccF5ca2NbckpgkkRkfj9lg0djgz1joUtjfltfeEJoh0Vmk2Nge0Rojkpnh01m
jU9nglRmiUpqhGFjhlhmj05qi2VleltnhFdrjT9xnExsq1ZtiVJuj09umlNtn01wlUJ1k1ZvllJz
jW5sgVVyk19vmEdzuk91lFFxuWVwiVB0rG9vik14nFF2qHtthlt1lm1xkVV3nU55pWtyl1t1qV12
nm10h1l3pXVxmV58qk+AsVx+pFd/q1iAoW97mVt/smZ8sVaBuVV/0VCDwG5+pGCBu3t+l2+AsVSJ
wF6Fy1yHv2KGuVyKrVuJu2KItHyCqliMtmqJrmmHyFiRwoaGqGeOu2OO0l2RyWOQwl6SvW+Mzl+R
z26Qto2JpmaQ3VqYtHqPuWySyWSXu4eNuYKPtWGaxICRw4OTsXGXxWeZz32TzGObzHmWxXaYv2uZ
23We2HCf6W2i13+eynakxG+ny3il0Gqp03Ws4Huz6X2z9n+24Hu63n682oHB2IjE6YbF8IzD+o3N
6JjM6JPY8ZfY6KLg/J7k+6Tk9aTt/Kzs/Z7y/6f1/aD3/rH0/qr4/6f6+rH6/Kr8/a/966L//qT/
/7r5/aj/+av+/q3/8rH++az//63//7X+/7b/87b//7r/+8P//f7//CwAAAAAZABkAAAI/gDRCRSY
rmC6gQMPJjTI0CC7dO3aqWNHkV3Eixgz1tuIb2NEdyBBXqzXzh1Gi+02eswYUaXKiAjRMZSpkKbC
hgwropxYkeVIlyrxCQVKtKjHlz9JGo0JoKnTpumeSnX6cCqAduysat3KVWq9rgA2PgWKsOm/s2id
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
MA
"""




#import hitherdither    #does not work
import struct
import numpy
from Tkinter import *
import tkMessageBox
from tkFileDialog import askopenfilename, asksaveasfilename
from PIL import Image, ImageTk, ImageEnhance, ImageFilter
import ConfigParser



#global constants
def _global_constants():
        return None
PROGNAME = 'CONVERTRON3000';
VERSION = '1.01';
DATUM = '22.04.2017';
C64_CHAR_HEIGHT=25  #200/8
C64_CHAR_WIDTH=40   #320/8


_padx = 2
_pady = 2
_bd = 4


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
    0,   0,   0,	#0
    250, 250, 250,	#1
    127,  39,  52,	#2
    111, 192, 180,	#3
    135,  60, 149,	#4
     86, 156,  73,	#5
     62,  62, 142,	#6
    187, 187, 106,	#7
    134,  61,  39,	#8
     85,  44,   0,	#9
    174,  86,  99,	#10
     78,  78,  78,	#11
    117, 117, 117,	#12
    148, 218, 135,	#13
    117, 117, 197,	#14
    156, 156, 156	#15
)

PALETTEDATA_VICE = (
    0,   0,   0,	#0
    255, 255, 255,	#1
    146,  74,  64,	#2
    132, 197, 204,	#3
    147,  81, 182,	#4
    114, 177,  75,	#5
     72,  58, 170,	#6
    213, 223, 124,	#7
    153, 105,  45,	#8
    103,  82,   0,	#9
    193, 129, 120,	#10
     92,  92,  92,	#11
    151, 151, 151,	#12
    179, 236, 145,	#13
    135, 139, 221,	#14
    200, 200, 200	#15
)

PALETTEDATA_COLODORE = (
    0,   0,   0,	#0
    255, 255, 255,	#1
    129,  51, 56,	#2
    117, 206, 200,	#3
    142,  60, 151,	#4
    86, 172,  77,	#5
    46,  44, 155,	#6
    237, 241, 113,	#7
    142,  80,  41,	#8
    85,  56,   0,	#9
    196, 108, 113,	#10
    74,  74,  74,	#11
    123, 123, 123,	#12
    169, 255, 159,	#13
    112, 109, 235,	#14
    178, 178, 178	#15
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
REPLACEMENT_TABLE = numpy.array([
    [	11,	6,	2,	5,	9,	12,	8,	4,	10,	7,	14,	13,	3,	15,	1],#00 black    
    [	15,	3,	13,	14,	7,	10,	7,	8,	12,	9,	5,	2,	6,	11,	0],#01 white
    [	8,	9,	10,	0,	4,	11,	6,	5,	12,	7,	14,	13,	3,	15,	1],#02 red
    [	14,	13,	15,	10,	12,	7,	1,	6,	5,	8,	2,	9,	4,	11,	0],#03 cyan
    [	6,	8,	10,	2,	9,	11,	12,	13,	14,	7,	5,	0,	3,	15,	1],#04 purple
    [	13,	3,	11,	12,	6,	2,	9,	0,	4,	8,	10,	14,	7,	15,	1],#05 green
    [	14,	4,	0,	2,	9,	5,	3,	11,	12,	8,	10,	7,	13,	15,	1],#06 blue
    [	1,	13,	3,	15,	14,	10,	8,	12,	11,	4,	5,	6,	2,	9,	0],#07 yellow
    [	2,	9,	10,	7,	15,	13,	14,	3,	1,	4,	5,	6,	11,	12,	0],#08 light brown
    [	2,	8,	10,	11,	0,	6,	5,	12,	4,	7,	14,	13,	3,	15,	1],#09 brown
    [	8,	7,	2,	9,	15,	12,	11,	6,	5,	4,	0,	10,	14,	15,	1],#10 light-red
    [	12,	0,	15,	2,	9,	8,	6,	5,	4,	10,	7,	14,	13,	3,	1],#11 dark-gray
    [	11,	15,	0,	2,	9,	8,	6,	5,	4,	10,	7,	14,	13,	3,	1],#12 gray
    [	3,	5,	7,	15,	14,	10,	12,	11,	8,	1,	4,	9,	2,	6,	0],#13 light-green
    [	3,	6,	1,	13,	15,	10,	8,	4,	7,	12,	5,	2,	11,	9,	0],#14 light-blue
    [	1,	12,	11,	7,	13,	14,	4,	10,	8,	9,	5,	2,	6,	3,	0] #15 light-gray
], dtype=numpy.uint8)

CURSOR_HAND = 'hand2'

CONFIG_FILENAME = "convertron3000.ini"  #"c:\\convertron3000.ini"



#global variables
def _global_variables():
        return None
        
root = Tk()

user_filename_open = "none"
user_filename_save = "none"

user_start_address = StringVar()
user_start_address_checkbutton = IntVar()
user_sharpness = IntVar()
user_color_saturation = IntVar()
user_brightness = IntVar()
user_contrast = IntVar()
user_modes = StringVar()
user_outputformat = StringVar()
user_palette = StringVar()
user_filename_open_textvariable = StringVar()


user_effects_blur = IntVar()
user_effects_detail = IntVar()
user_effects_enhance = IntVar()
user_effects_enhance_more = IntVar()
user_effects_smooth = IntVar()
user_effects_smooth_more = IntVar()
user_effects_sharpen = IntVar()
user_effects_dither_floyd_steinberg = IntVar()
user_effects_dither_ordered1 = IntVar()
user_effects_dither_ordered2 = IntVar()

user_gradient_sceme = StringVar()
user_backgroundcolor = IntVar()
user_backgroundcolor.set(99)


#defaults
user_outputformat.set("koala")
user_modes.set("colors")
user_palette.set("colodore")
user_gradient_sceme.set("purple")
user_filename_open_textvariable.set("none")


textbox = Text()
label_original_image = Label()
label_preview_image = Label()
label_koala_image = Label()
image_original = Image.new("RGB", (320, 200), "black")
image_preview = Image.new("RGB", (320, 200), "black")
image_koala = Image.new("RGB", (320, 200), "black")
image_preview_convert = Image.new("RGB", (160, 200), "black")

temp=[None]*8
koala_bitmap=[None]*1000
for a in range(0,1000) : koala_bitmap.append(temp)
koala_col12=[None]*1000
koala_col3=[None]*1000
koala_bg=0

#initialize empty 320x200 data
#koala_preview_image_data = [['None']*320] * 200
koala_preview_image_data = numpy.zeros((200, 160, 3), dtype=numpy.uint8)
hires_preview_image_data = numpy.zeros((200, 320, 3), dtype=numpy.uint8)

scale_modifier_list=[]

config = ConfigParser.RawConfigParser()
user_custom_gradient_sceme = numpy.array([0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0])
user_custom_gradient_sceme_size = 0



#https://docs.python.org/2.7/library/configparser.html#examples
def config_write(
    filename
) :
    section = 'paletted brightness'
    user_brightnesspalette_size = 16
    user_brightnesspalette_color = [
        3,4,5,6,7,8,9,10,11,12,123,14,15,1,16,17
    ]
    
    config.add_section(section)
    config.set(section, 'size', user_brightnesspalette_size)
    for a in range(0,user_brightnesspalette_size) :
        config.set(section, 'color'+str(a), user_brightnesspalette_color[a])

    # Writing our configuration file to 'example.cfg'
    with open(filename, 'wb') as configfile:
        config.write(configfile)

    return None


#https://docs.python.org/2.7/library/configparser.html#examples
def config_read(
    filename
) :
    global user_custom_gradient_sceme
    global user_custom_gradient_sceme_size
    
    config.read(filename)
    section = 'paletted brightness'

    user_custom_gradient_sceme_size = config.getint(section, 'size')

    for a in range(0,16) :
        user_custom_gradient_sceme[a] = config.getint(section, 'color'+str(a))        
        
    return None






def gen_matrix( e ):
#https://github.com/justmao945/lab/tree/master/halftoning/ordered-dithering
  ''' Generating new matrix.
      @param e The width and height of the matrix is 2^e.
      @return New 2x2 to 2^e x 2^e matrix list.
  '''
  if e < 1: return None
  m_list = [ [[1,2],[3,0]] ]
  _b = m_list[0]
  for n in xrange(1, e):
    m = m_list[ n - 1 ]
    m_list.append( [
      [4*i+_b[0][0] for i in m[0]] + [4*i+_b[0][1] for i in m[0]],
      [4*i+_b[0][0] for i in m[1]] + [4*i+_b[0][1] for i in m[1]],
      [4*i+_b[1][0] for i in m[0]] + [4*i+_b[1][1] for i in m[0]],
      [4*i+_b[1][0] for i in m[1]] + [4*i+_b[1][1] for i in m[1]],
    ] )
  return m_list


def ordered_dithering( pixel, size, matrix ):
#https://github.com/justmao945/lab/tree/master/halftoning/ordered-dithering
    """ Dithering on a single channel.
    @param pixel PIL PixelAccess object.
    @param size A tuple to represent the size of pixel.
    @param matrix Must be NxN, and N == 2^e where e>=1
    """
    X, Y = size
    N = len(matrix)

    T = [[255*(matrix[x][y]+0.5)/N/N for x in xrange(N)] for y in xrange(N)]
    for y in xrange(0, Y):
        for x in xrange(0, X):
            pixel[x,y] = 255 if pixel[x,y] > T[x%N][y%N] else 0









def image_quantize_c64_colors(image):
    pal_image= Image.new("P", (1,1))

    switcher_palette = {
        'pepto': PALETTEDATA_PEPTO,
        'view64': PALETTEDATA_VIEW64,
        'vice': PALETTEDATA_VICE,
        'colodore': PALETTEDATA_COLODORE,
    }
    my_palettedata = switcher_palette.get(user_palette.get(), PALETTEDATA_PEPTO)
    
    pal_image.putpalette(
        (my_palettedata)
        +(0,0,0)*(256-16)
    )
    
    #https://github.com/justmao945/lab/tree/master/halftoning/ordered-dithering
    """
    ordered-dithering
    the big problem is: you cannot specify a palette to map to!
    so the results are not optimal... (to do)
    """
    e=0
    if (int(user_effects_dither_ordered1.get())== 1) : e=1
    if (int(user_effects_dither_ordered2.get())== 1) : e=2
    if (e>0):            # only values 1 and 2 will result in ordered dithering
        image = image.convert('CMYK').split()
        for ch in image:
            ordered_dithering(ch.load(), ch.size, gen_matrix(e)[e-1])
        image = Image.merge("CMYK",image).convert("RGB")

    #quantizise to palette (either undithered or floyd_steinberg dithered
    quantisized_image = image.im.convert(
        "P",
        int(user_effects_dither_floyd_steinberg.get()),
        pal_image.im
    )
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

    pal_image= Image.new("P", (1,1))
    pal_image.putpalette(my_palettedata)
    
    #quantisize image to grayscale with given grayscale palette holding (gradient_colors) number of colors
    quantisized_image = image.im.convert(
        "P",
        int(user_effects_dither_floyd_steinberg.get()),              # no dithering
        pal_image.im
    )
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
    #constants
    SHR_PRE = [
        6,
        4,
        2,
        0
    ]
    
    global koala_preview_image_data

    for y in range(0, C64_CHAR_HEIGHT):
        for x in range(0, C64_CHAR_WIDTH):
            this_block = koala_bitmap[ (y*C64_CHAR_WIDTH+x)]   #this_block holds 8 bytes

            for row in range(0, 8):
                this_row = this_block[row]
                
                for column in range(0, 4):
                    koalaindex = (this_row >> SHR_PRE[column]) & 0b00000011 #result should be 0..3
                    colorindex = koala_index_to_colorindex(koalaindex,x,y)
                    rgb_color = koala_colorindex_to_rgb(colorindex) #rgb_color holds 3 bytes
                    
                    iy = y*8    +row
                    ix = x*4    +column
                                        
                    koala_preview_image_data[iy][ix] = rgb_color 
    return None





def hires_to_image(
):
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
    
    global koala_preview_image_data

    for y in range(0, C64_CHAR_HEIGHT):
        for x in range(0, C64_CHAR_WIDTH):
            this_block = koala_bitmap[ (y*C64_CHAR_WIDTH+x)]   #this_block holds 8 bytes

            for row in range(0, 8):
                this_row = this_block[row]
                
                for column in range(0, 8):
                    hiresindex = (this_row >> SHR_PRE[column]) & 0b00000001 #result should be 0..1
                    colorindex = hires_index_to_colorindex(hiresindex,x,y)
                    rgb_color = koala_colorindex_to_rgb(colorindex) #rgb_color holds 3 bytes
                    
                    iy = y*8    +row
                    ix = x*8    +column
                                        
                    hires_preview_image_data[iy][ix] = rgb_color 
    return None





 
 
 
 

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
        for a in range (0,4) : print ("%d " % palette[a].color),
        print

        print ( 'Replacement table for color %d: '% replace_this)
        for a in range (0,16) : print( "%d " % REPLACEMENT_TABLE[replace_this][a]),
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
    return None

    
    
    
def convert_to_koala_sort_palette(
    palette
):
    #normal bubble sort
    for a in range(0,16):
        for b in range(0,16):
            if (a==b) : continue
            if (palette[a,1] > palette[b,1]):
                palette[b], palette[a] = palette[a].copy(), palette[b].copy() 
    return palette




def convert_to_koala_find_best_background_color(
    bmp_bitmap
) :
    """
    sets background color ($d021) to the most used color in the original image
    """    
    my_palette = numpy.zeros((16,2), dtype=numpy.uint8)    #32 bytes 
    
    #init
    for y in range (0,16) : my_palette[y][0] = y    #color
    for y in range (0,16) : my_palette[y][1] = 0    #amount

    for y in range (0,200) :
        for x in range (0,160) :
            my_palette[bmp_bitmap[y][x]][1] += 1  #amount

    convert_to_koala_sort_palette(my_palette)
        
    return my_palette[0][0] #color
    



def convert_to_koala(
) :
    """
    converts a palettes image mode "P" to a koala
    also checks color clashes
    * reads: image_preview_convert
    * sets: koala_bitmap, koala_col12, koala_col3 and koala_bg
    """
    global textbox
    global koala_bg
    
    textbox.delete('1.0', END)      #clear textbox

    block = numpy.zeros((8, 4), dtype=numpy.uint8)  #32 bytes
    bitmap = numpy.zeros((25,40,8), dtype=numpy.uint8)  #8000 bytes
    screen = numpy.zeros((25,40), dtype=numpy.uint8)    #1000 bytes
    colram = numpy.zeros((25,40), dtype=numpy.uint8)    #1000 bytes
    palette = numpy.zeros((16,2), dtype=numpy.uint8)    #32 bytes   palette[x][0]=color palette[x][1]=amount
    
    user_koala_bg_color = user_backgroundcolor.get()

    textbox.insert(END,"procedure \"convert_to_koala\": working...\n")
    
    root.update()


    #fill bmp_bitmap with image_preview 160x200 data
    bmp_bitmap = numpy.zeros((200, 160), dtype=numpy.uint8)
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
    for y in range (0,25):
        for x in range (0,40):


            #fill block with values
            for c in range (0,8):
                for d in range (0,4):
                    block[c][d] = bmp_bitmap[y*8+c][x*4+d]
            
            # count all colors in this block: make palette
            for c in range (0,16):
                palette[c][1]=0	# clear amount palette[c].amount
                palette[c][0]=c  #palette[c].color

            for c in range (0,8):
                for d in range (0,4):
                    palette[block[c][d]][1] += 1 # buggy? palette.amount
            
            palette[background_color][1] = 99   # palette.amount BACKGROUND_COLOR always has to be in the palette
            convert_to_koala_sort_palette(palette)



            used_colors_count = 0
            for c in range (0,16):
                if (palette[c][1] > 0): #palette[c].amount
                    used_colors_count += 1  #this color has already been used (amount > 0)

            if (used_colors_count > 4) :    #this character has more than 4 colors -> fix this color clash
                color_clash_chars_counter += 1

                for c in range (4,16):  #
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

    #convert to our format used in koala_to_image
    for y in range (0,25) :
        for x in range (0,40) :
            koala_bitmap[(y*40)+x] = bitmap[y][x].copy()
            koala_col12[(y*40)+x] = screen[y][x].copy()
            koala_col3[(y*40)+x] = colram[y][x].copy()
    koala_bg = background_color
    
    return None



 
 

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
    return None

    
    




def convert_to_hires(
) :
    """
    converts a palettes image mode "P" to a hires
    also checks color clashes
    * reads: image_preview_convert
    * sets: koala_bitmap, koala_col12
    """
    global textbox
    
    textbox.delete('1.0', END)      #clear textbox

    block = numpy.zeros((8, 8), dtype=numpy.uint8)  #64 bytes
    bitmap = numpy.zeros((25,40,8), dtype=numpy.uint8)  #8000 bytes
    screen = numpy.zeros((25,40), dtype=numpy.uint8)    #1000 bytes
    palette = numpy.zeros((16,2), dtype=numpy.uint8)    #32 bytes   palette[x][0]=color palette[x][1]=amount
    
    textbox.insert(END,"procedure \"convert_to_hires\": working...\n")
    
    root.update()


    #fill bmp_bitmap with image_preview_convert data
    bmp_bitmap = numpy.zeros((200, 320), dtype=numpy.uint8)
    my_list = list(image_preview_convert.getdata()) #image is in "P" mode
    for y in range(0,200) :
        for x in range(0,320) :
            bmp_bitmap[y][x] = my_list[(y*320)+x]




    #converting to hires: begin...
    color_clash_counter = 0
    color_clash_chars_counter = 0

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
                    palette[block[c][d]][1] += 1 # buggy? palette.amount
            
            convert_to_koala_sort_palette(palette)



            used_colors_count = 0
            for c in range (0,16):
                if (palette[c][1] > 0): #palette[c].amount
                    used_colors_count += 1  #this color has already been used (amount > 0)

            if (used_colors_count > 2) :    #this character has more than 2 colors -> fix this color clash
                color_clash_chars_counter += 1

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

    #convert to our format used in koala_to_image
    for y in range (0,25) :
        for x in range (0,40) :
            koala_bitmap[(y*40)+x] = bitmap[y][x].copy()
            koala_col12[(y*40)+x] = screen[y][x].copy()
    
    return None






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
    if (user_outputformat.get()=='koala') :
#        image_koala = image_koala_create()
        convert_to_koala()    #reads: image_preview_convert sets koala_bitmap, koala_col12, koala_col3 and koala_bg
        koala_to_image()    #prepares koala_preview_image_data
        image_koala = Image.fromarray(koala_preview_image_data, 'RGB')
        image_koala = image_koala.resize((320,200))
       
        
    if (user_outputformat.get()=='hires') :
#        image_koala = image_hires_create()
        convert_to_hires()    #reads: image_preview_convert sets koala_bitmap, koala_col12
        hires_to_image()    #prepares hires_preview_image_data
        image_koala = Image.fromarray(hires_preview_image_data, 'RGB')
        #image_koala = image_koala.resize((320,200))
        
        
    image_koalaTk = ImageTk.PhotoImage(image_koala)
    label_koala_image.configure(image=image_koalaTk)
    label_koala_image.image = image_koalaTk # keep a reference!
    return None




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
            image_preview_convert = image_preview_convert.resize((160,200))
        image_preview_convert = image_quantize_paletted_brightness(image_preview_convert)   #quantisize to selected gradient
        image_preview_convert = image_preview_convert.convert("RGB")
        image_preview_convert = image_quantize_c64_colors(image_preview_convert)    #map to 16 colors using normal c64 palette
    else:
        image_preview_convert = image_preview_create_effects(image_original)
        if (user_outputformat.get() == "koala") :
            image_preview_convert = image_preview_convert.resize((160,200))
        image_preview_convert = image_quantize_c64_colors(image_preview_convert)

    #prepare image_preview (this image will only be seen in preview window)
    if (user_outputformat.get() == "koala") :
        image_preview = image_preview_convert.resize((320,200))
    if (user_outputformat.get() == "hires") :
        image_preview = image_preview_convert
        
    image_previewTk = ImageTk.PhotoImage(image_preview)
    label_preview_image.configure(image=image_previewTk)
    label_preview_image.image = image_previewTk # keep a reference!

    #converting every time the image is refreshed: takes a lot of time and cpu power
    #action_convert()
    return None
	
	

def action_preview_scale(
    scale_value
):
    action_image_refresh()
    return None



def create_empty_images():
    global label_original_image
    global image_original
    global image_originalTk
    image_original = Image.new("RGB",(320,200), "BLACK")
    image_originalTk = ImageTk.PhotoImage(image_original)
    label_original_image.configure(image=image_originalTk)
    label_original_image.image = image_original # keep a reference!

    global label_koala_image
    global image_koala
    global image_koalaTk
    image_koala = Image.new("RGB",(320,200), "BLACK")
    image_koalaTk = ImageTk.PhotoImage(image_koala)
    label_koala_image.configure(image=image_koalaTk)
    label_koala_image.image = image_koala # keep a reference!

    action_image_refresh()  #this will also create a preview image from the original image
    return None



def load_image(
	filename
):
	global label_original_image
	global image_original
	global image_originalTk
#	print("opening image \"%s\"..."%filename)
	image_original = Image.open(filename)
	image_original = image_original.resize((320,200))
	image_original = image_original.convert("RGB")
	image_originalTk = ImageTk.PhotoImage(image_original)
	label_original_image.configure(image=image_originalTk)
	label_original_image.image = image_original # keep a reference!
	action_image_refresh()
	return None



def action_OpenGradient():
    textbox.delete('1.0', END)      #clear textbox

    ftypes = [('gradient', '*.grd')]
    filename = askopenfilename(filetypes = ftypes)
    if not filename : return None

    textbox.insert(END,"Reading custom gradient from file \"%s\"...\n"%filename)
    config_read(filename)

    textbox.insert(END,"%d colors read."%user_custom_gradient_sceme_size)
    return None



def action_SaveGradient():
    textbox.delete('1.0', END)      #clear textbox

    ftypes = [('gradient', '*.grd')]
    filename = asksaveasfilename(filetypes = ftypes)
    if not filename : return None

    textbox.insert(END,"Writing custom gradient to file \"%s\"...\n"%filename)
#    config_write(filename)
    textbox.insert(END,"not implemented yet.\n")
    return None





def action_OpenFile():
    global user_filename_open
    global user_filename_open_textvariable
    user_filename_open = ""
    
    ftypes = [('Image Files', '*.tif *.jpg *.png *.bmp *.gif')]
    user_filename_open = askopenfilename(filetypes = ftypes)
    
    user_filename_open_textvariable.set("\"..."+user_filename_open[-30:]+"\"")

    if not user_filename_open : return None

    load_image(user_filename_open)
    action_convert()    
    return None



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

    #write stuff...
    file_out = open(user_filename_save , "wb")
    
    #start address
    if var_start_address_checkbutton :
        i=var_start_address & 0xff  #low
        file_out.write(chr(i))
        i=var_start_address >> 8    #high
        file_out.write(chr(i))
    
    #koala data
    for i in range(0,1000):
        for j in range(0,8):
            file_out.write(chr(koala_bitmap[i][j]))
    for i in koala_col12:
        file_out.write(chr(i))
    if (user_outputformat.get() == "koala") :
        for i in koala_col3:
            file_out.write(chr(i))
        file_out.write(chr(koala_bg))
    file_out.close()
    
    return None



def action_reset_modifiers():
    global scale_modifier_list
    for a in scale_modifier_list: a.set(50)
    return None


def create_drop_down_menu (
	root
) :
    menu = Menu(root)
    root.config(menu=menu)

    filemenu = Menu(menu)

    filemenu.add_command(label="open...", command=action_OpenFile, underline=0, accelerator="Alt+O")
    filemenu.add_command(label="save...", command=action_SaveFile, underline=0, accelerator="Alt+S")
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
    global scale_modifier_list

#scales modifiers
    frame_border = Frame(
        root,
        bd=_bd,
    )
    frame_border.grid(
        row=_row,
        column=_column
    )
    frame_inner = Frame(
        frame_border,
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
        text="color modifiers",
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
        ("saturation", user_color_saturation, 1,0),
        ("brightness", user_brightness, 2,0),
        ("contrast", user_contrast, 3,0),
        ("sharpness", user_sharpness, 4,0)
    ]

    scale_modifier_list=[]
    for text,var,my_row,my_column in MODIFIERS:
        scale_modifier = Scale(
            frame_inner,
            from_=1,
            to=100,
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
        scale_modifier.set(50)
        scale_modifier_list.append(scale_modifier)
        
#        last_row = my_row
 
    button_reset = Button(
        frame_inner,
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
        bd=_bd,
    )
    frame_border.grid(
        row=_row,
        column=_column
    )
    frame_inner = Frame(
        frame_border,
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
        text="effects",
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
        ("dither floyd-steinberg",	user_effects_dither_floyd_steinberg,	1,0),
        ("dither ordered 1",		user_effects_dither_ordered1, 			2,0),
        ("dither ordered 2",		user_effects_dither_ordered2, 			3,0),
        ("blur",					user_effects_blur,						4,0),
        ("detail",					user_effects_detail, 					5,0),
        ("enhance",					user_effects_enhance, 					1,1),
        ("enhance_more",			user_effects_enhance_more, 				2,1),
        ("smooth",					user_effects_smooth, 					3,1),
        ("smooth_more",				user_effects_smooth_more,				4,1),
        ("sharpen",					user_effects_sharpen,					5,1),
    ]
    for text,var, my_row, my_column in EFFECTS:
        checkbutton_effects = Checkbutton(
            frame_inner,
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
        bd=_bd,
    )
    frame_border.grid(
        row=_row,
        column=_column
    )
    frame_inner = Frame(
        frame_border,
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
        text="output format",
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
            ("koala", "koala"),
            ("hires", "hires"),
    ]

    for text, mode in MODES:
        radiobutton_user_mode = Radiobutton(
            frame_inner,
            text = text,
            value = mode,
            indicatoron=0,
            variable=user_outputformat,
            cursor=CURSOR_HAND,
            command=action_image_refresh
        )
        _row += 1
        radiobutton_user_mode.grid(
            row=_row,
            column=1,
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
        bd=_bd,
    )
    frame_border.grid(
        row=_row,
        column=_column
    )
    frame_inner = Frame(
        frame_border,
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
        bd=_bd,
    )
    frame_border.grid(
        row=_row,
        column=_column
    )
    frame_inner = Frame(
        frame_border,
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
        bd=_bd,
    )
    frame_border.grid(
        row=_row,
        column=_column
    )
    frame_inner = Frame(
        frame_border,
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
        text="brightness palette",
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
            ("purple", "purple"),
            ("brown", "brown"),
            ("gray", "gray"),
            ("green", "green"),
            ("blue", "blue"),
            ("green2", "green2"),
            ("custom", "custom"),
    ]

    for text, mode in MODES:
        radiobutton_user_mode = Radiobutton(
            frame_inner,
            text = text,
            value = mode,
            indicatoron=0,
            variable=user_gradient_sceme,
            command=action_image_refresh,
            cursor=CURSOR_HAND
        )
        _row += 1
        radiobutton_user_mode.grid(
            row=_row,
            column=1,
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
        bd=_bd,
    )
    frame_border.grid(
        row=_row,
        column=_column
    )
    frame_inner = Frame(
        frame_border,
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
        text="palette",
        wraplength=100,
        anchor='c',
        justify='left',
        fg="#000088"
    )
    label.grid(
        row=_row,
        column=1,
        sticky=W+E
    )
    MODES = [
            ("colodore", "colodore"),
            ("pepto", "pepto"),
            ("view64", "view64"),
            ("vice", "vice"),
        ]

    for text, mode in MODES:
        radiobutton_user_mode = Radiobutton(
            frame_inner,
            text = text,
            value = mode,
            indicatoron=0,
            variable=user_palette,
            cursor=CURSOR_HAND,
            command=action_image_refresh
        )
        _row += 1
        radiobutton_user_mode.grid(
            row=_row,
            column=1,
            sticky=W+E
        )




def create_gui_settings_startaddress (
	root,
    _row,
    _column
) :
    frame_border = Frame(
        root,
        bd=_bd,
    )
    frame_border.grid(
        row=_row,
        column=_column
    )
    frame_inner = Frame(
        frame_border,
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
        text="start address in hex:",
        anchor='c',
        fg="#000088"
    )
    checkbutton_start_address = Checkbutton(
        frame_inner,
        variable = user_start_address_checkbutton
        )
    label_start_address = Label(
        frame_inner,
        text="values $0-$ffff $",
        anchor='c'
    )
    entry_start_address= Entry(
        frame_inner,
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
        bd=_bd,
    )
    frame_border.grid(
        row=_row,
        column=_column
    )
    frame_inner = Frame(
        frame_border,
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
        text="image",
        anchor='c',
        fg="#000088"
    )
    label_filename = Label(
        frame_inner,
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
    _padx = 10
    _pady = 10
    
	#http://effbot.org/tkinterbook/toplevel.htm
    about_window = Toplevel(
        bd=10
    )
    about_window.title("About")

    msg_text = """\
This is %s
Version %s [%s]
by fieserWolF / Abyss-Connection

For feature requests or bug reports
feel free to contact me:
http://csdb.dk/scener/?id=3623
wolf@abyss-connection.de

I know this is far from being complete,
so look out for new versions!

wolf


Convertron3000 Commodore 64 graphics converter
Copyright (C) 2017 fieserWolF / Abyss-Connection

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
http://csdb.dk/scener/?id=3623 or wolf@abyss-connection.de

For Python2.7, The Python Imaging Library (PIL), Numpy and Tcl/Tk licenses see file "licenses.txt".\
    """ % (PROGNAME, VERSION, DATUM)

    frame_left = Frame( about_window)
    frame_right = Frame( about_window)

    #http://effbot.org/tkinterbook/message.htm
    #text
    msg = Text(
        frame_right,
#        bd=10,
        relief=FLAT,
        width=40,
        height=10
    )

    #scrollbar
    msg_scrollBar = Scrollbar(
        frame_right
    )
    msg_scrollBar.config(command=msg.yview)
    msg.config(yscrollcommand=msg_scrollBar.set)

    #label with image
    #http://effbot.org/tkinterbook/photoimage.htm
    #image = Image.open("wolf.jpg")
    #photo = ImageTk.PhotoImage(image)
    photo = PhotoImage(data=about_graphic)
    label_image = Label(
        frame_left,
#        bd=10,
        image=photo,
        padx=_padx,
        pady=_pady
    )
    label_image.image = photo # keep a reference!

    #button
    button = Button(
        frame_left,
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



    msg.insert(END, msg_text)
    msg.config(state=DISABLED)

    return None
	
	

def create_gui_action_buttons (
	root,
    _row,
    _column
) :
    frame_border = Frame(
        root,
        bd=_bd,
    )
    frame_border.grid(
        row=_row,
        column=_column
    )
    frame_inner = Frame(
        frame_border,
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
        text = "convert\nAlt+C",
        width=7,
        height=3,
        command=action_convert,
        cursor=CURSOR_HAND,
        bg="#ccccdd"
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
        bd=_bd,
    )
    frame_border.grid(
        row=_row,
        column=_column
    )
    frame_inner = Frame(
        frame_border,
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
		text="converter output",
        fg="#000088"
	)
    textbox = Text(
        frame_inner,
        height=14,
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
        bd=_bd,
    )
    frame_border.grid(
        row=_row,
        column=_column
    )
    frame_inner = Frame(
        frame_border,
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
		text="original",
        fg="#000088"
	)
    label_original_image = Label(
        frame_inner
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
        bd=_bd,
    )
    frame_border.grid(
        row=_row,
        column=_column
    )
    frame_inner = Frame(
        frame_border,
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
		text="preview",
        fg="#000088"
	)
    label_preview_image = Label(
        frame_inner
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
        bd=_bd,
    )
    frame_border.grid(
        row=_row,
        column=_column
    )
    frame_inner = Frame(
        frame_border,
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
		text="output",
        fg="#000088"
	)
    label_koala_image = Label(
        frame_inner
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
#def keyboard_SaveGradient(self):
#    action_SaveGradient()




def _main_procedure() :
        
    #main procedure
    root.title("%s v%s [%s]" % (PROGNAME, VERSION, DATUM) )

    root.grid_columnconfigure(0, weight=10)
    root.grid_rowconfigure(0, weight=10)


    frame_left = Frame(root)
    frame_left.grid(
        row=0,
        column=0,
        sticky=N
    )
    frame_left.grid_columnconfigure(0, weight=1)
    frame_left.grid_rowconfigure(0, weight=1)

    frame_middle = Frame(root)
    frame_middle.grid(
        row=0,
        column=1,
        sticky=N
    )
    frame_middle.grid_columnconfigure(0, weight=1)
    frame_middle.grid_rowconfigure(0, weight=1)

    frame_right = Frame(root)
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
    create_gui_backgroundcolor(
        frame_right,
        3,  #row
        0   #column
    )
    create_gui_settings_startaddress(
        frame_right,
        4,  #row
        0   #column
    )
    create_gui_text(
        frame_right,
        5,  #row
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

    mainloop()
    return None
    



if __name__ == '__main__':
    _main_procedure()
