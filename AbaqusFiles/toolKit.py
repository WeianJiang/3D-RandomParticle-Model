from abaqus import *
from abaqusConstants import *
from AbaqusFiles.ModelModule import MyModel
import numpy as np 

modelName=MyModel._modelName
path=MyModel._path
partName='MeshPart'

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
        return 'ITZ'
    elif outsider==sphereNum:
        return 'Matrix'
        

def createSetAccordingToPart():
    loadpath='ModelInfoFiles/'+str(path)
    sphereData=[]
    MatrixSet=[]#the set containing the matrix
    AggregateSet=[]
    ITZSet=[]
    sphereData=np.loadtxt(loadpath+'/'+'sphereData.txt')
    elements=mdb.models[modelName].parts[partName].elements
    eleNumber=len(elements)
    for i in range(eleNumber):
        nodes=elements[i].getNodes()
        x_sum,y_sum,z_sum=0,0,0
        nodeNumber=len(nodes)
        for node in nodes:
            x_sum+=node.coordinates[0]
            y_sum+=node.coordinates[1]
            z_sum+=node.coordinates[2]
        x_mean=x_sum/nodeNumber
        y_mean=y_sum/nodeNumber
        z_mean=z_sum/nodeNumber
        #for now you have got the gravity point of the elements
        #spheredata 0 1 2 3 for x y z radi
        result=_positionResult(x_mean,y_mean,z_mean,sphereData)
        if result=='Matrix':
            if len(MatrixSet)==0:# A very clever step, 2020.03.17
                MatrixSet=elements[i:i+1]
            else:
                MatrixSet=MatrixSet+elements[i:i+1]
        elif result=='Aggregate':
            if len(AggregateSet)==0:
                AggregateSet=elements[i:i+1]
            else:
                AggregateSet=elements[i:i+1]+AggregateSet
        elif result=='ITZ':
            if len(ITZSet)==0:
                ITZSet=elements[i:i+1]
            else:
                ITZSet=elements[i:i+1]+ITZSet
    p = mdb.models[modelName].parts[partName]
    p.Set(elements=MatrixSet, name='MatrixSet')
    p.Set(elements=AggregateSet,name='AggregateSet')
    p.Set(elements=ITZSet,name='ITZSet')
    