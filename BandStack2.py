import os
import rasterio as rio
print("This script will read from a folder containing Sentinel2 or Landsat images and stack the bands in the order of 'BGRN'. \n Please enter full filepaths.")
#root variable
img_type = input("Image type [Enter 'sentinel' or 'landsat'] :")
if not (img_type == 'sentinel' or img_type == 'landsat'):
    print('Image type not recognized, try again!')
    img_type = input("Image type [Enter 'sentinel' or 'landsat'] :")

#sentinel data downloads as .jp2 files while landsat comes as .tif
if img_type == 'sentinel':
    file_ext = ".jp2"
else:
    file_ext = ".TIF"
print(file_ext)
data_str = "Directory containing {} images:".format(img_type)
data_dir = input(data_str) # directory to be searched for images
results_dir = input("Directory to save output(will be created if does not exist): ")
new_raster = input("Save new raster as: ")

if not os.path.exists(results_dir):
    os.mkdir(results_dir)

# empty list to hold rasters
raster_list = []

# set the order of bands. To match planet data: BGRN
if img_type == 'sentinel':
    band_order = ['B02', 'B03', 'B04', 'B08']
elif img_type == 'landsat':
    band_order = ['B2', 'B3', 'B4', 'B5']
print(band_order)
# band_order first to ensure rasters added in desired order
for band in band_order:
    # now go into data directory, list files using os.listdir:
    for raster in os.listdir(data_dir):
        # append desired .tif or .jp2 files to raster_list:
        if raster.endswith(band + file_ext):
            print('raster_found')
            raster_list.append(raster)

print(raster_list)
# ----RASTERIO (imported as rio) ----
# could say:
# source = os.path.join(data_dir, raster_list[0])
# sample_band = rio.open(source)
# meta = sample_band.meta
            
# (assigns meta data from first raster to variable: meta)
# NOTE that in the present case all rasters have the same meta data, and thus
# the meta variable can be and is used for all bands.
            
with rio.open(os.path.join(data_dir, raster_list[0])) as source:
    meta = source.meta

# update the 'count' metadata to equal # of bands being stacked.
if file_ext == ".jp2":
    meta.update(count = len(raster_list), driver = 'Gtiff')
elif file_ext == ".tif":
    meta.update(count = len(raster_list))
else: print('tif error')

# write new_raster.tif as variable 'destination'
with rio.open(os.path.join(results_dir, new_raster), 'w', **meta) as destination:
    # count rasters while iterating over raster_list staring at 1
    for counter, band in enumerate(raster_list, start=1):
        #read each raster as the variable 'band', assign it as 'source1', then 
        # write it to the new raster 'destination'.
        # 'counter' is position of band to be written, 'source1.read(1)' reads
        # each of the rasters in the directory, the (1) specifies that it is a
        # 2d array(ie. a raster of a single band with length and width dimensions.)
        with rio.open(os.path.join(data_dir, band)) as source1:
            destination.write_band(counter, source1.read(1))

# That's it! #