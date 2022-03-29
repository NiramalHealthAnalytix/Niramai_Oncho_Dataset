**Welcome to Niramai Oncho Dataset**

* This is the dataset collected during the pilot study conducted in Ghana, Africa
* Dataset involves thermal images and videos captured for palpable nodule locations of 125 patients participated in this study
* Repository includes groundtruth.xlsx, code and data folder

This work is licensed under a
[Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License][cc-by-nc-nd].

[![CC BY-NC-ND 4.0][cc-by-nc-nd-image]][cc-by-nc-nd]

[cc-by-nc-nd]: http://creativecommons.org/licenses/by-nc-nd/4.0/
[cc-by-nc-nd-image]: https://licensebuttons.net/l/by-nc-nd/4.0/88x31.png
[cc-by-nc-nd-shield]: https://img.shields.io/badge/License-CC%20BY--NC--ND%204.0-lightgrey.svg


**Groundtruth.xlsx:**
1. It includes following information:
    * Batch number of the patient
    * Patient ID
    * Location of nodule region i.e Trochanter, Sacrum, IIiacCrest, Knee, ChestWall etc
    * Side of nodule region: Left side, right side
    * Label: 0 - No alive female worm, 1 - Alive female worm
2. Batch B0 - B7 is used for training and validating the data while B8,B9,B10 belongs to prospective blind set.    

**Data Folder:**
1. It includes following folder directory structure:
    * Data/Patient ID/Locations/
2. Folder includes:
    * thermal video : side.avi
    * min max temp file for video : side_temp.csv
    * thermal image (csv file) : side.csv or side.npy
    * aligned thermal image to video files: side_aligned.npy
    * croppoints.crpt: nodule and roi region polygon croppoints
    * Here side is either "left" or "right"
3. thermal video is stored in grayscale format, to get actual temperature value - conversion code is provided in code folder.

**Code Folder:**
1. Sample code for converting video fram from grayscale format (0-255) to actual temperature value using min_max temperature file.
2. Sample code for nodule and roi segmentation from croppoints.crpt
3. Run notebook.ipynb to access the code


```python
%load_ext autoreload
%autoreload 2
from utils import *
import matplotlib.pyplot as plt
```

```python
filename = "C:/users/ronakdediya/Desktop/Onchocerciasis/PPT/Data/IM95C2/IIiacCrest/left"
grayScale, actualvideoTempFrame = getActualVideo(filename)          
plotData([grayScale[0],actualvideoTempFrame[0]],["GrayScale","Actual temp - First Video Frame"])
```


    
![png](Code/output_2_0.png)
    



```python
basepath = "C:/users/ronakdediya/Desktop/Onchocerciasis/PPT/Data/IM95C2/IIiacCrest/"
side = "left_1" ## Use "_1" as extension to your side for getting croppointsM

mask = getMaskFromCrpt(basepath,side)/255
plotData([mask,actualvideoTempFrame[0] + mask],["Mask","Mask overlayed on First Video Frame"])

noduleMask = getNodule(basepath,side)
plotData([noduleMask,actualvideoTempFrame[0] + noduleMask],["Nodule Mask","Mask overlayed on First Video Frame"])
```


    
![png](Code/output_3_0.png)
    



    
![png](Code/output_3_1.png)
    

