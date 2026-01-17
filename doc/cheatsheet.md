# Ditheridoo Cheatsheet

## GUI controls

key | function
---|---
Ctrl+q | quit
Ctrl+o | open file
Ctrl+s | save file
Ctrl+p | preferences
Ctrl+h | this help

## mouse control

mouse action | function
---|---
right mouse button | set color
left mouse button | set other color
middle mouse button | scroll image
mouse wheel | zoom in and out

## editing

key | function
---|---
Ctrl+z | undo (single pixel editing only, not for block-commands like cut or paste)
Ctrl+x | cut
Ctrl+c | copy
Ctrl+v | paste
m | set marker
Ctrl+n | normal pencil
Ctrl+b | checkerboard dither pencil
Ctrl+d | x-line dither pencil
Ctrl+y | y-line dither pencil
Ctrl+l | light dither pencil

## editor visuals

key | function
---|---
plus/ minus | zoom in and out
cursor keys | scroll image

## left mouse-button color

key | function
---|---
0-9 a-f | select color
F1 | screen-color-1 of block
F2 | screen-color-2 of block
F3 | colorram of block
F4 | background

## right mouse-button color

key | function
---|---
Shift+ 0-9 a-f | select color
Shift+F1 | screen-color-1 of block
Shift+F2 | screen-color-2 of block
Shift+F3 | colorram of block
Shift+F4 | background

Note: If shift does not work for you, please, try out some other modifier that works with your keyboard layout like Apple-key, fn-key or whatever.

## color to replace (only when in draw mode 'select'):

key | function
---|---
F5 | screen-color-1 of block
F6 | screen-color-2 of block
F7 | colorram of block
F8 | background
Space | no overwriting

## notes: draw-modes

Can be set in settings window.
Behavior if too many colors are used (color-clash):

mode | description
---|---
keep color    | keep color if too many colors are used
replace color | replace color if too many colors are used
select color  | overwrite selected data: screen-color1, screen-color2, colorram or background
dye | do not touch bitmap, only overwrite color
