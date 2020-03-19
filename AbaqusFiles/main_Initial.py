from abaqus import *
from abaqusConstants import *

from ModelModule import MyModel


def createModel():
    mdb.Model(name=MyModel._modelName, modelType=STANDARD_EXPLICIT)