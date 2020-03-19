from abaqus import *
from abaqusConstants import *
from AlgorithmFiles.GridTopo import GridTopo



model=GridTopo()
model.setPath(1)
model.setSize(150,150)
model.setMeshSize(15)