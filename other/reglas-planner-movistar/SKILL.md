---
name: Reglas Transversales del Planner
key: reglas-planner-movistar
description: 20 reglas transversales (P01-P20) para el Planner. Checklist auditable de criterio estratégico aplicable a cualquier briefing.
version: 1.0.0
owner: client
status: active
---

# Reglas Transversales del Planner

Cargada por el Planner/Planner. El Campaign Manager la usa en Cierre para auditar que las reglas se han respetado.

Cada regla tiene un ID, una descripción y la acción que el Planner debe tomar. Si una regla se activa, el Planner lo registra en su output como flag con el ID correspondiente.

---

## Checklist

| ID | Regla | Acción |
|---|---|---|
| P01 | El briefing mezcla más de un objetivo principal | Jerarquizar o pedir aclaración |
| P02 | No hay idea dominante | Proponer una |
| P03 | Un canal solicitado no tiene rol diferencial | Recomendar eliminar o redefinir |
| P04 | Todos los canales repiten el mismo mensaje | Proponer arquitectura por roles |
| P05 | Un soporte intrusivo se usa para mensaje tactico menor | Desaconsejar |
| P06 | El precio domina en fases altas o medias del funnel | Corregir hacia beneficio / valor |
| P07 | La personalización resulta invasiva | Corregir tono y segmentación |
| P08 | No hay frecuencia definida | Alertar |
| P09 | Se usa Movistar+ como inventario publicitario genérico | Corregir rol |
| P10 | Se usa tienda como folleto fisico | Corregir mision de soporte |
| P11 | Se usa CRM como contenedor de inputs comerciales | Reducir y jerarquizar |
| P12 | Se usa digital como volumen barato | Reorientar a precision |
| P13 | Performance degrada códigos de marca | Corregir |
| P14 | El briefing no conecta con territorio Movistar | Alertar |
| P15 | Falta puente entre canales (no hay secuencia de journey) | Proponer secuencia |
| P16 | El canal contradice el momento mental del cliente | Recomendar alternativa |
| P17 | Un mecanismo comercial se convierte en idea principal sin justificación | Corregir |
| P18 | Falta CTA principal | Proponer uno |
| P19 | La campaña no diferencia cliente de prospect | Alertar |
| P20 | El briefing pide "todos los medios" sin jerarquía | Replantear arquitectura |

---

## Como aplicar

1. El Planner pasa este checklist después de diagnosticar el briefing y antes de cerrar su output.
2. Para cada regla activada, incluye un flag en su JSON: `{"regla": "P03", "descripción": "Canal X no tiene rol diferencial", "accion_tomada": "Eliminado de la arquitectura"}`.
3. Las reglas no activadas no se mencionan (no rellenar con "OK" -- solo las que aplican).
4. El Campaign Manager verifica en Cierre que las reglas evidentes se han aplicado. Si el briefing pedia "todos los medios" y el Planner no activo P20, es un flag del Campaign Manager.

---

## Priorización de territorios

Cuando el briefing incluye más de 10 territorios, el Planner agrupa en bloques antes de asignar canales:

| Bloque | Criterio |
|---|---|
| P1 (Prioridad 1) | Mayor impacto comercial + urgencia temporal |
| P2 (Prioridad 2) | Alta relevancia estratégica, menor urgencia |
| Apoyo tactico | Refuerzo o estacional |
| Revisar/limitar | Baja prioridad o riesgo de saturación |

Orden recomendado dentro de cada bloque: paraguas > comerciales > entretenimiento > conectividad.

El Campaign Manager verifica en Cierre que la priorización es coherente con el briefing y que no se ha omitido un territorio P1.

---

## Criterio de severidad

- **Bloqueante**: P01 (objetivos multiples sin jerarquizar), P02 (sin idea dominante), P05 (intrusivo para tactico menor). Si no se resuelven, el Creative Copywriter no puede trabajar con coherencia.
- **Alta**: P03, P04, P06, P09, P10, P11, P17. Degradan calidad pero el flujo puede continuar con flag.
- **Media**: el resto. Son mejoras de precision que el Planner propone y el humano decide.
