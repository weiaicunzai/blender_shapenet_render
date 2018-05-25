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

#folders to store synthetic data
g_syn_rgb_folder = '/media/admin-bai/000CA9E800027341/Untitled Folder/syn_rgb'
g_syn_depth_folder = '/media/admin-bai/000CA9E800027341/Untitled Folder/syn_depth'
g_syn_pose_foloder = '/media/admin-bai/000CA9E800027341/Untitled Folder/syn_pose'

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

