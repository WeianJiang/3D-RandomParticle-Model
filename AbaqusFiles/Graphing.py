from abaqus import *
from abaqusConstants import *
from caeModules import *
from AbaqusFiles.ModelModule import MyModel

odb = session.odbs['Job-'+MyModel._modelName+'.odb']
xyList = xyPlot.xyDataListFromField(odb=odb, outputPosition=NODAL, variable=((
    'RF', NODAL, ((COMPONENT, 'RF2'), )), ('U', NODAL, ((COMPONENT, 'U2'), )), 
    ), nodeSets=('M_SET-COUPLING', ))
xyp = session.XYPlot('XYPlot-1')
chartName = xyp.charts.keys()[0]
chart = xyp.charts[chartName]
curveList = session.curveSet(xyData=xyList)
chart.setValues(curvesToPlot=curveList)
#session.viewports['Viewport: 1'].setValues(displayedObject=xyp)
xy1 = session.xyDataObjects['_U:U2 PI: ASSEMBLY N: 1']
xy2 = session.xyDataObjects['_RF:RF2 PI: ASSEMBLY N: 1']
xy3 = combine(xy1, xy2)
xyp = session.xyPlots['XYPlot-1']
chartName = xyp.charts.keys()[0]
chart = xyp.charts[chartName]
c1 = session.Curve(xyData=xy3)
chart.setValues(curvesToPlot=(c1, ), )