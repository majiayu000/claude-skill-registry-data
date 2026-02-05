---
name: wgpu-shader-specialist
description: Expert on wgpu GPU rendering, WGSL shaders, and GPU pipeline configuration. Use when discussing rendering, shaders, GPU, textures, or graphics pipeline.
---

# wgpu Shader Specialist

Expert skill for wgpu-based GPU rendering and WGSL shader development.

## When to Use

Activate this skill when the user:
- Discusses GPU rendering or graphics
- Writes or debugs WGSL shaders
- Configures render pipelines
- Works with textures or buffers
- Optimizes GPU performance

## wgpu Architecture

### Core Concepts
```
Instance → Adapter → Device → Queue
                          ↓
              RenderPipeline ← BindGroupLayout
                          ↓
              CommandEncoder → RenderPass → Submit
```

### FLUI's wgpu Usage
- Backend: wgpu 25.x (stay on 25.x - 26.0+ has issues)
- Features: Vulkan/Metal/DX12/WebGPU
- Text: glyphon for GPU text
- Paths: lyon for tessellation

## WGSL Shader Patterns

### Vertex Shader
```wgsl
struct VertexInput {
    @location(0) position: vec3<f32>,
    @location(1) tex_coords: vec2<f32>,
}

struct VertexOutput {
    @builtin(position) clip_position: vec4<f32>,
    @location(0) tex_coords: vec2<f32>,
}

@vertex
fn vs_main(in: VertexInput) -> VertexOutput {
    var out: VertexOutput;
    out.clip_position = vec4<f32>(in.position, 1.0);
    out.tex_coords = in.tex_coords;
    return out;
}
```

### Fragment Shader
```wgsl
@group(0) @binding(0)
var t_diffuse: texture_2d<f32>;
@group(0) @binding(1)
var s_diffuse: sampler;

@fragment
fn fs_main(in: VertexOutput) -> @location(0) vec4<f32> {
    return textureSample(t_diffuse, s_diffuse, in.tex_coords);
}
```

### Uniform Buffer
```wgsl
struct Uniforms {
    transform: mat4x4<f32>,
    color: vec4<f32>,
}

@group(0) @binding(0)
var<uniform> uniforms: Uniforms;
```

## Common Patterns

### Render Pipeline Creation
```rust
let pipeline = device.create_render_pipeline(&wgpu::RenderPipelineDescriptor {
    label: Some("Render Pipeline"),
    layout: Some(&pipeline_layout),
    vertex: wgpu::VertexState {
        module: &shader,
        entry_point: Some("vs_main"),
        buffers: &[vertex_buffer_layout],
        compilation_options: Default::default(),
    },
    fragment: Some(wgpu::FragmentState {
        module: &shader,
        entry_point: Some("fs_main"),
        targets: &[Some(wgpu::ColorTargetState {
            format: surface_format,
            blend: Some(wgpu::BlendState::ALPHA_BLENDING),
            write_mask: wgpu::ColorWrites::ALL,
        })],
        compilation_options: Default::default(),
    }),
    primitive: wgpu::PrimitiveState::default(),
    depth_stencil: None,
    multisample: wgpu::MultisampleState::default(),
    multiview: None,
    cache: None,
});
```

### Buffer Updates
```rust
// Staging buffer pattern for frequent updates
queue.write_buffer(&uniform_buffer, 0, bytemuck::bytes_of(&uniforms));
```

## GPU Debugging

### Validation Errors
```rust
// Enable validation in development
let instance = wgpu::Instance::new(&wgpu::InstanceDescriptor {
    backends: wgpu::Backends::all(),
    flags: wgpu::InstanceFlags::validation(),
    ..Default::default()
});
```

### Performance Tips
1. **Batch draw calls**: Minimize pipeline switches
2. **Instanced rendering**: For repeated geometry
3. **Texture atlases**: Reduce bind group changes
4. **Buffer pooling**: Reuse buffers instead of recreating

### Common Issues
- **Validation error**: Check bind group compatibility
- **Black screen**: Verify clip space coordinates (-1 to 1)
- **Texture sampling**: Check texture format compatibility
- **Alignment**: WGSL requires 16-byte alignment for uniforms

## FLUI-Specific Considerations

### Layer Composition
- Use separate render passes for overlay layers
- Implement scissor rects for clipping
- Consider texture caching for complex shapes

### Text Rendering
```rust
// glyphon integration
let mut text_renderer = TextRenderer::new(
    &device,
    &queue,
    swash_cache,
    Some(surface_format),
);
```

### Performance Monitoring
- Track GPU buffer allocations
- Monitor texture memory usage
- Profile shader execution time
