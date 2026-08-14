import numpy as np
import matplotlib.pyplot as plt
from lmfit import Model
import functions as fun
from pathlib import Path

def get_image(path,n_voxels):
    vol = np.fromfile(path, dtype=np.float32)
    vol = np.reshape(vol,n_voxels,order = 'F')
    vol_flip = np.flip(vol,1)
    return vol_flip

def find_min(xs,data): #computes a differential of data, returns min value
    
    idx = np.where(xs>=135)
    diff = np.gradient(data[idx],xs[idx])
    short_range = xs[idx]

    #the index of the found value needs to be shifted by one 
    
    #np.where returns a tuple, so the first element needs to be extracted
    min_idx = np.where(diff == np.min(diff))[0] - 1
    return short_range[min_idx]

#lmfit models
sig = Model(fun.sigmoid)
doseResp = Model(fun.DoseResponse)
h = Model(fun.hill,nan_policy = 'propagate') #nan policy flag was necessary 
#to handle one pencil beam profile 
logDoseResp = Model(fun.logDoseResponse)
log5params = Model(fun.logistic5params)
my_atan = Model(fun.atan)
my_tanh = Model(fun.tanh)

models = [sig,doseResp,h,logDoseResp,log5params] #list of models
models_funcs = {sig:fun.sigmoid, doseResp:fun.DoseResponse, h:fun.hill,logDoseResp:fun.logDoseResponse,log5params:fun.logistic5params, my_atan:fun.atan,my_tanh:fun.tanh}

f_path = "/home/jpet/ccb_dane/offbeam_plexa/plexi_recoim_noAtt/plexi_recoim_noAtt_it5.img"
f_name = Path(f_path).stem

n_voxels = [160,160, 200]
#range on y i want to take
l_y = 45
r_y = 160

vol = get_image(f_path, n_voxels)

vol_fov = vol[60:100, l_y:r_y, 75:125]

#im_slice = vol[:,:,100]

#y_prof = np.sum(im_slice,axis = 0)

intens = np.sum(vol_fov, axis = (0,2))

slices = np.arange(l_y*2.5,r_y*2.5, 2.5)

min_val = find_min(slices, intens)
#print(min_val)

fit_start = min_val - 18
fit_stop = min_val + 50

arr =intens[np.where( (slices>=fit_start) & (slices<=fit_stop) )]


fit_range = np.arange(fit_start,fit_stop+1,2.5)


result = doseResp.fit(intens[np.where( (slices>=fit_start) & (slices<=fit_stop)  )], x = fit_range)
fit_params = list(result.best_values.values())
xs = np.linspace(fit_start,fit_stop, 10000)
#print(result.fit_report())
print("z param: ", result.params['z'].value, "err:", result.params['z'].stderr)

plt.figure(figsize=(8, 5))
#plt.plot(slices, intens, marker='o', linestyle='-', color='b', markersize=4)
plt.step(slices, intens,  color='black')
plt.plot(xs, fun.DoseResponse(xs, *fit_params),label='dopasowanie',linewidth=2.5, color='red')
plt.axvline(result.params['z'].value,color='m', label = 'parametr z',linewidth=2.25)
plt.title(f" Emission profile of {f_name}")
plt.xlabel("y-axis slice * 2.5 [mm]") #voxel no. * voxel size=2.5 mm
#plt.xlabel("slice no.")
plt.ylabel("Total Intensity (a.u.)")
plt.grid(True, linestyle='--', alpha=0.6)
plt.show()

#print(np.shape(intens))