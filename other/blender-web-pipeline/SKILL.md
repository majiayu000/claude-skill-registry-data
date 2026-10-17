---
name: blender-web-pipeline
description: "Exportar modelos Blender a glTF/GLB para web: bpy, Draco, decimación, baking, LODs, texturas, lotes por CLI (blender --background). No para renderizar 3D en navegador (threejs-webgl, babylonjs-engine) ni pintar PBR (substance-3d-texturing)."
---

# blender-web-pipeline (índice Senzu, ES)

Documentación completa upstream (inglés): `SKILL.upstream.md` (613 líneas). **No la leas entera**: usa el mapa y lee solo la sección que necesites (Read con offset/limit o Grep).

## Cuándo usar / cuándo NO
- Usar: exportar .blend a .glb con compresión Draco y texturas reducidas para Three.js, R3F, Babylon o PlayCanvas.
- Usar: automatizar con `blender --background --python`, procesar lotes, generar LODs, hornear (bake) materiales complejos.
- Usar: un .glb pesa demasiado, faltan texturas, la animación no se reproduce o los materiales se ven distintos en web.
- NO usar: cargar/renderizar el modelo en el navegador → threejs-webgl, react-three-fiber, babylonjs-engine, playcanvas-engine.
- NO usar: pintar texturas PBR → substance-3d-texturing; patrones de integración 3D en la web → web3d-integration-patterns.

## Lectura mínima por tarea
| Tarea | Lee solo |
|---|---|
| Empezar un proyecto/starter (primera exportación) | `SKILL.upstream.md` L80-110 (§1. Basic glTF Export) + L572-588 (§Export Settings) |
| Exportar por lotes / CLI | L112-168 (§2. Python Script for Batch Export) + L324-359 (§7. Command-Line Automation) o `scripts/batch_export.py` |
| Reducir peso (polígonos, texturas, LOD) | L170-195 (§3. Decimation), L253-322 (§5-6 LOD y compresión) + `references/optimization_strategies.md` |
| Cargar el .glb en Three/R3F/Babylon | L361-419 (§Integration Patterns) |
| Depurar / rendimiento | L489-551 (§Common Pitfalls) + L553-570 (§Pre-Export Checklist) |

## Mapa de `SKILL.upstream.md`
| Líneas | Sección | Para qué |
|---|---|---|
| 8-27 | Overview | Alcance y capacidades del pipeline |
| 28-77 | Core Concepts | glTF vs GLB, bases de `bpy`, métricas objetivo (<5 MB, <50k tris, 2048 px máx) |
| 78-359 | Common Patterns | Exportación básica, lote, decimación, baking, LODs, compresión de texturas, CLI |
| 197-251 | 4. Texture Baking for Web | Hornear materiales en una sola textura con Cycles |
| 361-419 | Integration Patterns | Carga con GLTFLoader+DRACOLoader, `useGLTF`, `SceneLoader.ImportMesh` |
| 421-487 | Optimization Techniques | Remove doubles, triangular, JPEG, atlas UV, Principled BSDF |
| 489-551 | Common Pitfalls | Archivos enormes, texturas ausentes, animaciones, materiales, exportación lenta, lag |
| 553-588 | Best Practices | Checklist pre-exportación y parámetros recomendados de `export_scene.gltf` |
| 590-613 | Resources / Related Skills | Índice de scripts, references y skills relacionadas |

## Recursos
- `references/gltf_export_guide.md` — Referencia completa de opciones de exportación glTF.
- `references/bpy_api_reference.md` — Chuleta de la API Python de Blender.
- `references/optimization_strategies.md` — Técnicas de optimización detalladas (geometría, texturas, materiales).
- `scripts/batch_export.py` — Exporta todos los .blend de una carpeta a .glb: `blender --background --python scripts/batch_export.py -- /entrada /salida`.
- `scripts/optimize_model.py` — Decima y reduce texturas de un modelo: `blender --background modelo.blend --python scripts/optimize_model.py`.
- `scripts/generate_lods.py` — Genera copias LOD0-2: `blender --background modelo.blend --python scripts/generate_lods.py`.
- `assets/README.md` — Solo descripción; el upstream cita `export_template.blend` y `shader_library/` pero NO existen en el paquete.

## Reglas duras
- Exporta siempre GLB binario con `export_apply=True` y Draco activado (nivel 6; 8 si prima el tamaño); objetivo <5 MB (ideal <1 MB) y <50k triángulos.
- Texturas máximo 2048 px (preferible 1024), JPEG con calidad 85 salvo que se necesite alpha; sin luces ni cámaras exportadas (recréalas en código).
- Solo materiales Principled BSDF con canales soportados (Base Color, Metallic, Roughness, Normal, Emission); los nodos personalizados no se exportan.
- Antes de exportar: aplicar modificadores y transformaciones, merge por distancia, limpiar datos huérfanos, animaciones en timeline con acciones asignadas.
- Si usas Draco, la web debe registrar el decodificador (`DRACOLoader.setDecoderPath`), o el modelo no cargará.

## Integración con el stack del proyecto
- Detecta el stack como indica la skill `front-activation`/`skill-router` (senzu/senzu.json → package.json). Esta skill se ejecuta fuera del front (Blender + Python); su salida .glb se consume desde threejs-webgl (vanilla/Vue/Astro), react-three-fiber (React) o babylonjs-engine. Coloca los .glb en `public/models/` y el decodificador Draco en `public/draco/`.
