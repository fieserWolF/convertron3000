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
    print("%s %s *** by fieserWolF"% (myGlobals.PROGNAME, myGlobals.VERSION))

    #https://docs.python.org/3/library/argparse.html
    parser = argparse.ArgumentParser(
        description='This program reads an image-file, lets the user adjust settings and converts it to a C64 koala or hires image.',
        epilog='Example: '+sys.argv[0]+' -i image.png -c /tmp/clashes.json -d'
    )
    parser.add_argument('-i', '--image', dest='input_image', help='image file)')
    #parser.add_argument('-c', '--clashes', dest='clashes_json', help='filename of report containing all color-clashes (in json-format (default="'+FILENAME_JSON_PRE+'")', default=FILENAME_JSON_PRE)
    #parser.add_argument('-o', '--output', dest='clashes_image', help='filename of color-clash image (default="'+FILENAME_CLASH_IMAGE_PRE+'")', default=FILENAME_CLASH_IMAGE_PRE)
    parser.add_argument('-d', '--debug', dest='debug_clashes', help='show color-clashes on consule', action='store_true')
    myGlobals.args = parser.parse_args()
    
    gui._start_gui()

    if (myGlobals.args.input_image) :
        action.loadFile(myGlobals.args.input_image)


    #keyboard shortcuts
    myGlobals.root.bind_all("<Alt-q>", lambda event: myGlobals.root.quit())
    myGlobals.root.bind_all("<Alt-o>", lambda event: action.OpenFile())
    myGlobals.root.bind_all("<Alt-s>", lambda event: action.SaveFile())
    myGlobals.root.bind_all("<F1>", lambda event: gui_help.create_gui())
    myGlobals.root.bind_all("<Alt-c>", lambda event: action.convert())
    myGlobals.root.bind_all("<Alt-d>", lambda event: action.debug_settings())
    myGlobals.root.bind_all("<Alt-p>", lambda event: action.OpenSettings())
    myGlobals.root.bind_all("<Alt-v>", lambda event: action.SaveSettings())
    #myGlobals.root.bind_all("<Alt-g>", lambda event: action.OpenGradient())
    #myGlobals.root.bind_all("<Alt-h>", lambda event: action.action_SaveGradient())

    #action.SaveSettings()
    #action.OpenSettings()

    

    tk.mainloop()




if __name__ == '__main__':
    _main_procedure()

