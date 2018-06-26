"""this module execute render operation 

author baiyu
"""



import os
import subprocess
import pickle

from render_helper import *
from settings import *



if __name__ == '__main__':

    #6 models per category
    #18000 vps for each category(each vp will be used for only once)

    #I need to serialize path ad vp since subprocess.run cant pass 
    #python object

    #you could also just comment these 6 lines after run it once
    #if you want to use the same models and vps instead of generate
    #again randomly
    obj_pathes = random_sample_objs(2)
    vps = random_sample_vps(3)

    if not os.path.exists(g_temp):
        os.mkdir(g_temp)
    with open(os.path.join(g_temp, g_tmp_path), 'wb') as f:
        pickle.dump(obj_pathes, f)
    with open(os.path.join(g_temp, g_tmp_vp), 'wb') as f:
        pickle.dump(vps, f)



    #render rgb
    command = [g_blender_excutable_path, '--background', '--python', 'render_rgb.py']
    subprocess.run(command)

    #render depth
    command = [g_blender_excutable_path, '--background', '--python', 'render_depth.py']
    subprocess.run(command)

    #write pose
    command = [g_blender_excutable_path, '--background', '--python', 'render_pose.py']
    subprocess.run(command)

