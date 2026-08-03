import numpy as np
import matplotlib.pyplot as plt
from lmfit import Model
import functions as fun

def get_image(path,n_voxels):
    vol = np.fromfile(path, dtype=np.float32)
    vol = np.reshape(vol,n_voxels,order = 'F')
    vol_flip = np.flip(vol,1)
    return vol_flip

#lmfit models
sig = Model(sigmoid)
doseResp = Model(DoseResponse)
h = Model(hill,nan_policy = 'propagate') #nan policy flag was necessary 
#to handle one pencil beam profile 
logDoseResp = Model(logDoseResponse)
log5params = Model(logistic5params)
my_atan = Model(atan)
my_tanh = Model(tanh)

models = [sig,doseResp,h,logDoseResp,log5params] #list of models
models_funcs = {sig:sigmoid, doseResp:DoseResponse, h:hill,logDoseResp:logDoseResponse,log5params:logistic5params, my_atan:atan,my_tanh:tanh}

n_voxels = [160,160, 200]
#range on y i want to take
l_y = 100
r_y = 140

vol = np.fromfile("/home/jpet/ccb_dane/offbeam_no_plexa/no_plexi_recoim_noAtt/no_plexi_recoim_noAtt_it5.img", dtype=np.float32)

vol = np.reshape(vol, n_voxels, order='F')

vol_flip = np.flip(vol,1)

vol_fov = vol_flip[60:100, l_y:r_y, 75:125]

im_slice = vol[:,:,100]

#y_prof = np.sum(im_slice,axis = 0)

intens = np.sum(vol_fov, axis = (0,2))

slices = np.arange(l_y,r_y, 1) 

fit_start = 108
fit_stop = 131

fit_range = np.arange(fit_start,fit_stop+1,1)

result = sig.fit(intens[np.where( (slices>=fit_start) & (slices<=fit_stop)  )], x = fit_range)
fit_params = list(result.best_values.values())
xs = np.linspace(fit_start,fit_stop, 10000)

print("z param: ", result.params['z'].value, "err:", result.params['z'].stderr)

plt.figure(figsize=(8, 5))
#plt.plot(slices, intens, marker='o', linestyle='-', color='b', markersize=4)
plt.step(slices, intens,  color='black')
plt.plot(xs, sigmoid(xs, *fit_params),label='dopasowanie',linewidth=2.5, color='red')
plt.axvline(result.params['z'].value,color='m', label = 'parametr z',linewidth=2.25)
plt.title("Sum of Pixel Intensities in XZ Plane vs. Y slice no.")
plt.xlabel("slice no.")
plt.ylabel("Total Intensity (a.u.)")
plt.grid(True, linestyle='--', alpha=0.6)
plt.show()

#print(np.shape(intens))