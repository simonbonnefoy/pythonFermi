import pyLikelihood
from UnbinnedAnalysis import *
from likeSED import *
from math import log10
import sys


class fermiUnbinnedAnalysis:
    """ Class computing the binned likelihood analysis of Fermi data"""
  

    def __init__(self, src, srcFermi, scFile, gtiFile, ltcubeFile, expmapFile, irfs, EBIN, EMIN, EMAX, model):
        self.src=src
        self.srcFermi = srcFermi
        self.scFile=scFile
        self.gtiFile=gtiFile
        self.ltcubeFile=ltcubeFile
        self.expmapFile=expmapFile
        self.irfs=irfs
        self.EBIN=EBIN
        self.EMIN=EMIN
        self.EMAX=EMAX
        self.model=model

        global obs 
        obs = UnbinnedObs(self.gtiFile, self.scFile, self.expmapFile, self.ltcubeFile)


    def unBinnedlikeFit1(self, optmz, emin, emax, plot, write, analysisType):
        """Computing a first likelihood fit."""
        
      #  global obs 
      #  obs = UnbinnedObs(self.gtiFile, self.scFile, expMap=self.expmapFile, expCube=self.ltcubeFile, irfs=self.irfs)        
        like1 = UnbinnedAnalysis(obs,self.model,optimizer=optmz)
        like1.tol = 0.1
#        like1.setEnergyRange(emin, emax)
        like1.fit(verbosity=1)
        
        if plot:
            like1.plot()
        if write:
            like1.logLike.writeXml(str(self.src)+"_model_likehoodFit1.xml")
        
#        if analysisType == 1:
#            preFactor = like1.model[str(self.srcFermi)].funcs['Spectrum'].getParam('Prefactor').value()
#            print like1.model[str(self.srcFermi)]
#            return preFactor
      

    def unBinnedlikeFit2(self, optmz, write):
        """ Computig a second likelihood fit needed to compute the SED"""
       
        global like2 
        like2 = UnbinnedAnalysis(obs,str(self.src)+"_model_likehoodFit1.xml" ,optimizer=optmz)
        like2.tol = 1e-8
        like2obj = pyLike.NewMinuit(like2.logLike)
        like2.fit(verbosity=1,covar=True,optObject=like2obj)

        if write:
            like2.logLike.writeXml(str(self.src)+"_model_likehoodFit2.xml")



    def unBinnedSED(self):
        """Computing the custom bin and the final SED"""

        low_edges=[]
        high_edges=[]

        if self.EBIN==9:
            print "Working on 9 energy bins"

            low_edges = [200.,427.69,914.61,1955.87,4182.56,8944.27,19127.05,40902.61]
            high_edges = [427.69,914.61,1955.87,4182.56,8944.27,19127.05,40902.61,187049.69]
            
        else:
            print "Working on ", self.EBIN, " energy bins"
           
            energyLow=float(self.EMIN)
            incremEnergy=(log10(self.EMAX)-log10(self.EMIN))/self.EBIN

            while energyLow < float(self.EMAX):
                energyUp = energyLow*(10**(incremEnergy))
                low_edges.append(float(energyLow))
                high_edges.append(float(energyUp))
                energyLow=energyUp
                
   # print "Energy bins created: ", low_edges, high_edges

  #  inputs = likeInput(like2, self.srcFermi, nbins=self.EBIN, model=str(self.src)+"_model_likehoodFit2.xml")
  #  
  #  inputs.customBins(low_edges,high_edges)
  #  inputs.fullFit(CoVar=True)
  #  sed = bdlikeSED(inputs)
  #  sed.getECent()
  #  sed.fitBands()
  #  sed.Plot()
