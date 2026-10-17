---
name: backend-audit
description: "Auditoría de backend y arquitectura con PRUEBAS: herramientas reales por stack, cada hallazgo con evidencia (salida, archivo:línea, test que falla), informe y plan de refactor seguro. Úsala para auditar, deuda técnica, legacy o antes de refactorizar."
---

# backend-audit (Senzu)

Diagnostica el backend como un médico: **primero las pruebas, después el diagnóstico**. No se
reporta nada que no se pueda demostrar. Esta skill ENCUENTRA; los arreglos viven donde ya estaban:
`code-quality` (recetas por tema), `ddd-hexagonal` (estructura) y `deploy-ops` (infraestructura).
Cada tipo de hallazgo del catálogo apunta a su receta: diagnóstico y tratamiento en armonía.

## Lectura mínima por tarea
| Tarea | Lee solo |
|---|---|
| Auditar el backend o un área (`/auditar`) | `references/protocolo.md` → luego las que indique |
| Qué herramientas usar en ESTE stack | `references/herramientas-por-stack.md` §el stack del proyecto |
| Qué buscar, qué evidencia exige cada cosa y qué receta lo arregla | `references/catalogo-hallazgos.md` |
| Escribir el informe | `references/informe.md` (plantilla de informe y de hallazgo) |
| Refactorizar sin romper nada (`/refactor`) | `references/refactor-seguro.md` |
| Reglas de arquitectura que se comprueban solas | `references/reglas-arquitectura.md` |
| Dónde se concentra el riesgo (código que cambia mucho y es complejo) | `scripts/hotspots.mjs` |

## Reglas duras
1. **Sin prueba no hay hallazgo.** Cada hallazgo lleva al menos una evidencia verificable: salida
   de una herramienta, `archivo:línea` con el fragmento, un **test que falla** y lo reproduce, o una
   medición. "Parece que", "podría" o "huele a" sin evidencia van a una lista aparte de sospechas.
2. **Herramientas antes que lectura.** Primero se ejecuta lo que mide (análisis estático, auditoría de
   dependencias, reglas de capas, cobertura, hotspots); después se lee el código señalado. Leer 200
   archivos "a ver qué veo" no es una auditoría.
3. **Verifica cada hallazgo antes de reportarlo**: abre el código, confirma que no es un falso
   positivo de la herramienta y anota el nivel de confianza (confirmado o probable).
4. **La versión real manda** (`code-quality/references/stack-versions.md`): lo que está bien en Laravel 13 puede no
   existir en 10. No reportes como fallo lo que la versión del proyecto no permite.
5. **Las convenciones del proyecto no son hallazgos.** Si `senzu/conventions.md` fija algo, respetarlo no es
   deuda técnica, aunque no sea tu preferencia.
6. **Solo lectura.** La auditoría no cambia código (solo crea el informe y, si hace falta, tests de
   reproducción en una rama). Los arreglos van al plan y se hacen con `/refactor` o `/siguiente`.
7. **Prioriza por riesgo real**: gravedad × probabilidad × superficie (hotspots). Un fallo de seguridad
   en un endpoint público va antes que 40 funciones largas en un script que nadie toca.
8. Herramientas que falten en el proyecto: proponlas, pero **no las instales sin preguntar** (son
   dependencias nuevas). Si no se instalan, dilo en el informe como límite de la auditoría.

## Salida
- `senzu/auditoria/<AAAA-MM-DD>-<area>.md`: resumen ejecutivo, mapa de riesgo, hallazgos con evidencia,
  sospechas sin confirmar, límites de la auditoría y plan propuesto.
- Tarjetas en `senzu/plan/PLAN.md` (skill `project-planner`) para lo que el usuario apruebe arreglar.
- Entrada en `senzu/devlog/` con el resumen y las herramientas ejecutadas.

## Relación con otras skills
- Arreglar un hallazgo → la receta que indica el catálogo (`code-quality`, `ddd-hexagonal`, `deploy-ops`).
- Seguridad a fondo → `code-quality/references/security-owasp.md`.
- Estilo propio del proyecto → `/adoptar` (y sus reglas de arquitectura, `references/reglas-arquitectura.md`).
