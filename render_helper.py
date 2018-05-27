"""render_helper.py contains functions that processing
data to the format we want


Available functions:
- load_viewpoint: read viewpoint file
- load_object_list: return a list of object file pathes
- camera_location: return a tuple contains camera location (x, y, z)
    in world coordinates system
- camera_rot_XYZEuler: return a tuple contains cmera ration

author baiyu
"""


import os 
import glob
import math

from collections import namedtuple
from settings import *



def load_viewpoint(viewpoint_file):
    """read viewpoints from a file, can only read one file at once

    Args: 
        viewpoint_file: file path to viewpoint file, read only one file
        for each function call

    Returns: 
        list of viewpoint parameters(contains azimuth,elevation,tilt angles and distance)
    """
    params = []
    Param = namedtuple('Param',['azimuth', 'elevation', 'tilt', 'distance'])
    with open(viewpoint_file) as viewpoints:
        for line in viewpoints.readlines():
            params.append(Param(*line.strip().split()))
    return params

def load_object_list(category=None):
    """
        load object pathes according to the given category

    Args:
        category:a iterable object contains the category which
            we want render

    Returns:
        list of obj file pathes
    """
    
    #type checking
    if not category:
        category = g_shapenet_categlory_pair.keys()
    elif isinstance(category, str):
        category = [category]
    else:
        try:
            iter(category)
        except TypeError:
            print("category should be an iterable object")

    result = []
    #load obj file path
    for cat in category:
        num = g_shapenet_categlory_pair[cat]
        search_path = os.path.join(g_shapenet_path, num, '**','*.obj')
        result.extend(list(glob.iglob(search_path, recursive=True)))
    return result

def camera_location(azimuth, elevation, dist):
    """get camera_location (x, y, z)

    you can write your own version of camera_location function
    to return the camera loation in the blender world coordinates
    system

    Args:
        azimuth: azimuth degree(object centered)
        elevation: elevation degree(object centered)
        dist: distance between camera and object(in meter)
    
    Returens:
        return the camera location in world coordinates in meters
    """

    #convert azimuth, elevation degree to radians
    phi = float(elevation) * math.pi / 360
    theta = float(azimuth) * math.pi / 360
    dist = float(dist)

    x = dist * math.cos(phi) * math.cos(theta)
    y = dist * math.cos(phi) * math.sin(theta)
    z = dist * math.sin(phi)

    return x, y, z

def camera_rot_XYZEuler(azimuth, elevation, tilt):
    """get camera rotaion in XYZEuler

    Args:
        azimuth: azimuth degree(object centerd)
        elevation: elevation degree(object centerd)
        tilt: twist degree(object centerd)
    
    Returns:
        return the camera rotation in Euler angles(XYZ ordered)
    """

    azimuth, elevation, tilt = float(azimuth), float(elevation), float(tilt)
    x, y, z = 90, 0, 90 #set camera at x axis facing towards object

    #twist
    if tilt > 0:
        y = tilt
    else:
        y = 360 - tilt

    #latitude
    x = x - elevation
    #longtitude
    z = z - azimuth

    return x, y, z

    


