import numpy as np 
import gc


inputfile=open('ModelInfoFiles/1/inputfile.inp')
lines=inputfile.readlines()
inputfile.close()


Keyword_Node="*Node\r\n"
Keyword_Element="*Element, type=C3D8R\r\n"
Keyword_ElementBottom='*End Part\r\n'

NodeIndex=lines.index(Keyword_Node)+1
ElementIndex=lines.index(Keyword_Element)+1
NodeBottomIndex=ElementIndex-2
ElementBottomIndex=lines.index(Keyword_ElementBottom)-1

del lines
gc.collect()

NodeRowNumber=NodeBottomIndex-NodeIndex+1
ElementRowNumber=ElementBottomIndex-ElementIndex+1
NodeData=[]
NodeData=np.loadtxt('ModelInfoFiles/1/inputfile.inp',delimiter=',',skiprows=NodeIndex,max_rows=NodeRowNumber)
np.savetxt('NodeData.txt',NodeData)
del NodeData
gc.collect()
EleData=[]
EleData=np.loadtxt('ModelInfoFiles/1/inputfile.inp',delimiter=',',skiprows=ElementIndex,max_rows=ElementRowNumber)
np.savetxt('ElementData.txt',EleData)

# for i in range(NodeIndex,NodeBottomIndex):
#     lines[i]= lines[i].replace(' ','').replace('\r\n','').split(',')



# def rearrange(begin,end):
#     for i in range(begin,end+1):
#         lines[i]= lines[i].replace(' ','').replace('\r\n','').split(',')


# rearrange(NodeIndex,NodeBottomIndex)
# rearrange(ElementIndex,ElementBottomIndex)

# newfile=open('NewFile.txt','w')

# for newline in lines:
#     newfile.write(newline)

# newfile.close()