from abaqus import *
from abaqusConstants import *
from AbaqusFiles.ModelModule import MyModel


class PropertyModule(MyModel):

    def __init__(self,materialName):
        self._modelName=MyModel._modelName
        self._path=MyModel._path
        self._materialName=materialName
        

    def setBasicInfo(self,elasticModules,possionRatio,density):

        loadPath='Constitution/'+str(self._path)
        ElasticData=np.loadtxt(loadPath+'/'+self._materialName+'Elastic.txt')
        E_SF=np.loadtxt(loadPath+'/'+self._materialName+'ElasticScaleFactor.txt')

        SampleSize=len(E_SF)
        randomPick=np.random.randint(0,SampleSize,SampleSize)

        for i in range(len(ElasticData)):

            materialName=self._materialName+'-'+str(i)
            random=randomPick[i]

            mdb.models[self._modelName].Material(name=materialName)
            thisMaterial=mdb.models[self._modelName].materials[materialName]
            thisMaterial.Elastic(table=((float(elasticModules*E_SF[random]), float(possionRatio)), ))
            thisMaterial.Density(table=((density, ), ))

            self._sectionCreate(materialName)

        if self._materialName=='Matrix':
            self._setCDPInfo()
        elif self._materialName=='Interface':
            self._setCDPInfo()


    def _sectionCreate(self,materialName):
        mdb.models[self._modelName].HomogeneousSolidSection(name='SecOf-'+str(materialName), 
            material=materialName, thickness=None)

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

        CDP_SF=np.loadtxt(loadPath+'/'+self._materialName+'CDPScaleFactor.txt')
        SampleSize=len(CDP_SF)
        randomPick=np.random.randint(0,SampleSize,SampleSize)
        for i in range(SampleSize):
            
            materialName=self._materialName+'-'+str(i)
            thisMaterial=mdb.models[self._modelName].materials[materialName]
            thisMaterial.ConcreteDamagedPlasticity(table=((
            38.0, 0.1, 1.16, 0.667, 0.0), ))

            random=randomPick[i]
            Compress[0]=Compress[0]*CDP_SF[random]
            Tensile[0]=Tensile[0]*CDP_SF[random]
            TensionDamage[0]=TensionDamage[0]*CDP_SF[random]
            CompressionDamage[0]=CompressionDamage[0]*CDP_SF[random]
            
            thisMaterial.concreteDamagedPlasticity.ConcreteCompressionHardening(
            table=(Compress))
            thisMaterial.concreteDamagedPlasticity.ConcreteTensionStiffening(
            table=(Tensile),type=STRAIN)
            thisMaterial.concreteDamagedPlasticity.ConcreteTensionDamage(
            table=TensionDamage, type=STRAIN) 
            thisMaterial.concreteDamagedPlasticity.ConcreteCompressionDamage(
            table=CompressionDamage) 
