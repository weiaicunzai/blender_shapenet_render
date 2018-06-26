"""render_helper.py contains functions that processing
data to the format we want


Available functions:
- load_viewpoint: read viewpoint file
- load_object_lists: return a generator of object file pathes
- camera_location: return a tuple contains camera location (x, y, z)
    in world coordinates system
- camera_rot_XYZEuler: return a tuple contains cmera ration

author baiyu
"""


import os 
import glob
import math
import random

from collections import namedtuple
from settings import *

# need to write outside the function, otherwise pickle can find
# where Param were defined
Param = namedtuple('Param',['azimuth', 'elevation', 'tilt', 'distance'])
def load_viewpoint(viewpoint_file):
    """read viewpoints from a file, can only read one file at once

    Args: 
        viewpoint_file: file path to viewpoint file, read only one file
        for each function call

    Returns: 
        generator of viewpoint parameters(contains azimuth,elevation,tilt angles and distance)
    """
    with open(viewpoint_file) as viewpoints:
        for line in viewpoints.readlines():
            yield Param(*line.strip().split())

def load_viewpoints(viewpoint_file_list):
    """load multiple viewpoints file from given lists

    Args:
        viewpoint_file_list: a list contains obj path
        a wrapper for load_viewpoint function
    
    Returns:
        return a generator contains multiple generators
        which contains obj pathes
    """

    if isinstance(viewpoint_file_list, str):
        vp_file_list = [viewpoint_file_list]
    
    try:
        vp_file_list = iter(viewpoint_file_list)
    except TypeError:
        print("viewpoint_file_list is not an iterable object")

    for vp_file in vp_file_list:
        yield load_viewpoint(vp_file) 
    
def load_object_lists(category=None):
    """
        load object pathes according to the given category

    Args:
        category:a iterable object contains the category which
            we want render

    Returns:
        generator of gnerators of obj file pathes
    """
    
    #type checking
    if not category:
        category = g_render_objs
    elif isinstance(category, str):
        category = [category]
    else:
        try:
            iter(category)
        except TypeError:
            print("category should be an iterable object")

    #load obj file path
    for cat in category:
        num = g_shapenet_categlory_pair[cat]
        search_path = os.path.join(g_shapenet_path, num, '**','*.obj')
        yield glob.iglob(search_path, recursive=True)

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
    phi = float(elevation) * math.pi / 180 
    theta = float(azimuth) * math.pi / 180
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
        return the camera rotation in Euler angles(XYZ ordered) in radians
    """

    azimuth, elevation, tilt = float(azimuth), float(elevation), float(tilt)
    x, y, z = 90, 0, 90 #set camera at x axis facing towards object

    #twist
    #if tilt > 0:
    #    y = tilt
    #else:
    #    y = 360 + tilt

    #latitude
    x = x - elevation
    #longtitude
    z = z + azimuth

    return x * math.pi / 180, y * math.pi / 180, z * math.pi / 180

def random_sample_objs(num_per_cat):    
    """randomly sample object file from ShapeNet for each
    category in global variable g_render_objs, and then 
    save the result in global variable g_obj_path 
    
    Args:
        num_per_cat: how many obj file we want to sample per
        category

    Returns:
        vps: a dictionary contains category name and its corresponding
            obj file path
    """

    obj_path_lists = load_object_lists(g_render_objs)
    obj_path_dict = {}

    for cat, pathes in zip(g_render_objs, obj_path_lists):
        pathes = list(pathes)
        random.shuffle(pathes)
        samples = random.sample(pathes, num_per_cat)
        obj_path_dict[cat] = samples
    
    return obj_path_dict
    
def random_sample_vps(num_per_cat):
    """randomly sample vps from vp lists, for each category,
    we sample num_per_cat number vps, and save the result to
    g_vps
    Args:
        num_per_cat: how many view point to sample per category
    
    Returns:
        vps: a dictionary contains category name and its corresponding
             viewpoints
    """

    vp_file_lists = [g_view_point_file[name] for name in g_render_objs]
    viewpoint_lists = load_viewpoints(vp_file_lists)

    vp_dict = {}
    for cat, vps in zip(g_render_objs, viewpoint_lists):
        vps = list(vps)
        random.shuffle(vps)
        samples = random.sample(vps, num_per_cat)
        vp_dict[cat] = samples

    return vp_dict 

