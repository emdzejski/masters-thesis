import numpy as np 
import matplotlib.pyplot as plt
from pathlib import Path
from mpl_toolkits.axes_grid1 import make_axes_locatable

voxel_size = 2.5 #mm
f_path = "/home/jpet/ct_scan/m_umap_resampled.img"
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

# vol_fov = vol_y_flipped[
#     fov_limits[0][0]:fov_limits[0][1], 
#     fov_limits[1][0]:fov_limits[1][1], 
#     fov_limits[2][0]:fov_limits[2][1]
# ]

#vol_fov = vol_y_flipped[20:140, 20:110, 50:140]

#slice = vol_y_flipped[80, ::, ::].T

# fig, ax = plt.subplots(figsize=(8, 6))
# im = ax.imshow(slice, aspect= 'auto')
# divider = make_axes_locatable(ax)
# cax = divider.append_axes("right", size="5%", pad=0.15)
# fig.colorbar(im, cax=cax)

# plt.tight_layout()
# #plt.savefig(f"/home/jpet/ccb_dane/graphs/reco_ims/plexi_noatt/{axes_label[a]}_{f_name}.png", dpi=300)
# plt.show()
# plt.close()

axes = [0,1,2]
for a in axes:
    if a == 0:
        x_idx, y_idx = 1, 2 
        slice_num = 80 # Plotting Y on x-axis, Z on y-axis
    elif a == 1:
        x_idx, y_idx = 0, 2
        slice_num = 80  # Plotting X on x-axis, Z on y-axis
    elif a == 2:
        x_idx, y_idx = 0, 1 
        slice_num = 100 # Plotting X on x-axis, Y on y-axis

    # x_min, x_max = fov_limits[x_idx]
    # y_min, y_max = fov_limits[y_idx]
    slice = np.take(vol_y_flipped, slice_num, axis = a)
    slice = slice.T

    dims = np.shape(slice)[:2]

    
    extent_mm = [
        0,  dims[0]* voxel_size, 
        dims[1] * voxel_size, 0 * voxel_size
    ]    

    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(slice, aspect= 'auto',extent = extent_mm)
    ax.set_xlabel(f"{axes_label[a][1]} [mm]")
    ax.set_ylabel(f"{axes_label[a][0]} [mm]")

    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.15)
    fig.colorbar(im, cax=cax, label = r"$\mu \hspace{0.5}[\mathrm{cm}^-1]$")
   
    plt.tight_layout()
    plt.savefig(f"/home/jpet/ccb_dane/graphs/att_map/{axes_label[a]}_{f_name}.png", dpi=300)
    plt.show()
    plt.close()