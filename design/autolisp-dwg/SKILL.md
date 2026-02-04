---
name: autolisp-dwg
description: Use this when working with DWG file generation features (Tiles, Playground, Symbol Generator). Provides AutoLISP script patterns, DWGUNITS command, entity creation (entmake), APS Design Automation requirements, and critical rules for headless AutoCAD operation.
---

# AutoLISP DWG Generation Patterns

Essential AutoLISP patterns for generating DWG files via APS Design Automation. Used across three features: Tiles, Playground, and Symbol Generator.

---

## Features Using AutoLISP

| Feature | File Location | Description |
|---------|--------------|-------------|
| **Tiles** | `src/lib/tiles/script-generator.ts` | Programmatic tile layout generation |
| **Playground** | `src/lib/playground/prompts.ts` | Natural language to DWG via LLM |
| **Symbol Generator** | `src/lib/symbol-generator/script-prompts.ts` | Luminaire plan-view symbols |

---

## Script Structure Template

All generated scripts **must** follow this structure:

```lisp
(setvar "cmdecho" 0)
(setvar "filedia" 0)

; === SET METRIC UNITS (mm) ===
(command "-DWGUNITS" 3 2 2 "Y" "Y" "N")

; === LAYER SETUP ===
(command "-LAYER" "Make" "OUTLINE" "Color" "7" "" "")
(command "-LAYER" "Make" "TEXT" "Color" "1" "" "")

; === GEOMETRY ===
; Draw entities with entmake or command
(entmake '((0 . "LINE") (8 . "OUTLINE") (10 0.0 0.0 0.0) (11 100.0 0.0 0.0)))

; === FINALIZE ===
(command "ZOOM" "E")
(command "SAVEAS" "2018" "result.dwg")
```

### ⚠️ Critical Rules

**MUST include:**
- ✅ `(setvar "filedia" 0)` - Required for headless operation
- ✅ `(command "-DWGUNITS" 3 2 2 "Y" "Y" "N")` - Sets metric units
- ✅ `(command "SAVEAS" "2018" "filename.dwg")` - Saves output

**MUST NOT include:**
- ❌ `(command "QUIT")` - APS handles process termination
- ❌ Interactive prompts - No dialogs available in headless mode

---

## DWGUNITS Command (REQUIRED)

Sets drawing units to metric/millimeters. **Must be included in every script.**

```lisp
(command "-DWGUNITS" 3 2 2 "Y" "Y" "N")
```

### Parameter Breakdown

| Position | Value | Meaning |
|----------|-------|---------|
| 1 | `3` | Linear units = **Millimeters** |
| 2 | `2` | Linear display format = Decimal |
| 3 | `2` | Linear display precision = 0.00 |
| 4 | `"Y"` | Scale objects from other drawings = Yes |
| 5 | `"Y"` | Match INSUNITS to drawing units = Yes |
| 6 | `"N"` | Reset scale list = No |

### Other Unit Codes (for reference)

| Code | Unit |
|------|------|
| 1 | Inches |
| 2 | Feet |
| 3 | **Millimeters** ← FOSSAPP standard |
| 4 | Centimeters |
| 5 | Meters |

**Why millimeters?** All product specifications in the database are in mm.

---

## Entity Creation with entmake

### LINE

```lisp
(entmake '(
  (0 . "LINE")
  (8 . "LAYER_NAME")
  (10 X1 Y1 0.0)    ; Start point
  (11 X2 Y2 0.0)    ; End point
))
```

**Example:**
```lisp
(entmake '((0 . "LINE") (8 . "OUTLINE") (10 0.0 0.0 0.0) (11 100.0 50.0 0.0)))
```

### CIRCLE

```lisp
(entmake '(
  (0 . "CIRCLE")
  (8 . "LAYER_NAME")
  (10 CX CY 0.0)    ; Center point
  (40 . RADIUS)     ; Radius (NOT diameter!)
))
```

**⚠️ CRITICAL:** Specifications often give **DIAMETER** - always divide by 2 for radius!

**Example:**
```lisp
; Drawing a 67mm diameter circle
(setq diameter 67)
(setq radius (/ diameter 2.0))
(entmake '((0 . "CIRCLE") (8 . "OUTLINE") (10 0.0 0.0 0.0) (40 . 33.5)))
```

### ARC

```lisp
(entmake '(
  (0 . "ARC")
  (8 . "LAYER_NAME")
  (10 CX CY 0.0)           ; Center point
  (40 . RADIUS)            ; Radius
  (50 . START_ANGLE_RAD)   ; Start angle in RADIANS
  (51 . END_ANGLE_RAD)     ; End angle in RADIANS
))
```

**⚠️ ANGLES ARE RADIANS!** Convert degrees to radians:

```lisp
(setq angle_radians (* angle_degrees (/ pi 180)))

; Example: 90 degree arc from 0 to 90
(setq start_rad 0.0)
(setq end_rad (* 90 (/ pi 180)))  ; = 1.5708
(entmake '((0 . "ARC") (8 . "OUTLINE") (10 0.0 0.0 0.0) (40 . 50.0) (50 . 0.0) (51 . 1.5708)))
```

### LWPOLYLINE (Closed Rectangle)

```lisp
(entmake '(
  (0 . "LWPOLYLINE")
  (100 . "AcDbEntity")
  (8 . "LAYER_NAME")
  (100 . "AcDbPolyline")
  (90 . 4)              ; Number of vertices
  (70 . 1)              ; 1=closed, 0=open
  (10 X1 Y1)            ; Vertex 1 (2D only)
  (10 X2 Y2)            ; Vertex 2
  (10 X3 Y3)            ; Vertex 3
  (10 X4 Y4)            ; Vertex 4
))
```

**Example - 100mm x 50mm rectangle centered at origin:**
```lisp
(setq half_w (/ 100 2.0))  ; 50mm
(setq half_h (/ 50 2.0))   ; 25mm
(entmake '(
  (0 . "LWPOLYLINE")
  (100 . "AcDbEntity")
  (8 . "OUTLINE")
  (100 . "AcDbPolyline")
  (90 . 4)
  (70 . 1)
  (10 -50.0 -25.0)  ; Bottom-left
  (10 50.0 -25.0)   ; Bottom-right
  (10 50.0 25.0)    ; Top-right
  (10 -50.0 25.0)   ; Top-left
))
```

### MTEXT (Multiline Text)

```lisp
(entmake (list
  '(0 . "MTEXT")
  '(100 . "AcDbEntity")
  '(8 . "TEXT")
  '(100 . "AcDbMText")
  '(10 X Y 0.0)         ; Insertion point
  '(40 . TEXT_HEIGHT)   ; Text height (mm)
  '(41 . COLUMN_WIDTH)  ; Column width (mm)
  '(71 . ATTACHMENT)    ; Attachment point (see below)
  (cons 1 "Your text here\\PNext line")
))
```

**Attachment point codes (71):**
| Code | Position |
|------|----------|
| 1 | Top Left |
| 2 | Top Center |
| 3 | Top Right |
| 4 | Middle Left |
| 5 | Middle Center ← Common |
| 6 | Middle Right |
| 7 | Bottom Left |
| 8 | Bottom Center |
| 9 | Bottom Right |

**MTEXT formatting codes:**
| Code | Effect |
|------|--------|
| `\\P` | New line |
| `\\L...\\l` | Underline |
| `{\\C1;text}` | Color (1=red, 3=green, 5=blue) |
| `{\\H1.5x;text}` | Height 1.5x |

**Example:**
```lisp
(entmake (list
  '(0 . "MTEXT")
  '(100 . "AcDbEntity")
  '(8 . "TEXT")
  '(100 . "AcDbMText")
  '(10 0.0 -100.0 0.0)
  '(40 . 3.5)
  '(41 . 200.0)
  '(71 . 5)
  (cons 1 "DELTA-123456\\PDOWNLIGHT 67MM")
))
```

---

## Layer Management

### Create Layer with Color

```lisp
(command "-LAYER" "Make" "LAYER_NAME" "Color" "COLOR_NUM" "" "")
```

**Example:**
```lisp
(command "-LAYER" "Make" "OUTLINE" "Color" "7" "" "")  ; White
(command "-LAYER" "Make" "TEXT" "Color" "1" "" "")     ; Red
(command "-LAYER" "Make" "DIMS" "Color" "3" "" "")     ; Green
```

### DXF Color Codes

| Code | Color | Use Case |
|------|-------|----------|
| 1 | Red | Text, important info |
| 2 | Yellow | Warnings |
| 3 | Green | Dimensions |
| 4 | Cyan | Construction lines |
| 5 | Blue | Water/special |
| 6 | Magenta | Highlights |
| 7 | White | Standard outlines |

**Add color to entity:**
```lisp
(entmake '((0 . "LINE") (8 . "OUTLINE") (62 . 7) (10 0.0 0.0 0.0) (11 100.0 0.0 0.0)))
;                                        ↑ color code
```

### Set Current Layer

```lisp
(setvar "CLAYER" "LAYER_NAME")
```

### Load Linetype (e.g., DASHED)

```lisp
(command "-LINETYPE" "Load" "DASHED" "" "")
(command "-LAYER" "Ltype" "DASHED" "LAYER_NAME" "")
```

---

## Image Insertion (for Tiles feature)

```lisp
(command "-IMAGE" "Attach" "path/to/image.png" "X,Y" "SCALE" "0")
```

**Example:**
```lisp
(command "-IMAGE" "Attach" "product.png" "0,0" "1.0" "0")
```

**Notes:**
- Images must be uploaded to APS bucket before script execution
- Paths are relative to script working directory
- Scale 1.0 = 1 pixel = 1 mm (for 300dpi images at 1500x1500)

---

## Block Operations

### Create Block with entmake

```lisp
; 1. Start block definition
(entmake '((0 . "BLOCK") (2 . "BLOCKNAME") (10 0.0 0.0 0.0) (70 . 0)))

; 2. Add entities (layers still needed)
(entmake '((0 . "LINE") (8 . "0") (10 0.0 0.0 0.0) (11 10.0 0.0 0.0)))
(entmake '((0 . "CIRCLE") (8 . "0") (10 5.0 5.0 0.0) (40 . 3.0)))

; 3. End block
(entmake '((0 . "ENDBLK") (8 . "0")))

; 4. Insert block
(entmake '(
  (0 . "INSERT")
  (2 . "BLOCKNAME")
  (8 . "LAYER_NAME")
  (10 X Y 0.0)      ; Insertion point
  (41 . 1.0)        ; X scale
  (42 . 1.0)        ; Y scale
  (50 . 0.0)        ; Rotation (radians)
))
```

### Insert Block with command

```lisp
(command "-INSERT" "BLOCKNAME" "X,Y" "XSCALE" "YSCALE" "ROTATION_DEGREES")
```

---

## Common Calculations

### Center a Rectangle

```lisp
(setq width 100)
(setq height 50)
(setq half_w (/ width 2.0))
(setq half_h (/ height 2.0))

; Corners:
; (-50, -25), (50, -25), (50, 25), (-50, 25)
```

### Degrees to Radians

```lisp
(setq angle_rad (* angle_deg (/ pi 180)))

; Common angles:
; 0° = 0.0
; 45° = 0.7854
; 90° = 1.5708
; 180° = 3.1416
; 270° = 4.7124
; 360° = 6.2832
```

### Diameter to Radius

```lisp
(setq diameter 67)
(setq radius (/ diameter 2.0))  ; 33.5
```

### Distance Between Points

```lisp
(setq dx (- x2 x1))
(setq dy (- y2 y1))
(setq distance (sqrt (+ (* dx dx) (* dy dy))))
```

---

## APS Design Automation Requirements

### Environment Constraints

- **Headless mode:** No interactive dialogs (`filedia=0`)
- **No QUIT command:** APS handles process termination
- **File paths:** Relative to working directory
- **Output:** Must use SAVEAS with explicit filename

### File Upload Workflow

1. Upload images/assets to APS OSS bucket
2. Create script referencing uploaded files
3. Upload script to bucket
4. Submit WorkItem with script + assets
5. Download generated DWG from output

### Debugging Failed Scripts

**Common errors:**
- Missing DWGUNITS → Drawing uses wrong units
- Missing SAVEAS → No DWG output generated
- Using QUIT → Process terminates before completion
- Diameter instead of radius → Circles twice as large
- Degrees instead of radians → Arcs at wrong angles
- Missing filedia=0 → Script waits for dialog input

---

## Complete Example: Tile Layout

```lisp
; Headless setup
(setvar "cmdecho" 0)
(setvar "filedia" 0)

; Set metric units (mm)
(command "-DWGUNITS" 3 2 2 "Y" "Y" "N")

; Create layers
(command "-LAYER" "Make" "OUTLINE" "Color" "7" "" "")
(command "-LAYER" "Make" "TEXT" "Color" "1" "" "")
(command "-LAYER" "Make" "IMAGE" "Color" "5" "" "")

; Draw border (200mm x 200mm)
(setq size 200)
(setq half (/ size 2.0))
(entmake '(
  (0 . "LWPOLYLINE")
  (100 . "AcDbEntity")
  (8 . "OUTLINE")
  (100 . "AcDbPolyline")
  (90 . 4)
  (70 . 1)
  (10 -100.0 -100.0)
  (10 100.0 -100.0)
  (10 100.0 100.0)
  (10 -100.0 100.0)
))

; Insert product image
(setvar "CLAYER" "IMAGE")
(command "-IMAGE" "Attach" "product.png" "-75,-75" "1.0" "0")

; Add product text
(entmake (list
  '(0 . "MTEXT")
  '(100 . "AcDbEntity")
  '(8 . "TEXT")
  '(100 . "AcDbMText")
  '(10 0.0 -105.0 0.0)
  '(40 . 3.5)
  '(41 . 180.0)
  '(71 . 5)
  (cons 1 "DELTA-123456\\PDOWNLIGHT 67MM")
))

; Finalize
(command "ZOOM" "E")
(command "SAVEAS" "2018" "tile.dwg")
```

---

## Quick Reference

### Critical Rules Checklist

- [ ] `(setvar "filedia" 0)` included
- [ ] `(command "-DWGUNITS" 3 2 2 "Y" "Y" "N")` included
- [ ] All dimensions in millimeters
- [ ] Circles use radius, not diameter
- [ ] Arc angles in radians, not degrees
- [ ] All points are 3D (include 0.0 for Z)
- [ ] `(command "SAVEAS" "2018" "filename.dwg")` included
- [ ] NO `(command "QUIT")` command

### Common Mistakes

| ❌ Wrong | ✅ Correct |
|---------|-----------|
| `(40 . 67)` for 67mm diameter | `(40 . 33.5)` (radius = diameter/2) |
| `(50 . 90)` for 90° arc | `(50 . 1.5708)` (radians = deg × π/180) |
| `(10 100 50)` | `(10 100.0 50.0 0.0)` (include Z coordinate) |
| Missing DWGUNITS | Always include DWGUNITS command |
| `(command "QUIT")` | Never use QUIT (APS handles termination) |
| No SAVEAS | Always use SAVEAS to create output |

---

## See Also

- Tiles feature: [docs/features/tiles.md](../../docs/features/tiles.md)
- Playground feature: [docs/features/playground.md](../../docs/features/playground.md)
- Symbol Generator: [docs/features/symbol-generator.md](../../docs/features/symbol-generator.md)
- Full AutoLISP reference: [docs/development/autolisp-reference.md](../../docs/development/autolisp-reference.md)
