---
name: render-defect-forensics
description: Use when debugging a visual defect in a rendered scene (Blender/USD or any 3D pipeline) — verify by rendering (never by geometry math), A/B every perceptual change, and ray-cast the exact offending pixel once a defect survives two fixes.
stacks: [python]
domains: [game, any]
phases: [dev]
tags: [rendering, blender, usd, debugging, raycast, lighting, materials]
scope: kit
---
**When to use.** Any "the image looks wrong" bug. *Why:* predictions about images are usually wrong —
hand camera-cone math mispredicted framing every time; one artifact survived six rounds of
plausible-but-wrong theories until a single ray cast named the true object.

**Procedure.**
1. Reproduce with a cheap targeted render (one view, low samples). Composition questions are answered
   ONLY by rendering.
2. Two failed fixes → stop theorizing: cast a ray from the camera through the offending pixel and
   print what it hits. Fix the named object at its root (ours: a floor slab 20 mm high since four
   phases earlier).
3. Know the physics traps before inventing new ones: emission meshes block their own light source;
   small emitters need glossy/transmission ray visibility off; filmic tonemaps eat EV lifts (measure
   landed exposure and correct once, don't stack fixed lifts); smooth-shaded slab rims fake light
   leaks (flat-shade architecture); crushed shadows usually mean the sun:sky ratio, not geometry.
4. A/B render before keeping any perceptual change, and check for NEW artifact classes the change
   can introduce (per-channel sharpening ⇒ chromatic fringing; fix: luminance-only).
5. **Done when:** the fixed still is rendered and inspected (not asserted), and a mechanical probe or
   test now guards the defect class.

**Knowledge:** FIELD-KNOWLEDGE-NOTHOMEWRECKER.md §F3 (incl. USD-importer flattening, stamp-based
matching, exposure targeting, de-tiling and albedo-grunge recipes).
