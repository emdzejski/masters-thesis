import numpy as np

#dimensions from castor .hdr file
dim_x = 160  
dim_y = 160  
dim_z = 200  

input_file = "/home/jpet/ccb_dane/offbeam_no_plexa/no_plexi_recoim_noAtt/no_plexi_recoim_noAtt_it5.img"
output_file = "/home/jpet/overlay_test/no_plexi_recoim_noAtt_it5_flipped.img"

img = np.fromfile(input_file, dtype=np.float32)

#order='F'(Fortran/column-major), because CASToR writes data this way, 
img_3d = img.reshape((dim_x, dim_y, dim_z), order='F')

#flipping y axis to match the direction of the beam
flipped_img = np.flip(img_3d, axis=1)

flipped_img.flatten(order='F').tofile(output_file)

print(f"Done! Flipped image saved to: {output_file}")