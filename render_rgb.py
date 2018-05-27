""" render_rgb.py renders obj file to rgb image

Aviable function:
- clear_mash: delete all the mesh in the secene
author baiyu
"""
import sys
import os
import bpy

asb_path = os.path.abspath(__file__)
sys.path.append(os.path.dirname(asb_path))

from render_helper import *
from settings import *



#clear all the mesh in the secene:
def clear_mesh():
    """ clear all meshes in the secene

    """
    bpy.ops.object.select_all(action='DESELECT')
    for obj in bpy.data.objects:
        print(obj.name)
        if obj.type == 'MESH':
            obj.select = True
    bpy.ops.object.delete()

def scene_setting_init(use_gpu):
    """initialize blender setting configurations

    """

    sce = bpy.context.scene.name

    bpy.data.scenes[sce].render.engine = g_engine_type

    #output
    #bpy.data.scenes[sce].render.filepath = g_syn_rgb_folder
    bpy.data.scenes[sce].render.image_settings.color_mode = g_color_mode
    bpy.data.scenes[sce].render.image_settings.color_depth = g_color_depth
    bpy.data.scenes[sce].render.image_settings.file_format = g_file_format

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



clear_mesh()
scene_setting_init(g_gpu_render_enable)

print(bpy.data.scenes['Scene'].cycles.device)

obj_path_list = load_object_list('chair')
viewpoint_list = load_viewpoint(g_view_point_file['chair'])

#for obj in bpy.data.objects:
#    if obj.type == 'CAMERA':
#        cam_obj = obj

cam_obj = bpy.data.objects['Camera']
cam_obj.rotation_mode = g_rotation_mode


bpy.data.objects['Lamp'].data.energy = 100

for obj_p in obj_path_list:
    bpy.ops.import_scene.obj(filepath=obj_p)
    for index, vp in enumerate(viewpoint_list):
        cam_location = camera_location(vp.azimuth, vp.elevation, vp.distance)
        cam_rot = camera_rot_XYZEuler(vp.azimuth, vp.elevation, vp.tilt)

        cam_obj.location[0] = cam_location[0]
        cam_obj.location[1] = cam_location[1]
        cam_obj.location[2] = cam_location[2]

        cam_obj.rotation_euler[0] = cam_rot[0]
        cam_obj.rotation_euler[1] = cam_rot[1]
        cam_obj.rotation_euler[2] = cam_rot[2]

        print(cam_location, cam_rot)
        bpy.data.scenes['Scene'].render.filepath = os.path.join(g_syn_rgb_folder, 'blender-{:06}.color.png'.format(index))

        bpy.ops.render.render(write_still=True)