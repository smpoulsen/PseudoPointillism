import pandas as pd
from PIL import Image

class PointillismImage(object):
    def __init__(self, f_name):
        self.f_name = f_name
        self.im = self.open_image()
        self.pixel_matrix = self.set_pixel_data()

    def open_image(self):
        return Image.open(self.f_name)

    def set_pixel_data(self):
        pix = [[self.im.getpixel((x,y)) for x in range(self.im.size[0])] \
            for y in range(self.im.size[1])]
        pix_frame = pd.DataFrame(pix)
        return pix_frame

    def get_pixel_json(self, height):
        skip = round(self.im.size[1]/height)
        colors = [{"x": x, "y": y, "color": "rgba({0}, {1}, {2}, 0.75)".\
                format(self.pixel_matrix[x][y][0], self.pixel_matrix[x][y][1], \
                self.pixel_matrix[x][y][2])} for y in self.pixel_matrix.index \
                for x in self.pixel_matrix.columns if y % skip == 0 \
                and x % skip == 0]
        return colors

    def get_aspect(self):
        return self.im.size[0] / float(self.im.size[1])

