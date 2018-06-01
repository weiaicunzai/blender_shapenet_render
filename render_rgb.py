""" render_rgb.py renders obj file to rgb image

Aviable function:
- clear_mash: delete all the mesh in the secene
- scene_setting_init: set scene configurations


author baiyu
"""
import sys
import os
import random
import bpy

abs_path = os.path.abspath(__file__)
sys.path.append(os.path.dirname(abs_path))

from render_helper import *
from settings import *


def clear_mesh():
    """ clear all meshes in the secene

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
    bpy.data.scenes[sce].cycles.film_transparent = g_use_film_transparent
    #output
    bpy.data.scenes[sce].render.image_settings.color_mode = g_rgb_color_mode
    bpy.data.scenes[sce].render.image_settings.color_depth = g_rgb_color_depth
    bpy.data.scenes[sce].render.image_settings.file_format = g_rgb_file_format

    #dimensions
    bpy.data.scenes[sce].render.resolution_x = g_resolution_x
    bpy.data.scenes[sce].render.resolution_y = g_resolution_y
    bpy.data.scenes[sce].render.resolution_percentage = g_resolution_percentage

    if use_gpu:
        bpy.data.scenes[sce].render.engine = 'CYCLES' #only cycles engine can use gpu
        bpy.data.scenes[sce].render.tile_x = g_hilbert_spiral
        bpy.data.scenes[sce].render.tile_x = g_hilbert_spiral
        bpy.types.CyclesRenderSettings.device = 'GPU'
        bpy.data.scenes[sce].cycles.device = 'GPU'

def node_setting_init():
    """node settings for render rgb images

    mainly for compositing the background images
    """


    bpy.context.scene.use_nodes = True
    tree = bpy.context.scene.node_tree
    links = tree.links

    for node in tree.nodes:
        tree.nodes.remove(node)
    
    image_node = tree.nodes.new('CompositorNodeImage')
    scale_node = tree.nodes.new('CompositorNodeScale')
    alpha_over_node = tree.nodes.new('CompositorNodeAlphaOver')
    render_layer_node = tree.nodes.new('CompositorNodeRLayers')
    file_output_node = tree.nodes.new('CompositorNodeOutputFile')

    scale_node.space = g_scale_space
    file_output_node.base_path = g_syn_rgb_folder

    links.new(image_node.outputs[0], scale_node.inputs[0])
    links.new(scale_node.outputs[0], alpha_over_node.inputs[1])
    links.new(render_layer_node.outputs[0], alpha_over_node.inputs[2])
    links.new(alpha_over_node.outputs[0], file_output_node.inputs[0])


def render(obj_path, viewpoints):
    """render rbg image 

    render a object rgb image by given camera viewpoints and
    choose random image as background

    Args:
        obj_path: a string variable indicate the obj file path
        viewpoints: a generator of cmera viewpoints
    """

    background_images = os.listdir(g_background_image_path)

    for index, vp in enumerate(viewpoint_list):
        cam_location = camera_location(vp.azimuth, vp.elevation, vp.distance)
        cam_rot = camera_rot_XYZEuler(vp.azimuth, vp.elevation, vp.tilt)

        cam_obj.location[0] = cam_location[0]
        cam_obj.location[1] = cam_location[1]
        cam_obj.location[2] = cam_location[2]

        cam_obj.rotation_euler[0] = cam_rot[0]
        cam_obj.rotation_euler[1] = cam_rot[1]
        cam_obj.rotation_euler[2] = cam_rot[2]

        if not os.path.exists(g_syn_rgb_folder):
            os.mkdir(g_syn_rgb_folder)
        
        image_name = random.choice(background_images)
        image_path = os.path.join(g_background_image_path, image_name)

        image_node = bpy.context.scene.node_tree.nodes[0]
        image_node.image = bpy.data.images.load(image_path)
        file_output_node = bpy.context.scene.node_tree.nodes[4]
        file_output_node.file_slots[0].path = 'blender-######.color.png' # blender placeholder #
        bpy.context.scene.frame_set(index + 1)

        bpy.ops.render.render(write_still=True)



scene_setting_init(g_gpu_render_enable)
node_setting_init()


obj_path_list = load_object_list(g_render_objs)
viewpoint_list = load_viewpoint(g_view_point_file['chair'])


cam_obj = bpy.data.objects['Camera']
cam_obj.rotation_mode = g_rotation_mode

bpy.data.objects['Lamp'].data.energy = 50
#bpy.data.objects['Lamp'].type = 'SUN'
bpy.ops.object.lamp_add(type='POINT', location=(-3, -3, 3))

for obj_lists in obj_path_list:
    for obj_p in obj_lists:
        clear_mesh()
        bpy.ops.import_scene.obj(filepath=obj_p)
        render(obj_p, obj_lists)

