import numpy as np 


def ITZGenerator():
    outerSphereData=[]
    innerSphereData=[]
    ringData=[]

    outerSphereData=np.loadtxt('SphereData.txt')
    SphereNumbers=len(outerSphereData)
    
    for i in range(SphereNumbers):
        innerSphereData.append((outerSphereData[i][0],outerSphereData[i][1],outerSphereData[i][2],
            outerSphereData[i][3]*10/11,outerSphereData[i][4]))
        ringData.append((outerSphereData[i][0],outerSphereData[i][1],outerSphereData[i][2],
            outerSphereData[i][3],outerSphereData[i][3]*10/11,outerSphereData[i][4]))
    np.savetxt('innerSphereData.txt',innerSphereData)#[x,y,radius,sequence number]
    np.savetxt('ITZ.txt',ringData)#[x,y,outter radius, inner raidus,sequence]


if __name__=='__main__':
    ITZGenerator()