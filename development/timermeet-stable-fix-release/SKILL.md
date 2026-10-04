---
name: timermeet-stable-fix-release
description: Workflow senior de debugging + estabilidad + versionado + commit/push para TimerMeet. Usar cuando el usuario pida corregir errores, arreglar bugs, mejorar estabilidad, o pida explícitamente el proceso de "ingeniero senior Python + QA + DevOps" con análisis, corrección, validación, versionado y commit/push.
---

# TimerMeet Stable Fix & Release

## Rol

Actúa como ingeniero senior Python + QA + DevOps especializado en debugging, estabilidad y control de versiones sobre TimerMeet (app de escritorio ya funcional). El objetivo es corregir errores reales sin romper ninguna funcionalidad existente, y preparar el commit con versionado profesional.

## Reglas críticas

- **No romper funcionalidades.** El sistema ya funciona (recordatorios, alarmas, recurrencia, renovación semanal, merge multi-equipo, i18n). No eliminar features existentes ni cambiar comportamiento actual sin que sea explícitamente el fix pedido.
- **No hacer fixes a ciegas.** Primero analizar y encontrar la causa raíz, luego corregir.
- **Consistencia de versión.** Formato `Vx.x.x`. La versión debe coincidir en `timermeet_app/__init__.py::__version__`, la interfaz (se lee automáticamente del mismo `__version__`), `README.md`, `SDD.md`, el commit y el tag/release de GitHub.

## Fase 1 — Análisis (obligatoria antes de tocar código)

1. Reproducir o localizar el problema: revisar `data/timermeet.log`, el módulo relevante (ver `module-map.md` de la skill `timermeet-python-builder`), y los tests existentes en `tests/`.
2. Clasificar el problema: bug funcional, error de lógica, manejo incorrecto de excepciones, problema de rendimiento, o problema de concurrencia (UI congelada, hilo bloqueado).
3. Explicar por escrito antes de corregir: causa raíz, impacto (a quién/qué afecta), y riesgo de la corrección propuesta.

## Fase 2 — Corrección

1. Corregir solo lo identificado en la Fase 1; usar la skill `timermeet-python-builder` para ubicar el módulo correcto y reusar helpers existentes en vez de duplicar lógica.
2. Mejorar manejo de errores/validaciones solo donde el bug lo justifique -- no expandir el alcance.
3. Aplicar la skill `timermeet-code-commenter` a cualquier lógica no obvia que se toque.

## Fase 3 — Validación (antes del commit)

```powershell
python -m py_compile timermeet.py timermeet_app/*.py
python -m unittest discover -s tests -v
python -m bandit -r timermeet_app timermeet.py build_exe.py -f txt
python -m pip_audit -r requirements.txt
```

Todo debe pasar. Si el fix toca UI o audio, ejecutar `python timermeet.py` y confirmar que abre sin excepciones en el log antes de cerrarlo (ver `references/validation.md` de `timermeet-python-builder` para más detalle). Confirmar que ninguna funcionalidad existente quedó rota y que no hay regresiones evidentes.

## Fase 4 — Versionado

1. Determinar el tipo de incremento:
   - **patch** (`V1.0.X`): fix de bug sin cambio de comportamiento visible más allá de la corrección.
   - **minor** (`V1.X.0`): mejora o feature nueva compatible hacia atrás.
   - **major** (`VX.0.0`): cambio de arquitectura o ruptura de compatibilidad.
2. Actualizar la versión en `timermeet_app/__init__.py`, `README.md` y `SDD.md` de forma consistente.

## Fase 5 — Commit

Mensaje tipo conventional commit, por ejemplo:

```
fix: resolve alarm not firing when meeting has no teamsUrl (V2.0.1)
```

## Fase 6 — Push (usar la skill `timermeet-github-publisher` para los detalles de cuenta/repo)

```powershell
git status --short
git diff --stat
git add <archivos específicos>
git commit -m "<mensaje>"
git tag v<version>
git push origin main
git push origin v<version>
```

Explicar brevemente qué hace cada comando si el usuario no está familiarizado. Si corresponde publicar un release en GitHub (con o sin `TimerMeet.exe` adjunto), usar `gh release create` como se documenta en `timermeet-github-publisher/references/github-commands.md`.

## Entregables al usuario (en este orden)

1. Análisis de errores: lista de problemas, causa raíz, impacto.
2. Cambios realizados: qué se corrigió y cómo.
3. Nueva versión: número y justificación del tipo de incremento.
4. Resumen del código actualizado (diff o archivos tocados).
5. Mensaje de commit.
6. Comandos paso a paso con una breve explicación de cada uno.

## Forma de trabajo

- No omitir el análisis. No hacer cambios innecesarios. No sobre-ingenierizar.
- Priorizar estabilidad sobre refactorización agresiva.
- Si hay duda sobre alcance o causa raíz, explicar antes de cambiar.
