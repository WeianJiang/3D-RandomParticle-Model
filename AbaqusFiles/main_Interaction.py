from abaqus import *
from abaqusConstants import *
import regionToolset
from AbaqusFiles.ModelModule import MyModel


class InteractionModule(MyModel):

    def _createLoadingPlate(self):
        #-----create the loadingPlate Part
        plateSize=MyModel._sectionLength+100
        s1 = mdb.models[MyModel._modelName].ConstrainedSketch(
            name='__profile__', sheetSize=200.0)
        g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
        s1.setPrimaryObject(option=STANDALONE)
        s1.rectangle(point1=(-plateSize/2, plateSize/2), point2=(plateSize/2, -plateSize/2))
        p = mdb.models[MyModel._modelName].Part(name='LoadingPlate', 
            dimensionality=THREE_D, type=DEFORMABLE_BODY)
        p = mdb.models[MyModel._modelName].parts['LoadingPlate']
        p.BaseShell(sketch=s1)
        s1.unsetPrimaryObject()
        del mdb.models[MyModel._modelName].sketches['__profile__']
        #----------end of Part

        #---this section create the loadingPlate Material
        mdb.models[MyModel._modelName].SurfaceSection(name='LoadingPlate', 
            useDensity=ON, density=2.5e-09)
        p = mdb.models[MyModel._modelName].parts['LoadingPlate']
        f = p.faces
        faces = f.getSequenceFromMask(mask=('[#1 ]', ), )
        region = p.Set(faces=faces, name='Part_LoadingPlate-Set')
        p.SectionAssignment(region=region, sectionName='LoadingPlate', offset=0.0, 
            offsetType=MIDDLE_SURFACE, offsetField='', 
            thicknessAssignment=FROM_SECTION)

        # #this section create the Section
        # mdb.models[MyModel._modelName].HomogeneousSolidSection(name='LoadingPlate', 
        #     material='LoadingPlate', thickness=None)
        # p = mdb.models[MyModel._modelName].parts['LoadingPlate']
        # c = p.cells
        # cells = c.getSequenceFromMask(mask=('[#1 ]', ), )
        # region = p.Set(cells=cells, name='Set-1')
        # p = mdb.models[MyModel._modelName].parts['LoadingPlate']
        # p.SectionAssignment(region=region, sectionName='LoadingPlate', offset=0.0, 
        #     offsetType=MIDDLE_SURFACE, offsetField='', 
        #     thicknessAssignment=FROM_SECTION)
        #end of Material

        #this section create the instance of loading plate
        a = mdb.models[MyModel._modelName].rootAssembly
        p = mdb.models[MyModel._modelName].parts['LoadingPlate']
        a.Instance(name='LoadingPlate-Up', part=p, dependent=ON)
        a.Instance(name='LoadingPlate-Low', part=p, dependent=ON)

        a.rotate(instanceList=('LoadingPlate-Up', 'LoadingPlate-Low'), axisPoint=(0.0, 0.0, 0.0), 
            axisDirection=(1.0, 0.0, 0.0), angle=90.0)

        a.translate(instanceList=('LoadingPlate-Up', ), vector=(
            0.5*MyModel._sectionLength, 
            MyModel._sectionHeight, 
            0.5*MyModel._sectionLength))
        a.translate(instanceList=('LoadingPlate-Low', ), vector=(
            0.5*MyModel._sectionLength, 
            0, 
            0.5*MyModel._sectionLength))
        #end of Instance

        #this section create Interation
        a.ReferencePoint(point=(0.5*MyModel._sectionLength, MyModel._sectionHeight, 0.5*MyModel._sectionLength))
        a.ReferencePoint(point=(0.5*MyModel._sectionLength, 0, 0.5*MyModel._sectionLength))

        f1 = a.instances['LoadingPlate-Up'].faces
        faces1 = f1.findAt(((0.5*MyModel._sectionLength, MyModel._sectionHeight, 0.5*MyModel._sectionLength), ))
        region2=regionToolset.Region(faces=faces1)

        r1 = a.referencePoints
        refPoints1=(r1.findAt([0.5*MyModel._sectionLength, MyModel._sectionHeight, 0.5*MyModel._sectionLength]),)
        a.Set(referencePoints=refPoints1, name='Set-LoadRefPoint')
        region1=regionToolset.Region(referencePoints=refPoints1)
        mdb.models[MyModel._modelName].RigidBody(name='Constrain_LoadingPlate_Up_Rigid', 
            refPointRegion=region1, bodyRegion=region2, refPointAtCOM=ON)
        #-------------Lower plate
        f1 = a.instances['LoadingPlate-Low'].faces
        faces1 = f1.findAt(((0.5*MyModel._sectionLength, 0, 0.5*MyModel._sectionLength), ))
        region2=regionToolset.Region(faces=faces1)

        r1 = a.referencePoints
        refPoints1=(r1.findAt([0.5*MyModel._sectionLength, 0, 0.5*MyModel._sectionLength]),)
        a.Set(referencePoints=refPoints1, name='Set-BoundaryRefPoint')
        region1=regionToolset.Region(referencePoints=refPoints1)
        mdb.models[MyModel._modelName].RigidBody(name='Constrain_LoadingPlate_Low_Rigid', 
            refPointRegion=region1, bodyRegion=region2, refPointAtCOM=ON)
        #-------------------------------------
        #create contact property
        mdb.models[MyModel._modelName].ContactProperty('FrictionContact')
        mdb.models[MyModel._modelName].interactionProperties['FrictionContact'].TangentialBehavior(
            formulation=PENALTY, directionality=ISOTROPIC, slipRateDependency=OFF, 
            pressureDependency=OFF, temperatureDependency=OFF, dependencies=0, table=((
            0.15, ), ), shearStressLimit=None, maximumElasticSlip=FRACTION, 
            fraction=0.005, elasticSlipStiffness=None)


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

        a = mdb.models[MyModel._modelName].rootAssembly
        #upper plate
        s1 = a.instances['LoadingPlate-Up'].faces
        side1Faces1 = s1.findAt(((0.5*MyModel._sectionLength, MyModel._sectionHeight, 0.5*MyModel._sectionLength), ))
        region1=regionToolset.Region(side1Faces=side1Faces1)#means the lower side

        region2=regionToolset.Region(nodes=UpperNodeSet)
        mdb.models[MyModel._modelName].SurfaceToSurfaceContactExp(
            name ='Int-Contact-Up', createStepName='Step-1', master = region1, slave = region2, 
            mechanicalConstraint=PENALTY, sliding=FINITE, 
            interactionProperty='FrictionContact', initialClearance=OMIT, 
            datumAxis=None, clearanceRegion=None)
        #lower plate
        s1 = a.instances['LoadingPlate-Low'].faces
        side2Faces1 = s1.findAt(((0.5*MyModel._sectionLength, 0, 0.5*MyModel._sectionLength), ))
        region1=regionToolset.Region(side2Faces=side2Faces1)

        region2=regionToolset.Region(nodes=LowerNodeSet)
        mdb.models[MyModel._modelName].SurfaceToSurfaceContactExp(
            name ='Int-Contact-Low', createStepName='Step-1', master = region1, slave = region2, 
            mechanicalConstraint=PENALTY, sliding=FINITE, 
            interactionProperty='FrictionContact', initialClearance=OMIT, 
            datumAxis=None, clearanceRegion=None)
        #end Interaction
        import mesh
        p = mdb.models[MyModel._modelName].parts['LoadingPlate']
        elemType1 = mesh.ElemType(elemCode=SFM3D4R, elemLibrary=STANDARD)
        elemType2 = mesh.ElemType(elemCode=SFM3D3, elemLibrary=STANDARD)
        f = p.faces
        faces = f.getSequenceFromMask(mask=('[#1 ]', ), )
        pickedRegions =(faces, )
        p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2))
        p.seedPart(size=10.0, deviationFactor=0.1, minSizeFactor=0.1)
        p.generateMesh()
        



    def setCoupling(self):
        self._createLoadingPlate()
        # length=MyModel._sectionLength
        # height=MyModel._sectionHeight
        # a = mdb.models[MyModel._modelName].rootAssembly
        # r1 = a.referencePoints
        # refPoints1=(r1.findAt([0.5*length, height, 0.5*length]),)
        # region1=a.Set(referencePoints=refPoints1, name='m_Set-Coupling')
        # a = mdb.models[MyModel._modelName].rootAssembly
        # s1 = a.instances['LoadingPlate-Up'].faces
        # side2Faces1 = s1.findAt(((0.5*MyModel._sectionLength, MyModel._sectionHeight, 0.5*MyModel._sectionLength), ))
        # region2=regionToolset.Region(side2Faces=side2Faces1)
        # mdb.models[MyModel._modelName].Coupling(name='UpperPlateCoupling', 
        #     controlPoint=region1, surface=region2, influenceRadius=WHOLE_SURFACE, 
        #     couplingType=KINEMATIC, localCsys=None, u1=ON, u2=ON, u3=ON, ur1=ON, 
        #     ur2=ON, ur3=ON)


        


