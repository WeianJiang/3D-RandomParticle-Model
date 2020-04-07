from abaqus import *
from abaqusConstants import *
from AbaqusFiles.ModelModule import MyModel

class LoadModule(MyModel):



    def _createAMP(self):
        mdb.models[MyModel._modelName].SmoothStepAmplitude(name='SmooothStepAMP', timeSpan=STEP, 
        data=((0.0, 0.0), (1.0, 1.0)))

    def _createBoundary(self):
        a = mdb.models[MyModel._modelName].rootAssembly
        f1 = a.instances['LoadingPlate-Low'].faces
        faces1 = f1.findAt(((0.5*MyModel._sectionLength, -20,0.5*MyModel._sectionLength), ))
        region = a.Set(faces=faces1, name='Set-Boundary')
        mdb.models[MyModel._modelName].DisplacementBC(name='BC-Boundary', 
            createStepName='Initial', region=region, u1=UNSET, u2=SET, u3=UNSET, 
            ur1=UNSET, ur2=UNSET, ur3=UNSET, amplitude=UNSET, distributionType=UNIFORM, 
            fieldName='', localCsys=None)

    def createLoad(self,load):

        self._createAMP()

        length=MyModel._sectionLength
        height=MyModel._sectionHeight
        a = mdb.models[MyModel._modelName].rootAssembly
        # r1 = a.referencePoints
        # refPoints1=(r1.findAt([length/2,height,length/2]),)
        # region = a.Set(referencePoints=refPoints1, name='Set-LoadPoint')
        region=a.sets['m_Set-Coupling']
        mdb.models[MyModel._modelName].DisplacementBC(name='BC-Load', 
            createStepName='Step-1', region=region, u1=UNSET, u2=load, u3=UNSET, 
            ur1=UNSET, ur2=UNSET, ur3=UNSET, amplitude='SmooothStepAMP', fixed=OFF, 
            distributionType=UNIFORM, fieldName='', localCsys=None)

        self._createBoundary()


    
