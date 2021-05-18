Project: stingrayMold
Author: Alexander L Cunningham
Summary: create a printable mold based on a stingray ct-scan
Description: This folder contains a quick project which reads in an mhd file of a stingray finthen produces a step file mold of this profile allowing the fin to be 3D printed.To define thestep file you need to give the mhd file, the x,y,z dimensions of the implantrectangle you wishto print and the clearance x,y,z clearance between the implant rectangle and fin.
Directories: image -> .mhd files, objectFiles -> .xml objectFiles to generate mold without the
need to process image, pre-processing -> preprocessing of stingray image (get slice, anisotropic diffusion)
