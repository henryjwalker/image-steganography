import sys
from PIL import Image

args = sys.argv

def help():
    print(" ----------= ISCAR Tools =----------")
    print("")
    print("Usage: ")
    print("     tools.py [options]")
    print("")
    print("Options: ")
    print("     -i      Sets path to the image file to analyse.")
    print("     -t      Sets path to the text file to analyse..")
    print("     -h      Displays this help information.")
    print("")

settings = {
    "image": "",
    "text": "",
}

args = sys.argv

for arg in args:
    if arg.split("=")[0] == "-i":
        settings["image"] = arg.split("=")[1]
    elif arg.split("=")[0] == "-t":
        settings["text"] = arg.split("=")[1]
    elif arg == "-h":
        help()

if settings["image"] != "":
    image = Image.open(settings["image"])
    width, height = image.size
    print(f"You are able to store {width*height*3*2} bits of data within this image.")

if settings["text"] != "":
    with open(settings["text"], "r", encoding="utf-8") as f:
        temp = f.read()
    print(f"This text requires {len(temp)*8} bits.")
    