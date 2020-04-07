from abaqus import *
from abaqusConstants import *
from AbaqusFiles.ModelModule import MyModel


class InteractionModule(MyModel):

    def _createLoadingPlate(self):
        #-----create the loadingPlate Part
        plateSize=MyModel._sectionLength+100
        s = mdb.models[MyModel._modelName].ConstrainedSketch(name='__profile__', 
            sheetSize=200.0)
        g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
        s.setPrimaryObject(option=STANDALONE)
        s.rectangle(point1=(-plateSize/2, 10.0), point2=(plateSize/2, -10.0))
        p = mdb.models[MyModel._modelName].Part(name='LoadingPlate', 
            dimensionality=THREE_D, type=DEFORMABLE_BODY)
        p = mdb.models[MyModel._modelName].parts['LoadingPlate']
        p.BaseSolidExtrude(sketch=s, depth=plateSize)
        s.unsetPrimaryObject()
        del mdb.models[MyModel._modelName].sketches['__profile__']
        #----------end of Part

        #---this section create the loadingPlate Material
        mdb.models[MyModel._modelName].Material(name='LoadingPlate')
        mdb.models[MyModel._modelName].materials['LoadingPlate'].Density(table=((1.0, 
            ), ))
        mdb.models[MyModel._modelName].materials['LoadingPlate'].Elastic(table=((
            9999999.0, 0.2), ))

        #this section create the Section
        mdb.models[MyModel._modelName].HomogeneousSolidSection(name='LoadingPlate', 
            material='LoadingPlate', thickness=None)
        p = mdb.models[MyModel._modelName].parts['LoadingPlate']
        c = p.cells
        cells = c.getSequenceFromMask(mask=('[#1 ]', ), )
        region = p.Set(cells=cells, name='Set-1')
        p = mdb.models[MyModel._modelName].parts['LoadingPlate']
        p.SectionAssignment(region=region, sectionName='LoadingPlate', offset=0.0, 
            offsetType=MIDDLE_SURFACE, offsetField='', 
            thicknessAssignment=FROM_SECTION)
        #end of Material

        #this section create the instance of loading plate
        a = mdb.models[MyModel._modelName].rootAssembly
        p = mdb.models[MyModel._modelName].parts['LoadingPlate']
        a.Instance(name='LoadingPlate-Up', part=p, dependent=ON)
        a.Instance(name='LoadingPlate-Low', part=p, dependent=ON)
   
        a.translate(instanceList=('LoadingPlate-Up', ), vector=(
            0.5*MyModel._sectionLength-0,
            MyModel._sectionHeight+10, 
            0.5*MyModel._sectionLength-0.5*plateSize))
        a.translate(instanceList=('LoadingPlate-Low', ), vector=(
            0.5*MyModel._sectionLength-0,
            -10, 
            0.5*MyModel._sectionLength-0.5*plateSize))
        #end of Instance

        #this section create TIE
        n1 = a.instances['MeshPart-1'].nodes
        UpperNodeSet=[]
        LowerNodeSet=[]
        for i in range (len(n1)):
            nodeCoordinates=n1[i].coordinates
            y_coordinate=nodeCoordinates[1]
            if y_coordinate==MyModel._sectionHeight:
                if len(UpperNodeSet)==0:
                    UpperNodeSet=n1[i:i+1]
                else:
                    UpperNodeSet=UpperNodeSet+n1[i:i+1]
            elif y_coordinate==0:
                if len(LowerNodeSet)==0:
                    LowerNodeSet=n1[i:i+1]
                else:
                    LowerNodeSet=LowerNodeSet+n1[i:i+1]
        UpperNodeRegion=a.Set(nodes=UpperNodeSet, name='UpperNodeSet')
        a = mdb.models[MyModel._modelName].rootAssembly

        s1 = a.instances['LoadingPlate-Up'].faces
        UpperPlateSurface = s1.findAt(((0.5*MyModel._sectionLength, MyModel._sectionHeight, 0.5*MyModel._sectionLength), ))
        UpperPlateRegion=a.Surface(side1Faces=UpperPlateSurface, name='UpperPlateSurface')
        mdb.models[MyModel._modelName].Tie(name='UpperNodeTie', master=UpperPlateRegion, 
            slave=UpperNodeRegion, positionToleranceMethod=COMPUTED, adjust=ON, 
            tieRotations=ON, thickness=ON)

        LowerNodeRegion=a.Set(nodes=LowerNodeSet, name='LowerNodeSet')
        s1 = a.instances['LoadingPlate-Low'].faces
        LowerPlateSurface = s1.findAt(((0.5*MyModel._sectionLength, 0, 0.5*MyModel._sectionLength), ))
        LowerPlateRegion=a.Surface(side1Faces=LowerPlateSurface, name='LowerPlateSurface')
        mdb.models[MyModel._modelName].Tie(name='LowerNodeTie', master=LowerPlateRegion, 
            slave=LowerNodeRegion, positionToleranceMethod=COMPUTED, adjust=ON, 
            tieRotations=ON, thickness=ON)
        #end Interaction

        p = mdb.models[MyModel._modelName].parts['LoadingPlate']
        p.seedPart(size=10.0, deviationFactor=0.1, minSizeFactor=0.1)
        p.generateMesh()
        



    def setCoupling(self):
        self._createLoadingPlate()
        length=MyModel._sectionLength
        height=MyModel._sectionHeight
        a = mdb.models[MyModel._modelName].rootAssembly
        a.ReferencePoint(point=(0.5*length, height+20, 0.5*length))
        r1 = a.referencePoints
        refPoints1=(r1.findAt([0.5*length, height+20, 0.5*length]),)
        region1=a.Set(referencePoints=refPoints1, name='m_Set-Coupling')

        s1 = a.instances['LoadingPlate-Up'].faces
        side1Faces1 = s1.findAt(((0.5*length, height+20, 0.5*length), ))
        region2=a.Surface(side1Faces=side1Faces1, name='s_Surf-Coupling')
        mdb.models[MyModel._modelName].Coupling(name='Constraint-Coupling', 
            controlPoint=region1, surface=region2, influenceRadius=WHOLE_SURFACE, 
            couplingType=KINEMATIC, localCsys=None, u1=ON, u2=ON, u3=ON, ur1=ON, 
            ur2=ON, ur3=ON)

