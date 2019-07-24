//problemtype for KRATOS structural application
//and ekate extension
//(c) 2012 Janosch Stascheit, Ruhr-University Bochum
//(c) 2016 Hoang Giang Bui, Ruhr-University Bochum
*tcl(Initialize)
Begin ModelPartData
//  VARIABLE_NAME value
End ModelPartData
*loop materials
*if(strcmp(MatProp(ConstitutiveLaw),"UserDefined")==0)
Begin Properties *MatNum
BODY_FORCE [3] (0.0, 0.0, 0.0)
*if(strcmp(GenData(Enable_Gravity),"1")==0)
GRAVITY [3] ( *GenData(Gravity_X,real), *GenData(Gravity_Y,real), *GenData(Gravity_Z,real) )
*else
GRAVITY [3] ( 0.0, 0.0, 0.0 )
*endif
End Properties
*else
Begin Properties *MatNum
DENSITY *MatProp(Density,real)  //scalar
*set var bodyForceX = Operation(MatProp(Density,real)*GenData(Gravity_X,real))
*set var bodyForceY = Operation(MatProp(Density,real)*GenData(Gravity_Y,real))
*set var bodyForceZ = Operation(MatProp(Density,real)*GenData(Gravity_Z,real))
*if(strcmp(GenData(Enable_Gravity),"1")==0)
//BODY_FORCE [3] (*bodyForceX, *bodyForceY, *bodyForceZ)
BODY_FORCE [3] (0.0, 0.0, 0.0)
GRAVITY [3] ( *GenData(Gravity_X,real), *GenData(Gravity_Y,real), *GenData(Gravity_Z,real) )
*else
BODY_FORCE [3] (0.0, 0.0, 0.0)
GRAVITY [3] ( 0.0, 0.0, 0.0 )
*endif
*if(strcmp(MatProp(ConstitutiveLaw),"Isotropic3D")==0)
YOUNG_MODULUS *MatProp(Young_modulus,real)
POISSON_RATIO *MatProp(Poisson_ratio,real)
*endif
*if(strcmp(MatProp(ConstitutiveLaw),"TutorialDamageModel")==0)
YOUNG_MODULUS *MatProp(Young_modulus,real)
POISSON_RATIO *MatProp(Poisson_ratio,real)
DAMAGE_E0 *MatProp(E0,real)
DAMAGE_EF *MatProp(Ef,real)
*endif
*if(strcmp(MatProp(ConstitutiveLaw),"GroutingMortar")==0)
YOUNG_MODULUS *MatProp(Young_modulus,real)
POISSON_RATIO *MatProp(Poisson_ratio,real)
PRIMARY_HYDRATION_TIME *MatProp(prim_hyd_time,real)
PRIMARY_HYDRATION_TIME_GRADIENT *MatProp(gradient_prim_hyd_time,real)
STIFFNESS_RATIO *MatProp(E_ratio,real)
*endif
*if(strcmp(MatProp(ConstitutiveLaw),"TrussMaterial")==0)
YOUNG_MODULUS *MatProp(Young_modulus,real)
POISSON_RATIO *MatProp(Poisson_ratio,real)
*endif
End Properties
*endif
*end materials

Begin Nodes
*RealFormat "%10.5f"
*loop nodes
*nodesnum   *NodesCoord(1)  *NodesCoord(2)  *NodesCoord(3)
*end nodes
End Nodes

*include ekate_elements.include


//Begin Conditions Condition2D
//1799 0        644        650
//1800 0        650        663
//1801 0        663        673
//...
//1947 0        972        973
//1948 0        973        974
//End Conditions


*set var condID=1
*set var condID2=1

Begin Conditions MasterContactFace3D3
*set cond Contact_Master
*loop elems *OnlyInCond
*if(ElemsNnodeFace==3)
*condID      *ElemsMat    *\
*GlobalNodes(2) *GlobalNodes(1) *GlobalNodes(3) 
//ElementAssignment *condID *ElemsNum
*set var condID= condID+1
*endif
*end elems
End Conditions

Begin Conditions MasterContactFace3D6
*set cond Contact_Master
*loop elems *OnlyInCond
*if(ElemsNnodeFace==6)
*condID      *ElemsMat    *\
*Globalnodes(2) *Globalnodes(1) *Globalnodes(3) *Globalnodes(4) *Globalnodes(6) *Globalnodes(5)
//ElementAssignment *condID *ElemsNum
*set var condID= condID+1
*endif
*end elems
End Conditions

Begin Conditions MasterContactFace3D
*set cond Contact_Master
*loop elems *OnlyInCond
*if(ElemsNnodeFace==4)
*CondID      *ElemsMat    *\
*Globalnodes(4) *Globalnodes(3) *Globalnodes(2) *Globalnodes(1)
//ElementAssignment *condID *ElemsNum
*set var condID= condID+1
*endif
*end elems
End Conditions

Begin Conditions MasterContactFace3D8
*set cond Contact_Master
*loop elems *OnlyInCond
*if(ElemsNnodeFace==8)
*condID      *ElemsMat    *\
*Globalnodes(4) *Globalnodes(3) *Globalnodes(2) *Globalnodes(1) *Globalnodes(7) *Globalnodes(6) *Globalnodes(5) *Globalnodes(8)
//ElementAssignment *condID *ElemsNum
*set var condID= condID+1
*endif
*end elems
End Conditions

Begin Conditions MasterContactFace3D9
*set cond Contact_Master
*loop elems *OnlyInCond
*if(ElemsNnodeFace==9)
*condID      *ElemsMat    *\
*Globalnodes(4) *Globalnodes(3) *Globalnodes(2) *Globalnodes(1) *Globalnodes(7) *Globalnodes(6) *Globalnodes(5) *Globalnodes(8) *Globalnodes(9)
//ElementAssignment *condID *ElemsNum
*set var condID= condID+1
*endif
*end elems
End Conditions

Begin Conditions SlaveContactFace3D3
*set cond Contact_Slave
*loop elems *OnlyInCond
*if(ElemsNnodeFace==3)
*condID      *ElemsMat    *\
*GlobalNodes(2) *GlobalNodes(1) *GlobalNodes(3) 
//ElementAssignment *condID *ElemsNum
*set var condID= condID+1
*endif
*end elems
End Conditions

Begin Conditions SlaveContactFace3D6
*set cond Contact_Slave
*loop elems *OnlyInCond
*if(ElemsNnodeFace==6)
*condID      *ElemsMat    *\
*Globalnodes(2) *Globalnodes(1) *Globalnodes(3) *Globalnodes(4) *Globalnodes(6) *Globalnodes(5)
//ElementAssignment *condID *ElemsNum
*set var condID= condID+1
*endif
*end elems
End Conditions

Begin Conditions SlaveContactFace3D
*set cond Contact_Slave
*loop elems *OnlyInCond
*if(ElemsNnodeFace==4)
*condID      *ElemsMat    *\
*Globalnodes(4) *Globalnodes(3) *Globalnodes(2) *Globalnodes(1)
//ElementAssignment *condID *ElemsNum
*set var condID= condID+1
*endif
*end elems
End Conditions

Begin Conditions SlaveContactFace3D8
*set cond Contact_Slave
*loop elems *OnlyInCond
*if(ElemsNnodeFace==8)
*condID      *ElemsMat    *\
*Globalnodes(4) *Globalnodes(3) *Globalnodes(2) *Globalnodes(1) *Globalnodes(7) *Globalnodes(6) *Globalnodes(5) *Globalnodes(8)
//ElementAssignment *condID *ElemsNum
*set var condID= condID+1
*endif
*end elems
End Conditions

Begin Conditions SlaveContactFace3D9
*set cond Contact_Slave
*loop elems *OnlyInCond
*if(ElemsNnodeFace==9)
*condID      *ElemsMat    *\
*Globalnodes(4) *Globalnodes(3) *Globalnodes(2) *Globalnodes(1) *Globalnodes(7) *Globalnodes(6) *Globalnodes(5) *Globalnodes(8) *Globalnodes(9)
//ElementAssignment *condID *ElemsNum
*set var condID= condID+1
*endif
*end elems
End Conditions

Begin Conditions SurfaceMortarCondition3D3N
*set cond Surface_Mortar *elems *canRepeat
*loop elems *OnlyInCond
*if(ElemsNnodeFace==3)
*condID   *ElemsMat    *\
*GlobalNodes(2) *GlobalNodes(1) *GlobalNodes(3)
//ElementAssignment *condID *ElemsNum
*if(strcmp(cond(2),"Master")==0)
*tcl(SaveCond Surface_Mortar_MasterIndex *condID *cond(1))
*else
*tcl(SaveCond Surface_Mortar_SlaveIndex *condID *cond(1))
*endif
*set var condID= condID+1
*endif
*end elems
End Conditions

Begin Conditions SurfaceMortarCondition3D4N
*set cond Surface_Mortar *elems *canRepeat
*loop elems *OnlyInCond
*if(ElemsNnodeFace==4)
*condID   *ElemsMat    *\
*GlobalNodes(4) *GlobalNodes(3) *GlobalNodes(2) *GlobalNodes(1)
//ElementAssignment *condID *ElemsNum
*if(strcmp(cond(2),"Master")==0)
*tcl(SaveCond Surface_Mortar_MasterIndex *condID *cond(1))
*else
*tcl(SaveCond Surface_Mortar_SlaveIndex *condID *cond(1))
*endif
*set var condID= condID+1
*endif
*end elems
End Conditions

Begin Conditions SurfaceMortarCondition3D6N
*set cond Surface_Mortar *elems *canRepeat
*loop elems *OnlyInCond
*if(ElemsNnodeFace==6)
*condID   *ElemsMat    *\
*Globalnodes(2) *Globalnodes(1) *Globalnodes(3) *Globalnodes(4) *Globalnodes(6) *Globalnodes(5)
//ElementAssignment *condID *ElemsNum
*if(strcmp(cond(2),"Master")==0)
*tcl(SaveCond Surface_Mortar_MasterIndex *condID *cond(1))
*else
*tcl(SaveCond Surface_Mortar_SlaveIndex *condID *cond(1))
*endif
*set var condID= condID+1
*endif
*end elems
End Conditions

Begin Conditions SurfaceMortarCondition3D8N
*set cond Surface_Mortar *elems *canRepeat
*loop elems *OnlyInCond
*if(ElemsNnodeFace==8)
*condID *ElemsMat *\
*GlobalNodes(4) *GlobalNodes(3) *GlobalNodes(2) *GlobalNodes(1) *GlobalNodes(7) *GlobalNodes(6) *GlobalNodes(5) *GlobalNodes(8)
//ElementAssignment *condID *ElemsNum
*if(strcmp(cond(2),"Master")==0)
*tcl(SaveCond Surface_Mortar_MasterIndex *condID *cond(1))
*else
*tcl(SaveCond Surface_Mortar_SlaveIndex *condID *cond(1))
*endif
*set var condID= condID+1
*endif
*end elems
End Conditions

Begin Conditions SurfaceMortarCondition3D9N
*set cond Surface_Mortar *elems *canRepeat
*loop elems *OnlyInCond
*if(ElemsNnodeFace==9)
*condID *ElemsMat *\
*GlobalNodes(4) *GlobalNodes(3) *GlobalNodes(2) *GlobalNodes(1) *GlobalNodes(7) *GlobalNodes(6) *GlobalNodes(5) *GlobalNodes(8) *GlobalNodes(9)
//ElementAssignment *condID *ElemsNum
*if(strcmp(cond(2),"Master")==0)
*tcl(SaveCond Surface_Mortar_MasterIndex *condID *cond(1))
*else
*tcl(SaveCond Surface_Mortar_SlaveIndex *condID *cond(1))
*endif
*set var condID= condID+1
*endif
*end elems
End Conditions

Begin Conditions VolumeMortarCondition3D4N
*set cond Volume_Mortar *elems *canRepeat
*loop elems *OnlyInCond
*if(ElemsType==4)
*if(ElemsNnode==4)
*set var i=0
*set var j= ElemsNnode
*condID *ElemsMat*\
*for(i=1;i<=j;i=i+1)*\
 *ElemsConec(*i)*\
*end

//ElementAssignment *condID *ElemsNum
*set var condID= condID+1
*endif
*endif
*end elems
End Conditions

Begin Conditions VolumeMortarCondition3D8N
*set cond Volume_Mortar *elems *canRepeat
*loop elems *OnlyInCond
*if(ElemsType==5)
*if(ElemsNnode==8)
*set var i=0
*set var j= ElemsNnode
*condID *ElemsMat*\
*for(i=1;i<=j;i=i+1)*\
 *ElemsConec(*i)*\
*end

//ElementAssignment *condID *ElemsNum
*set var condID= condID+1
*endif
*endif
*end elems
End Conditions

Begin Conditions VolumeMortarCondition3D10N
*set cond Volume_Mortar *elems *canRepeat
*loop elems *OnlyInCond
*if(ElemsType==4)
*if(ElemsNnode==10)
*set var i=0
*set var j= ElemsNnode
*condID *ElemsMat*\
*for(i=1;i<=j;i=i+1)*\
 *ElemsConec(*i)*\
*end

//ElementAssignment *condID *ElemsNum
*set var condID= condID+1
*endif
*endif
*end elems
End Conditions

Begin Conditions VolumeMortarCondition3D20N
*set cond Volume_Mortar *elems *canRepeat
*loop elems *OnlyInCond
*if(ElemsType==5)
*if(ElemsNnode==20)
*condID *ElemsMat*\
 *ElemsConec(1) *ElemsConec(2) *ElemsConec(3) *ElemsConec(4) *ElemsConec(5) *ElemsConec(6) *ElemsConec(7) *ElemsConec(8) *ElemsConec(9) *ElemsConec(10) *ElemsConec(11) *ElemsConec(12) *ElemsConec(17) *ElemsConec(18) *ElemsConec(19) *ElemsConec(20) *ElemsConec(13) *ElemsConec(14) *ElemsConec(15) *ElemsConec(16)*\

//ElementAssignment *condID *ElemsNum
*set var condID= condID+1
*endif
*endif
*end elems
End Conditions

Begin Conditions VolumeMortarCondition3D27N
*set cond Volume_Mortar *elems *canRepeat
*loop elems *OnlyInCond
*if(ElemsType==5)
*if(ElemsNnode==27)
*set var i=0
*set var j= ElemsNnode
*condID *ElemsMat*\
*for(i=1;i<=j;i=i+1)*\
 *ElemsConec(*i)*\
*end

//ElementAssignment *condID *ElemsNum
*set var condID= condID+1
*endif
*endif
*end elems
End Conditions

Begin Conditions PointForce3D
*set cond Point_Force *nodes
*add cond Line_Force *nodes
*add cond Surface_Force *nodes
*add cond Volume_Force *nodes
*loop nodes *OnlyInCond
*condID 1 *NodesNum
*set var condID= condID+1
*end nodes
End Conditions

Begin Conditions FaceForce3D3N
*set cond Distributed_Surface_Load *elems *canRepeat
*loop elems *onlyInCond
*if(ElemsNnodeFace==3)
*condID      *ElemsMat    *\
*GlobalNodes(2) *GlobalNodes(1) *GlobalNodes(3) 
//ElementAssignment *condID *ElemsNum
*set var condID= condID+1
*endif
*end elems
End Conditions

Begin Conditions FaceForce3D6N
*set cond Distributed_Surface_Load *elems *canRepeat
*loop elems *onlyInCond
*if(ElemsNnodeFace==6)
*condID      *ElemsMat    *\
*Globalnodes(2) *Globalnodes(1) *Globalnodes(3) *Globalnodes(4) *Globalnodes(6) *Globalnodes(5)
//ElementAssignment *condID *ElemsNum
*set var condID= condID+1
*endif
*end elems
End Conditions

Begin Conditions FaceForce3D4N
*set cond Distributed_Surface_Load *elems *canRepeat
*loop elems *onlyInCond
*if(ElemsNnodeFace==4)
*condID      *ElemsMat    *\
*Globalnodes(4) *Globalnodes(3) *Globalnodes(2) *Globalnodes(1)
//ElementAssignment *condID *ElemsNum
*set var condID= condID+1
*endif
*end elems
End Conditions

Begin Conditions FaceForce3D8N
*set cond Distributed_Surface_Load *elems *canRepeat
*loop elems *onlyInCond
*if(ElemsNnodeFace==8)
*condID      *ElemsMat    *\
*Globalnodes(4) *Globalnodes(3) *Globalnodes(2) *Globalnodes(1) *Globalnodes(7) *Globalnodes(6) *Globalnodes(5) *Globalnodes(8)
//ElementAssignment *condID *ElemsNum
*set var condID= condID+1
*endif
*end elems
End Conditions

Begin Conditions FaceForce3D9N
*set cond Distributed_Surface_Load *elems *canRepeat
*loop elems *onlyInCond
*if(ElemsNnodeFace==9)
*condID      *ElemsMat    *\
*Globalnodes(4) *Globalnodes(3) *Globalnodes(2) *Globalnodes(1) *Globalnodes(7) *Globalnodes(6) *Globalnodes(5) *Globalnodes(8) *Globalnodes(9)
//ElementAssignment *condID *ElemsNum
*set var condID= condID+1
*endif
*end elems
End Conditions

Begin Conditions Face3D3N
*set cond Following_Surface_Load *elems *canRepeat
*loop elems *onlyInCond
*if(ElemsNnodeFace==3)
*condID      *ElemsMat    *\
*GlobalNodes(2) *GlobalNodes(1) *GlobalNodes(3) 
//ElementAssignment *condID *ElemsNum
*tcl(SaveCond Following_Surface_Load *condID *cond(2))
*set var condID= condID+1
*endif
*end elems
End Conditions

Begin Conditions Face3D6N
*set cond Following_Surface_Load *elems *canRepeat
*loop elems *onlyInCond
*if(ElemsNnodeFace==6)
*condID      *ElemsMat    *\
*Globalnodes(2) *Globalnodes(1) *Globalnodes(3) *Globalnodes(4) *Globalnodes(6) *Globalnodes(5)
//ElementAssignment *condID *ElemsNum
*tcl(SaveCond Following_Surface_Load *condID *cond(2))
*set var condID= condID+1
*endif
*end elems
End Conditions

Begin Conditions Face3D4N
*set cond Following_Surface_Load *elems *canRepeat
*loop elems *onlyInCond
*if(ElemsNnodeFace==4)
*condID      *ElemsMat    *\
*Globalnodes(4) *Globalnodes(3) *Globalnodes(2) *Globalnodes(1)
//ElementAssignment *condID *ElemsNum
*tcl(SaveCond Following_Surface_Load *condID *cond(2))
*set var condID= condID+1
*endif
*end elems
End Conditions

Begin Conditions Face3D8N
*set cond Following_Surface_Load *elems *canRepeat
*loop elems *onlyInCond
*if(ElemsNnodeFace==8)
*condID      *ElemsMat    *\
*Globalnodes(4) *Globalnodes(3) *Globalnodes(2) *Globalnodes(1) *Globalnodes(7) *Globalnodes(6) *Globalnodes(5) *Globalnodes(8)
//ElementAssignment *condID *ElemsNum
*tcl(SaveCond Following_Surface_Load *condID *cond(2))
*set var condID= condID+1
*endif
*end elems
End Conditions

Begin Conditions Face3D9N
*set cond Following_Surface_Load *elems *canRepeat
*loop elems *onlyInCond
*if(ElemsNnodeFace==9)
*condID      *ElemsMat    *\
*Globalnodes(4) *Globalnodes(3) *Globalnodes(2) *Globalnodes(1) *Globalnodes(7) *Globalnodes(6) *Globalnodes(5) *Globalnodes(8) *Globalnodes(9)
//ElementAssignment *condID *ElemsNum
*tcl(SaveCond Following_Surface_Load *condID *cond(2))
*set var condID= condID+1
*endif
*end elems
End Conditions

Begin Conditions LiningEndFace3D3N
*set cond Lining_End *elems *canRepeat
*loop elems *onlyInCond
*if(ElemsNnodeFace==3)
*condID      *ElemsMat    *\
*GlobalNodes(2) *GlobalNodes(1) *GlobalNodes(3) 
//ElementAssignment *condID *ElemsNum
*set var condID= condID+1
*endif
*end elems
End Conditions

Begin Conditions LiningEndFace3D6N
*set cond Lining_End *elems *canRepeat
*loop elems *onlyInCond
*if(ElemsNnodeFace==6)
*condID      *ElemsMat    *\
*Globalnodes(2) *Globalnodes(1) *Globalnodes(3) *Globalnodes(4) *Globalnodes(6) *Globalnodes(5)
//ElementAssignment *condID *ElemsNum
*set var condID= condID+1
*endif
*end elems
End Conditions

Begin Conditions LiningEndFace3D4N
*set cond Lining_End *elems *canRepeat
*loop elems *onlyInCond
*if(ElemsNnodeFace==4)
*condID      *ElemsMat    *\
*Globalnodes(4) *Globalnodes(3) *Globalnodes(2) *Globalnodes(1)
//ElementAssignment *condID *ElemsNum
*set var condID= condID+1
*endif
*end elems
End Conditions

Begin Conditions LiningEndFace3D8N
*set cond Lining_End *elems *canRepeat
*loop elems *onlyInCond
*if(ElemsNnodeFace==8)
*condID      *ElemsMat    *\
*Globalnodes(4) *Globalnodes(3) *Globalnodes(2) *Globalnodes(1) *Globalnodes(7) *Globalnodes(6) *Globalnodes(5) *Globalnodes(8)
//ElementAssignment *condID *ElemsNum
*set var condID= condID+1
*endif
*end elems
End Conditions

Begin Conditions LiningEndFace3D9N
*set cond Lining_End *elems *canRepeat
*loop elems *onlyInCond
*if(ElemsNnodeFace==9)
*condID      *ElemsMat    *\
*Globalnodes(4) *Globalnodes(3) *Globalnodes(2) *Globalnodes(1) *Globalnodes(7) *Globalnodes(6) *Globalnodes(5) *Globalnodes(8) *Globalnodes(9)
//ElementAssignment *condID *ElemsNum
*set var condID= condID+1
*endif
*end elems
End Conditions

Begin Conditions TBMEndFace3D3N
*set cond TBM_End *elems *canRepeat
*loop elems *onlyInCond
*if(ElemsNnodeFace==3)
*condID      *ElemsMat    *\
*GlobalNodes(2) *GlobalNodes(1) *GlobalNodes(3) 
//ElementAssignment *condID *ElemsNum
*set var condID= condID+1
*endif
*end elems
End Conditions

Begin Conditions TBMEndFace3D6N
*set cond TBM_End *elems *canRepeat
*loop elems *onlyInCond
*if(ElemsNnodeFace==6)
*condID      *ElemsMat    *\
*Globalnodes(2) *Globalnodes(1) *Globalnodes(3) *Globalnodes(4) *Globalnodes(6) *Globalnodes(5)
//ElementAssignment *condID *ElemsNum
*set var condID= condID+1
*endif
*end elems
End Conditions

Begin Conditions TBMEndFace3D4N
*set cond TBM_End *elems *canRepeat
*loop elems *onlyInCond
*if(ElemsNnodeFace==4)
*condID      *ElemsMat    *\
*Globalnodes(4) *Globalnodes(3) *Globalnodes(2) *Globalnodes(1)
//ElementAssignment *condID *ElemsNum
*set var condID= condID+1
*endif
*end elems
End Conditions

Begin Conditions TBMEndFace3D8N
*set cond TBM_End *elems *canRepeat
*loop elems *onlyInCond
*if(ElemsNnodeFace==8)
*condID      *ElemsMat    *\
*Globalnodes(4) *Globalnodes(3) *Globalnodes(2) *Globalnodes(1) *Globalnodes(7) *Globalnodes(6) *Globalnodes(5) *Globalnodes(8)
//ElementAssignment *condID *ElemsNum
*set var condID= condID+1
*endif
*end elems
End Conditions

Begin Conditions TBMEndFace3D9N
*set cond TBM_End *elems *canRepeat
*loop elems *onlyInCond
*if(ElemsNnodeFace==9)
*condID      *ElemsMat    *\
*Globalnodes(4) *Globalnodes(3) *Globalnodes(2) *Globalnodes(1) *Globalnodes(7) *Globalnodes(6) *Globalnodes(5) *Globalnodes(8) *Globalnodes(9)
//ElementAssignment *condID *ElemsNum
*set var condID= condID+1
*endif
*end elems
End Conditions

Begin Conditions ElasticPointConstraint
*set cond Nodal_Bedding *nodes *or(1,int)
*add cond Nodal_Bedding *nodes *or(3,int)
*add cond Nodal_Bedding *nodes *or(5,int)
*loop nodes *OnlyInCond
*if(cond(1,int)!=0 || cond(3,int)!=0 || cond(5,int)!=0)
*condID 1 *NodesNum
*set var condID= condID+1
*endif
*end nodes
End Conditions

Begin Conditions ElasticLineConstraint2N
*set cond Line_Bedding *elems *canRepeat
*loop elems *onlyInCond
*if(cond(1,int)!=0 || cond(3,int)!=0 || cond(5,int)!=0)
*if(ElemsNnodeFace==2)
*condID      *ElemsMat    *\
*Globalnodes(1) *Globalnodes(2)
//ElementAssignment *condID *ElemsNum
*set var condID= condID+1
*endif
*endif
*end elems
End Conditions

Begin Conditions ElasticLineConstraint3N
*set cond Line_Bedding *elems *canRepeat
*loop elems *onlyInCond
*if(cond(1,int)!=0 || cond(3,int)!=0 || cond(5,int)!=0)
*if(ElemsNnodeFace==3)
*condID      *ElemsMat    *\
*Globalnodes(1) *Globalnodes(3)  *Globalnodes(2)
//ElementAssignment *condID *ElemsNum
*set var condID= condID+1
*endif
*endif
*end elems
End Conditions

Begin Conditions ElasticFaceConstraint3N
*set cond Surface_Bedding *elems *canRepeat
*loop elems *onlyInCond
*if(cond(1,int)!=0 || cond(3,int)!=0 || cond(5,int)!=0)
*if(ElemsNnodeFace==3)
*condID      *ElemsMat    *\
*Globalnodes(2) *Globalnodes(1)  *Globalnodes(3)
//ElementAssignment *condID *ElemsNum
*set var condID= condID+1
*endif
*endif
*end elems
End Conditions

Begin Conditions ElasticFaceConstraint6N
*set cond Surface_Bedding *elems *canRepeat
*loop elems *onlyInCond
*if(cond(1,int)!=0 || cond(3,int)!=0 || cond(5,int)!=0)
*if(ElemsNnodeFace==6)
*condID      *ElemsMat    *\
*Globalnodes(2) *Globalnodes(1) *Globalnodes(3) *Globalnodes(4) *Globalnodes(6) *Globalnodes(5)
//ElementAssignment *condID *ElemsNum
*set var condID= condID+1
*endif
*endif
*end elems
End Conditions

Begin Conditions ElasticFaceConstraint4N
*set cond Surface_Bedding *elems *canRepeat
*loop elems *onlyInCond
*if(cond(1,int)!=0 || cond(3,int)!=0 || cond(5,int)!=0)
*if(ElemsNnodeFace==4)
*condID      *ElemsMat    *\
*Globalnodes(4) *Globalnodes(3) *Globalnodes(2) *Globalnodes(1)
//ElementAssignment *condID *ElemsNum
*set var condID= condID+1
*endif
*endif
*end elems
End Conditions

Begin Conditions ElasticFaceConstraint8N
*set cond Surface_Bedding *elems *canRepeat
*loop elems *onlyInCond
*if(cond(1,int)!=0 || cond(3,int)!=0 || cond(5,int)!=0)
*if(ElemsNnodeFace==8)
*condID      *ElemsMat    *\
*Globalnodes(4) *Globalnodes(3) *Globalnodes(2) *Globalnodes(1) *Globalnodes(7) *Globalnodes(6) *Globalnodes(5) *Globalnodes(8)
//ElementAssignment *condID *ElemsNum
*set var condID= condID+1
*endif
*endif
*end elems
End Conditions

Begin Conditions ElasticFaceConstraint9N
*set cond Surface_Bedding *elems *canRepeat
*loop elems *onlyInCond
*if(cond(1,int)!=0 || cond(3,int)!=0 || cond(5,int)!=0)
*if(ElemsNnodeFace==9)
*condID      *ElemsMat    *\
*Globalnodes(4) *Globalnodes(3) *Globalnodes(2) *Globalnodes(1) *Globalnodes(7) *Globalnodes(6) *Globalnodes(5) *Globalnodes(8) *Globalnodes(9)
//ElementAssignment *condID *ElemsNum
*set var condID= condID+1
*endif
*endif
*end elems
End Conditions


Begin NodalData DISPLACEMENT_X
*set cond Nodal_Displacement *nodes *or(1,int)
*add cond Line_Displacement *nodes *or(1,int)
*add cond Surface_Displacement *nodes *or(1,int)
*add cond Volume_Displacement *nodes *or(1,int)
*loop nodes *OnlyInCond
*NodesNum    *cond(1)    *cond(2)
*end nodes
*set cond IsSide *nodes
*loop nodes *OnlyInCond
*NodesNum 1 0.0
*end nodes
End NodalData

Begin NodalData DISPLACEMENT_Y
*set cond Nodal_Displacement *nodes *or(3,int)
*add cond Line_Displacement *nodes *or(3,int)
*add cond Surface_Displacement *nodes *or(3,int)
*add cond Volume_Displacement *nodes *or(3,int)
*loop nodes *OnlyInCond
*NodesNum    *cond(3)    *cond(4)
*end nodes
*set cond IsSide *nodes
*loop nodes *OnlyInCond
*NodesNum 1 0.0
*end nodes
End NodalData

Begin NodalData DISPLACEMENT_Z
*set cond Nodal_Displacement *nodes *or(5,int)
*add cond Line_Displacement *nodes *or(5,int)
*add cond Surface_Displacement *nodes *or(5,int)
*add cond Volume_Displacement *nodes *or(5,int)
*loop nodes *OnlyInCond
*NodesNum    *cond(5)    *cond(6)
*end nodes
*set cond IsBottom *nodes
*loop nodes *OnlyInCond
*NodesNum 1 0.0
*end nodes
End NodalData

Begin NodalData ROTATION_X
*set cond Nodal_Displacement *nodes *or(7,int)
*add cond Line_Displacement *nodes *or(7,int)
*add cond Surface_Displacement *nodes *or(7,int)
*add cond Volume_Displacement *nodes *or(7,int)
*loop nodes *OnlyInCond
*NodesNum    *cond(7)    *cond(8)
*end nodes
End NodalData

Begin NodalData ROTATION_Y
*set cond Nodal_Displacement *nodes *or(9,int)
*add cond Line_Displacement *nodes *or(9,int)
*add cond Surface_Displacement *nodes *or(9,int)
*add cond Volume_Displacement *nodes *or(9,int)
*loop nodes *OnlyInCond
*NodesNum    *cond(9)    *cond(10)
*end nodes
End NodalData

Begin NodalData ROTATION_Z
*set cond Nodal_Displacement *nodes *or(11,int)
*add cond Line_Displacement *nodes *or(11,int)
*add cond Surface_Displacement *nodes *or(11,int)
*add cond Volume_Displacement *nodes *or(11,int)
*loop nodes *OnlyInCond
*NodesNum    *cond(11)    *cond(12)
*end nodes
End NodalData

Begin NodalData WATER_PRESSURE
*set cond Nodal_Water_Pressure *nodes *or(1,int)
*add cond Line_Water_Pressure *nodes *or(1,int)
*add cond Surface_Water_Pressure *nodes *or(1,int)
*add cond Volume_Water_Pressure *nodes *or(1,int)
*loop nodes *OnlyInCond
*NodesNum    *cond(1)    *cond(2)
*end nodes
*set cond IsTop *nodes
*add cond IsSide *nodes
*loop nodes *OnlyInCond
*NodesNum 1 0.0
*end nodes
End NodalData

Begin NodalData AIR_PRESSURE
*set cond Nodal_Air_Pressure *nodes *or(1,int)
*add cond Line_Air_Pressure *nodes *or(1,int)
*add cond Surface_Air_Pressure *nodes *or(1,int)
*add cond Volume_Air_Pressure *nodes *or(1,int)
*loop nodes *OnlyInCond
*NodesNum    *cond(1)    *cond(2)
*end nodes
*set cond IsTop *nodes
*add cond IsSide *nodes
*loop nodes *OnlyInCond
*NodesNum 1 0.0
*end nodes
End NodalData

Begin NodalData ELASTIC_BEDDING_STIFFNESS_X
*set cond Nodal_Bedding *nodes
*add cond Line_Bedding *nodes
*add cond Surface_Bedding *nodes
*loop nodes *OnlyInCond
*if(cond(1,int)!=0)
*NodesNum 1 *cond(2,real)
*endif
*end nodes
End NodalData

Begin NodalData ELASTIC_BEDDING_STIFFNESS_Y
*set cond Nodal_Bedding *nodes
*add cond Line_Bedding *nodes
*add cond Surface_Bedding *nodes
*loop nodes *OnlyInCond
*if(cond(3,int)!=0)
*NodesNum 1 *cond(4,real)
*endif
*end nodes
End NodalData

Begin NodalData ELASTIC_BEDDING_STIFFNESS_Z
*set cond Nodal_Bedding *nodes
*add cond Line_Bedding *nodes
*add cond Surface_Bedding *nodes
*loop nodes *OnlyInCond
*if(cond(5,int)!=0)
*NodesNum 1 *cond(6,real)
*endif
*end nodes
End NodalData


Begin NodalData FACE_LOAD
*set cond Distributed_Surface_Load *nodes
*loop nodes *OnlyInCond
*NodesNum 0 [3] ( *cond(1), *cond(2), *cond(3) )
*end nodes
End NodalData

Begin NodalData POSITIVE_FACE_PRESSURE
*set cond Following_Surface_Load *nodes
*loop nodes *OnlyInCond
*NodesNum 0 *cond(2)
*end nodes
End NodalData

Begin ElementalData AREA
*set cond LineElementType *elems
*loop elems *OnlyInCond
*if((strcmp(cond(1),"Truss")==0) || (strcmp(cond(1),"Beam")==0))
*ElemsNum *cond(2)
*endif
*end elems
End ElementalData

Begin ElementalData INERTIA
*set cond LineElementType *elems
*loop elems *OnlyInCond
*if(strcmp(cond(1),"Beam")==0)
*ElemsNum [3,3] (( *cond(5), 0, 0 ),(0.0, *cond(3), 0.0),(0.0, 0.0, *cond(4)))
*endif
*end elems
End ElementalData

Begin ElementalData ACTIVATION_LEVEL
*set cond Line_Activation_Level *elems
*add cond Surface_Activation_Level *elems
*add cond Volume_Activation_Level *elems
*format "%i%i"
*loop elems
*ElemsNum *cond(1)
*end elems
End ElementalData

Begin ElementalData USE_DISTRIBUTED_PROPERTIES
*loop elems
*if(strcmp(ElemsMatProp(ConstitutiveLaw),"UserDefined")==0)
*ElemsNum 1
*endif
*end elems
End ElementalData

Begin ElementalData DENSITY_WATER
*set cond VolumeElementType *elems
*loop elems *OnlyInCond
*if(strcmp(cond(1),"UnsaturatedSoil_2Phase")==0)
*ElemsNum *cond(2)
*endif
*if(strcmp(cond(1),"UnsaturatedSoil_3Phase")==0)
*ElemsNum *cond(2)
*endif
*if(strcmp(cond(1),"Grouting_Element")==0)
*ElemsNum *cond(2)
*endif
*end elems
End ElementalData

Begin ElementalData DENSITY_AIR
*set cond VolumeElementType *elems
*loop elems *OnlyInCond
*if(strcmp(cond(1),"UnsaturatedSoil_2Phase")==0)
*ElemsNum *cond(3)
*endif
*if(strcmp(cond(1),"UnsaturatedSoil_3Phase")==0)
*ElemsNum *cond(3)
*endif
*end elems
End ElementalData

Begin ElementalData POROSITY
*set cond VolumeElementType *elems
*loop elems *OnlyInCond
*if(strcmp(cond(1),"UnsaturatedSoil_2Phase")==0)
*ElemsNum *cond(4)
*endif
*if(strcmp(cond(1),"UnsaturatedSoil_3Phase")==0)
*ElemsNum *cond(4)
*endif
*end elems
End ElementalData

Begin ElementalData PERMEABILITY_WATER
*set cond VolumeElementType *elems
*loop elems *OnlyInCond
*if(strcmp(cond(1),"UnsaturatedSoil_2Phase")==0)
*format "%i%14.12e"
*ElemsNum *cond(5)
*endif
*if(strcmp(cond(1),"UnsaturatedSoil_3Phase")==0)
*format "%i%14.12e"
*ElemsNum *cond(5)
*endif
*end elems
End ElementalData

Begin ElementalData PERMEABILITY_AIR
*set cond VolumeElementType *elems
*loop elems *OnlyInCond
*if(strcmp(cond(1),"UnsaturatedSoil_2Phase")==0)
*format "%i%14.12e"
*ElemsNum *cond(6)
*endif
*if(strcmp(cond(1),"UnsaturatedSoil_3Phase")==0)
*format "%i%14.12e"
*ElemsNum *cond(6)
*endif
*end elems
End ElementalData

Begin ElementalData FIRST_SATURATION_PARAM
*set cond VolumeElementType *elems
*loop elems *OnlyInCond
*if(strcmp(cond(1),"UnsaturatedSoil_2Phase")==0)
*ElemsNum 2.5
*endif
*if(strcmp(cond(1),"UnsaturatedSoil_3Phase")==0)
*ElemsNum 2.5
*endif
*end elems
End ElementalData

Begin ElementalData SECOND_SATURATION_PARAM
*set cond VolumeElementType *elems
*loop elems *OnlyInCond
*if(strcmp(cond(1),"UnsaturatedSoil_2Phase")==0)
*ElemsNum 0.4
*endif
*if(strcmp(cond(1),"UnsaturatedSoil_3Phase")==0)
*ElemsNum 0.4
*endif
*end elems
End ElementalData

Begin ElementalData AIR_ENTRY_VALUE
*set cond VolumeElementType *elems
*loop elems *OnlyInCond
*if(strcmp(cond(1),"UnsaturatedSoil_2Phase")==0)
*ElemsNum 3000.0
*endif
*if(strcmp(cond(1),"UnsaturatedSoil_3Phase")==0)
*ElemsNum 3000.0
*endif
*end elems
End ElementalData

Begin ElementalData PERMEABILITY_28_DAYS
*set cond VolumeElementType *elems
*loop elems *OnlyInCond
*if(strcmp(cond(1),"Grouting_Element")==0)
*ElemsNum *cond(7)
*endif
*end elems
End ElementalData

Begin ElementalData PERMEABILITY_1_DAY
*set cond VolumeElementType *elems
*loop elems *OnlyInCond
*if(strcmp(cond(1),"Grouting_Element")==0)
*ElemsNum *cond(8)
*endif
*end elems
End ElementalData

Begin ElementalData PERMEABILITY_TRANSITION
*set cond VolumeElementType *elems
*loop elems *OnlyInCond
*if(strcmp(cond(1),"Grouting_Element")==0)
*ElemsNum *cond(9)
*endif
*end elems
End ElementalData

Begin ElementalData GRAVITY
*loop elems
*if(strcmp(ElemsMatProp(ConstitutiveLaw),"UserDefined")==0)
*if(strcmp(GenData(Enable_Gravity),"1")==0)
*ElemsNum [3] (*GenData(Gravity_X,real), *GenData(Gravity_Y,real), *GenData(Gravity_Z,real))
*endif
*endif
*end elems
End ElementalData

Begin ConditionalData PRESSURE
*tcl(GetCond Following_Surface_Load)
End ConditionalData

Begin ConditionalData MASTER_INDEX
*tcl(GetCond Surface_Mortar_MasterIndex)
End ConditionalData

Begin ConditionalData SLAVE_INDEX
*tcl(GetCond Surface_Mortar_SlaveIndex)
End ConditionalData

