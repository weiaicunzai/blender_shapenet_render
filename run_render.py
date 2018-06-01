"""this module execute render operation 

author baiyu
"""



import os
import subprocess

from settings import *



if __name__ == '__main__':


    #render rgb
    command = [g_blender_excutable_path, '--background', '--python', 'render_rgb.py']
    subprocess.run(command)

    #render depth
    command = [g_blender_excutable_path, '--background', '--python', 'render_depth.py']
    subprocess.run(command)

    #write pose
    command = [g_blender_excutable_path, '--background', '--python', 'render_pose.py']
    subprocess.run(command)

