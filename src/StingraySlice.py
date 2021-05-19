#Name: getStingraySlice
#Description: get stingray slice from ct scan 
#Author: Alex Cunningham
#Sources: 
#https://stackoverflow.com/questions/22161088/how-to-extract-a-file-within-a-folder-within-a-zip
# https://vedo.embl.es/autodocs/_modules/vedo/plotter.html
# https://github.com/dgobbi/VTK/blob/master/Examples/ImageProcessing/Python/ImageInteractorReslice.py
import SimpleITK as sitk
import tempfile
import os
from vedo import volume,show
from vedo.applications import Slicer2d,SlicerPlotter
import vtk

class StingraySlice():
    """
    StingraySlice contains methods for stingray ct scan IO and processing. Final objectiv
    is to produce a segmentation file for use by Profile class
    """
    def  __init__(self,copy=False):
        """Initialize stingray slice class
        Parameters: copy(bool): if true a copy of the original is kept wih name sitkImageCopy
        """
        self.fin=str()
        self.sitkImage=None
        self.cropCentre=tuple()
        self.imageType=None
        self.copy=copy
        if copy is False:
            self.sitkImageCopy=None
        else:
            self.sitkImageCopy=self.sitkImage

    def  __set__(self,fin: str):
        """Set stingray slice
        Parameters:
        fin (str): Filename for .mhd ct scan
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
        """Crop ct-scan 
        Parameters:
        cropSize (tuple): crop size (3,2) with ((x1,y1,z1),(x2,y2,z2)) where x bounds are xcentre-x1:xcentre+x2
        """
        self.sitkImage=self.sitkImage[self.cropCentre[0]-self.cropSize[0][0]:self.cropCentre[0]+self.cropSize[0][1],
        self.cropCentre[1]-self.cropSize[1][0]:self.cropCentre[1]+self.cropSize[1][1],
        self.cropCentre[2]-self.cropSize[2][0]:self.cropCentre[2]+self.cropSize[2][1]]
        if self.sitkImage.GetSize()==0:
            print("crop out of bounds, user is prompted to __set__ object")
            return
        self.sitkImage=sitk.GradientAnisotropicDiffusion(self.sitkImage)
    def showImage2DSlice(self):
        """Shows render of ct scan image
        """
        Slicer2d(volume.Volume(os.listdir(self.fin)))
    def showImage3D(self):
        """
        show 3D render of binary image array
        TODO: function not tested yet!
        """
        binaryImageArray = sitk.GetArrayFromImage(self.sitkImage)
        vol = Volume(binaryImageArray)
        vol.addScalarBar3D()
        text1 = Text2D('Segmentation Volume',c='blue')
        show((vol,text1)],N=2,azimuth=10)
    def selectSeed(self):
        """Select seed from ct scan
        """
        #TODO: select using 3dslice
        def clickSeed(key):
            """taken from vedo/examples/basic/keypress.py
            """
            global clickedSeeds
            clickedSeeds=[]
            mesh = vp.clickedActor
            if not mesh or key != "c":
                printc("click a mesh and press c.", c="r")
                printc("press 'esc' to exit.", c="r")
                return
            printc("clicked mesh    :", mesh.filename[-40:], c=4)
            printc("clicked 3D point:", mesh.picked3d, c=4)
            printc("clicked renderer:", [vp.renderer], c=2)
            clickedSeed.append(mesh.picked3d)
        vp = SlicerPlotter()
        numpyArrayImage=sitk.GetArrayFromImage(self.sitkImage).astype(np.uint8).T
        vp.keyPressFunction = clickSeed
    def thresholdImage(self,threshold=(-29,150) ,view=False):
        """Thresholds image and then updates self.sitkImage.
        Parameters:
        threshold in HU, and view boolean for visualization
        Returns:
        """
        #otsu threshold range based on -29HU to +150HU 
        #https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4309522/
        #otsuFilter = sitk.OtsuThresholdImageFilter()
        #otsuFilter.SetInsideValue(0)
        #otsuFilder.SetOutsideValue(1)
        #seg = otsuFilter.Execute(sitk.Image)
        self.selectSeed()
        self.sitkImage=sitk.ConnectedThreshold(self.sitkImage,[clickedSeed],lower=threshold[0],upper=threshold[1]) 
    def __get__(self)->sitk.Image:
        """Get stingray sitkImage
        Parameters:
        Returnsm
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
                    if zipRef.namelist()[0].find("/")!=-1:
                        insideDir=zipRef.namelist()[0]
                        self.fin=tmpDir+"/insideDir/"
                    else:
                        self.fin=tmpDir
                    zipRef.extractall(path=tmpDir)
            elif self.imageType == ".gz":
                import tarfile
                tmpDir=tempfile.gettempdir()
                with tarfile.TarFile(self.fin,'r') as tarRef:
                    if tarRef.namelist()[0].has("/"):
                        insideDir=tarRef.namelist()[0]
                        self.fin=tmpDir+"/insideRef/"
                    else:
                        self.fin=tmpDir
                    tarRef.extractall(path=tmpDir)
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
print("running...")
myStingray = StingraySlice()
myStingray.__set__("/home/alex/projects/stingrayMold/images/ctStingray.zip")
print(myStingray.GetSize())
