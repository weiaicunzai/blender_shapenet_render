"""render_helper.py contains functions that processing
data to the format we want


Available functions:
- load_viewpoint: read viewpoint file
- load_object_list: return a list of object file pathes

author baiyu
"""


import os 
import glob

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
    Param = namedtuple('Param',['azimuth', 'evalutaion', 'tilt', 'distance'])
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

