from flask import Flask, request, render_template, jsonify
from random import randrange
import os

import pointillism_image as pointillism

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def main():
    """
    Entry point. Selects a random picture from './images', and returns the
    pixel and aspect information to the application on loading.

    """
    image_data = image_handler()
    return render_template("layout.html", aspect=image_data[0], 
        dataset=image_data[1], background=image_data[2])

@app.route("/new_picture", methods=["GET", "POST"])
def generate_picture_data():
    """
    Called by click handler in javascript to draw a new image.
    Returns pixel and aspect data as JSON.

    """
    image_data = image_handler()
    return jsonify({"aspect": image_data[0], "dataset": image_data[1], 
        "background": image_data[2]})

def image_handler():
    """
    Selects random picture, opens it and returns pixel and aspect 
    data.
    """
    pixel_height = 70 
    picture = select_picture("images")
    image = pointillism.PointillismImage(picture)
    aspect = image.get_aspect()
    dataset = image.get_pixel_json(pixel_height)
    avg_color = image.get_average_color()
    return (aspect, dataset, avg_color)

def select_picture(pic_dir):
    """
    Selects random image from images directory.

    """
    pics = os.listdir(pic_dir)
    return "{0}/{1}".format(pic_dir, pics[randrange(0, len(pics))])

if __name__ == "__main__":
    app.debug = True
    app.run(port=8080)
