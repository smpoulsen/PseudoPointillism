import pandas as pd
from PIL import Image
from math import trunc

class PointillismImage(object):
    """
    Opens an image and provides accessors for aspect ratio and
    JSON formatted pixel data.

    """
    def __init__(self, f_name):
        """
        Initializes with provided filename.

        """
        self.f_name = f_name
        self.im = self.open_image()
        self.pixel_matrix = self.set_pixel_data()

    def open_image(self):
        """
        Opens image and sets the Image object to self.im

        """
        return Image.open(self.f_name)

    def set_pixel_data(self):
        """
        Gets pixel colors (R,G,B) for all (X, Y)'s. Sets self.pixel_matrix
        with the resulting Data Frame.

        """
        pix_frame = pd.DataFrame([[self.im.getpixel((x, y)) for x in range(self.im.size[0])] \
            for y in range(self.im.size[1])])
        #pix_frame = pd.DataFrame(pix)
        return pix_frame

    def get_pixel_json(self, height):
        """
        Uses height and sets skip to determine which pixels to take,
        then formats the the points needed to plot the image in a list
        of dicts that will be parseable from D3.

        """
        skip = round(self.im.size[1]/height)
        colors = [{"x": x, "y": y, "color": "rgba({0}, {1}, {2}, 0.75)".\
                format(self.pixel_matrix[x][y][0], self.pixel_matrix[x][y][1], \
                self.pixel_matrix[x][y][2])} for y in self.pixel_matrix.index \
                for x in self.pixel_matrix.columns if y % skip == 0 \
                and x % skip == 0]
        return colors

    def get_average_color(self):
        """
        Gets the average color of the image to set as the page background.

        """
        pix = [self.im.getpixel((x, y)) for x in range(self.im.size[0]) \
            for y in range(self.im.size[1])]
        avg_hex = "".join([y[2:] for y in [hex(trunc(x)) \
            for x in pd.DataFrame(pix).mean()]])  
        return "#" + avg_hex  
    
    def get_aspect(self):
        """
        Floating point aspect ratio of image.
        """
        return self.im.size[0] / float(self.im.size[1])
