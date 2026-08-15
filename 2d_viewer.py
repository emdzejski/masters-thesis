import numpy as np 
import matplotlib.pyplot as plt
from pathlib import Path

f_path = "/home/jpet/ccb_dane/offbeam_no_plexa/no_plexi_recoim_noAtt/no_plexi_recoim_noAtt_it5.img"
f_name = Path(f_path).stem


n_voxels = [160,160, 200]
l_y = 0
r_y = 160
title_label = {0:"YZ", 1:"XZ", 2:"XY"}

vol = np.fromfile(f_path, dtype=np.float32)
vol = np.reshape(vol, n_voxels, order='F')
vol_y_flipped = np.flip(vol,1)

vol_fov = vol_y_flipped[::, l_y:r_y, ::]
ax = 0

projection_2d = np.sum(vol_fov, axis = ax) #sum along a given axis to create a plane projection 

projection_2d = projection_2d.T

plt.figure(figsize=(5.5, 6))
plt.imshow(projection_2d, cmap='turbo')
plt.colorbar(label="")
plt.title(f"{title_label[ax]} plane of {f_name}")
plt.tight_layout()
plt.show()