---
name: libgdx-framebuffer-pixmap
description: Use when writing libGDX Java/Kotlin code involving FrameBuffer (FBO), render-to-texture, post-processing, FloatFrameBuffer, GLFrameBuffer, Pixmap, runtime texture generation, screen capture, pixel manipulation, or PixmapIO. Use when debugging upside-down FBO rendering, FBO nesting issues, native memory leaks from Pixmap, or blend state corruption from post-processing.
---

# libGDX FrameBuffer & Pixmap

Quick reference for render-to-texture (FBO) and CPU-side pixel manipulation. Covers `FrameBuffer`, `GLFrameBuffer`, `FloatFrameBuffer`, `Pixmap`, `PixmapIO`, and `Color` int conversions.

## FrameBuffer (FBO)

`com.badlogic.gdx.graphics.glutils.FrameBuffer` extends `GLFrameBuffer<Texture>`, implements `Disposable`.

### Construction

```java
// Standard — width/height in PIXELS, not world units
FrameBuffer fbo = new FrameBuffer(Pixmap.Format.RGBA8888, width, height, hasDepth);
FrameBuffer fbo = new FrameBuffer(Pixmap.Format.RGBA8888, width, height, hasDepth, hasStencil);

// Typical: match screen resolution
FrameBuffer fbo = new FrameBuffer(Pixmap.Format.RGBA8888,
    Gdx.graphics.getBackBufferWidth(), Gdx.graphics.getBackBufferHeight(), false);
```

- `hasDepth` adds a 16-bit depth renderbuffer (`GL_DEPTH_COMPONENT16`).
- `hasStencil` adds an 8-bit stencil renderbuffer (`GL_STENCIL_INDEX8`).
- Width/height are **pixel dimensions**. Do NOT pass world units or viewport units.

### begin() / end() Pattern

```java
fbo.begin();
// Binds FBO + sets glViewport to FBO dimensions.
// Does NOT save previous framebuffer or viewport state.
ScreenUtils.clear(0, 0, 0, 1);  // MUST clear — previous frame persists otherwise
batch.setProjectionMatrix(camera.combined);
batch.begin();
// ... render scene into FBO ...
batch.end();
fbo.end();
// Unbinds FBO (binds default framebuffer) + restores viewport to back buffer size.
```

`end(int x, int y, int width, int height)` — restores a specific viewport instead of auto-detecting back buffer size.

**Gotchas:**
- `begin()` does NOT save previous state. `end()` ALWAYS unbinds to the default framebuffer. There is no stack.
- You MUST clear after `begin()` — the FBO retains content from the previous frame.
- The camera/projection matrix used inside the FBO should match the FBO's dimensions, not the screen.

### Drawing the FBO Texture to Screen

The FBO texture is **vertically flipped** (OpenGL renders Y-up but textures sample Y-down). You MUST flip it:

```java
// Approach 1: TextureRegion with flip (recommended)
TextureRegion fboRegion = new TextureRegion(fbo.getColorBufferTexture());
fboRegion.flip(false, true);  // create once, reuse

// Draw to screen
batch.setProjectionMatrix(screenCamera.combined);
batch.begin();
batch.draw(fboRegion, 0, 0, screenWidth, screenHeight);
batch.end();
```

### Standard Post-Processing Pattern

```java
// 1. Render scene into FBO
fbo.begin();
ScreenUtils.clear(0, 0, 0, 1);
batch.setProjectionMatrix(gameCamera.combined);
batch.begin();
// ... draw game world ...
batch.end();
fbo.end();

// 2. Draw FBO texture to screen (with optional shader)
batch.setProjectionMatrix(screenCamera.combined);
batch.setShader(postProcessShader);  // optional: blur, vignette, etc.
batch.begin();
batch.draw(fboRegion, 0, 0, screenWidth, screenHeight);
batch.end();
batch.setShader(null);
```

### bind() vs begin()

| Method | Binds FBO | Sets Viewport | Saves Previous State |
|--------|-----------|---------------|---------------------|
| `begin()` | Yes | Yes (to FBO dimensions) | No |
| `end()` | Unbinds to default | Yes (to back buffer) | N/A |
| `bind()` | Yes | No | No |
| `unbind()` (static) | Unbinds to default | No | N/A |

Use `bind()`/`unbind()` when you manage the viewport yourself. Use `begin()`/`end()` for standard rendering.

### FBO Nesting — Does NOT Work

```java
// BROKEN — do NOT do this:
fbo1.begin();
  fbo2.begin();
  fbo2.end();   // unbinds to DEFAULT framebuffer, NOT fbo1
  // rendering here goes to screen, not fbo1!
fbo1.end();
```

`end()` always unbinds to the default framebuffer. There is no stack or save/restore mechanism. Structure FBO passes **sequentially**:

```java
// CORRECT — sequential passes:
fbo1.begin();
// render scene
fbo1.end();

fbo2.begin();
// render fbo1's texture with shader
fbo2.end();
```

### Key Methods

| Method | Returns | Notes |
|--------|---------|-------|
| `getColorBufferTexture()` | `Texture` | First color attachment. **Owned by FBO** — do NOT dispose separately. |
| `getTextureAttachments()` | `Array<Texture>` | All color attachments (for MRT). |
| `getWidth()` | `int` | FBO width in pixels. |
| `getHeight()` | `int` | FBO height in pixels. |
| `getFramebufferHandle()` | `int` | GL handle. Note: lowercase 'b' in "buffer". |
| `dispose()` | `void` | Disposes FBO, all attachments, AND the color texture(s). |
| `transfer(destination)` | `void` | Blit to another FBO (same dimensions required). GL30+. |
| `transfer(destination, copyBits)` | `void` | Blit with explicit buffer bits mask. GL30+. |

**DO NOT use** `fbo.getColorBufferTexture().dispose()` — the FBO owns this texture. Disposing it separately corrupts the FBO.

### FrameBufferBuilder (Advanced)

For custom FBO configurations (multiple color attachments, specific GL formats):

```java
FrameBuffer fbo = new GLFrameBuffer.FrameBufferBuilder(width, height)
    .addBasicColorTextureAttachment(Pixmap.Format.RGBA8888)
    .addBasicDepthRenderBuffer()
    .build();

// With explicit GL formats:
FrameBuffer fbo = new GLFrameBuffer.FrameBufferBuilder(width, height)
    .addColorTextureAttachment(GL30.GL_RGBA8, GL20.GL_RGBA, GL20.GL_UNSIGNED_BYTE)
    .addDepthTextureAttachment(GL30.GL_DEPTH_COMPONENT24, GL20.GL_UNSIGNED_INT)
    .build();
```

Builder class is `GLFrameBuffer.FrameBufferBuilder` (NOT `GLFrameBuffer.GLFrameBufferBuilder` — that's the abstract base).

Builder methods (all return builder for chaining):

| Method | Parameters |
|--------|-----------|
| `addBasicColorTextureAttachment` | `(Pixmap.Format)` |
| `addColorTextureAttachment` | `(int internalFormat, int format, int type)` |
| `addFloatAttachment` | `(int internalFormat, int format, int type, boolean gpuOnly)` |
| `addDepthTextureAttachment` | `(int internalFormat, int type)` |
| `addStencilTextureAttachment` | `(int internalFormat, int type)` |
| `addBasicDepthRenderBuffer` | `()` — uses `GL_DEPTH_COMPONENT16` |
| `addBasicStencilRenderBuffer` | `()` — uses `GL_STENCIL_INDEX8` |
| `addBasicStencilDepthPackedRenderBuffer` | `()` — uses `GL_DEPTH24_STENCIL8` |
| `addDepthRenderBuffer` | `(int internalFormat)` |
| `addStencilRenderBuffer` | `(int internalFormat)` |
| `addColorRenderBuffer` | `(int internalFormat)` |

### FloatFrameBuffer

`com.badlogic.gdx.graphics.glutils.FloatFrameBuffer` extends `FrameBuffer`. Uses `GL30.GL_RGBA32F` — for HDR rendering, deferred shading. Requires GL ES 3.0 / GL 3.0+.

```java
FloatFrameBuffer hdrFbo = new FloatFrameBuffer(width, height, hasDepth);
```

On mobile (non-Desktop), texture filter is forced to `Nearest` (linear filtering of float textures is not supported on GL ES).

Builder variant: `GLFrameBuffer.FloatFrameBufferBuilder`.

### Managed State

FBOs are **managed** — libGDX automatically recreates GL objects after context loss (Android). However, the **rendered contents** are lost. Only the FBO structure (handle, attachments) is rebuilt.

## Pixmap

`com.badlogic.gdx.graphics.Pixmap` implements `Disposable`. CPU-side pixel buffer — all operations are software-rendered, no GL.

**Coordinate system: Y-down, top-left origin** — unlike libGDX's default Y-up for rendering.

### Construction

```java
Pixmap pm = new Pixmap(256, 256, Pixmap.Format.RGBA8888);  // blank
Pixmap pm = new Pixmap(Gdx.files.internal("image.png"));    // from file (PNG, JPEG, BMP)
Pixmap pm = new Pixmap(encodedBytes, offset, len);           // byte[] of encoded image data
Pixmap pm = new Pixmap(encodedByteBuffer);                   // ByteBuffer of encoded image data
```

### Pixmap.Format

`Alpha`, `Intensity`, `LuminanceAlpha`, `RGB565`, `RGBA4444`, `RGB888`, `RGBA8888`

Use `RGBA8888` as the safe default. Other formats save memory but limit functionality.

### Drawing (CPU-side, no GL)

```java
pm.setColor(1, 0, 0, 1);                     // set draw color (float RGBA)
pm.setColor(Color.RED);                       // set draw color (Color object)
pm.setColor(0xFF0000FF);                      // set draw color (packed RGBA8888 int)

pm.fill();                                    // fill entire pixmap with current color
pm.drawPixel(x, y);                           // single pixel with current color
pm.drawPixel(x, y, 0xFF0000FF);              // single pixel with explicit RGBA8888 color
pm.drawLine(x1, y1, x2, y2);
pm.drawRectangle(x, y, w, h);                // outline
pm.fillRectangle(x, y, w, h);                // filled
pm.drawCircle(x, y, radius);                 // outline
pm.fillCircle(x, y, radius);                 // filled
pm.fillTriangle(x1, y1, x2, y2, x3, y3);   // filled only — NO drawTriangle() exists
```

There are NO `drawTriangle`, `drawArc`, `drawPolygon`, `drawEllipse`, or path methods.

### Pixmap-to-Pixmap Blitting

```java
pm.drawPixmap(src, x, y);                                              // draw entire src at (x,y)
pm.drawPixmap(src, x, y, srcX, srcY, srcW, srcH);                     // draw region of src, no scaling
pm.drawPixmap(src, srcX, srcY, srcW, srcH, dstX, dstY, dstW, dstH);  // with scaling
```

### Pixel Access

```java
int rgba = pm.getPixel(x, y);   // packed RGBA8888 int regardless of pixmap format
Color c = new Color();
Color.rgba8888ToColor(c, rgba); // unpack to Color (mutates c, returns void)
int packed = Color.rgba8888(c); // pack Color to RGBA8888 int

ByteBuffer pixels = pm.getPixels();  // direct ByteBuffer of raw pixel data
pm.setPixels(byteBuffer);           // replace pixel data from ByteBuffer
```

### Settings

```java
pm.setBlending(Pixmap.Blending.None);        // overwrite mode (no alpha blending)
pm.setBlending(Pixmap.Blending.SourceOver);  // alpha blending (default)
pm.setFilter(Pixmap.Filter.NearestNeighbour); // for drawPixmap scaling
pm.setFilter(Pixmap.Filter.BiLinear);         // for drawPixmap scaling
```

Set blending to `None` when writing opaque content or when you need to write specific alpha values.

### Creating Texture from Pixmap

```java
Texture tex = new Texture(pm);  // copies pixel data — Pixmap can be disposed after
pm.dispose();
```

The Texture copies the data. The Pixmap and Texture have independent lifetimes.

### Screen Capture

```java
// Reads from currently bound framebuffer (default or FBO)
// Coordinates use OpenGL BOTTOM-LEFT origin
Pixmap screenshot = Pixmap.createFromFrameBuffer(0, 0,
    Gdx.graphics.getBackBufferWidth(), Gdx.graphics.getBackBufferHeight());

// Result is Y-FLIPPED relative to screen — must flip for correct orientation:
PixmapIO.writePNG(Gdx.files.local("screenshot.png"), screenshot, 6, true); // flipY=true
screenshot.dispose();
```

**Gotchas:**
- `createFromFrameBuffer` is static. Uses `glReadPixels` with bottom-left origin.
- The returned Pixmap is Y-flipped vs screen appearance. Use `PixmapIO.writePNG` with `flipY=true` or manually flip.
- Always produces `RGBA8888` format.
- Works with FBOs too — reads from whatever framebuffer is currently bound.

### Disposal

```java
pm.dispose();       // MUST call — native heap memory
pm.isDisposed();    // check if already disposed
```

### Properties

```java
pm.getWidth();      // int — original dimensions
pm.getHeight();     // int
pm.getFormat();     // Pixmap.Format
pm.getGLFormat();   // int — GL format constant
pm.getGLType();     // int — GL type constant
```

### Async Download

```java
Pixmap.downloadFromUrl("https://example.com/image.png",
    new Pixmap.DownloadPixmapResponseListener() {
        public void downloadComplete(Pixmap pixmap) { /* use pixmap, must dispose */ }
        public void downloadFailed(Throwable t) { /* handle error */ }
    });
```

## PixmapIO

`com.badlogic.gdx.graphics.PixmapIO` — static utility for saving Pixmaps to files.

```java
PixmapIO.writePNG(fileHandle, pixmap);                         // default compression, no flip
PixmapIO.writePNG(fileHandle, pixmap, compression, flipY);     // compression: 0–9, flipY: boolean
```

There is NO 3-parameter `writePNG(file, pixmap, compression)` overload — the extended version requires all 4 params.

CIM format (libGDX custom compressed):
```java
PixmapIO.writeCIM(fileHandle, pixmap);
Pixmap pm = PixmapIO.readCIM(fileHandle);
```

Reusable PNG writer (avoids buffer reallocation):
```java
PixmapIO.PNG writer = new PixmapIO.PNG();
writer.setFlipY(true);            // default: true
writer.setCompression(6);         // deflate level
writer.write(fileHandle, pixmap);
writer.dispose();                  // reusable, dispose when done with all writes
```

## Platform Differences

| Behavior | Desktop | Android | iOS |
|----------|---------|---------|-----|
| FBO managed (recreated) | N/A (no context loss) | Yes — contents lost, structure rebuilt | GL context preserved |
| Default FBO handle | 0 | 0 | Non-zero (auto-detected) |
| FloatFrameBuffer | GL 3.0+ | GL ES 3.0+ | GL ES 3.0+ |
| `createFromFrameBuffer` | Works | Works | Works |
| Max FBO size | GPU-dependent | Often 4096×4096 | GPU-dependent |
| Float texture filtering | Linear works | Nearest only | Nearest only |

## Common Mistakes

1. **Drawing FBO texture without flipping** — FBO textures are Y-flipped. Use `TextureRegion.flip(false, true)` or the image renders upside-down.
2. **Disposing the FBO's color texture** — `getColorBufferTexture()` returns a texture owned by the FBO. Disposing it separately corrupts the FBO. Only call `fbo.dispose()`.
3. **Nesting FBO begin/end** — `end()` always unbinds to the default framebuffer, not the previously bound FBO. Structure FBO passes sequentially, never nested.
4. **Forgetting to clear after begin()** — FBO retains previous frame content. Call `ScreenUtils.clear()` after `fbo.begin()`.
5. **Using world units for FBO dimensions** — FBO constructor takes pixel dimensions. Use `Gdx.graphics.getBackBufferWidth/Height()` or a fixed pixel resolution, not camera viewport units.
6. **Creating Pixmap in render loop without disposing** — Pixmap allocates native memory. Creating one per frame without `dispose()` causes rapid memory exhaustion.
7. **Inventing `fbo.getTexture()`** — The method is `getColorBufferTexture()`. There is no `getTexture()`.
8. **Assuming `createFromFrameBuffer` uses screen coordinates** — It uses OpenGL bottom-left origin and the result is Y-flipped. Use `PixmapIO.writePNG` with `flipY=true` for correct orientation.
9. **Calling `scaleEffect` on wrong class** — Pixmap has no scale method. Use `drawPixmap()` with different src/dst rectangles for scaling.
10. **Forgetting Pixmap is Y-down** — Pixmap uses top-left origin (Y increases downward), unlike libGDX's rendering coordinate system (Y-up). Pixel coordinates from `getPixel()`/`drawPixel()` use this Y-down system.
11. **Using 3-param `writePNG`** — `PixmapIO.writePNG(file, pixmap, compression)` does not exist. Use the 4-param version: `writePNG(file, pixmap, compression, flipY)`.
12. **Setting Pixmap blending to SourceOver when writing alpha** — Default blending (`SourceOver`) composites alpha. Set `Blending.None` when you need to write specific alpha values or overwrite pixels completely.
