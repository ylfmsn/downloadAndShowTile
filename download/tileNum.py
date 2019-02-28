#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import math
from collections import namedtuple


def deg2num(lat_deg, lon_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
    mytile = namedtuple('mytile', ['xtile', 'ytile', 'zoom'])
    mytile.xtile = xtile
    mytile.ytile = ytile
    mytile.zoom = zoom
    return mytile


def num2deg(xtile, ytile, zoom):
    n = 2.0 ** zoom
    lon_deg = xtile / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
    lat_deg = math.degrees(lat_rad)
    mydegree = namedtuple('mydegree', ['lat', 'lon', 'zoom'])
    mydegree.lat = lat_deg
    mydegree.lon = lon_deg
    mydegree.zoom = zoom
    return mydegree