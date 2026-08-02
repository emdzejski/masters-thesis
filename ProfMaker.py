import numpy as np 
import matplotlib.pyplot as plt
from pathlib import Path

n_voxels = [160,160, 200]
#range on y i want to take
l_y = 0
r_y = 160

f_path = "/home/jpet/ccb_dane/offbeam_no_plexa/no_plexi_recoim_noAtt/no_plexi_recoim_noAtt_it5.img"

f_name = Path(f_path).stem


vol = np.fromfile(f_path, dtype=np.float32)

vol = np.reshape(vol, n_voxels, order='F')

vol_fov = vol[60:100, l_y:r_y, 75:125]

#flipping the y axis to match the direction of the beam
vol_y_flipped = np.flip(vol_fov,1)

im_slice = vol[:,:,100]

#y_prof = np.sum(im_slice,axis = 0)

intens = np.sum(vol_y_flipped, axis = (0,2))
max_intens = np.max(intens)
norm_intens = intens/max_intens

#array, in which the profile begins with the maximum intensity 
#np.where returns a tuple, so the first element needs to be extracted
max_idx, = np.where(norm_intens == 1)[0]
#print(norm_intens)
max_norm_intens = norm_intens[max_idx:]

#print(max_norm_intens)
slices = np.arange(l_y, r_y,1)
max_slices = slices[max_idx:]
#slices = np.arange(norm_intens[max_idx],r_y, 1)
# #slices = np.arange(0,r_y-l_y,1)*2.5
# #activity = np.zeros(160)



# # for i in range(200):
# #     im_slice = vol[:,:,i] 
# #     activity = 
# #     #activity[i] = np.sum(bin_act)
# #     #print(costam)

plt.figure(figsize=(8, 5))
#plt.plot(slices, intens, marker='o', linestyle='-', color='b', markersize=4)
plt.step(slices, norm_intens,  color='black')
#plt.title("Sum of Pixel Intensities in XZ Plane vs. Y slice no.")
plt.title(f" Emission profile of {f_name}")
plt.xlabel("slice no.")
#plt.xlabel("range [mm]")
plt.ylabel("Total Intensity (a.u.)")
plt.grid(True, linestyle='--', alpha=0.6)
plt.show()