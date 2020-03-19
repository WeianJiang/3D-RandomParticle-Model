import numpy as np 

MatrixEle=np.loadtxt('Matrix.txt')
AggregateEle=np.loadtxt('Aggregate.txt')
ITZEle=np.loadtxt('ITZ.txt')

np.savetxt('NewMatrix.txt',MatrixEle,fmt='%i')
np.savetxt('NewAggregate.txt',AggregateEle,fmt='%i')
np.savetxt('NewITZ.txt',ITZEle,fmt='%i')
