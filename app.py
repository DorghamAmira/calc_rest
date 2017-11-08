from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from PIL import Image
import numpy as np



from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/faktum', methods=['POST'])
def faktum():
    req = request.data['image']
    path = os.path.join(os.getcwd(), 'images/test_calc.png')
    calc = Image.open(path)
    img_capture = req
    print(type(req))
    cropped_img=crop(calc,img_capture)
    grey_capture = cropped_img.convert('1')
    pixel_list = extract(calc)
    message=compare(grey_capture,pixel_list)
    return message
    
def crop(calc,image):
    width_calc, height_calc = calc.size
    width_cap, height_cap = image.size

    left_margin = float(width_cap - width_calc) / 2
    top_margin = float(height_cap - height_calc) / 2

    area = (int(left_margin), int(top_margin), int(left_margin + width_calc), int(top_margin + height_calc))
    cropped_img = image.crop(area)
    return cropped_img
    
    
def compare(image,list):
    index = 0

    for item in list:
        position = item[0]
        if image.getpixel((position[0],position[1]))==item[1][0]:
            index+=1
    if index == len(list):
        return ("FAKTUM")
    else:
        return ("NON FAKTUM")


def extract(image_calc):
    list=[]
    for x in range(0,600):
        for y in range(0,360):
            if (image_calc.getpixel((x,y)) == (0,0,0,0)) or (image_calc.getpixel((x,y))==(255,255,255,255)):
                pixel = image_calc.getpixel((x,y))
                item = ((x,y),pixel)
                list.append(item)
    return list


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print ("Starting app on port %d" % port)

app.run(debug=True, port=port, host='0.0.0.0')
