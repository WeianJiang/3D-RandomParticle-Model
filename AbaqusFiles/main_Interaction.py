from abaqus import *
from abaqusConstants import *
from AbaqusFiles.ModelModule import MyModel


class InteractionModule(MyModel):

    def setCoupling(self):
        length=MyModel._sectionLength
        height=MyModel._sectionHeight
        a = mdb.models[MyModel._modelName].rootAssembly
        r1 = a.referencePoints
        refPoints1=(r1.findAt([length/2,height,length/2]),)
        region1=a.Set(referencePoints=refPoints1, name='m_Set-Coupling')

        nodeSet=[]
        n1=a.instances['MeshPart-1'].nodes
        for i in range (len(n1)):
            nodeCoordinates=n1[i].coordinates
            y_coordinate=nodeCoordinates[1]
            if y_coordinate==height:
                if len(nodeSet)==0:
                    nodeSet=n1[i:i+1]
                else:
                    nodeSet=nodeSet+n1[i:i+1]
        region2=a.Set(nodes=nodeSet, name='s_Set-Coupling')
        mdb.models[MyModel._modelName].Coupling(name='Constraint-1', controlPoint=region1, 
        surface=region2, influenceRadius=WHOLE_SURFACE, couplingType=KINEMATIC, 
        localCsys=None, u1=ON, u2=ON, u3=ON, ur1=ON, ur2=ON, ur3=ON)

