# ISCAR (Image Steganography Creator and Reader)
Coded using Python, this program can 'hide' text within images and read text 'hidden' within images. I use hide in quotations because from a quick look, it is impossible/very hard to know there is hidden text within the image however, there are methods to detect the use of steganography.
## Usage
### Encoding text within an image
To encode text within an image, run the following command from the directory where you have the program:
```
python main.py -m=encode -i=[path_to_image] -t=[path_to_text]
```
This will encode the text within `[path_to_text]` text file into the `[path_to_image]` image file.

To decode text from an image, use the following command:
```
python main.py  -m=decode -i=[path_to_image]
```
This will decode the text from within the `[path_to_image]` image file.
#### Tips
 - Use `" "` around file paths.
 - Use `-d` to view debugging messages.
 - Use `-h` to view the help page.
 - Text files should ideally be formatted using `utf-8`.
 - Image files should ideally be in `png` formats.
