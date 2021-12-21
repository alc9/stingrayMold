import skan
from skimage.util import invert
from scipy.ndimage import binary_fill_holes
from skimage import morphology
from skimage.measure import label,regionprops,find_contours
from skimage.transform import rotate
from sklearn.preprocessing import normalize
import SimpleITK as sitk
import cv2 as cv
import numpy as np
import matplotlib as mpl
import matplotlib.ticker
from matplotlib.ticker import FormatStrFormatter
from matplotlib import pyplot as plt
from symfit import parameters,variables,Fit
import pandas as pd
import re 
class Profile:
    """
    Takes in the segmentation sitkImage, orientated the image, generates array of
    positions for the outlines, fits shape to aerofoil equation
    :param sitkImage: binary image file name for slice of profile 
    """
    def  __init__(self,sitkImage,fname,rotate=True):
        #image array
        #N.B z,y,x
        self.fname=fname
        self.sitkImageArray = sitk.GetArrayFromImage(sitkImage)
        self.spacing=list(sitkImage.GetSpacing())[:-1]
        self.origin=list(sitkImage.GetOrigin())[:-1]
        self.sitkImageArray=np.squeeze(self.sitkImageArray,axis=0)
        #self.sitkImageArray=np.swapaxes(self.sitkImageArray,0,1)
        if rotate:
            self.sitkImageArray=np.rot90(self.sitkImageArray) 
        #array of from skan outline positions 
        self.profile = None
        #best fit results dict
        self.resultsDict = {}
        #original region properties
        self.regionProperties = None

    def showProfile(self):
        """show generated profile
        f = lambda x,pos: str(x).rstrip('0').rstrip('.')
        plt.rc('font', family='serif')
        plt.rc('xtick', labelsize='x-small')
        plt.rc('ytick', labelsize='x-small')
        plt.rc('legend', fontsize=10)    # legend fontsize
        """
        fig = plt.figure(figsize=(6, 5))
        ax = fig.add_subplot(1, 1, 1)
        #plt.margins(x=0.0001,y=0.003)
        ax.plot(self.profile["x"],self.profile["y"],'o',linestyle='None',marker="o",color="black")
        #plt.savefig("self.fname",dpi=300)
        plt.show()
    def showImage(self):
        """ shows sitk image"""
        plt.imshow(self.sitkImageArray,cmap=plt.cm.gray,interpolation='nearest')
        plt.show()
    
    def writeProfile(self):
        """write profileGraph to csv file 
        """
        import pandas as pd
        self.profile.to_csv("testingPositions.csv")
 
    def writeBestFit(self):
        """writes best fit equation
        """
        print("place holder")
    
    def orientateImageArray(self):
        """orientates fin 
        """
        #only one region, due to largest island algorithm 
        self.regionProperties = regionprops(self.sitkImageArray)[0]
        orientation=self.regionProperties.orientation
        orientationDegrees=orientation*(180/np.pi)+90
        self.regionProperties = regionprops(self.sitkImageArray)[0]
        self.sitkImageArray=rotate(self.sitkImageArray,-orientationDegrees,resize=False)
    def getSkanSkelCoords(self,skanSkel):
        skelCoordsList=[]
        for seg in range(skanSkel.n_paths):
            skelCoords = skanSkel.path_coordinates(seg)
            branchCoords=skelCoords[0]
            skelCoordsList.append(skelCoords)
        #return skelCoordsList

    def makeProfile(self,showRawSkel=True):
        """makes profile for fin using skan
        """
        kernel = np.ones((3,3),np.uint8)
        rawSkel=cv.morphologyEx(self.sitkImageArray,cv.MORPH_GRADIENT,kernel)
        rawSkel=cv.erode(np.float32(rawSkel),kernel,iterations=1).astype(bool)
        if showRawSkel:
            print("showing rawSkel")
            plt.imshow(rawSkel,cmap=plt.cm.gray)
            plt.show()
        (rows,cols)=np.where(rawSkel==True)
        # Initialize empty list of co-ordinates
        skel_coords = []
        # For each non-zero pixel...
        for (r,c) in zip(rows,cols):
            skel_coords.append((r,c))
        self.profile=pd.DataFrame(np.array(skel_coords),columns=["y","x"])
        #place zero position at centroid
        #np.where(self.regionProperties.centroid)
        self.profile["y"]=np.subtract(self.profile["y"],list(self.regionProperties.centroid)[0])
        #self.profile["x"]=np.subtract(self.profile["x"],list(self.regionProperties.centroid)[1])
        #scale data
        self.profile["y"]=np.divide(self.profile["y"],np.max(self.profile["y"]))
        self.profile["x"]=np.divide(self.profile["x"],np.max(self.profile["x"]))

    def fitShapeFourDigitSeries(self,showResult=False):
        """
        fits array of positions to aerofoil equation using symfit
        https://en.wikipedia.org/wiki/NACA_airfoil
        takes top of image and bottom then takes the best r from the two
        results
        """
        x , y = variables('x,y')
        t , r= parameters('t,r')
        filteredDf=self.profile[(self.profile[["y"]]>=0).all(1)]
        #cons=
        model={y: 5 * t * ( 0.2969 * (x**0.5) - 0.1260 * x - 0.3516 * (x**2) + 0.2843 * (x**3) - 0.1015 * (x**4))}
        fit=Fit(model,x=filteredDf["x"],y=filteredDf["y"])
        fitResult1=fit.execute()
        print(fitResult1)
        t=fitResult1.value(t)
        self.resultsDict.update({re.findall('[0-9]+',self.fname)[0]:{"t1":t}})
        if showResult:
            fig = plt.figure(figsize=(6, 5))
            ax = fig.add_subplot(1, 1, 1)
            x=filteredDf["x"]
            print(type(x))
            #pd.DataFrame(5 * t * (0.2969 * (x**0.5) - 0.1260 * x - 0.3516 *(x**2)+  0.2843 * (x**3) - 0.1015 * (x**4))).to_csv("approxData.csv")
            yt =  5 * t * (0.2969 * (x**0.5) - 0.1260 * x - 0.3516 *(x**2)+  0.2843 * (x**3) - 0.1015 * (x**4))
            ax.plot(x,yt,'o',linestyle='None',marker="o",color="black")
            ax.plot(x,filteredDf["y"],'o',color="red")
            plt.show()
        #process data for the half  
        filteredDf=self.profile[(self.profile[["y"]]<=0).all(1)]
        filteredDf["y"]=np.absolute(filteredDf["y"])
        x , y = variables('x,y')
        t , p = parameters('t,p')
        model={y: 5 * t * (0.2969 * x**0.5 - 0.1260 * x - 0.3516 * x**2 + 0.2843 * x**3 - 0.1015 * x**4)}
        fit=Fit(model,x=filteredDf["x"],y=filteredDf["y"])
        fitResult2=fit.execute()
        print(fitResult2)
        t=fitResult2.value(t)
        self.resultsDict[re.findall('[0-9]+',self.fname)[0]].update({"t2":t})
        if showResult:
            fig = plt.figure(figsize=(6, 5))
            ax = fig.add_subplot(1, 1, 1)
            x=filteredDf["x"]
            ax.plot(x,5 * t * 0.2969 * x**0.5 - 5 * t * 0.1260 * x - 5 * t * 0.3516 * x**2 + 5 * t * 0.2843 * x**3 - 5 * t * 0.1015 *x**4,'o',linestyle='None',marker="o",color="black")
            ax.plot(x,filteredDf["y"],'o',color="red")
            plt.show()


