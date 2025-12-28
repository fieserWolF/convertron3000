import code.myGlobals as myGlobals
import tkinter as tk



def create_gui (
) :
    TEXT_HEIGHT=30

    def close_window():
        #global help_window
        #global help_window_open
        
        if (help_window_open == True) :
            help_window.destroy()
            help_window_open = False

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
    help_window = tk.Toplevel(
        bd=10
    )
    help_window.title("Help")
    help_window.configure(background=myGlobals.BGCOLOR)

    frame_left = tk.Frame( help_window)
    frame_right = tk.Frame( help_window)

    #http://effbot.org/tkinterbook/message.htm
    #text
    msg = tk.Text(
        frame_right,
#        bd=10,
        relief=tk.FLAT,
        width=80,
        height=30
    )

    #scrollbar
    msg_scrollBar = tk.Scrollbar(
        frame_right,
        bg=myGlobals.BGCOLOR
    )
    msg_scrollBar.config(command=msg.yview)
    msg.insert(tk.END, open(myGlobals.RES_DOC_HELP, encoding="utf_8").read())
    msg.config(yscrollcommand=msg_scrollBar.set)
    msg.config(state=tk.DISABLED)

    #label with image
    #http://effbot.org/tkinterbook/photoimage.htm
    #image = Image.open("wolf.jpg")
    #photo = ImageTk.PhotoImage(image)
    photo = tk.PhotoImage(file=myGlobals.RES_GFX_ABOUT)
    label_image = tk.Label(
        frame_left,
        bg=myGlobals.BGCOLOR,
#        bd=10,
        image=photo,
        padx=_padx,
        pady=_pady
    )
    label_image.image = photo # keep a reference!

    #button
    button = tk.Button(
        frame_left,
        bg=myGlobals.BGCOLOR,
        text="OK",
        command=help_window.destroy,
        padx=_padx,
        pady=_pady
    )


    #placement in grid
    frame_left.grid(
        row=0,
        column=0,
        sticky=tk.W
    )
    frame_right.grid(
        row=0,
        column=1,
        sticky=tk.W
    )
    
    label_image.grid(
        row=0,
        column=0,
        sticky=tk.W
    )
    button.grid(
        row=1,
        column=0,
        sticky=tk.W+tk.E
    )

    msg.grid(
        row=0,
        column=0,
        sticky=tk.W
    )
    msg_scrollBar.grid(
        row=0,
        column=1,
        sticky=tk.N+tk.S
    )

    help_window.bind('<Up>', keyboard_up) 
    help_window.bind('<Down>', keyboard_down) 
    help_window.bind('<Next>', keyboard_pageup) 
    help_window.bind('<Prior>', keyboard_pagedown) 


