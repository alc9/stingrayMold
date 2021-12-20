from FinProfile import *
import SimpleITK as sitk
fileName = "../processedImages/seg05ThreshIslandSmooth.seg.nrrd"
sitkImageArray05=sitk.ReadImage(fileName)
img05Profile=Profile(sitkImageArray05,fileName)
del(sitkImageArray05)
img05Profile.orientateImageArray()
img05Profile.makeProfile(showRawSkel=True)
img05Profile.showProfile()
#img05Profile.writeProfile()
