---
name: architecture-review
description: Revisar arquitectura sin tocar código, por foco [boundaries|data-flow|domain|concurrency], con findings por severidad; no valida un diseño nuevo (design-feature).
argument-hint: "[boundaries|data-flow|domain|concurrency]"
allowed-tools: Read, Grep, Glob, Agent, Bash(git diff *), Bash(git log *), Bash(git status *)
---

# architecture-review

Revisa el ámbito indicado en `$ARGUMENTS` (por defecto `boundaries`). Solo lectura: no modifica código ni docs.

## Cuándo usarla
- Tras implementar un lote o antes de cerrar un hito, para detectar deriva respecto a `docs/arquitectura.md` y `docs/DECISIONES.md`.
- Cambio de alto impacto (esquema Room, capas, servicio de ubicación, motor de notas): delegar la revisión en un revisor [opus] (cuenta 1 punto del presupuesto de subagentes).

## Cuándo NO usarla
- Diseñar lo que aún no existe → usa `design-feature`.
- Registrar una decisión → usa `registrar-decision`.
- Seguridad/permisos en profundidad → usa `security-review`.

## Precondiciones
- `$ARGUMENTS` es uno de los cuatro valores; si es otro o falta, usar `boundaries` y avisarlo.
- Leer `docs/arquitectura.md` (si existe), `docs/DECISIONES.md` y el hito activo. Acotar el diff (`git diff`, `git log`) o el módulo.

## Pasos
1. Delimitar el alcance: archivos/módulos del diff o los indicados. Si es de alto impacto, delegar con un brief ≤ 40 líneas (skill `delegate-task`) e integrar sus findings.
2. Aplicar el foco de `$ARGUMENTS`:

| Valor | Qué comprobar |
|---|---|
| `boundaries` | Dependencias entre `app/` y `motor/`; `motor/` sin dependencias Android; capas UI → dominio → datos (`DomainDependencyRuleTest`); ciclos; lógica de negocio en UI. |
| `data-flow` | Offline por defecto; Room como persistencia de usuario; mapas, grafo y elevación descargados y cacheados; red solo para mapas e incidencias; trazas y tramos solo en el dispositivo (sin backend). |
| `domain` | Modelos (traza, tramo, sector, nota, alerta, ruta); invariantes de notas, cronometraje y deltas en `motor/` y no en la UI; notas editadas siempre prevalecen sobre automáticas; nombres coherentes. |
| `concurrency` | Corrutinas y scopes, foreground service de ubicación, flujo de posiciones, TTS y ducking, transacciones Room, cancelación, muerte del proceso y pantalla apagada. |

3. Contrastar cada hallazgo con `docs/DECISIONES.md` (por sección). Una desviación no registrada es finding; si procede, sugerir `registrar-decision`.
4. Verificar con evidencia (`archivo:línea`); descartar lo que no se pueda demostrar. Lo no verificable → `VERIFICAR`.
5. Emitir la lista ordenada (CRITICO | ALTO | MEDIO | BAJO) como `SEVERIDAD | archivo:línea | problema | corrección propuesta`, y un veredicto (apto / apto con cambios / no apto).

## Validaciones / tests
- Cada finding tiene `archivo:línea` existente y corrección concreta.
- Sin findings: indicar qué se revisó y qué quedó fuera.
- `git status` sin cambios atribuibles a la revisión.

## Definition of Done
- [ ] Foco cubierto según la tabla; alcance declarado.
- [ ] Findings con formato `SEVERIDAD | archivo:línea | problema | corrección propuesta`.
- [ ] Contraste con `docs/DECISIONES.md` citado por sección.
- [ ] Ningún archivo modificado.
- [ ] Alto impacto: revisado por un revisor [opus].

## Docs a actualizar
- Ninguno por la revisión; `registrar-decision` si hay decisión pendiente · docs/ESTADO.md (skill `session-handoff`)
