import code.myGlobals as myGlobals
#import os
#import sys
import hitherdither
#import struct
from PIL import ImageTk, ImageEnhance, ImageFilter, ImageDraw
import PIL.Image as PilImage    #we need another name, as it collides with tkinter.Image otherwise
#from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
import json

#from tkinter import ttk
#ttk.Style().theme_use('clam')

import tkinter as tk




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

hitherdither_palette = hitherdither.palette.Palette(convert_to_hitherdither_palette(myGlobals.PALETTEDATA_PEPTO))  #do to
hitherdither_tres_value=256/8    #play around with tresholds
hitherdither_tresholds = [hitherdither_tres_value, hitherdither_tres_value, hitherdither_tres_value]
hitherdither_order=8  #2,4,8,16,32,64,128








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
        'pepto': myGlobals.PALETTEDATA_PEPTO,
        'view64': myGlobals.PALETTEDATA_VIEW64,
        'vice': myGlobals.PALETTEDATA_VICE,
        'colodore': myGlobals.PALETTEDATA_COLODORE,
    }
    my_palettedata = switcher_palette.get(myGlobals.user_palette.get(), myGlobals.PALETTEDATA_PEPTO)
    
    hitherdither_tresholds = [256/myGlobals.user_treshold.get(), 256/myGlobals.user_treshold.get(), 256/myGlobals.user_treshold.get()]

    #https://github.com/justmao945/lab/tree/master/halftoning/ordered-dithering
    if (myGlobals.user_dithering.get() == 'bayer') :
        hitherdither_palette = hitherdither.palette.Palette(convert_to_hitherdither_palette(my_palettedata))
        image = hitherdither.ordered.bayer.bayer_dithering(image, hitherdither_palette, hitherdither_tresholds, order=hitherdither_order)
    if (myGlobals.user_dithering.get() == 'yliluomas1') :
        hitherdither_palette = hitherdither.palette.Palette(convert_to_hitherdither_palette(my_palettedata))
        image = hitherdither.ordered.yliluoma.yliluomas_1_ordered_dithering(image, hitherdither_palette, order=hitherdither_order)
    if (myGlobals.user_dithering.get() == 'line') :
        hitherdither_palette = hitherdither.palette.Palette(convert_to_hitherdither_palette(my_palettedata))
        my_width, my_height = image.size
        image = image.resize((my_width*2,my_height), resample=PilImage.NEAREST)
        image = hitherdither.ordered.bayer.bayer_dithering(image, hitherdither_palette, hitherdither_tresholds, order=hitherdither_order)
        image = image.resize((my_width,my_height), resample=PilImage.NEAREST)
    if (myGlobals.user_dithering.get() == 'dots') :
        hitherdither_palette = hitherdither.palette.Palette(convert_to_hitherdither_palette(my_palettedata))
        image = hitherdither.ordered.cluster.cluster_dot_dithering(image, hitherdither_palette, hitherdither_tresholds, order=hitherdither_order)

    if (myGlobals.user_dithering.get() == 'floyd-steinberg') :
        pal_image.putpalette(
            (my_palettedata)
            +(0,0,0)*(256-16)
        )
        quantisized_image = image.im.convert("P",1,pal_image.im)
        image = image._new(quantisized_image)

    if (myGlobals.user_dithering.get() == 'none') :
        pal_image.putpalette(
            (my_palettedata)
            +(0,0,0)*(256-16)
        )
        quantisized_image = image.im.convert("P",0,pal_image.im)
        image = image._new(quantisized_image)

    return image



def image_quantize_paletted_brightness(image):

    switcher_gradient_sceme = {
        'purple': myGlobals.GRADIENT_PURPLE_SCEME,
        'brown': myGlobals.GRADIENT_BROWN_SCEME,
        'gray': myGlobals.GRADIENT_GRAY_SCEME,
        'green': myGlobals.GRADIENT_GREEN_SCEME,
        'blue': myGlobals.GRADIENT_BLUE_SCEME,
        'green2': myGlobals.GRADIENT_GREEN2_SCEME,
        'custom': myGlobals.user_custom_gradient_sceme,
    }
    gradient_sceme = switcher_gradient_sceme.get(myGlobals.user_gradient_sceme.get(), myGlobals.GRADIENT_PURPLE_SCEME)

    switcher_gradient_colors = {
        'purple': myGlobals.GRADIENT_PURPLE_COLORS,
        'brown': myGlobals.GRADIENT_BROWN_COLORS,
        'gray': myGlobals.GRADIENT_GRAY_COLORS,
        'green': myGlobals.GRADIENT_GREEN_COLORS,
        'blue': myGlobals.GRADIENT_BLUE_COLORS,
        'green2': myGlobals.GRADIENT_GREEN2_COLORS,
        'custom': myGlobals.user_custom_gradient_sceme_size,
    }
    gradient_colors = switcher_gradient_colors.get(myGlobals.user_gradient_sceme.get(), myGlobals.GRADIENT_PURPLE_COLORS)


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

    hitherdither_tresholds = [256/myGlobals.user_treshold.get(), 256/myGlobals.user_treshold.get(), 256/myGlobals.user_treshold.get()]


    #quantisize image to grayscale with given grayscale palette holding (gradient_colors) number of colors
    if (myGlobals.user_dithering.get() == 'bayer') :
        hitherdither_palette = hitherdither.palette.Palette(convert_to_hitherdither_palette(my_palettedata))
        image = hitherdither.ordered.bayer.bayer_dithering(image, hitherdither_palette, hitherdither_tresholds, order=hitherdither_order)
    if (myGlobals.user_dithering.get() == 'yliluomas1') :
        hitherdither_palette = hitherdither.palette.Palette(convert_to_hitherdither_palette(my_palettedata))
        image = hitherdither.ordered.yliluoma.yliluomas_1_ordered_dithering(image, hitherdither_palette, order=hitherdither_order)
    if (myGlobals.user_dithering.get() == 'line') :
        hitherdither_palette = hitherdither.palette.Palette(convert_to_hitherdither_palette(my_palettedata))
        my_width, my_height = image.size
        image = image.resize((my_width*2,my_height), resample=PilImage.NEAREST)
        image = hitherdither.ordered.bayer.bayer_dithering(image, hitherdither_palette, hitherdither_tresholds, order=hitherdither_order)
        image = image.resize((my_width,my_height), resample=PilImage.NEAREST)
    if (myGlobals.user_dithering.get() == 'dots') :
        hitherdither_palette = hitherdither.palette.Palette(convert_to_hitherdither_palette(my_palettedata))
        image = hitherdither.ordered.cluster.cluster_dot_dithering(image, hitherdither_palette, hitherdither_tresholds, order=hitherdither_order)

    if (myGlobals.user_dithering.get() == 'floyd-steinberg') :
        pal_image= PilImage.new("P", (1,1))
        pal_image.putpalette(my_palettedata)
        quantisized_image = image.im.convert("P",1,pal_image.im)
        image = image._new(quantisized_image)

    if (myGlobals.user_dithering.get() == 'none') :
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
    location = (y*myGlobals.C64_CHAR_WIDTH)+x
        
    switcher = {
        0 : myGlobals.koala_bg,    #=koala_bg;	// pixel not set = $d021 colour
        1 : myGlobals.koala_col12[location] >> 4,   #=koala_col12[(y*C64_CHAR_WIDTH)+x] SHR 4;
        2 : myGlobals.koala_col12[location] & 0b00001111,    #=koala_col12[(y*C64_CHAR_WIDTH)+x] and %00001111;
        3 : myGlobals.koala_col3[location] & 0b00001111    #=koala_col3[(y*C64_CHAR_WIDTH)+x] and %00001111;
    }
    return switcher.get(index,0)




def hires_index_to_colorindex(
    index,  #0..1
    x,
    y
) :
    location = (y*myGlobals.C64_CHAR_WIDTH)+x
        
    switcher = {
        0 : myGlobals.koala_col12[location] & 0b00001111,    #=koala_col12[(y*C64_CHAR_WIDTH)+x] and %00001111;
        1 : myGlobals.koala_col12[location] >> 4,   #=koala_col12[(y*C64_CHAR_WIDTH)+x] SHR 4;
    }
    return switcher.get(index,0)



def koala_colorindex_to_rgb(
    index
):
    switcher_palette = {
        'pepto': myGlobals.PALETTEDATA_PEPTO,
        'view64': myGlobals.PALETTEDATA_VIEW64,
        'vice': myGlobals.PALETTEDATA_VICE,
        'colodore': myGlobals.PALETTEDATA_COLODORE,
    }
    my_palette = switcher_palette.get(myGlobals.user_palette.get(), myGlobals.PALETTEDATA_PEPTO)

    return_palette = []
    return_palette.append(my_palette[(index*3)+0])
    return_palette.append(my_palette[(index*3)+1])
    return_palette.append(my_palette[(index*3)+2])

    return return_palette




def koala_to_image(
):
    SHR_PRE = [
        6,
        4,
        2,
        0
    ]

    for y in range(0, myGlobals.C64_CHAR_HEIGHT):
        for x in range(0, myGlobals.C64_CHAR_WIDTH):
            pos = ((y*myGlobals.C64_CHAR_WIDTH)+x)*8
            this_block = myGlobals.koala_bitmap[ pos:pos+8]   #this_block holds 8 bytes
        #    print(this_block)

            for row in range(0, 8):
                this_row = this_block[row]
                
                for column in range(0, 4):
                    iy = y*8    +row
                    ix = x*4    +column

                    #normal data
                    koalaindex = (this_row >> SHR_PRE[column]) & 0b00000011 #result should be 0..3
                    myGlobals.koala_colorindex_data[iy*myGlobals.KOALA_WIDTH+ix] = koala_index_to_colorindex(koalaindex,x,y)









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

    for y in range(0, myGlobals.C64_CHAR_HEIGHT):
        for x in range(0, myGlobals.C64_CHAR_WIDTH):
            pos = ((y*myGlobals.C64_CHAR_WIDTH)+x)*8
            this_block = myGlobals.koala_bitmap[ pos:pos+8]   #this_block holds 8 bytes

            for row in range(0, 8):
                this_row = this_block[row]
                
                for column in range(0, 8):
                    my_index = (this_row >> SHR_PRE[column]) & 0b00000001 #result should be 0..1

                    iy = y*8    +row
                    ix = x*8    +column

                    myGlobals.hires_colorindex_data[iy*myGlobals.HIRES_WIDTH+ix] = hires_index_to_colorindex(my_index,x,y)


 
 
 
 

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
                (myGlobals.REPLACEMENT_TABLE[replace_this][a] == palette[b][0])
            ):
                return_value = palette[b][0]
                found = True
#                print('solution found: %d -> %d' %(replace_this, palette[b][0]))


    if (found == False) :
        #myGlobals.textbox.delete('1.0', tk.END)      #clear textbox
        myGlobals.textbox.insert(tk.END,'ERROR in replacement table for color %d:\n'% replace_this)
        myGlobals.textbox.insert(tk.END,myGlobals.REPLACEMENT_TABLE[replace_this])
        myGlobals.textbox.insert(tk.END,'\n4 mostly used colors in the whole image: ')

        print('ERROR in the color replacement table for color %d: '%replace_this)
        print('Replacement table for color %d: '% replace_this, end='')
        print(myGlobals.REPLACEMENT_TABLE[replace_this])

        print( '2 mostly used colors in the whole image: ',end='')
        for a in range (0,4) :
            myGlobals.textbox.insert(tk.END,"%d, " % palette[a][0])
            print ("%d" % palette[a][0],end=', ')
        print ()

        return_value = palette[0][0];
        myGlobals.textbox.insert(tk.END,'\nDirty fix: Replacing color %d with most used color %d.\n\n' % (replace_this,return_value))
        print('Dirty fix: Replacing color %d with most used color %d.' % (replace_this,return_value));
        print()

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
    myGlobals.textbox.delete('1.0', tk.END)      #clear textbox
    myGlobals.textbox.insert(tk.END,'Opening json-file "%s" for writing color-clashes.\n' % filename_out)
    
    if ( len(my_data) > 0 ) :
        # write file
        print ('    Opening json-file "%s" for writing.' % filename_out, end='')
        try:
            file_out = open(filename_out , "w")
        except IOError as err:
            myGlobals.textbox.insert(tk.END,"I/O error: %s\n"%format(err))
            print("I/O error: {0}".format(err))
            return None

        json_data = {}

        #info
        my_item = {}
        my_item['program'] = myGlobals.PROGNAME
        my_item['version'] = myGlobals.VERSION
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
    
    
def write_settings_to_json_file(
    filename_out,
    my_data
) :
    myGlobals.textbox.delete('1.0', tk.END)      #clear textbox
    myGlobals.textbox.insert(tk.END,'Opening json-file "%s" for writing settings.\n' % filename_out)

    
    if ( len(my_data) > 0 ) :
        # write file
        print ('    Opening json-file "%s" for writing.' % filename_out, end='')
        try:
            file_out = open(filename_out , "w")
        except IOError as err:
            myGlobals.textbox.insert(tk.END,"I/O error: %s\n"%format(err))
            print("I/O error: {0}".format(err))
            return None

        json_data = {
            'info' : {
                'program' : myGlobals.PROGNAME,
                'version' : myGlobals.VERSION,
                'content' : 'settings',
            },
            'settings' : my_data
        }

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
    myGlobals.textbox.delete('1.0', tk.END)      #clear textbox

    block = [ [0] * 4 for i in range(8)]    #32 bytes
    bitmap = [[ [0] * 8 for i in range(myGlobals.C64_CHAR_WIDTH)] for i in range(myGlobals.C64_CHAR_HEIGHT)]    #8000 bytes
    screen = [ [0] * myGlobals.C64_CHAR_WIDTH for i in range(myGlobals.C64_CHAR_HEIGHT)]    #1000 bytes
    colram = [ [0] * myGlobals.C64_CHAR_WIDTH for i in range(myGlobals.C64_CHAR_HEIGHT)]    #1000 bytes
    palette = [ [0] * 2 for i in range(16)]    #32 bytes   palette[x][0]=color palette  /  [x][1]=amount
    
    user_koala_bg_color = myGlobals.user_backgroundcolor.get()

    myGlobals.textbox.insert(tk.END,"procedure 'convert_to_koala': working...\n")
    
    myGlobals.root.update()


    #fill bmp_bitmap with image_preview 160x200 data
    bmp_bitmap = [ [0] * 160 for i in range(200) ]
    my_list = list(myGlobals.image_preview_convert.getdata()) #image is in "P" mode
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
    myGlobals.textbox.insert(tk.END,"Background Color = %d\n" % background_color)



    #main loop
    myGlobals.color_clash_chars_xy = []
    for y in range (0,myGlobals.C64_CHAR_HEIGHT):
        for x in range (0,myGlobals.C64_CHAR_WIDTH):

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
                myGlobals.color_clash_chars_xy.append(my_coords)
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
                    myGlobals.textbox.insert(tk.END,'Convert error in char[%d,%d]:\n'%(y,x))
                    myGlobals.textbox.insert(tk.END,'Color %d in block[%d,%d] not found!\n'% (block[c][d], c, d))
                    myGlobals.textbox.insert(tk.END,'Block row %d, column %d (convert bitmap data)\n' % (c,d))
                    myGlobals.textbox.insert(tk.END,"\n")
                    return None # halt(1);

            # store bitmap data
            for c in range (0,8) :
                bitmap[y][x][c] = block[c][0]
                bitmap[y][x][c] = (bitmap[y][x][c] << 2) | block[c][1]
                bitmap[y][x][c] = (bitmap[y][x][c] << 2) | block[c][2]
                bitmap[y][x][c] = (bitmap[y][x][c] << 2) | block[c][3]

    myGlobals.textbox.insert(tk.END,'Fixed %d color clashes in %d character blocks.\n'% (color_clash_counter, color_clash_chars_counter));

    if (myGlobals.args.debug_clashes) :
        show_color_clashes_on_console(myGlobals.color_clash_chars_xy)


    #convert to our format used in koala_to_image
    for y in range (0,myGlobals.C64_CHAR_HEIGHT) :
        for x in range (0,myGlobals.C64_CHAR_WIDTH) :
            for c in range (0,8) : myGlobals.koala_bitmap[((y*myGlobals.C64_CHAR_WIDTH)+x)*8 +c] = bitmap[y][x][c]
            myGlobals.koala_col12[(y*myGlobals.C64_CHAR_WIDTH)+x] = screen[y][x]
            myGlobals.koala_col3[(y*myGlobals.C64_CHAR_WIDTH)+x] = colram[y][x]
    myGlobals.koala_bg = background_color
    



 
 

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
                (myGlobals.REPLACEMENT_TABLE[replace_this][a] == palette[b][0])
            ):
                return_value = palette[b][0]
                found = True
                #print('solution found: %d -> %d' %(replace_this, palette[b][0]))

    if (found == False) :
        #myGlobals.textbox.delete('1.0', tk.END)      #clear textbox
        myGlobals.textbox.insert(tk.END,'ERROR in replacement table for color %d:\n'% replace_this)
        myGlobals.textbox.insert(tk.END,myGlobals.REPLACEMENT_TABLE[replace_this])
        myGlobals.textbox.insert(tk.END,'\n2 mostly used colors in the whole image: ')

        print('ERROR in the color replacement table for color %d: '%replace_this)
        print('Replacement table for color %d: '% replace_this, end='')
        print(myGlobals.REPLACEMENT_TABLE[replace_this])

        print( '2 mostly used colors in the whole image: ',end='')
        for a in range (0,2) :
            myGlobals.textbox.insert(tk.END,"%d, " % palette[a][0])
            print ("%d" % palette[a][0],end=', ')
        print ()

        return_value = palette[0][0];
        myGlobals.textbox.insert(tk.END,'\nDirty fix: Replacing color %d with most used color %d.\n\n' % (replace_this,return_value))
        print('Dirty fix: Replacing color %d with most used color %d.' % (replace_this,return_value));
        print()

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
    #global textbox
    #global koala_bitmap, koala_col12
    #global color_clash_chars_xy

    myGlobals.textbox.delete('1.0', tk.END)      #clear textbox

    block = [ [0] * 8 for i in range(8)]    #8*8 = 64 bytes
    bitmap = [[ [0] * 8 for i in range(myGlobals.C64_CHAR_WIDTH)] for i in range(myGlobals.C64_CHAR_HEIGHT)]    #25*40*8 = 8000 bytes
    screen = [ [0] * myGlobals.C64_CHAR_WIDTH for i in range(myGlobals.C64_CHAR_HEIGHT)]    #25*40 = 1000 bytes
    palette = [ [0] * 2 for i in range(16)]    #16*2 = 32 bytes   palette[x][0]=color palette  /  [x][1]=amount
 
    
    myGlobals.textbox.insert(tk.END,"procedure \"convert_to_hires\": working...\n")
    
    myGlobals.root.update()


    #fill bmp_bitmap with image_preview_convert data
    bmp_bitmap = [ [0] * myGlobals.HIRES_WIDTH for i in range(myGlobals.HIRES_HEIGHT)]   #200*320 = 64000 bytes
    my_list = list(myGlobals.image_preview_convert.getdata()) #image is in "P" mode
    for y in range(0,myGlobals.HIRES_HEIGHT) :
        for x in range(0,myGlobals.HIRES_WIDTH) :
            bmp_bitmap[y][x] = my_list[(y*myGlobals.HIRES_WIDTH)+x]




    #converting to hires: begin...
    color_clash_counter = 0
    color_clash_chars_counter = 0
    myGlobals.color_clash_chars_xy = []

    #main loop
    for y in range (0,myGlobals.C64_CHAR_HEIGHT):
        for x in range (0,myGlobals.C64_CHAR_WIDTH):


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
                myGlobals.color_clash_chars_xy.append(my_coords)

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
                    myGlobals.textbox.insert(tk.END,'Convert error in char[%d,%d]:\n'%(y,x))
                    myGlobals.textbox.insert(tk.END,'Color %d in block[%d,%d] not found!\n'% (block[c][d], c, d))
                    myGlobals.textbox.insert(tk.END,'Block row %d, column %d (convert bitmap data)\n' % (c,d))
                    myGlobals.textbox.insert(tk.END,"\n")
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

    myGlobals.textbox.insert(tk.END,'Fixed %d color clashes in %d character blocks.\n'% (color_clash_counter, color_clash_chars_counter));

    if (myGlobals.args.debug_clashes) :
        show_color_clashes_on_console(myGlobals.color_clash_chars_xy)


    #convert to our format used in hires_to_image
    for y in range (0,myGlobals.C64_CHAR_HEIGHT) :
        for x in range (0,myGlobals.C64_CHAR_WIDTH) :
            for c in range (0,8) : myGlobals.koala_bitmap[((y*myGlobals.C64_CHAR_WIDTH)+x)*8 +c] = bitmap[y][x][c]
            myGlobals.koala_col12[(y*myGlobals.C64_CHAR_WIDTH)+x] = screen[y][x]
    





def image_preview_create_effects(
    my_image
) :
    """creates the preview image 160x200 object"""

#Hue-Saturation-Lightness
#contrast

#http://pillow.readthedocs.io/en/3.4.x/reference/ImageFilter.html
    if (myGlobals.user_effects_blur.get() == 1) :
        my_image = my_image.filter(ImageFilter.BLUR)
    if (myGlobals.user_effects_detail.get() == 1) :
        my_image = my_image.filter(ImageFilter.DETAIL)
    if (myGlobals.user_effects_enhance.get() == 1) :
        my_image = my_image.filter(ImageFilter.EDGE_ENHANCE)
    if (myGlobals.user_effects_enhance_more.get() == 1) :
        my_image = my_image.filter(ImageFilter.EDGE_ENHANCE_MORE)
    if (myGlobals.user_effects_smooth.get() == 1) :
        my_image = my_image.filter(ImageFilter.SMOOTH)
    if (myGlobals.user_effects_smooth_more.get() == 1) :
        my_image = my_image.filter(ImageFilter.SMOOTH_MORE)
    if (myGlobals.user_effects_sharpen.get() == 1) :
        my_image = my_image.filter(ImageFilter.SHARPEN)
  
    fineness = 50.0
  
#http://pillow.readthedocs.io/en/3.1.x/reference/ImageEnhance.html
#sharpness
    enhancer = ImageEnhance.Sharpness(my_image)
    factor = int(myGlobals.user_sharpness.get()) / fineness
    my_image = enhancer.enhance(factor)

#color balance
    enhancer = ImageEnhance.Color(my_image)
    factor = int(myGlobals.user_color_saturation.get()) / fineness
    my_image = enhancer.enhance(factor)

#color brightness
    enhancer = ImageEnhance.Brightness(my_image)
    factor = int(myGlobals.user_brightness.get()) / fineness
    my_image = enhancer.enhance(factor)

#color contrast
    enhancer = ImageEnhance.Contrast(my_image)
    factor = int(myGlobals.user_contrast.get()) / fineness
    my_image = enhancer.enhance(factor)
  
    return my_image





def prepare_image_color_clashes():
    myGlobals.image_clashes = myGlobals.image_koala
    if (len(myGlobals.color_clash_chars_xy) == 0): return None

    image_markers = PilImage.new("RGBA", (320,200), (0,0,0,0))
    img1 = ImageDraw.Draw(image_markers)
    for i in myGlobals.color_clash_chars_xy:
        img1.rectangle(
            [
                (i[0]*8, i[1]*8),           # start: x,y
                (i[0]+1)*8, (i[1]+1)*8      # end: x,y
            ],
            fill=(255,255,0,128),
            outline=(255,0,0,128)
        )
    
    myGlobals.image_clashes = PilImage.alpha_composite(myGlobals.image_koala, image_markers)

    #print ('    Opening image-file "%s" for writing...' % args.clashes_image)
    #image_koala_new.save(args.clashes_image)
    #write_color_clashes_to_json_file(args.clashes_json,color_clash_chars_xy)
    #textbox.insert(tk.END,'See files "%s" and "%s" for details.\n'% (args.clashes_json, args.clashes_image));

    #return myGlobals.image_clashes



def create_empty_images():
    myGlobals.image_original = PilImage.new("RGB",(320,200), "BLACK")
    myGlobals.image_originalTk = ImageTk.PhotoImage(myGlobals.image_original)
    myGlobals.label_original_image.configure(image=myGlobals.image_originalTk)
    myGlobals.label_original_image.image = myGlobals.image_original # keep a reference!

    myGlobals.image_koala = PilImage.new("RGB",(320,200), "BLACK")
    myGlobals.image_koalaTk = ImageTk.PhotoImage(myGlobals.image_koala)
    myGlobals.label_koala_image.configure(image=myGlobals.image_koalaTk)
    myGlobals.label_koala_image.image = myGlobals.image_koala # keep a reference!

    image_refresh()  #this will also create a preview image from the original image



def load_image(
	filename
):
    myGlobals.textbox.delete('1.0', tk.END)      #clear textbox
    myGlobals.textbox.insert(tk.END,'Opening image "%s".\n' % filename)

    try:
        myGlobals.image_original = PilImage.open(filename)
    except FileNotFoundError as err:
        myGlobals.textbox.insert(tk.END,"FileNotFoundError: %s\n"%format(err))
        print("FileNotFoundError: {0}".format(err))
        return None

    myGlobals.image_original = myGlobals.image_original.resize((320,200), resample=PilImage.NEAREST)
    myGlobals.image_original = myGlobals.image_original.convert("RGB")
    myGlobals.image_originalTk = ImageTk.PhotoImage(myGlobals.image_original)
    myGlobals.label_original_image.configure(image=myGlobals.image_originalTk)
    myGlobals.label_original_image.image = myGlobals.image_original # keep a reference!
    image_refresh()






def convert():
    myGlobals.convertbutton_text.set("busy...")

    switcher_palette = {
        'pepto': myGlobals.PALETTEDATA_PEPTO,
        'view64': myGlobals.PALETTEDATA_VIEW64,
        'vice': myGlobals.PALETTEDATA_VICE,
        'colodore': myGlobals.PALETTEDATA_COLODORE,
    }
    my_palettedata = switcher_palette.get(myGlobals.user_palette.get(), myGlobals.PALETTEDATA_PEPTO)



    if (myGlobals.user_outputformat.get()=='koala') :
        convert_to_koala()    #reads: image_preview_convert sets koala_bitmap, koala_col12, koala_col3 and koala_bg
        koala_to_image()    #prepares koala_colorindex_data

        myGlobals.image_result_koala.putpalette(my_palettedata)
        myGlobals.image_result_koala.putdata(myGlobals.koala_colorindex_data)

        myGlobals.image_koala = myGlobals.image_result_koala.resize((320,200), resample=PilImage.NEAREST).convert("RGBA")
       
        
    if (myGlobals.user_outputformat.get()=='hires') :
        convert_to_hires()    #reads: image_preview_convert sets koala_bitmap, koala_col12
        hires_to_image()    #prepares koala_colorindex_data

        myGlobals.image_result_hires.putpalette(my_palettedata)
        myGlobals.image_result_hires.putdata(myGlobals.hires_colorindex_data)
        myGlobals.image_koala = myGlobals.image_result_hires.convert("RGBA")


    #show color_clashes()
    #before:myGlobals.image_koala
    prepare_image_color_clashes()

    if (myGlobals.user_effects_showClashes.get() == 0) :
        image_koala_new = myGlobals.image_koala
    else :
        image_koala_new = myGlobals.image_clashes

    #image_koala_new = show_color_clashes()
    image_koalaTk = ImageTk.PhotoImage(image_koala_new)
    myGlobals.label_koala_image.configure(image=image_koalaTk)
    myGlobals.label_koala_image.image = image_koalaTk # keep a reference!

    myGlobals.convertbutton_text.set("convert\nAlt+C")



def image_refresh():
    #prepare image_preview_convert (this image will be converted later)
    if (myGlobals.user_modes.get() == "palette") :
        image_grayscale = ImageEnhance.Color(myGlobals.image_original).enhance(0)   #make grayscale
        myGlobals.image_preview_convert = image_preview_create_effects(image_grayscale)   #apply effects
        if (myGlobals.user_outputformat.get() == "koala") :
            myGlobals.image_preview_convert = myGlobals.image_preview_convert.resize((160,200), resample=PilImage.NEAREST)
        myGlobals.image_preview_convert = image_quantize_paletted_brightness(myGlobals.image_preview_convert).convert("RGB")   #quantisize to selected gradient
    else:
        myGlobals.image_preview_convert = image_preview_create_effects(myGlobals.image_original)
        if (myGlobals.user_outputformat.get() == "koala") :
            myGlobals.image_preview_convert = myGlobals.image_preview_convert.resize((160,200), resample=PilImage.NEAREST)
    myGlobals.image_preview_convert = image_quantize_c64_colors(myGlobals.image_preview_convert)

    #prepare image_preview (this image will only be seen in preview window)
    if (myGlobals.user_outputformat.get() == "koala") :
        myGlobals.image_preview = myGlobals.image_preview_convert.resize((320,200), resample=PilImage.NEAREST)
    if (myGlobals.user_outputformat.get() == "hires") :
        myGlobals.image_preview = myGlobals.image_preview_convert

    myGlobals.image_previewTk = ImageTk.PhotoImage(myGlobals.image_preview)
    myGlobals.label_preview_image.configure(image=myGlobals.image_previewTk)
    myGlobals.label_preview_image.image = myGlobals.image_previewTk # keep a reference!

    #converting every time the image is refreshed: takes a lot of time and cpu power
    #convert()


	
	

def preview_scale(
    scale_value
):
    image_refresh()



def OpenSettings():
    myGlobals.textbox.delete('1.0', tk.END)      #clear textbox

    ftypes = [('settings', '*.json')]
    filename = askopenfilename(filetypes = ftypes)
    #filename = 'settings.json'  #debug
    if not filename : return None

    myGlobals.textbox.insert(tk.END,'Reading settings from file "%s"...\n'%filename)

    #https://docs.python.org/2.7/library/configparser.html#examples
    #with open(filename, "r") as f: data = json.load(f)

    try:
        f = open(filename, "r")
    except FileNotFoundError as err:
        myGlobals.textbox.insert(tk.END,'FileNotFoundError: "%s"\n'%format(err))
        print("FileNotFoundError: {0}".format(err))
        return None

    data = json.load(f)

    sanity_check = False
    if ('info' in data) :
        if ('content' in data['info']) :
            if (data['info']['content'] == 'settings') : sanity_check = True
    
    if (sanity_check == False) :
        myGlobals.textbox.insert(tk.END,'Wrong file format.\n')
        return None
    
    if ('start address' in data['settings']) : myGlobals.user_start_address.set(data['settings']['start address'])
    if ('start address checkbutton' in data['settings']) : myGlobals.user_start_address_checkbutton.set(data['settings']['start address checkbutton'])
    if ('sharpness' in data['settings']) : myGlobals.user_sharpness.set(data['settings']['sharpness'])
    if ('treshold' in data['settings']) : myGlobals.user_treshold.set(data['settings']['treshold'])
    if ('saturation' in data['settings']) : myGlobals.user_color_saturation.set(data['settings']['saturation'])
    if ('brightness' in data['settings']) : myGlobals.user_brightness.set(data['settings']['brightness'])
    if ('contrast' in data['settings']) : myGlobals.user_contrast.set(data['settings']['contrast'])
    if ('modes' in data['settings']) : myGlobals.user_modes.set(data['settings']['modes'])
    if ('outputformat' in data['settings']) : myGlobals.user_outputformat.set(data['settings']['outputformat'])
    if ('palette' in data['settings']) : myGlobals.user_palette.set(data['settings']['palette'])
    if ('filename' in data['settings']) : myGlobals.user_filename_open_textvariable.set(data['settings']['filename'])
    if ('effects blur' in data['settings']) : myGlobals.user_effects_blur.set(data['settings']['effects blur'])
    if ('effects detail' in data['settings']) : myGlobals.user_effects_detail.set(data['settings']['effects detail'])
    if ('effects enhance' in data['settings']) : myGlobals.user_effects_enhance.set(data['settings']['effects enhance'])
    if ('effects enhance more' in data['settings']) : myGlobals.user_effects_enhance_more.set(data['settings']['effects enhance more'])
    if ('effects smooth' in data['settings']) : myGlobals.user_effects_smooth.set(data['settings']['effects smooth'])
    if ('effects smooth more' in data['settings']) : myGlobals.user_effects_smooth_more.set(data['settings']['effects smooth more'])
    if ('effects sharpen' in data['settings']) : myGlobals.user_effects_sharpen.set(data['settings']['effects sharpen'])
    if ('effects showclashes' in data['settings']) : myGlobals.user_effects_showClashes.set(data['settings']['effects showclashes'])
    if ('gradient sceme' in data['settings']) : myGlobals.user_gradient_sceme.set(data['settings']['gradient sceme'])
    if ('dithering' in data['settings']) : myGlobals.user_dithering.set(data['settings']['dithering'])
    if ('background color' in data['settings']) : myGlobals.user_backgroundcolor.set(data['settings']['background color'])
    
    #myGlobals.textbox.insert(tk.END,"%d colors read.\n"%myGlobals.user_custom_gradient_sceme_size)
    
    image_refresh()    


def OpenGradient():
    myGlobals.textbox.delete('1.0', tk.END)      #clear textbox

    ftypes = [('gradient', '*.json')]
    filename = askopenfilename(filetypes = ftypes)
    if not filename : return None

    myGlobals.textbox.insert(tk.END,"Reading custom gradient from file \"%s\"...\n"%filename)

    #https://docs.python.org/2.7/library/configparser.html#examples
    with open(filename, "r") as f: config = json.load(f)

    #get size
    myGlobals.user_custom_gradient_sceme_size = int(config['size'])

    #apply values
    for a in range(0,len(myGlobals.user_custom_gradient_sceme)) :
        myGlobals.user_custom_gradient_sceme[a] = int(config['color'+str(a)])

    myGlobals.textbox.insert(tk.END,"%d colors read.\n"%myGlobals.user_custom_gradient_sceme_size)

    """
    for a in range(0,16) :
        myGlobals.textbox.insert(tk.END,"color %d: %d\n"%(a,myGlobals.user_custom_gradient_sceme[a]))
    """
    
    image_refresh()    








def OpenFile():
    #global user_filename_open
    myGlobals.user_filename_open = ""
    
    ftypes = [('Image Files', '*.tif *.jpg *.png *.bmp *.gif')]
    myGlobals.user_filename_open = askopenfilename(filetypes = ftypes)
    if not myGlobals.user_filename_open : return None
    
    loadFile(myGlobals.user_filename_open)



def loadFile(user_filename_open):    
    #print('load "%s"'%user_filename_open)

    myGlobals.user_filename_open_textvariable.set("\"..."+user_filename_open[-30:]+"\"")
    load_image(user_filename_open)
#    convert()    



def SaveFile():
    myGlobals.textbox.delete('1.0', tk.END)      #clear textbox

    user_filename_save = ""
    if (myGlobals.user_outputformat.get() == "koala") :
        ftypes = [('koala', '*.koa')]
    if (myGlobals.user_outputformat.get() == "hires") :
        ftypes = [('hires', '*.hir')]
    user_filename_save = asksaveasfilename(filetypes = ftypes)
    if not user_filename_save : return None

    convert()

    out_buffer = []
    
    #start address
    if (myGlobals.user_start_address_checkbutton.get() == True) :
        try:
            var_start_address = int (myGlobals.user_start_address.get(),16)
        except ValueError:
            var_start_address = 0

        if (var_start_address > 0xffff) :
            myGlobals.textbox.insert(tk.END, "*** error: Start address has to be 0-65535 (2bytes). Setting to $6000.\n")
            var_start_address = 0x6000    #dirty fix: set start address to $6000

        i=var_start_address & 0xff  #low
        out_buffer.append(i)
        i=var_start_address >> 8    #high
        out_buffer.append(i)
    
    #koala data
    for i in range(0,8000) : out_buffer.append(int(myGlobals.koala_bitmap[i]))
    for i in myGlobals.koala_col12 : out_buffer.append(i)
    if (myGlobals.user_outputformat.get() == "koala") :
        for i in myGlobals.koala_col3 : out_buffer.append(i)
        out_buffer.append(int(myGlobals.koala_bg))

    #write stuff...
    myGlobals.textbox.insert(tk.END, 'Writing image "%s".\n'%user_filename_save)
    file_out = open(user_filename_save , "wb")
    file_out.write(bytearray(out_buffer))
    file_out.close()



def SaveFile_clash_json():
    #user_filename_save_clash_json = args.clashes_json

    myGlobals.textbox.delete('1.0', tk.END)      #clear textbox

    user_filename = asksaveasfilename(filetypes = [('json', '*.json')])
    if not user_filename : return None

    write_settings_to_json_file(user_filename, myGlobals.color_clash_chars_xy)


def SaveSettings():
    #user_filename_save_clash_json = args.settings_json

    myGlobals.textbox.delete('1.0', tk.END)      #clear textbox

    user_filename = asksaveasfilename(filetypes = [('json', '*.json')])
    #user_filename = 'settings.json' #debug
    if not user_filename : return None

    data = {
        'start address' : myGlobals.user_start_address.get(),
        'start address checkbutton' : myGlobals.user_start_address_checkbutton.get(),
        'sharpness' : myGlobals.user_sharpness.get(),
        'treshold' : myGlobals.user_treshold.get(),
        'saturation' : myGlobals.user_color_saturation.get(),
        'brightness' : myGlobals.user_brightness.get(),
        'contrast' : myGlobals.user_contrast.get(),
        'modes' : myGlobals.user_modes.get(),
        'outputformat' : myGlobals.user_outputformat.get(),
        'palette' : myGlobals.user_palette.get(),
        'filename' : myGlobals.user_filename_open_textvariable.get(),
        'effects blur' : myGlobals.user_effects_blur.get(),
        'effects detail' : myGlobals.user_effects_detail.get(),
        'effects enhance' : myGlobals.user_effects_enhance.get(),
        'effects enhance more' : myGlobals.user_effects_enhance_more.get(),
        'effects smooth' : myGlobals.user_effects_smooth.get(),
        'effects smooth more' : myGlobals.user_effects_smooth_more.get(),
        'effects sharpen' : myGlobals.user_effects_sharpen.get(),
        'effects showclashes' : myGlobals.user_effects_showClashes.get(),
        'gradient sceme' : myGlobals.user_gradient_sceme.get(),
        'dithering' : myGlobals.user_dithering.get(),
        'background color' : myGlobals.user_backgroundcolor.get(),
    }

    write_settings_to_json_file(user_filename , data)



def SaveFile_clash_image():
    #global user_filename_save_clash_image
    myGlobals.user_filename_save_clash_image = ""

    #global textbox
    myGlobals.textbox.delete('1.0', tk.END)      #clear textbox

    myGlobals.user_filename_save_clash_image = asksaveasfilename(filetypes = [('image', '*.png')])

    if not myGlobals.user_filename_save_clash_image : return None

    print ('    Opening image-file "%s" for writing...' % myGlobals.user_filename_save_clash_image, end='')
    myGlobals.image_clashes.save(myGlobals.user_filename_save_clash_image)
    print ('done.')
    
    return None




def reset_modifiers():
    #global scale_modifier_list
    for a in range(0,len(myGlobals.scale_modifier_list)):
        myGlobals.scale_modifier_list[a].set( myGlobals.scale_modifier_list_default[a])


