---
name: project-analysis
description: "Analiza proyectos, módulos o áreas funcionales frontend para detectar fortalezas, deuda técnica, inconsistencias y oportunidades de mejora con impacto real. Usa esta skill cuando el usuario pida una auditoría amplia del repo, de una feature, screen, flujo o carpeta; cuando quiera saber qué mejorar, qué riesgos existen o qué conviene priorizar antes de refactorizar."
---

# Project Analysis

## Propósito

Analizar un proyecto, módulo o flujo frontend con criterio técnico y devolver un diagnóstico útil, priorizado y accionable.

Esta skill no existe para enumerar buenas prácticas genéricas, sino para:

- entender cómo está construido el proyecto;
- detectar problemas reales y no solo preferencias de estilo;
- reconocer fortalezas que conviene conservar;
- encontrar oportunidades de mejora con impacto concreto;
- diferenciar deuda técnica importante de detalles menores;
- proponer un orden razonable de trabajo antes de refactorizar.

## Cuándo usarla

Usala cuando el usuario pida:

- analizar un proyecto completo;
- revisar un módulo, feature, screen, modal, carpeta o flujo;
- detectar mejoras posibles;
- evaluar arquitectura, organización o mantenibilidad;
- identificar deuda técnica;
- encontrar riesgos antes de refactorizar;
- priorizar mejoras en una base de código existente;
- comparar el estado actual contra una dirección técnica deseada.

También aplica a pedidos como:

- "¿Qué mejorarías de este proyecto?"
- "¿Qué está mal o puede escalar mal?"
- "¿Qué refactors valen la pena?"
- "¿Dónde ves sobreingeniería o deuda técnica?"
- "¿Qué priorizarías si tuvieras que mejorar este módulo?"

## Cuándo no usarla

No la uses si:

- el usuario pide implementar directamente una feature concreta;
- el pedido es un bug puntual y no requiere diagnóstico amplio;
- el usuario pide únicamente performance: en ese caso corresponde `performance-analysis`;
- el usuario pide dividir un trabajo ya entendido en entregas: corresponde `vertical-slice-planning`;
- el usuario pide crear o refactorizar una pieza de UI específica: corresponde `ui-component-architecture`;
- el usuario pide revisar services, contratos o backend de una integración puntual: corresponde `frontend-data-integration`.

Si durante el análisis detectás que una de esas skills aplica para profundizar un frente particular, señalalo explícitamente.

## Regla central

Analizá antes de juzgar.  
Basate en evidencia del repo.  
Priorizá por impacto.  
No propongas reescrituras totales por reflejo.

## Proceso

1. Definí el alcance real:
   - proyecto completo;
   - módulo;
   - screen/modal;
   - flujo;
   - carpeta o dominio.
2. Leé el contexto mínimo necesario para entender la estructura y el flujo.
3. Ampliá la exploración solo si cambia una conclusión de arquitectura, deuda o prioridad.
4. Identificá:
   - fortalezas;
   - problemas;
   - riesgos;
   - oportunidades.
5. Clasificá los hallazgos por prioridad:
   - alta;
   - media;
   - baja.
6. Proponé mejoras concretas:
   - qué cambiar;
   - por qué;
   - impacto;
   - esfuerzo estimado relativo.
7. Cerrá con un orden de mejora recomendado y lo que **no** conviene tocar todavía.

## Referencias a consultar según el caso

- Si el análisis es de arquitectura general, límites o estructura del repo, leé `references/architecture-and-boundaries.md`.
- Si el análisis es de un módulo, flujo, feature o screen concreta, leé `references/module-and-flow-audit.md`.
- Si necesitás detectar señales de deuda técnica, fragilidad o riesgo de evolución, leé `references/technical-debt-and-risk-signals.md`.
- Si el usuario pide priorizar mejoras, ordenar refactors o armar un roadmap técnico, leé `references/prioritization-and-roadmap.md`.
- Si necesitás elegir el formato de entrega más útil, leé `references/report-formats.md`.

## Criterios generales

- No marques como problema algo que:
  - funciona bien;
  - es consistente con el repo;
  - no genera costo actual ni futuro claro;
  - solo difiere de una preferencia personal.
- No uses frases vagas como:
  - "mejorar la arquitectura";
  - "modularizar";
  - "reducir complejidad";
  sin explicar **dónde**, **por qué** y **qué impacto genera**.
- Reconocé las decisiones bien resueltas.
- Si una zona está suficientemente bien para su complejidad actual, decilo.
- Evitá recomendar:
  - "migrar todo";
  - "reescribir desde cero";
  - "separar en microservicios";
  salvo que el repo y el pedido lo justifiquen claramente.
- Si una mejora requiere intervención amplia, sugerí `vertical-slice-planning`.
- Si el análisis deriva en un refactor relevante de UI, sugerí `ui-component-architecture`.
- Si deriva en persistencia, contratos o services, sugerí `frontend-data-integration`.
- Si el problema exige medición concreta de rendimiento, sugerí `performance-analysis`.

## Severidad

Clasificá hallazgos así:

### Alta prioridad
Problemas que:
- generan bugs o retrabajo frecuente;
- bloquean escalabilidad;
- mezclan responsabilidades de forma peligrosa;
- vuelven costoso extender una feature;
- hacen probable romper contratos o flujos.

### Media prioridad
Problemas que:
- no rompen hoy, pero aumentan costo futuro;
- reducen claridad;
- fomentan duplicación;
- complican refactors;
- dificultan el uso consistente del repo.

### Baja prioridad
Mejoras:
- de naming puntual;
- de legibilidad menor;
- de consistencia;
- útiles pero no urgentes.

## Salida esperada

La respuesta debe dejar claro:

- qué parte del proyecto se analizó;
- qué fortalezas existen;
- qué problemas reales se detectaron;
- cuáles son prioritarios;
- qué mejoras convienen;
- qué **no** conviene tocar todavía;
- cuál sería el siguiente paso técnico más razonable.
