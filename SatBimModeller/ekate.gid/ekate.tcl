# kratos0.1.tcl  -*- TCL -*-
# Kratos Team - 2003
# http://www.cimne.upc.es/kratos/           http://www.kratos.cimne.upc.es
#---------------------------------------------------------------------------
# This file is written in TCL lenguage
# For more information about TCL look at: http://www.sunlabs.com/research/tcl/
#
# At least two procs must be in this file:
#
#    InitGIDProject dir - Will be called whenever a project is begun to be used.
#           where dir is the project's directory
#    EndGIDProject - Will be called whenever a project ends to be used.
#
# For more information about GID internals, check the program scripts.
#---------------------------------------------------------------------------

## Create global variable

# thia variable is to set the correct condition if and its property
set g_conddict [dict create]

# this variable stores all the nodes_group condition in the model
set g_condgroup []

# this is the map from local material index (that GiD assigns to element) to the material index in the book
#unused
set g_matmap [dict create]

# this is the list of the materials in the model
set g_matlist []

# this is the dictionary of the material, the key is the material index, the value is the list of elements having that material
set g_matdict []

# create the transformation array of connectivities
# for hexahedra 20-nodes the convention from GiD is different with Abaqus
set g_hex20tr [list 1 2 3 4 5 6 7 8 9 10 11 12 17 18 19 20 13 14 15 16]
set g_hex27tr [list 1 2 3 4 5 6 7 8 9 10 11 12 17 18 19 20 13 14 15 16 27 21 26 22 23 24 25]

proc MyBitmaps { dir { type "DEFAULT INSIDELEFT"} } {
    global MyBitmapsNames MyBitmapsCommands MyBitmapsHelp kratosPriv



    set MyBitmapsNames(0) "images/Thermal.gif --- \
            images/Displacement.gif \
            images/Pressure.gif \
            images/Source.gif \
            images/BoundCond.gif \
            images/Materials.gif \
            images/Data.gif --- \
            images/Mesh.gif \
            images/Compute.gif --- \
            images/k.gif"
    set MyBitmapsCommands(0) [list \
            [ list -np- HelpWindow "CUSTOM_HELP_REFERENCE" \
		   [file join $dir html Contents.html] \
		   [file join $dir html index.html]] \
            [ list ""] \
	    [list -np- GidOpenConditions Fixed_Displacement] \
	    [list -np- GidOpenConditions Face_Pressure] \
	    [list -np- GidOpenMaterials Solids] \
	    [list -np- GidOpenProblemData] \
	    [ list ""] \
	    "Meshing generate" \
	    "Utilities Calculate" \
	    [ list ""] \
	    [list -np- WebPageKratos $kratosPriv(Web)]
    ]
    set MyBitmapsHelp(0) { "About Thermal . . ." "" \
	"Fixed Displacements" \
        "Face Pressure" \
	"Heat Sources" \
        "Velocity" \
        "Materials" \
	"Problem Data" "" \
        "Generate Mesh" \
        "Calculate" ""\
        "Kratos WebPage"}

    # prefix values:
    #          Pre        Only active in the preprocessor
    #          Post       Only active in the postprocessor
    #          PrePost    Active Always

    set prefix Pre

    set kratosPriv(toolbarwin) [CreateOtherBitmaps MyBar "My toolbar" \
	    MyBitmapsNames MyBitmapsCommands \
	    MyBitmapsHelp $dir "MyBitmaps [list $dir]" $type $prefix]
    AddNewToolbar "kratos bar" ${prefix}MyBarWindowGeom \
	    "MyBitmaps [list $dir]"
}

proc EndMyBitmaps {} {
    global kratosPriv

    ReleaseToolbar "kratos bar"
    rename MyBitmaps ""

    catch { destroy $kratosPriv(toolbarwin) }
}

proc InitGIDProject { dir } {
    global MenuNames MenuEntries MenuCommands MenuAcceler
    global MenuNamesP MenuEntriesP MenuCommandsP MenuAccelerP
    global kratosPriv
    global GidUtils

    set kratosPriv(ProgramName) "ekate"
    set kratosPriv(VersionNumber) 0.1
    set kratosPriv(Web) "http://www.cimne.upc.es/kratos/"

    #set GidVersion [.gid.central.s info GiDVersion]
    #set GidVersion [string trim $GidVersion]
    #set GidVersion [string index $GidVersion 0]

    #if { $GidVersion < 7 } {
	#WarnWin [_ "%s v%s is not compatible with GiD version lower than 7" \
	#	$kratosPriv(ProgramName) $kratosPriv(VersionNumber)]
	return
    }

    #    WarnWinText $dir

    Splash $dir 2501

    set ipos [lsearch $MenuNames Help]
    if { $ipos != -1 } {
	set MenuEntries($ipos) [linsert $MenuEntries($ipos) 0 \
                [_ "%s v%s Help" $kratosPriv(ProgramName) $kratosPriv(VersionNumber)] --- ]
	set MenuCommands($ipos) [linsert $MenuCommands($ipos) 0 \
		[list -np- HelpWindow "CUSTOM_HELP_REFERENCE" \
	        [file join $dir html Contents.html] \
		[file join $dir html index.html]] ""]
	set MenuAcceler($ipos) [linsert $MenuAcceler($ipos) 0 ""]

	lappend MenuEntries($ipos) \
	        [_ "About %s v%s" $kratosPriv(ProgramName) $kratosPriv(VersionNumber)] --- \
	        [_ "%s WebPage" $kratosPriv(ProgramName)]
	lappend MenuCommands($ipos) [list -np- Splash $dir] "" [list -np- WebPageKratos $kratosPriv(Web)]
	lappend MenuAcceler($ipos) ""

    	UpdateMenus
    }

    set ipos [lsearch $MenuNamesP Help]
    if { $ipos != -1 } {
	set MenuEntriesP($ipos) [linsert $MenuEntriesP($ipos) 0 \
                [_ "%s v%s Help" $kratosPriv(ProgramName) $kratosPriv(VersionNumber)] --- ]
	set MenuCommandsP($ipos) [linsert $MenuCommandsP($ipos) 0 \
		[list -np- HelpWindow "CUSTOM_HELP_REFERENCE" \
	        [file join $dir html Contents.html] \
		[file join $dir html index.html]] ""]
	set MenuAccelerP($ipos) [linsert $MenuAccelerP($ipos) 0 ""]

	lappend MenuEntriesP($ipos) \
	        [_ "About %s v%s" $kratosPriv(ProgramName) $kratosPriv(VersionNumber)]
	lappend MenuCommandsP($ipos) [list -np- Splash $dir]
	lappend MenuAccelerP($ipos) ""

    	UpdateMenus
    }

    MyBitmaps $dir

    GidChangeDataLabel "Data units" ""
    GidChangeDataLabel "Interval" ""
    GidChangeDataLabel "Conditions" ""
    GidChangeDataLabel "Local Axes" ""
    GidChangeDataLabel "Materials" ""

    GidAddUserDataOptions "---" "" 1
    GidAddUserDataOptions "Fixed Displacement" "GidOpenConditions Fixed_Displacement" 2
    GidAddUserDataOptions "Forces" "GidOpenConditions Forces" 3
    GidAddUserDataOptions "---" "" 4
	GidAddUserDataOptions "Fixed Pressures" "GidOpenConditions Fixed_Pressures" 5
	GidAddUserDataOptions "Surface Pressure" "GidOpenConditions Face_Pressure" 6
    GidAddUserDataOptions "---" "" 7
	GidAddUserDataOptions "Initial Conditions" "GidOpenConditions Initial_Conditions" 8
    GidAddUserDataOptions "---" "" 9
    GidAddUserDataOptions "Model Boundaries" "GidOpenConditions Model_Boundaries" 10
    GidAddUserDataOptions "Contact" "GidOpenConditions Contact" 11
    GidAddUserDataOptions "Tying" "GidOpenConditions Tying" 12
	GidAddUserDataOptions "Hydraulic Jacks" "GidOpenConditions Hydraulic_Jacks" 13
    GidAddUserDataOptions "Activation" "GidOpenConditions Activation" 14
    GidAddUserDataOptions "Groups" "GidOpenConditions Groups" 15
    GidAddUserDataOptions "---" "" 16
    GidAddUserDataOptions "Solids" "GidOpenMaterials Solids" 17
	GidAddUserDataOptions "---" "" 18
    GidAddUserDataOptions "Select Boundaries" GetBoundary 19
	GidAddUserDataOptions "Cut Model" CutModel 20

}

proc EndGIDProject {} {
    EndMyBitmaps
}

proc WebPageKratos { dir } {
    global kratosPriv

    VisitWeb $dir
}


proc HelpOnkratos { dir } {
    global kratosPriv

    WarnWin [_ "To obtain help for %s v%s, check the lates news in %s" \
			$kratosPriv(ProgramName) $kratosPriv(VersionNumber) $kratosPriv(Web)]
}

#  Modified Routine for Kratos 2003
#  February 3rd, 2003
#  Program Logo and Version

proc Splash { dir { TimeOut 0 } } {
    global GIDDEFAULT

    if { [.gid.central.s disable windows] } { return }

    if { [ winfo exist .splash]} {
	destroy .splash
	update
    }

    toplevel .splash

    set im [image create photo -file [ file join $dir images/splash.gif]]
    set x [expr [winfo screenwidth .splash]/2-[image width $im]/2]
    set y [expr [winfo screenheight .splash]/2-[image height $im]/2]

    wm geom .splash +$x+$y
    wm transient .splash .gid
    wm overrideredirect .splash 1
    pack [label .splash.l -image $im -relief ridge -bd 2]

    bind .splash <1> "destroy .splash"
    bind .splash <KeyPress> "destroy .splash"
    raise .splash .gid
    grab .splash
    focus .splash
    update

    if { $TimeOut > 0 } {
        after $TimeOut "if { [ winfo exist .splash] } { destroy .splash  }"
    }
}

#############OLD EKATE SUBROUTINES##########################
proc CutModel {} {
	#domain file path
	set domain_file [GiD_Info Project ModelName]
	set domain_file [split $domain_file "/"]
	set domain_file [lrange $domain_file 0 [expr [llength $domain_file] -2]]
	lappend domain_file "domain.sat"
	set domain_file [join $domain_file "/"]
	#WarnWin [_ $domain_file]
	#get list of all existing volumes
	set i [GiD_Info Geometry NumVolumes]
	set stop 1
	set volume_list {}
	while {$i >= $stop} {
		#determine id of new volume
		set last_volume [GiD_Info Geometry NumVolumes]
		#get layer of current volume
		set str [GiD_Info list_entities volumes $i]
		set end [string first "NumSurfaces" $str]
		set begin [string first "LAYER" $str]
		set layername [string range $str [expr $begin+7] [expr $end-2] ]
		#change to active layer
		GiD_Process Mescape View Layers ToUse $layername
		GiD_Process Mescape
		#read domain volume
		GiD_Process Mescape Files ACISRead $domain_file
		#intersect volume and domain volume
		GiD_Process Mescape Geometry Create IntSolid3D Intersect $i [expr $last_volume+1]
		#WarnWin [_ $volume_id ]
		incr i -1
	}
	GiD_Process Mescape
	#clean up geometry
	GiD_Process Mescape Geometry Delete surface InvertSelection Mescape
	GiD_Process Mescape Geometry Delete line InvertSelection Mescape
	GiD_Process Mescape Geometry Delete point InvertSelection Mescape
}

proc GetBoundary {} {
	set i 1
	set stop [GiD_Info Geometry NumSurfaces]
	#bounding box
	set bbcoords [GiD_Info layers -bbox]
	#WarnWin [_ $bbcoords ]
	set bbcoords [lindex $bbcoords 0]
	set bbcoords [split $bbcoords ]
	set bottom [expr [expr [lindex $bbcoords 2] < [lindex $bbcoords 5]] ? [lindex $bbcoords 2] : [lindex $bbcoords 5]]
	while {$i <= $stop} {
		set str [GiD_Info list_entities surfaces $i]
		set end [string first "conditions" $str]
		set begin [string first "HigherEntity" $str]
		set numVol [string range $str [expr $begin+14] [expr $end-2] ]
		#if surface is boundary
		#WarnWin [_ $str ]
		if { [string compare $numVol "1"] == 0 } {
			#GiD_Process Mescape Data Conditions AssignCond IsBoundary Change 1 $i Mescape
			#check for position of surface
			set aend [string first "Normal" $str]
			set abegin [string first "Center" $str]
			set center [string range $str [expr $abegin+8] [expr $aend-2] ]
			set center [split $center]
			#for gid_8.1.1b
			#set bend [string first "END" $str]
			#for gid_8.1.7
			set bbegin $aend
			#set normal [string range $str [expr $bbegin+8] [expr $bend-2] ]
			set normal [string range $str [expr $bbegin+8] [string length $str] ]
			set normal [split $normal]
			set znormal [expr abs([lindex $normal 2]) - 0.00001]
			if { [expr $bottom == [lindex $center 2] ] } then {
				#WarnWin [_ "Surface is bottom surface" ]
				GiD_Process Mescape Data Conditions AssignCond IsBottom Change 1 $i Mescape
			} elseif { $znormal < 0.0 } then {
					#WarnWin [_ "Surface is side surface"]
					GiD_Process Mescape Data Conditions AssignCond IsSide Change 1 $i Mescape
					#GiD_Process Mescape Data Conditions AssignCond Surface_Water_Pressure Change 1 0.0 $i Mescape
			} else {
				#WarnWin [_ "neither Bottom nor side: must be top"]
				GiD_Process Mescape Data Conditions AssignCond IsTop Change 1 $i Mescape
			}
		}
		incr i
	}
}

proc GetLayerNodes { layername } {
        set surfaces [GiD_Info layers -entities surfaces $layername ]
        #WarnWin [_ $surfaces]
	#get all lines that are attached to the surfaces belonging to the specified layer
        set lines {}
	foreach surf $surfaces {
	        set lineinfo [GiD_Info list_entities surfaces $surf]
		WarnWin [_ $lineinfo]
                set lineinfo [split $lineinfo "\n"]
                foreach line $lineinfo {
			set line [split $line]
			if {[lindex $line 0] == "Line:"} {
				lappend lines [lindex $line 1]
			}
		}

	}
        set lines [lsort -unique $lines]
	#WarnWin [_ $lines]
	#get all points belonging to the specified lines
	set points {}
	foreach line $lines {
		set lineinfo [GiD_Info list_entities lines $line]
		set lineinfo [split $lineinfo "\n"]
		foreach item $lineinfo {
			set item [split $item]
			if {[lindex $item 0] == "Points:"} {
				lappend points [lindex $item 1]
				lappend points [lindex $item 2]
			}
		}
	}
	set points [lsort -unique $points]
	#WarnWin [_ $points]
	set nodes [GiD_Info list_entities PreNodes 1]
	#WarnWin [_ $nodes]
	return $points
}

############################General subroutines#############################
## Get the Automatic Tolerance of the model
#Usage: *tcl(GetATInfo)
proc GetATInfo {} {
    set tol [GiD_Info AutomaticTolerance]
    return $tol
}

## Get the GiD version
#Usage: *tcl(GetGiDVersion)
proc GetGiDVersion {} {
    set ver [GiD_Info GiDVersion]
    return $ver
}

## Get the number of elements of the model
#Usage: *tcl(GetNumElements)
proc GetNumElements {} {
    set ne [GiD_Info Mesh NumElements]
    return $ne
}

## Get an element of specific type and element id
#Usage: *tcl(GetElement Hexahedra an_id)
proc GetElement { elemtype e_id } {
    set e [GiD_Info Mesh Elements $elemtype $e_id $e_id]
    return $e
}

## Get an element of specific type and element id
#Usage: *tcl(GetElement an_id)
proc GetElement2 { e_id } {
    set e [GiD_Info Mesh Elements Any $e_id $e_id]
    return $e
}

## List an element by element id
#Usage: *tcl(ListElement an_id)
proc ListElement { e_id } {
    set e_info [GiD_Info list_entities Elements $e_id]
    return $e_info
}

## Get the layer of the element i
#Usage: *tcl(GetElement Hexahedra an_id)
proc GetLayer { e_id } {
    set e_info [GiD_Info list_entities Elements $e_id]
    set e_layer [lindex $e_info 10]
    return $e_layer
}

## Get the information of a condition of cond_name
#Usage: *tcl(GetCondition a_cond_name)
proc GetCondition { cond_name } {
    set c_info [GiD_Info conditions $cond_name]
    return $c_info
}

proc Initialize {} {
    global g_conddict
    global g_condgroup
    global g_matmap
    global g_matlist
    global g_matdict
    set g_condgroup []
    set g_matmap [dict create]
    set g_matlist [GiD_Info materials]
    set g_matdict [dict create]
    set g_conddict [dict create]
    return "//Hello from TCL. Are you OK today?"
}

##################Subroutines handle conditions#############################
proc SaveCond { cond_type args } {
    global g_conddict
    dict append g_conddict $cond_type "$args\n"
    return ""
}

proc GetCond { cond_type } {
    global g_conddict
    if { [dict exists $g_conddict $cond_type] } {
        return [dict get $g_conddict $cond_type]
    } else {
        return ""
    }
}

######################SUBROUTINES HANDLING MATERIALS###################

## save to material map
# elems_mat: material id that GiD assignes to the element (it's a random number, I supposed)
# elems_num: id of the element
# Usage: *loop elems
#        *tcl(SaveElemsMat *ElemsMat *ElemsNum)*\
#        *end elems
proc SaveElemsMat { elems_mat elems_num } {
    set e_info [GiD_Info list_entities Elements $elems_num]
    set e_mat [lindex $e_info 8]
    global g_matmap
    dict set g_matmap $elems_mat $e_mat
    return ""
}

## get the name of the material in the book based on the element material id (as above this is assigned randomly by GiD)
# Usage: *tcl(GetMatName *MatNum) (put inside *loop materials)
proc GetMatName { elems_mat } {
    set mat_list [GiD_Info materials]
    global g_matmap
    if { [dict exists $g_matmap $elems_mat] } {
        return [lindex $mat_list [expr {[dict get $g_matmap $elems_mat] - 1}]]
    #    return $g_matmap
    } else {
        return "Element of material $elems_mat is not assigned material\n"
    }
}

######################SUBROUTINES HANDLING NODE GROUPS###################
proc AddCondGroupName { group_name } {
    global g_condgroup
    if {[lsearch -exact $g_condgroup $group_name] < 0} {
        lappend g_condgroup $group_name
    }
    return ""
}

proc InitializeNodeGroups {} {
    global g_condgroup
    set output "node_groups = {}"
    foreach group_name $g_condgroup {
        set output "$output\n    node_groups\['$group_name'\] = \[\]"
    }
    return $output
}

############################ABAQUS interface#############################
## Write the elemens connectivities and materials to ABAQUS .inp file
# this version is an all-in-one solution and prone to error, use the separate version instead
proc WriteAbaqusInp {} {
    # initialize output
    set output ""

    global g_hex20tr
    global g_hex27tr

    # initialize the material dictionary
    set matdict [dict create]

    # extract all the elements in the mesh
    set all_elems [GiD_Info Mesh Elements Any -array]
    # It will return, i.e
    # Hexahedra {1 2 3 4 5 6 7 8} {{23 56 16 47 14 46 6 32} {15 23 7 16 5 14 1 6} {43 54 15 23 30 42 5 14} {54 76 23 56 42 70 14 46} {55 77 44 71 23 56 16 47} {45 55 31 44 15 23 7 16} {69 75 45 55 43 54 15 23} {75 81 55 77 54 76 23 56} {20 41 12 29 8 25 3 18} {27 39 11 21 17 26 2 9} {48 64 20 41 33 57 8 25} {39 68 21 53 26 61 9 37} {40 67 24 62 22 52 13 38} {28 40 19 24 10 22 4 13} {58 63 28 40 34 49 10 22} {63 79 40 67 49 73 22 52} {50 66 35 59 20 41 12 29} {60 65 36 51 27 39 11 21} {72 78 50 66 48 64 20 41} {65 80 51 74 39 68 21 53}} {8 8 8 8 8 8 8 8}

    foreach elems_info $all_elems {
        # set output "$output\nelements information:$elems_info"

        # extract the geometry type, i.e Hexahedra, Tetrahedra
        set geom_type [lindex $elems_info 0]
        # set output "$output\ngeometry type:$geom_type"

        # extract the list of elements associated with this type of geometry
        set elems_list [lindex $elems_info 1]
        # set output "$output\nelements list:$elems_list"

        # get the information of each element in the list
        foreach e $elems_list {
            set e_info [GiD_Info list_entities Elements $e]
            # set output "$output\nelement_info:$e_info"

            # extract the information based on observation of the index. I don't know if this will be changed in future version of GiD or not.
            set e_id [lindex $e_info 2]
            set e_mat [lindex $e_info 8]
            set e_conn [lrange $e_info 12 [expr {[llength $e_info]-2}]]
            # set output "$output--\n$e_id\n$e_mat\n$e_conn"

            # append the element to material dictionary
            dict append matdict $e_mat " $e_id"

            # write the element
            set output "$output\n*ELEMENT, TYPE=C3D[llength $e_conn]"
            set output "$output\n$e_id"

            # account for the different in connectivity sequence
            if {[string match $geom_type "Hexahedra"] && [expr {[llength $e_conn] == 20}]} {
                for {set i 0} {$i < [llength $e_conn]} {incr i} {
                    set output "$output, [lindex $e_conn [expr {[lindex $g_hex20tr $i] - 1}]]"
                }
            } elseif {[string match $geom_type "Hexahedra"] && [expr {[llength $e_conn] == 27}]} {
                for {set i 0} {$i < [llength $e_conn]} {incr i} {
                    set output "$output, [lindex $e_conn [expr {[lindex $g_hex27tr $i] - 1}]]"
                }
            } else {
                foreach n $e_conn {
                    set output "$output, $n"
                }
            }
        }
    }

    # write the material
    set output "$output\n"
    # set output "$output\nmaterial dictionary:$matdict"

    # get the list of material in the model
    set mat_list [GiD_Info materials]
    # set output "$output\nlist of material:$mat_list"

    # loop through each material and write the material record
    foreach mat $mat_list {
#        set output "$output\n$mat"
        set mat_info [GiD_Info materials $mat]
        set constitutive_law [lindex $mat_info 2]
        set output "$output\n*MATERIAL,NAME=$mat"

        # TODO extract relevant information of each material model
    #    set output "$output\n[lindex $mat_info 0]"
        # foreach i $mat_info {
        #     set output "$output\n$i"
        # }
        # set output "$output\n"
    }

    # write the material set
    set output "$output\n"
    dict for {mat_id e_list} $matdict {
        set output "$output\n*ELSET,ELSET=[lindex $mat_list [expr {$mat_id -1}]]\_Set"
        foreach e $e_list {
            set output "$output\n$e,"
        }
    }

    return $output
}

#proc WriteAbaqusInpElements {e_id} {
#    set output ""

#    global g_hex20tr
#    global g_hex27tr
#    global g_matdict

##    set e_info [GiD_Info list_entities -more Elements $e_id]
###    set output "$output\nelements information:$e_info"
###    this will return, i.e.
###    elements information:ELEMENTS
###    Num: 1 HigherEntity: 0 conditions: 1 material: 8
###    LAYER: Layer0
###    1 23 11 22 27 10 1 9 21 17 16 25 26 15 4 13 24 2 3 12 14 20 7 6 18 19 5 8 8
###    Type=Hexahedra Nnode=27 Volume=1
#    #NOTE: We can get the geom_type here

##    set e_info [GiD_Info list_entities Elements $e_id]
###    set output "$output\nelements information:$e_info"
###    this will return, i.e.
###    elements information:ELEMENTS
###    Num: 1 HigherEntity: 0 conditions: 1 material: 8
###    LAYER: Layer0
###    1 23 11 22 27 10 1 9 21 17 16 25 26 15 4 13 24 2 3 12 14 20 7 6 18 19 5 8 8

##    # extract the information based on observation of the index. I don't know if this will be changed in future version of GiD or not.
##    set e_mat [lindex $e_info 8]
##    set e_conn [lrange $e_info 12 [expr {[llength $e_info]-2}]]
###    set output "$output--\n$e_id\n$e_mat\n$e_conn"

#    set e_info [GiD_Info Mesh Elements Any $e_id $e_id]

#    set e_mat [lindex $e_info [expr {[llength $e_info]-1}]]
#    set e_conn [lrange $e_info 1 [expr {[llength $e_info]-2}]]

#    # append the element to the material dictionary
#    dict append g_matdict $e_mat " $e_id"

#    # write the element
#    set output "$output*ELEMENT, TYPE=C3D[llength $e_conn]"
#    set output "$output\n$e_id"

#    # account for the different in connectivity sequence
#    if {[expr {[llength $e_conn] == 20}]} {
#        for {set i 0} {$i < [llength $e_conn]} {incr i} {
#            set output "$output, [lindex $e_conn [expr {[lindex $g_hex20tr $i] - 1}]]"
#        }
#    } elseif {[expr {[llength $e_conn] == 27}]} {
#        for {set i 0} {$i < [llength $e_conn]} {incr i} {
#            set output "$output, [lindex $e_conn [expr {[lindex $g_hex27tr $i] - 1}]]"
#        }
#    } else {
#        foreach n $e_conn {
#            set output "$output, $n"
#        }
#    }

#    return $output
#}

# Usage: *tcl(WriteAbaqusInpElements *ElemsNum *ElemsType)
proc WriteAbaqusInpElements {e_id e_type} {
    set e_info [GiD_Info Mesh Elements Any $e_id $e_id]

    set e_mat [lindex $e_info [expr {[llength $e_info]-1}]]
    set e_conn [lrange $e_info 1 [expr {[llength $e_info]-2}]]

    return [WriteAbaqusInpElements2 $e_id $e_type $e_mat $e_conn]
}

# Usage: *tcl(WriteAbaqusInpElements *ElemsNum *ElemsType *ElemsMat *ElemsConec) # for some reason it doesn't work yet
proc WriteAbaqusInpElements2 {e_id e_type e_mat e_conn} {
    set output ""

    global g_hex20tr
    global g_hex27tr
    global g_matdict

    # append the element to the material dictionary
    dict append g_matdict $e_mat " $e_id"

    # write the element
    if { $e_type == 1 } {
        # only 3D beam is supported
        set output "$output*ELEMENT, TYPE=B3[expr {[llength $e_conn] - 1}]"
    } elseif { $e_type == 2 || $e_type == 3 } {
        set output "$output*ELEMENT, TYPE=S[llength $e_conn]"
    } elseif { $e_type == 4 || $e_type == 5 } {
        set output "$output*ELEMENT, TYPE=C3D[llength $e_conn]"
    } else {
        set output "$output*ELEMENT, TYPE=$e_type"
    }
    set output "$output\n$e_id"

    # account for the different in connectivity sequence
    if {[expr {[llength $e_conn] == 20}]} {
        for {set i 0} {$i < [llength $e_conn]} {incr i} {
            set output "$output, [lindex $e_conn [expr {[lindex $g_hex20tr $i] - 1}]]"
        }
    } elseif {[expr {[llength $e_conn] == 27}]} {
        for {set i 0} {$i < [llength $e_conn]} {incr i} {
            set output "$output, [lindex $e_conn [expr {[lindex $g_hex27tr $i] - 1}]]"
        }
    } else {
        foreach n $e_conn {
            set output "$output, $n"
        }
    }

    return $output
}

proc WriteAbaqusInpMaterials {} {
    set output ""

    global g_matlist
    global g_matdict

    # loop through each material and write the material record
    foreach mat $g_matlist {
#        set output "$output\n$mat"
        set mat_info [GiD_Info materials $mat]
#        set constitutive_law [lindex $mat_info 2]
        set output "$output\n*MATERIAL,NAME=$mat"

        # TODO extract relevant information of each material model
    #    set output "$output\n[lindex $mat_info 0]"
        # foreach i $mat_info {
        #     set output "$output\n$i"
        # }
        # set output "$output\n"
    }

    # write the material set
    set output "$output\n"
    dict for {mat_id e_list} $g_matdict {
        set output "$output\n*ELSET,ELSET=[lindex $g_matlist [expr {$mat_id -1}]]\_Set"
        foreach e $e_list {
            set output "$output\n$e,"
        }
    }

    return $output
}

