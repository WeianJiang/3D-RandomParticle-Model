import numpy as np 

class MaterialGenerator():

    def __init__(self,MaterialName):
        self._MaterialName=MaterialName

    def _weibullGenrator(self,scale,shapeM,number):
        return scale * np.random.weibull(shapeM,number)

    def elasticGenerator(self,baseNumber,weibullShapeNumber):
        '''
        material type: Aggregate, Matrix, interface
        para1: base number
        para2: shape number
        '''
        
        elasticData=self._weibullGenrator(baseNumber,weibullShapeNumber,1000)
        np.savetxt('Constitution/'+str(self._MaterialName)+'ElasticScaleFactor.txt',elasticData)
        return elasticData
    
    def CDPScaleFactorGenerator(self,baseNumber,shapeNumberOfScaleFactor):
        scaleFactor=self._weibullGenrator(1,shapeNumberOfScaleFactor,1000)
        np.savetxt('Constitution/'+str(self._MaterialName)+'CDPScaleFactor.txt',scaleFactor)
        return scaleFactor




if __name__=='__main__':
    # Aggregate=MaterialGenerator('Aggregate')
    # Aggregate.elasticGenerator(1,9)
    # Matrix=MaterialGenerator('Matrix')
    # matrixEla=Matrix.elasticGenerator(1,3)
    # matrixCDP=Matrix.CDPScaleFactorGenerator(1,3)
    # Interface=MaterialGenerator('Interface')
    # interfaceEla=Interface.elasticGenerator(1,1.3)
    # interfaceCDP=Interface.CDPScaleFactorGenerator(1,1.3)
    import matplotlib.pyplot as plt
    # plt.hist(matrixEla)
    # plt.hist(interfaceEla)

    matrix200CDP=np.loadtxt('Matrix200Strength.txt')
    print np.average(matrix200CDP)
    plt.hist(matrix200CDP)

    matrix150CDP=np.loadtxt('Matrix150Strength.txt')
    print np.average(matrix150CDP)
    plt.hist(matrix150CDP)

    matrix100CDP=np.loadtxt('Matrix100Strength.txt')
    print np.average(matrix100CDP)
    plt.hist(matrix100CDP)

    interface200CDP=np.loadtxt('Interface200Strength.txt')
    print np.average(interface200CDP)
    plt.hist(interface200CDP)

    
    interface150CDP=np.loadtxt('Interface150Strength.txt')
    print np.average(interface150CDP)
    plt.hist(interface150CDP)

    interface100CDP=np.loadtxt('Interface100Strength.txt')
    print np.average(interface100CDP)
    plt.hist(interface100CDP)   
    

    plt.show()
