---
name: mobile
description: "Mobile optimization — tile-based GPU, ASTC textures, draw call budget (<100), thermal throttling, battery, touch input, safe areas, App Store guidelines."
alwaysApply: true
globs: ["**/*.cs"]
---

# Mobile Optimization

## GPU Architecture

Mobile GPUs use **tile-based rendering** (TBDR). Key implications:
- Overdraw is expensive — minimize transparent layers
- Alpha-tested geometry is costly (breaks early-Z)
- Keep fragment shader complexity low
- Avoid full-screen post-processing when possible

## Performance Budgets

| Metric | Low-End | Mid-Range | High-End |
|--------|---------|-----------|----------|
| Draw calls | < 50 | < 100 | < 200 |
| Triangles | < 50k | < 100k | < 200k |
| Frame time | 33ms (30fps) | 16.6ms (60fps) | 16.6ms |
| Texture memory | < 100MB | < 150MB | < 256MB |
| Total memory | < 300MB | < 500MB | < 800MB |
| Build size | < 100MB | < 200MB | < 500MB |

## Texture Compression

- **ASTC** — use on both iOS and Android (best quality/size ratio)
- Max sizes: 512 for UI elements, 1024 for props, 2048 for hero characters
- Enable mipmaps for 3D objects, disable for UI sprites
- Use texture atlases to reduce draw calls

## Draw Call Reduction

1. **SRP Batcher** — enabled by default in URP, ensure shader compatibility
2. **GPU Instancing** — for repeated objects (trees, rocks, enemies)
3. **Static Batching** — for non-moving environment
4. **Texture Atlasing** — combine sprite sheets
5. **Material sharing** — same material = same batch

## Shader Complexity

- Limit math operations per fragment
- Avoid dependent texture reads
- Use `half` precision where possible (color, UV, normals)
- No real-time shadows on low-end (baked only)
- Avoid post-processing stack on low-end (or use simpler alternatives)

## Thermal Throttling

```csharp
// Adaptive Performance package
using UnityEngine.AdaptivePerformance;

private void Update()
{
    IAdaptivePerformance ap = Holder.Instance;
    if (ap != null && ap.ThermalStatus.ThermalMetrics.WarningLevel > WarningLevel.NoWarning)
    {
        // Reduce quality: lower resolution, reduce particles, cap framerate
        QualitySettings.resolutionScalingFixedDPIFactor = 0.75f;
    }
}
```

- Target 30fps for casual games (saves battery)
- Offer 60fps as opt-in option
- Reduce GPU load when battery < 20%
- Monitor thermal state and downscale dynamically

## Touch Input

```csharp
// Input System touch
[SerializeField] private float _swipeThreshold = 50f;

// Minimum tap target: 44x44 points (Apple HIG)
// Minimum tap target: 48x48 dp (Material Design)
```

- Tap: primary touch press+release < 0.3s
- Swipe: delta > threshold in one direction
- Pinch: two-finger distance change
- Long press: hold > 0.5s
- Drag: press + move

## Safe Area

```csharp
private void ApplySafeArea()
{
    Rect safeArea = Screen.safeArea;
    Vector2 anchorMin = safeArea.position;
    Vector2 anchorMax = safeArea.position + safeArea.size;

    anchorMin.x /= Screen.width;
    anchorMin.y /= Screen.height;
    anchorMax.x /= Screen.width;
    anchorMax.y /= Screen.height;

    RectTransform rect = GetComponent<RectTransform>();
    rect.anchorMin = anchorMin;
    rect.anchorMax = anchorMax;
}
```

Apply to the root UI panel to respect notches and rounded corners.

## Audio Compression

| Type | Format | Quality | Load Type |
|------|--------|---------|-----------|
| Music | Vorbis | 40-60% | Streaming |
| SFX (short) | ADPCM | — | Decompress On Load |
| SFX (long) | Vorbis | 70% | Compressed In Memory |
| UI clicks | PCM | — | Decompress On Load |

## Build Size

- Strip unused code (IL2CPP stripping: High)
- Compress textures aggressively
- Use Addressables for optional/DLC content
- Remove unused packages from manifest
- Target < 100MB for initial download (App Store recommendation)
