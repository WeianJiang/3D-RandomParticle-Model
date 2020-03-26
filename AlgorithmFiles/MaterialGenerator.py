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
    Aggregate=MaterialGenerator('Aggregate')
    Aggregate.elasticGenerator(1,9)
    Matrix=MaterialGenerator('Matrix')
    matrixEla=Matrix.elasticGenerator(1,3)
    matrixCDP=Matrix.CDPScaleFactorGenerator(1,3)
    Interface=MaterialGenerator('Interface')
    interfaceEla=Interface.elasticGenerator(1,1.5)
    interfaceCDP=Interface.CDPScaleFactorGenerator(1,1.5)
    import matplotlib.pyplot as plt
    # plt.hist(matrixEla)
    # plt.hist(interfaceEla)
    plt.hist(interfaceCDP)
    plt.hist(matrixCDP)

    plt.show()
