import numpy as np
# import matplotlib.pyplot as plt

def weibullGenrator(shapeM,scale):
    return scale * np.random.weibull(shapeM)



if __name__=='__main__':
    print weibullGenrator(10,480000)