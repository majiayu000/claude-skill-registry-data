---
name: smartassembly
description: >
  Expert-level SmartAssembly scripting for SIGMAXIM's Creo Parametric automation.
  Use for: .tab script writing/review/debug, CREATE_UDF/ASSEMBLE commands,
  BEGIN_GUI_DESCR/BEGIN_TAB_DESCR configuration, INCLUDE modular design,
  BEGIN_CATCH_ERROR error handling, feature/reference manipulation,
  Excel integration (EXCEL_* commands), drawing automation (CREATE_DRW_*),
  PDF export (EXPORT_DRW_PDF), XML manipulation (READ/MODIFY_FEATURE_XML),
  JSON commands (JSON_LOAD_DOCUMENT, JSON_GET_VALUE, JSON_SET_VALUE for REST API/data exchange),
  PowerShell-Creo COM API integration, manufacturing workflows (Model→Drawing→Export→PDF),
  path system (SA_Paths.txt, lib: prefix), product patterns (Counters, WorkTables, Tops,
  DishTables, Wall_Panels, Curbs, Channels), vector geometry analysis, map operations,
  multi-stage GUI, auto-generation logic, field joints, material selection, or any
  PTC Creo automation scripting.
---

# SmartAssembly Scripting Language

SmartAssembly is SIGMAXIM's proprietary scripting language for Creo Parametric automation. It uses Creo's Toolkit API to automate parametric modeling, component assembly, UDF creation, drawing generation, and manufacturing workflows for industrial kitchen equipment.

## Quick Start

**New to SmartAssembly?** Start here:
1. Read **Script Structure** below for .tab file anatomy
2. Review **path-system.md** for lib: prefix and SA_Paths.txt configuration
3. Study **Variable Types** for DECLARE_VARIABLE patterns
4. Check **Reference Guide** section to find the right documentation for your task

**Common Tasks:**
- Creating UDFs → **commands-udf.md** + **UDF Creation Patterns** below
- Building GUIs → **commands-gui.md** + **gui-patterns.md**
- Excel integration → **excel-integration.md**
- JSON/REST API → **json-commands.md**
- Drawing/export → **manufacturing-workflows.md**
- Product modules → **product-patterns.md**
- PowerShell orchestration → **powershell-integration.md**

## Script Structure

Every SmartAssembly script (.tab file) follows this three-section structure:

```
!  © 2023 Company Name
! Optional copyright header

!---------------------------------------------------------------------------------
BEGIN_GUI_DESCR          ! Optional: User interface definition
    ! GUI elements, pictures, user inputs
    ! Conditional logic for dynamic UI
END_GUI_DESCR
!---------------------------------------------------------------------------------

!---------------------------------------------------------------------------------
BEGIN_TAB_DESCR          ! Optional: Table-driven configuration
    BEGIN_TABLE name "Title"
        ! Table definition
    END_TABLE
END_TAB_DESCR
!---------------------------------------------------------------------------------

!---------------------------------------------------------------------------------
BEGIN_ASM_DESCR          ! Required: Main automation logic

    !-----------------------------------------------------------------------
    ! Declare all variables / references / arrays
    !-----------------------------------------------------------------------
    ! Variable declarations organized by type

    ! Main processing logic
    ! UDF creation, feature operations

    WINDOW_ACTIVATE      ! Activate window for user at end

END_ASM_DESCR
!---------------------------------------------------------------------------------
```

## Comments

```
! Single line comment
/* Multi-line
   comment block */
```

## Variable Types and Declaration

Always organize declarations by type at script start:

```
!-----------------------------------------------------------------------
! Declare all variables / references / arrays
!-----------------------------------------------------------------------
! Strings
DECLARE_VARIABLE STRING UDF_DIR "udfs"
DECLARE_VARIABLE STRING UDF_NAME
DECLARE_VARIABLE STRING NAME ""

! Integers
DECLARE_VARIABLE INTEGER DONE 0
DECLARE_VARIABLE INTEGER i 0
DECLARE_VARIABLE INTEGER FEAT_COUNT

! Doubles
DECLARE_VARIABLE DOUBLE THICKNESS 0.075
DECLARE_VARIABLE DOUBLE CURRENT_DIST
DECLARE_VARIABLE DOUBLE MIN_DIST 100

! Booleans
DECLARE_VARIABLE BOOL CURB_BODY FALSE
DECLARE_VARIABLE BOOL START_SPACER TRUE

! References (Creo geometry)
DECLARE_REFERENCE SKEL_MDL
DECLARE_REFERENCE GROUP_HEAD
DECLARE_REFERENCE FLANGE_SURFACE

! Arrays
DECLARE_ARRAY FEATURES_TO_GROUP
DECLARE_ARRAY ARRAY_ALL_SURFS
DECLARE_ARRAY ARRAY_DIMS

! Maps
DECLARE_MAP STRING SUBASMS_MAP
DECLARE_MAP INTEGER FIELD_JOINTS_MAP

! Structures
DECLARE_STRUCT POINT pos
DECLARE_STRUCT VECTOR direction
DECLARE_STRUCT PDF_OPTION option
!-----------------------------------------------------------------------
```

## Control Structures

### Conditional Statements
```
IF condition
    ! code
ELSE_IF other_condition
    ! code
ELSE
    ! code
END_IF

! Multiple conditions
IF STOCKTYPE == 1 AND stof(THICKNESS) < 1.0
    ! code
END_IF

IF NOT REF_VALID SURF1 OR NOT REF_VALID SURF2
    ! code
END_IF
```

### Loop Structures
```
! For loop over array
FOR item REF ARRAY my_array
    ! code using item
    BREAK      ! exit loop
    CONTINUE   ! next iteration
END_FOR

! For loop over map
FOR ELEM REF MAP my_map
    key = ELEM.key
    value = ELEM.value
END_FOR

! While loop with counter
i = 1
WHILE i <= NUM_FEATS
    GET_GROUP_FEATURE GROUP_HEAD i CURRENT_FEAT
    i++
END_WHILE

! Infinite loop with explicit break
WHILE "A" <> "B"
    ! Processing
    IF condition
        BREAK
    END_IF
END_WHILE
```

## GUI Development Patterns

### Main GUI with Checkboxes
```
BEGIN_GUI_DESCR
    CHECKBOX_PARAM INTEGER MAIN_DONE "Y/N"

    IF MAIN_DONE == 0
        ! Radio button for material selection
        RADIOBUTTON_PARAM INTEGER CURB_MATERIAL "Galv" "All SS"

        ! Conditional checkbox visibility (mutually exclusive options)
        IF NOT OPTION_B AND NOT OPTION_C
            CHECKBOX_PARAM BOOL OPTION_A "#1"

            IF OPTION_A
                USER_INPUT_PARAM DOUBLE THICKNESS REQUIRED
                USER_SELECT_MULTIPLE COMPOSITE_CURVE -1 CURB_CURVES FILTER_GEOM FILTER_ARRAY
            END_IF
        END_IF

        IF NOT OPTION_A AND NOT OPTION_C
            CHECKBOX_PARAM BOOL OPTION_B "#2"
        END_IF
    ELSE
        ! Reset all when done
        OPTION_A = FALSE
        OPTION_B = FALSE
        OPTION_C = FALSE
    END_IF
END_GUI_DESCR
```

### Optional User Selection with Delete
```
BEGIN_GUI_DESCR
    CHECKBOX_PARAM INTEGER DONE "Y/N"

    IF DONE == 0
        ! Show delete option only if items exist
        IF NOT ARRAY_EMPTY ARRAY_EXISTING_ITEMS
            USER_SELECT_MULTIPLE_OPTIONAL FEATURE_PARAM "ITEM_PARAM" -1 ITEMS_TO_DELETE
        END_IF

        ! Show add inputs only if not deleting
        IF ARRAY_EMPTY ITEMS_TO_DELETE
            USER_SELECT EDGE DRIVING_EDGE FILTER_GEOM ARRAY_EDGES
            USER_INPUT_PARAM DOUBLE OFFSET TOOLTIP "Offset distance from edge"
        END_IF
    END_IF
END_GUI_DESCR
```

### Placeholder/Spacer Pattern
```
! Use impossible condition to create visual spacing in GUI
IF "A" == "B"
    CHECKBOX_PARAM INTEGER BLANK_TEMP ""
END_IF
```

## UDF Creation Patterns

### Standard UDF with Dynamic Path
```
UDF_NAME = "curb_stringer_recess_l"

CREATE_UDF "lib:"+&UDF_DIR+"\\"+&UDF_NAME SKEL_MDL REMOVE_UDF_RELATIONS UDF_GROUP
    UDF_REF "DRIVING_EDGE" DRIVING_EDGE
    UDF_REF "BACK_EDGE" SECOND_EDGE
    UDF_REF "TOP_FLANGE_SURFACE" FLANGE_SURFACE
    UDF_REF "FLOOR_PLN" SUB_FLOOR_PLN

    UDF_EXP_REF GROUP_HEAD FEATURE 0
    UDF_EXP_REF ROUND_FEAT FEATURE 6
    UDF_EXP_REF EXTRUDE_CUT FEATURE 7
END_CREATE_UDF
UNGROUP_FEATURES UDF_GROUP
```

### UDF with Error Handling and Fallback
```
CLEAR_CATCH_ERROR
BEGIN_CATCH_ERROR
    UDF_NAME = "curb_knuckle_l"
    CREATE_UDF "lib:"+&UDF_DIR+"\\"+&UDF_NAME SKEL_MDL REMOVE_UDF_RELATIONS UDF_GROUP
        UDF_REF "BREAK_EDGE" BREAK_EDGE
        UDF_REF "BREAK_SURF" BREAK_SURF
        UDF_EXP_REF GROUP_HEAD FEATURE 0
    END_CREATE_UDF
    UNGROUP_FEATURES UDF_GROUP
    SET_REF_NAME GROUP_HEAD "KNUCKLE_L_"+*
END_CATCH_ERROR

! Try alternate UDF if first fails
IF ERROR
    CLEAR_CATCH_ERROR
    BEGIN_CATCH_ERROR
        UDF_NAME = "curb_knuckle_r"
        CREATE_UDF "lib:"+&UDF_DIR+"\\"+&UDF_NAME SKEL_MDL REMOVE_UDF_RELATIONS UDF_GROUP
            UDF_REF "BREAK_EDGE" BREAK_EDGE
            UDF_REF "BREAK_SURF" BREAK_SURF
            UDF_EXP_REF GROUP_HEAD FEATURE 0
        END_CREATE_UDF
        UNGROUP_FEATURES UDF_GROUP
        SET_REF_NAME GROUP_HEAD "KNUCKLE_R_"+*
    END_CATCH_ERROR
END_IF
```

### Post-UDF Dimension Manipulation
```
CREATE_UDF lib:udfs\component SKEL_MDL UDF_GROUP
    UDF_EXP_REF EXTRUDE_FEAT FEATURE 4
END_CREATE_UDF
UNGROUP_FEATURES UDF_GROUP

! Get and modify dimensions after creation
CLEAR_ARRAY ARRAY_DIMS
GET_FEATURE_DIMS EXTRUDE_FEAT ARRAY_DIMS

DIM_COUNT = 0
FOR EACH_DIM REF ARRAY ARRAY_DIMS
    GET_DIM_VALUE EACH_DIM value

    IF abs(value) == 1.875
        SPACER_OFFSET_COUNT = DIM_COUNT
    END_IF

    DIM_COUNT++
END_FOR

GET_ARRAY_ELEM ARRAY_DIMS SPACER_OFFSET_COUNT CURRENT_OFFSET_DIM
SET_DIM_VALUE CURRENT_OFFSET_DIM NEW_VALUE
SET_DIM_SYMBOL CURRENT_OFFSET_DIM "UNIQUE_SYMBOL_"+itos(NUM)
```

## Surface and Edge Analysis Patterns

### Vector Direction Analysis
```
! Get normal direction of reference plane
GET_SURFACE_NORM NULL SUB_FLOOR_PLN SB_POS SB_VEC
VECTOR_NORMALIZE SB_VEC

! Compare surface/edge direction to reference
FOR EACH_EDGE REF ARRAY CONTOUR.array_edges
    GET_LINE_DATA NULL EACH_EDGE LINE_DATA
    VECTOR_FROM_POINTS LINE_DATA.pnt_from LINE_DATA.pnt_to LINE_VEC
    VECTOR_NORMALIZE LINE_VEC

    ! Check if edge is parallel to reference plane normal (vertical)
    IF abs(LINE_VEC.x) == abs(SB_VEC.x) AND abs(LINE_VEC.y) == abs(SB_VEC.y) AND abs(LINE_VEC.z) == abs(SB_VEC.z)
        ADD_ARRAY_ELEM VERTICAL_EDGES EACH_EDGE
    ELSE
        ! Horizontal edge - find closest to floor
        MEASURE_DISTANCE SUB_FLOOR_PLN EACH_EDGE EDGE_DIST
        IF EDGE_DIST < CURRENT_DIST
            CURRENT_DIST = EDGE_DIST
            COPY_REF EACH_EDGE BOTTOM_EDGE
        END_IF
    END_IF
END_FOR
```

### Surface Contour Processing
```
! Get external contour
GET_SURFACE_CONTOUR SURF EXTERNAL SURF_CONTOUR

! Process edges in contour
FOR EACH_EDGE REF ARRAY SURF_CONTOUR.array_edges
    GET_REF_VERTEX EACH_EDGE START START_PNT
    GET_REF_VERTEX EACH_EDGE END END_PNT

    GET_REF_POS NULL START_PNT START_POS
    GET_REF_POS NULL END_POS END_POS

    VECTOR_FROM_POINTS START_POS END_POS EDGE_VEC
    VECTOR_NORMALIZE EDGE_VEC
END_FOR
```

### Finding Opposing Surfaces (Field Joint Pattern)
```
FOR POTENTIAL_FJS1 REF ARRAY POTENTIAL_FIELD_SURFS
    GET_SURFACE_NORM DEFAULT_CSYS POTENTIAL_FJS1 FJS1_POS FJS1_VEC
    VECTOR_NORMALIZE FJS1_VEC

    FOR POTENTIAL_FJS2 REF ARRAY POTENTIAL_FIELD_SURFS
        IF REF_EQUAL POTENTIAL_FJS1 POTENTIAL_FJS2
            CONTINUE
        END_IF

        GET_SURFACE_NORM DEFAULT_CSYS POTENTIAL_FJS2 FJS2_POS FJS2_VEC
        VECTOR_NORMALIZE FJS2_VEC

        ! Check if surfaces face opposite directions
        IF FJS1_VEC.x == -1*FJS2_VEC.x AND FJS1_VEC.y == -1*FJS2_VEC.y AND FJS1_VEC.z == -1*FJS2_VEC.z
            MEASURE_DISTANCE POTENTIAL_FJS1 POTENTIAL_FJS2 DIST

            IF DIST <= 0.1
                ! Found matching field joint surfaces
            END_IF
        END_IF
    END_FOR
END_FOR
```

## Feature Group Iteration Pattern

```
! Get group info
GET_GROUP_FEATURE_NUM GROUP_HEAD NUM_FEATS
GET_GROUP_HEAD GROUP_HEAD HEAD

! Iterate through group features
FEAT_COUNT = 1
WHILE FEAT_COUNT <= NUM_FEATS
    GET_GROUP_FEATURE GROUP_HEAD FEAT_COUNT CURRENT_FEAT

    ! Get feature properties
    GET_FEATURE_TYPE CURRENT_FEAT CURRENT_FEAT_TYPE
    GET_FEATURE_SUBTYPE_NAME CURRENT_FEAT CURRENT_FEAT_SUBTYPE
    GET_FEATURE_NAME CURRENT_FEAT CURRENT_FEAT_NAME

    IF CURRENT_FEAT_TYPE == "GEOM_COPY"
        SET_FEAT_PARAM CURRENT_FEAT "CURB_GROUP" CURB_NUM
    END_IF

    IF CURRENT_FEAT_SUBTYPE == "*SWEEP*"
        SET_FEAT_PARAM CURRENT_FEAT "STRINGER" TRUE
    END_IF

    ! Check for failed features
    IF IS_FAILED CURRENT_FEAT
        ! Handle failure
        BREAK
    END_IF

    FEAT_COUNT++
END_WHILE
```

## Feature Parameter Tracking Pattern

```
! Set tracking parameters for later identification
SET_FEAT_PARAM CURB_QUILT "CURB" CURB_NUM
SET_FEAT_PARAM GROUP_HEAD "CURB_GROUP" CURB_NUM
SET_FEAT_PARAM SWEEP_FEAT "STRINGER" TRUE

! Search by parameter later
SEARCH_MDL_REFS SKEL_MDL FEATURE_PARAM "CURB_GROUP" CURB_GROUP_FEATURES
SEARCH_MDL_REFS SKEL_MDL FEATURE_PARAM "STRINGER" ARRAY_STRINGERS

! Search with specific value
SEARCH_MDL_REFS SKEL_MDL FEATURE_PARAM "CURB_GROUP" WITH_CONTENT INTEGER CG_NUM CURB_GROUP_FEATURES
```

## Reference Parameter Pattern

```
! Set reference parameter on geometry (edges, surfaces)
SET_REF_PARAM EACH_EDGE "BREAK_EDGE" "BREAK_EDGE"

! Search by reference parameter
SEARCH_MDL_REFS SKEL_MDL EDGE_PARAM "BREAK_EDGE" ARRAY_BREAK_EDGES
```

## Excel Integration Pattern

```
! Start Excel if not connected
IF NOT EXCEL_CONNECTED
    EXCEL_START !INVISIBLE
END_IF

! Load document
CLEAR_CATCH_ERROR
BEGIN_CATCH_ERROR
    EXCEL_LOAD_DOCUMENT DXF_DIRECTORY+"\\"+BOM_DOCUMENT_NAME
END_CATCH_ERROR

EXCEL_TO_FOREGROUND
EXCEL_ACTIVATE_DOCUMENT BOM_DOCUMENT_NAME
EXCEL_ACTIVATE_SHEET SHEET_BY_NAME "LISTING"

! Read/write cells
EXCEL_GET_VALUE EXCEL_ROW 1 EXCEL_COMPONENT_NAME
EXCEL_GET_VALUE EXCEL_ROW 2 STOCKTYPE
EXCEL_SET_VALUE EXCEL_ROW 20 ASM_CODE

! Process rows until empty
EXCEL_ROW = 6
WHILE EOF == "FALSE"
    EXCEL_GET_VALUE EXCEL_ROW 1 COMPONENT_NAME

    IF COMPONENT_NAME == ""
        BREAK
    END_IF

    ! Process row...

    EXCEL_ROW++
END_WHILE

! Save and close
EXCEL_SAVE_DOCUMENT DXF_DIRECTORY+"\\"+BOM_DOCUMENT_NAME+EXCEL_EXT
EXCEL_CLOSE_DOCUMENT
EXCEL_DISCONNECT
```

## XML Feature Manipulation Pattern

```
! Read feature XML for modification
GET_WORKING_DIRECTORY WORKING_DIR
GET_REF_NAME SKEL_MDL NAME
NAME = NAME + ".prt"

! Clean up old files
BEGIN_CATCH_ERROR
    DELETE_FILE WORKING_DIR+\+"existing.xml"
    DELETE_FILE WORKING_DIR+\+"modified.xml"
END_CATCH_ERROR
CLEAR_CATCH_ERROR

! Read current feature XML
READ_FEATURE_XML REMOVE_FEAT WORKING_DIR+\+"existing.xml"
WAIT_FOR_FILE WORKING_DIR+\+"existing.xml" TIMEOUT 10.0

! Open files for modification
FILE_OPEN WORKING_DIR+\+"existing.xml" "r" EXISTING_XML
FILE_OPEN WORKING_DIR+\+"modified.xml" "w" NEW_XML

! Process XML line by line
WHILE NOT FILE_END EXISTING_XML
    FILE_READ_LINE EXISTING_XML eachLINE
    FILE_WRITE_LINE NEW_XML eachLINE

    ! Insert additional XML at specific location
    IF strfind(eachLINE, "</PRO_XML_SRFCOLL_REF>") > -1
        FOR eachID REF ARRAY ID_NUMBERS
            FILE_WRITE_LINE NEW_XML "              <PRO_XML_SRFCOLL_REF type=\"compound\">"
            FILE_WRITE_LINE NEW_XML "                <PRO_XML_REFERENCE_ID type=\"id\">"+itos(eachID)+"</PRO_XML_REFERENCE_ID>"
            FILE_WRITE_LINE NEW_XML "              </PRO_XML_SRFCOLL_REF>"
        END_FOR
    END_IF
END_WHILE

FILE_CLOSE EXISTING_XML
FILE_CLOSE NEW_XML

! Apply modified XML to feature
MODIFY_FEATURE_XML REMOVE_FEAT WORKING_DIR+\+"modified.xml"

! Cleanup
DELETE_FILE WORKING_DIR+\+"existing.xml"
DELETE_FILE WORKING_DIR+\+"modified.xml"
```

## Drawing Automation Pattern

```
! Retrieve template drawing
USE_LIBRARY_MDL lib:dxf_temp DRAWING dxf

! Create drawing view
CREATE_DRW_VIEW_GENERAL dxf DXF_COMP VIEW SCALE X_POS Y_POS ANGLE dxfView
SET_DRW_VIEW_TANGENT_EDGE_DISPLAY dxfView NONE
SET_DRW_VIEW_DISPLAY dxfView NO_HIDDEN

! Create notes
CREATE_DRW_NOTE refDrawing X Y "Text" HEIGHT 0.375 HORIZONTAL LEFT refNote

! Process multiple sheets
GET_DRW_SHEET_NUM refDrawing numberSheets
i = 1
WHILE i <= numberSheets
    SET_DRW_CUR_SHEET refDrawing i

    ! Process sheet...

    i++
END_WHILE

! Export PDF with options
DECLARE_STRUCT PDF_OPTION option
option.sheets = "CURRENT"
option.color_depth = "gray"
option.use_pentable = "TRUE"
option.launch_viewer = "FALSE"

EXPORT_DRW_PDF refDrawing option DIRECTORY+\+PDF_NAME

! Cleanup
GET_DRW_MDL dxf DXF_MDL
DELETE_DRW_MDL dxf DXF_MDL
DELETE_FILE "*.log*"
```

## Processing Box (Progress Indicator) Pattern

```
PROCESSING_BOX_START "Identifying Break Edges...Please Wait!"

GET_ARRAY_SIZE EDGES_TO_PROCESS NUM_EDGES

EDGE_COUNT = 1
FOR EACH_EDGE REF ARRAY EDGES_TO_PROCESS
    PROCESSING_BOX_SET_STATE (EDGE_COUNT/NUM_EDGES)*100

    ! Processing logic...

    EDGE_COUNT++
END_FOR

PROCESSING_BOX_END
```

## Message Box Patterns

```
! Simple message
MESSAGE_BOX IMAGE lib:Images\Attention.gif "No 'CURB_SKETCH' found!\n\nPlease select curves."

! Message box with buttons
DECLARE_ARRAY arrayButtons
ADD_ARRAY_ELEM arrayButtons "KEEP"
ADD_ARRAY_ELEM arrayButtons "FLIP X"
ADD_ARRAY_ELEM arrayButtons "FLIP Z"

MESSAGE_BOX_EX SCREEN_LOCATION BOTTOM_CENTER QUESTION "CORRECT CSYS DIRECTION?" "What should we do" arrayButtons paramChoice

IF paramChoice == 1
    ! User chose "KEEP"
ELSE_IF paramChoice == 2
    ! User chose "FLIP X"
END_IF
```

## INCLUDE Module Pattern

### Main Script Calling Modules
```
! Conditional includes based on user selection
IF STRINGERS
    INCLUDE lib:Curb_Stringers.tab
END_IF

IF FIELD_JOINTS
    INCLUDE lib:Curb_Field_Joints.tab
END_IF

! Shared utility include
INCLUDE lib:Curb_Set_Feat_Group_Num.tab

! Path relative include
INCLUDE lib:..\\Flip_Csys_Direction.tab
```

### Module Script Structure
```
! Module that expects inherited variables
BEGIN_ASM_DESCR

!-----------------------------------------------------------------------
! Declare module-specific variables only
!-----------------------------------------------------------------------
DECLARE_VARIABLE INTEGER DIM_INDEX
DECLARE_ARRAY MODULE_ARRAY
!-----------------------------------------------------------------------

! Use inherited variables from parent (SKEL_MDL, GROUP_HEAD, CURB_NUM, etc.)
GET_GROUP_FEATURE_NUM GROUP_HEAD NUM_FEATS

FEAT_COUNT = 1
WHILE FEAT_COUNT <= NUM_FEATS
    GET_GROUP_FEATURE GROUP_HEAD FEAT_COUNT CURRENT_FEAT

    ! Process using inherited context...

    FEAT_COUNT++
END_WHILE

END_ASM_DESCR
```

## Error Handling Patterns

### Standard Error Handling
```
CLEAR_CATCH_ERROR
BEGIN_CATCH_ERROR
    SEARCH_MDL_REF THIS CSYS "ACS0" ref
END_CATCH_ERROR

IF ERROR
    CLEAR_CATCH_ERROR
    ! Alternative code or error message
END_IF

IF NOT ERROR
    ! Success path
END_IF
```

### Fix Failed UDF Pattern
```
CLEAR_CATCH_ERROR
BEGIN_CATCH_ERROR FIX_FAIL_UDF
    CREATE_UDF lib:udfs\component SKEL_MDL UDF_GROUP
        UDF_REF "EDGE" EDGE
        UDF_REF "SURFACE" SURF
    END_CREATE_UDF
END_CATCH_ERROR
```

### PARAM_VALID Check
```
CLEAR_CATCH_ERROR
BEGIN_CATCH_ERROR
    SEARCH_MDL_PARAM SKEL_MDL "ALL_SS" NO_UPDATE ALL_SS
    SEARCH_MDL_PARAM SKEL_MDL "THICKNESS" NO_UPDATE THICKNESS
END_CATCH_ERROR

IF NOT PARAM_VALID THICKNESS
    THICKNESS = 0.0750
END_IF

IF PARAM_VALID ALL_SS
    CURB_MATERIAL = ALL_SS
END_IF
```

## Stopwatch / Performance Monitoring

```
DECLARE_STOPWATCH total_watch
START_STOPWATCH total_watch

! ... processing ...

STOP_STOPWATCH total_watch
GET_STOPWATCH_TIME total_watch time
PRINT "Total Processing Time: %" time
```

## Reference Guide Decision Tree

**Use this guide to find the right documentation for your task:**

### Core Language & Syntax
- **.tab syntax, variables, control flow** → SKILL.md (this file)
- **Complete command reference (751 commands)** → commands.md
- **Search commands (SEARCH_MDL_*)** → commands-search.md
- **UDF commands (CREATE_UDF, UDF_REF)** → commands-udf.md
- **Assembly commands (ASSEMBLE, constraints)** → commands-assembly.md
- **GUI commands (USER_INPUT_PARAM, RADIOBUTTON)** → commands-gui.md

### Integration & Workflows
- **Excel integration (EXCEL_* commands)** → excel-integration.md
- **JSON commands (JSON_* for REST API/data)** → json-commands.md
- **PowerShell-Creo COM API** → powershell-integration.md
- **Manufacturing pipeline (Model→Drawing→Export→PDF)** → manufacturing-workflows.md
- **Path system (SA_Paths.txt, lib: prefix)** → path-system.md

### Product Development
- **Product modules (Counters, WorkTables, Tops, etc.)** → product-patterns.md
- **Company workflows (EMJAC-specific)** → company-patterns.md

### Advanced Techniques
- **Multi-stage GUI, XML manipulation, maps, vectors** → advanced-patterns.md
- **GUI patterns (conditional visibility, wizards)** → gui-patterns.md

## Usage Scenarios

**1. "Review Auto_Top.tab for errors"**
→ Use: SKILL.md + commands.md + advanced-patterns.md
→ Check: Error handling, parameter validation, UDF creation patterns

**2. "Add field joint automation to new product module"**
→ Use: product-patterns.md (Field Joint Pattern) + commands-assembly.md
→ Implement: Opposing surface detection, distance measurement, UDF placement

**3. "Parse Specifications_DB.xlsx and populate model parameters"**
→ Use: excel-integration.md + path-system.md
→ Implement: EXCEL_* workflow, row iteration with EOF, parameter setting

**4. "Debug creoD.ps1 failure on PDF export"**
→ Use: powershell-integration.md + manufacturing-workflows.md
→ Check: COM API connection, IsRunning() checks, PDF merge integration

**5. "Generate drawing and DXF export for counter assembly"**
→ Use: manufacturing-workflows.md + commands.md
→ Implement: CREATE_DRW_VIEW_GENERAL, EXPORT_FILE (DXF), EXPORT_DRW_PDF

**6. "Create multi-shape WorkTable with A/C/L variants"**
→ Use: product-patterns.md (Multi-Shape Pattern) + gui-patterns.md
→ Implement: Shape selection radiobuttons, shape-specific GUI includes

**7. "Fix 'lib:Counters\file.tab' path resolution error"**
→ Use: path-system.md
→ Check: SA_Paths.txt configuration, EMJAC_SA_PATHS environment variable

**8. "Implement XML feature manipulation for surface collection"**
→ Use: advanced-patterns.md (XML Manipulation) + SKILL.md (XML Pattern)
→ Implement: READ_FEATURE_XML, line-by-line parsing, MODIFY_FEATURE_XML

**9. "Add material selection with downstream propagation"**
→ Use: product-patterns.md (Material Selection Pattern) + gui-patterns.md
→ Implement: RADIOBUTTON_PARAM, material→UDF variant logic

**10. "Optimize slow geometry analysis loop"**
→ Use: advanced-patterns.md (Performance Monitoring) + SKILL.md (Stopwatch)
→ Implement: DECLARE_STOPWATCH, sectional timing, optimization

**11. "Create conditional GUI with mutually exclusive options"**
→ Use: gui-patterns.md + SKILL.md (GUI Patterns)
→ Implement: Nested IF conditions for parameter visibility

**12. "Build BOM generation script with Excel export"**
→ Use: excel-integration.md + manufacturing-workflows.md
→ Implement: Feature group iteration, EXCEL_SET_VALUE buffer operations

**13. "Automate Creo via PowerShell with database integration"**
→ Use: powershell-integration.md
→ Implement: COM API connection, SQLQuery class, secure PSSession transfer

**14. "Debug 'Invalid reference' error after model regeneration"**
→ Use: SKILL.md (Best Practices #6-7) + commands.md
→ Fix: INVALIDATE_REF before reuse, re-fetch references after REGEN_MDL

**15. "Implement auto-generation logic for Tops module"**
→ Use: product-patterns.md (Auto-Generation Pattern) + advanced-patterns.md
→ Implement: AUTO_COMMIT detection, RESOLVE_PATH, conditional includes

## Anti-Patterns (Common Mistakes)

**❌ Anti-Pattern 1: Low error handling in geometry operations**
```
! RISKY - No validation
SEARCH_MDL_REFS SKEL_MDL FEATURE "PANEL_CURVE*" PANEL_CURVES
GET_ARRAY_SIZE PANEL_CURVES num_curves
! If PANEL_CURVES empty, subsequent operations fail
```
**✅ Fix:** Add defensive checks
```
BEGIN_CATCH_ERROR
    SEARCH_MDL_REFS SKEL_MDL FEATURE "PANEL_CURVE*" PANEL_CURVES
END_CATCH_ERROR

IF ERROR OR ARRAY_EMPTY PANEL_CURVES
    MESSAGE_BOX IMAGE lib:Images\Error.gif "No panel curves found!"
    RETURN
END_IF
```

**❌ Anti-Pattern 2: Missing parameter validation before CREATE_UDF**
```
! RISKY - EDGE_REF might be invalid
CREATE_UDF lib:udfs\component SKEL_MDL UDF_GROUP
    UDF_REF "EDGE" EDGE_REF
END_CREATE_UDF
```
**✅ Fix:** Validate references first
```
IF NOT REF_VALID EDGE_REF
    MESSAGE_BOX IMAGE lib:Images\Error.gif "Invalid edge reference!"
    RETURN
END_IF

CREATE_UDF lib:udfs\component SKEL_MDL UDF_GROUP
    UDF_REF "EDGE" EDGE_REF
END_CREATE_UDF
```

**❌ Anti-Pattern 3: Hard-coded paths**
```
INCLUDE C:\SmartAssembly\Library_New\SA_PROD_L\Utilities\helper.tab
```
**✅ Fix:** Use lib: prefix
```
INCLUDE lib:Utilities\helper.tab
```

**❌ Anti-Pattern 4: Direct reference use after regeneration**
```
REGEN_MDL SKEL_MDL
! EDGE_REF now invalid!
CREATE_UDF lib:udfs\bend SKEL_MDL UDF_GROUP
    UDF_REF "EDGE" EDGE_REF  ! FAILS
END_CREATE_UDF
```
**✅ Fix:** Invalidate and re-fetch
```
REGEN_MDL SKEL_MDL
INVALIDATE_REF EDGE_REF
SEARCH_MDL_REF SKEL_MDL EDGE "BEND_EDGE" EDGE_REF
CREATE_UDF lib:udfs\bend SKEL_MDL UDF_GROUP
    UDF_REF "EDGE" EDGE_REF
END_CREATE_UDF
```

**❌ Anti-Pattern 5: Forgetting to close Excel connections**
```
EXCEL_START
EXCEL_LOAD_DOCUMENT file.xlsx
EXCEL_GET_VALUE 1 1 VALUE
! Script exits without cleanup - Excel process remains
```
**✅ Fix:** Always cleanup
```
EXCEL_START
EXCEL_LOAD_DOCUMENT file.xlsx
EXCEL_GET_VALUE 1 1 VALUE
EXCEL_CLOSE_DOCUMENT
EXCEL_DISCONNECT  ! Critical
```

**❌ Anti-Pattern 6: Array mutation during iteration**
```
FOR EDGE REF ARRAY ARRAY_EDGES
    IF condition
        REMOVE_ARRAY_ELEM ARRAY_EDGES EDGE  ! Breaks iteration
    END_IF
END_FOR
```
**✅ Fix:** Reverse iteration for deletion
```
GET_ARRAY_SIZE ARRAY_EDGES NUM_EDGES
i = NUM_EDGES
WHILE i >= 1
    GET_ARRAY_ELEM ARRAY_EDGES i EDGE
    IF condition
        REMOVE_ARRAY_ELEM ARRAY_EDGES EDGE
    END_IF
    i--
END_WHILE
```

## Trail File Debugging Workflow

After running scripts in Creo, check trail files for errors:

**1. Find latest trail file:**
```powershell
Get-ChildItem 'C:\Users\waveg\VsCodeProjects\jac-v1\SmartAssembly\trail_files\trail.txt.*' |
  Sort-Object {[int]($_.Name -replace 'trail.txt.','')} -Descending |
  Select-Object -First 1 -ExpandProperty FullName
```

**2. Parse errors** - Look for `!%CEERROR` lines:
```
!%CEERROR in Line lib:\PATH\file.tab (LINE_NUM): ERROR_MESSAGE
```

**3. Extract:** File path, line number (in parentheses), error message

**4. Fix source** at identified line, using error-solutions.md for patterns

**5. Re-run** and repeat until no errors

→ See **trail-file-debugging.md** for full parsing details
→ See **error-solutions.md** for fix patterns

## Self-Learning

When discovering new error patterns or solutions:

1. **Update error-solutions.md** with:
   - Error pattern (exact text)
   - Cause
   - Solution with before/after code

2. **Update relevant reference files** if discovering new command patterns

This ensures the skill improves over time.

## Reference Files

**Core Language:**
- **commands.md** - Complete command reference (751 commands, 69 categories)
- **commands-search.md** - SEARCH_MDL_* command details
- **commands-udf.md** - UDF creation command reference
- **commands-assembly.md** - Assembly and constraint commands
- **commands-gui.md** - GUI parameter commands

**Integration & Workflows:**
- **excel-integration.md** - Excel integration (40+ EXCEL_* commands, 5 workflows, cell mapping)
- **json-commands.md** - JSON commands (16 commands for REST API/data exchange)
- **powershell-integration.md** - PowerShell-Creo COM API, SQL Server, PDF merge
- **manufacturing-workflows.md** - 4-stage manufacturing pipeline (Model→Drawing→Export→PDF)
- **path-system.md** - SA_Paths.txt configuration, lib: prefix resolution

**Debugging & Learning:**
- **trail-file-debugging.md** - Trail file parsing, error extraction, debug workflow
- **error-solutions.md** - Error patterns and fixes (self-updateable knowledge base)

**Product & Patterns:**
- **product-patterns.md** - Product modules (Counters, WorkTables, Tops, etc.), architecture patterns
- **advanced-patterns.md** - Multi-stage GUI, XML manipulation, maps, vectors, performance
- **gui-patterns.md** - GUI configuration patterns, conditional visibility
- **company-patterns.md** - EMJAC-specific workflows

## Best Practices

1. **Organize declarations by type** at script start with clear section headers
2. **Use descriptive variable names** that indicate purpose (ARRAY_EXISTING_SPACERS, BOTTOM_EDGE)
3. **Always UNGROUP_FEATURES after CREATE_UDF** for proper naming and access
4. **Use wildcard suffix (+\*)** in SET_REF_NAME for unique names
5. **Wrap searches in BEGIN_CATCH_ERROR** for robust error handling
6. **Clear arrays before reuse** with CLEAR_ARRAY
7. **Use INVALIDATE_REF** before reusing reference variables
8. **Group related features** at section end for organization
9. **Use CONFIG_ELEM CONTINUE_ON_CANCEL** for GUI that allows cancellation
10. **Track features with parameters** for later searching (SET_FEAT_PARAM)
11. **Use vector comparison** for direction-based geometry analysis
12. **Include WINDOW_ACTIVATE** at end of scripts for user focus
13. **Use PROCESSING_BOX** for long operations
14. **Clear CATCH_ERROR before reuse** to avoid false positives
15. **Use modular INCLUDE files** for shared functionality
16. **Always include path resolution** (INCLUDE lib:Read_SA_Paths.tab)
17. **Validate references before UDF creation** (REF_VALID checks)
18. **Close Excel connections** (EXCEL_DISCONNECT mandatory)
19. **Use lib: prefix** for all path references (never hard-code)
20. **Add defensive parameter validation** for production code
