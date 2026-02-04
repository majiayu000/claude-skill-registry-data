---
name: openscad
description: Create parametric 3D models using OpenSCAD, a script-based solid CAD modeler. Use when the user asks to create 3D printable objects, parametric designs, mechanical parts, CAD models, or requests .scad files. OpenSCAD uses constructive solid geometry (CSG) and extrusion of 2D shapes to create 3D models through code.
---

# OpenSCAD Skill

Generate OpenSCAD (.scad) files for parametric 3D modeling. OpenSCAD is a functional programming language for creating solid 3D CAD objects using CSG (Constructive Solid Geometry).

## Core Concepts

OpenSCAD scripts describe geometry through:
1. **Primitives** - Basic 2D/3D shapes (cube, sphere, cylinder, circle, square, polygon)
2. **Transformations** - Position/modify objects (translate, rotate, scale, mirror, color)
3. **Boolean Operations** - Combine shapes (union, difference, intersection)
4. **Modules** - Reusable parametric components
5. **Extrusion** - Convert 2D to 3D (linear_extrude, rotate_extrude)

## Workflow

1. Define parameters as variables at the top for easy customization
2. Create modules for reusable components
3. Build geometry using primitives and boolean operations
4. Use comments to explain complex sections
5. Set `$fn` for curved surface resolution (higher = smoother but slower)

## Quick Reference

### 3D Primitives
```openscad
cube([x, y, z], center=false);
cube(size, center=false);
sphere(r=radius);  // or d=diameter
cylinder(h=height, r=radius, center=false);
cylinder(h=height, r1=bottom_r, r2=top_r);  // cone
polyhedron(points=[[x,y,z],...], faces=[[p0,p1,p2],...]);
```

### 2D Primitives
```openscad
square([x, y], center=false);
circle(r=radius);  // or d=diameter
polygon(points=[[x,y],...]);
text("string", size=10, font="Liberation Sans");
```

### Transformations
```openscad
translate([x, y, z]) object();
rotate([x_deg, y_deg, z_deg]) object();
rotate(a=degrees, v=[x,y,z]) object();  // rotate around axis
scale([x, y, z]) object();
mirror([x, y, z]) object();  // mirror across plane
color("red") object();
color([r, g, b, a]) object();  // 0-1 values
```

### Boolean Operations
```openscad
union() { obj1(); obj2(); }         // combine (implicit if no operator)
difference() { base(); cut1(); }    // subtract from first child
intersection() { obj1(); obj2(); }  // keep only overlap
```

### Extrusion (2D to 3D)
```openscad
linear_extrude(height=h, twist=deg, scale=s, slices=n, center=false)
    2d_shape();
rotate_extrude(angle=360, $fn=n)
    2d_shape();  // shape must be on positive X side
```

### Control Structures
```openscad
// Loops
for (i = [0:10]) translate([i*5, 0, 0]) cube(3);
for (i = [0:2:10]) ...;  // start:step:end
for (pos = [[0,0], [10,5], [5,10]]) translate(pos) sphere(2);

// Conditionals
if (condition) { ... } else { ... }
variable = condition ? value_if_true : value_if_false;
```

### Modules and Functions
```openscad
// Module (creates geometry)
module my_part(size=10, holes=true) {
    difference() {
        cube(size);
        if (holes) cylinder(h=size+1, r=size/4, center=true);
    }
}
my_part(20, holes=false);

// Function (returns value)
function circumference(r) = 2 * PI * r;
```

### Special Variables
```openscad
$fn = 100;  // fragments for full circle (overrides $fa/$fs)
$fa = 12;   // minimum angle per fragment
$fs = 2;    // minimum size per fragment
$preview    // true during F5 preview, false during F6 render
```

## Best Practices

### Parametric Design
```openscad
// Define all dimensions as variables
wall_thickness = 2;
inner_diameter = 20;
height = 30;

// Derive other values
outer_diameter = inner_diameter + 2*wall_thickness;
```

### Avoiding Rendering Issues
```openscad
// Use epsilon to prevent z-fighting in boolean operations
eps = 0.01;
difference() {
    cube([10, 10, 10]);
    translate([2, 2, -eps])
        cylinder(h=10 + 2*eps, r=3);  // slightly taller than parent
}
```

### Manifold Geometry for 3D Printing
- Ensure all geometry is watertight (no gaps)
- Holes must fully penetrate surfaces
- Use `render()` to verify complex geometry
- Check face orientation with F12 (Thrown Together view)

## Detailed References

- For complete syntax: See `references/language_reference.md`
- For example patterns: See `references/examples.md`

## Output

Save generated code as `.scad` files. Users can open in OpenSCAD for:
- F5: Quick preview
- F6: Full render (required before export)
- Export to STL/AMF/3MF for 3D printing
