import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider
from scipy.ndimage import shift

def get_image(path,n_voxels):
    vol = np.fromfile(path, dtype=np.float32)
    vol = np.reshape(vol,n_voxels,order = 'F')
    vol_flip = np.flip(vol,1)
    return vol_flip

map_path= "/home/jpet/ct_scan/map_tests/m_umap_resampled.img"
pet_path = "/home/jpet/ccb_dane/offbeam_no_plexa/no_plexi_recoim_noAtt/no_plexi_recoim_noAtt_it5.img"

n_voxels = [160, 160, 200]
umap = get_image(map_path, n_voxels)
pet_im = get_image(pet_path, n_voxels)


umap_slice = umap[80, :, :]
pet_slice = pet_im[80, :, :]

#figure with extra space at the bottom for sliders
fig, ax = plt.subplots(figsize=(6, 7))
plt.subplots_adjust(bottom=0.25) 


ct_plot = ax.imshow(umap_slice, cmap='gray')
pet_plot = ax.imshow(pet_slice, cmap='turbo', alpha=0.6)
ax.set_title('Overlaid Images')

#axes for the sliders
ax_shift_x = plt.axes([0.2, 0.1, 0.6, 0.03])
ax_shift_y = plt.axes([0.2, 0.05, 0.6, 0.03])


slider_x = Slider(ax_shift_x, 'Shift X', -80, 80, valinit=0, valstep=1)
slider_y = Slider(ax_shift_y, 'Shift Y', -80, 80, valinit=0, valstep=1)

#function updating the image
def update(val):
    dx = slider_x.val
    dy = slider_y.val
    
    #shifting ct/umap
    shifted_map = shift(umap_slice, (dy, dx), mode='constant', cval=0.0)
    
    # Update the plot data and redraw
    ct_plot.set_data(shifted_map)
    fig.canvas.draw_idle()

slider_x.on_changed(update)
slider_y.on_changed(update)

plt.show()