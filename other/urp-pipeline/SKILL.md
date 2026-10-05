---
name: urp-pipeline
description: "Universal Render Pipeline — URP asset configuration, renderer features, 2D renderer, lighting, shadows, post-processing volumes, SRP Batcher."
globs: ["**/URP*.asset", "**/*Renderer*.asset", "**/*Volume*.cs"]
---

# Universal Render Pipeline (URP)

## URP Pipeline Asset Configuration

The URP Pipeline Asset controls global rendering settings. Create via Assets > Create > Rendering > URP Asset (with Universal Renderer).

### Key Pipeline Asset Settings

| Setting | Recommended | Notes |
|---------|-------------|-------|
| HDR | Enabled | Required for Bloom and color grading |
| Anti-Aliasing | MSAA 4x or FXAA | MSAA on mobile, FXAA on desktop |
| Shadow Resolution | 2048 (desktop) / 1024 (mobile) | Balance quality vs performance |
| Shadow Cascade Count | 4 (desktop) / 2 (mobile) | More cascades = better shadow distribution |
| Shadow Distance | 50-150 | Depends on game scale |
| SRP Batcher | Enabled | Major draw call optimization |
| Dynamic Batching | Disabled when SRP Batcher is on | They conflict; SRP Batcher is superior |

### Configuring Pipeline Asset via Script

```csharp
using UnityEngine;
using UnityEngine.Rendering.Universal;

public class URPQualityManager : MonoBehaviour
{
    [SerializeField] private UniversalRenderPipelineAsset[] qualityLevels;

    public void SetQualityLevel(int level)
    {
        if (level >= 0 && level < qualityLevels.Length)
        {
            QualitySettings.renderPipeline = qualityLevels[level];
        }
    }

    public void AdjustShadowDistance(float distance)
    {
        var urpAsset = (UniversalRenderPipelineAsset)QualitySettings.renderPipeline;
        urpAsset.shadowDistance = distance;
    }
}
```

## Renderer Features (Custom Render Passes)

Renderer Features let you inject custom rendering logic into URP's render pipeline.

### Creating a Custom Renderer Feature

```csharp
using UnityEngine;
using UnityEngine.Rendering;
using UnityEngine.Rendering.Universal;

public class OutlineRendererFeature : ScriptableRendererFeature
{
    [System.Serializable]
    public class OutlineSettings
    {
        public RenderPassEvent renderPassEvent = RenderPassEvent.AfterRenderingOpaques;
        public Material outlineMaterial;
        public LayerMask layerMask;
        [Range(1, 4)] public int downSample = 1;
    }

    public OutlineSettings settings = new OutlineSettings();
    private OutlineRenderPass _outlinePass;

    public override void Create()
    {
        _outlinePass = new OutlineRenderPass(settings);
        _outlinePass.renderPassEvent = settings.renderPassEvent;
    }

    public override void AddRenderPasses(ScriptableRenderer renderer, ref RenderingData renderingData)
    {
        if (settings.outlineMaterial == null) return;
        renderer.EnqueuePass(_outlinePass);
    }
}
```

### Custom Render Pass

```csharp
using UnityEngine.Rendering;
using UnityEngine.Rendering.Universal;

public class OutlineRenderPass : ScriptableRenderPass
{
    private readonly OutlineRendererFeature.OutlineSettings _settings;
    private RTHandle _tempTexture;

    public OutlineRenderPass(OutlineRendererFeature.OutlineSettings settings)
    {
        _settings = settings;
        profilingSampler = new ProfilingSampler("OutlinePass");
    }

    public override void OnCameraSetup(CommandBuffer cmd, ref RenderingData renderingData)
    {
        var desc = renderingData.cameraData.cameraTargetDescriptor;
        desc.depthBufferBits = 0;
        RenderingUtils.ReAllocateIfNeeded(ref _tempTexture, desc, name: "_TempOutline");
    }

    public override void Execute(ScriptableRenderContext context, ref RenderingData renderingData)
    {
        CommandBuffer cmd = CommandBufferPool.Get();
        using (new ProfilingScope(cmd, profilingSampler))
        {
            var source = renderingData.cameraData.renderer.cameraColorTargetHandle;
            Blitter.BlitCameraTexture(cmd, source, _tempTexture, _settings.outlineMaterial, 0);
            Blitter.BlitCameraTexture(cmd, _tempTexture, source);
        }
        context.ExecuteCommandBuffer(cmd);
        CommandBufferPool.Release(cmd);
    }

    public override void OnCameraCleanup(CommandBuffer cmd)
    {
        _tempTexture?.Release();
    }
}
```

## Forward vs Forward+ Renderer

- **Forward**: Traditional forward rendering. Good for mobile, limited additional lights per object.
- **Forward+**: Uses clustered lighting. Removes per-object light limit. Better for scenes with many lights. Requires Unity 2022.2+.

Set in the Universal Renderer Data asset under Rendering Path.

## 2D Renderer Setup

For 2D games, use the 2D Renderer:

1. Create URP Asset with 2D Renderer (Assets > Create > Rendering > URP Asset with 2D Renderer)
2. 2D Renderer supports: Light2D, ShadowCaster2D, Sprite-Lit-Default shader
3. Use Light2D components: Global, Freeform, Sprite, Point, Spot

```csharp
using UnityEngine;
using UnityEngine.Rendering.Universal;

public class DynamicLight2DController : MonoBehaviour
{
    private Light2D _light2D;

    private void Awake()
    {
        _light2D = GetComponent<Light2D>();
    }

    public void SetIntensity(float intensity)
    {
        _light2D.intensity = intensity;
    }

    public void FlickerLight(float minIntensity, float maxIntensity)
    {
        _light2D.intensity = Random.Range(minIntensity, maxIntensity);
    }
}
```

## URP Lighting Configuration

### Main Light (Directional)

- Shadow type: Soft Shadows for quality, Hard for performance
- Shadow resolution: Set per-light or globally in Pipeline Asset
- Shadow bias: Normal Bias 0.4, Depth Bias 1.0 (starting values)

### Additional Lights

- Per-object limit in Pipeline Asset (default 4 for Forward)
- Forward+ removes this limit via clustered lighting
- Shadow support for additional lights must be enabled in Pipeline Asset

### Shadow Settings

```
Pipeline Asset:
  Shadow Distance: 100
  Cascade Count: 4
  Cascade Ratios: 0.067, 0.2, 0.467 (default)
  Depth Bias: 1
  Normal Bias: 1
  Soft Shadows: Enabled
```

## Post-Processing (Volume Framework)

URP uses the Volume framework for post-processing. No separate post-processing package needed.

### Setting Up Post-Processing

1. Enable Post Processing on the Camera component
2. Create a Global Volume (or local with collider)
3. Add Volume overrides (Bloom, Color Grading, etc.)

### Common Volume Profile Script

```csharp
using UnityEngine;
using UnityEngine.Rendering;
using UnityEngine.Rendering.Universal;

public class PostProcessController : MonoBehaviour
{
    [SerializeField] private Volume globalVolume;

    private Bloom _bloom;
    private ColorAdjustments _colorAdjustments;
    private Vignette _vignette;
    private ChromaticAberration _chromaticAberration;

    private void Awake()
    {
        var profile = globalVolume.profile;
        profile.TryGet(out _bloom);
        profile.TryGet(out _colorAdjustments);
        profile.TryGet(out _vignette);
        profile.TryGet(out _chromaticAberration);
    }

    public void SetDamageEffect(float intensity)
    {
        if (_vignette != null)
        {
            _vignette.intensity.Override(Mathf.Lerp(0.2f, 0.6f, intensity));
            _vignette.color.Override(Color.Lerp(Color.black, Color.red, intensity));
        }

        if (_chromaticAberration != null)
        {
            _chromaticAberration.intensity.Override(intensity * 0.5f);
        }
    }

    public void SetBloomIntensity(float intensity)
    {
        if (_bloom != null)
        {
            _bloom.intensity.Override(intensity);
        }
    }

    public void SetExposure(float exposure)
    {
        if (_colorAdjustments != null)
        {
            _colorAdjustments.postExposure.Override(exposure);
        }
    }
}
```

### Tonemapping Modes

- **None**: Raw HDR values clamped. Not recommended.
- **Neutral**: Minimal color shift. Good default.
- **ACES**: Film-like look, saturated. Industry standard.

## SRP Batcher Compatibility

The SRP Batcher groups draw calls by shader variant. To make a shader compatible:

### Shader Must Use CBUFFER

```hlsl
CBUFFER_START(UnityPerMaterial)
    float4 _BaseColor;
    float _Smoothness;
    float4 _BaseMap_ST;
CBUFFER_END
```

**Rules for SRP Batcher compatibility:**
- All material properties must be in the `UnityPerMaterial` CBUFFER
- Built-in engine properties must be in `UnityPerDraw` CBUFFER
- MaterialPropertyBlock breaks batching (avoid in URP)

### Checking SRP Batcher Compatibility

Select any shader in the Inspector. The "SRP Batcher" field shows Compatible or Not Compatible with a reason.

## URP Shader Includes

```hlsl
// Core URP includes for custom shaders
#include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"
#include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Lighting.hlsl"
#include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Input.hlsl"
#include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Shadows.hlsl"
```

## Camera Stacking

Camera stacking renders multiple cameras in sequence (e.g., world camera + UI camera + minimap).

```csharp
using UnityEngine;
using UnityEngine.Rendering.Universal;

public class CameraStackManager : MonoBehaviour
{
    [SerializeField] private Camera baseCamera;
    [SerializeField] private Camera uiCamera;
    [SerializeField] private Camera minimapCamera;

    private void Awake()
    {
        var baseCameraData = baseCamera.GetUniversalAdditionalCameraData();
        baseCameraData.renderType = CameraRenderType.Base;

        var uiCameraData = uiCamera.GetUniversalAdditionalCameraData();
        uiCameraData.renderType = CameraRenderType.Overlay;

        var minimapData = minimapCamera.GetUniversalAdditionalCameraData();
        minimapData.renderType = CameraRenderType.Overlay;

        // Add overlay cameras to the stack
        baseCameraData.cameraStack.Add(uiCamera);
        baseCameraData.cameraStack.Add(minimapCamera);
    }
}
```

**Camera stacking rules:**
- Only one Base camera renders first
- Overlay cameras render on top in stack order
- Each overlay camera adds a full render pass (expensive)
- Use sparingly; prefer single camera with layers when possible

## Render Pass Events

When creating custom render passes, choose the appropriate injection point:

| Event | Use Case |
|-------|----------|
| BeforeRenderingShadows | Custom shadow passes |
| AfterRenderingShadows | Shadow post-processing |
| BeforeRenderingOpaques | Pre-opaque effects |
| AfterRenderingOpaques | Outlines, SSAO |
| BeforeRenderingTransparents | Effects behind transparents |
| AfterRenderingTransparents | Distortion effects |
| BeforeRenderingPostProcessing | Custom pre-post effects |
| AfterRenderingPostProcessing | Final overlays, UI effects |
| AfterRendering | Debug visualization |
