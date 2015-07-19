# Codemap

*Look at your code at a distance*

Codemap creates a pixel image. This is the output of codemap when used with the its own code:

![Codemap](https://raw.githubusercontent.com/Muffo/codemap/master/codemap.py.png "Codemap")


### Installation

Codemap is contained in a single Python script that can be easily downloaded and executed in your terminal.


You also need [PyPNG](https://github.com/drj11/pypng) and [Pygments](http://pygments.org)

To install the first you can simply run:

    curl -LO https://raw.github.com/drj11/pypng/master/code/png.py


You can download Pygments from the [Python Package Index](https://pypi.python.org/pypi/Pygments).
For installation of packages from PyPI, we recommend Pip, which works on all major platforms.

Under Linux, most distributions include a package for Pygments, usually called pygments or python-pygments.
You can install it with the package manager as usual.


Finally, you can install optional Pygments styles to be used in the codemaps.
For example, to install Solarized run:

    pip install pygments-style-solarized



### Usage


    usage: codemap.py [-h] [-i INPUT] [-o OUTPUT] [-s STYLE] [-d]

    Transform your source files in codemap images.

    optional arguments:
      -h, --help            show this help message and exit
      -i INPUT, --input INPUT
                            Path of the folder containing the source files.
                            Default: the current folder.
      -o OUTPUT, --output OUTPUT
                            Path of the folder where the images will be stored.
                            Default: a folder called codemap inside the current
                            folder.
      -s STYLE, --style STYLE
                            Style of the output (see Pygments style)
      -d, --debug           Print debug output



**Example:** to generate the image above:

    python -i /path/to/codemap -o /path/to/outputFolder -s solarizeddark

