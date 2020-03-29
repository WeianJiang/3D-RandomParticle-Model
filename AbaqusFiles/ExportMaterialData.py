from abaqus import *
from abaqusConstants import *
import numpy as np 
from AbaqusFiles.ModelModule import MyModel


m=mdb.models[MyModel._modelName]
p=m.parts['MeshPart']
secAssigns=p.sectionAssignments # return a tuple: SecAssigns[i], get secAssigns[i].sectionName
matrixCompressionStrength=[]
interfaceCompressionStrength=[]
for eachSectionAssign in secAssigns:
    sectionName=eachSectionAssign.sectionName
    section=m.sections[sectionName]
    materialName=section.material
    thisMaterial=m.materials[materialName]
    if materialName[0]=='M':
        CDPCompressStrength=thisMaterial.concreteDamagedPlasticity.concreteCompressionHardening.table[1][0]
        #CDPTensionStrength=thisMaterial.concreteDamagedPlasticity.concreteTensionStiffening.table[0][0]
        matrixCompressionStrength.append(CDPCompressStrength)
    elif materialName[0]=='I':
        CDPCompressStrength=thisMaterial.concreteDamagedPlasticity.concreteCompressionHardening.table[1][0]
        interfaceCompressionStrength.append(CDPCompressStrength)

np.savetxt('MatrixStrength.txt',matrixCompressionStrength)
np.savetxt('InterfaceStrength.txt',interfaceCompressionStrength)