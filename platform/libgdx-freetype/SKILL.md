---
name: libgdx-freetype
description: Use when writing libGDX Java/Kotlin code that generates BitmapFont at runtime from .ttf/.otf files using gdx-freetype — FreeTypeFontGenerator, FreeTypeFontParameter, font size/color/border/shadow configuration, characters parameter for i18n, incremental glyph rendering for CJK, AssetManager integration with FreeTypeFontLoader, or density-scaled font sizes. Use when debugging missing glyphs, blurry fonts, generator disposal issues, or FreeType crashes on iOS.
---

# libGDX gdx-freetype

Runtime BitmapFont generation from .ttf/.otf files. Use instead of pre-baking fonts with Hiero when you need multiple sizes, dynamic scaling, or user-selectable fonts.

## Gradle Dependencies

```groovy
// core
implementation "com.badlogicgames.gdx:gdx-freetype:$gdxVersion"

// desktop
implementation "com.badlogicgames.gdx:gdx-freetype-platform:$gdxVersion:natives-desktop"

// android (all four ABIs)
natives "com.badlogicgames.gdx:gdx-freetype-platform:$gdxVersion:natives-armeabi-v7a"
natives "com.badlogicgames.gdx:gdx-freetype-platform:$gdxVersion:natives-arm64-v8a"
natives "com.badlogicgames.gdx:gdx-freetype-platform:$gdxVersion:natives-x86"
natives "com.badlogicgames.gdx:gdx-freetype-platform:$gdxVersion:natives-x86_64"

// iOS
natives "com.badlogicgames.gdx:gdx-freetype-platform:$gdxVersion:natives-ios"
```

The platform artifact is **`gdx-freetype-platform`**, not `gdx-freetype`. Missing platform natives causes `UnsatisfiedLinkError` at runtime.

**iOS/RoboVM:** Also add to `robovm.xml` inside `<config>`:
```xml
<forceLinkClasses>
    <pattern>com.badlogic.gdx.graphics.g2d.freetype.**</pattern>
</forceLinkClasses>
```
Without this, RoboVM's AOT compiler strips FreeType classes, causing runtime crashes on iOS.

## Basic Usage

```java
FreeTypeFontGenerator generator = new FreeTypeFontGenerator(Gdx.files.internal("fonts/myfont.ttf"));

FreeTypeFontParameter parameter = new FreeTypeFontParameter();
parameter.size = (int)(24 * Gdx.graphics.getDensity());  // density-scaled
parameter.color = Color.WHITE;
parameter.borderWidth = 1;
parameter.borderColor = Color.BLACK;
parameter.minFilter = Texture.TextureFilter.Linear;
parameter.magFilter = Texture.TextureFilter.Linear;
parameter.characters = FreeTypeFontGenerator.DEFAULT_CHARS;  // ASCII + common punctuation

BitmapFont font = generator.generateFont(parameter);
generator.dispose();  // safe — the font is independent of the generator
// font remains fully usable after generator disposal
```

**FreeType requires an OpenGL context.** It bakes glyphs into a texture atlas. It does not work in the headless backend or before `create()`.

**FreeTypeFontGenerator is NOT thread-safe.** Generating fonts from multiple threads simultaneously crashes. `AssetManager` handles synchronization internally, but manual multi-threaded generation will fail.

## Key Parameter Fields

| Field | Default | Description |
|---|---|---|
| `size` | 16 | Pixel height. Scale with `Gdx.graphics.getDensity()` for consistent physical size across devices. |
| `characters` | `DEFAULT_CHARS` | Which glyphs to bake. ASCII by default — add accented chars for European languages, or use `incremental` for CJK. |
| `color` | `Color.WHITE` | Font fill color |
| `borderWidth` | 0 | Outline thickness in pixels |
| `borderColor` | `Color.BLACK` | Outline color |
| `shadowOffsetX/Y` | 0 | Drop shadow offset |
| `shadowColor` | `Color(0,0,0,0.75f)` | Drop shadow color |
| `minFilter` / `magFilter` | `Nearest` | Texture filtering. Use `Linear` for smooth scaled text. |
| `hinting` | `AutoMedium` | `None`, `Slight`, `Medium`, `Full`, `AutoSlight`, `AutoMedium`, `AutoFull`. Default is best for most fonts. Use `None` for pixel art fonts; `Full` can cause artifacts with some fonts. |
| `kerning` | true | Adjust spacing between glyph pairs |
| `mono` | false | Monospace rendering (all glyphs same width) |
| `genMipMaps` | false | Generate mipmaps for minification |
| `incremental` | false | Render glyphs on demand instead of all at once — see CJK section |

## Disposal Lifecycle

**Generator and font are independent.** After `generateFont()`, the font owns its own texture. The generator is no longer needed.

```java
// Generate multiple sizes from one .ttf, then dispose generator
FreeTypeFontGenerator generator = new FreeTypeFontGenerator(Gdx.files.internal("font.ttf"));

FreeTypeFontParameter param = new FreeTypeFontParameter();
param.size = 16;
BitmapFont small = generator.generateFont(param);
param.size = 24;
BitmapFont medium = generator.generateFont(param);
param.size = 48;
BitmapFont large = generator.generateFont(param);

generator.dispose();  // fonts remain usable

// In dispose():
small.dispose();
medium.dispose();
large.dispose();
```

**Exception — incremental mode:** When `parameter.incremental = true`, the generator must stay alive because it renders new glyphs on demand. Dispose the generator only after disposing the font. See CJK section below.

**Generated BitmapFonts are managed textures** — they auto-reload after Android GL context loss like any other managed resource. Do NOT re-run the generator in `resume()` to "reload" fonts.

## Characters Parameter (i18n)

`DEFAULT_CHARS` covers basic ASCII. For European languages, add accented characters:

```java
parameter.characters = FreeTypeFontGenerator.DEFAULT_CHARS
    + "ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿ"
    + "ŁłŃńŚśŹźŻżŒœ¿¡«»";
```

Characters not in the set render as missing glyphs. If text looks broken, check this parameter first.

**Atlas size:** The default atlas page is 1024x1024. Large character sets without incremental mode can fill it, silently dropping glyphs. For large sets, either use `incremental = true` or provide a larger packer: `parameter.packer = new PixmapPacker(2048, 2048, Pixmap.Format.RGBA8888, 1, false);`

## Incremental Rendering (CJK)

CJK character sets have thousands of glyphs. Baking them all upfront creates enormous textures and long load times. Use incremental mode instead:

```java
FreeTypeFontGenerator generator = new FreeTypeFontGenerator(Gdx.files.internal("fonts/NotoSansCJK.ttf"));
FreeTypeFontParameter param = new FreeTypeFontParameter();
param.size = 24;
param.incremental = true;  // glyphs rendered on first use
param.characters = "";     // start empty — glyphs added on demand

BitmapFont cjkFont = generator.generateFont(param);
// DO NOT dispose generator — it's needed to render new glyphs
```

**With `incremental = true`:**
- Glyphs are baked into the atlas the first time they're drawn
- The generator MUST stay alive — dispose it only after the font
- Small hitch on first render of each new glyph
- Pre-load common characters during a loading screen to reduce hitches

```java
// Dispose order for incremental fonts
cjkFont.dispose();
generator.dispose();  // AFTER the font
```

## AssetManager Integration

Register the FreeType loaders, then load fonts asynchronously:

```java
AssetManager assets = new AssetManager();

// Register loaders (once, at startup)
assets.setLoader(FreeTypeFontGenerator.class,
    new FreeTypeFontGeneratorLoader(assets.getFileHandleResolver()));
assets.setLoader(BitmapFont.class, ".ttf",
    new FreetypeFontLoader(assets.getFileHandleResolver()));

// Queue a font for loading
FreetypeFontLoader.FreeTypeFontLoaderParameter params =
    new FreetypeFontLoader.FreeTypeFontLoaderParameter();
params.fontFileName = "fonts/myfont.ttf";           // actual .ttf path
params.fontParameters.size = (int)(24 * Gdx.graphics.getDensity());
params.fontParameters.minFilter = Texture.TextureFilter.Linear;
params.fontParameters.magFilter = Texture.TextureFilter.Linear;

assets.load("myfont-24.ttf", BitmapFont.class, params);  // key is arbitrary, not a file path

// In render loop:
if (assets.update()) {
    BitmapFont font = assets.get("myfont-24.ttf", BitmapFont.class);
}
```

The asset key (first argument to `load()`) doesn't need to match the actual .ttf filename, but it **must end in `.ttf`** — the FreeType loader is registered for the `.ttf` extension. A key like `"heading-font"` without `.ttf` won't match the loader and silently fails to load.

## Density Scaling

Scale font size by screen density so text appears the same physical size across devices:

```java
parameter.size = (int)(24 * Gdx.graphics.getDensity());
// mdpi (1.0) → 24px, xhdpi (2.0) → 48px, xxhdpi (3.0) → 72px
```

## Common Mistakes

1. **Wrong platform artifact name** — The natives artifact is `gdx-freetype-platform`, not `gdx-freetype`. Using the wrong name compiles fine but crashes with `UnsatisfiedLinkError` at runtime.
2. **Disposing generator before generating the font** — The generator must be alive when `generateFont()` is called. Dispose it after.
3. **Thinking font disposal is tied to generator disposal** — They're independent. Disposing the generator does NOT affect already-generated fonts (unless using incremental mode).
4. **Disposing generator in incremental mode** — When `incremental = true`, the generator must stay alive to render new glyphs on demand. Dispose the generator only after the font.
5. **Missing `characters` for i18n** — `DEFAULT_CHARS` is ASCII only. European accented characters (é, ñ, ü) must be added explicitly or they render as missing glyphs.
6. **Not knowing about `incremental` for CJK** — Baking all CJK glyphs upfront creates huge textures. Use `parameter.incremental = true` for on-demand rendering.
7. **Suggesting Hiero when runtime generation is needed** — Hiero pre-bakes fonts at build time. Use FreeType when sizes must be computed at runtime (density scaling, user preferences).
8. **Missing platform natives in Gradle** — The core `gdx-freetype` dependency alone is not enough. Each platform needs its `gdx-freetype-platform` natives or FreeType crashes at runtime.
9. **Missing robovm.xml forceLinkClasses for iOS** — RoboVM strips FreeType classes without this entry. App compiles but crashes on iOS.
10. **Hardcoding pixel size without density scaling** — `parameter.size = 24` looks different on every device. Use `(int)(24 * Gdx.graphics.getDensity())` for consistent physical size.
11. **Using FreeType in headless backend** — FreeType bakes glyphs into a GL texture atlas. It requires an OpenGL context and does not work in headless mode.
12. **Re-running generator in `resume()` on Android** — Generated BitmapFonts are managed textures and auto-reload after GL context loss. Regenerating wastes time and leaks the old font.
13. **AssetManager key without `.ttf` extension** — The FreeType loader is registered for `.ttf`. A key like `"heading-font"` won't match — use `"heading-font.ttf"` instead.
