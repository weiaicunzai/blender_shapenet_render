"""this module execute render operation 

author baiyu
"""



import os
import subprocess

from settings import *



if __name__ == '__main__':


    #render rgb
 #   command = [g_blender_excutable_path, '--background', '--python', 'render_rgb.py']
 #   result = subprocess.run(command)

    #render depth
    command = [g_blender_excutable_path, '--background', '--python', 'render_depth.py']
    result = subprocess.run(command)

