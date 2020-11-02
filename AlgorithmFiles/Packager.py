'''
This python file aims to introduce multi-thread processing into material assignment in MaterialModule. Since the single thread processing is too slow for material assignment.
'''

import thread 
import regionToolset
from abaqus import *
from abaqusConstants import *
from AbaqusFiles.ModelModule import MyModel
import numpy as np 


class PackagerModule(MyModel):
    
    def __init__(self,dividedPackage):
        self.dividedPackage=dividedPackage
   

    
    def _threadWork(self,threadName,startNum,endNum):
        modelName=MyModel._modelName
        partName='MeshPart'
        p = mdb.models[modelName].parts[partName]
        print "%s starts" % threadName
        for i in range(startNum,endNum):
            nodes=self.elements[i].getNodes()
            MatrixCounter=0
            InterfaceCounter=0
            AggregateCounter=0
            Finalresult=''
            nodeNum=len(nodes)

            for node in nodes:
                x_coordinate=node.coordinates[0]
                y_coordinate=node.coordinates[1]
                z_coordinate=node.coordinates[2]
                result=_positionResult(x_coordinate,y_coordinate,z_coordinate,self.sphereData)
                if result=='Matrix':
                    MatrixCounter+=1
                elif result=='Interface':
                    InterfaceCounter+=1
                elif result=='Aggregate':
                    AggregateCounter+=1

            if MatrixCounter==nodeNum:
                Finalresult='Matrix'
            elif AggregateCounter==nodeNum:
                Finalresult='Aggregate'
            else:
                Finalresult='Interface'

            if Finalresult=='Matrix':
                region = regionToolset.Region(elements=self.elements[i:i+1])
                p.SectionAssignment(region=region, sectionName='SecOf-'+'Matrix-'+str(np.random.randint(0,1000)), offset=0.0, 
                offsetType=MIDDLE_SURFACE, offsetField='', 
                thicknessAssignment=FROM_SECTION)
                if len(self.MatrixSet)==0:
                    self.MatrixSet=self.elements[i:i+1]
                else:
                    self.MatrixSet=self.MatrixSet+self.elements[i:i+1]

            elif Finalresult=='Aggregate':
                region = regionToolset.Region(elements=self.elements[i:i+1])
                p.SectionAssignment(region=region, sectionName='SecOf-'+'Aggregate-'+str(np.random.randint(0,1000)), offset=0.0, 
                offsetType=MIDDLE_SURFACE, offsetField='', 
                thicknessAssignment=FROM_SECTION)
                if len(self.AggregateSet)==0:
                    self.AggregateSet=self.elements[i:i+1]
                else:
                    self.AggregateSet=self.AggregateSet+self.elements[i:i+1]

            elif Finalresult=='Interface':
                region = regionToolset.Region(elements=self.elements[i:i+1])
                p.SectionAssignment(region=region, sectionName='SecOf-'+'Interface-'+str(np.random.randint(0,1000)), offset=0.0, 
                offsetType=MIDDLE_SURFACE, offsetField='', 
                thicknessAssignment=FROM_SECTION)
                if len(self.InterfaceSet)==0:
                    self.InterfaceSet=self.elements[i:i+1]
                else:
                    self.InterfaceSet=self.InterfaceSet+self.elements[i:i+1]
        
        print "%s finished" % threadName
    



    def assignRandomSection(self):

        self.MatrixSet=[]
        self.InterfaceSet=[]
        self.AggregateSet=[]
        modelName=MyModel._modelName
        path=MyModel._path
        partName='MeshPart'
        p = mdb.models[modelName].parts[partName]
        self.sphereData=[]
        self.sphereData=np.loadtxt('ModelInfoFiles/'+str(path)+'/sphereData.txt')# 0 1 2 3=x y z r
        self.elements=p.elements
        eleNum=len(self.elements)

        #eachPackageNumber=eleNum/self.dividedPackage

        try:
            thread.start_new_thread(self._threadWork,('Package_1',0,eleNum/2))
            thread.start_new_thread(self._threadWork,('Package_2',eleNum/2,eleNum))
        except:
            print "Error starting new thread"
        # #the first step, determine the node positions
        # nodes=p.nodes
        # nodePosition=[]
        # for i in range(len(nodes)):
        #     x_coordinate=nodes[i][0]
        #     y_coordinate=nodes[i][1]
        #     z_coordinate=nodes[i][2]
        #     result=positionResult(x_coordinate,y_coordinate,z_coordinate,sphereData)
        #     nodePosition.append([i,result])
        # #got the node NO and its position results
        
        #the following program, is to determine the element position by the node number.

        try:
            p.Set(elements=self.MatrixSet, name='Matrix-Set') 
        except:
            pass
        try:
            p.Set(elements=self.AggregateSet, name='Aggregate-Set')
        except:
            pass
        try:
            p.Set(elements=self.InterfaceSet, name='Interface-Set')
        except:
            pass


def _positionDetermine(x,y,z,xcentroid,ycentroid,zcentroid,radi):
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


def _positionResult(xmean,ymean,zmean,sphereData=[]):
    insider,outsider,border=0,0,0
    sphereNum=len(sphereData)
    for sphere in sphereData:
        result=_positionDetermine(xmean,ymean,zmean,sphere[0],sphere[1],sphere[2],sphere[3])
        if result=='InSide':
            insider+=1
        elif result=='OutSide':
            outsider+=1
        else:
            border+=1
    if insider>=1:
        return 'Aggregate'
    elif border>=1:
        return 'Interface'
    elif outsider==sphereNum:
        return 'Matrix'
