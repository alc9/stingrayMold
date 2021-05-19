import skan
import SimpleITK as sitk
import numpy as np
class Profile:
    """
    Profile takes a simpleITK image of stingray pectoral fin then performs operations to output an xml defining the stingray fin profile

    :param sitkImage: binary array generated using StingraySlice() used for defining stingray fin profile
    :param sliceStride: stride between slices used during profiling 
    """
    def  __init__(self,sitkImage,sliceStride=1):
        self.sitkImageArray = sitk.GetArrayFromImage(sitkImage)
        self.sliceStride = sliceStride
        self.profileGraph = None

    def showProfile(self):
        """show generated profile
        """
        print("place holder")
    
    def writeProfile(self):
        """write profileGraph to an xml
        """
        print("place holder")

    def __set__(self):
        """sets profileGraph
        """
        print("profile graph")
