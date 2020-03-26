from abaqus import *
from abaqusConstants import *

modelName='Model-Default'
m=mdb.models[modelName]
mat=m.materials


def getElastic(materialName):
    return mat[materialName].elastic.table[0][0]

def getconcreteCompressionHardening(materialName):
    '''
    return a matrix
    '''
    return mat[materialName].concreteDamagedPlasticity.concreteCompressionHardening.table

def getconcreteTensionStiffening(materialName):
    '''
    return a matrix
    '''
    return mat[materialName].concreteDamagedPlasticity.concreteTensionStiffening.table

def getconcreteCompressionDamage(materialName):
    '''
    return matrix
    '''
    return mat[materialName].concreteDamagedPlasticity.concreteCompressionDamage.table

def getconcreteTensionDamage(materialName):
    '''
    return matrix
    '''
    return mat[materialName].concreteDamagedPlasticity.concreteTensionDamage.table

def cal(Stress,crackStrain,damageFactor,elastic):
    return crackStrain-(damageFactor/(1-damageFactor))*(Stress/(elastic))


for i in range(1000):
    mate='Matrix-'
    plasticStrain=[]
    tension=getconcreteTensionStiffening(mate+str(i))
    tensionDamage=getconcreteTensionDamage(mate+str(i))
    elastic=getElastic(mate+str(i))
    for j in range(len(tension)-1):
        result=cal(tension[j][0],tension[j][1],tensionDamage[j][0],elastic)
        if result<0:
            print j,'Negative'
        plasticStrain.append(result)
    for j in range(len(tension)-2):
        if plasticStrain[j]>plasticStrain[j+1]:
            print j,'Descending'

print 'Done'
