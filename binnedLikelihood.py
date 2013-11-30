import pyLikelihood
from BinnedAnalysis import *
from bdlikeSED import *
from math import log10
import sys

firstSourceFit = 'crab_fit1_allSources.xml'
secondSourceFit = 'crab_fit2_allSources.xml'

#Reading the variable
#
variableArg=["spacecraftFile", "gtiFile", "ltcubeFile", "srcmapsFile", "expcubeFile", "ccubeFile", "bin", "energyMin", "energyMax", "sourceModel"]
variable={}
for t in range(0, len(variableArg)):
    
    variable[variableArg[t]]=sys.argv[t+1]


incremEnergy=float(log10(float(variable['energyMax']))-log10(float(variable['energyMin'])))/float(variable['bin'])

#Beginning of the main part
#

#obs=BinnedObs(variable['gtiFile'],variable['spacecraftFile'],expMap=variable['expmapFile'],expCube=variable['ltcubeFile'],irfs='P7SOURCE_V6')
obs = BinnedObs(variable['srcmapsFile'], variable['ltcubeFile'], variable['expcubeFile'], irfs='P7SOURCE_V6')

like1 = BinnedAnalysis(obs,variable['sourceModel'],optimizer='MINUIT')
#like1.tol = 0.01
#like1.setEnergyRange(100, 200)
#like1.fit(verbosity=1)
#like1.plot()
#like1.logLike.writeXml(firstSourceFit)
#print like1.model['CrabSync']
#print like1.model['CrabIC']
like2 = BinnedAnalysis(obs,firstSourceFit ,optimizer='NewMinuit')
#like2.tol = 0.01
#like2obj = pyLike.NewMinuit(like2.logLike)
#like2.fit(verbosity=1,covar=True,optObject=like2obj)
#like2.logLike.writeXml(secondSourceFit)

# Creating the bins in energy for the likelihood analysis
#
#

if float(variable['bin'])==9:
    print "Working on 9 energy bins"
    #inputs = bdlikeInput(like2,'_2FGLJ0534.5+2201',nbins=9, model=secondSourceFit)
    low_edges = [200.,427.69,914.61,1955.87,4182.56,8944.27,19127.05,40902.61]
    high_edges = [427.69,914.61,1955.87,4182.56,8944.27,19127.05,40902.61,187049.69]

else:
    print "Working on ", variable['bin'], " energy bins"
    low_edges=[]
    high_edges=[]
    energyLow=float(variable['energyMin'])
    
    while energyLow <= float(variable['energyMax']):
        energyUp = energyLow*(10**(incremEnergy))
        low_edges.append(float(energyLow))
        high_edges.append(float(energyUp))
        energyLow=energyUp
        print energyLow
     
print "Energy bins created: ", low_edges, high_edges
inputs = bdlikeInput(like2,variable['gtiFile'],variable['ccubeFile'], variable['spacecraftFile'], '_2FGLJ1555.7+1111', model=secondSourceFit, nbins=int(variable['bin']))


print "input object created"
inputs.customBins(low_edges,high_edges)
print "custom bin done"
inputs.fullFit(CoVar=True)
print "full fit done"
sed = bdlikeSED(inputs)
sed.getECent()
sed.fitBands()
sed.Plot()
