import numpy as np 
import copy

def cal(crackStrain,Stress,damageFactor,elasticScaleFactor=1):
    return crackStrain-(damageFactor/(1-damageFactor))*(Stress/(23000*elasticScaleFactor))

loadPath='Constitution/'
Compress=np.loadtxt(loadPath+'Compression.txt')
Tensile=np.loadtxt(loadPath+'Tension.txt')
TensionDamage=np.loadtxt(loadPath+'TensionDamage.txt')
CompressionDamage=np.loadtxt(loadPath+'CompressionDamage.txt')
CDP_SF=np.loadtxt(loadPath+'Matrix'+'CDPScaleFactor.txt')
ElasticData=np.loadtxt(loadPath+'Matrix'+'Elastic.txt')
E_SF=np.loadtxt(loadPath+'Matrix'+'ElasticScaleFactor.txt')
for k in range(1000):
    random=np.random.randint(0,1000)
    Temp_Compress=copy.deepcopy(Compress)
    Temp_Tensile=copy.deepcopy(Tensile)
    Temp_TensionDamage=copy.deepcopy(TensionDamage)
    Temp_CompressionDamage=copy.deepcopy(CompressionDamage)
    Temp_Compress=Compress*CDP_SF[np.random.randint(0,1000)]
    Temp_Tensile=Tensile*CDP_SF[np.random.randint(0,1000)]

    Temp_TensionDamage[:,1]=TensionDamage[:,1]*CDP_SF[random]
    Temp_CompressionDamage[:,1]=CompressionDamage[:,1]*CDP_SF[random]

    Temp_ElasticData=ElasticData*E_SF[random]
    result=[]
    for i in range(len(Compress)):
        result.append(cal(Temp_Compress[i][1],Temp_Compress[i][0],Temp_CompressionDamage[i][0],Temp_ElasticData[i]))
        if result[i]<0:
            print 'Negative'

    for i in range(0,9):
        if result[i+1]<result[i]:
            print 'Descending'



