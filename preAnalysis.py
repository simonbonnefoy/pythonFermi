from GtApp import GtApp
import pyLikelihood
from BinnedAnalysis import *
import os


class preAnalysis:
    """ Class to run the pre-analysis of the Fermi data
        generating all the files needed to run the binned likelihood"""
    
    def __init__(self, srcName, scfile, RA, DEC, ROI, EMIN, EMAX, EBIN, ZMAX,irfs, phaseMin, phaseMax):
        self.srcName=srcName
        #self.evfile=evfile
        self.scfile=scfile
        self.RA=RA
        self.DEC=DEC
        self.ROI=ROI
        self.EMIN=EMIN
        self.EMAX=EMAX
        self.EBIN=EBIN
        self.ZMAX=ZMAX
        self.irfs=irfs
        self.phaseMin=phaseMin
        self.phaseMax=phaseMax
        
        os.system("ls *_PH* > events.txt")
        
    def gtselect(self, phased, pulsarMode):
        if pulsarMode:
            if phased:
                phMin=self.phaseMin
                phMax=self.phaseMax
                outputFile = self.srcName+'_gti_'+self.phaseMin+'_'+self.phaseMax+'.fits'
                evfile=self.srcName+'_gti.fits'
                
            else:
                phMin=0 
                phMax=0
                evfile='@events.txt'
                outputFile = self.srcName+'_filtered.fits'
        else:
            outputFile = self.srcName+'_filtered.fits'
            evfile='@events.txt'
            phMin=0 
            phMax=0

        gtselect = GtApp('gtselect')
        gtselect.run(
            evclass=2,
            infile=evfile,
            outfile=outputFile,
            ra=self.RA,
            dec=self.DEC,
            rad=self.ROI,
            emin=self.EMIN,
            emax=self.EMAX,
            zmax=self.ZMAX,
            phasemin=phMin, 
            phasemax=phMax,
            tmin='0',
            tmax='0')
    
    def gtmktime(self, pulsarMode):
        
        if pulsarMode:
            outputFile=self.srcName+'_filtered.fits'
        else:
            outputFile = self.srcName+'_gti_'+self.phaseMin+'_'+self.phaseMax+'.fits'

        gtmktime = GtApp('gtmktime')
        gtmktime.run(
            scfile=self.scfile,
            evfile=self.srcName+'_filtered.fits',
            outfile=outputFile,
            filter='DATA_QUAL==1 && LAT_CONFIG==1 && ABS(ROCK_ANGLE)<52',
            roicut='yes')

    def gtpphase(self, ephemeris, srcName, pulsarMode):
        if pulsarMode:
            gtpphase = GtApp('gtpphase')
            gtpphase.run(
                chatter='4',
                evfile=self.srcName+'_gti.fits',
                scfile=self.scfile,
                psrdbfile=ephemeris,
                psrname=srcName,
                ephstyle='DB',
                solareph='JPL DE200')
            
        
    def gtbin(self, algth):
        gtbin = GtApp('gtbin')
        
        if algth=="CMAP":
            gtbin.run(
                evfile=self.srcName+'_gti_'+self.phaseMin+'_'+self.phaseMax+'.fits',
                outfile=self.srcName+'_cmap_'+self.phaseMax+'_'+self.phaseMin+'.fits',
                algorithm=algth,
                scfile=self.scfile,
                nxpix='300',
                nypix='300',
                binsz='0.2',
                coordsys ='CEL',
                xref=self.RA,
                yref=self.DEC,
                axisrot='0',
                proj='STG')
            
        elif algth=="CCUBE":
            gtbin.run(
                evfile=self.srcName+'_gti_'+self.phaseMin+'_'+self.phaseMax+'.fits',
                outfile=self.srcName+'_ccube_'+self.phaseMin+'_'+self.phaseMax+'.fits',
                algorithm=algth,
                scfile=self.scfile,
                nxpix='200',
                nypix='200',
                binsz='0.2',
                coordsys ='CEL',
                xref=self.RA,
                yref=self.DEC,
                axisrot='0',
                proj='STG',
                ebinalg='LOG',
                emin=self.EMIN,
                emax=self.EMAX,
                enumbins=self.EBIN)

    def gtltcube(self):
        gtltcube = GtApp('gtltcube')
        gtltcube.run(
            evfile =self.srcName+'_gti_'+self.phaseMin+'_'+self.phaseMax+'.fits',
            scfile =self.scfile,
            outfile =self.srcName+'_ltcube_'+self.phaseMin+'_'+self.phaseMax+'.fits',
            dcostheta = '0.025',
            binsz = '1')
        
       
        
    def gtexpcube2(self,mode):
        gtexpcube2 = GtApp('gtexpcube2')
        if mode=='_expcube_':
            nx=400
            ny=400
        elif mode=='_allsky_':
            nx=1800
            ny=900
        
        gtexpcube2.run(
            infile=self.srcName+'_ltcube_'+self.phaseMin+'_'+self.phaseMax+'.fits',
            outfile=self.srcName+mode+self.phaseMin+'_'+self.phaseMax+'.fits',
            cmap='none',
            irfs=self.irfs,
            nxpix=nx,
            nypix=ny,
            binsz='0.2',
            coordsys ='CEL',
            xref=self.RA,
            yref=self.DEC,
            axisrot='0',
            proj='AIT',
            emin=self.EMIN,
            emax=self.EMAX,
            enumbins=self.EBIN)

    def gtsrcmaps(self, model):
        gtsrcmaps = GtApp('gtsrcmaps')
        gtsrcmaps.run(
            scfile=self.scfile,
            expcube=self.srcName+'_ltcube_'+self.phaseMin+'_'+self.phaseMax+'.fits',
            cmap=self.srcName+'_ccube_'+self.phaseMin+'_'+self.phaseMax+'.fits',
            srcmdl=model,
            bexpmap=self.srcName+'_allsky_'+self.phaseMin+'_'+self.phaseMax+'.fits',
            outfile=self.srcName+'_scrmap_'+self.phaseMin+'_'+self.phaseMax+'.fits',
            irfs=self.irfs,
            chatter='4',
            emapbnds="no")
    
       
