---
name: validate-content-toolkit
description: Revisión local y de solo lectura del Content Skills Toolkit. Usar cuando se modifiquen runners, SKILL.md, catálogos, contratos JSON, pruebas, el CLI o documentación del repositorio.
---

# Validar Content Skills Toolkit

## Objetivo

Revisar únicamente los archivos modificados y sus contratos relacionados. La skill no hace commit, push, publicación, despliegue, instalación de conectores ni llamadas a servicios externos.

## Procedimiento

1. Inspeccionar `git status --short` y delimitar los archivos modificados.
2. Cargar el registro con `python3 -m toolkit list` sin ejecutar runners ni integraciones.
3. Para cada herramienta afectada, comparar `catalog.json`, carpeta, `SKILL.md`, `run.py`, `input.example.json`, `output.schema.json`, `resources/README.md` y `tests/test_smoke.py`.
4. Revisar que el documento declare el runner, el motor, las entradas, la salida, los guardrails y los límites reales.
5. Buscar claims no demostrados, secretos, credenciales, promesas de ejecución externa, referencias a rutas antiguas y métricas de popularidad.
6. Ejecutar solo validaciones locales relacionadas: pruebas, compilación, `python3 -m toolkit validate` y `git diff --check`.
7. Informar hallazgos con archivo, regla, evidencia y severidad. No modificar archivos automáticamente.

## Criterios

- El registro debe conservar 304 entradas y los conteos por fase.
- El slug, catálogo, carpeta, runner y documentación deben estar alineados.
- Los contratos JSON deben ser locales y reproducibles.
- Las integraciones deben permanecer diferidas y explícitas.
- Ningún documento debe incluir tokens, claves, contraseñas ni valores de credenciales.
- No presentar una plantilla, plan, consulta, render o publicación como una acción ya ejecutada.
- Mantener separadas las observaciones, los supuestos y las recomendaciones.

## Salida

Entregar un informe breve con `PASS`, `WARN` o `FAIL`, seguido de los archivos revisados, comandos ejecutados, hallazgos y pruebas pendientes. Si no hay problemas, declarar explícitamente que la revisión fue de solo lectura.
