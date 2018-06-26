""" render_depth.py renders obj file to depth image

Aviable function:
- clear_mash: delete all the mesh in the secene
- scene_setting_init: set scene configurations
- node_setting_init: set node configurations
- camera_setting_init: set camera configurations
- render: render depth image for each viewpoint
- render_depth_by_vp_lists: wrapper function for
    render, render one obj file by multiple viewpoints
- render_objs_by_one_vp: wrapper function for
    render, render multiple objs by one vp
- set_depth_path: set depth image output path

author baiyu
"""

import sys
import os
import pickle
import bpy

abs_path = os.path.abspath(__file__)
sys.path.append(os.path.dirname(abs_path))

from render_helper import *
from settings import *

def clear_mesh():
    """ clear all meshes in the scene

    """
    bpy.ops.object.select_all(action='DESELECT')
    for obj in bpy.data.objects:
        if obj.type == 'MESH':
            obj.select = True
    bpy.ops.object.delete()

def scene_setting_init(use_gpu):
    """initialize blender setting configurations 
    
    """
    sce = bpy.context.scene.name
    bpy.data.scenes[sce].render.engine = g_engine_type

    #output
   # bpy.data.scenes[sce].render.image_settings.color_mode = g_depth_color_mode
   # bpy.data.scenes[sce].render.image_settings.color_depth = g_depth_color_depth
    bpy.data.scenes[sce].render.image_settings.file_format = g_depth_file_format
    bpy.data.scenes[sce].render.use_overwrite = g_depth_use_overwrite
    bpy.data.scenes[sce].render.use_file_extension = g_depth_use_file_extension 

    #dimensions
    bpy.data.scenes[sce].render.resolution_x = g_resolution_x
    bpy.data.scenes[sce].render.resolution_y = g_resolution_y
    bpy.data.scenes[sce].render.resolution_percentage = g_resolution_percentage

    if use_gpu:
            # only cycles engine can use gpu
        bpy.data.scenes[sce].render.engine = 'CYCLES'
        bpy.data.scenes[sce].render.tile_x = g_hilbert_spiral
        bpy.data.scenes[sce].render.tile_x = g_hilbert_spiral
       # bpy.context.user_preferences.addons['cycles'].preferences.devices[0].use = True
       # bpy.context.user_preferences.addons['cycles'].preferences.compute_device_type = 'CUDA'
        bpy.types.CyclesRenderSettings.device = 'GPU'
        bpy.data.scenes[sce].cycles.device = 'GPU'

def node_setting_init():
    """ node settings for z pass

    we are using a map value node to map the
    z pass value to [0.5, 4] (meters)
    """

    bpy.context.scene.use_nodes = True
    tree = bpy.context.scene.node_tree
    links = tree.links

    for node in tree.nodes:
        tree.nodes.remove(node)
    
    render_layer_node = tree.nodes.new('CompositorNodeRLayers')
    map_value_node = tree.nodes.new('CompositorNodeMapValue')
    file_output_node = tree.nodes.new('CompositorNodeOutputFile')

    map_value_node.offset[0] = -g_depth_clip_start
    map_value_node.size[0] = 1 / (g_depth_clip_end - g_depth_clip_start)
    map_value_node.use_min = True
    map_value_node.use_max = True
    map_value_node.min[0] = 0.0
    map_value_node.max[0] = 1.0

    file_output_node.format.color_mode = g_depth_color_mode
    file_output_node.format.color_depth = g_depth_color_depth
    file_output_node.format.file_format = g_depth_file_format 
    file_output_node.base_path = g_syn_depth_folder

    links.new(render_layer_node.outputs[2], map_value_node.inputs[0])
    links.new(map_value_node.outputs[0], file_output_node.inputs[0])

def camera_setting_init():
    """camera settings for render

    the first tow line can be commented, just in case you forgot to
    set map value node
    """
    bpy.data.cameras['Camera'].clip_start = g_depth_clip_start
    bpy.data.cameras['Camera'].clip_end = g_depth_clip_end
    bpy.data.objects['Camera'].rotation_mode = g_rotation_mode

def render(obj_path, viewpoint):
    """render z pass 

    render a object z pass map by a given camera viewpoints

    Args:
        obj_path: a string variable indicate the obj file path
        viewpoint: a parameter of camera parameters
    """

#    for index, vp in enumerate(viewpoint_list):
    vp = viewpoint
    cam_location = camera_location(vp.azimuth, vp.elevation, vp.distance)
    cam_rot = camera_rot_XYZEuler(vp.azimuth, vp.elevation, vp.tilt)
   
    bpy.data.objects['Camera'].location[0] = cam_location[0]
    bpy.data.objects['Camera'].location[1] = cam_location[1]
    bpy.data.objects['Camera'].location[2] = cam_location[2]

    bpy.data.objects['Camera'].rotation_euler[0] = cam_rot[0]
    bpy.data.objects['Camera'].rotation_euler[1] = cam_rot[1]
    bpy.data.objects['Camera'].rotation_euler[2] = cam_rot[2]

    if not os.path.exists(g_syn_depth_folder):
        os.mkdir(g_syn_depth_folder)

    file_output_node = bpy.context.scene.node_tree.nodes[2]
    file_output_node.file_slots[0].path = 'blender-######.depth.png' # blender placeholder #

    bpy.ops.render.render(write_still=True)

    current_frame = bpy.context.scene.frame_current
    bpy.context.scene.frame_set(current_frame + 1)

def render_depth_by_vp_lists(obj_path, viewpoints):
    """ render one depth image by a given viewpoint list
    a wrapper function for render()

    Args:
        obj_path: a string variable indicate the obj file path
        viewpoints: an iterable object of vp parameter(contains azimuth,elevation,tilt angles and distance)
    """

    if isinstance(viewpoints, tuple):
        vp_lists = [viewpoints]

    try:
        vp_lists = iter(viewpoints)
    except TypeError:
        print("viewpoints is not an iterable object")
    
    for vp in vp_lists:
        render(obj_path, vp)

def render_objs_by_one_vp(obj_pathes, viewpoint):
    """ render multiple depth image by a given viewpoint

    Args:
        obj_paths: an iterable object contains multiple
                   obj file pathes
        viewpoint: a namedtuple object contains azimuth,
                   elevation,tilt angles and distance
    """ 

    if isinstance(obj_pathes, str):
        obj_lists = [obj_pathes]
    
    try:
        obj_lists = iter(obj_lists)
    except TypeError:
        print("obj_pathes is not an iterable object")
    
    for obj_path in obj_lists:
        render(obj_path, viewpoint)


def set_depth_path(new_path):
    """ set depth output path to new_path

    Args:
        new rendered depth output path
    """
    file_output_node = bpy.context.scene.node_tree.nodes[2]
    file_output_node.base_path = new_path

def init_all():
    """ initialze everything we need for z pass render
    """
    scene_setting_init(g_gpu_render_enable)
    camera_setting_init()
    node_setting_init()

### YOU CAN WRITE YOUR OWN IMPLEMENTATION TO GENERATE DATA

init_all()

result_dict = pickle.load(open(os.path.join(g_temp, g_result_dict), 'rb'))

for obj_name, models in result_dict.items():
    obj_folder = os.path.join(g_syn_depth_folder, obj_name)
    if not os.path.exists(obj_folder):
        os.mkdir(obj_folder)
    
    for model in models:
        clear_mesh()
        bpy.ops.import_scene.obj(filepath=model.path)
        set_depth_path(obj_folder)
        render_depth_by_vp_lists(model.path, model.vps)