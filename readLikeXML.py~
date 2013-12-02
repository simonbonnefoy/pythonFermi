def header(model):
    fileWrite = open(str(model),'w')
    fileWrite.write('<?xml version="1.0" ?>\n')
    fileWrite.write('<source_library title="source library">\n')
    fileWrite.write('<!-- Point Sources -->\n')
    fileWrite.close()

def tail(model):
    fileWrite = open(str(model),'a')
    fileWrite.write('</source_library>')

def countLine(model):
    file = open(model,'r')
    eof="default"
    line=0
    while eof != "":
        eof = file.readline()
        line = line +1
    return line

def modelOut(src,pivot):
    return str(src)+"_model_BinnedPL_"+str(pivot)+"_GeV.xml"

#################################################################
#
#      Beginning of the class to create the tuned source model
#
#################################################################

class readLikeXML:

    def __init__(self, pivot, srcName, srcFermiName, model, fl):
        self.pivot=pivot
        self.SIF=srcFermiName
        self.SI=srcName
        self.model=model
        self.factorLimit=fl
        #self.p1=p1
        #self.p2=p2
        #self.d1=d1

    
    def fillSIBinnedPL(self):
        """filling the xml file for the source of interest
        The binned power law creates a power law with index -2 to make a fit in each energy band.
        The pivot energy is the energy where will be plotted the spectral point"""
        
        model = modelOut(self.SI, self.pivot)
        header(model)
        nbline=countLine(self.model)
        flagSource=0
        flagSpatial=0
        fileWrite = open(str(model),'a')
        sourceInterest = self.SI
        fileRead = open(self.model,'r')
        i=0
        while i<nbline+1:
            line = fileRead.readline()
                       
            if self.SIF in line: #check s
                flagSource=1
                
            if flagSource ==1 and flagSpatial==0 and not "parameter" in line:
                if "spectrum type" in line and flagSource==1:
                    fileWrite.write("<spectrum type=\"PowerLaw\"> \n")
                else:
                    fileWrite.write(line)
                

            if flagSource ==1 and flagSpatial==0 and "parameter" in line:
                fileWrite.write("\t \t<parameter free=\"1\" max=\"1e6\" min=\"1e-6\" name=\"Prefactor\" scale=\"1e-13\" value=\"1\"/>\n")
                fileWrite.write("\t \t<parameter free=\"0\" max=\"5.0\" min=\"-5.0\" name=\"Index\" scale=\"1.0\" value=\"-2\"/>\n")
                scale = "\t \t<parameter free=\"0\" max=\"5e5\" min=\"30\" name=\"Scale\" scale=\"1.0\" value=\""+str(self.pivot)+"\"/>\n"
                fileWrite.write(scale)
                fileWrite.write(" </spectrum> \n")
                flagSpatial=1
           
            if "<spatialModel" in line and flagSpatial==1 :
                flagSpatial=2
               
            if flagSource ==1 and flagSpatial==2:
                fileWrite.write(line)
                if "</source>" in line :
                    fileRead.close()
                    break
           
            i+=1
           
    def fillBkgSrc(self):
        """Filling the source model file with the background sources"""

        model = modelOut(self.SI, self.pivot)
        fileWrite = open(str(model),'a')
        nbline=countLine(self.model)
        flagSource=0
        i=0
        fileRead = open(self.model,'r')
        scale=0
        bufferModel=""
      
        while i<nbline+1:
            
            line = fileRead.readline()

            if "<source name" in line and not self.SIF in line:
                sourceLine = line
                flagSource=1
                bufferModel=""
                scale=10
                
            #if "iso" in line:       ## the isotropic model has not scale factor. Need to set scale to 1 for iso to be written
            #    scale = 1
                
            if "Prefactor" in line:
                start=line.find('scale=\"')+7
                stop=line.find(' value=', start)-1
                #scale = float(line[start:stop])

            
            if flagSource ==1:
                bufferModel+=line
                                
            if "</source>" in line and flagSource==1 :
                flagSource=0

                if scale >= self.factorLimit:
                    fileWrite.write(bufferModel)
                
            i = i+1

        fileRead.close() 
        fileWrite.close()
        tail(model)
       
        


#    def fillDiffBkgSrc(self):
#        """Filling the source model file with the diffuses sources.
#        Usually, two sources are taken into account."""
#
#        model = modelOut(self.pivot)
#
#        fileWrite = open(str(model),'a')
#        diffuseSources=["gal_2yearp7v6_v0", "iso_p7v6source"]
#        nbline=countLine()
#        flagSource=0
#        fileWrite.write('<!-- Diffuse Sources --> \n')
#        for source in diffuseSources:
#            #print source
#            i=0
#            fileRead = open('crab_model_3sources.xml','r')
#            
#            while i<nbline+1:
#                line = fileRead.readline()
#                if source in line:
#                    flagSource=1
#                    
#                if flagSource ==1:
#                    #print line
#                    fileWrite.write(line)
#                    if "</source>" in line and flagSource==1 :
#                        flagSource=0
#
#                i = i+1
#            fileRead.close() 
#        fileWrite.write('</source_library>')
#        fileWrite.close()
#
    def modelOut(self, src, pivot):
        return str(src)+"_model_BinnedPL_"+str(pivot)+"_GeV.xml"
