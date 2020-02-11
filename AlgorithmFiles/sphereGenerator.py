import numpy as np 


xSize=0
ySize=0
zSize=0 #initialing default variables

def set3DSize(crossSectX,crossSectY,depth):
    global xSize
    global ySize
    global zSize
    xSize=crossSectX
    ySize=crossSectY
    zSize=depth


def boudaryDetect(x, y, z,r):  # Funtion used to detect whether the circle cross the boundry
    if x-r > 0 and y-r > 0 and z-r>0 and x+r < xSize and y+r < ySize and z+r<zSize:
        return True

def overlapDetect(x1, y1,z1, r1, x2, y2,z2, r2):
    distanceSquare = np.square(x1-x2)+np.square(y1-y2)+np.square(z1-z2)
    if distanceSquare < (r1+r2)**2:
        return True  # return ture if overlap


def dataGen(minimumRadi,maximumRadi):  # generate parameters of circle
    centroid_x = np.random.rand()*xSize
    centroid_y = np.random.rand()*ySize
    centroid_z=np.random.rand()*zSize
    radi = np.random.uniform(minimumRadi, maximumRadi)
    if boudaryDetect(centroid_x, centroid_y,centroid_z, radi):
        return [centroid_x, centroid_y,centroid_z, radi]
    else:
        return dataGen(minimumRadi,maximumRadi)


def sphereGenerator(trialTimes,minimumRadi,maximumRadi,circleData=[]):
    if len(circleData)==0:
        circleData.append(dataGen(minimumRadi,maximumRadi))
        formerLength=0
    else:
        formerLength=len(circleData)
    for number in range(trialTimes):
        newCircle = dataGen(minimumRadi,maximumRadi)
        looptimes = 0
        for i in range(len(circleData)):
            if overlapDetect(newCircle[0], newCircle[1], newCircle[2],newCircle[3], circleData[i][0], circleData[i][1], circleData[i][2],circleData[i][3]):
                break
            looptimes += 1
        if looptimes == len(circleData):
            circleData.append(newCircle)
    for order in range(formerLength,len(circleData)):
        circleData[order].append(order)
    return circleData
# set3DSize(1,2,3)
# print xSize, ySize, zSize

def drawCircle(centroid_x, centroid_y, centroid_z,radi):  # draw circles by given parameters, in which order is useless
    from mpl_toolkits.mplot3d import Axes3D
    u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
    x=centroid_x + radi*np.cos(u)*np.sin(v)
    y=centroid_y + radi*np.sin(u)*np.sin(v)
    z=centroid_z + radi*np.cos(v)
    ax.plot_surface(x, y, z)


if __name__=="__main__":
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    import mpl_toolkits.mplot3d
    set3DSize(150,150,150)
    fig = plt.figure(figsize=(6, 6), dpi=100)
    ax=Axes3D(fig)
    ax.set_xlim(0,150)
    ax.set_ylim(0,150)
    ax.set_zlim(0,150)

    sphereData=sphereGenerator(3,8,10)
    for i in range(len(sphereData)):  # draw module
        # "*" used for transfer three parameters in one
        drawCircle(sphereData[i][0],sphereData[i][1],sphereData[i][2],sphereData[i][3])
    plt.show()
    sphereData=np.array(sphereData)
    np.savetxt('sphereData.txt',sphereData)