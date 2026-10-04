---
name: git-workflow-pro
description: Esta guía de versionado de código proporciona estándares y listas de verificación para commits, ramificación, resolución de conflictos y procesos de lanzamiento. Al aplicar estrategias de commits atómicos y reglas de versionado semántico, ayuda a los desarrolladores a mantener una base de código organizada a través de flujos de trabajo paralelos y a producir registros de cambios bien estructurados para cualquier cambio de código.
---

# Git Workflow Pro

## Propósito
Esta guía de versionado de código proporciona estándares y listas de verificación para commits, ramificación, resolución de conflictos y procesos de lanzamiento. Al aplicar estrategias de commits atómicos y reglas de versionado semántico, ayuda a los desarrolladores a mantener una base de código organizada a través de flujos de trabajo paralelos y a producir registros de cambios bien estructurados para cualquier cambio de código.

## Flujo de trabajo
1. Definir objetivo, repositorio, runtime, restricciones y criterio de éxito.
2. Inspeccionar código, configuración, dependencias y pruebas sin modificar antes de proponer cambios.
3. Diseñar una modificación mínima, reproducible y reversible.
4. Implementar con pruebas primero cuando corresponda.
5. Ejecutar validaciones actualizadas y registrar limitaciones.

## Entradas aceptadas
- Solicitud, código, configuración, logs, especificaciones y archivos proporcionados por el usuario.
- Fuentes externas solo mediante integración explícita y autorizada.

## Salida esperada
Un plan o artefacto técnico revisable, con comandos, archivos afectados, pruebas y supuestos.

## Guardrails
- No ejecutar comandos destructivos, cambios de permisos, despliegues, commits, pushes ni acciones externas sin alcance explícito.
- No instalar dependencias ni consultar APIs sin informar el servicio, credencial, riesgos y alternativa local.
- No afirmar que una compilación, prueba o despliegue pasó sin ejecutarlo.

## Plantilla de solicitud
Objetivo: [resultado]
Repositorio o código: [ruta]
Runtime: [lenguaje y versión]
Restricciones: [límites]
Formato: [salida]

## Lista de control
- [ ] La entrada y el alcance están definidos.
- [ ] El plan no cambia archivos fuera de alcance.
- [ ] Las pruebas y comandos son reproducibles.
- [ ] Los riesgos y límites están documentados.

## Runner asociado

- **Runner:** `toolkit/phase-3-programming/git-workflow-pro/run.py`
- **Motor:** `toolkit/phase_3_engine.py`
- **Entrada de ejemplo:** `toolkit/phase-3-programming/git-workflow-pro/input.example.json`
- **Esquema de salida:** `toolkit/phase-3-programming/git-workflow-pro/output.schema.json`
- **Prueba smoke:** `toolkit/phase-3-programming/git-workflow-pro/tests/test_smoke.py`

La documentación debe mantenerse sincronizada con el runner, el catálogo de la fase y el contrato JSON. El runner local no debe interpretarse como una ejecución externa, publicación o despliegue.
