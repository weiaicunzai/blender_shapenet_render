""" render_depth.py renders obj file to depth image

Aviable function:
- clear_mash: delete all the mesh in the secene
- scene_setting_init: set scene configurations


author baiyu
"""

import sys
import os
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

def render(obj_path, viewpoints):
    """render z pass 

    render a object z pass map by given camera viewpoints

    Args:
        obj_path: a string variable indicate the obj file path
        viewpoints: a generator of cmera viewpoints
    """

    for index, vp in enumerate(viewpoint_list):
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
        bpy.context.scene.frame_set(index + 1)

        bpy.ops.render.render(write_still=True)
        break



scene_setting_init(g_gpu_render_enable)
camera_setting_init()
node_setting_init()

obj_path_list = load_object_list(g_render_objs)
viewpoint_list = load_viewpoint(g_view_point_file['chair'])

for obj_path_list in obj_path_list:
    for obj_p in obj_path_list:
        clear_mesh()
        bpy.ops.import_scene.obj(filepath=obj_p)
        render(obj_p, viewpoint_list)

