#Name: getStingraySlice
#Description: get stingray slice from ct scan 
#Author: Alex Cunningham
#TODO https://stackoverflow.com/questions/22161088/how-to-extract-a-file-within-a-folder-within-a-zip
import SimpleITK as sitk
import tempfile
import os
#SlicerPlotter,Slicer2d
from vedo import volume
from vedo.applications import Slicer2d
import vtk
#from vedo.applications import SlicerPlotter
# https://github.com/dgobbi/VTK/blob/master/Examples/ImageProcessing/Python/ImageInteractorReslice.py
class StingraySlice():
    def  __init__(self,copy=False):
        """Initialize stingray slice class
        Parameters: copy(bool): if true a copy of the original is kept wih name sitkImageCopy
        """
        self.fin=str()
        self.sitkImage=None
        self.cropCentre=tuple()
        self.imageType=None
        self.copy=copy
        if copy is True:
            self.sitkImageCopy=None

    def  __set__(self,fin: str):
        """Set stingray slice
        Parameters:
        fin (str): Filename for .mhd ct scan
        fout(str): Output filename for ct scan
        cropSize(tuple): Size to crop ct scan with shape (3,2)
        Returns:
        None: Only sets class variable
        """
        self.fin=fin
        passedCheckFin,statusString=self.__checkFin()
        if passedCheckFin is False:
            raise ValueError("File {0} {1}".format(fin,statusString))
        if self.imageType == ".mhd":
            self.sitkImage=sitk.ReadImage(fin[1])
        else:
            self.sitkImage=self.__readDicomStack()
        imageSize_=self.sitkImage.GetSize()
        self.cropCentre=(imageSize_[0],imageSize_[1],imageSize_[2])
        if self.copy is True:
            self.sitkImageCopy=sitkImage

    def cropImage(self,cropSize: tuple):
        self.sitkImage=self.sitkImage[self.cropCentre[0]-self.cropSize[0][0]:self.cropCentre[0]+self.cropSize[0][1],
        self.cropCentre[1]-self.cropSize[1][0]:self.cropCentre[1]+self.cropSize[1][1],
        self.cropCentre[2]-self.cropSize[2][0]:self.cropCentre[2]+self.cropSize[2][1]]
        self.sitkImage=sitk.GradientAnisotropicDiffusion(self.sitkImage)
    def showImage2DSlice(self):
        """
        Shows render of ct scan image
        """
        Slicer2d(volume.Volume(os.listdir(self.fin)))
        

    def thresholdImage(self,threshold,view=False):
        """Thresholds image and then updates self.sitkImage.
        Parameters:
        threshold in HU, and view boolean for visualization
        Returns:
        """
        otsuFilter = sitk.OtsuThresholdImageFilter()
        #otsuFilter.SetInsideValue(0)
        #otsuFilder.SetOutsideValue(1)
        #seg = otsuFilter.Executre(sitk.Image)
        #sitk.ConnectedThreshold() 
    def __get__(self)->sitk.Image:
        """Get stingray sitkImage
        Parameters:
        Returns:
        sitk.image: simpleITK image 
        """
        return self.sitkImage

    def __checkFin(self)->(bool,str):
        """Check the file in 
        Parameters:
        Returns:
        (bool,str): status of input check and status string 
        """
        from pathlib import Path
        finPath = Path(self.fin)
        if not finPath.is_file() and not finPath.is_dir():
            return(False,"is not a real path")
        if not finPath.is_dir():
            self.imageType=os.path.splitext(self.fin)[1]
            if self.imageType == ".mhd":
                return(True, "")
            if self.imageType == ".dcm":
                return(True,"")
            if self.imageType == ".zip":
                import zipfile
                tmpDir=tempfile.gettempdir()
                with zipfile.ZipFile(self.fin,'r') as zipRef:
                    if zipRef.namelist()[0].has("/"):
                        insideDir=zipRef.namelist()[0]
                        self.fin=tmpDir+"/insideDir/"
                    else:
                        self.fin=tmpDir
                    zipRef.extractall(self.fin,tmpDir)
            elif self.imageType == ".gz":
                import tarfile
                tmpDir=tempfile.gettempdir()
                with tarfile.TarFile(self.fin,'r') as tarRef:
                    if tarRef.namelist()[0].has("/"):
                        insideDir=tarRef.namelist()[0]
                        self.fin=tmpDir+"/insideRef/"
                    else:
                        self.fin=tmpDir
                    tarRef.extractall(self.fin,tmpDir)
            else:
                return(False,"file type {0} not supported".format(self.imageType)) 
        else:
            fileNames=os.list.dir(fin)
            self.imageType=os.path.splitext(fileNames[0])[0]
            if self.imageType == ".dcm" and len(fileNames)>1:
                self.imageType=".dcmdir"
                return(True,"")
            if self.imageType == ".mhd":
                return(True, "")
            if self.imageType == ".dcm":
                return(True,"")
            else:
                return(False, "file type {0} not supported".format(self.imageType)) 

    def __readDicomStack(self)->sitk.Image:
        """Reads in a dicom stack folder
        Parameters:
        Returns:
        sitk.image: stingray image
        """
        reader=sitk.ImageSeriesReader()
        dicomNames = reader.GetGDCMSeriesFileNames(self.fin)
        reader.SetFileNames(dicomNames)
        return reader.Execute()

#if __name__ ==' __main__':

