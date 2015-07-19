import argparse
from collections import deque
import json
import png
from pygments.formatter import Formatter


"""
Convert the color from hex format to tuple:
'#RRGGBB' --> (red, green, blue)
"""
def hex_color_to_tuple(color):

    if color[0] == "#":
        color = color[1:]

    red = int(color[:2], 16)
    green = int(color[2:4], 16)
    blue = int(color[4:], 16)

    return red, green, blue


class MinimapFormatter(Formatter):

    def __init__(self, **options):
        Formatter.__init__(self, **options)

        # dictionary that contains the color for each token type
        self.styles = {}

        self.background_color = hex_color_to_tuple(self.style.background_color)

        # we iterate over the `_styles` attribute of a style item
        # that contains the parsed style values.
        for token, style in self.style:

            # set the color for the current style converting from hex format
            if style['color']:
                self.styles[token] = hex_color_to_tuple(style['color'])
            else:
                self.styles[token] = (0, 0, 0)

    def format(self, tokensource, outfile):
        code_map = deque()
        row = deque()

        for ttype, value in tokensource:

            # if the token type doesn't exist in the stylemap
            while ttype not in self.styles:
                ttype = ttype.parent

            # if this is a new line I just add new row
            if value == "\n":
                code_map.append(row)
                row = deque()
                continue

            # handle multi-lines comments
            if "\n" in value:
                text_rows = value.split("\n")

                for text in text_rows[:-1]:
                    pixels = [self.styles[ttype] if c != " " else self.background_color for c in text]
                    row.extend(pixels)
                    code_map.append(row)
                    row = deque()

                value = text_rows[-1]

            pixels = [self.styles[ttype] if c != " " else self.background_color for c in value]
            row.extend(pixels)

            # print "-> %s : '%s' (%d) - Color: %s" % (ttype, value, len(value), self.styles[ttype])

        # size of the image
        height = len(code_map)
        width = max([len(row) for row in code_map])

        if width > 0 and height > 0:
            print "Size: %d x %d" % (width, height)
        else:
            print "Image is empty"
            return

        # create the image:
        # - code lines are 2 pixels wide
        # - empty line is 1 pixel wide
        img = deque()
        empty_row = self.background_color * width

        for row in code_map:
            row_len = len(row)
            flat_row = deque([item for sublist in row for item in sublist])
            flat_row.extend(self.background_color * (width - row_len))
            img.append(flat_row)
            img.append(flat_row)
            img.append(empty_row)

        # write the image in png format
        w = png.Writer(width, 3 * height)
        w.write(outfile, img)


from pygments import highlight
from pygments.lexers import get_lexer_for_filename
from pygments.util import ClassNotFound


import os

def list_files(dir_path):
    result = []
    for root, dirs, files in os.walk(dir_path):
        files = [f for f in files if not f[0] == '.']
        dirs[:] = [d for d in dirs if not d[0] == '.']

        for f in files:
            result.append(root + "/" + f)

    return result


def run(argv):

    parser = argparse.ArgumentParser(add_help=True)
    
    parser.add_argument("-i", "--input", default=".",
                        help="Path of the folder containing the source files.\nDefault: the current folder.")
    
    parser.add_argument("-o", "--output", default="./codemap",
                        help="Path of the folder where the images will be stored.\n" +
                             "Default: a folder called codemap inside the current folder.")
    
    parser.add_argument("-s", "--style", default="",
                        help="Style of the output (see Pygments style)")

    parser.add_argument("-d", "--debug", action="store_true",
                        help="Print debug output")
    
    parser.description = """
        Transform your source files in codemap images.
        """
    
    conf = parser.parse_args(argv)
    print conf

    images = []
    
    for file_name in list_files(conf.input):

        if conf.debug:
            print "Processing file: " + file_name, " ... ",
    
        with open(file_name, 'r') as code_file:
            code = code_file.read()
    
        try:
            lexer = get_lexer_for_filename(file_name)
    
            image_file = os.path.join(conf.output, os.path.relpath(file_name, conf.input) + ".png")
    
            images.append(image_file)
    
            image_dir = os.path.dirname(image_file)
            if not os.path.exists(image_dir):
                os.makedirs(image_dir)
    
            with open(image_file, 'wb') as outfile:
                highlight(code, lexer, MinimapFormatter(style=conf.style), outfile)
    
        except ClassNotFound:
            print "Cannot find lexer"
            continue

    with open(os.path.join(conf.output, 'images.json'), 'w') as outfile:
        json.dump(images, outfile)


if __name__ == "__main__":
    import sys
    run(sys.argv[1:])

