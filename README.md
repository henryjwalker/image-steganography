# ISCAR (Image Steganography Creator and Reader)
Coded using Python, this program can 'hide' text within images and read text 'hidden' within images. I use hide in quotations because from a quick look, it is impossible/very hard to know there is hidden text within the image however, there are methods to detect the use of steganography.
## Installation
To install this program download the scripts.
You will also need Python 3.x or above, as well as the following Python modules:
 - PIL (Pillow)
## Usage
### Encoding text within an image
To encode text within an image, run the following command from the directory where you have the program:
```
python main.py -m=encode -i=[path_to_image] -t=[path_to_text]
```
This will encode the text within `[path_to_text]` text file into the `[path_to_image]` image file.
### Decodeing text from an image
To decode text from an image, use the following command:
```
python main.py  -m=decode -i=[path_to_image]
```
This will decode the text from within the `[path_to_image]` image file.
### Analysing an image or text file
Using the `tools.py` program, you can see how much data an image can store, and how much data a text file requires.
To analyse a text file and an image file at the same time use this command:
```
python tools.py -i=[path_to_image] -t=[path_to_text]
```
You can analyse a single file at a time, or you can analyse an image and a text file together.
#### Tips
 - Use `" "` around file paths.
 - Use `-d` to view debugging messages.
 - Use `-h` to view the help page.
 - Text files should ideally be formatted using `utf-8`.
 - Image files should ideally be in `png` formats.
