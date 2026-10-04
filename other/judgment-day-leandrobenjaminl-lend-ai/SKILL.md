---
name: judgment-day
description: >
  Revisión adversarial: dos jueces ciegos analizan el mismo código desde
  perspectivas opuestas para encontrar fallos antes de producción.
  Trigger: "judgment day", "doble review", "juzgar", "que lo juzguen".
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "2.0"
  model_tier: T4-reasoning
---

# Skill: judgment-day

Dos jueces ciegos. Tu código contra la pared.

## Trigger

- Terminaste una implementación y decís "listo"
- Antes de un merge importante a main
- El código toca lógica crítica (pagos, seguridad, datos sensibles)
- Querés una segunda opinión antes de deployar

## Workflow LEND

1. ANALIZAR
   ├── ¿Qué cambió? archivos, lógica, dependencias
   ├── Riesgo: ¿afecta seguridad, datos, performance?
   └── Scope: ¿cuántas líneas? ¿cuántos archivos?

2. OFRECER (Menú del Senior)
   ├── A) Juez 1 (El Pesimista) — SRE/Security: busca fallos de seguridad, bottlenecks, qué pasa si explota
   ├── B) Juez 2 (El Purista) — Clean Code: violaciones SOLID, código repetido, nombres horribles
   └── C) Full Judgment — ambos jueces + veredicto final con acciones concretas

3. ELEGIR → confirmación

4. HACER
   ├── Juez 1: analiza errores, manejo de excepciones, seguridad, performance
   ├── Juez 2: analiza legibilidad, estructura, patrones, deuda técnica
   ├── Sintetizar hallazgos en orden de severidad: crítico → mayor → menor
   ├── Ofrecer 3 salidas: refactor total, parche crítico, o asumir deuda
   └── Documentar veredicto y guardar en engram

5. VERIFICAR
   ├── Los hallazgos críticos tienen acción correctiva
   └── El autor entendió por qué cada hallazgo es importante
