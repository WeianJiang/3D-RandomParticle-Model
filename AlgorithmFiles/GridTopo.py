from AbaqusFiles.ModelModule import MyModel
from AbaqusFiles.main_Initial import createModel
from AbaqusFiles.main_Part import PartModule
from AbaqusFiles.main_Property import PropertyModule
from AbaqusFiles.main_Property import sectionAssign
from AbaqusFiles.main_Step import StepModule
from AbaqusFiles.main_Assembly import AssemblyModule
from AbaqusFiles.main_Interaction import InteractionModule
from AbaqusFiles.main_Load import LoadModule
from AbaqusFiles.main_Job import JobMoudle
from AbaqusFiles import toolKit

class GridTopo(MyModel):

    def __init__(self):
        pass

    def _setImportFile(self,CircleFileName='sphereData.txt'):
        self.circleData = np.loadtxt('ModelInfoFiles/'+str(MyModel._path)+'/'+CircleFileName)
        MyModel._circleNum=len(self.circleData)    
    
    def setPath(self,Path,name='Default'):
        MyModel._path=Path
        MyModel._modelName='Model-'+str(name)
        createModel()

    def setSize(self,length,height):
        self._length=length
        self._height=height
        MyModel._sectionHeight=height
        MyModel._sectionLength=length
    
    def setMeshSize(self,meshSize):

        self._meshSize=meshSize
        #toolKit.createSetAccordingToPart()


    def setLoad(self,load):

        self._load=load

        self._Part()
        self._Property()
        self._Assembly()
        self._Step()
        self._Interaction()
        self._Load()
        self._Job()

    def _Part(self):
        myPart=PartModule('Part-1')
        myPart.setSize(self._length,self._height)
        myPart.setMeshSize(self._meshSize)
    
    def _Property(self):

        Aggregate=PropertyModule('Aggregate')
        Aggregate.materialCreate(51246,0.3,2.7e-9)
        
        Interface=PropertyModule('Interface')
        Interface.materialCreate(2.56E+04,0.2,2e-9)

        Matrix=PropertyModule('Matrix')
        Matrix.materialCreate(3.29E+04,0.2,2e-9)



    def _Assembly(self):

        myAssembly=AssemblyModule()
        myAssembly.createInstance()
        # myAssembly.createReferencePoint(self._length/2,self._height,self._length/2)
        
    def _Step(self):

        myStep=StepModule()
        myStep.createStep()

    def _Interaction(self):
        
        interaction1=InteractionModule()
        interaction1.setCoupling()


    def _Load(self):

        load1=LoadModule()
        load1.createLoad(self._load)

    def _Job(self):

        job1=JobMoudle('Job-'+MyModel._modelName)
        job1.createJob(2)

