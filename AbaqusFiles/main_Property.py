from abaqus import *
from abaqusConstants import *
from AbaqusFiles.ModelModule import MyModel
import numpy as np 
import copy
import regionToolset

class PropertyModule(MyModel):

    def __init__(self,materialName):
        self._modelName=MyModel._modelName
        self._path=MyModel._path
        self._materialName=materialName
        

    def setBasicInfo(self,elasticModules,possionRatio,density):

        loadPath='Constitution/'+str(self._path)
        ElasticData=np.loadtxt(loadPath+'/'+self._materialName+'Elastic.txt')
        #E_SF=np.loadtxt(loadPath+'/'+self._materialName+'ElasticScaleFactor.txt')
        E_SF=np.ones(1000)
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


    def _setCDPInfo(self):

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

            Temp_Compress=copy.deepcopy(Compress)
            Temp_Tensile=copy.deepcopy(Tensile)
            Temp_TensionDamage=copy.deepcopy(TensionDamage)
            Temp_CompressionDamage=copy.deepcopy(CompressionDamage)

            Temp_Compress=Compress*CDP_SF[random]
            Temp_Tensile=Tensile*CDP_SF[random]

            Temp_TensionDamage[:,1]=TensionDamage[:,1]*CDP_SF[random]
            Temp_CompressionDamage[:,1]=CompressionDamage[:,1]*CDP_SF[random]
            
            thisMaterial.concreteDamagedPlasticity.ConcreteCompressionHardening(
            table=(Temp_Compress))
            thisMaterial.concreteDamagedPlasticity.ConcreteTensionStiffening(
            table=(Temp_Tensile),type=STRAIN)
            thisMaterial.concreteDamagedPlasticity.ConcreteTensionDamage(
            table=Temp_TensionDamage, type=STRAIN) 
            thisMaterial.concreteDamagedPlasticity.ConcreteCompressionDamage(
            table=Temp_CompressionDamage) 


    def _cal(self,crackStrain,Stress,damageFactor,elasticScaleFactor=1):
        return crackStrain-(damageFactor/(1-damageFactor))*(Stress/(23000*elasticScaleFactor))

def positionDetermine(x,y,z,xcentroid,ycentroid,zcentroid,radi):
    xdistance=abs(x-xcentroid)
    ydistance=abs(y-ycentroid)
    zdistance=abs(z-zcentroid)
    distance=np.sqrt(xdistance**2+ydistance**2+zdistance**2)
    thickness=0.1*radi
    if distance>radi:
        return 'OutSide'
    elif distance<radi and distance>radi-thickness:
        return 'OnBorder'
    else:
        return 'InSide'


def positionResult(xmean,ymean,zmean,sphereData=[]):
    insider,outsider,border=0,0,0
    sphereNum=len(sphereData)
    for sphere in sphereData:
        result=positionDetermine(xmean,ymean,zmean,sphere[0],sphere[1],sphere[2],sphere[3])
        if result=='InSide':
            insider+=1
        elif result=='OutSide':
            outsider+=1
        else:
            border+=1
    if insider>=1:
        return 'Aggregate'
    elif border>=1:
        return 'ITZ'
    elif outsider==sphereNum:
        return 'Matrix'


def sectionAssign():
    modelName=MyModel._modelName
    path=MyModel._path
    partName='MeshPart'

    sphereData=[]
    sphereData=np.loadtxt('ModelInfoFiles/'+str(path)+'/sphereData.txt')# 0 1 2 3=x y z r
    p = mdb.models[modelName].parts[partName]
    elements=p.elements
    eleNum=len(elements)
    for i in range(eleNum):
        x_sum,y_sum,z_sum=0,0,0
        nodeNumber=8
        for j in range(0,8):
            nodes=elements[i].getNodes()
            nodeCoordinate=nodes[j].coordinates
            x_sum+=nodeCoordinate[0]
            y_sum+=nodeCoordinate[1]
            z_sum+=nodeCoordinate[2]
        x_mean=x_sum/nodeNumber
        y_mean=y_sum/nodeNumber
        z_mean=z_sum/nodeNumber
        #for now you have got the gravity point of the elements
        #spheredata 0 1 2 3 for x y z radi
        result=positionResult(x_mean,y_mean,z_mean,sphereData)
        if result=='Matrix':
            region = regionToolset.Region(elements=elements[i:i+1])
            p.SectionAssignment(region=region, sectionName='SecOf-'+'Matrix-'+str(np.random.randint(0,1000)), offset=0.0, 
            offsetType=MIDDLE_SURFACE, offsetField='', 
            thicknessAssignment=FROM_SECTION)
        elif result=='Aggregate':
            region = regionToolset.Region(elements=elements[i:i+1])
            p.SectionAssignment(region=region, sectionName='SecOf-'+'Aggregate-'+str(np.random.randint(0,1000)), offset=0.0, 
            offsetType=MIDDLE_SURFACE, offsetField='', 
            thicknessAssignment=FROM_SECTION)
        elif result=='ITZ':
            region = regionToolset.Region(elements=elements[i:i+1])
            p.SectionAssignment(region=region, sectionName='SecOf-'+'Interface-'+str(np.random.randint(0,1000)), offset=0.0, 
            offsetType=MIDDLE_SURFACE, offsetField='', 
            thicknessAssignment=FROM_SECTION)


    