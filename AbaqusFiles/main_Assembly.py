from abaqus import *
from abaqusConstants import *
from AbaqusFiles.ModelModule import MyModel



class AssemblyModule(MyModel):

    def createInstance(self):
        a = mdb.models[MyModel._modelName].rootAssembly
        a.DatumCsysByDefault(CARTESIAN)
        p = mdb.models[MyModel._modelName].parts['MeshPart']
        a.Instance(name='MeshPart-1', part=p, dependent=ON)
    
    # def createReferencePoint(self,x,y,z):
    #     a = mdb.models[MyModel._modelName].rootAssembly
    #     a.ReferencePoint(point=(x, y, z))