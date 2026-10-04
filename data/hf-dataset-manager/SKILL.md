---
name: hf-dataset-manager
description: Este kit de herramientas oficial de Hugging Face ayuda a los profesionales del aprendizaje automático a crear y gestionar conjuntos de datos mediante configuraciones personalizadas y consultas SQL. Proporciona un flujo de trabajo fiable y estandarizado para manejar estructuras de datos complejas, lo que permite a los equipos procesar y preparar de forma eficiente conjuntos de datos de alta calidad para el entrenamiento y la evaluación de modelos.
---

# HF Dataset Manager

## Propósito
Este kit de herramientas oficial de Hugging Face ayuda a los profesionales del aprendizaje automático a crear y gestionar conjuntos de datos mediante configuraciones personalizadas y consultas SQL. Proporciona un flujo de trabajo fiable y estandarizado para manejar estructuras de datos complejas, lo que permite a los equipos procesar y preparar de forma eficiente conjuntos de datos de alta calidad para el entrenamiento y la evaluación de modelos.

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

- **Runner:** `toolkit/phase-3-programming/hf-dataset-manager/run.py`
- **Motor:** `toolkit/phase_3_engine.py`
- **Entrada de ejemplo:** `toolkit/phase-3-programming/hf-dataset-manager/input.example.json`
- **Esquema de salida:** `toolkit/phase-3-programming/hf-dataset-manager/output.schema.json`
- **Prueba smoke:** `toolkit/phase-3-programming/hf-dataset-manager/tests/test_smoke.py`

La documentación debe mantenerse sincronizada con el runner, el catálogo de la fase y el contrato JSON. El runner local no debe interpretarse como una ejecución externa, publicación o despliegue.
