from abaqus import *
from abaqusConstants import *

from AbaqusFiles.ModelModule import MyModel

class SteelBar_module(MyModel):

    def __init__(self,coverThickness):
        self.coverThickness=coverThickness

    
    def setNumberofLongui(self,numberofLongui):
        self.numberofLongui=numberofLongui
        self._longuiBarGeneration()
    
    def setSpacingofStir(self,enlargementSpacingofStir,nonEnlargementSpacingofStir):
        self.enlargementSpacingofStir=enlargementSpacingofStir
        self.nonEnlargementSpacingofStir=nonEnlargementSpacingofStir
        self._stirrupGeneration()
        self._steelBarAssembly()
    
    def setEnlargementofStirrup(self,enlargement,nonEnlargement):
        self.enlargement=enlargement
        self.nonEnlargement=nonEnlargement


    def _stirrupGeneration(self):
        s = mdb.models[MyModel._modelName].ConstrainedSketch(name='__profile__', 
            sheetSize=200.0)
        g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
        s.setPrimaryObject(option=STANDALONE)
        s.Line(point1=(0.0, 0.0), point2=(MyModel._sectionLength-2*self.coverThickness, 0.0))
        s.HorizontalConstraint(entity=g[2], addUndoState=False)
        p = mdb.models[MyModel._modelName].Part(name='stirrup', dimensionality=TWO_D_PLANAR, 
            type=DEFORMABLE_BODY)
        p = mdb.models[MyModel._modelName].parts['stirrup']
        p.BaseWire(sketch=s)
        s.unsetPrimaryObject()
        del mdb.models[MyModel._modelName].sketches['__profile__']

    def _longuiBarGeneration(self):
        s = mdb.models[MyModel._modelName].ConstrainedSketch(name='__profile__', 
            sheetSize=200.0)
        g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
        s.setPrimaryObject(option=STANDALONE)
        s.Line(point1=(0,0), point2=(0,MyModel._sectionHeight-self.coverThickness*2))
        #s.Line(point1=(0,0), point2=(0,MyModel._sectionHeight))
        s.VerticalConstraint(entity=g[2], addUndoState=False)
        p = mdb.models[MyModel._modelName].Part(name='longuiBar', dimensionality=TWO_D_PLANAR, 
            type=DEFORMABLE_BODY)
        p = mdb.models[MyModel._modelName].parts['longuiBar']
        p.BaseWire(sketch=s)
        s.unsetPrimaryObject()
        del mdb.models[MyModel._modelName].sketches['__profile__']

    
    def _steelBarAssembly(self):
        a = mdb.models[MyModel._modelName].rootAssembly
        p = mdb.models[MyModel._modelName].parts['longuiBar']
        spacingofLongui=(MyModel._sectionLength-2*self.coverThickness)/(self.numberofLongui-1)
        spacing=self.coverThickness
        for i in range(self.numberofLongui):
            a.Instance(name='longuiBar-'+str(i), part=p, dependent=ON)
            a.translate(instanceList=('longuiBar-'+str(i), ), vector=(spacing,self.coverThickness, 0.0))
            #a.translate(instanceList=('longuiBar-'+str(i), ), vector=(spacing,0.0, 0.0))
            spacing+=spacingofLongui

        #now assembly the stirrup
        p = mdb.models[MyModel._modelName].parts['stirrup']
        numberofEnlargeStirrup=round(self.enlargement/self.enlargementSpacingofStir)
        numberofNonenlargeStirrup=self.nonEnlargement/self.nonEnlargementSpacingofStir-1
        stirHeight=self.coverThickness
        #stirHeight=0

        for i in range(int(numberofEnlargeStirrup+1)):
            
            a.Instance(name='stirrup-'+str(i), part=p, dependent=ON)
            a.translate(instanceList=('stirrup-'+str(i), ), vector=(self.coverThickness,stirHeight, 0.0))
            if i < numberofEnlargeStirrup:
                stirHeight+=self.enlargementSpacingofStir


        
        for j in range(numberofNonenlargeStirrup):
            stirHeight+=self.nonEnlargementSpacingofStir
            a.Instance(name='stirrup-'+str(i+j+1), part=p, dependent=ON)
            a.translate(instanceList=('stirrup-'+str(i+j+1), ), vector=(self.coverThickness,stirHeight, 0.0))
            if j == numberofNonenlargeStirrup - 1:
                stirHeight+=self.nonEnlargementSpacingofStir
            

        
        for k in range(int(numberofEnlargeStirrup+1)):
            a.Instance(name='stirrup-'+str(i+j+k+2), part=p, dependent=ON)
            a.translate(instanceList=('stirrup-'+str(i+j+k+2), ), vector=(self.coverThickness,stirHeight, 0.0))
            stirHeight+=self.enlargementSpacingofStir


        #create set
        
        edges0 = a.instances['stirrup-0'].edges.getSequenceFromMask(mask=('[#1 ]', ), )
        edges=edges0
        for i in range(1,numberofEnlargeStirrup+2*(numberofNonenlargeStirrup+2)):
            edges=edges+a.instances['stirrup-'+str(i)].edges.getSequenceFromMask(mask=('[#1 ]', ), )
        
        for i in range(self.numberofLongui):
            edges=edges+a.instances['longuiBar-'+str(i)].edges.getSequenceFromMask(mask=('[#1 ]', ), )
        
        a.Set(edges=edges, name='RebarSet')
    
    def setStirrupMate(self,di,yieldStrng):
        mdb.models[MyModel._modelName].Material(name='stirrup')
        mdb.models[MyModel._modelName].materials['stirrup'].Density(table=((7.85e-12, ), ))
        mdb.models[MyModel._modelName].materials['stirrup'].Elastic(table=((210000.0, 0.3), ))
        mdb.models[MyModel._modelName].materials['stirrup'].Plastic(table=((yieldStrng, 0.0), ))

        mdb.models[MyModel._modelName].CircularProfile(name='stirrup', r=di/2)
        #mdb.models[MyModel._modelName].TrussSection(name='stirrup', material='stirrup', area=3.14*(di/2)**2)
        mdb.models[MyModel._modelName].BeamSection(name='stirrup', 
            integration=DURING_ANALYSIS, poissonRatio=0.0, profile='stirrup', 
            material='stirrup', temperatureVar=LINEAR, consistentMassMatrix=False)

        p = mdb.models[MyModel._modelName].parts['stirrup']
        e = p.edges
        edges = e.getSequenceFromMask(mask=('[#1 ]', ), )
        region = p.Set(edges=edges, name='Set-stirrup')
        p = mdb.models[MyModel._modelName].parts['stirrup']
        p.SectionAssignment(region=region, sectionName='stirrup', offset=0.0, 
            offsetType=MIDDLE_SURFACE, offsetField='', 
            thicknessAssignment=FROM_SECTION)
        p = mdb.models[MyModel._modelName].parts['stirrup']
        e = p.edges
        edges = e.getSequenceFromMask(mask=('[#1 ]', ), )
        region=p.Set(edges=edges, name='Set-stirrup-beam')
        p = mdb.models[MyModel._modelName].parts['stirrup']
        p.assignBeamSectionOrientation(region=region, method=N1_COSINES, n1=(0.0, 0.0, 
            -1.0))

    def setLonguiBarMate(self,di,yieldStrng):
        mdb.models[MyModel._modelName].Material(name='longuiBar')
        mdb.models[MyModel._modelName].materials['longuiBar'].Density(table=((7.85e-12, ), ))
        mdb.models[MyModel._modelName].materials['longuiBar'].Elastic(table=((210000.0, 0.3), ))
        mdb.models[MyModel._modelName].materials['longuiBar'].Plastic(table=((yieldStrng, 0.0), ))

        mdb.models[MyModel._modelName].CircularProfile(name='longuiBar', r=di/2)
        mdb.models[MyModel._modelName].BeamSection(name='longuiBar', 
            integration=DURING_ANALYSIS, poissonRatio=0.0, profile='longuiBar', 
            material='longuiBar', temperatureVar=LINEAR, consistentMassMatrix=False)

        p = mdb.models[MyModel._modelName].parts['longuiBar']
        e = p.edges
        edges = e.getSequenceFromMask(mask=('[#1 ]', ), )
        region = p.Set(edges=edges, name='Set-longuiBar')
        p = mdb.models[MyModel._modelName].parts['longuiBar']
        p.SectionAssignment(region=region, sectionName='longuiBar', offset=0.0, 
            offsetType=MIDDLE_SURFACE, offsetField='', 
            thicknessAssignment=FROM_SECTION)
        p = mdb.models[MyModel._modelName].parts['longuiBar']
        e = p.edges
        edges = e.getSequenceFromMask(mask=('[#1 ]', ), )
        region=p.Set(edges=edges, name='Set-longuiBar-beam')
        p = mdb.models[MyModel._modelName].parts['longuiBar']
        p.assignBeamSectionOrientation(region=region, method=N1_COSINES, n1=(0.0, 0.0, 
            -1.0))
