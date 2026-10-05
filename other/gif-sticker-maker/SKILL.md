---
name: gif-sticker-maker
description: Animated GIF and sticker creation expertise using AI image generation, video processing, and frame animation. Use when creating animated stickers.
---

# GIF and Sticker Maker

Structured guidance for creating animated GIFs and stickers using AI image generation, video processing, and programmatic frame animation. Covers the full pipeline from image generation through animation assembly to platform-specific optimization.

## When to Use This Skill

Use this skill for:

- Generating animated stickers from text prompts using AI image providers
- Converting video clips or screen recordings into optimized GIFs
- Building sprite sheet animations with tweening and easing
- Creating avatar generators with animated expression cycles
- Automating sticker pack creation for Telegram, Discord, Slack, or WhatsApp
- Applying animation effects (bounce, pulse, rotate, fade) to static images
- Optimizing GIF file sizes while preserving visual quality

**Trigger phrases**: "animated GIF", "sticker maker", "GIF creation", "sticker generator", "sprite animation", "video to GIF", "avatar animation", "animated emoji", "GIF optimization", "sticker pack", "frame animation", "Pillow GIF", "ffmpeg GIF", "animated sticker"

## What This Skill Does

Provides GIF and sticker creation patterns including:

- **Pipeline Architecture**: Image generation, frame assembly, GIF encoding, and optimization stages
- **AI Image Generation**: Provider-agnostic integration with DALL-E, Stable Diffusion, and other APIs
- **Pillow GIF Assembly**: Frame generation, palette optimization, duration control, looping, transparency
- **ffmpeg Conversion**: Video-to-GIF with two-pass palette generation, scaling, and frame rate control
- **Animation Techniques**: Sprite sheets, tweening, easing functions, keyframe interpolation, bounce/pulse/rotate effects
- **Sticker Formatting**: Transparent backgrounds, outline strokes, caption overlays, platform-specific sizing
- **Batch Processing**: Parallel generation, file size targets, color reduction, dithering, output validation

## Instructions

### Step 1: Pipeline Architecture and Tool Selection

The GIF and sticker creation pipeline flows through four stages: content generation, frame preparation, animation assembly, and output optimization. Select tools based on your input source and quality requirements.

**Pipeline Overview**:

```
Input Source          Frame Preparation       Assembly            Optimization
-----------          -----------------       --------            ------------
AI-generated      -> Resize / crop        -> Pillow GIF      -> Color reduction
  images             Remove background       assembly            Lossy compression
                     Add outlines                                Size validation
Video clip        -> Extract frames       -> ffmpeg palette   -> Frame rate trim
                     Select key frames       generation          Dimension scaling
                     Apply filters
Sprite sheet      -> Slice into frames    -> Pillow sequence  -> Dithering
                     Apply tweening          with duration       Palette optimization
                     Easing interpolation    control
Static image      -> Duplicate + transform -> Pillow animate  -> Loop optimization
                     Apply effects            with effects       File size check
```

**Tool Selection Matrix**:

| Tool | Best For | Install | Notes |
|------|----------|---------|-------|
| Pillow (Python) | Frame-by-frame GIF assembly, text overlays, effects | `pip install Pillow` | Pure Python, cross-platform |
| ffmpeg | Video-to-GIF, scaling, frame extraction, palette gen | System package | Industry standard, CLI-based |
| ImageMagick | GIF optimization, format conversion, batch ops | System package | `convert` and `gifsicle` combo |
| sharp (Node.js) | Server-side image processing, web pipelines | `npm install sharp` | Fast, libvips-based |
| gifsicle | GIF optimization, lossy compression, frame editing | System package | Specialized GIF optimizer |
| APNG Assembler | Animated PNG for platforms that support it | System package | Lossless alternative to GIF |

**Project Scaffold**:

```python
from pathlib import Path

# Standard project layout for a sticker generation pipeline
PROJECT_LAYOUT = {
    "src/": "Pipeline source code",
    "src/generators/": "AI image generation adapters",
    "src/processors/": "Frame processing (resize, crop, effects)",
    "src/assemblers/": "GIF/APNG assembly modules",
    "src/optimizers/": "File size optimization and validation",
    "assets/sprites/": "Source sprite sheets",
    "assets/fonts/": "Fonts for text overlays",
    "output/": "Generated GIFs and stickers",
    "output/previews/": "Low-res previews for review",
    "config/": "Platform presets and generation configs",
}

# Configuration dataclass for the pipeline
from dataclasses import dataclass, field

@dataclass
class PipelineConfig:
    """Configuration for a GIF/sticker generation run."""
    output_dir: Path = Path("output")
    width: int = 512
    height: int = 512
    frame_count: int = 24
    frame_duration_ms: int = 80
    loop_count: int = 0          # 0 = infinite loop
    max_file_size_kb: int = 256
    max_colors: int = 256
    transparent_background: bool = True
    platform: str = "telegram"   # telegram, discord, slack, whatsapp
```

**Platform Presets**:

```python
PLATFORM_PRESETS: dict[str, dict] = {
    "telegram": {
        "max_size_kb": 512,
        "dimensions": (512, 512),
        "format": "webm",            # Telegram prefers WebM for animated stickers
        "fallback_format": "gif",
        "max_duration_s": 3,
        "max_fps": 30,
    },
    "discord": {
        "max_size_kb": 256,           # Standard emoji limit
        "dimensions": (128, 128),     # Emoji size; stickers can be larger
        "format": "gif",
        "max_duration_s": 5,
        "max_fps": 50,
    },
    "slack": {
        "max_size_kb": 128,           # Custom emoji limit
        "dimensions": (128, 128),
        "format": "gif",
        "max_duration_s": None,       # No strict limit
        "max_fps": 30,
    },
    "whatsapp": {
        "max_size_kb": 500,
        "dimensions": (512, 512),
        "format": "webp",             # WhatsApp uses animated WebP
        "fallback_format": "gif",
        "max_duration_s": 6,
        "max_fps": 30,
    },
    "imessage": {
        "max_size_kb": 500,
        "dimensions": (618, 618),
        "format": "gif",              # or APNG
        "max_duration_s": None,
        "max_fps": 30,
    },
}
```

### Step 2: AI Image Generation Integration

Integrate with AI image generation providers using a provider-agnostic adapter pattern. This allows swapping providers without changing the pipeline logic.

**Provider Adapter Interface**:

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path

@dataclass
class GenerationRequest:
    """Provider-agnostic image generation request."""
    prompt: str
    negative_prompt: str = ""
    width: int = 512
    height: int = 512
    num_images: int = 1
    style: str = "sticker"        # sticker, pixel-art, cartoon, chibi, funko
    seed: int | None = None       # For reproducibility

@dataclass
class GeneratedImage:
    """Result from an image generation provider."""
    data: bytes
    width: int
    height: int
    provider: str
    seed: int | None = None
    metadata: dict = None

    def __post_init__(self) -> None:
        if self.metadata is None:
            self.metadata = {}

class ImageGenerator(ABC):
    """Abstract adapter for AI image generation providers."""

    @abstractmethod
    async def generate(self, request: GenerationRequest) -> list[GeneratedImage]:
        """Generate images from a text prompt."""
        ...

    @abstractmethod
    async def check_health(self) -> bool:
        """Verify the provider is accessible and quota is available."""
        ...
```

**OpenAI DALL-E Adapter**:

```python
import httpx
import base64

class DallEGenerator(ImageGenerator):
    """Adapter for OpenAI DALL-E image generation."""

    def __init__(self, api_key: str, model: str = "dall-e-3") -> None:
        self._api_key = api_key
        self._model = model
        self._base_url = "https://api.openai.com/v1"

    async def generate(self, request: GenerationRequest) -> list[GeneratedImage]:
        prompt = self._build_sticker_prompt(request)
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{self._base_url}/images/generations",
                headers={"Authorization": f"Bearer {self._api_key}"},
                json={
                    "model": self._model,
                    "prompt": prompt,
                    "n": request.num_images,
                    "size": f"{request.width}x{request.height}",
                    "response_format": "b64_json",
                },
            )
            response.raise_for_status()
            data = response.json()

        results = []
        for item in data["data"]:
            image_bytes = base64.b64decode(item["b64_json"])
            results.append(GeneratedImage(
                data=image_bytes,
                width=request.width,
                height=request.height,
                provider="dall-e",
                metadata={"revised_prompt": item.get("revised_prompt", "")},
            ))
        return results

    def _build_sticker_prompt(self, request: GenerationRequest) -> str:
        style_modifiers = STYLE_PROMPT_MODIFIERS.get(request.style, "")
        return f"{request.prompt}. {style_modifiers}"

    async def check_health(self) -> bool:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                f"{self._base_url}/models",
                headers={"Authorization": f"Bearer {self._api_key}"},
            )
            return response.status_code == 200
```

**Stable Diffusion Adapter** (local or API-based):

```python
class StableDiffusionGenerator(ImageGenerator):
    """Adapter for Stable Diffusion (via local Automatic1111 or Stability AI API)."""

    def __init__(self, base_url: str, api_key: str | None = None) -> None:
        self._base_url = base_url.rstrip("/")
        self._api_key = api_key

    async def generate(self, request: GenerationRequest) -> list[GeneratedImage]:
        prompt = self._build_sticker_prompt(request)
        headers = {}
        if self._api_key:
            headers["Authorization"] = f"Bearer {self._api_key}"

        payload = {
            "prompt": prompt,
            "negative_prompt": request.negative_prompt or DEFAULT_NEGATIVE_PROMPT,
            "width": request.width,
            "height": request.height,
            "num_inference_steps": 30,
            "guidance_scale": 7.5,
            "batch_size": request.num_images,
        }
        if request.seed is not None:
            payload["seed"] = request.seed

        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"{self._base_url}/sdapi/v1/txt2img",
                headers=headers,
                json=payload,
            )
            response.raise_for_status()
            data = response.json()

        results = []
        for img_b64 in data["images"]:
            image_bytes = base64.b64decode(img_b64)
            results.append(GeneratedImage(
                data=image_bytes,
                width=request.width,
                height=request.height,
                provider="stable-diffusion",
                seed=data.get("parameters", {}).get("seed"),
            ))
        return results

    def _build_sticker_prompt(self, request: GenerationRequest) -> str:
        style_modifiers = STYLE_PROMPT_MODIFIERS.get(request.style, "")
        return f"{request.prompt}, {style_modifiers}"

    async def check_health(self) -> bool:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{self._base_url}/sdapi/v1/options")
            return response.status_code == 200

DEFAULT_NEGATIVE_PROMPT = (
    "blurry, low quality, watermark, signature, text, deformed, "
    "ugly, duplicate, morbid, mutilated, extra fingers, extra limbs"
)
```

**Style Prompt Modifiers**:

```python
STYLE_PROMPT_MODIFIERS: dict[str, str] = {
    "sticker": (
        "die-cut sticker design, white outline border, flat illustration style, "
        "vibrant colors, simple clean background, high contrast, vector art feel"
    ),
    "chibi": (
        "chibi anime style, cute proportions, large head small body, expressive eyes, "
        "kawaii aesthetic, pastel colors, clean linework, sticker-ready"
    ),
    "funko": (
        "Funko Pop vinyl figure style, large round head, small body, black bead eyes, "
        "no mouth or small simple mouth, glossy plastic look, collectible figure"
    ),
    "pixel-art": (
        "pixel art style, 32x32 grid snapped, limited color palette, retro game aesthetic, "
        "crisp pixel edges, no anti-aliasing, nostalgic 8-bit feel"
    ),
    "cartoon": (
        "cartoon illustration, bold outlines, cel-shaded, bright saturated colors, "
        "expressive character, clean vector style, animation-ready"
    ),
    "emoji": (
        "emoji style, simple geometric shapes, flat design, universal expression, "
        "circular framing, high readability at small sizes, bold colors"
    ),
    "watercolor": (
        "watercolor painting style, soft edges, translucent color washes, "
        "artistic texture, hand-painted feel, organic shapes"
    ),
}
```

**Prompt Engineering Tips for Sticker Generation**:

- Always include "sticker design" or "die-cut sticker" to signal the intended format
- Specify "transparent background" or "white background" explicitly for clean extraction
- Add "no text" to the negative prompt unless the sticker intentionally contains words
- Use "centered composition" to keep the subject within the sticker boundary
- For animated sequences, prompt for consistent character design across frames by specifying "character sheet" or "expression sheet" styles
- Include the target emotion or action clearly: "waving hello", "laughing", "thumbs up"

### Step 3: Python Pillow GIF Creation

Pillow provides full control over GIF assembly, including per-frame duration, palette optimization, transparency, and text overlays.

**Basic GIF Assembly**:

```python
from PIL import Image, ImageDraw, ImageFont, ImageSequence
from pathlib import Path
import io

def assemble_gif(
    frames: list[Image.Image],
    output_path: Path,
    duration_ms: int = 80,
    loop: int = 0,
    optimize: bool = True,
) -> Path:
    """Assemble a list of PIL Image frames into an animated GIF.

    Args:
        frames: List of PIL Image objects (same dimensions required).
        output_path: Where to save the GIF.
        duration_ms: Delay between frames in milliseconds.
        loop: Number of loops (0 = infinite).
        optimize: Enable palette optimization per frame.

    Returns:
        Path to the saved GIF.
    """
    if not frames:
        raise ValueError("At least one frame is required")

    # Ensure all frames match the first frame's dimensions
    target_size = frames[0].size
    processed = []
    for frame in frames:
        if frame.size != target_size:
            frame = frame.resize(target_size, Image.Resampling.LANCZOS)
        # Convert to palette mode for GIF compatibility
        if frame.mode != "P":
            frame = frame.convert("RGBA").convert("P", palette=Image.Palette.ADAPTIVE, colors=256)
        processed.append(frame)

    processed[0].save(
        output_path,
        save_all=True,
        append_images=processed[1:],
        duration=duration_ms,
        loop=loop,
        optimize=optimize,
    )
    return output_path
```

**Transparent GIF with Alpha Channel**:

```python
def assemble_transparent_gif(
    frames: list[Image.Image],
    output_path: Path,
    duration_ms: int = 80,
    loop: int = 0,
    transparency_color: tuple[int, int, int] = (0, 255, 0),
) -> Path:
    """Assemble a GIF with transparency support.

    GIF transparency works by designating one palette color as transparent.
    This function composites RGBA frames onto a solid color background,
    then marks that color as transparent in the palette.
    """
    processed = []
    for frame in frames:
        if frame.mode != "RGBA":
            frame = frame.convert("RGBA")

        # Create background with the transparency key color
        bg = Image.new("RGBA", frame.size, (*transparency_color, 255))
        composite = Image.alpha_composite(bg, frame)
        # Convert to palette mode
        p_frame = composite.convert("RGB").convert(
            "P", palette=Image.Palette.ADAPTIVE, colors=255,
        )
        processed.append(p_frame)

    # Find the palette index closest to our transparency color
    palette = processed[0].getpalette()
    transparency_index = _find_closest_palette_index(palette, transparency_color)

    processed[0].save(
        output_path,
        save_all=True,
        append_images=processed[1:],
        duration=duration_ms,
        loop=loop,
        transparency=transparency_index,
        disposal=2,  # Restore to background between frames
    )
    return output_path

def _find_closest_palette_index(
    palette: list[int], target: tuple[int, int, int],
) -> int:
    """Find the palette index whose RGB value is closest to target."""
    min_dist = float("inf")
    best_index = 0
    for i in range(0, len(palette), 3):
        r, g, b = palette[i], palette[i + 1], palette[i + 2]
        dist = (r - target[0]) ** 2 + (g - target[1]) ** 2 + (b - target[2]) ** 2
        if dist < min_dist:
            min_dist = dist
            best_index = i // 3
    return best_index
```

**Text Overlay on Frames**:

```python
def add_text_overlay(
    frame: Image.Image,
    text: str,
    position: str = "bottom",
    font_path: str | None = None,
    font_size: int = 24,
    text_color: tuple[int, int, int, int] = (255, 255, 255, 255),
    stroke_color: tuple[int, int, int, int] = (0, 0, 0, 255),
    stroke_width: int = 2,
    padding: int = 10,
) -> Image.Image:
    """Add a text caption to a frame with stroke outline for readability."""
    frame = frame.convert("RGBA")
    overlay = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    if font_path:
        font = ImageFont.truetype(font_path, font_size)
    else:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Calculate position
    x = (frame.width - text_width) // 2
    if position == "bottom":
        y = frame.height - text_height - padding
    elif position == "top":
        y = padding
    else:
        y = (frame.height - text_height) // 2

    draw.text(
        (x, y), text, font=font, fill=text_color,
        stroke_width=stroke_width, stroke_fill=stroke_color,
    )
    return Image.alpha_composite(frame, overlay)
```

**Global Palette for Consistent Colors Across Frames**:

```python
from PIL import Image
import numpy as np

def create_global_palette(frames: list[Image.Image], max_colors: int = 256) -> Image.Image:
    """Create a single optimized palette from all frames.

    Using a global palette prevents color flickering between frames
    that can occur when each frame has its own adaptive palette.
    """
    # Concatenate all frames into one tall image for palette computation
    total_height = sum(f.size[1] for f in frames)
    combined = Image.new("RGB", (frames[0].size[0], total_height))
    y_offset = 0
    for frame in frames:
        rgb = frame.convert("RGB")
        combined.paste(rgb, (0, y_offset))
        y_offset += rgb.size[1]

    # Quantize the combined image to get a global palette
    quantized = combined.quantize(colors=max_colors, method=Image.Quantize.MEDIANCUT)
    return quantized

def apply_global_palette(
    frames: list[Image.Image], palette_image: Image.Image,
) -> list[Image.Image]:
    """Apply a precomputed global palette to all frames."""
    result = []
    for frame in frames:
        rgb = frame.convert("RGB")
        quantized = rgb.quantize(palette=palette_image, dither=Image.Dither.FLOYDSTEINBERG)
        result.append(quantized)
    return result
```

### Step 4: ffmpeg Video-to-GIF Pipeline

ffmpeg produces higher quality GIFs from video sources than most other tools. The two-pass palette generation technique is essential for good results.

**Two-Pass Palette Generation** (the gold standard for ffmpeg GIF quality):

```bash
#!/usr/bin/env bash
set -euo pipefail

# Pass 1: Generate an optimized palette from the video content
ffmpeg -i input.mp4 \
    -vf "fps=15,scale=480:-1:flags=lanczos,palettegen=stats_mode=diff" \
    -y palette.png

# Pass 2: Use the palette to encode the GIF
ffmpeg -i input.mp4 -i palette.png \
    -lavfi "fps=15,scale=480:-1:flags=lanczos [x]; [x][1:v] paletteuse=dither=bayer:bayer_scale=5" \
    -y output.gif
```

**Python Wrapper for ffmpeg**:

```python
import subprocess
import shutil
from pathlib import Path

class FfmpegGifConverter:
    """Convert video files to optimized GIFs using ffmpeg two-pass encoding."""

    def __init__(self) -> None:
        if not shutil.which("ffmpeg"):
            raise RuntimeError("ffmpeg not found in PATH")

    def convert(
        self,
        input_path: Path,
        output_path: Path,
        fps: int = 15,
        width: int = 480,
        start_time: float | None = None,
        duration: float | None = None,
        dither: str = "bayer",
        bayer_scale: int = 5,
    ) -> Path:
        """Convert a video file to an optimized GIF.

        Args:
            input_path: Source video file.
            output_path: Destination GIF file.
            fps: Target frame rate.
            width: Target width (-1 preserves aspect ratio for height).
            start_time: Start offset in seconds (None = beginning).
            duration: Duration in seconds (None = full video).
            dither: Dithering algorithm (bayer, floyd_steinberg, sierra2).
            bayer_scale: Bayer dither scale (0-5, lower = more dithering).
        """
        palette_path = output_path.with_suffix(".palette.png")
        input_args = self._build_input_args(input_path, start_time, duration)
        filter_base = f"fps={fps},scale={width}:-1:flags=lanczos"

        try:
            # Pass 1: palette generation
            self._run_ffmpeg([
                *input_args,
                "-vf", f"{filter_base},palettegen=stats_mode=diff",
                "-y", str(palette_path),
            ])

            # Pass 2: GIF encoding with palette
            self._run_ffmpeg([
                *input_args,
                "-i", str(palette_path),
                "-lavfi", (
                    f"{filter_base} [x]; "
                    f"[x][1:v] paletteuse=dither={dither}:bayer_scale={bayer_scale}"
                ),
                "-y", str(output_path),
            ])
        finally:
            palette_path.unlink(missing_ok=True)

        return output_path

    def _build_input_args(
        self, input_path: Path, start_time: float | None, duration: float | None,
    ) -> list[str]:
        args = []
        if start_time is not None:
            args.extend(["-ss", str(start_time)])
        args.extend(["-i", str(input_path)])
        if duration is not None:
            args.extend(["-t", str(duration)])
        return args

    def _run_ffmpeg(self, args: list[str]) -> None:
        result = subprocess.run(
            ["ffmpeg", *args],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            raise RuntimeError(f"ffmpeg failed: {result.stderr[-500:]}")
```

**Common ffmpeg Filter Recipes**:

```bash
# Crop to square (center crop)
ffmpeg -i input.mp4 \
    -vf "crop=min(iw\,ih):min(iw\,ih)" \
    -y cropped.mp4

# Speed up 2x (for creating fast loops)
ffmpeg -i input.mp4 \
    -vf "setpts=0.5*PTS" \
    -y fast.mp4

# Reverse playback (for ping-pong loops)
ffmpeg -i input.mp4 \
    -vf "reverse" \
    -y reversed.mp4

# Concatenate forward + reverse for seamless loop
ffmpeg -i input.mp4 -i reversed.mp4 \
    -filter_complex "[0:v][1:v]concat=n=2:v=1:a=0" \
    -y pingpong.mp4

# Extract frames as PNGs for manual editing
ffmpeg -i input.mp4 \
    -vf "fps=10" \
    frames/frame_%04d.png

# Reassemble edited frames into GIF
ffmpeg -framerate 10 -i frames/frame_%04d.png \
    -vf "palettegen" -y palette.png
ffmpeg -framerate 10 -i frames/frame_%04d.png -i palette.png \
    -lavfi "paletteuse" -y output.gif
```

### Step 5: Animation Techniques

Create animations programmatically using sprite sheets, tweening, easing functions, and keyframe interpolation.

**Easing Functions**:

```python
import math

def ease_linear(t: float) -> float:
    return t

def ease_in_quad(t: float) -> float:
    return t * t

def ease_out_quad(t: float) -> float:
    return t * (2 - t)

def ease_in_out_quad(t: float) -> float:
    if t < 0.5:
        return 2 * t * t
    return -1 + (4 - 2 * t) * t

def ease_in_cubic(t: float) -> float:
    return t * t * t

def ease_out_cubic(t: float) -> float:
    return 1 - (1 - t) ** 3

def ease_out_bounce(t: float) -> float:
    if t < 1 / 2.75:
        return 7.5625 * t * t
    elif t < 2 / 2.75:
        t -= 1.5 / 2.75
        return 7.5625 * t * t + 0.75
    elif t < 2.5 / 2.75:
        t -= 2.25 / 2.75
        return 7.5625 * t * t + 0.9375
    else:
        t -= 2.625 / 2.75
        return 7.5625 * t * t + 0.984375

def ease_out_elastic(t: float) -> float:
    if t == 0 or t == 1:
        return t
    return 2 ** (-10 * t) * math.sin((t - 0.075) * (2 * math.pi) / 0.3) + 1

EASING_FUNCTIONS = {
    "linear": ease_linear,
    "ease-in": ease_in_quad,
    "ease-out": ease_out_quad,
    "ease-in-out": ease_in_out_quad,
    "ease-in-cubic": ease_in_cubic,
    "ease-out-cubic": ease_out_cubic,
    "bounce": ease_out_bounce,
    "elastic": ease_out_elastic,
}
```

**Keyframe Animation System**:

```python
from dataclasses import dataclass
from PIL import Image

@dataclass
class Keyframe:
    """A single keyframe defining a property value at a specific time."""
    time: float          # 0.0 to 1.0 (normalized)
    value: float
    easing: str = "linear"

@dataclass
class AnimationTrack:
    """A sequence of keyframes for one property (x, y, scale, rotation, opacity)."""
    property_name: str
    keyframes: list[Keyframe]

    def evaluate(self, t: float) -> float:
        """Interpolate the property value at normalized time t (0.0 to 1.0)."""
        if not self.keyframes:
            return 0.0
        if t <= self.keyframes[0].time:
            return self.keyframes[0].value
        if t >= self.keyframes[-1].time:
            return self.keyframes[-1].value

        # Find the surrounding keyframes
        for i in range(len(self.keyframes) - 1):
            k0 = self.keyframes[i]
            k1 = self.keyframes[i + 1]
            if k0.time <= t <= k1.time:
                local_t = (t - k0.time) / (k1.time - k0.time)
                easing_fn = EASING_FUNCTIONS.get(k0.easing, ease_linear)
                eased_t = easing_fn(local_t)
                return k0.value + (k1.value - k0.value) * eased_t

        return self.keyframes[-1].value

def render_animation(
    source: Image.Image,
    tracks: list[AnimationTrack],
    frame_count: int,
    canvas_size: tuple[int, int],
) -> list[Image.Image]:
    """Render an animation by evaluating tracks at each frame."""
    frames = []
    for i in range(frame_count):
        t = i / max(frame_count - 1, 1)
        props = {track.property_name: track.evaluate(t) for track in tracks}

        canvas = Image.new("RGBA", canvas_size, (0, 0, 0, 0))
        transformed = _apply_transform(
            source,
            x=props.get("x", 0),
            y=props.get("y", 0),
            scale=props.get("scale", 1.0),
            rotation=props.get("rotation", 0),
            opacity=props.get("opacity", 1.0),
        )
        # Center the transformed image on the canvas with offset
        paste_x = (canvas_size[0] - transformed.width) // 2 + int(props.get("x", 0))
        paste_y = (canvas_size[1] - transformed.height) // 2 + int(props.get("y", 0))
        canvas.paste(transformed, (paste_x, paste_y), transformed)
        frames.append(canvas)

    return frames

def _apply_transform(
    img: Image.Image,
    x: float = 0,
    y: float = 0,
    scale: float = 1.0,
    rotation: float = 0,
    opacity: float = 1.0,
) -> Image.Image:
    """Apply scale, rotation, and opacity transforms to an image."""
    if scale != 1.0:
        new_size = (int(img.width * scale), int(img.height * scale))
        img = img.resize(new_size, Image.Resampling.LANCZOS)
    if rotation != 0:
        img = img.rotate(-rotation, expand=True, resample=Image.Resampling.BICUBIC)
    if opacity < 1.0:
        img = img.convert("RGBA")
        r, g, b, a = img.split()
        a = a.point(lambda p: int(p * opacity))
        img = Image.merge("RGBA", (r, g, b, a))
    return img
```

**Common Animation Presets**:

```python
def bounce_animation(amplitude: float = 20, cycles: int = 2) -> list[AnimationTrack]:
    """Create a vertical bounce animation."""
    keyframes = []
    for i in range(cycles * 2 + 1):
        t = i / (cycles * 2)
        value = 0 if i % 2 == 0 else -amplitude
        keyframes.append(Keyframe(time=t, value=value, easing="ease-out"))
    return [AnimationTrack(property_name="y", keyframes=keyframes)]

def pulse_animation(min_scale: float = 0.9, max_scale: float = 1.1) -> list[AnimationTrack]:
    """Create a pulsing scale animation."""
    return [AnimationTrack(
        property_name="scale",
        keyframes=[
            Keyframe(time=0.0, value=1.0, easing="ease-in-out"),
            Keyframe(time=0.25, value=max_scale, easing="ease-in-out"),
            Keyframe(time=0.5, value=1.0, easing="ease-in-out"),
            Keyframe(time=0.75, value=min_scale, easing="ease-in-out"),
            Keyframe(time=1.0, value=1.0, easing="ease-in-out"),
        ],
    )]

def rotate_animation(degrees: float = 360) -> list[AnimationTrack]:
    """Create a full rotation animation."""
    return [AnimationTrack(
        property_name="rotation",
        keyframes=[
            Keyframe(time=0.0, value=0, easing="linear"),
            Keyframe(time=1.0, value=degrees, easing="linear"),
        ],
    )]

def shake_animation(intensity: float = 5, frequency: int = 8) -> list[AnimationTrack]:
    """Create a horizontal shake animation."""
    keyframes = [Keyframe(time=0.0, value=0, easing="linear")]
    for i in range(1, frequency + 1):
        t = i / (frequency + 1)
        direction = 1 if i % 2 == 0 else -1
        decay = 1 - (i / frequency)  # Decay over time
        keyframes.append(Keyframe(time=t, value=intensity * direction * decay, easing="linear"))
    keyframes.append(Keyframe(time=1.0, value=0, easing="linear"))
    return [AnimationTrack(property_name="x", keyframes=keyframes)]
```

**Sprite Sheet Slicer**:

```python
def slice_sprite_sheet(
    sheet: Image.Image,
    columns: int,
    rows: int,
    frame_count: int | None = None,
) -> list[Image.Image]:
    """Slice a sprite sheet into individual frames.

    Args:
        sheet: The full sprite sheet image.
        columns: Number of columns in the grid.
        rows: Number of rows in the grid.
        frame_count: Total frames to extract (None = all cells).
    """
    frame_width = sheet.width // columns
    frame_height = sheet.height // rows
    total = frame_count or (columns * rows)

    frames = []
    for i in range(total):
        col = i % columns
        row = i // columns
        if row >= rows:
            break
        box = (
            col * frame_width,
            row * frame_height,
            (col + 1) * frame_width,
            (row + 1) * frame_height,
        )
        frames.append(sheet.crop(box))
    return frames
```

### Step 6: Sticker-Specific Patterns

Stickers require specific visual treatments: transparent backgrounds, outline strokes, caption overlays, and precise sizing for each chat platform.

**Background Removal and Outline Stroke**:

```python
from PIL import Image, ImageFilter, ImageDraw

def add_sticker_outline(
    image: Image.Image,
    stroke_width: int = 4,
    stroke_color: tuple[int, int, int, int] = (255, 255, 255, 255),
) -> Image.Image:
    """Add a solid outline stroke around the non-transparent content.

    This creates the classic sticker "die-cut" appearance with a white
    border around the subject.
    """
    if image.mode != "RGBA":
        image = image.convert("RGBA")

    # Extract the alpha channel and create a dilated mask
    alpha = image.split()[3]
    # Dilate the alpha mask by the stroke width
    dilated = alpha.copy()
    for _ in range(stroke_width):
        dilated = dilated.filter(ImageFilter.MaxFilter(3))

    # Create the stroke layer
    stroke_layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
    stroke_pixels = stroke_layer.load()
    alpha_pixels = alpha.load()
    dilated_pixels = dilated.load()

    for y in range(image.height):
        for x in range(image.width):
            # Stroke region: dilated but not in original alpha
            if dilated_pixels[x, y] > 128 and alpha_pixels[x, y] < 128:
                stroke_pixels[x, y] = stroke_color

    # Composite: stroke behind, original on top
    result = Image.alpha_composite(stroke_layer, image)
    return result

def remove_background_simple(
    image: Image.Image,
    threshold: int = 240,
) -> Image.Image:
    """Remove near-white backgrounds by converting to transparency.

    For production use, prefer a dedicated background removal model
    (rembg, remove.bg API, or SAM-based segmentation).
    """
    if image.mode != "RGBA":
        image = image.convert("RGBA")

    pixels = image.load()
    for y in range(image.height):
        for x in range(image.width):
            r, g, b, a = pixels[x, y]
            if r > threshold and g > threshold and b > threshold:
                pixels[x, y] = (r, g, b, 0)
    return image
```

**Sticker Caption Overlay**:

```python
def create_sticker_with_caption(
    image: Image.Image,
    caption: str,
    font_path: str,
    font_size: int = 28,
    caption_height: int = 50,
    bg_color: tuple[int, int, int, int] = (0, 0, 0, 160),
    text_color: tuple[int, int, int, int] = (255, 255, 255, 255),
) -> Image.Image:
    """Add a semi-transparent caption bar at the bottom of a sticker."""
    # Expand canvas to accommodate caption
    new_height = image.height + caption_height
    canvas = Image.new("RGBA", (image.width, new_height), (0, 0, 0, 0))
    canvas.paste(image, (0, 0))

    # Draw caption background
    draw = ImageDraw.Draw(canvas)
    draw.rectangle(
        [(0, image.height), (image.width, new_height)],
        fill=bg_color,
    )

    # Draw caption text centered
    font = ImageFont.truetype(font_path, font_size)
    bbox = draw.textbbox((0, 0), caption, font=font)
    text_width = bbox[2] - bbox[0]
    text_x = (image.width - text_width) // 2
    text_y = image.height + (caption_height - font_size) // 2
    draw.text((text_x, text_y), caption, font=font, fill=text_color)

    return canvas
```

**Platform Export Functions**:

```python
from pathlib import Path

def export_for_telegram(
    frames: list[Image.Image],
    output_path: Path,
    duration_ms: int = 80,
) -> Path:
    """Export animated sticker for Telegram (512x512, WebM or GIF).

    Telegram animated stickers use WebM (VP9) or Lottie format.
    For GIF fallback, use standard GIF with 512x512 dimensions.
    """
    target_size = (512, 512)
    resized = [f.resize(target_size, Image.Resampling.LANCZOS) for f in frames]
    gif_path = output_path.with_suffix(".gif")
    assemble_transparent_gif(resized, gif_path, duration_ms=duration_ms)
    return gif_path

def export_for_discord(
    frames: list[Image.Image],
    output_path: Path,
    duration_ms: int = 80,
    max_size_kb: int = 256,
) -> Path:
    """Export animated emoji for Discord (128x128, under 256 KB)."""
    target_size = (128, 128)
    resized = [f.resize(target_size, Image.Resampling.LANCZOS) for f in frames]
    gif_path = output_path.with_suffix(".gif")
    assemble_gif(resized, gif_path, duration_ms=duration_ms)

    # Check size and reduce if needed
    file_size_kb = gif_path.stat().st_size / 1024
    if file_size_kb > max_size_kb:
        _reduce_gif_size(gif_path, max_size_kb)
    return gif_path

def export_for_slack(
    frames: list[Image.Image],
    output_path: Path,
    duration_ms: int = 80,
    max_size_kb: int = 128,
) -> Path:
    """Export custom emoji for Slack (128x128, under 128 KB)."""
    target_size = (128, 128)
    resized = [f.resize(target_size, Image.Resampling.LANCZOS) for f in frames]
    gif_path = output_path.with_suffix(".gif")
    assemble_gif(resized, gif_path, duration_ms=duration_ms)

    file_size_kb = gif_path.stat().st_size / 1024
    if file_size_kb > max_size_kb:
        _reduce_gif_size(gif_path, max_size_kb)
    return gif_path
```

### Step 7: Batch Processing and Optimization

Automate large-scale sticker generation with parallel processing, file size optimization, and output validation.

**Batch Generation Pipeline**:

```python
import asyncio
from dataclasses import dataclass
from pathlib import Path

@dataclass
class BatchItem:
    """A single item in a batch generation job."""
    name: str
    prompt: str
    style: str = "sticker"
    animation: str = "bounce"      # bounce, pulse, rotate, shake, none

@dataclass
class BatchResult:
    """Result for a single batch item."""
    name: str
    output_path: Path | None
    file_size_kb: float
    frame_count: int
    success: bool
    error: str | None = None

async def generate_sticker_batch(
    items: list[BatchItem],
    generator: ImageGenerator,
    config: PipelineConfig,
    max_concurrent: int = 4,
) -> list[BatchResult]:
    """Generate a batch of animated stickers with concurrency control."""
    semaphore = asyncio.Semaphore(max_concurrent)
    results = []

    async def process_item(item: BatchItem) -> BatchResult:
        async with semaphore:
            try:
                # Generate base image
                request = GenerationRequest(
                    prompt=item.prompt,
                    width=config.width,
                    height=config.height,
                    style=item.style,
                )
                images = await generator.generate(request)
                if not images:
                    return BatchResult(
                        name=item.name, output_path=None,
                        file_size_kb=0, frame_count=0,
                        success=False, error="No images generated",
                    )

                # Load the generated image
                base_image = Image.open(io.BytesIO(images[0].data)).convert("RGBA")

                # Apply animation
                animation_tracks = _get_animation_tracks(item.animation)
                frames = render_animation(
                    base_image, animation_tracks,
                    frame_count=config.frame_count,
                    canvas_size=(config.width, config.height),
                )

                # Add sticker outline
                frames = [add_sticker_outline(f) for f in frames]

                # Export
                output_path = config.output_dir / f"{item.name}.gif"
                assemble_transparent_gif(
                    frames, output_path,
                    duration_ms=config.frame_duration_ms,
                )

                # Optimize
                optimize_gif(output_path, config.max_file_size_kb)

                file_size_kb = output_path.stat().st_size / 1024
                return BatchResult(
                    name=item.name,
                    output_path=output_path,
                    file_size_kb=file_size_kb,
                    frame_count=len(frames),
                    success=True,
                )
            except Exception as e:
                return BatchResult(
                    name=item.name, output_path=None,
                    file_size_kb=0, frame_count=0,
                    success=False, error=str(e),
                )

    tasks = [process_item(item) for item in items]
    results = await asyncio.gather(*tasks)
    return list(results)

def _get_animation_tracks(animation_type: str) -> list[AnimationTrack]:
    presets = {
        "bounce": bounce_animation,
        "pulse": pulse_animation,
        "rotate": rotate_animation,
        "shake": shake_animation,
        "none": lambda: [],
    }
    factory = presets.get(animation_type, bounce_animation)
    return factory()
```

**GIF Size Optimization**:

```python
import subprocess
import shutil
from pathlib import Path
from PIL import Image

def optimize_gif(
    gif_path: Path,
    target_size_kb: int,
    min_colors: int = 32,
    min_fps: int = 8,
) -> Path:
    """Iteratively reduce GIF file size to meet target.

    Optimization strategies applied in order:
    1. Reduce color count (256 -> 128 -> 64 -> 32)
    2. Reduce frame rate (drop every other frame)
    3. Reduce dimensions (scale down 10% per iteration)
    4. Apply lossy compression with gifsicle (if available)
    """
    current_size = gif_path.stat().st_size / 1024
    if current_size <= target_size_kb:
        return gif_path

    # Strategy 1: Color reduction
    for colors in [128, 64, 32]:
        if colors < min_colors:
            break
        _reduce_colors(gif_path, colors)
        if gif_path.stat().st_size / 1024 <= target_size_kb:
            return gif_path

    # Strategy 2: Frame decimation (drop alternating frames)
    _decimate_frames(gif_path)
    if gif_path.stat().st_size / 1024 <= target_size_kb:
        return gif_path

    # Strategy 3: Lossy compression with gifsicle
    if shutil.which("gifsicle"):
        for lossy_level in [30, 60, 80, 100, 150, 200]:
            _gifsicle_optimize(gif_path, lossy_level)
            if gif_path.stat().st_size / 1024 <= target_size_kb:
                return gif_path

    # Strategy 4: Scale down
    for scale_pct in [90, 80, 70, 60, 50]:
        _scale_gif(gif_path, scale_pct / 100)
        if gif_path.stat().st_size / 1024 <= target_size_kb:
            return gif_path

    return gif_path

def _reduce_colors(gif_path: Path, max_colors: int) -> None:
    """Re-quantize a GIF to fewer colors."""
    img = Image.open(gif_path)
    frames = []
    durations = []
    for frame in ImageSequence.Iterator(img):
        durations.append(frame.info.get("duration", 80))
        rgb = frame.convert("RGB")
        quantized = rgb.quantize(colors=max_colors, method=Image.Quantize.MEDIANCUT)
        frames.append(quantized)

    frames[0].save(
        gif_path,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=img.info.get("loop", 0),
        optimize=True,
    )

def _decimate_frames(gif_path: Path) -> None:
    """Drop every other frame and double the duration of remaining frames."""
    img = Image.open(gif_path)
    frames = []
    durations = []
    for i, frame in enumerate(ImageSequence.Iterator(img)):
        if i % 2 == 0:
            durations.append(frame.info.get("duration", 80) * 2)
            frames.append(frame.copy())

    if len(frames) < 2:
        return

    frames[0].save(
        gif_path,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=img.info.get("loop", 0),
        optimize=True,
    )

def _gifsicle_optimize(gif_path: Path, lossy_level: int) -> None:
    """Apply lossy compression using gifsicle."""
    tmp_path = gif_path.with_suffix(".opt.gif")
    subprocess.run(
        ["gifsicle", "-O3", f"--lossy={lossy_level}", str(gif_path), "-o", str(tmp_path)],
        capture_output=True,
    )
    if tmp_path.exists() and tmp_path.stat().st_size < gif_path.stat().st_size:
        tmp_path.replace(gif_path)
    else:
        tmp_path.unlink(missing_ok=True)

def _scale_gif(gif_path: Path, scale: float) -> None:
    """Scale all frames down by the given factor."""
    img = Image.open(gif_path)
    new_size = (int(img.width * scale), int(img.height * scale))
    frames = []
    durations = []
    for frame in ImageSequence.Iterator(img):
        durations.append(frame.info.get("duration", 80))
        resized = frame.resize(new_size, Image.Resampling.LANCZOS)
        frames.append(resized)

    frames[0].save(
        gif_path,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=img.info.get("loop", 0),
        optimize=True,
    )
```

**Output Validation**:

```python
from dataclasses import dataclass
from pathlib import Path
from PIL import Image, ImageSequence

@dataclass
class ValidationResult:
    """Result of validating a generated GIF/sticker."""
    valid: bool
    file_size_kb: float
    dimensions: tuple[int, int]
    frame_count: int
    duration_ms: int
    errors: list[str]
    warnings: list[str]

def validate_output(
    gif_path: Path,
    platform: str = "telegram",
) -> ValidationResult:
    """Validate a generated GIF against platform requirements."""
    preset = PLATFORM_PRESETS.get(platform, PLATFORM_PRESETS["telegram"])
    errors: list[str] = []
    warnings: list[str] = []

    file_size_kb = gif_path.stat().st_size / 1024

    img = Image.open(gif_path)
    dimensions = img.size
    frame_count = 0
    total_duration_ms = 0
    for frame in ImageSequence.Iterator(img):
        frame_count += 1
        total_duration_ms += frame.info.get("duration", 80)

    # Check file size
    max_kb = preset["max_size_kb"]
    if file_size_kb > max_kb:
        errors.append(f"File size {file_size_kb:.1f} KB exceeds {platform} limit of {max_kb} KB")

    # Check dimensions
    expected = preset["dimensions"]
    if dimensions != expected:
        warnings.append(f"Dimensions {dimensions} differ from {platform} recommended {expected}")

    # Check duration
    max_duration_s = preset.get("max_duration_s")
    if max_duration_s and total_duration_ms / 1000 > max_duration_s:
        errors.append(f"Duration {total_duration_ms / 1000:.1f}s exceeds {platform} limit of {max_duration_s}s")

    # Check frame count (too few = choppy, too many = large file)
    if frame_count < 4:
        warnings.append(f"Only {frame_count} frames; animation may appear choppy")
    if frame_count > 100:
        warnings.append(f"{frame_count} frames is excessive; consider decimating")

    return ValidationResult(
        valid=len(errors) == 0,
        file_size_kb=file_size_kb,
        dimensions=dimensions,
        frame_count=frame_count,
        duration_ms=total_duration_ms,
        errors=errors,
        warnings=warnings,
    )
```

## Best Practices

- **Two-pass palette generation**: Always use ffmpeg's palettegen/paletteuse pipeline for video-to-GIF. Single-pass produces visibly worse color reproduction
- **Global palette for frame sequences**: When assembling GIFs from individually generated frames, compute a shared palette across all frames to prevent inter-frame color flickering
- **Transparency via disposal mode**: Set `disposal=2` (restore to background) when creating transparent GIFs; otherwise transparent regions accumulate artifacts from previous frames
- **Size budget first**: Know the platform's file size limit before generating. Working backward from 256 KB is easier than trying to compress a 2 MB GIF after the fact
- **Consistent character design**: When generating multiple frames with AI, include "character sheet" or "model sheet" in the prompt and use seeds or reference images to maintain visual consistency
- **Easing makes motion feel natural**: Never use linear interpolation for character animations. Ease-out for arrivals, ease-in for departures, ease-in-out for continuous loops
- **Test at actual display size**: Stickers that look good at 512x512 may lose important detail when displayed at 64x64 in a chat bubble
- **Looping matters**: Design animations to loop seamlessly. Use ping-pong (forward then reverse) for simple motions; match the first and last frame positions for complex animations
- **Batch with concurrency limits**: AI image generation APIs have rate limits. Use semaphores to control concurrent requests and implement exponential backoff for retries
- **Validate every output**: Automatically check file size, dimensions, frame count, and duration against platform requirements before delivering stickers

## Quality Checklist

- [ ] GIF file size is within the target platform's limit
- [ ] Dimensions match the platform's recommended size
- [ ] Animation loops smoothly without visible jumps
- [ ] Transparent background renders correctly (no green fringe or artifacts)
- [ ] Sticker outline is visible at the platform's display size
- [ ] Text captions are legible at the final display resolution
- [ ] Color palette is optimized (no unnecessary colors wasting bits)
- [ ] Frame rate produces smooth motion without bloating file size
- [ ] AI-generated frames maintain visual consistency across the animation
- [ ] Batch outputs are validated against platform requirements
- [ ] Easing functions are applied to movement animations
- [ ] Duration stays within platform time limits
- [ ] Output directory structure is organized for delivery

## Related Skills

- `creative-generation` - Image prompt engineering and creative ideation
- `python-expert` - Python patterns for image processing pipelines
- `containerization` - Dockerizing the pipeline with ffmpeg and system dependencies
- `async-patterns` - Concurrency patterns for batch AI generation
- `code-optimizer` - Performance optimization for frame processing

---

**Version**: 1.0.0
**Last Updated**: March 2026

### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets are not met, repeat the specific implementation steps with improved context.
