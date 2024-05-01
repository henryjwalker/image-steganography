# 2024-05-01    -   V6

from PIL import Image, ImageDraw
import random
from time import gmtime, strftime, time
from codecs import ascii_encode
import sys

# Args:
# -m is mode. -m=encode or -m=decode
# -i image path -m=path_to_image
# -t text path -t=path_to_text
# -h help
# 

class iscar:
    def __init__(self, debug):
        self.__debug_mode__ = debug

    def encode(self, image_path, text_path):
        name = strftime("%Y-%m-%d %H-%M-%S", gmtime())

        # Open image file
        try:
            self.__debugger__("Loading image...")
            image = Image.open(image_path)
            self.__debugger__("Image loaded.")
        except:
            self.__errorer__("Image not found.")
        
        # Open text file
        try:
            self.__debugger__("Loading text...")
            with open(text_path, "r+") as f:
                text = f.read()
            self.__debugger__("Text loaded.")
        except:
            self.__errorer__("Text not found.")

        # Convert text to binary
        self.__debugger__("Converting text to binary...")
        bin_list = self.__text_to_binary__(text)
        self.__debugger__("Text converted to binary.")

        # For each pixel, there will be 6 bits of encoded data, 2 bits in each colour.
        # The first 8 bits encoded is the length of the text in bits.

        # To make the length of the list a multiple of 6
        # (otherwise it crashes due to not having enough data to complete a full pixel)
        for i in range(6 - (len(bin_list) % 6)):
            bin_list.append(random.choice(["0","1"]))
        self.__debugger__(f"Total length of text (bits): {len(bin_list)}")

        x,y = 0,0
        image_rgb = image.convert('RGB')
        draw = ImageDraw.Draw(image)
        width, height = image.size
        original_length = len(bin_list)

        self.__debugger__("Encoding text into image...")
        previous_percentage = -1

        time_percentage = 0
        time_getpixel = 0
        time_rgbtobin = 0
        time_modify = 0
        time_draw = 0

        pos = 0
        while pos <= len(bin_list):

            temp = time()

            # Used to output progress when debugging is enabled
            percentage_complete = round( (pos) / original_length * 100)
            if percentage_complete % 10 == 0 and percentage_complete != previous_percentage:
                self.__debugger__(f" --> {percentage_complete}% of text encoded...")
                previous_percentage = percentage_complete

            time_percentage += time()-temp



            temp = time()

            # Read pixel rgb values
            pixel_rgb = image_rgb.getpixel((x,y))

            time_getpixel += time()-temp




            temp = time()

            # Convert rgb into list of binary rgb values
            pixel_rgb_bin = self.__rgb_to_bin__(pixel_rgb)

            time_rgbtobin += time()-temp


            temp = time()

            # Modify rgb to contain message
            for i in range(3):
                pixel_rgb_bin[i] = pixel_rgb_bin[i][:-2] + bin_list[pos:pos+2]
                pos += 2

            time_modify += time()-temp

            
            temp = time()

            # Draw pixel with new rgb values
            rgb = self.__bin_to_rgb__(pixel_rgb_bin)
            #draw.point((x, y), fill=tuple([255,0,0]))
            draw.point((x, y), fill=rgb)

            time_draw += time()-temp


            x += 1
            if x==width:
                x=0
                y+=1

        self.__debugger__(f"Text took up {round((((width*y)+x) / (width*height))*100)}% of the image.")
        self.__debugger__(f"Combined time (in sec.) to excute individual parts:\n     Percentage calcuation: {time_percentage}\n     Get pixel value: {time_getpixel}\n     RGB to binary: {time_rgbtobin}\n     Modify pixel: {time_modify}\n     Draw pixel: {time_draw}")
        self.__debugger__("Encoding complete.")
        new_filename = "Encoded - "+name

        self.__debugger__("Saving encoded image...")
        image.save(new_filename+".png")
        self.__debugger__("Encoded image saved.")
        print(f"Image saved as '{new_filename}.png'")

    def decode(self, image_path):

        # Open image file
        try:
            self.__debugger__("Loading image...")
            image = Image.open(image_path)
            width, height = image.size
            self.__debugger__("Image loaded.")
        except:
            self.__errorer__("Image not found.")

        image_rgb = image.convert('RGB')
        x,y = 0,0

        self.__debugger__("Extracting length of text...")
        try:
            length_bits = []
            while not len(length_bits) >= 36:
                #print(f"Extracting:    x:{x}  y:{y}")
                pixel_rgb = image_rgb.getpixel((x,y))
                length_bits += self.__read_rgb__(pixel_rgb)
                x += 1
                if x==width:
                    x=0
                    y+=1
            length = int("".join(length_bits), 2)
            self.__debugger__("Length of text extracted.")
        except:
            self.__errorer__("Couldn't find text terminator.")

        x = 6
        message_bits = []
        self.__debugger__("Extracting data...")

        previous_percentage = -1
        while not len(message_bits) >= length:

            percentage_complete = round( len(message_bits) / length * 100)
            if percentage_complete % 10 == 0 and percentage_complete != previous_percentage:
                self.__debugger__(f" --> {percentage_complete}% of data extracted...")
                previous_percentage = percentage_complete
        
            pixel_rgb = image_rgb.getpixel((x,y))
            message_bits += self.__read_rgb__(pixel_rgb)
            x += 1
            if x==width:
                x=0
                y+=1

        self.__debugger__("Data extracted.")
        message_bits = message_bits[:length]

        self.__debugger__("Converting data into bytes...")
        message_bytes = self.__split_list__(message_bits)
        self.__debugger__("Data converted into bytes.")

        message = ""

        self.__debugger__("Converting bytes into text...")
        for byte in message_bytes:
            message += chr(int(byte, 2))
        self.__debugger__("Bytes converted into text.")


        self.__debugger__("Saving text file...")
        with open(image_path+".txt", "w+", encoding="utf-8") as f:
            f.write(message)

        self.__debugger__("Text file saved.")
        print(f"Decoded text saved within: '{image_path}.txt'")

    def __text_to_binary__(self, text):
        bintext = ascii_encode(text)

        binlist = ""
        for i in range(bintext[1]):
            binlist += str(format(bintext[0][i], "08b"))
        binlist = list(binlist)
        binlist = list(format(len(binlist), "036b")) + binlist
        return list(binlist)
    
    def __rgb_to_bin__(self, rgb):
        new = []
        for i in range(3):
            new.append(list(str(format(rgb[i], "08b"))))
        return new

    def __bin_to_rgb__(self, bin):
        rgb = []
        for i in range(3):
            bin[i] = "".join(bin[i])
            rgb.append(int(bin[i], 2))
        return tuple(rgb)

    def __read_rgb__(self, rgb):          # Takes in rgb tuple of ints, returns a list of 6 indivual message bits
        values = []
        rgb_bin = self.__rgb_to_bin__(rgb)
        for i in range(3):
            values.append("".join(rgb_bin[i][-2:]))
        values = list("".join(values))
        return values

    def __split_list__(self, lis):        # Splits a list of individual str bits into a list of str bytes
        """new_list = []
        while not len(lis) == 0:
            current_str = ""
            for i in range(8):
                current_str += lis[0]
                del lis[0]
            new_list.append(current_str)

        return new_list"""
    
        return [''.join(lis[i:i+8]) for i in range(0, len(lis), 8)]

    def __debugger__(self, message):
        if self.__debug_mode__:
            print(f"[DEBUG] {strftime("%Y-%m-%d %H-%M-%S", gmtime())} --> {message}")

    def __errorer__(self, message):
        print(f"[ERROR] {strftime("%Y-%m-%d %H-%M-%S", gmtime())} --> {message}")
        exit()

def help():
    print(" ----------= ISCAR =----------")
    print("")
    print("Usage: ")
    print("     iscar.py [options]")
    print("")
    print("Options: ")
    print("     -m      Sets the mode [encode/decode]")
    print("     -i      Sets path to the image file. Required for encoding and decoding.")
    print("     -t      Sets path to the text file. Required for encoding.")
    print("     -d      Enables debugging.")
    print("     -h      Displays this help information.")
    print("")
    print("E.g. to encode message.txt into image.png with debugging enabled: ")
    print("     iscar.py -m=encode -i=image.png -t=message.txt -d")
    print("")
    print("E.g. to decode image.png with debugging enabled: ")
    print("     iscar.py -m=decode -i=image.png -d")

settings = {
    "mode": "",
    "image": "",
    "text": "",
    "debug": False
}

args = sys.argv

for arg in args:
    if arg.split("=")[0] == "-m":
        settings["mode"] = arg.split("=")[1]
    elif arg.split("=")[0] == "-i":
        settings["image"] = arg.split("=")[1]
    elif arg.split("=")[0] == "-t":
        settings["text"] = arg.split("=")[1]
    elif arg == "-d":
        settings["debug"] = True
    elif arg == "-h":
        help()


if settings["mode"] == "encode":
    ISCAR = iscar(settings["debug"])
    ISCAR.encode(settings["image"], settings["text"])

elif settings["mode"] == "decode":
    ISCAR = iscar(settings["debug"])
    ISCAR.decode(settings["image"])

else:
    print("[ERROR] Invalid mode selected.")
    exit()
