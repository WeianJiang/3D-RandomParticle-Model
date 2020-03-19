from abaqus import *
from abaqusConstants import *
from AbaqusFiles.ModelModule import MyModel


class PropertyModule(MyModel):

    def __init__(self,materialName):
        self._modelName=MyModel._modelName
        self._path=MyModel._path
        self._materialName=materialName
        mdb.models[self._modelName].Material(name=self._materialName)

    def setBasicInfo(self,elasticModules,possionRatio,density):
        thisMaterial=mdb.models[self._modelName].materials[self._materialName]
        thisMaterial.Elastic(table=((float(elasticModules), float(possionRatio)), ))
        thisMaterial.Density(table=((density, ), ))
        self._setCDPInfo()
        self._sectionCreate()
        #self._sectionAssign()

    def _sectionCreate(self):
        mdb.models[self._modelName].HomogeneousSolidSection(name='SecOf-'+str(self._materialName), 
            material=self._materialName, thickness=None)

    def _sectionAssign(self):
        partName='MeshPart'
        p = mdb.models[self._modelName].parts[partName]
        e = p.elements
        elements = e[800:801]
        region = p.Set(elements=elements, name='Set-2')
        p.SectionAssignment(region=region, sectionName='Section-1', offset=0.0, 
            offsetType=MIDDLE_SURFACE, offsetField='', 
            thicknessAssignment=FROM_SECTION)

    def _setCDPInfo(self):
        import numpy as np 
        loadPath='Constitution/'+str(self._path)
        Compress=np.loadtxt(loadPath+'/Compression.txt')
        Tensile=np.loadtxt(loadPath+'/Tension.txt')
        TensionDamage=np.loadtxt(loadPath+'/TensionDamage.txt')
        CompressionDamage=np.loadtxt(loadPath+'/CompressionDamage.txt')
        thisMaterial=mdb.models[self._modelName].materials[self._materialName]
        thisMaterial.ConcreteDamagedPlasticity(table=((
        38.0, 0.1, 1.16, 0.667, 0.0), ))
        thisMaterial.concreteDamagedPlasticity.ConcreteCompressionHardening(
        table=(Compress))
        thisMaterial.concreteDamagedPlasticity.ConcreteTensionStiffening(
        table=(Tensile),type=STRAIN)
        thisMaterial.concreteDamagedPlasticity.ConcreteTensionDamage(
        table=TensionDamage, type=STRAIN) 
        thisMaterial.concreteDamagedPlasticity.ConcreteCompressionDamage(
        table=CompressionDamage) 