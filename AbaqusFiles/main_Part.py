from abaqus import *
from abaqusConstants import *
from ModelModule import MyModel



class PartModule(MyModel):

    def __init__(self,partName):
        self._modelName=MyModel._modelName
        self._partName=partName

    def setSize(self,Length,Height):
        self._length=Length
        self._height=Height
        self._createPart()
    
    def setMeshSize(self,meshSize):
        self._meshSize=meshSize
        self._createMeshPart()


    def _createPart(self):
        s = mdb.models[self._modelName].ConstrainedSketch(name='__profile__', 
            sheetSize=200.0)
        g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
        s.setPrimaryObject(option=STANDALONE)
        s.rectangle(point1=(0.0, 0.0), point2=(self._length, self._height))
        p = mdb.models[self._modelName].Part(name=self._partName, dimensionality=THREE_D, 
            type=DEFORMABLE_BODY)
        p = mdb.models[self._modelName].parts[self._partName]
        p.BaseSolidExtrude(sketch=s, depth=self._length)
        s.unsetPrimaryObject()
        p = mdb.models[self._modelName].parts[self._partName]
        del mdb.models[self._modelName].sketches['__profile__']
    
    def _createMeshPart(self):
        p = mdb.models[self._modelName].parts[self._partName]
        p.seedPart(size=self._meshSize, deviationFactor=0.1, minSizeFactor=0.1)
        p.generateMesh()
        p.PartFromMesh(name='MeshPart', copySets=True)