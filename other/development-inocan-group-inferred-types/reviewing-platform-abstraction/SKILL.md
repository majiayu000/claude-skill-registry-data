---
name: reviewing-platform-abstraction
description: Validates platform abstraction compliance - ensures rendering code uses IRendererAPI interfaces, no direct OpenGL in engine core, proper namespace isolation. Reviews graphics features and guides alternative backend implementation.
---

# Reviewing Platform Abstraction

## Table of Contents
- [Core Principle](#core-principle)
- [Quick Reference](#quick-reference)
- [Architecture Overview](#architecture-overview)
- [When to Use This Skill](#when-to-use-this-skill)
- [Review Checklist](#review-checklist)
- [Key Violations to Check](#key-violations-to-check)
- [Abstraction Interfaces](#abstraction-interfaces)
- [Platform Code Locations](#platform-code-locations)
- [Adding New Rendering Backend](#adding-new-rendering-backend)
- [Validating Abstraction Compliance](#validating-abstraction-compliance)
- [Review Output Format](#review-output-format)

## Core Principle
**All platform-specific code must live in `Engine/Platform/{PlatformName}/`**

## Quick Reference

**✅ Engine code should:**
- Use `IRendererAPI`, `IShader`, `ITexture2D` interfaces
- Inject dependencies via constructors
- Never import `Silk.NET.*` namespaces
- Never instantiate platform types directly

**✅ Platform code should:**
- Live in `Engine/Platform/SilkNet/`
- Implement abstraction interfaces
- Use `SilkNetContext.GL` for OpenGL
- Call `GLDebug.CheckError()` after GL calls

**❌ Never:**
- Import `Silk.NET.OpenGL` in Engine namespace
- Use concrete types like `SilkNetShader` in engine code
- Put OpenGL code outside Platform/SilkNet
- Add graphics features without interface abstraction

## Architecture Overview
```
Engine Core (Platform-Agnostic)
    ↓ Uses interfaces only
Abstraction Layer (IRendererAPI, IShader, ITexture2D, etc.)
    ↓ Implemented by
Platform Implementation (Engine/Platform/SilkNet/)
```

**Current**: OpenGL via Silk.NET
**Future**: Vulkan, DirectX, Metal, WebGL

## When to Use This Skill

Invoke this skill when:
- **Reviewing rendering/graphics PRs** - Check for platform abstraction violations before merge
- **Adding new graphics features** - Ensure compute shaders, geometry shaders, or advanced rendering features use proper abstraction
- **Investigating rendering bugs** - Determine if issues are platform-specific due to leaky abstractions
- **Architecture audits** - Validate that engine core remains platform-agnostic
- **Refactoring graphics code** - Ensure changes maintain abstraction boundaries
- **Planning new rendering backend** - Understand requirements for adding Vulkan, DirectX, Metal, or WebGL support

## Review Checklist

Run these commands to detect violations automatically:

### 1. Check for direct Silk.NET imports in engine code
```bash
grep -r "using Silk\.NET\." Engine/ --exclude-dir=Platform
```
**Expected**: No matches outside `Engine/Platform/`

### 2. Find concrete platform types in engine code
```bash
grep -rE "SilkNet[A-Z]" Engine/ --exclude-dir=Platform | grep -E "(private|public|protected)"
```
**Expected**: No `SilkNetShader`, `SilkNetTexture2D`, etc. in engine code

### 3. Verify interface usage in core rendering
Check `Engine/Renderer/Graphics2D.cs` and `Engine/Renderer/Graphics3D.cs`:
- All fields use interface types (`IRendererAPI`, `IShader`, `ITexture2D`, etc.)
- No direct GL calls or OpenGL imports

### 4. Validate new graphics features
For any new rendering features, verify:
- Interface exists in `Engine/Renderer/` or `Engine/Core/`?
- Implementation in `Engine/Platform/SilkNet/`?
- Factory registered in `Program.cs` DI container?

## Key Violations to Check

| Violation Type | ❌ Wrong | ✅ Correct |
|----------------|----------|------------|
| **Direct OpenGL** | `using Silk.NET.OpenGL;`<br>`GL.DrawElements(...)` | `private readonly IRendererAPI _api;`<br>`_api.DrawIndexed(...)` |
| **Concrete Types** | `private SilkNetShader _shader;`<br>`_shader = new SilkNetShader(path);` | `private readonly IShader _shader;`<br>`_shader = factory.Create(path);` |
| **Wrong Namespace** | `Engine/Renderer/OpenGLBuffer.cs`<br>`namespace Engine.Renderer;` | `Engine/Platform/SilkNet/Buffers/`<br>`namespace Engine.Platform.SilkNet.Buffers;` |

### Detailed Example: Adding New Graphics Features

When adding graphics features (compute shaders, geometry shaders, etc.), always create interface first:
```csharp
// 1. Interface in Engine/Renderer/
public interface IComputeShader : IDisposable {
    void Dispatch(uint x, uint y, uint z);
}

// 2. Implementation in Engine/Platform/SilkNet/
public class SilkNetComputeShader : IComputeShader { ... }

// 3. Factory for creation
public interface IComputeShaderFactory {
    IComputeShader Create(string path);
}

// 4. Engine uses interface
public ParticleSystem(IComputeShaderFactory factory) {
    _compute = factory.Create("particles.comp");
}
```

## Abstraction Interfaces

**Core Interfaces** (must use in engine code):
- `IRendererAPI` - Draw commands, clear, viewport
- `IShader` - Shader programs
- `ITexture2D` - Texture resources
- `IVertexArray` - Vertex array objects
- `IFrameBuffer` - Render targets
- `IVertexBuffer`, `IIndexBuffer` - Vertex/index data

**Platform Implementations** (only in Platform/SilkNet):
- All live in `Engine/Platform/SilkNet/`
- Use `SilkNetContext.GL` for OpenGL access
- Call `GLDebug.CheckError()` after GL calls

## Platform Code Locations
```
Engine/Platform/SilkNet/
├── SilkNetRendererApi.cs      # IRendererAPI
├── SilkNetShader.cs           # IShader
├── SilkNetTexture2D.cs        # ITexture2D
├── SilkNetVertexArray.cs      # IVertexArray
├── Buffers/
│   ├── SilkNetFrameBuffer.cs
│   ├── SilkNetVertexBuffer.cs
│   └── SilkNetIndexBuffer.cs
├── Audio/
│   └── SilkNetAudioEngine.cs  # OpenAL
└── Input/
    └── SilkNetInputSystem.cs
```

## Adding New Rendering Backend

**1. Create namespace:** `Engine/Platform/Vulkan/`

**2. Implement interfaces:**
```csharp
public class VulkanRendererApi : IRendererAPI { ... }
public class VulkanShader : IShader { ... }
// etc.
```

**3. Update DI registration:**
```csharp
// Program.cs
switch (backend) {
    case "OpenGL":
        container.Register<IRendererAPI, SilkNetRendererApi>();
        break;
    case "Vulkan":
        container.Register<IRendererAPI, VulkanRendererApi>();
        break;
}
```

**4. No engine code changes needed** - already uses interfaces!

## Validating Abstraction Compliance

After fixing violations or adding new features, validate compliance:

### 1. Build Test
```bash
dotnet build
```
**Expected**: Build succeeds without errors

### 2. Automated Violation Check
Run grep commands from [Review Checklist](#review-checklist)
**Expected**: No Silk.NET imports or concrete types in engine code

### 3. Smoke Test
```bash
cd Editor && dotnet run
```
**Expected**: Editor launches, rendering works correctly

### 4. Future-Proof Test
Ask: "Could I swap `SilkNetRendererApi` for `VulkanRendererApi` without changing engine code?"
**Expected**: Yes - all engine code uses `IRendererAPI` interfaces

## Review Output Format

**Issue**: [Violation description]
**Location**: [File:Line]
**Type**: [Direct OpenGL / Concrete Type / Wrong Namespace / Missing Interface]
**Fix**:
```csharp
// Current (wrong)
[bad code]

// Should be (correct)
[fixed code]
```
**Priority**: [Critical/High/Medium/Low]
