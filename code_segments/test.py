import numpy as np
import transforms3d

with open('rotation_euler.txt') as euler:
    for index, line in enumerate(euler.readlines()):
        line = line.strip().split()
        
        xyz = np.array(line)
        print(index)
        print(transforms3d.euler.euler2mat(float(xyz[0]), float(xyz[1]), float(xyz[2])))
        #tokens = line.split(line.strip())
        #print(tokens)
