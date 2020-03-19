import numpy as np 



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

def _findNodeCoordinate(NodeNO):
    for Node in NodeData:
        if NodeNO==Node[0]:
            return Node#return [number,x,y,z]



sphereData=[]
sphereData=np.loadtxt('ModelInfoFiles/1/sphereData.txt')# 0 1 2 3=x y z r
NodeData=[]
NodeData=np.loadtxt('NodeData.txt')
ElementData=[]
ElementData=np.loadtxt('ElementData.txt')
eleNumber=len(ElementData)
sphereData=[]
MatrixSet=[]#the set containing the matrix
AggregateSet=[]
ITZSet=[]
for i in range(eleNumber):
    print i
    x_sum,y_sum,z_sum=0,0,0
    nodeNumber=8
    for j in range(1,9):
        node=ElementData[i][j]
        nodeCoordinate=_findNodeCoordinate(node)#return [number,x,y,z]
        x_sum+=nodeCoordinate[1]
        y_sum+=nodeCoordinate[2]
        z_sum+=nodeCoordinate[3]
    x_mean=x_sum/nodeNumber
    y_mean=y_sum/nodeNumber
    z_mean=z_sum/nodeNumber
    #for now you have got the gravity point of the elements
    #spheredata 0 1 2 3 for x y z radi
    result=_positionResult(x_mean,y_mean,z_mean,sphereData)
    if result=='Matrix':
        MatrixSet.append(ElementData[i][0])
    elif result=='Aggregate':
        AggregateSet.append(ElementData[i][0])
    elif result=='ITZ':
        ITZSet.append(ElementData[i][0])
np.savetxt('Matrix.txt',MatrixSet)
np.savetxt('Aggregate.txt',AggregateSet)
np.savetxt('ITZ.txt',ITZSet)

