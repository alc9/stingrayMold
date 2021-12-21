from FinProfile import *
from CADMold import *  
import SimpleITK as sitk
relative="../processedImages/"
fileNames=["{}seg0ThresFillIslandSmooth.seg.nrrd".format(relative),"{}seg01ThreshIslandFillSmooth.seg.nrrd".format(relative),"{}seg02ThreshIslandSmooth.seg.nrrd".format(relative),"{}seg03ThreshFillIslandSmooth.seg.nrrd".format(relative),"{}seg04ThreshIslandSmooth.seg.nrrd".format(relative),"{}seg05ThreshIslandSmooth.seg.nrrd".format(relative),"{}seg06ThreshIslandSmooth.seg.nrrd".format(relative),"{}seg07ThreshIslandSmooth.seg.nrrd".format(relative)]
resultList=[]
for fileName in fileNames:
    sitkImageArray05=sitk.ReadImage(fileName)
    img05Profile=Profile(sitkImageArray05,fileName)
    del(sitkImageArray05)
    img05Profile.orientateImageArray()
    img05Profile.makeProfile(showRawSkel=False)
    #img05Profile.showProfile()
    #img05Profile.writeProfile()
    img05Profile.fitShapeFourDigitSeries(showResult=False)
    resultList.append(img05Profile.resultsDict)
print(resultList[3])
cad05=CADMoldObject(4,resultList[3]["03"])
cad05.setFin()

