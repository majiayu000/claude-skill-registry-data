---
name: tdd-process
description: "Define y ejecuta un flujo TDD completo (Red-Green-Refactor) con brief técnico, casos de prueba, y checklist de revisión final. USE FOR: crear features con TDD, corregir bugs con pruebas primero, refactor seguro, validación de DoD y seguridad básica."
---

# TDD Process Skill

## Objetivo
Aplicar un proceso TDD repetible para desarrollar cambios de forma incremental, verificable y segura.

## Resultado Esperado
- Cambios funcionales implementados mediante ciclos Red-Green-Refactor.
- Pruebas automatizadas que capturan el comportamiento esperado y casos borde.
- Validación final con checklist técnico, de lógica y seguridad.

## Entradas Mínimas
- Objetivo de la tarea.
- Contexto funcional/técnico.
- Restricciones (stack, dependencias, tiempos, compatibilidad).
- Definición de terminado (DoD).

## Flujo Paso A Paso

### 1. Definir el brief técnico
Usar esta estructura:
- Título de la tarea.
- Contexto.
- Requerimientos técnicos.
- Restricciones.
- DoD.

Chequeo de salida:
- El objetivo está claro y sin ambigüedad.
- Hay límites explícitos de alcance.
- DoD es verificable.

### 2. Diseñar pruebas antes del código (RED)
- Definir el comportamiento esperado (happy path + casos borde).
- Escribir primero pruebas unitarias y, si aplica, de integración.
- Ejecutar pruebas y confirmar fallo inicial por ausencia de implementación.

Decisiones:
- Si el requerimiento involucra reglas aisladas: priorizar unit tests.
- Si involucra contratos entre componentes: agregar integration tests.

Chequeo de salida:
- Existe al menos una prueba fallando por cada comportamiento nuevo.
- El fallo describe claramente qué falta implementar.

### 3. Implementar mínimo código para pasar (GREEN)
- Implementar la solución más pequeña posible.
- Evitar optimizaciones prematuras.
- Ejecutar pruebas del alcance y llevarlas a verde.

Decisiones:
- Si pasan tests pero hay duplicación evidente: planear refactor inmediato.
- Si para pasar tests se rompe un contrato existente: ajustar diseño o tests.

Chequeo de salida:
- Todas las pruebas nuevas pasan.
- No hay regresiones en pruebas existentes críticas.

### 4. Refactorizar con red de seguridad (REFACTOR)
- Mejorar legibilidad, nombres, modularidad y duplicación.
- Mantener comportamiento sin cambios funcionales.
- Re-ejecutar suite de pruebas tras cada refactor relevante.

Chequeo de salida:
- Código más simple o mantenible que antes.
- Suite en verde después del refactor.

### 5. Validar con checklist de revisión
Revisar:
- Alucinaciones en librerías: nombres, métodos y versiones reales.
- Lógica de negocio: cumplimiento de reglas y casos borde.
- Seguridad: validación de inputs/outputs, datos sensibles y credenciales.
- Context window: no faltan restricciones ni criterios del brief.

Chequeo de salida:
- No hay hallazgos críticos abiertos.
- Riesgos residuales documentados.

### 6. Cierre
- Confirmar DoD completo.
- Documentar decisiones clave y trade-offs.
- Dejar próximos pasos si hay deuda técnica no bloqueante.

## Reglas de Calidad
- No escribir implementación antes de pruebas del comportamiento nuevo.
- No mezclar refactor con cambio funcional sin tests que protejan.
- No cerrar tarea sin validar DoD y checklist de revisión.

## Plantilla Rápida de Ejecución
1. Brief: objetivo, contexto, requerimientos, restricciones, DoD.
2. RED: escribir tests nuevos y verlos fallar.
3. GREEN: mínimo código para pasar.
4. REFACTOR: simplificar sin romper comportamiento.
5. REVIEW: checklist técnico/lógico/seguridad/contexto.
6. CIERRE: DoD cumplido y documentación mínima.
