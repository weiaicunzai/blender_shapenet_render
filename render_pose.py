import os
import sys
import pickle
import numpy as np
import bpy


abs_path = os.path.abspath(__file__)
sys.path.append(os.path.dirname(abs_path))

from render_helper import *
from settings import *

#obj_path_list = load_object_lists(g_render_objs)
#viewpoint_list = load_viewpoint(g_view_point_file['chair'])

def render(pose_folder, viewpoint):
    """render pose

    convert euler angle to quaterion and then convert to rotation matrix
    you can implement your own version

    Args:
        pose_folder: path to pose folder
        viewpoint: a parameter of camera viewpoint
    """

    vp = viewpoint 
    cam_location = camera_location(vp.azimuth, vp.elevation, vp.distance)
    cam_rot = camera_rot_XYZEuler(vp.azimuth, vp.elevation, vp.tilt)
   
    bpy.data.objects['Camera'].rotation_mode = g_rotation_mode

    bpy.data.objects['Camera'].location[0] = cam_location[0]
    bpy.data.objects['Camera'].location[1] = cam_location[1]
    bpy.data.objects['Camera'].location[2] = cam_location[2]

    bpy.data.objects['Camera'].rotation_euler[0] = cam_rot[0]
    bpy.data.objects['Camera'].rotation_euler[1] = cam_rot[1]
    bpy.data.objects['Camera'].rotation_euler[2] = cam_rot[2]

    bpy.data.objects['Camera'].rotation_mode = 'QUATERNION'
    q = bpy.data.objects['Camera'].rotation_quaternion

    m = np.array(
    [[1-2*q[2]*q[2]-2*q[3]*q[3], 2*q[1]*q[2]-2*q[0]*q[3],   2*q[1]*q[3]+2*q[0]*q[2],   cam_location[0]], 
     [2*q[1]*q[2]+2*q[0]*q[3],   1-2*q[1]*q[1]-2*q[3]*q[3], 2*q[2]*q[3]-2*q[0]*q[1],   cam_location[1]],
     [2*q[1]*q[3]-2*q[0]*q[2],   2*q[2]*q[3]+2*q[0]*q[1],   1-2*q[1]*q[1]-2*q[2]*q[2], cam_location[2]],
     [0,                         0,                         0,                         1]])
        
    if not os.path.exists(g_syn_pose_folder):
        os.mkdir(g_syn_pose_folder)

    current_frame = bpy.context.scene.frame_current
    np.savetxt(os.path.join(g_syn_pose_folder, 'blender-{:06}.pose.txt'.format(current_frame)), m)
    bpy.context.scene.frame_set(current_frame + 1)

def render_pose_by_vp_lists(pose_folder, viewpoints):
    """generate pose by a list of viewpoint
    
    Args:
        pose_folder: path to pose_folder
        viewpoints: a list of viewpoint
    """

    if isinstance(tuple, viewpoints):
        vps = [viewpoints]
    
    try:
        vps = iter(viewpoints)
    except TypeError:
        print("viewpoints is not a iterable object!")
    
    for vp in vps:
        render(pose_folder, vp)

#obj_path = pickle.load(open("tmp_data/path.p", 'rb'))
vps = pickle.load(open("tmp_data/vp.p", 'rb'))

for obj_name, vp in zip(g_render_objs, vps):

    pose_folder = os.path.join(g_syn_pose_folder, obj_name)
    if not os.path.exists(pose_folder):
        os.mkdir(pose_folder)
    
    render_pose_by_vp_lists(pose_folder, vp)
    

#for obj_path_list in obj_path_list:
#    for obj_p in obj_path_list:
#        render(obj_p, viewpoint_list)