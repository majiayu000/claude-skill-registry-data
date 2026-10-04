---
name: libgdx-bitmap-font-text
description: Use when writing libGDX Java/Kotlin code involving text rendering (BitmapFont, GlyphLayout, BitmapFontCache), NinePatch scalable graphics, DistanceFieldFont, or color markup language. Use when debugging wrong text position, blurry scaled fonts, text measurement, or NinePatch stretching issues.
---

# libGDX BitmapFont, Text & NinePatch

Quick reference for BitmapFont text rendering, GlyphLayout measurement, BitmapFontCache, NinePatch, DistanceFieldFont, and color markup. Covers `com.badlogic.gdx.graphics.g2d.BitmapFont`, `GlyphLayout`, `BitmapFontCache`, `NinePatch`, `DistanceFieldFont`.

## BitmapFont

Pre-rendered font stored as texture(s) + `.fnt` descriptor. Created with Hiero, BMFont, or at runtime via FreeType (see `libgdx-freetype` skill).

### Default Font

```java
BitmapFont font = new BitmapFont(); // Built-in 15px Liberation Sans
```

Useful for prototyping only. The default font is bundled in the libGDX JAR.

### Constructors

```java
new BitmapFont()                                              // default 15px Liberation Sans
new BitmapFont(boolean flip)                                  // default font, flipped
new BitmapFont(FileHandle fontFile)                           // load from .fnt
new BitmapFont(FileHandle fontFile, boolean flip)
new BitmapFont(FileHandle fontFile, FileHandle imageFile, boolean flip)
new BitmapFont(FileHandle fontFile, FileHandle imageFile, boolean flip, boolean integer)
new BitmapFont(FileHandle fontFile, TextureRegion region)     // custom texture
new BitmapFont(FileHandle fontFile, TextureRegion region, boolean flip)
new BitmapFont(BitmapFontData data, TextureRegion region, boolean integer)
new BitmapFont(BitmapFontData data, Array<TextureRegion> pageRegions, boolean integer)
```

- **flip**: If `true`, Y=0 is top (top-down coordinates). Default `false` (Y-up, libGDX standard). Scene2D uses unflipped fonts.
- **integer**: If `true`, positions are rounded to integers to reduce filtering artifacts. Default `true`.

### draw() Methods — CRITICAL

**The `y` parameter is the top of capital letters (cap height), NOT the baseline, NOT the bottom of text.**

```java
// All return GlyphLayout except the GlyphLayout overload which returns void
GlyphLayout draw(Batch batch, CharSequence str, float x, float y)
GlyphLayout draw(Batch batch, CharSequence str, float x, float y,
    float targetWidth, int halign, boolean wrap)
GlyphLayout draw(Batch batch, CharSequence str, float x, float y,
    int start, int end, float targetWidth, int halign, boolean wrap)
GlyphLayout draw(Batch batch, CharSequence str, float x, float y,
    int start, int end, float targetWidth, int halign, boolean wrap, String truncate)
void draw(Batch batch, GlyphLayout layout, float x, float y)  // pre-computed layout
```

- `x` — left edge of text.
- `y` — top of most capital letters (cap height position). The GlyphLayout height is the distance from `y` down to the baseline.
- `targetWidth` — max width for wrapping/alignment/truncation.
- `halign` — `Align.left`, `Align.center`, or `Align.right` (lowercase! NOT `Align.CENTER`).
- `wrap` — word wrap within `targetWidth`.
- `truncate` — if non-null, truncate with this suffix (e.g., `"..."`) instead of wrapping.

**Gotchas:**
- `draw()` must be called between `batch.begin()` / `batch.end()`.
- All `draw()` calls clear the internal cache. For static text drawn every frame, use `BitmapFontCache` instead.
- The returned `GlyphLayout` is owned by the font's internal cache and will be overwritten on the next `draw()` call. Copy metrics immediately if needed.

### Color and Scaling

```java
font.setColor(Color.RED);                    // affects subsequent draws
font.setColor(1, 0, 0, 1);                  // r, g, b, a
Color c = font.getColor();                   // returns mutable Color — modify in place

font.getData().setScale(2f);                 // uniform scale (on BitmapFontData, NOT BitmapFont)
font.getData().setScale(2f, 3f);             // scaleX, scaleY (throws if 0)
float sx = font.getScaleX();                 // convenience getters on BitmapFont
float sy = font.getScaleY();
```

**DO NOT use `font.setScale()`** — no such method exists on BitmapFont. Use `font.getData().setScale()`.

**DO NOT use `font.setSize()`** — no such method exists. Scale is the only option, and it causes blurriness. For clean multi-size text, generate separate BitmapFonts at each size (or use FreeType at runtime).

### Metrics

All metric methods are on BitmapFont (convenience delegates to BitmapFontData):

```java
font.getLineHeight()      // distance between baselines of consecutive lines
font.getCapHeight()       // top of capitals to baseline
font.getXHeight()         // top of lowercase to baseline
font.getAscent()          // cap height to top of tallest glyph
font.getDescent()         // baseline to bottom of lowest descender (NEGATIVE value)
font.getSpaceXadvance()   // width of space character
```

### Other Methods

```java
font.getData()                     // returns BitmapFontData
font.getData().markupEnabled       // public boolean field, default false
font.getRegions()                  // Array<TextureRegion> — texture pages
font.getRegion()                   // first TextureRegion (convenience)
font.getCache()                    // internal BitmapFontCache (expert use)
font.newFontCache()                // creates new independent BitmapFontCache
font.setFixedWidthGlyphs("0123456789")  // make digits fixed-width for score display
font.ownsTexture()                 // true if font created the texture (dispose will free it)
font.setOwnsTexture(boolean)       // control texture ownership
font.dispose()                     // disposes texture(s) IF font owns them
```

**DO NOT use `font.getBounds()`** — removed in libGDX 1.5.6. Use `GlyphLayout` for text measurement.

## GlyphLayout (Text Measurement)

Computes text metrics without drawing. Implements `Pool.Poolable`.

### Constructors

```java
new GlyphLayout()
new GlyphLayout(BitmapFont font, CharSequence str)
new GlyphLayout(BitmapFont font, CharSequence str, Color color,
    float targetWidth, int halign, boolean wrap)
new GlyphLayout(BitmapFont font, CharSequence str, int start, int end, Color color,
    float targetWidth, int halign, boolean wrap, String truncate)
```

### setText() — Reuse Without Allocating

```java
layout.setText(font, str)
layout.setText(font, str, color, targetWidth, halign, wrap)
layout.setText(font, str, start, end, color, targetWidth, halign, wrap, truncate)
```

### Public Fields (NOT methods)

```java
layout.width    // actual rendered width (float)
layout.height   // actual rendered height (float) — distance from y to baseline
layout.runs     // Array<GlyphRun> — one per line segment
layout.glyphCount  // total glyphs
```

### Centering Example

```java
GlyphLayout layout = new GlyphLayout(font, "Hello");
float x = (screenWidth - layout.width) / 2;
float y = (screenHeight + layout.height) / 2; // y is TOP of text, so add height
font.draw(batch, layout, x, y);
```

### Pooling

```java
GlyphLayout layout = Pools.obtain(GlyphLayout.class);
layout.setText(font, "text");
// ... use layout.width, layout.height ...
Pools.free(layout);  // calls reset(), returns to pool
```

**Gotchas:**
- `width` and `height` are **public fields**, not methods. `layout.width` not `layout.getWidth()`.
- Reuse layouts with `setText()` to avoid per-frame allocation.

## BitmapFontCache

Pre-computes vertex data for static text. Avoids recomputing glyph positions every frame.

```java
BitmapFontCache cache = new BitmapFontCache(font);
BitmapFontCache cache = new BitmapFontCache(font, boolean integer);
// Or get the font's internal cache:
BitmapFontCache cache = font.getCache();
```

### Key Methods

```java
// setText clears then adds (returns GlyphLayout)
GlyphLayout setText(str, x, y)
GlyphLayout setText(str, x, y, targetWidth, halign, wrap)
GlyphLayout setText(str, x, y, start, end, targetWidth, halign, wrap)
GlyphLayout setText(str, x, y, start, end, targetWidth, halign, wrap, truncate)
void setText(GlyphLayout layout, x, y)         // from pre-computed layout, returns VOID

// addText appends without clearing (returns GlyphLayout)
GlyphLayout addText(str, x, y)
GlyphLayout addText(str, x, y, targetWidth, halign, wrap)
GlyphLayout addText(str, x, y, start, end, targetWidth, halign, wrap)
GlyphLayout addText(str, x, y, start, end, targetWidth, halign, wrap, truncate)
void addText(GlyphLayout layout, x, y)         // returns VOID

// Drawing
void draw(Batch batch)                          // Batch interface, not SpriteBatch
void draw(Batch batch, int start, int end)      // character range
void draw(Batch batch, float alphaModulation)   // alpha multiplier

// Positioning (without recomputing glyphs)
void setPosition(float x, float y)
void translate(float xAmount, float yAmount)
float getX()
float getY()

// Color
void setColor(Color color)     // for FUTURE text
void setColor(float r, float g, float b, float a)
Color getColor()               // color for future text
void setColors(Color tint)     // overwrites ALL cached text to flat color
void setColors(float r, float g, float b, float a)
void tint(Color tint)          // multiplies tint with each glyph's existing color (preserves markup colors)
void setAlphas(float alpha)    // changes only alpha, preserves RGB

void clear()
```

**Key distinction:** `setColor()`/`getColor()` affect **subsequently added** text. `setColors()` and `tint()` affect **already cached** text. `tint()` preserves per-glyph color variation from markup; `setColors()` overwrites to flat color.

## Color Markup

Inline color tags in text strings. **Color only — no size, bold, or italic markup.**

### Enable

```java
font.getData().markupEnabled = true;  // default is false
```

Or in Skin JSON:
```json
{ "com.badlogic.gdx.graphics.g2d.BitmapFont": {
    "default-font": { "file": "myfont.fnt", "markupEnabled": true }
}}
```

### Syntax

| Tag | Effect |
|---|---|
| `[RED]` | Named color (case-sensitive, ALL_CAPS for built-in) |
| `[#FF0000]` | Hex `RRGGBB` (alpha defaults to FF) |
| `[#FF0000AA]` | Hex `RRGGBBAA` with explicit alpha |
| `[]` | Pop to previous color (stack-based) |
| `[[` | Escaped literal `[` character |

```java
font.draw(batch, "[RED]Warning:[] normal text", x, y);
font.draw(batch, "[#00FF00]green [#FF000080]translucent red", x, y);
font.draw(batch, "Array index [[0]", x, y); // displays: Array index [0]
```

### Built-in Color Names (35 total, from `Colors` class)

`CLEAR`, `CLEAR_WHITE`, `BLACK`, `WHITE`, `LIGHT_GRAY`, `GRAY`, `DARK_GRAY`, `BLUE`, `NAVY`, `ROYAL`, `SLATE`, `SKY`, `CYAN`, `TEAL`, `GREEN`, `CHARTREUSE`, `LIME`, `FOREST`, `OLIVE`, `YELLOW`, `GOLD`, `GOLDENROD`, `ORANGE`, `BROWN`, `TAN`, `FIREBRICK`, `RED`, `SCARLET`, `CORAL`, `SALMON`, `PINK`, `MAGENTA`, `PURPLE`, `VIOLET`, `MAROON`

### Custom Colors

```java
Colors.put("PERU", Color.valueOf("CD853F"));
// Then use: font.draw(batch, "[PERU]custom color[]", x, y);
```

**Gotchas:**
- Unknown color names and malformed hex codes are rendered as literal text (silently ignored).
- When using markup with Scene2D Labels, remove `fontColor` from `LabelStyle` in skin JSON — it overrides markup colors.
- `[]` is a **pop** operation, not "reset to default." Excess pops are silently ignored.

## NinePatch

Scalable image preserving corners and edges. Used for UI backgrounds (buttons, panels).

### Constructors

```java
new NinePatch(TextureRegion region, int left, int right, int top, int bottom) // border widths in px
new NinePatch(Texture texture, int left, int right, int top, int bottom)
new NinePatch(TextureRegion... patches)       // 9 explicit regions (TOP_LEFT..BOTTOM_RIGHT)
new NinePatch(TextureRegion region)           // degenerate: center-only, stretches uniformly
new NinePatch(Texture texture)                // degenerate: center-only
new NinePatch(NinePatch ninePatch)            // copy
new NinePatch(NinePatch ninePatch, Color color)
```

Constructor border parameters are **`int`**, not float. Order is `left, right, top, bottom`.

### Drawing

```java
ninePatch.draw(Batch batch, float x, float y, float width, float height)
ninePatch.draw(Batch batch, float x, float y, float originX, float originY,
    float width, float height, float scaleX, float scaleY, float rotation)
```

Parameter type is `Batch` (interface), not `SpriteBatch`.

### Dimensions

```java
ninePatch.getTotalWidth()    // leftWidth + middleWidth + rightWidth (minimum width)
ninePatch.getTotalHeight()   // topHeight + middleHeight + bottomHeight (minimum height)
ninePatch.getLeftWidth()     // all six patch dimensions have getters AND setters
ninePatch.getRightWidth()
ninePatch.getTopHeight()
ninePatch.getBottomHeight()
ninePatch.getMiddleWidth()
ninePatch.getMiddleHeight()
```

### Padding (for content insets)

```java
ninePatch.getPadLeft()       // returns padLeft if set, else getLeftWidth()
ninePatch.getPadRight()      // same pattern for right/top/bottom
ninePatch.setPadding(left, right, top, bottom)
```

### Color

```java
ninePatch.setColor(Color color)  // tint (blended with Batch color at draw time)
ninePatch.getColor()             // returns mutable Color, default WHITE
```

### From TextureAtlas

```java
NinePatch patch = atlas.createPatch("panel");  // reads split/pad data from .atlas file
```

Returns `null` if region not found. Throws `IllegalArgumentException` if region has no split data. Cache the result — this method does string lookup + new allocation each call.

### NinePatchDrawable (Scene2D wrapper)

```java
NinePatchDrawable drawable = new NinePatchDrawable(ninePatch);
drawable.setPatch(ninePatch);         // also sets minWidth/minHeight/padding from patch
NinePatchDrawable tinted = drawable.tint(Color.GRAY); // returns NEW drawable with tinted copy
```

## DistanceFieldFont

Resolution-independent text using signed distance field textures. Extends `BitmapFont`.

```java
DistanceFieldFont font = new DistanceFieldFont(Gdx.files.internal("myfont.fnt"));
```

Has 8 constructors mirroring most BitmapFont overloads (missing: no-arg default font and flip-only). Automatically sets `TextureFilter.Linear` on load.

### Shader Setup — REQUIRED

```java
ShaderProgram shader = DistanceFieldFont.createDistanceFieldShader(); // static method
batch.setShader(shader);
// ... draw distance field font ...
batch.setShader(null); // restore default shader for non-SDF rendering
```

The shader uses a `u_smoothing` uniform. The font's internal `DistanceFieldFontCache` sets this uniform automatically before/after each draw, flushing the batch as needed. This means **you only need to set the shader on the batch** — smoothing is handled internally.

### Smoothing Control

```java
font.setDistanceFieldSmoothing(float smoothing) // on DistanceFieldFont, NOT BitmapFont
font.getDistanceFieldSmoothing()
```

Smoothing is automatically scaled by `getScaleX()` internally.

### Generating SDF Fonts

Use Hiero with the "Distance field" effect, or external tools like `msdf-atlas-gen`. The `.fnt` file format is standard BMFont; only the texture is different (stores distance values in alpha channel).

## Align Constants

All lowercase. `com.badlogic.gdx.utils.Align`:

```java
Align.center       // 1    DO NOT use Align.CENTER (doesn't exist)
Align.top          // 2
Align.bottom       // 4
Align.left         // 8
Align.right        // 16
Align.topLeft      // top | left
Align.topRight     // top | right
Align.bottomLeft   // bottom | left
Align.bottomRight  // bottom | right
```

## Integration Notes

- **FreeType** (see `libgdx-freetype` skill): Generates BitmapFont at runtime from `.ttf`/`.otf`. The result IS a BitmapFont — all APIs here apply.
- **Scene2D** (see `libgdx-scene2d-ui` skill): `Label` wraps BitmapFont. Skin loads BitmapFont from `.fnt` files and supports `markupEnabled` in JSON.
- **AssetManager** (see `gdx-assetmanager` skill): Loads BitmapFont asynchronously. Do NOT manually dispose AssetManager-loaded fonts.

## Common Mistakes

1. **Expecting y to be the bottom of text** — `y` in `draw()` is the top of capital letters (cap height), not the baseline or bottom. To position text at a bottom y, use `y + layout.height`.
2. **Using `font.getBounds()`** — Removed in libGDX 1.5.6. Use `GlyphLayout` to measure text.
3. **Using `font.setScale()` or `font.setSize()`** — Neither exists on BitmapFont. Use `font.getData().setScale()`. Scaling causes blurriness — generate fonts at the needed size instead.
4. **Using `Align.CENTER`** — Does not exist. Align constants are lowercase: `Align.center`, `Align.left`, `Align.right`.
5. **Allocating GlyphLayout every frame** — Reuse with `setText()` or use `BitmapFontCache` for static text. GlyphLayout implements `Poolable` for pool-based reuse.
6. **Forgetting `markupEnabled` before using color tags** — Tags render as literal text like `[RED]` if markup is not enabled.
7. **Disposing AssetManager-loaded font** — Causes double-dispose crash. Only dispose fonts you created with `new BitmapFont(...)`.
8. **Calling `draw()` outside batch.begin()/end()** — Same rules as SpriteBatch. Will throw or produce no output.
9. **Confusing NinePatch constructor parameter order** — It is `left, right, top, bottom` (NOT left, top, right, bottom).
10. **Not caching `atlas.createPatch()` result** — Does string lookup and allocates a new NinePatch each call. Call once and store the result.
11. **Using `draw(Batch, GlyphLayout, x, y)` and expecting a return value** — This overload returns `void`. The other `draw()` overloads return `GlyphLayout`.
12. **Setting DistanceFieldFont shader but not `setDistanceFieldSmoothing()`** — The default smoothing value of 0 disables the SDF effect. Set a positive value (typically the font's spread value divided by the texture scale).
