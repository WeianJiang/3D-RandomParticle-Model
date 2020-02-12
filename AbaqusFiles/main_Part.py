from abaqus import *
from abaqusConstants import *



s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=10.0)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=STANDALONE)
s.ConstructionLine(point1=(0.0, -5.0), point2=(0.0, 5.0))
s.FixedConstraint(entity=g[2])
session.viewports['Viewport: 1'].view.setValues(nearPlane=6.91285, 
    farPlane=11.9433, width=16.943, height=10.6143, cameraPosition=(1.55708, 
    -1.17012, 9.42809), cameraTarget=(1.55708, -1.17012, 0))
s.unsetPrimaryObject()
del mdb.models['Model-1'].sketches['__profile__']
s1 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
    sheetSize=10.0)
g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
s1.setPrimaryObject(option=STANDALONE)
s1.ConstructionLine(point1=(0.0, -5.0), point2=(0.0, 5.0))
s1.FixedConstraint(entity=g[2])
session.viewports['Viewport: 1'].view.setValues(nearPlane=6.66343, 
    farPlane=12.1927, width=18.623, height=11.6669, cameraPosition=(-1.30362, 
    0.161188, 9.42809), cameraTarget=(-1.30362, 0.161188, 0))
s1.unsetPrimaryObject()
del mdb.models['Model-1'].sketches['__profile__']
s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=10.0)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=STANDALONE)
s.ConstructionLine(point1=(0.0, -5.0), point2=(0.0, 5.0))
s.FixedConstraint(entity=g[2])
session.viewports['Viewport: 1'].view.setValues(nearPlane=7.08634, 
    farPlane=11.7698, width=15.7743, height=9.88219, cameraPosition=(1.01874, 
    1.30163, 9.42809), cameraTarget=(1.01874, 1.30163, 0))
session.viewports['Viewport: 1'].view.setValues(cameraPosition=(0.823599, 
    0.0826082, 9.42809), cameraTarget=(0.823599, 0.0826082, 0))
session.viewports['Viewport: 1'].view.setValues(nearPlane=6.7659, 
    farPlane=12.0903, width=17.9328, height=11.2344, cameraPosition=(1.09731, 
    0.00254041, 9.42809), cameraTarget=(1.09731, 0.00254041, 0))
s.ArcByCenterEnds(center=(0.0, 0.0), point1=(0.0, -5.0), point2=(0.0, 5.0), 
    direction=COUNTERCLOCKWISE)
s.CoincidentConstraint(entity1=v[2], entity2=g[2], addUndoState=False)
s.CoincidentConstraint(entity1=v[0], entity2=g[2], addUndoState=False)
s.CoincidentConstraint(entity1=v[1], entity2=g[2], addUndoState=False)
s.Line(point1=(0.0, 5.0), point2=(0.0, -5.0))
s.VerticalConstraint(entity=g[4], addUndoState=False)
s.PerpendicularConstraint(entity1=g[3], entity2=g[4], addUndoState=False)
p = mdb.models['Model-1'].Part(name='Part-1', dimensionality=THREE_D, 
    type=DEFORMABLE_BODY)
p = mdb.models['Model-1'].parts['Part-1']
p.BaseSolidRevolve(sketch=s, angle=360.0, flipRevolveDirection=OFF)
s.unsetPrimaryObject()
p = mdb.models['Model-1'].parts['Part-1']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
del mdb.models['Model-1'].sketches['__profile__']