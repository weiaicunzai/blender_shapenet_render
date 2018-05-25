import sys
import os
import bpy

asb_path = os.path.abspath(__file__)
sys.path.append(os.path.dirname(asb_path))

from settings import *



sce = bpy.context.scene.name
bpy.data.scenes[sce].render.filepath = os.path.join(g_syn_rgb_folder, 'test.png')
bpy.ops.render.render(write_still=True)
