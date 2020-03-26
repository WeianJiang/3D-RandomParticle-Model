from abaqus import *
from abaqusConstants import *
from AbaqusFiles.ModelModule import MyModel

class LoadModule(MyModel):



    def _createAMP(self):
        mdb.models[MyModel._modelName].SmoothStepAmplitude(name='SmooothStepAMP', timeSpan=STEP, 
        data=((0.0, 0.0), (1.0, 1.0)))

    def createLoad(self,load):

        self._createAMP()

        length=MyModel._sectionLength
        height=MyModel._sectionHeight
        a = mdb.models[MyModel._modelName].rootAssembly
        r1 = a.referencePoints
        refPoints1=(r1.findAt([length/2,height,length/2]),)
        region = a.Set(referencePoints=refPoints1, name='Set-6')
        mdb.models[MyModel._modelName].DisplacementBC(name='BC-Load', 
            createStepName='Step-1', region=region, u1=UNSET, u2=load, u3=UNSET, 
            ur1=UNSET, ur2=UNSET, ur3=UNSET, amplitude='SmooothStepAMP', fixed=OFF, 
            distributionType=UNIFORM, fieldName='', localCsys=None)