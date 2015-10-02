#! /usr/bin/env python3

from PIL import Image
from PIL import ImageChops
from PIL import ImageOps
from PIL import ImageFilter
# import numpy
import time
import subprocess


interval = 5
quality = 25


def run_monitor():
    import http.server
    import socketserver

    PORT = 8000
    Handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", PORT), Handler)

    print("serving at port", PORT)
    httpd.serve_forever()


def check():
    subprocess.call("raspistill --quality {0} -o tmp.png".format(quality), shell=True)

    new_contents = Image.open("tmp.png")
    old_contents = Image.open("current.png")
    # new_gray = ImageOps.grayscale(new_contents)
    # old_gray = ImageOps.grayscale(old_contents)
    # new_edge = new_contents.filter(ImageFilter.FIND_EDGES)
    # old_edge = old_contents.filter(ImageFilter.FIND_EDGES)

    # new_edge.save("processing/new_edge.jpg", 'JPEG')
    # old_edge.save("processing/old_edge.jpg", 'JPEG')

    diff_img = ImageChops.difference(new_contents, old_contents)
    diff_img.save("processing/diff.jpg", 'JPEG')
    diff_img_gray = ImageOps.grayscale(diff_img)
    diff_img_gray.save("processing/diff_gray.jpg", 'JPEG')

    diff = sum(diff_img_gray.getdata())

    # subprocess.call("raspistill -o current.png", shell=True)
    subprocess.call("mv -f tmp.png current.png", shell=True)

    return diff > 10583188 * 2


if __name__ == '__main__':
    # run_monitor()

    subprocess.call("raspistill --quality {0} -o current.png".format(quality), shell=True)

    while True:
        time.sleep(interval)
        if check():
            subprocess.call("cp current.png mails/{0}.png".format(str(time.time())), shell=True)
            print("new mail!", time.time())
