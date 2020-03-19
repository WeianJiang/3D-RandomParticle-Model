from AbaqusFiles.ModelModule import MyModel
from AbaqusFiles.main_Initial import createModel
from AbaqusFiles.main_Part import PartModule
from AbaqusFiles.main_Property import PropertyModule
from AbaqusFiles import toolKit

class GridTopo(MyModel):

    def __init__(self):
        pass
    
    def setPath(self,Path,name='Default'):
        MyModel._path=Path
        MyModel._modelName='Model-'+str(name)
        createModel()

    def setSize(self,length,height):
        self._length=length
        self._height=height
    
    def setMeshSize(self,meshSize):
        self._meshSize=meshSize
        self._Part()
        toolKit.createSetAccordingToPart()

    def _Part(self):
        myPart=PartModule('Part-1')
        myPart.setSize(self._length,self._height)
        myPart.setMeshSize(self._meshSize)
    
    def _Property(self):
        Aggregate=PropertyModule('Aggregate')
        Aggregate.setBasicInfo(51246,0.3,2.7e-9)
        Matrix=PropertyModule('Matrix')
        Matrix.setBasicInfo(23000,0.2,2e-9)
        Interface=PropertyModule('Interface')
        Interface.setBasicInfo(12000,0.2,2e-9)


        


