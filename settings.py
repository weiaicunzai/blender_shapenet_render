"""settings.py contains all configuration parameters the blender needs


author baiyu
"""



g_shapenet_path = '/media/admin-bai/000CA9E800027341/DATA/RenderForCNN-master/datasets/shapenetcore'
g_blender_excutable_path = '/home/admin-bai/Downloads/blender-2.79b-linux-glibc219-x86_64/blender'

#if you have multiple viewpoint files, add to the dict
#files contains azimuth,elevation,tilt angles and distance for each row
g_view_point_file ={
    'chair' : '/media/admin-bai/000CA9E800027341/DATA/RenderForCNN-master/data/view_distribution/chair.txt'
}

g_background_image_path = '/media/admin-bai/000CA9E800027341/DATA/RenderForCNN-master/datasets/sun2012pascalformat/JPEGImages'


#background image composite
#enum in [‘RELATIVE’, ‘ABSOLUTE’, ‘SCENE_SIZE’, ‘RENDER_SIZE’], default ‘RELATIVE’
g_scale_space = 'RENDER_SIZE'
g_use_film_transparent = True

#camera:
#enum in [‘QUATERNION’, ‘XYZ’, ‘XZY’, ‘YXZ’, ‘YZX’, ‘ZXY’, ‘ZYX’, ‘AXIS_ANGLE’]
g_rotation_mode = 'XYZ'
g_depth_clip_start = 0.5
g_depth_clip_end = 4

#output:

#folders to store synthetic data
g_syn_rgb_folder = '/media/admin-bai/000CA9E800027341/Untitled Folder/syn_rgb'
g_syn_depth_folder = '/media/admin-bai/000CA9E800027341/Untitled Folder/syn_depth'
g_syn_pose_foloder = '/media/admin-bai/000CA9E800027341/Untitled Folder/syn_pose'

#enum in [‘BW’, ‘RGB’, ‘RGBA’], default ‘BW’
g_rgb_color_mode = 'RGB'
#enum in [‘8’, ‘10’, ‘12’, ‘16’, ‘32’], default ‘8’
g_rgb_color_depth = '16'
g_rgb_file_format = 'PNG'

g_depth_color_mode = 'BW'
g_depth_color_depth = '8'
g_depth_file_format = 'PNG'

g_depth_use_overwrite = True
g_depth_use_file_extension = True

#dimension:

#engine type [CYCLES, BLENDER_RENDER]
g_engine_type = 'CYCLES'

#output image size =  (g_resolution_x * resolution_percentage%, g_resolution_y * resolution_percentage%)
g_resolution_x = 1920
g_resolution_y = 1080
g_resolution_percentage = 50


#performance:

g_gpu_render_enable = True

#if you are using gpu render, recommand to set hilbert spiral to 256 or 512
#default value for cpu render is fine
g_hilbert_spiral = 512 

g_render_objs = ['chair']

#total 55 categories
g_shapenet_categlory_pair = {
    'table' : '04379243',
    'jar' : '03593526',
    'skateboard' : '04225987',
    'car' : '02958343',
    'bottle' : '02876657',
    'tower' : '04460130',
    'chair' : '03001627',
    'bookshelf' : '02871439',
    'camera' : '02942699',
    'airplane' : '02691156',
    'laptop' : '03642806',
    'basket' : '02801938',
    'sofa' : '04256520',
    'knife' : '03624134',
    'can' : '02946921',
    'rifle' : '04090263',
    'train' : '04468005',
    'pillow' : '03938244',
    'lamp' : '03636649',
    'trash bin' : '02747177',
    'mailbox' : '03710193',
    'watercraft' : '04530566',
    'motorbike' : '03790512',
    'dishwasher' : '03207941',
    'bench' : '02828884',
    'pistol' : '03948459',
    'rocket' : '04099429',
    'loudspeaker' : '03691459',
    'file cabinet' : '03337140',
    'bag' : '02773838',
    'cabinet' : '02933112',
    'bed' : '02818832',
    'birdhouse' : '02843684',
    'display' : '03211117',
    'piano' : '03928116',
    'earphone' : '03261776',
    'telephone' : '04401088',
    'stove' : '04330267',
    'microphone' : '03759954',
    'bus' : '02924116',
    'mug' : '03797390',
    'remote' : '04074963',
    'bathtub' : '02808440',
    'bowl' : '02880940',
    'keyboard' : '03085013',
    'guitar' : '03467517',
    'washer' : '04554684',
    'bicycle' : '02834778',
    'faucet' : '03325088',
    'printer' : '04004475',
    'cap' : '02954340',
    'clock' : '03046257',
    'helmet' : '03513137',
    'flowerpot' : '03991062',
    'microwaves' : '03761084'
}

