import numpy as np
import sys
import cadquery as cq
from cadquery import Wire,Face,cqgi
import pandas as pd
from math import sin,cos,pi,floor
"""
#locate FreeCAD
FREECADPATH = '/snap/freecad/22/opt/local/FreeCAD-0.19/lib/FreeCAD.so'
FREECADPARTPATH = '/snap/freecad/22/opt/local/FreeCAD-0.19/lib/Part.so'
LIBPYTHON3_5_1_0='/snap/freecad/19/usr/lib/x86_84-linux-gnu/libpython3.5m.so.1.0'
sys.path.append(FREECADPATH)
sys.path.append(FREECADPARTPATH)
sys.path.append(LIBPYTHON3_5_1_0)
try:
    import FreeCAD
    import Part
except ValueError:
    raise("failed to import freecad libs")
"""
class CADMoldObject:
    """Generated CAD of stingray fin then takes the negative to produce a mold"""
    def __init__(self,fittedEqn,fittedParamsDict):
        if fittedEqn==4:
            self.fittedEqn = fittedEqn
            self.t=fittedParamsDict["t1"]
            self.airfoilDf=None
        else:
            raise Exception("{}-digit series NACA airfoil not implemented".format(fittedEqn))
    def setFin(self):
        """this function generates the cad for the fin"""
        #create airfoil profile
        x = np.linspace(0,1,1000)
        if self.fittedEqn==4:
            yt =np.multiply(5*self.t,np.multiply(0.2969,np.sqrt(x))-np.multiply(0.126,x)-np.multiply(0.3516,np.power(x,2))+np.multiply(0.2843,np.power(x,3))-np.multiply(0.105,np.power(x,4)))
            #generate yt coordinates
            self.airfoilDf=pd.DataFrame({"x":x,"yt":yt})
        lineListTop=[]
        lineListBottom=[]
        """
        for index,row in self.airfoilDf.iterrows():
            if index==len(self.airfoilDf)-1:
               break
            xcoord=row["x"].item()
            ycoord=row["yt"].item()
            xcoordNext=self.airfoilDf["x"].index[index+1]
            ycoordNext=self.airfoilDf["yt"].index[index+1]
            firstPoint=cq.Vector(xcoord,ycoord,0.0)
            secondPoint=cq.Vector(xcoordNext,ycoordNext,0.0)
            lineListTop.append(cq.Edge.makeLine(firstPoint,secondPoint))
            #repeat for mirror
            firstPoint=cq.Vector(xcoord,-1*ycoord,0.0)
            secondPoint=cq.Vector(xcoordNext,-1*ycoordNext,0.0)
            lineListBottom.append(cq.Edge.makeLine(firstPoint,secondPoint))
        #use list of edges to create a wire (collection of edges that are connected together)
        airfoilWireTop=Wire.assembleEdges(lineListTop)
        airfoilWireBottom=Wire.assembleEdges(lineListBottom)
        #create face as ruled surface from set of edges that enclose a surface
        airfoilSection=Face.makeRuledSurface(airfoilWireTop,airfoilWireBottom)
        #create planform using bspline
        """
        #draw line for fin to follow
        #loft shape
        # https://stackoverflow.com/questions/61186339/how-to-iteratively-loft-wires-in-cadquery
        # https://cadquery.readthedocs.io/en/latest/assy.html
        surf = cq.Workplane().parametricSurface(lambda u, v: (u, v, 5 * sin(pi*u / 10) * cos(pi * v / 10)),True,N=40,start=0,stop=20)
        p=[]
        for index,row in self.airfoilDf.iterrows():
            p.append((row["x"].item(),row["yt"].item()))
        r = cq.Workplane("front")
        r = r.pushPoints(p)
        result=r.extrude(0.125)
        result.save("testing.step")
    def setMold(self):
        """this function generates the mold for the fin geometry"""
        print("not implemented yet")
    
    def writeCoords(self,fname):
        """this function writes fin coords"""
        self.airfoilDf.to_csv(fname)
    def writeFin(self):
        """this function writes the stingray fin"""
        print("not implemented yet")

    def writeMold(self):
        """this function writes the stingray mold"""
        print("not implemented yet")

    def showFinCAD(self):
        """this function shows the stingray fin CAD model"""
        print("not implemented yet")

    def showMoldCAD(self):
        """this function shows the stingray fin mold CAD model"""
        print("not implemented yet")
