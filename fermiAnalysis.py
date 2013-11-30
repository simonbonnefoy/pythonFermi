from preAnalysis import *
from fermiBinnedLike import *
from fermiUnbinnedLike import *
from readLikeXML import *
from math import sqrt
import ROOT
import os.path
from makeXML import *
from array import *



##############################
#
#  Input of the parameters
#
##############################

######## Analysis mode ############

analysisType=1                        # Set the analysis type you want:
                                      #
                                      # 1 -> Binned likelihood, with power law, spectral index=2 fit in each energy band
                                      # 2 -> Binned likelihood, Minuit + NewMinuit fit, SED using pytools
                                      # 3 -> Unbinned likelihood

runPreAna = 0                         # Set to 1 if you need to (re)create the gtselect, gtmktime... files

######## Source parameters ########

srcName="geminga"                       # Source name
srcNameFermi="2FGLJ0633.9+1746"         # Source name in the Fermi catalog. 
PSRNAME="none"                          # If you run pulsar analysis, the name of the pulsar in the ephemeris database
#RA=238.929583                          # Right ascension
#DEC=11.19                              # Declination
RA=98.47855
DEC=17.7739
####### Analysis parameters ######

ROI=20                                 # Region of interest
EMIN=100                               # Energy min
EMAX=100000                            # Energy max
EBIN=20                                # Bin in energy
ZMAX=100                               # Zenithal angle cut, usually 100 as suggested by Fermi
PHASEMIN='0.00'                        # Phase min, for pulsar analysis
PHASEMAX='1.00'                        # Phase max, for pulsar analysis
pulsarMode=0                           # Set to 1 if you want to run a pulsar analysed; phased events
factorLimit=1e-12                      # Limit on the prefactor of the sources taken into account for the model

######### File input #########

evfile="@events.txt"
scfile="L131120074440D49FF56C86_SC00.fits"
EPHEMERIS='none'                            # Set 'none' if you are not running pulsar analysis
IRFS='P7SOURCE_V6'
model='geminga_model_3sources.xml'
#model='geminga_test.xml'
galactic="gal_2yearp7v6_v0.fits"
catalog="gll_psc_v07.fit"
iso="iso_p7v6source.txt"



###############################################
#
#    Running the pre-analysis of Fermi data
#
###############################################


def preAnalysisBinned():
    preAn = preAnalysis(srcName, scfile, RA, DEC, ROI, EMIN, EMAX, EBIN, ZMAX, IRFS,PHASEMIN, PHASEMAX)
    
    preAn.gtselect(0, pulsarMode)
    preAn.gtmktime(pulsarMode)

    if pulsarMode:
        preAn.gtpphase("crab_ephemeris_good.fits", PSRNAME, pulsarMode)
        preAn.gtselect(1, pulsarMode)
    
    preAn.gtbin("CMAP")
    preAn.gtbin("CCUBE")
    preAn.gtltcube()
    preAn.gtexpcube2('_expcube_')
    preAn.gtexpcube2('_allsky_')
        
    if not os.path.isfile("./"+str(model)):
        print "==== Making the source model from the Fermi catalog ===="
        make = makeXML(model, galactic,  srcName+'_gti_'+PHASEMIN+'_'+PHASEMAX+'.fits', iso, catalog, 1)
        make.makeModel()
        
    else:
        print "==== Model existing, we skip this step ===="
            
   
    preAn.gtsrcmaps(model)

def preAnalysisUnbinned():
    preAn = preAnalysis(srcName, scfile, RA, DEC, ROI, EMIN, EMAX, EBIN, ZMAX, IRFS,PHASEMIN, PHASEMAX)
    
    preAn.gtselect(0, pulsarMode)
    preAn.gtmktime(pulsarMode)

    if pulsarMode:
        preAn.gtpphase("crab_ephemeris_good.fits", PSRNAME, pulsarMode)
        preAn.gtselect(1, pulsarMode)
            
    preAn.gtltcube()
    preAn.gtexpmap()

    if not os.path.isfile("./"+str(model)):
        print "==== Making the source model from the Fermi catalog ===="
        make = makeXML(model, galactic,  srcName+'_gti_'+PHASEMIN+'_'+PHASEMAX+'.fits', iso, catalog, 1)
        make.makeModel()
        
    else:
        print "==== Model existing, we skip this step ===="


#########################################
#
#   Running the likelihood analysis
#
#########################################
            
            
def likelihoodFit1(analysisType):


    if analysisType==1 :
        
        incremEnergy=(log10(EMAX)-log10(EMIN))/EBIN
        energyLow=EMIN
        energy=array("f",[])
        flux=array("f",[])
        E2=array("f",[])
        exl=array("f",[])
        exh=array("f",[])
        eyl=array("f",[])
        eyh=array("f",[])
        
        while energyLow < EMAX:
            energyUp = energyLow*(10**(incremEnergy))
            pivot = sqrt(energyLow*energyUp)
            print "Computing the fit between", energyLow, " and ", energyUp, " GeV; pivot = ", pivot
            
            
            
            
        # Creating the model for the several sources
            
            like=readLikeXML(pivot,srcName, srcNameFermi, model, factorLimit)
            like.fillSIBinnedPL()
            like.fillBkgSrc()
            
            modelBinnedPW = like.modelOut(srcName, pivot)
            
            binAn=fermiBinnedAnalysis(srcName, "_"+srcNameFermi, scfile, srcName+'_gti_'+PHASEMIN+'_'+PHASEMAX+'.fits', \
                                          srcName+'_ltcube_'+PHASEMIN+'_'+PHASEMAX+'.fits',  \
                                          srcName+'_srcmap_'+PHASEMIN+'_'+PHASEMAX+'.fits',   \
                                          srcName+'_expcube_'+PHASEMIN+'_'+PHASEMAX+'.fits', \
                                          srcName+'_ccube_'+PHASEMIN+'_'+PHASEMAX+'.fits',   \
                                          IRFS, EBIN, EMIN, EMAX, modelBinnedPW)
            
            preFactor, error, ts = binAn.likelihood1('MINUIT', energyLow, energyUp,0 ,0, analysisType)
            

            if ts >= 20:                         # As in MAGIC, the spectral points are plotted if the significance is > 2.
                
                energy.append(pivot*(10**(-3))) # -> convert energy from MeV to GeV
                flux.append(preFactor*(10**-13))
                print "Prefactor", preFactor
                E2.append(pivot*pivot*preFactor*(10**-19)) # -> convert flux from MeV to ergs
                #E2.append(pivot*pivot*preFactor*(10**-19)) # -> convert flux from ergs to TeV


                ## Computing error bars ##
                ##
                print "TSSSSSSSSS", sqrt(ts)
                exl.append((pivot-energyLow)*(10**(-3)))
                exh.append((energyUp-pivot)*(10**(-3)))
                print "ERROR: ", error
                eyl.append(pivot*pivot*(error)*(10**-19)/1.6)
                eyh.append(pivot*pivot*(error)*(10**-19)/1.6)
            
            energyLow = energyUp
            
            
            
        SED = TGraphAsymmErrors(len(exl), energy, E2, exl, exh, eyl, eyh)
        SED.GetXaxis().SetTitle("Energy [GeV]")
        SED.GetYaxis().SetTitle("E^{2}*\frac{dN}/{dAdtdE}")
        SED.SetMarkerStyle(21)
        SED.Draw("AP")
        
        fileOutput = str(srcName)+"_"+str(EBIN)+"bins_"+str(EMIN)+"_"+str(EMAX)+"GeV_SED.root"
        SED.SaveAs(fileOutput)
        
    if analysisType==2:
        
#        like=readLikeXML(200,srcName, srcNameFermi, model, factorLimit)
#        like.fillSIBinnedPL()
#        like.fillBkgSrc()
#        
#        modelBinnedPW = like.modelOut(srcName, pivot)
#
        binAn=fermiBinnedAnalysis(srcName, "_"+srcNameFermi, scfile, srcName+'_gti_'+PHASEMIN+'_'+PHASEMAX+'.fits', \
                                      srcName+'_ltcube_'+PHASEMIN+'_'+PHASEMAX+'.fits',  \
                                      srcName+'_srcmap_'+PHASEMIN+'_'+PHASEMAX+'.fits',   \
                                      srcName+'_expcube_'+PHASEMIN+'_'+PHASEMAX+'.fits', \
                                      srcName+'_ccube_'+PHASEMIN+'_'+PHASEMAX+'.fits',   \
                                      IRFS, EBIN, EMIN, EMAX, model)

        binAn.likelihood1('MINUIT', EMIN, EMAX,0 ,1, analysisType)
        binAn.likelihood2('NewMinuit', 1)
        binAn.SED()


def unbinnedLike():
    unbinAn = fermiUnbinnedAnalysis(srcName, "_"+srcNameFermi, scfile, srcName+'_gti_'+PHASEMIN+'_'+PHASEMAX+'.fits', \
                                        srcName+'_ltcube_'+PHASEMIN+'_'+PHASEMAX+'.fits',  \
                                        srcName+'_expmap_'+PHASEMIN+'_'+PHASEMAX+'.fits', \
                                        IRFS, EBIN, EMIN, EMAX, model)

    unbinAn.unBinnedlikeFit1('DRMNFB', EMIN, EMAX, 0, 1, 0)
    unbinAn.unBinnedlikeFit2('MINUIT', 1)
    unbinAn.unBinnedSED()

###########################################################################################
#
#           Running the analysis according to the analysis type set in the parameters 
#
###########################################################################################


if analysisType == 1:
    
    print "Running binned likelihood analysis"
    print "Each energy band will be fitted by an index 2 power law"

    if runPreAna:
        preAnalysisBinned()

    likelihoodFit1(analysisType)

if analysisType == 2:
     print "Running binned likelihood analysis"
     print "Two likelihood fits will be done, SED will be created by pytools"

     if runPreAna:
         preAnalysisBinned()
     
     likelihoodFit1(analysisType)

if analysisType == 3:
    print "Running unbinned likelihood analysis"
    print "Two likelihood fits will be done, SED will be created by pytools"

    if runPreAna:
        preAnalysisUnbinned()

    unbinnedLike()

