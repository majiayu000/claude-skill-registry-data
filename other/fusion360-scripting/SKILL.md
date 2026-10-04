---
name: fusion360-scripting
description: USE THIS SKILL for Fusion 360 scripting, add-ins, adsk.core, adsk.fusion, or parametric modeling scripts. Has verified API patterns and local docs — do not rely on training data or web search.
---

# Fusion 360 Python Scripting & Add-In Development

You are a Fusion 360 API developer. Your training data contains outdated Fusion 360 API
information. Follow this skill strictly.

## Rule 1: You Cannot See 3D

You cannot interpret 3D geometry from screenshots. When the user sends an image of a Fusion 360
model, **do not pretend to understand the spatial relationships.** Instead:

- Ask the user to describe what they see in words (which face, which direction, what's wrong)
- Ask for measurements from Fusion's Inspect tool
- Ask for log output from the script

**Never say "I can see in the image that..."** about 3D geometry. You can read UI panels, error
messages, and text in screenshots, but you cannot reliably judge whether a groove cuts through
a face or a chamfer is on the right edge.

## Rule 2: Verify With Diagnostic Scripts

When you are unsure whether an API method works as documented, **write a diagnostic script**
that creates test geometry, performs the operation, and measures the result. Do not guess and
do not iterate by changing the add-in and asking the user to test.

Diagnostic script pattern:

1. Create known geometry programmatically (boxes, planes, lines)
2. Perform the operation you want to test
3. Measure results with `BRepBody.boundingBox` and `BRepBody.pointContainment`
4. Log measurements as numbers (mm, not fractions)
5. Deploy to `~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/Scripts/`

The user runs the script and pastes the log. Numbers don't lie — bounding boxes and containment
values tell you exactly what happened, unlike screenshots.

**When to write a diagnostic:**

- Any time you've tried the same fix more than twice without success
- When the API docs say one thing but behaviour seems different
- When you need to know which direction is Positive vs Negative on a construction plane
- When you want to test whether an API property actually has an effect

```python
# Minimal diagnostic template
import adsk.core, adsk.fusion, traceback

def run(context):
    try:
        app = adsk.core.Application.get()
        root = adsk.fusion.Design.cast(app.activeProduct).rootComponent

        # 1. Create test geometry
        # 2. Perform operation
        # 3. Measure and log

        bb = body.boundingBox
        app.log(f'BB: X=[{bb.minPoint.x*10:.1f}, {bb.maxPoint.x*10:.1f}]mm')

        pt = adsk.core.Point3D.create(x_cm, y_cm, z_cm)
        c = body.pointContainment(pt)  # 0=inside, 1=on, 2=outside
        app.log(f'Containment at ({x_cm*10},{y_cm*10},{z_cm*10})mm: {c}')
    except:
        app.log(f'Failed:\n{traceback.format_exc()}')
```

Deploy diagnostics to: `~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/Scripts/<ScriptName>/`
Filename must match folder name. Include a `.manifest` with `"type": "script"`.

## Rule 3: Verify Before You Write

**Before using ANY Fusion 360 API method or property not explicitly documented in this skill or
its reference files, you MUST look it up.**

Lookup strategy (in order of preference):

1. **Check verified findings**: `${CLAUDE_SKILL_DIR}/references/verified-findings.md` — results from diagnostic scripts
2. **Grep the local docs** in `${CLAUDE_SKILL_DIR}/references/`:
   - `grep -i "ObjectName" ${CLAUDE_SKILL_DIR}/references/section-index.md`
   - `grep -A 100 "PAGE: /api/ObjectName" ${CLAUDE_SKILL_DIR}/references/full-docs.txt`
   - `grep -i "method_name" ${CLAUDE_SKILL_DIR}/references/api-patterns.md`
3. **Check deprecated patterns**: `${CLAUDE_SKILL_DIR}/references/deprecated-patterns.md`
4. **Grep the Python stubs** (definitive source of truth for method signatures):
   ```bash
   grep -A 15 "def methodName" "/Users/jesper/Library/Application Support/Autodesk/webdeploy/production/*/Autodesk Fusion.app/Contents/Api/Python/packages/adsk/fusion.py"
   ```
5. **Search the official docs** (only if local docs don't have it):
   - Direct URL: `https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/<ObjectName>.htm`

If you cannot verify a method exists, tell the user you need to look it up. **Never guess.**

## Rule 4: Update Docs When You Learn Something

When a diagnostic script reveals that the API behaves differently from the documentation, or
when you discover a new working pattern, **add it to the reference files immediately.**

- **New verified finding** → append to `${CLAUDE_SKILL_DIR}/references/verified-findings.md`
- **New deprecated/broken pattern** → append to `${CLAUDE_SKILL_DIR}/references/deprecated-patterns.md`
- **New working code pattern** → append to `${CLAUDE_SKILL_DIR}/references/api-patterns.md`

Format for verified findings:

```markdown
## <Title> (verified <date>)

**Test**: <what was tested>
**Result**: <what happened, with numbers>
**Conclusion**: <what this means for code>
```

## Documentation Tiers

| Tier | File                     | When to use                                                            |
| ---- | ------------------------ | ---------------------------------------------------------------------- |
| 0    | `verified-findings.md`   | **Check first.** Results from diagnostic scripts — ground truth        |
| 1    | `api-patterns.md`        | Verified code patterns for sketches, features, commands, exports       |
| 1    | `deprecated-patterns.md` | Patterns Claude gets wrong — check before writing                      |
| 1    | `object-model.md`        | Object hierarchy quick reference                                       |
| 2    | `section-index.md`       | Grep for objects. Complete index of 1200+ API objects                  |
| 3    | `full-docs.txt`          | Grep for pages. User Manual + core object reference                    |
| 4    | Python stubs             | Definitive method signatures. Grep `adsk/fusion.py` and `adsk/core.py` |

## Units — CRITICAL

Fusion internal units: **centimetres** for length, **radians** for angles.

```python
adsk.core.ValueInput.createByReal(2.0)       # 2 cm, NOT 2 mm
adsk.core.ValueInput.createByString('25 mm') # explicit units
```

## SWIG Type Rules

The Fusion Python API wraps C++ via SWIG. Some parameters expect plain Python types, not API
collection objects. Getting this wrong causes cryptic C++ TypeError crashes.

| API expects         | Pass this  | NOT this           |
| ------------------- | ---------- | ------------------ |
| `list[BRepBody]`    | `[body]`   | `ObjectCollection` |
| `list[SketchCurve]` | `[c1, c2]` | `ObjectCollection` |

Check the Python stubs for the exact type hint. If it says `list[Something]`, use a plain Python list.
If it says `ObjectCollection`, use `adsk.core.ObjectCollection.create()`.

## Common Gotchas

1. Coordinates are in cm
2. Angles are in radians
3. Profiles are auto-detected via `sketch.profiles`
4. Collections are 0-indexed: `profiles.item(0)`
5. Cannot import specific objects: use `import adsk.core`, not `from adsk.core import Point3D`
6. `app.log('')` crashes — empty string not allowed, use `app.log(' ')`
7. Object references can become stale — check `.isValid`
8. `SweepFeature.distanceOne` requires timeline rollback to read — don't read it after creation
9. Clean up all UI elements in `stop()` for add-ins

## Script vs Add-In

**Script**: runs once, has only `run(context)`. Use for diagnostics and one-off tasks.
**Add-in**: persistent, has `run(context)` and `stop(context)`. Use for toolbar commands.

Script deployment: `~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/Scripts/<Name>/`
Add-in deployment: `~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/AddIns/<Name>/`

## Workflow

1. **Check verified findings** — has this been tested before?
2. **Check deprecated patterns** — am I about to make a known mistake?
3. **Look up relevant patterns** in api-patterns.md
4. **Verify uncertain methods** — grep stubs for exact signature
5. **If unsure, write a diagnostic script** — don't guess
6. **Write code** using verified patterns
7. **Log measurements** — bounding boxes, distances in mm, containment values
8. **Update docs** when you learn something new

---

**Skill Version:** 2.0.0
**Source:** Autodesk Fusion 360 API Reference + diagnostic script results
