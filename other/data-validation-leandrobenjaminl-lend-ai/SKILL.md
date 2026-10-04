---
name: data-validation
description: >
  Validación de esquemas y calidad de datos — pandera, great expectations,
  contratos de datos. Garantizá que los datos cumplen lo esperado.
  Trigger: Cuando necesitás validar esquemas de datos, garantizar calidad, o definir contratos de datos.
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "3.0"
  model_tier: T2-fast
---

# Skill: data-validation

Validación de datos. Si entra basura, sale basura — pero no si la frenás antes.

## Trigger

- Llegan datos de una fuente externa y necesitás verificar que estén bien
- Definiste un esquema y querés asegurarte de que se cumple
- Un pipeline de producción necesita garantías de calidad
- Querés documentar qué esperás de cada columna

## Workflow LEND

```
1. ANALIZAR
   ├── Origen: ¿API, CSV, DB, usuario? ¿confiable?
   ├── Tipo de validación: ¿esquema (tipos), rango (valores), integridad (unicidad)?
   ├── ¿Qué pasa si falla? ¿rechazar, alertar, imputar?
   └── Frecuencia: ¿one-shot o pipeline recurrente?

2. OFRECER (Menú del Senior)
   ├── A) Pandera — esquemas en Python, integración con Pandas, lightweight
   ├── B) Great Expectations — suites de expectativas, documentación, UI
   └── C) Manual + asserts — validación ad-hoc con condiciones if/assert

3. ELEGIR → confirmación

4. HACER
   ├── Pandera: definir DataFrameModel con tipos, rangos, nulos permitidos
   ├── Great Expectations: crear expectation suite con expect_column_values_to_be_between, etc.
   ├── Manual: asserts + logging con mensajes claros
   ├── Documentar qué campos son requeridos, opcionales, y sus constraints
   └── Si falla: decidir comportamiento (detener pipeline, alertar, imputar)

5. VERIFICAR
   ├── El esquema pasa con datos válidos
   ├── El esquema falla con datos inválidos (probado)
   └── El mensaje de error es claro sobre qué falló y dónde
```

## Patrones

- **Validar temprano**: en cuanto los datos entran al pipeline, no después de transformarlos
- **Contrato de datos**: documentar qué espera cada etapa del pipeline
- **Pandera para DataFrames**: validación tipada con integración Pandas nativa
- **Great Expectations para producción**: suites compartibles, data docs, alertas

## Anti-patrones

- ❌ Validar después de transformar — perdés la traza del error original
- ❌ Mensajes de error genéricos — "validation failed" no ayuda a nadie
- ❌ No documentar el esquema — "esto funciona" no es documentación
- ❌ Validar todo como required cuando hay campos opcionales
