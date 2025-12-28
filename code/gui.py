import code.myGlobals as myGlobals
import code.action as action
import code.gui_help as gui_help
import code.gui_about as gui_about
import tkinter as tk
import tkinter.filedialog as filedialog



def create_drop_down_menu (
	root
) :
    menu = tk.Menu(myGlobals.root)
    root.config(menu=menu)

    filemenu = tk.Menu(menu)
    infomenu = tk.Menu(menu)

    filemenu.add_command(label="open image...", command=action.OpenFile, underline=0, accelerator="Alt+O")
    filemenu.add_command(label="save image...", command=action.SaveFile, underline=0, accelerator="Alt+S")
    filemenu.add_separator()
    filemenu.add_command(label="open settings...", command=action.OpenSettings, underline=1, accelerator="Alt+P")
    filemenu.add_command(label="save settings...", command=action.SaveSettings, underline=1, accelerator="Alt+V")
    filemenu.add_separator()
    filemenu.add_command(label="save color-clash image...", command=action.SaveFile_clash_image)
    filemenu.add_command(label="save color-clash json...", command=action.SaveFile_clash_json)
    filemenu.add_separator()
    filemenu.add_command(label="open custom gradient...", command=action.OpenGradient)
#    filemenu.add_command(label="save custom gradient...", command=action.action_SaveGradient, underline=5, accelerator="Alt+H")
    filemenu.add_separator()
    filemenu.add_command(label="quit", command=root.quit, underline=0, accelerator="Alt+Q")

    infomenu.add_command(label="help", command=gui_help.create_gui, underline=0, accelerator="f1")
    infomenu.add_command(label="about", command=gui_about.create_gui)

    #add all menus
    menu.add_cascade(label="menu", menu=filemenu, underline=0, accelerator="Alt+m")
    menu.add_cascade(label="info", menu=infomenu, underline=0, accelerator="Alt+i")





def create_gui_settings_modifiers (
	root,
    _row,
    _column
) :
    #global scale_modifier_list, scale_modifier_list_default

#scales modifiers
    frame_border = tk.Frame(
        root,
        bg=myGlobals.BGCOLOR,
        bd=myGlobals._bd,
    )
    frame_border.grid(
        row=_row,
        column=_column
    )
    frame_inner = tk.Frame(
        frame_border,
        bg=myGlobals.BGCOLOR,
        bd=1,
        padx = myGlobals._padx,
        pady = myGlobals._pady,
        relief=tk.RAISED
        )
    frame_inner.grid()
    frame_inner.grid_columnconfigure(0, weight=1)
    frame_inner.grid_rowconfigure(0, weight=1)

    _row=0
    label = tk.Label(
        frame_inner,
        bg=myGlobals.BGCOLOR,
        text="modifiers",
        wraplength=100,
        anchor='c',
        justify='left',
        fg="#000088"
    )
    label.grid(
        row=_row,
        column=0,
        sticky=tk.W+tk.E
    )

    MODIFIERS = [
        #text, variable, row, column
        ("saturation", myGlobals.user_color_saturation, 1,0, 1,100),
        ("brightness", myGlobals.user_brightness, 2,0, 1,100),
        ("contrast", myGlobals.user_contrast, 3,0, 1,100),
        ("sharpness", myGlobals.user_sharpness, 4,0, 1,100),
        ("dithering treshold", myGlobals.user_treshold, 5,0, 2,20),
    ]

    myGlobals.scale_modifier_list=[]
    myGlobals.scale_modifier_list_default=[]
    for text, var, my_row, my_column, low, high in MODIFIERS:
        scale_modifier = tk.Scale(
            frame_inner,
            bg=myGlobals.BGCOLOR,
            from_=low,
            to=high,
            orient=tk.HORIZONTAL,
            variable=var,
            label=text,
            length=200,
            cursor=myGlobals.CURSOR_HAND,
            command=action.preview_scale
        )
        scale_modifier.grid(
            row=my_row,
            column=my_column,
            sticky='w'
        )
        #set default value
        scale_modifier.set(high/2)
        myGlobals.scale_modifier_list.append(scale_modifier)
        myGlobals.scale_modifier_list_default.append(high/2)
        
#        last_row = my_row
 
    button_reset = tk.Button(
        frame_inner,
        bg=myGlobals.BGCOLOR,
        text = "reset",
        command=action.reset_modifiers,
        cursor=myGlobals.CURSOR_HAND,
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
    frame_border = tk.Frame(
        root,
        bg=myGlobals.BGCOLOR,
        bd=myGlobals._bd,
    )
    frame_border.grid(
        row=_row,
        column=_column
    )
    frame_inner = tk.Frame(
        frame_border,
        bg=myGlobals.BGCOLOR,
        bd=1,
        padx = myGlobals._padx,
        pady = myGlobals._pady,
        relief=tk.RAISED
        )
    frame_inner.grid()
    frame_inner.grid_columnconfigure(0, weight=1)
    frame_inner.grid_rowconfigure(0, weight=1)
    
    _row = 0
    label = tk.Label(
        frame_inner,
        bg=myGlobals.BGCOLOR,
        text="options",
        wraplength=100,
        anchor='c',
        justify='left',
        fg="#000088"
    )
    label.grid(
        row=_row,
        column=0,
        sticky=tk.W+tk.E,
        columnspan=2
    )
    EFFECTS = [
        #text, variable, row, column
        ("blur",					myGlobals.user_effects_blur,						1,0),
        ("detail",					myGlobals.user_effects_detail, 					2,0),
        ("enhance",					myGlobals.user_effects_enhance, 					3,0),
        ("enhance_more",			myGlobals.user_effects_enhance_more, 				4,0),
        ("smooth",					myGlobals.user_effects_smooth, 					1,1),
        ("smooth_more",				myGlobals.user_effects_smooth_more,				2,1),
        ("sharpen",					myGlobals.user_effects_sharpen,					3,1),
        ("show clashes",			myGlobals.user_effects_showClashes,				4,1),
 
    ]
    for text,var, my_row, my_column in EFFECTS:
        checkbutton_effects = tk.Checkbutton(
            frame_inner,
            bg=myGlobals.BGCOLOR,
            text=text,
            variable=var,
            cursor=myGlobals.CURSOR_HAND,
            command=action.image_refresh
        )
        checkbutton_effects.grid(
            row=my_row,
            column=my_column,
            sticky=tk.W
        )




def create_gui_settings_outputformat (
	root,
    _row,
    _column
) :
#mode radiobuttons
#http://effbot.org/tkinterbook/radiobutton.htm
    frame_border = tk.Frame(
        root,
        bg=myGlobals.BGCOLOR,
        bd=myGlobals._bd,
    )
    frame_border.grid(
        row=_row,
        column=_column
    )
    frame_inner = tk.Frame(
        frame_border,
        bg=myGlobals.BGCOLOR,
        bd=1,
        padx = myGlobals._padx,
        pady = myGlobals._pady,
        relief=tk.RAISED
        )
    frame_inner.grid()
    frame_inner.grid_columnconfigure(0, weight=1)
    frame_inner.grid_rowconfigure(0, weight=1)

    label = tk.Label(
        frame_inner,
        bg=myGlobals.BGCOLOR,
        text="output format",
        wraplength=100,
        anchor="c",
        justify='left',
        fg="#000088"
    )
    label.grid(
        row=0,
        column=0,
        sticky=tk.W+tk.E,
        columnspan=2
    )
    MODES = [
            ("koala", "koala",1,0),
            ("hires", "hires",1,1),
    ]

    for text, mode, row, column in MODES:
        radiobutton_user_mode = tk.Radiobutton(
            frame_inner,
            bg=myGlobals.BGCOLOR,
            text = text,
            value = mode,
            indicatoron=0,
            variable=myGlobals.user_outputformat,
            cursor=myGlobals.CURSOR_HAND,
            command=action.image_refresh
        )
        radiobutton_user_mode.grid(
            row=row,
            column=column,
            sticky=tk.W+tk.E
        )




def create_gui_settings_mode (
	root,
    _row,
    _column
) :
#mode radiobuttons
#http://effbot.org/tkinterbook/radiobutton.htm
    frame_border = tk.Frame(
        root,
        bg=myGlobals.BGCOLOR,
        bd=myGlobals._bd,
    )
    frame_border.grid(
        row=_row,
        column=_column
    )
    frame_inner = tk.Frame(
        frame_border,
        bg=myGlobals.BGCOLOR,
        bd=1,
        padx = myGlobals._padx,
        pady = myGlobals._pady,
        relief=tk.RAISED
        )
    frame_inner.grid()
    frame_inner.grid_columnconfigure(0, weight=1)
    frame_inner.grid_rowconfigure(0, weight=1)

    _row = 0
    label = tk.Label(
        frame_inner,
        bg=myGlobals.BGCOLOR,
        text="mode",
        wraplength=100,
        anchor="c",
        justify='left',
        fg="#000088"
    )
    label.grid(
        row=_row,
        column=1,
        sticky=tk.W+tk.E
    )
    MODES = [
            ("keep colors", "colors"),
            ("brightness palette", "palette"),
    ]

    for text, mode in MODES:
        radiobutton_user_mode = tk.Radiobutton(
            frame_inner,
            bg=myGlobals.BGCOLOR,
            text = text,
            value = mode,
            indicatoron=0,
            variable=myGlobals.user_modes,
            cursor=myGlobals.CURSOR_HAND,
            command=action.image_refresh
        )
        _row += 1
        radiobutton_user_mode.grid(
            row=_row,
            column=1,
            sticky=tk.W+tk.E
        )




def create_gui_backgroundcolor (
	root,
    _row,
    _column
) :
    frame_border = tk.Frame(
        root,
        bg=myGlobals.BGCOLOR,
        bd=myGlobals._bd,
    )
    frame_border.grid(
        row=_row,
        column=_column
    )
    frame_inner = tk.Frame(
        frame_border,
        bg=myGlobals.BGCOLOR,
        bd=1,
        padx = myGlobals._padx,
        pady = myGlobals._pady,
        relief=tk.RAISED
        )
    frame_inner.grid()
    frame_inner.grid_columnconfigure(0, weight=1)
    frame_inner.grid_rowconfigure(0, weight=1)

    _row = 0
    label = tk.Label(
        frame_inner,
        bg=myGlobals.BGCOLOR,
        text="background color ($d021)",
        anchor="c",
        justify='left',
        fg="#000088"
    )
    label.grid(
        row=_row,
        column=1,
        sticky=tk.W+tk.E,
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
            myGlobals.PALETTEDATA_PEPTO[(value*3)+0],
            myGlobals.PALETTEDATA_PEPTO[(value*3)+1],
            myGlobals.PALETTEDATA_PEPTO[(value*3)+2]
        )
        radiobutton_user_value = tk.Radiobutton(
            frame_inner,
            value = value,
            width=2,
            indicatoron=0,
            variable = myGlobals.user_backgroundcolor,
            background = mycolor,
            activebackground = mycolor,
            selectcolor = mycolor,
            cursor = myGlobals.CURSOR_HAND,
            bd=4,
            relief=tk.GROOVE,
            offrelief=tk.RAISED,
            #command=action_convert
        )
        radiobutton_user_value.grid(
            row=2+my_row,
            column=my_column,
            sticky=tk.W+tk.E
        )

    radiobutton_automatic = tk.Radiobutton(
        frame_inner,
        bg=myGlobals.BGCOLOR,
        value = 99,
        text="auto",
        indicatoron=0,
        variable=myGlobals.user_backgroundcolor,
        cursor=myGlobals.CURSOR_HAND
        #command=action.convert
    )
    radiobutton_automatic.grid(
        row=1,
        column=0,
        sticky=tk.W+tk.E,
        columnspan=8
    )



def create_gui_palette_brightness_mode (
	root,
    _row,
    _column
) :
    frame_border = tk.Frame(
        root,
        bg=myGlobals.BGCOLOR,
        bd=myGlobals._bd,
    )
    frame_border.grid(
        row=_row,
        column=_column
    )
    frame_inner = tk.Frame(
        frame_border,
        bg=myGlobals.BGCOLOR,
        bd=1,
        padx = myGlobals._padx,
        pady = myGlobals._pady,
        relief=tk.RAISED
        )
    frame_inner.grid()
    frame_inner.grid_columnconfigure(0, weight=1)
    frame_inner.grid_rowconfigure(0, weight=1)

    label = tk.Label(
        frame_inner,
        bg=myGlobals.BGCOLOR,
        text="brightness palette",
        wraplength=100,
        anchor="c",
        justify='left',
        fg="#000088"
    )
    label.grid(
        row=0,
        column=0,
        sticky=tk.W+tk.E,
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
        radiobutton_user_mode = tk.Radiobutton(
            frame_inner,
            bg=myGlobals.BGCOLOR,
            text = text,
            value = mode,
            indicatoron=0,
            variable=myGlobals.user_gradient_sceme,
            command=action.image_refresh,
            cursor=myGlobals.CURSOR_HAND
        )
        radiobutton_user_mode.grid(
            row=row,
            column=column,
            sticky=tk.W+tk.E
        )



def create_gui_dithering (
	root,
    _row,
    _column
) :
    frame_border = tk.Frame(
        root,
        bg=myGlobals.BGCOLOR,
        bd=myGlobals._bd,
    )
    frame_border.grid(
        row=_row,
        column=_column
    )
    frame_inner = tk.Frame(
        frame_border,
        bg=myGlobals.BGCOLOR,
        bd=1,
        padx = myGlobals._padx,
        pady = myGlobals._pady,
        relief=tk.RAISED
        )
    frame_inner.grid()
    frame_inner.grid_columnconfigure(0, weight=1)
    frame_inner.grid_rowconfigure(0, weight=1)

    label = tk.Label(
        frame_inner,
        bg=myGlobals.BGCOLOR,
        text="dithering",
        wraplength=100,
        anchor="c",
        justify='left',
        fg="#000088"
    )
    label.grid(
        row=0,
        column=0,
        sticky=tk.W+tk.E,
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
        radiobutton_user_mode = tk.Radiobutton(
            frame_inner,
            bg=myGlobals.BGCOLOR,
            text = text,
            value = mode,
            indicatoron=0,
            variable=myGlobals.user_dithering,
            command=action.image_refresh,
            cursor=myGlobals.CURSOR_HAND
        )
        radiobutton_user_mode.grid(
            row=row,
            column=column,
            sticky=tk.W+tk.E
        )




def create_gui_settings_palette (
	root,
    _row,
    _column
) :
#palette radiobuttons
#http://effbot.org/tkinterbook/radiobutton.htm
    frame_border = tk.Frame(
        root,
        bg=myGlobals.BGCOLOR,
        bd=myGlobals._bd,
    )
    frame_border.grid(
        row=_row,
        column=_column
    )
    frame_inner = tk.Frame(
        frame_border,
        bg=myGlobals.BGCOLOR,
        bd=1,
        padx = myGlobals._padx,
        pady = myGlobals._pady,
        relief=tk.RAISED
        )
    frame_inner.grid()
    frame_inner.grid_columnconfigure(0, weight=1)
    frame_inner.grid_rowconfigure(0, weight=1)

    label = tk.Label(
        frame_inner,
        bg=myGlobals.BGCOLOR,
        text="palette",
        wraplength=100,
        anchor='c',
        justify='left',
        fg="#000088"
    )
    label.grid(
        row=0,
        column=0,
        sticky=tk.W+tk.E,
        columnspan=2
    )
    MODES = [
            ("colodore", "colodore",1,0),
            ("pepto", "pepto",2,0),
            ("view64", "view64",1,1),
            ("vice", "vice",2,1),
        ]

    for text, mode, row, column in MODES:
        radiobutton_user_mode = tk.Radiobutton(
            frame_inner,
            bg=myGlobals.BGCOLOR,
            text = text,
            value = mode,
            indicatoron=0,
            variable=myGlobals.user_palette,
            cursor=myGlobals.CURSOR_HAND,
            command=action.image_refresh
        )
        radiobutton_user_mode.grid(
            row=row,
            column=column,
            sticky=tk.W+tk.E
        )




def create_gui_settings_startaddress (
	root,
    _row,
    _column
) :
    frame_border = tk.Frame(
        root,
        bg=myGlobals.BGCOLOR,
        bd=myGlobals._bd,
    )
    frame_border.grid(
        row=_row,
        column=_column
    )
    frame_inner = tk.Frame(
        frame_border,
        bg=myGlobals.BGCOLOR,
        bd=1,
        padx = myGlobals._padx,
        pady = myGlobals._pady,
        relief=tk.RAISED
        )
    frame_inner.grid()
    frame_inner.grid_columnconfigure(0, weight=1)
    frame_inner.grid_rowconfigure(0, weight=1)
    
    label_start_address_title = tk.Label(
        frame_inner,
        bg=myGlobals.BGCOLOR,
        text="start address in hex:",
        anchor='c',
        fg="#000088"
    )
    checkbutton_start_address = tk.Checkbutton(
        frame_inner,
        bg=myGlobals.BGCOLOR,
        variable = myGlobals.user_start_address_checkbutton
        )
    label_start_address = tk.Label(
        frame_inner,
        bg=myGlobals.BGCOLOR,
        text="values $0-$ffff $",
        anchor='c'
    )
    entry_start_address= tk.Entry(
        frame_inner,
        bg=myGlobals.BGCOLOR,
        width=8,
        textvariable = myGlobals.user_start_address
    )
    #placement in grid layout
    label_start_address_title.grid(
        row=0,
        column=0,
        sticky=tk.W+tk.E,
        columnspan=3
    )
    checkbutton_start_address.grid(
        row=1,
        column=0,
        sticky=tk.W
    )
    label_start_address.grid(
        row=1,
        column=1,
        sticky=tk.W+tk.E
    )
    entry_start_address.grid(
        row=1,
        column=2,
        sticky=tk.E
    )
    myGlobals.user_start_address.set("6000")
    myGlobals.user_start_address_checkbutton.set(1)






def create_gui_filename (
	root,
    _row,
    _column
) :
    
    frame_border = tk.Frame(
        root,
        bg=myGlobals.BGCOLOR,
        bd=myGlobals._bd,
    )
    frame_border.grid(
        row=_row,
        column=_column
    )
    frame_inner = tk.Frame(
        frame_border,
        bg=myGlobals.BGCOLOR,
        bd=1,
        padx = myGlobals._padx,
        pady = myGlobals._pady,
        relief=tk.RAISED
        )
    frame_inner.grid()
    frame_inner.grid_columnconfigure(0, weight=1)
    frame_inner.grid_rowconfigure(0, weight=1)
    
    label_title = tk.Label(
        frame_inner,
        bg=myGlobals.BGCOLOR,
        text="image",
        anchor='c',
        fg="#000088"
    )
    label_filename = tk.Label(
        frame_inner,
        bg=myGlobals.BGCOLOR,
        textvariable = myGlobals.user_filename_open_textvariable,
        anchor='c'
    )
    #placement in grid layout
    label_title.grid(
        row=0,
        column=0,
        sticky=tk.W+tk.E
    )
    label_filename.grid(
        row=1,
        column=0,
        sticky=tk.W+tk.E
    )




def create_gui_action_buttons (
	root,
    _row,
    _column
) :
    frame_border = tk.Frame(
        root,
        bg=myGlobals.BGCOLOR,
        bd=myGlobals._bd,
    )
    frame_border.grid(
        row=_row,
        column=_column
    )
    frame_inner = tk.Frame(
        frame_border,
        bg=myGlobals.BGCOLOR,
        bd=1,
        padx = myGlobals._padx,
        pady = myGlobals._pady,
        relief=tk.RAISED
        )
    frame_inner.grid()
    frame_inner.grid_columnconfigure(0, weight=1)
    frame_inner.grid_rowconfigure(0, weight=1)
    
    button_convert = tk.Button(
        frame_inner,
        bg=myGlobals.BGCOLOR,
        textvariable = myGlobals.convertbutton_text,
        width=7,
        height=3,
        command=action.convert,
        cursor=myGlobals.CURSOR_HAND
    )
    #placement in grid layout
    button_convert.grid(
        row=0,
        column=0,
        sticky=tk.W+tk.E
    )






def create_gui_text (
    root,
    _row,
    _column
) :
    #creation of elements
    #global textbox

    frame_border = tk.Frame(
        root,
        bg=myGlobals.BGCOLOR,
        bd=myGlobals._bd,
    )
    frame_border.grid(
        row=_row,
        column=_column
    )
    frame_inner = tk.Frame(
        frame_border,
        bg=myGlobals.BGCOLOR,
        bd=1,
        padx = myGlobals._padx,
        pady = myGlobals._pady,
        relief=tk.RAISED
        )
    frame_inner.grid()
    frame_inner.grid_columnconfigure(0, weight=1)
    frame_inner.grid_rowconfigure(0, weight=1)

    label_textbox_text = tk.Label(
		frame_inner,
        bg=myGlobals.BGCOLOR,
		text="converter output",
        fg="#000088"
	)
    myGlobals.textbox = tk.Text(
        frame_inner,
        height=10,
        width=40
    )

    #placement in grid layout
    label_textbox_text.grid(
        row=0,
        column=0,
        sticky=tk.W+tk.E
    )
    myGlobals.textbox.grid(
        row=1,
        column=0,
        sticky=tk.W+tk.E
    )







def create_gui_image_original (
	root,
    _row,
    _column
) :
    #global label_original_image
    
    frame_border = tk.Frame(
        root,
        bg=myGlobals.BGCOLOR,
        bd=myGlobals._bd,
    )
    frame_border.grid(
        row=_row,
        column=_column
    )
    frame_inner = tk.Frame(
        frame_border,
        bg=myGlobals.BGCOLOR,
        bd=1,
        padx = myGlobals._padx,
        pady = myGlobals._pady,
        relief=tk.RAISED
        )
    frame_inner.grid()
    frame_inner.grid_columnconfigure(0, weight=1)
    frame_inner.grid_rowconfigure(0, weight=1)
    
    #creation of elements
    label_original_text = tk.Label(
		frame_inner,
        bg=myGlobals.BGCOLOR,
		text="original",
        fg="#000088"
	)
    myGlobals.label_original_image = tk.Label(
        frame_inner,
        bg=myGlobals.BGCOLOR
    )
	
    #placement in grid layout
    label_original_text.grid(
        row=0,
        column=0,
        sticky=tk.W+tk.E
    )
    myGlobals.label_original_image.grid(
        row=1,
        column=0,
        sticky=tk.W+tk.E
    )



def create_gui_image_preview (
	root,
    _row,
    _column
) :
    #global label_preview_image
    
    frame_border = tk.Frame(
        root,
        bg=myGlobals.BGCOLOR,
        bd=myGlobals._bd,
    )
    frame_border.grid(
        row=_row,
        column=_column
    )
    frame_inner = tk.Frame(
        frame_border,
        bg=myGlobals.BGCOLOR,
        bd=1,
        padx = myGlobals._padx,
        pady = myGlobals._pady,
        relief=tk.RAISED
        )
    frame_inner.grid()
    frame_inner.grid_columnconfigure(0, weight=1)
    frame_inner.grid_rowconfigure(0, weight=1)
    
    #creation of elements
    label_preview_text = tk.Label(
		frame_inner,
        bg=myGlobals.BGCOLOR,
		text="preview",
        fg="#000088"
	)
    myGlobals.label_preview_image = tk.Label(
        frame_inner,
        bg=myGlobals.BGCOLOR
    )
	
    #placement in grid layout
    label_preview_text.grid(
        row=0,
        column=0,
        sticky=tk.W+tk.E
    )
    myGlobals.label_preview_image.grid(
        row=1,
        column=0,
        sticky=tk.W+tk.E
    )




def create_gui_image_koala (
	root,
    _row,
    _column
) :
    #global label_koala_image
    
    frame_border = tk.Frame(
        root,
        bg=myGlobals.BGCOLOR,
        bd=myGlobals._bd,
    )
    frame_border.grid(
        row=_row,
        column=_column
    )
    frame_inner = tk.Frame(
        frame_border,
        bg=myGlobals.BGCOLOR,
        bd=1,
        padx = myGlobals._padx,
        pady = myGlobals._pady,
        relief=tk.RAISED
        )
    frame_inner.grid()
    frame_inner.grid_columnconfigure(0, weight=1)
    frame_inner.grid_rowconfigure(0, weight=1)
    
    #creation of elements
    label_koala_text = tk.Label(
		frame_inner,
        bg=myGlobals.BGCOLOR,
		text="output",
        fg="#000088"
	)
    myGlobals.label_koala_image = tk.Label(
        frame_inner,
        bg=myGlobals.BGCOLOR
    )
	
    #placement in grid layout
    label_koala_text.grid(
        row=0,
        column=0,
        sticky=tk.W+tk.E
    )
    myGlobals.label_koala_image.grid(
        row=1,
        column=0,
        sticky=tk.W+tk.E
    )




    
def _start_gui() :
    #main procedure
    title_string = myGlobals.PROGNAME+" "+myGlobals.VERSION
    myGlobals.root.title(title_string)
    #print("%s %s *** by WolF"% (myGlobals.PROGNAME, myGlobals.VERSION))

    myGlobals.root.configure(background = myGlobals.BGCOLOR)
    myGlobals.root.iconphoto(False, tk.PhotoImage(file = myGlobals.RES_GFX_ICON))


    myGlobals.root.grid_columnconfigure(0, weight=10)
    myGlobals.root.grid_rowconfigure(0, weight=10)


    frame_left = tk.Frame(myGlobals.root, bg=myGlobals.BGCOLOR)
    frame_left.grid(
        row=0,
        column=0,
        sticky=tk.N
    )
    frame_left.grid_columnconfigure(0, weight=1)
    frame_left.grid_rowconfigure(0, weight=1)

    frame_middle = tk.Frame(myGlobals.root, bg=myGlobals.BGCOLOR)
    frame_middle.grid(
        row=0,
        column=1,
        sticky=tk.N
    )
    frame_middle.grid_columnconfigure(0, weight=1)
    frame_middle.grid_rowconfigure(0, weight=1)

    frame_right = tk.Frame(myGlobals.root, bg=myGlobals.BGCOLOR)
    frame_right.grid(
        row=0,
        column=2,
        sticky=tk.N
    )
    frame_right.grid_columnconfigure(0, weight=1)
    frame_right.grid_rowconfigure(0, weight=1)


    create_drop_down_menu(
        myGlobals.root
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


    #frame_right elements
    create_gui_filename(
        frame_middle,
        0,  #row
        0   #column
    )
    create_gui_settings_mode(
        frame_middle,
        1,  #row
        0   #column
    )
    create_gui_palette_brightness_mode(
        frame_middle,
        2,  #row
        0   #column
    )
    create_gui_dithering(
        frame_middle,
        3,  #row
        0   #column
    )
    create_gui_backgroundcolor(
        frame_middle,
        4,  #row
        0   #column
    )
    create_gui_settings_startaddress(
        frame_middle,
        5,  #row
        0   #column
    )
    create_gui_text(
        frame_middle,
        6,  #row
        0   #column
    )




    #frame_middle elements
    create_gui_image_koala(
        frame_right,
        0,  #row
        0   #column
    )
    create_gui_image_preview(
        frame_right,
        1,  #row
        0   #column
    )
    create_gui_image_original(
        frame_right,
        2,  #row
        0   #column
    )


            

    action.create_empty_images()
    
    

