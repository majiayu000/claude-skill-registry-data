---
name: substance-3d-texturing
description: "Texturizado PBR con Adobe Substance 3D Painter y exportación web: presets metallic/roughness, glTF, Three.js, Babylon.js, ORM packing, API Python de Painter. No para cargar/modelar en el motor (threejs-webgl, blender-web-pipeline)."
---

# substance-3d-texturing (índice Senzu, ES)

Documentación completa upstream (inglés): `SKILL.upstream.md` (506 líneas). **No la leas entera**: usa el mapa y lee solo la sección que necesites (Read con offset/limit o Grep).

## Cuándo usar / cuándo NO
- Usar: exportar texturas PBR (baseColor, normal, metallicRoughness, AO) desde Substance Painter para Three.js, Babylon.js o glTF.
- Usar: automatizar exportaciones con la API Python de Painter (batch, resolución por asset, presets personalizados, plugin al guardar).
- Usar: reducir peso de texturas para web/móvil (canales ORM, JPEG para baseColor, presupuesto de memoria).
- NO usar: modelado, LOD o exportación de mallas → blender-web-pipeline; materiales y carga en el motor → threejs-webgl / react-three-fiber / babylonjs-engine.

## Lectura mínima por tarea
| Tarea | Lee solo |
|---|---|
| Empezar un proyecto/starter | `SKILL.upstream.md` L58-93 (§1. Basic Web Export) + `assets/export_templates/` |
| Exportación por lotes con Python | L95-166 (§2-3) + `scripts/batch_export.py` + `references/python_api_reference.md` |
| Preset personalizado / canales ORM | L168-216 (§4) + L396-416 (§Channel Packing) + `scripts/generate_export_preset.py` |
| Usar texturas en R3F, Babylon o glTF | L314-376 (§Integration Patterns) |
| Depurar / rendimiento | L377-428 (§Performance Optimization) + L429-488 (§Common Pitfalls) + `scripts/web_optimizer.py` |

## Mapa de `SKILL.upstream.md`
| Líneas | Sección | Para qué |
|---|---|---|
| 8-17 | Overview | Alcance: autoría PBR, export web, automatización Python |
| 18-55 | Core Concepts | Canales PBR metallic/roughness, presets integrados, resoluciones recomendadas |
| 58-94 | 1. Basic Web Export (Three.js/Babylon.js) | Export manual y `MeshStandardMaterial` con los mapas |
| 95-142 | 2. Batch Export with Python API | `export_project_textures` con config JSON para todos los texture sets |
| 143-167 | 3. Resolution Override per Asset | `sizeLog2` distinto por texture set mediante `filter` |
| 168-217 | 4. Custom Export Preset (Separate Channels) | Definir `exportPresets` con mapas y canales propios |
| 218-244 | 5. Mobile-Optimized Export | JPEG en baseColor, PNG en mapas de datos, 512 px |
| 245-279 | 6. glTF/GLB Integration | Config para glTF 2.0 y referencia en el JSON del material |
| 280-313 | 7. Event-Driven Export Plugin | Auto-export al guardar con `event.DISPATCHER` |
| 314-376 | Integration Patterns | `useTexture` en R3F, `PBRMaterial` en Babylon, pipeline glTF + Draco |
| 377-428 | Performance Optimization | Presupuesto de memoria, compresión, empaquetado ORM, mipmaps |
| 429-488 | Common Pitfalls | Espacio de color, normales Y+/Y-, orden de canales, padding, AO con uv2 |
| 489-506 | Resources / Related Skills | Índice de recursos y skills relacionadas |

## Recursos
- `references/python_api_reference.md` — API Python completa de Substance Painter (export, textureset, resource, event).
- `references/export_presets.md` — catálogo de presets integrados y personalizados.
- `references/pbr_channel_guide.md` — significado y rangos de cada canal PBR.
- `scripts/batch_export.py` — exporta todos los texture sets con preset PBR Metallic Roughness; se ejecuta DENTRO de Painter (File → Python → Execute Script o como plugin).
- `scripts/generate_export_preset.py` — genera JSON de preset personalizado: `py -3 scripts/generate_export_preset.py` (interactivo o con flags; `python3` en Linux/macOS).
- `scripts/web_optimizer.py` — redimensiona y convierte texturas exportadas (baseColor a JPEG, informe de ahorro): `py -3 scripts/web_optimizer.py --help`.
- `assets/export_templates/` — presets JSON listos: `gltf_standard`, `threejs_optimized`, `babylonjs_pbr`, `web_orm_packed`, `mobile_webgl`.

## Reglas duras
- Por defecto 1024×1024 para web; 2048 solo en assets hero; nunca 4K en web. Presupuesto: ~100-150 MB desktop, ~30-50 MB móvil.
- Siempre `paddingAlgorithm: "infinite"` para evitar líneas en las costuras UV.
- baseColor en sRGB (`texture.colorSpace = THREE.SRGBColorSpace`); mapas de datos (normal, metallic, roughness) en PNG sin pérdida y en espacio lineal.
- Orden de canales glTF: G = roughness, B = metallic (R libre o AO en ORM). Normales en formato OpenGL (Y+), igual que glTF.
- AO en Three.js requiere `uv2`; en Babylon activa `useAmbientOcclusionFromMetallicTextureRed`.

## Integración con el stack del proyecto
- Detecta el stack como indica la skill `front-activation`/`skill-router` (senzu/senzu.json → package.json). Esta skill es agnóstica del framework (produce archivos de textura); el consumo depende del motor: React → react-three-fiber (`useTexture`), vanilla/Vue/Astro → threejs-webgl o babylonjs-engine.
