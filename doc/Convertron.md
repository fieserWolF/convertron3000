# Convertron3000

Convertron3000 is a graphics converter for Commodore 64 computers.
It runs on Linux, MacOS, Windows and other systems supported by Python. 

![screenshot](./screenshot.png)


# Why Convertron3000?

reason | description
---|---
open source | easy to modify and to improve, any useful contribution is highly welcome
portable | available on Linux, MacOS, Windows and any other system supported by Python3
instant preview | just fiddle around with the sliders and see the result before converting
deal with color clashes | visualize color clashes instantly or read out their position from an optional json-file


# Author

* fieserWolF/Abyss-Connection - *initial work* - [https://github.com/fieserWolF](https://github.com/fieserWolF) [https://csdb.dk/scener/?id=3623](https://csdb.dk/scener/?id=3623)


# Acknowledgments

* thanks to [Green/ATW](http://csdb.dk/scener/?id=20695) for spontaneously naming Convertron3000 :)
* thanks to people on [csdb.dk](http://csdb.dk/release/?id=155606) for commenting and giving ideas how to improve
* thanks to Henrik Blidh for his hitherdither library [https://github.com/hbldh/hitherdither](https://github.com/hbldh/hitherdither) which I use
# Using Convertron 3000


## Usage

Using Convertron3000 is pretty straight-forward:

* Open some image.
* Adjust the sliders or apply an effect.
* Convert to koala or hires format.
* optional: Check position of color-clashes.
* Save the resulting image.


## shortcuts

key | function
---|---
F1 | help
Alt-o | open image
Alt-s | save image (koala or hires format)
Alt-c | convert image
Alt-p | open settings
Alt-v | save settings
Alt-q | quit


## Dithering

As of now, Convertron3000 offers various dithering methods.
As the PIL-library only implements "floyd-steinberg"-dithering, all other dithering methods were taken from the hitherdither library.

reason | description
---|---
floyd-steinberg dithering | speedy performance from the PIL-library
bayer-ordered dithering | the speedy standard, my favourite for C64 pictures
line dithering | a modified bayer-ordered dithering method, sometimes looks better than normal ordered dithering
dot dithering | not my favourite, but might give nice results on some pictures
yliluomas1 dithering | Warning: Painfully slow - use with care! The results are stunningly good sometimes, though.


Please, take note that all dithering implementations except "floyd-steinberg"-dithering are quite slow when using the "Brightness palette"-mode, which is described below.




## Brightness palette

Sometimes converted images look better when applying a palette based on brightness values.

* Select "brightness palette" mode.
* Choose one of the presets ("purple", "brown" etc.).

You can also create your own palette like this:

* Edit the .json file: In the .json file you specify the size of your palette and the C64-colors like in one of the examples provided.
* Open your .json file. You find this option in the drop-down menu under "open custom gradient".
* Choose "custom" as your brightness palette.




## File Formats

The multicolor bitmap is stored in the widely-spread KoalaPainter (.koa) format:

* 2 bytes load address
* 8000 bytes raw bitmap data
* 1000 bytes raw "Video Matrix" (screen) data
* 1000 bytes raw "Color RAM" data
* 1 byte background data

The hires bitmap is stored in the widely-spread Advanced Art Studio (.art) format:

* 2 bytes load address
* 8000 bytes raw bitmap data
* 1000 bytes raw "Video Matrix" (screen) data


# Commandline options

	CONVERTRON3000 v1.34 [build 251229-205604] *** by fieserWolF
	usage: convertron.py [-h] [-i INPUT_IMAGE] [-g FILE_GRADIENT] [-s FILE_SETTINGS] [-d]

	This program reads an image-file, lets the user adjust settings and converts it to a C64 koala or hires image.

	options:
	  -h, --help            show this help message and exit
	  -i, --image INPUT_IMAGE
							image file)
	  -g, --gradient FILE_GRADIENT
							filename of custom gradient file (JSON) to be loaded
	  -s, --settings FILE_SETTINGS
							filename of settings file (JSON) to be loaded
	  -d, --debug           show color-clashes on consule

	Example: ./convertron.py -i image.png -g 8color_gradient-brown.json -s settings.json -d
# Getting Started

Convertron3000 comes in two flavors:

- Python3 script if you have python3 installed on your system (preferred method)
- executable for Linux and Windows (see [releases](https://github.com/fieserWolF/convertron3000/releases))

## Run the executable

Just download your zip-bundle at [releases](https://github.com/fieserWolF/convertron3000/releases), extract it to a folder of your choice and enjoy.

### Note for Windows users

If some antivirus scanner puts Convertron3000 into quarantine because it suspects a trojan or virus, simply put it out there again.
It isn`t harmful, I used PyInstaller to bundle the standalone executable for you.
Unfortunately, the PyInstaller bootloader triggers a false alarm on some systems.
I even tried my best and re-compiled the PyInstaller bootloader so that this should not happen anymore. Keep your fingers crossed ;)

### Note for MacOS users

In [releases](https://github.com/fieserWolF/convertron3000/releases) you also find older versions of Convertron 3000 compiled as standalone executables.
You may use this, but your system might complain that the code is not signed by a certificated developer. Well, I am not, so I signed the program on my own. 
```
"Convertron3000" can`t be opened because it is from an unidentified developer.
```
You need to right-click or Control-click the app and select “Open”.



## Run the Python3 script directly

### Prerequisites

At least this is needed to run the script directly:

- python 3
- python tkinter module
- python "The Python Imaging Library" (PIL)
- python "argparse" library
- python "hitherdither" library


Normally, you would use pip like this:
```
pip3 install pillow argparse git+https://www.github.com/hbldh/hitherdither
```
You might need to install git (apt install git) first.


On my Debian GNU/Linux machine I use apt-get to install everything needed:
```
apt update
apt install python3 python3-tk python3-pil python3-pil.imagetk
pip3 install git+https://www.github.com/hbldh/hitherdither
```


### Download Convertron3000

* Go to [https://github.com/fieserWolF/convertron3000](https://github.com/fieserWolF/convertron3000).
* Click on the green "Code" button and "Download ZIP".
* Extract the downloaded ZIP-file to any folder.



# Changelog

## Future plans

- custom brightness palette editor

Any help and support in any form is highly appreciated.

If you have a feature request, a bug report or if you want to offer help, please, contact me:


[http://csdb.dk/scener/?id=3623](http://csdb.dk/scener/?id=3623)
or
[wolf@abyss-connection.de](wolf@abyss-connection.de)



## Changes in 1.35

- resizable image windows
- various bug fixes


## Changes in 1.34 (on Dream210 Party 2025)

- all settings can now be written to a file and restored to a file (json format)
- rearranged the main layout to simplify the workflow (all controls are closer by now)
- rewritten the whole code, split up into parts
- rearranged the documentation
- responsive GUI
- bug fix: proper file-not-found handling when opening images
- bug fix: fixed crash when not finding reasonable color replacement in hires mode (thanks slesinger for the bug report)


## Changes in 1.33

- added: color-clashes can be saved as image and as json
- bug fixes


## Changes in 1.32

- added proper commandline argument parsing (try "convertron.py --help")
- added json output of color clashes (can be read from other tools to work on color clashes)
- fixed: removed leftover saving debug image "/tmp/1.png"


## Changes in 1.31

- fixed: wrong hires image dimensions when using line dithering


## Changes in 1.3 (on X2024)

- fixed: proper scaling, better conversion
- show position of color clashes in GUI and on console


## Changes in 1.2

- proper dithering support: bayer-ordered, line dither and some others
- GUI improvements
- moved standalone executables to [releases](https://github.com/fieserWolF/convertron3000/releases)


## Changes in 1.1

- transfered whole code to Python3
- great speed improvement, converts much faster now
- new feature: specify image on the command-line, e.g. "convertron.py picture.jpg"
- standalone executables for 64bit-systems: Linux, Darwin (MacOS) and Windows
- GUI design adjusted for MacOS/Darwin
- numpy library not used any more
- documentation
- custom brightness palette now uses .json format


## Changes in 1.01

- added licenses
- added to github with proper README.md


## Changes in 1.0

- hires mode
- colodore palette
- button: reset color modifiers to default
- start address now in hex
- custom brightness palette (config file)


## Changes in 0.1

- initial release


# License

_Convertron3000 is a graphics converter for Commodore 64 computers._

_Copyright (C) 2026 fieserWolF / Abyss-Connection_

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.
If not, see [http://www.gnu.org/licenses/](http://www.gnu.org/licenses/).

See the [LICENSE](LICENSE) file for details.

For further questions, please contact me at
[http://csdb.dk/scener/?id=3623](http://csdb.dk/scener/?id=3623)
or
[wolf@abyss-connection.de](wolf@abyss-connection.de)

For Python3, The Python Imaging Library (PIL), Tcl/Tk and other used source licenses see file [LICENSE_OTHERS](LICENSE_OTHERS).


