import numpy as np 
import matplotlib.pyplot as plt
from pathlib import Path
from mpl_toolkits.axes_grid1 import make_axes_locatable

voxel_size = 2.5 #mm
f_path = "/home/jpet/ccb_dane/offbeam_no_plexa/no_plexi_recoim_noAtt/no_plexi_recoim_noAtt_it5.img"
f_name = Path(f_path).stem


n_voxels = [160,160, 200]
l_y = 0
r_y = 160
axes_label = {0:"zy", 1:"zx", 2:"yx"}

vol = np.fromfile(f_path, dtype=np.float32)
vol = np.reshape(vol, n_voxels, order='F')
vol_y_flipped = np.flip(vol,1)

fov_limits = [
    (20, 140),  # X axis limits
    (20, 110),  # Y axis limits
    (50, 140)   # Z axis limits
]

vol_fov = vol_y_flipped[
    fov_limits[0][0]:fov_limits[0][1], 
    fov_limits[1][0]:fov_limits[1][1], 
    fov_limits[2][0]:fov_limits[2][1]
]

#vol_fov = vol_y_flipped[20:140, 20:110, 50:140]

axes = [0,1,2]
for a in axes:
    projection_2d = np.sum(vol_fov, axis = a) #sum along a given axis to create a plane projection 

    projection_2d = projection_2d.T

    if a == 0:
        x_idx, y_idx = 1, 2  # Plotting Y on x-axis, Z on y-axis
    elif a == 1:
        x_idx, y_idx = 0, 2  # Plotting X on x-axis, Z on y-axis
    elif a == 2:
        x_idx, y_idx = 0, 1  # Plotting X on x-axis, Y on y-axis

    x_min, x_max = fov_limits[x_idx]
    y_min, y_max = fov_limits[y_idx]

    
    extent_mm = [
        x_min * voxel_size, x_max * voxel_size, 
        y_max * voxel_size, y_min * voxel_size
    ]    

    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(projection_2d, cmap='turbo', aspect= 'auto',extent = extent_mm)
    ax.set_xlabel(f"{axes_label[a][1]} [mm]")
    ax.set_ylabel(f"{axes_label[a][0]} [mm]")

    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.15)
    fig.colorbar(im, cax=cax)
   
    plt.tight_layout()
    plt.savefig(f"/home/jpet/ccb_dane/graphs/reco_ims/noplexi_noatt/{axes_label[a]}_{f_name}.png", dpi=300)
    plt.show()
    plt.close()