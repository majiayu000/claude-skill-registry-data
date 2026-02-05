---
name: openscad-modeler
description: OpenSCAD 3D modeling assistant for creating and modifying parametric 3D models. Use when working with .scad files, making adjustments to 3D models (resizing, adding/removing sections, holes, fillets), creating new OpenSCAD geometry, or debugging OpenSCAD code. Supplements the openscad MCP server (mcp__openscad__render_single) with language knowledge and modification patterns.
---

# OpenSCAD Modeler

Workflow for creating and modifying OpenSCAD parametric 3D models.

## MCP Integration

Use `mcp__openscad__render_single` to preview changes:
```
scad_content: "cube([10,10,10]);"    // Inline code
scad_file: "/path/to/file.scad"     // Or file path
view: "isometric"                    // front/back/left/right/top/bottom/isometric
```

Render after each significant modification to verify results.

## Quick Reference

### Primitives
```scad
cube([x,y,z], center=true);
sphere(r=5); sphere(d=10);
cylinder(h=10, r=5); cylinder(h=10, r1=5, r2=3);  // cone
```

### Transforms
```scad
translate([x,y,z]) obj;
rotate([x,y,z]) obj;        // degrees
scale([x,y,z]) obj;
mirror([1,0,0]) obj;        // mirror across YZ plane
```

### Boolean Operations
```scad
difference() { base; subtract1; subtract2; }  // Remove
union() { obj1; obj2; }                        // Combine
intersection() { obj1; obj2; }                 // Keep overlap
```

### Extrusions
```scad
linear_extrude(height=10) circle(r=5);
linear_extrude(h=10, twist=90, scale=0.5) square(10);
rotate_extrude() translate([10,0]) circle(r=3);  // Torus
```

### Resolution
```scad
$fn = 100;  // Smooth curves (set globally or per-object)
cylinder(h=10, r=5, $fn=6);  // Hexagon
```

## Common Modifications

### Add hole
```scad
difference() {
    existing_part();
    translate([x,y,z]) cylinder(d=hole_d, h=99, center=true);
}
```

### Resize
```scad
scale([1.5, 1.5, 1]) existing_part();     // 150% XY, keep Z
resize([50, 0, 0], auto=true) part();     // 50mm wide, proportional
```

### Round edges
```scad
minkowski() {
    cube([w-2*r, d-2*r, h-2*r], center=true);
    sphere(r=r);
}
```

### Shell/hollow
```scad
difference() {
    outer_shape();
    offset(-wall) outer_shape();  // 2D
    // Or for 3D: scale down slightly
}
```

### Array
```scad
for (i = [0:count-1]) translate([i*spacing, 0, 0]) part();
for (i = [0:5]) rotate([0, 0, i*60]) translate([r, 0, 0]) part();
```

## Workflow

1. **Read** existing .scad file or start new
2. **Identify** what to modify (add/remove/resize)
3. **Apply** appropriate pattern from above
4. **Render** with MCP to verify (`view: "isometric"`)
5. **Iterate** as needed

## Detailed References

- **Full syntax**: See [references/syntax.md](references/syntax.md) for complete language reference
- **Modification patterns**: See [references/patterns.md](references/patterns.md) for detailed examples of common operations

## Debugging Tips

- Use `#` prefix to highlight object in preview: `#cube([10,10,10]);`
- Use `%` for transparent preview: `%cylinder(h=20, r=5);`
- Use `!` to show only that object: `!sphere(r=10);`
- Use `*` to disable object: `*cube([10,10,10]);`
- Check `$preview` for render vs preview mode
- Increase `convexity` parameter if preview renders incorrectly
