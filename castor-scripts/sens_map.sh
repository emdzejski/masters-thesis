########
#script for generating the phantom sensitivity map 

#-df -> sensitivity map of the detector
#dim -> image dimensions
#vox -> voxel dimensions
#fout -> directory, where the sens. map will be saved 
#img -> attenuation map created based on CT image of the phantom
########

castor-recon -df /home/jpet/pliki_szymona/configs/sensitivity_lm_dualhead_ccb_df.Cdh -dim 160,160,200 -vox 2.5,2.5,2.5 -th 0 -it 1:1 -fout /home/jpet/ccb_dane/sens_map_dualhead/ -proj multiSiddon,1,1 -opti SENS -ignore-corr fdur -img /home/jpet/ct_scan/m_umap_resampled.hdr -vb 2 

