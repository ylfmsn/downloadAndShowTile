#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from download.tileNum import *
from download.geo_utils import *
import asyncio
import functools
from urllib import request
import os
import random

tdturl = [
        'http://t0.tianditu.com/DataServer?',
        'http://t1.tianditu.com/DataServer?',
        'http://t2.tianditu.com/DataServer?',
        'http://t3.tianditu.com/DataServer?',
        'http://t4.tianditu.com/DataServer?',
        'http://t5.tianditu.com/DataServer?',
        'http://t6.tianditu.com/DataServer?',
        'http://t7.tianditu.com/DataServer?',
    ]

def create_image_path(rootpath, level, x):
    path = './%s/%d/%d'%(rootpath, level, x)
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def download_image(start_zoom, stop_zoom, lat_start, lat_stop, lon_start, lon_stop):
    basetileurl = 'https://elevation-tiles-prod.s3.amazonaws.com/terrarium'
    rootpath = './tilefile'
    imagelists = []
    geom = createGeometryFromWKT('./shannxi.txt')
    for zoom in range(start_zoom, stop_zoom):

        print(imagelists)
        imagelists.clear()
        print(imagelists)

        start_mytile = deg2num(lat_deg=lat_stop, lon_deg=lon_start, zoom=zoom)
        stop_mystile = deg2num(lat_deg=lat_start, lon_deg=lon_stop, zoom=zoom)

        start_x, stop_x = start_mytile.xtile, stop_mystile.xtile
        start_y, stop_y = start_mytile.ytile, stop_mystile.ytile

        # print("x range: ", start_x, stop_x)
        # print("y range: ", start_y, stop_y)

        for x in range(start_x, stop_x):

            for y in range(start_y, stop_y):
                mydegree = num2deg(xtile=x, ytile=y, zoom=zoom)
                # print(mydegree.lat, mydegree.lon)
                point = ogr.Geometry(ogr.wkbPoint)
                point.AddPoint(mydegree.lon, mydegree.lat)
                # print(point)
                intersection = point.Intersection(geom)
                if intersection.GetPointCount() > 0:
                    create_image_path(rootpath, zoom, x)
                    # print(point)
                    savepath = './%s/%d/%d/%d.png' % (rootpath, zoom, x, y)
                    # tileurl = basetileurl + '/%d/%d/%d' % (zoom, x, y) + '.png'
                    # tileurl = 'http://wprd03.is.autonavi.com/appmaptile?style=7&x=%d&y=%d&z=%d' % (x, y, zoom)
                    tileurl = random.choice(tdturl) + "T=img_w&x=" + str(x) + "&y=" + str(y) + "&l=" + str(zoom) + "&tk=359e09124b4b02aeaf02df88f7da6689"
                    imagelists.append((tileurl, savepath))

        tasks = [asyncio.ensure_future(save_image_v2(url)) for url in imagelists]
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(tasks))

    loop.close()


async def save_image_v2(url):
    tileurl, savepath = url[0], url[1]
    loop = asyncio.get_event_loop()
    try:
        response = await loop.run_in_executor(None, functools.partial(request.urlretrieve, url = tileurl, filename = savepath))
        print('---- PID:', os.getpid(), tileurl)
    except Exception as e:
        print('------------', e)


if __name__ == '__main__':
    filename = './shannxi.txt'
    envelop = createEnvelopeFromWKT(filename)
    zoom_start, zoom_stop = 8, 17
    lat_start, lon_start = 34.749336, 107.633933  # 左上
    lat_stop, lon_stop = 33.699932, 109.828903  # 右下
    download_image(start_zoom=zoom_start, stop_zoom=zoom_stop, lat_start=envelop.minY, lat_stop=envelop.maxY, lon_start=envelop.minX, lon_stop=envelop.maxX)

