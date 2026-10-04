---
name: data-verify
description: >
  Verificación de resultados antes de presentar — reproducibilidad,
  consistencia, y validación contra la pregunta original.
  Trigger: Cuando el análisis está terminado y necesitás revisarlo antes de presentarlo.
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "3.0"
  model_tier: T5-deep
---

# Skill: data-verify

Verificación final. Antes de presentar, asegurate de que no estás diciendo una mentira.

## Trigger

- Terminaste el análisis y estás por presentar
- Vas a hacer un commit con resultados
- Alguien más va a usar tus conclusiones para tomar decisiones
- El análisis tiene implicancias de negocio importantes

## Workflow LEND

```
1. ANALIZAR
   ├── ¿El análisis responde la pregunta original?
   ├── ¿Los datos son correctos? (verificar fuente, fechas, filtros)
   ├── ¿Las transformaciones son correctas? (re-ejecutar pipeline)
   └── ¿Las conclusiones están justificadas por los datos?

2. OFRECER (Menú del Senior)
   ├── A) Auto-verify — re-ejecutar pipeline de principio a fin, comparar resultados
   ├── B) Peer review — que otro agente (judgment-day) revise hallazgos y código
   └── C) Sanity checks — tests manuales: "esto tiene sentido?" con reglas de negocio

3. ELEGIR → confirmación

4. HACER
   ├── Re-ejecutar: correr el pipeline completo desde los datos crudos
   ├── Verificar: mismos datos crudos → mismos resultados (reproducibilidad)
   ├── Sanity checks: los números tienen sentido (no hay valores imposibles)
   ├── Cross-check: ¿las conclusiones cambian si cambia un parámetro? (sensibilidad)
   └── Documentar el proceso de verificación

5. VERIFICAR
   ├── El análisis es reproducible
   ├── Las conclusiones son robustas (no sensibles a pequeños cambios)
   └── Estaría dispuesto a defender estos resultados frente a un cliente
```

## Patrones

- **Reproducibilidad**: si no podés re-ejecutar y obtener lo mismo, no está verificado
- **Regla del titular**: si el resultado fuera un titular de diario, ¿lo publicarías?
- **Test de la abuela**: si se lo explicás a alguien no técnico, ¿lo entiende?
- **Sensibilidad**: ¿cómo cambian los resultados si sacás el 5% de los datos?

## Anti-patrones

- ❌ Presentar sin verificar — "funcionaba antes" no es verificación
- ❌ Confiar en un solo run — si no es reproducible, puede ser un accidente
- ❌ Ignorar resultados contra-intuitivos — si algo parece raro, investigá antes de presentar
- ❌ No documentar limitaciones — todo análisis tiene supuestos, documentalos
