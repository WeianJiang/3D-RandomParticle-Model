from abaqus import *
from abaqusConstants import *
from AbaqusFiles.ModelModule import MyModel


class JobMoudle(MyModel):

    def __init__(self,jobName):
        self._jobName=jobName


    def createJob(self,cores=1):
        mdb.Job(name=self._jobName, model=MyModel._modelName, description='', type=ANALYSIS, 
            atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
            memoryUnits=PERCENTAGE, explicitPrecision=SINGLE, 
            nodalOutputPrecision=SINGLE, echoPrint=OFF, modelPrint=OFF, 
            contactPrint=OFF, historyPrint=OFF, userSubroutine='', scratch='', 
            parallelizationMethodExplicit=DOMAIN, numDomains=cores, 
            activateLoadBalancing=False, multiprocessingMode=DEFAULT, numCpus=cores)

    def jobSubmit(self):
        mdb.jobs[self._jobName].submit(consistencyChecking=OFF)