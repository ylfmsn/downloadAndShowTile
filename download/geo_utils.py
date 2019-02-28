#!/usr/bin/env python3
# -*- coding: UTF-8 -*-


from osgeo import ogr
from collections import namedtuple


def createPoint():
    point = ogr.Geometry(ogr.wkbPoint)
    point.AddPoint(1198054.34, 648493.09)
    print(point.ExportToWkt())


def createLineString():
    line = ogr.Geometry(ogr.wkbLineString)
    line.AddPoint(1116651.439379124, 637392.6969887456)
    line.AddPoint(1188804.0108498496, 652655.7409537067)
    line.AddPoint(1226730.3625203592, 634155.0816022386)
    line.AddPoint(1281307.30760719, 636467.6640211721)
    print(line.ExportToWkt())


def createPolygon():
    ring = ogr.Geometry(ogr.wkbLinearRing)
    ring.AddPoint(1179091.1646903288, 712782.8838459781)
    ring.AddPoint(1161053.0218226474, 667456.2684348812)
    ring.AddPoint(1214704.933941905, 641092.8288590391)
    ring.AddPoint(1228580.428455506, 682719.3123998424)
    ring.AddPoint(1218405.0658121984, 721108.1805541387)
    ring.AddPoint(1179091.1646903288, 712782.8838459781)

    # Create polygon
    poly = ogr.Geometry(ogr.wkbPolygon)
    poly.AddGeometry(ring)

    # print(poly.ExportToWkt())
    return poly


# 根据wkt获取几何图形
def createGeometryFromWKT(filename):
    # str = None
    with open(filename, "r") as f:
        str = f.read()
    # 根据wkt获取面
    polygon = ogr.CreateGeometryFromWkt(str)
    print(polygon)
    return polygon


# 获取wkt的包罗圈
def createEnvelopeFromWKT(filename):
    with open(filename, "r") as f:
        str = f.read()
    geom = ogr.CreateGeometryFromWkt(str)
    env = geom.GetEnvelope()
    print("minX: %d, minY: %d, maxX: %d, maxY: %d" % (env[0], env[2], env[1], env[3]))
    envelop = namedtuple('envelop', ['minX', 'minY', 'maxX', 'maxY'])
    envelop.minX = env[0]
    envelop.minY = env[2]
    envelop.maxX = env[1]
    envelop.maxY = env[3]
    return envelop




def calculateIntesection():
    wkt1 = "POLYGON ((1208064.271243039 624154.6783778917, 1208064.271243039 601260.9785661874, 1231345.9998651114 601260.9785661874, 1231345.9998651114 624154.6783778917, 1208064.271243039 624154.6783778917))"
    wkt2 = "POLYGON ((1199915.6662253144 633079.3410163528, 1199915.6662253144 614453.958118695, 1219317.1067437078 614453.958118695, 1219317.1067437078 633079.3410163528, 1199915.6662253144 633079.3410163528)))"

    poly1 = ogr.CreateGeometryFromWkt(wkt1)
    # poly2 = ogr.CreateGeometryFromWkt(wkt2)
    poly2 = createPolygon()

    intersection = poly1.Intersection(poly2)

    print(intersection.GetPointCount() == 0)
    print(intersection.ExportToWkt())




if __name__ == '__main__':
    filename = 'shannxi.txt'
    # createPoint()
    # print('---------------------')
    # createLineString()
    # print('---------------------')
    # createPolygon()
    # print('---------------------')
    # calculateIntesection()
    createEnvelopeFromWKT(filename)