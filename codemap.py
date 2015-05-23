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
        code_map = []
        row = []

        for ttype, value in tokensource:

            # if the token type doesn't exist in the stylemap
            while ttype not in self.styles:
                ttype = ttype.parent

            # if this is a new line I just add new row
            if value == "\n":
                code_map.append(row)
                row = []
                continue

            # handle multi-lines comments
            if "\n" in value:
                text_rows = value.split("\n")

                for text in text_rows[:-1]:
                    pixels = [self.styles[ttype] if c != " " else self.background_color for c in text]
                    row.extend(pixels)

                    code_map.append(row)
                    row = []

                value = text_rows[-1]

            pixels = [self.styles[ttype] if c != " " else self.background_color for c in value]
            row.extend(pixels)

            # print "-> %s : '%s' (%d) - Color: %s" % (ttype, value, len(value), self.styles[ttype])

        # size of the image
        height = len(code_map)
        width = max([len(row) for row in code_map])

        print "Size: %d x %d" % (width, height)

        # create the image:
        # - code lines are 2 pixels wide
        # - empty line is 1 pixel wide
        img = []
        empty_row = self.background_color * width

        for row in code_map:
            row_len = len(row)
            flat_row = [item for sublist in row for item in sublist]
            flat_row.extend(self.background_color * (width - row_len))
            img.append(flat_row)
            img.append(flat_row)
            img.append(empty_row)

        # write the image in png format
        w = png.Writer(width, 3 * height)
        w.write(outfile, img)




from pygments import highlight
from pygments.lexers import get_lexer_for_filename

file_name = "png.py"

with open(file_name, 'r') as code_file:
    code = code_file.read()


lexer = get_lexer_for_filename(file_name)


outfile = open('test.png', 'wb')
highlight(code, lexer, MinimapFormatter(style='solarizeddark'), outfile)
outfile.close()