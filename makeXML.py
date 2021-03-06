from make2FGLxml import *

class makeXML:
    
    def __init__(self, output, galactic, gti, iso, catalog, binned):
        self.output = output
        self.galactic = galactic
        self.gti = gti
        self.iso = iso
        self.catalog = catalog
        self.binned=binned

    def makeModel(self):
        mymodel = srcList(self.catalog,self.gti,self.output)
        if self.binned:
            mymodel.makeModel(self.galactic, self.galactic.replace(".fits",""), self.iso, self.iso.replace(".txt",""))
        else:
            mymodel.makeModel(self.galactic, self.galactic.replace(".fits",""), self.iso, self.iso.replace(".txt",""), psForce=1)

    
