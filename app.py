#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from collections import namedtuple, Counter
from flask import Flask, Response, render_template, request


Tile = namedtuple('Tile', ['x', 'y', 'z'])
tile_counter = Counter()

app = Flask(__name__)

@app.route("/tile")
def tile():
    x = request.args['x']
    y = request.args['y']
    z = request.args['z']
    t = Tile(x, y, z)
    with open('./tilefile/%s/%s/%s.png' % (z, x, y), 'rb') as f:
        image = f.read()
    tile_counter[t] += 1
    return Response(image, mimetype='image/jpeg')


@app.route('/', methods=['GET'])
def map():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='localhost', debug=True, threaded=True)