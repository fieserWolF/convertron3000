import code.myGlobals as myGlobals
import code.gui as gui
import code.action as action
import code.gui_help as gui_help
import code.gui_about as gui_about
import sys

import tkinter as tk
import argparse


def _main_procedure() :
    #global args
    print("%s %s *** by fieserWolF" % (myGlobals.PROGNAME, myGlobals.VERSION))

    #https://docs.python.org/3/library/argparse.html
    parser = argparse.ArgumentParser(
        description='This program reads an image-file, lets the user adjust settings and converts it to a C64 koala or hires image.',
        epilog='Example: '+sys.argv[0]+' -i image.png -g 8color_gradient-brown.json -s settings.json -d'
    )
    parser.add_argument('-i', '--image', dest='input_image', help='image file)')
    parser.add_argument('-g', '--gradient', dest='file_gradient', help='filename of custom gradient file (JSON) to be loaded')
    parser.add_argument('-s', '--settings', dest='file_settings', help='filename of settings file (JSON) to be loaded')
    #parser.add_argument('-c', '--clashes', dest='clashes_json', help='filename of report containing all color-clashes (in json-format (default="'+FILENAME_JSON_PRE+'")', default=FILENAME_JSON_PRE)
    #parser.add_argument('-o', '--output', dest='clashes_image', help='filename of color-clash image (default="'+FILENAME_CLASH_IMAGE_PRE+'")', default=FILENAME_CLASH_IMAGE_PRE)
    parser.add_argument('-d', '--debug', dest='debug_clashes', help='show color-clashes on consule', action='store_true')
    myGlobals.args = parser.parse_args()

    #apply default values, do this before gui._start_gui() because of default values for the tk.Scale sliders
    for my_key, my_value in myGlobals.settings.items() :
        myGlobals.root.setvar(name=my_key, value=my_value)
    
    gui._start_gui()

    if (myGlobals.args.input_image) :
        action.OpenImage_Load(myGlobals.args.input_image)

    if (myGlobals.args.file_gradient) :
        action.OpenGradient_Load(myGlobals.args.file_gradient)

    if (myGlobals.args.file_settings) :
        action.OpenSettings_Load(myGlobals.args.file_settings)

    #keyboard shortcuts
    myGlobals.root.bind_all("<Alt-q>", lambda event: myGlobals.root.quit())
    myGlobals.root.bind_all("<Alt-o>", lambda event: action.OpenImage_FileDialog())
    myGlobals.root.bind_all("<Alt-s>", lambda event: action.SaveImage())
    myGlobals.root.bind_all("<F1>", lambda event: gui_help.create_gui())
    myGlobals.root.bind_all("<Alt-c>", lambda event: action.convert())
    myGlobals.root.bind_all("<Alt-d>", lambda event: action.debug_settings())
    myGlobals.root.bind_all("<Alt-p>", lambda event: action.OpenSettings_FileDialog())
    myGlobals.root.bind_all("<Alt-v>", lambda event: action.SaveSettings())


    """
    for my_key, my_value in myGlobals.settings.items() :
        print('%s : %s' % (my_key, myGlobals.root.getvar(name=my_key)))
    """


    tk.mainloop()




if __name__ == '__main__':
    _main_procedure()

