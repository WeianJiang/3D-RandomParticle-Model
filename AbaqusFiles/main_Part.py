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
    
    def setMeshSize(self,meshSize,meshtype='HEX'):
        self._meshSize=meshSize
        self._meshtype=meshtype
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
        if self._meshtype=='HEX':
            p = mdb.models[self._modelName].parts[self._partName]
            p.seedPart(size=self._meshSize, deviationFactor=0.1, minSizeFactor=0.1)
            p.generateMesh()
            p.PartFromMesh(name='MeshPart', copySets=True)
        elif self._meshtype=='TRI':
            p = mdb.models[MyModel._modelName].parts[self._partName]
            p.seedPart(size=self._meshSize, deviationFactor=0.1, minSizeFactor=0.1)
            c = p.cells
            pickedRegions = c.getSequenceFromMask(mask=('[#1 ]', ), )
            p.setMeshControls(regions=pickedRegions, elemShape=TET, technique=FREE)
            elemType1 = mesh.ElemType(elemCode=UNKNOWN_HEX, elemLibrary=EXPLICIT)
            elemType2 = mesh.ElemType(elemCode=UNKNOWN_WEDGE, elemLibrary=EXPLICIT)
            elemType3 = mesh.ElemType(elemCode=C3D10M, elemLibrary=EXPLICIT)
            cells = c.getSequenceFromMask(mask=('[#1 ]', ), )
            pickedRegions =(cells, )
            p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2, 
                elemType3))
            p.generateMesh()
            p.PartFromMesh(name='MeshPart', copySets=True)

        
        
    
