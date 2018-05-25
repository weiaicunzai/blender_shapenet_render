"""this module execute render operation 

Available functions:
- load_viewpoint  read viewpoint file
- load_object

author baiyu
"""



import os
import subprocess

from settings import *
def render_rgb(viewpoints, model):
    """render rgb images according to the given viewpoints and model

    Args:
        viewpoinst: a list contains viewpoint(azimuth,elevation,tilt angles and distance)
        model: a list contains obj file path
    """ 

    pass


def param_init():
    pass
if __name__ == '__main__':

    #param initialize:


    asb_path = os.path.abspath(__file__)
    print('fff')
    command = [g_blender_excutable_path, '--background', '--python', 'render_rgb.py']
    print(command)
    result = subprocess.run([g_blender_excutable_path, '--background', '--python', 'render_rgb.py'], stdout=subprocess.PIPE)
    #result = subprocess.run([command], stdout=subprocess.PIPE)
    print(result.stdout.decode())

