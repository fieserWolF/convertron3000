import os
import sys
import tkinter as tk
from PIL import ImageTk, ImageEnhance, ImageFilter, ImageDraw
import PIL.Image as PilImage    #we need another name, as it collides with tkinter.Image otherwise



#global constants
def _global_constants():
        return None

#BGCOLOR="#ff0000"
BGCOLOR="#d9d9d9"


PROGNAME = 'CONVERTRON3000';
C64_CHAR_HEIGHT = 25  #200/8
C64_CHAR_WIDTH = 40   #320/8

#FILENAME_JSON_PRE = '/tmp/color_clashes.json'
#FILENAME_CLASH_IMAGE_PRE = '/tmp/color_clashes.png'

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

RESOURCE_PATH = '../resources/'
RES_VERSION = resource_path(RESOURCE_PATH+'version.txt')
RES_GFX_ICON = resource_path(RESOURCE_PATH+'icon.png')
RES_GFX_ABOUT = resource_path(RESOURCE_PATH+'about.png')
RES_DOC_ABOUT = resource_path(RESOURCE_PATH+'about.txt')
RES_DOC_HELP = resource_path(RESOURCE_PATH+'help.txt')

VERSION = open(RES_VERSION, encoding="utf_8").read().rstrip()


_padx = 2
_pady = 2
_bd = 4

KOALA_WIDTH = 160
KOALA_HEIGHT = 200
HIRES_WIDTH = 320
HIRES_HEIGHT = 200
C64_COLOR_AMOUNT = 16


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

#settings = []
        
root = tk.Tk()


user_filename_open = "none"
user_filename_save = "none"
user_filename_save_clash_json = "none"
user_filename_save_clash_image = "none"

user_start_address = tk.StringVar(root, name='start address')
user_start_address_checkbutton = tk.IntVar(root, name='start address enable')
user_sharpness = tk.IntVar(root, name='sharpness')
user_treshold = tk.IntVar(root, name='treshold')
user_color_saturation = tk.IntVar(root, name='saturation')
user_brightness = tk.IntVar(root, name='brightness')
user_contrast = tk.IntVar(root, name='contrast')
user_modes = tk.StringVar(root, name='modes')
user_outputformat = tk.StringVar(root, name='outputformat')
user_palette = tk.StringVar(root, name='palette')
user_filename_open_textvariable = tk.StringVar(root, name='filename')
convertbutton_text = tk.StringVar()

user_effects_blur = tk.IntVar(root, name='effects blur')
user_effects_detail = tk.IntVar(root, name='effects detail')
user_effects_enhance = tk.IntVar(root, name='effects enhance')
user_effects_enhance_more = tk.IntVar(root, name='effects enhance more')
user_effects_smooth = tk.IntVar(root, name='effects smooth')
user_effects_smooth_more = tk.IntVar(root, name='effects smooth more')
user_effects_sharpen = tk.IntVar(root, name='effects sharpen')
user_effects_showClashes = tk.IntVar(root, name='effects showClashes')

user_gradient_sceme = tk.StringVar(root, name='gradient')
user_dithering = tk.StringVar(root, name='dithering')
user_backgroundcolor = tk.IntVar(root, name='backgroundcolor')
user_backgroundcolor.set(99)


#defaults
settings = {
    'start address' : None,
    'start address enable' : None,
    'sharpness' : 0,
    'treshold' : 0,
    'saturation' : 0,
    'brightness' : 0,
    'contrast' : 0,
    'modes' : 'colors',
    'outputformat' : 'koala',
    'palette' : 'pepto',
    'filename' : 'none',
    'effects blur' : 0,
    'effects detail' : 0,
    'effects enhance' : 0,
    'effects enhance more' : 0,
    'effects smooth' : 0,
    'effects smooth more' : 0,
    'effects sharpen' : 0,
    'effects showClashes' : 0,
    'gradient' : 'purple',
    'dithering' : 'none',
    'backgroundcolor' : 0,
}
user_filename_open_textvariable.set("none")
convertbutton_text.set("convert\nAlt+C")

textbox = tk.Text()
label_original_image = tk.Label()
label_preview_image = tk.Label()
label_koala_image = tk.Label()
image_original = PilImage.new("RGB", (HIRES_WIDTH,HIRES_HEIGHT), "black")
image_preview = PilImage.new("RGB", (HIRES_WIDTH,HIRES_HEIGHT), "black")
image_koala = PilImage.new("RGBA", (HIRES_WIDTH,HIRES_HEIGHT), "black")
image_preview_convert = PilImage.new("RGB", (KOALA_WIDTH,KOALA_HEIGHT), "black")

koala_bitmap=[None]*8000
koala_col12=[None]*1000
koala_col3=[None]*1000
koala_bg=0

koala_colorindex_data = [0] * KOALA_WIDTH*KOALA_HEIGHT
hires_colorindex_data = [0] * HIRES_WIDTH*HIRES_HEIGHT

#initialize empty images
image_result_koala = PilImage.new("P", (KOALA_WIDTH, KOALA_HEIGHT))
image_result_hires = PilImage.new("P", (HIRES_WIDTH, HIRES_HEIGHT))

image_clashes = PilImage.new("P", (KOALA_WIDTH, KOALA_HEIGHT))


scale_modifier_list=[]
scale_modifier_list_default=[]

user_custom_gradient_sceme = [0] * C64_COLOR_AMOUNT
user_custom_gradient_sceme_size = 0

color_clash_chars_xy = []

args = []
