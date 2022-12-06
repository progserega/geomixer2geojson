#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#import httplib
import sys
import os
import traceback
import datetime
import time
import json
import path
import math
from decimal import *

conn_local_osm=None
cur_local_osm=None
log=None
config=None
out_path=None
store_debug_layers = False
debug_enabled = False

def get_exception_traceback_descr(e):
  tb_str = traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__)
  result=""
  for msg in tb_str:
    result+=msg
  return result

def y2lat(y):
  return (2 * math.atan(math.exp(y / 6378137)) - math.pi / 2) / (math.pi / 180)

def lat2y(lat):
  return math.log(math.tan(( lat * (math.pi / 180) + math.pi / 2)/2))*6378137

def x2lon(x):
  return x / (math.pi / 180.0) / 6378137.0

def lon2x(lon):
  return lon * 6378137 * (math.pi / 180.0)

def xy2lonlat(x, y):
  return x2lon(x), y2lat(y)

def geomixer2geojson(in_data):
  out_data={"type": "FeatureCollection","features": []}
  for in_item in in_data["values"]:
    key7=in_item[6]
    key8=in_item[7]
    key9=in_item[8]
    in_coord=in_item[10]
    out_item={"type":"Feature","geometry":{"type":None,"coordinates":[]},"properties":{}}
    if in_coord["type"]=="POLYGON":
      out_item["geometry"]["type"]="Polygon"
      for polygon in in_coord["coordinates"]:
        out_polygon=[]
        for coord_par in polygon:
          x=coord_par[0]
          y=coord_par[1]
          lon,lat=xy2lonlat(x,y)
          out_polygon.append([lon,lat])
        out_item["geometry"]["coordinates"].append(out_polygon)
      out_item["properties"]["name"]=key7
      out_item["properties"]["id"]=key8
      out_item["properties"]["description"]=key9
      out_data["features"].append(out_item)
    break
  return out_data
  
# ======================================= main() ===========================

if len(sys.argv) < 2:
  print("need 1 param - input geomixer json")
  sys.exit(1)

#print(xy2lonlat(14825332.25,5322463.15))
#exit(0)

f = open(sys.argv[1],"r")
data = f.read()
in_data=json.loads(data)
out_data=geomixer2geojson(in_data)
print(json.dumps(out_data,indent=4))
