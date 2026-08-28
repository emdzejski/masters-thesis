import numpy as np 
import matplotlib.pyplot as plt
from pathlib import Path
from mpl_toolkits.axes_grid1 import make_axes_locatable

voxel_size = 2.5
f_path = "/home/jpet/ccb_dane/offbeam_plexa/plexi_recoim_noAtt/plexi_recoim_noAtt_it5.img"
f_name = Path(f_path).stem


n_voxels = [160,160, 200]
l_y = 0
r_y = 160
axes_label = {0:"zy", 1:"zx", 2:"yx"}

vol = np.fromfile(f_path, dtype=np.float32)
vol = np.reshape(vol, n_voxels, order='F')
vol_y_flipped = np.flip(vol,1)

vol_fov = vol_y_flipped[20:140, 20:110, 50:140]

axes = [0,1,2]
for a in axes:
    projection_2d = np.sum(vol_fov, axis = a) #sum along a given axis to create a plane projection 

    projection_2d = projection_2d.T

    h,w = projection_2d.shape[:2]
    extent = [0, w * voxel_size, h * voxel_size, 0]

    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(projection_2d, cmap='turbo', extent = extent, aspect= 'auto')
    ax.set_xlabel(f"{axes_label[a][1]} [mm]")
    ax.set_ylabel(f"{axes_label[a][0]} [mm]")

    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.15)
    fig.colorbar(im, cax=cax)
   
    plt.tight_layout()
    plt.savefig(f"/home/jpet/ccb_dane/graphs/reco_ims/plexi_noatt/{axes_label[a]}_{f_name}.png", dpi=300)
    plt.show()
    plt.close()