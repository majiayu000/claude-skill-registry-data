---
name: libgdx-math
description: Use when writing libGDX Java/Kotlin code involving math utilities — Vector2, Vector3, Matrix4, Quaternion, MathUtils, Interpolation, Intersector, Polygon, Circle, Rectangle, or spline curves. Use when debugging mutation bugs, wrong interpolation names, or incorrect collision detection.
---

# libGDX Math Utilities

Quick reference for `com.badlogic.gdx.math.*`. Covers vectors, matrices, quaternion, interpolation, intersection/collision, shapes, and math helpers.

## CRITICAL: Vectors Mutate In Place

Almost every Vector2/Vector3 method **mutates `this`** and returns `this` for chaining. This is the #1 source of bugs.

```java
Vector2 a = new Vector2(1, 2);
Vector2 b = new Vector2(3, 4);

a.add(b);            // a is now (4, 6) — b unchanged
a.cpy().add(b);      // returns new (4, 6) — a unchanged
a.sub(b).nor();      // a mutated TWICE — subtracted then normalized
```

This applies to: `set()`, `add()`, `sub()`, `scl()`, `nor()`, `lerp()`, `rotate*()`, `limit()`, `clamp()`, `setLength()`, `mulAdd()`, `setZero()`, `setToRandomDirection()`.

## Vector2

```java
new Vector2()                    // (0, 0)
new Vector2(float x, float y)
new Vector2(Vector2 v)           // copy constructor EXISTS

// Static constants (WARNING: mutable — treat as read-only)
Vector2.X   // (1, 0)
Vector2.Y   // (0, 1)
Vector2.Zero // (0, 0)
```

Key methods beyond the obvious (`set`, `add`, `sub`, `scl`, `nor`, `lerp`, `setZero`, `cpy` — all mutating, return `this`):

- `limit(float)` / `limit2(float)` — cap magnitude (limit2 avoids sqrt)
- `clamp(float min, float max)` — clamp magnitude
- `setLength(float)` / `setLength2(float)` — set magnitude
- `mulAdd(Vector2, float)` — `this += vec * scalar`
- `mul(Matrix3)` — transform by Matrix3 only, NOT Matrix4
- `crs(Vector2)` — **returns float** (2D cross product is a scalar)
- `len2()`, `dst2()` — squared versions (prefer for comparisons, avoids sqrt)

### Angle & Rotation (Vector2 only)

**Use `Deg` suffix methods. Non-suffixed versions are deprecated:**
- `angleDeg()` / `angleDeg(Vector2 ref)` — degrees 0–360
- `angleRad()` / `angleRad(Vector2 ref)` — radians
- `rotateDeg(float)` / `rotateRad(float)` — rotate vector
- `rotateAroundDeg(Vector2 ref, float deg)` — rotate around point
- `setAngleDeg(float)` / `setAngleRad(float)` — set direction
- `rotate90(int dir)` — `dir >= 0` = CCW, `dir < 0` = CW
- **DEPRECATED:** `angle()`, `rotate(float)`, `setAngle(float)`, `rotateAround(Vector2, float)` — use `Deg` versions

## Vector3

```java
new Vector3()
new Vector3(float x, float y, float z)
new Vector3(Vector3 other)              // copy constructor EXISTS
new Vector3(float[] values)             // uses [0], [1], [2]
new Vector3(Vector2 v, float z)

// Static constants (WARNING: mutable — treat as read-only)
Vector3.X, Vector3.Y, Vector3.Z, Vector3.Zero
```

Same methods as Vector2, plus key differences:

- `crs(Vector3)` — **MUTATES `this`** with 3D cross product (unlike Vector2's `crs()` which returns float). Use `a.cpy().crs(b)` to preserve `a`.
- `slerp(Vector3 target, float alpha)` — spherical lerp (Vector2 lacks this)
- `rotate(Vector3 axis, float degrees)` — NOT deprecated (unlike Vector2's `rotate`)
- `mul(Matrix4)`, `mul(Matrix3)`, `mul(Quaternion)` — transform by matrix/quaternion
- `prj(Matrix4)` — project (divide by w) — for projection matrices
- `rot(Matrix4)` — rotate only (ignores translation)

## Matrix4

Column-major 4x4 matrix. `public final float[] val = new float[16]`.

```java
Matrix4 mat = new Matrix4();        // identity by default
mat.idt();                          // reset to identity

// "setTo" methods — reset matrix, then apply ONE transform
mat.setToTranslation(x, y, z);     // or (Vector3)
mat.setToRotation(axis, degrees);   // Vector3 + float, or (ax,ay,az, degrees)
mat.setToScaling(x, y, z);         // or (Vector3)
mat.setToLookAt(direction, up);    // or (position, target, up)

// Post-multiply methods — compose onto existing matrix
mat.translate(x, y, z);            // mat = mat * T
mat.rotate(axis, degrees);         // mat = mat * R (also Quaternion overload)
mat.scale(sx, sy, sz);             // mat = mat * S

mat.mul(other);                    // mat = mat * other (post-multiply)
mat.inv();                         // invert in place
mat.tra();                         // transpose in place
float d = mat.det();               // determinant

// Extraction
Vector3 pos = mat.getTranslation(new Vector3());
Quaternion rot = mat.getRotation(new Quaternion());  // also (Quaternion, boolean normalizeAxes)

// Compose from components
mat.set(position, rotation, scale);  // Vector3, Quaternion, Vector3
mat.set(quaternion);                 // rotation only
```

**There is NO `setToRotation(Quaternion)`** — use `set(Quaternion)` instead.

## Matrix3

9-float 2D transform / normal matrix. `public float[] val = new float[9]` (NOT final).

```java
Matrix3 m3 = new Matrix3();
m3.set(matrix4);     // extract top-left 3x3 (for normal matrix)
m3.inv();            // invert in place
m3.mul(other);       // m3 = m3 * other
float d = m3.det();
```

## Quaternion

```java
new Quaternion()                           // identity (0,0,0,1)
new Quaternion(float x, float y, float z, float w)
new Quaternion(Quaternion other)           // copy
new Quaternion(Vector3 axis, float degrees)

q.idt();                                   // reset to identity (0,0,0,1)
q.set(other);                              // copy
q.setFromAxis(axis, degrees);              // or (ax,ay,az, degrees)
q.setFromAxisRad(axis, radians);           // or (ax,ay,az, radians)

// Euler angles — DEGREES, order is yaw/pitch/roll
q.setEulerAngles(yaw, pitch, roll);        // yaw=Y, pitch=X, roll=Z
q.setEulerAnglesRad(yaw, pitch, roll);     // same order, radians

q.getYaw();     // degrees (-180 to 180), rotation around Y
q.getPitch();   // degrees (-90 to 90), rotation around X
q.getRoll();    // degrees (-180 to 180), rotation around Z
// Also: getYawRad(), getPitchRad(), getRollRad()

q.slerp(endQuat, alpha);     // mutates this, alpha [0,1]
q.mul(other);                // this = this * other (Hamilton product)
q.mulLeft(other);            // this = other * this
q.nor();                     // normalize
q.conjugate();               // negate x,y,z (leave w)
q.transform(vector3);        // MUTATES the vector, returns the vector
q.toMatrix(float[16]);       // fills 16-float array, returns VOID (not this)
q.cpy();                     // new copy
```

**Gotchas:**
- `setEulerAngles` parameter order is **(yaw, pitch, roll)**, not (pitch, yaw, roll). Other engines differ.
- `transform(Vector3)` mutates the input vector — not the quaternion.
- `toMatrix()` returns `void`, not the Quaternion.
- Quaternion must be normalized for `getYaw/getPitch/getRoll` to be accurate.

## MathUtils

### Constants

| Constant | Value | Alias |
|---|---|---|
| `PI` | 3.14159... | |
| `PI2` | 6.28318... (2π) | |
| `HALF_PI` | 1.5708... (π/2) | |
| `E` | 2.71828... | |
| `radiansToDegrees` | 57.2957... | `radDeg` |
| `degreesToRadians` | 0.01745... | `degRad` |
| `FLOAT_ROUNDING_ERROR` | 0.000001f (1e-6) | |

### Random

```java
MathUtils.random()                    // float [0, 1)
MathUtils.random(int range)           // int [0, range] INCLUSIVE both ends
MathUtils.random(int start, int end)  // int [start, end] INCLUSIVE both ends
MathUtils.random(float range)         // float [0, range) EXCLUSIVE end
MathUtils.random(float start, float end)  // float [start, end) EXCLUSIVE end
MathUtils.randomSign()                // int: -1 or 1
MathUtils.randomBoolean()             // boolean
MathUtils.randomBoolean(float chance) // true if random() < chance
```

**int overloads are INCLUSIVE on both bounds. float overloads are EXCLUSIVE on the upper bound.** This catches people constantly.

### Trig (lookup-table — faster than Math.sin/cos)

| Method | Input | Returns |
|---|---|---|
| `sin(float rad)` | Radians | float |
| `cos(float rad)` | Radians | float |
| `sinDeg(float deg)` | Degrees | float |
| `cosDeg(float deg)` | Degrees | float |
| `atan2(float y, float x)` | y, x | Radians (−π to π) |
| `atan2Deg360(float y, float x)` | y, x | Degrees (0 to 360) |

### Utility

```java
MathUtils.clamp(value, min, max)   // float, int, long, short, double overloads
MathUtils.lerp(from, to, progress) // float
MathUtils.norm(rangeStart, rangeEnd, value)  // inverse lerp (NOT clamped)
MathUtils.map(inStart, inEnd, outStart, outEnd, value)  // remap (NOT clamped)
MathUtils.isZero(float)            // within FLOAT_ROUNDING_ERROR
MathUtils.isZero(float, tolerance) // within tolerance
MathUtils.isEqual(a, b)            // within FLOAT_ROUNDING_ERROR
MathUtils.isEqual(a, b, tolerance) // within tolerance
MathUtils.log2(float value)        // returns FLOAT (not int!)
MathUtils.lerpAngle(fromRad, toRad, progress)     // handles wrapping at 2π
MathUtils.lerpAngleDeg(fromDeg, toDeg, progress)  // handles wrapping at 360°
// Also: floor(float), ceil(float), round(float) — return int
// Also: nextPowerOfTwo(int), isPowerOfTwo(int)
```

## Interpolation

Usage: `Interpolation.NAME.apply(alpha)` where alpha in [0,1]. Also: `apply(start, end, alpha)`.

Naming pattern: `{category}`, `{category}In` (slow-to-fast), `{category}Out` (fast-to-slow).
Categories: `pow2`–`pow5`, `sine`, `exp5`, `exp10`, `circle`, `elastic`, `swing`, `bounce`.

Standalone: `linear`, `smooth` (smoothstep), `smooth2`, `smoother` (Perlin smootherstep).

**Aliases:** `fade` = `smoother` (NOT `smooth`), `slowFast` = `pow2In`, `fastSlow` = `pow2Out`.

Inverses exist ONLY for pow2 and pow3: `pow2InInverse`, `pow2OutInverse`, `pow3InInverse`, `pow3OutInverse`.

**DO NOT use** `quadIn`, `cubicOut`, `easeIn`, `easeOut`, `easeInOut`, `linear_in`, `quad` — **none exist**. Convention is `pow2`, `pow3`, etc.

Custom: `new Interpolation.Pow(6)`, `new Interpolation.Elastic(2, 10, 7, 1)`, `new Interpolation.Swing(2.5f)`.

## Intersector

Static utility — all methods are `public static`.

Key methods (all return boolean unless noted):
- `overlaps(Circle, Circle)`, `overlaps(Circle, Rectangle)`, `overlaps(Rectangle, Rectangle)`
- `overlapConvexPolygons(Polygon, Polygon)` — optional `MinimumTranslationVector` param for MTV
- `isPointInTriangle(...)`, `isPointInPolygon(...)` — Vector2 or float overloads
- `intersectSegments(x1,y1, x2,y2, x3,y3, x4,y4, Vector2 intersection)` — populates intersection
- `intersectRayTriangle(Ray, Vector3, Vector3, Vector3, Vector3 intersection)`
- `intersectLinePlane(...)` — returns **FLOAT (distance)**, NOT boolean
- `intersectRayBounds(Ray, BoundingBox, Vector3)`, `intersectRaySphere(Ray, Vector3, float, Vector3)`
- `nearestSegmentPoint(...)` — returns Vector2; `distanceSegmentPoint(...)` — returns float

## Common Mistakes

1. **Mutating vectors unintentionally** — `a.add(b)` changes `a`. Use `a.cpy().add(b)` to create a new vector. This applies to nearly every Vector method.
2. **Mutating Vector3.X/Y/Z/Zero constants** — These are mutable static fields, not true constants. `Vector3.Zero.set(1,0,0)` corrupts the constant globally. Never pass them to methods that mutate.
3. **Using invented Interpolation names** — There is no `quadIn`, `cubicOut`, `easeIn`, `easeInOut`. Use `pow2In`, `pow3Out`, etc. Use `fade` or `smoother` for smooth acceleration.
4. **Confusing `fade` with `smooth`** — `fade` is an alias for `smoother` (Perlin smootherstep), NOT for `smooth` (classic smoothstep).
5. **Wrong random bounds assumption** — `MathUtils.random(int start, int end)` is INCLUSIVE on both ends. `MathUtils.random(float start, float end)` is EXCLUSIVE on the upper bound.
6. **Calling `Intersector.overlap()` (singular)** — The method is `overlaps` (plural). There is no `overlap()`.
7. **Expecting `intersectLinePlane` to return boolean** — It returns `float` (distance from first point to plane), not boolean.
8. **Forgetting `Vector3.crs()` mutates** — Unlike Vector2's `crs()` which returns a float scalar, Vector3's `crs()` overwrites `this` with the cross product. Use `a.cpy().crs(b)`.
9. **Using deprecated Vector2 angle/rotate methods** — `angle()`, `rotate(float)`, `setAngle(float)`, `rotateAround(Vector2, float)` are all deprecated. Use `angleDeg()`, `rotateDeg()`, `setAngleDeg()`, `rotateAroundDeg()`.
10. **Allocating vectors in hot loops** — `new Vector2()` in render/update creates GC pressure. Declare reusable `private static final Vector2 tmp = new Vector2()` fields and call `tmp.set(...)`.
11. **Using `Matrix4.setToRotation(quaternion)`** — This method does not exist. Use `mat.set(quaternion)` or `mat.rotate(quaternion)` instead.
12. **Not calling `cpy()` before passing vectors to physics/AI** — Many libraries store references. If you reuse a temp vector, the stored reference silently changes value.
