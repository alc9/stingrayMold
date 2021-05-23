from skimage.filters import roberts
import skimage.measure as measure
import SimpleITK as sitk
import numpy as np
import matplotlib.pyplot as plt
import skan
import logging 
import networkx as nx

class CrossSectionProfile:
    """Profile takes a simpleITK image of stingray pectoral fin then performs operations to output a file defining the stingray fin profile

    :param sitkImage: binary array generated using StingraySlice() used for defining stingray fin profile
    :param sliceStride: stride between slices used during profiling 
    """

    def  __init__(self,sitkImage):
        self.sitkImageArray = sitk.GetArrayFromImage(sitkImage)
        self.profileArray = None
        self.centroid = None
        self.profileSkanGraph = None
        self.profileNxGraph = nx.Graph()

    def __pruneNxGraph(self):
        """Prune tree based on betweenness_centrality
        low centrality score 
        """
        print("placeholder")

    def __dumpSkanGraphToCSV(self):
        """Dumps points from skan graph to csv 
        """
        import csv
        with open('../points.csv',mode = 'w') as csvFile:
            writer = csv.writer(csvFile,delimiter = ',')
            for it in enumerate(self.profileSkanGraph,axis=0):
                writer.writerow([self.profileSkanGraph.path_coordinates(it)])

    def __convertSkanCSRToGraphx(self):
        """converts skan csr skeleton coordinates to nxgraph of coordinate points.
        """
        #used in array of int which are indices to subset
        #current node index is master
        masterNodeIdx = 0
        masterEdgeIdx = 0
        #length of list of segment end points
        nCoordinates = self.profileSkanGraph.coordinates.shape[0]
        nodes = np.full((nCoordinates),np.nan)
        for edgeIdx, path in enumerate(self.profileSkanGraph.paths_list()):
            srcPnt = path[0]
            dstPnt = path[-1]
            print(len(path))
            x = float(self.profileSkanGraph.coordinates[srcPnt,0])
            y = float(self.profileSkanGraph.coordinates[srcPnt,1])
            #if not nan and a valid node e.g >= 0
            if nodes[srcPnt] >= 0:
                srcNodeIdx = int(float(nodes[srcPnt]))
                #graph has additional edges
                self.profileNxGraph.add_edge(srcNodeIdx,masterEdgeIdx)
            else:
                #adding a new node
                srcNodeIdx = masterNodeIdx
                masterNodeIdx+=1
                #update nan entry with unique id
                nodes[srcPnt] = srcNodeIdx
                self.profileNxGraph.add_node(srcNodeIdx)
                self.profileNxGraph.add_edge(srcNodeIdx,masterEdgeIdx)
                #self.profileNxGraph.add_edge(srcNodeIdx,object=self.profileSkanGraph.path_coordinates(edgeIdx))
    def writeProfileToObj(self):
        """write profile
        """
        print(self.profileArray)

    def showProfile(self):
        fig,ax=plt.subplots()
        ax.imshow(self.profileArray)
        ax.grid()
        plt.show()

    def writeProfileToCSV(self):
        np.savetxt("../profileData.csv", self.profileArray, delimiter=",")

    def leastSquaresFit(self):
        """Minimize the sum of squares 
        """
        alpha = 5
        beta = 3 
        # https://stackoverflow.com/questions/47873759/how-to-fit-a-2d-ellipse-to-given-points
        print("placeholder")
    def airfoilSimilarity(self):
        """Determine the most similar airfoil to the stingray profile
        https://cs.stackexchange.com/questions/22781/similarity-between-two-geometric-shapes
        """
        print("placeholder")

    def mirrorProfile(self,RHS=True):
        #mirror shape to account for uneven profile
        #print(len(self.profileArray))
        if RHS:
            print(self.profileArray)
            flipped = np.fliplr(self.profileArray)[:,self.profileArray.size//2:]
            np.append(flipped,self.profileArray[:,self.profileArray.size//2:],axis=0)
            self.profileArray = flipped
            print(self.profileArray,"--------after--------")

    def showSkeleton(self):
        """Displays skan skeleton
        """
        print("placeholder")

    def showSlice(self,title=None,margin=0.05, dpi=80):
        nda = self.sitkImageArray
        spacing = img.GetSpacing() 
        if nda.ndim == 3:
            # fastest dim, either component or x
            c = nda.shape[-1]
        
         # the the number of components is 3 or 4 consider it an RGB image
            if not c in (3,4):
                nda = nda[:,:,0]
    
        elif nda.ndim == 4:
            c = nda.shape[-1]
        
            if not c in (3,4):
                raise Runtime("Unable to show 3D-vector Image")
            
        # take a z-slice
            nda = nda[:,:,:]
            
        ysize = nda.shape[0]
        xsize = nda.shape[1]
   
    
        # Make a figure big enough to accomodate an axis of xpixels by ypixels
        # as well as the ticklabels, etc...
        figsize = (1 + margin) * ysize / dpi, (1 + margin) * xsize / dpi

        fig = plt.figure(figsize=figsize, dpi=dpi)
        # Make the axis the right size...
        ax = fig.add_axes([margin, margin, 1 - 2*margin, 1 - 2*margin])
    
        extent = (0, xsize*spacing[1], ysize*spacing[0], 0)
    
        t = ax.imshow(nda,extent=extent,interpolation=None)
    
        if nda.ndim == 2:
            t.set_cmap("gray")
    
        if(title):
            plt.title(title)
        plt.show()
    def __removeCliques(self):
        """This function removes cliques from the graph.
        These are unwanted since we want a single route around
        the outline of the profile.
        """
        print("placeholder")

    def __removeSmallTerminalEdges(self):
        """This function removes small terminal 
        edges from the skan.csr graph in an initial pruning
        step
        """
        print("placeholder")

    def __dilateImage(self):
        """This function dilates the image to fill in gaps which occur
        after pruning
        """
        print("placeholder")

    def __set__(self):
        """sets profileArray
        """
        #X,Y=np.where(np.all(im==1,axis=2)) to get white pixels
        regionPropsStingray=measure.regionprops(self.sitkImageArray)
        if len(regionPropsStingray)==1:
            self.centroid = regionPropsStingray[0].centroid
            del(regionPropsStingray)
        self.profileArray = roberts(self.sitkImageArray)
        #get image spacing 
        imgspacing=sitk.ReadImage("/home/alex/projects/stingray/stingrayMold/images/segmentations/singleSliceUrobRHS.seg.nrrd")[0,:,:].GetSpacing()
        #get coordinate points and graph like structure
        self.profileSkanGraph=skan.csr.Skeleton(self.profileArray,spacing =imgspacing)
        #change datastructure to a more convenient structure
        self.__convertSkanCSRToGraphx()

        #print(self.profileGraph.n_paths)

img=sitk.ReadImage("/home/alex/projects/stingray/stingrayMold/images/segmentations/singleSliceUrobRHS.seg.nrrd")[0,:,:]
obj=CrossSectionProfile(img)
obj.__set__()
#obj.writeProfileToCSV()
#obj.mirrorProfile()
#obj.showProfile()
