from abaqus import *
from abaqusConstants import *
from AlgorithmFiles.GridTopo import GridTopo



model=GridTopo()
model.setPath(2)
model.setSize(100,100)
model.setMeshSize(5)
model.setLoad(-8)