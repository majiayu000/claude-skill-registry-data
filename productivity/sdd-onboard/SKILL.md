---
name: sdd-onboard
description: >
  Guía al usuario por un ciclo SDD completo de principio a fin usando su
  codebase real. Aprender haciendo.
  Trigger: Para hacer onboarding de un usuario nuevo en el ciclo SDD.
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "2.0"
---

# Skill: sdd-onboard

Onboarding SDD. Aprender haciendo un cambio real.

## Trigger

- Un usuario nuevo necesita aprender SDD
- Alguien pidió "sdd on board" o "guíame por SDD"
- El orquestador detecta que el usuario no usó SDD antes

## Workflow LEND

1. ANALIZAR
   ├── Usuario: ¿nivel técnico? ¿conoce el proyecto?
   ├── Proyecto: ¿tiene SDD inicializado? ¿tiene specs?
   ├── Cambio ideal: algo chico, real y valioso
   └── Tiempo: ¿cuánto tiene el usuario? (30 min, 1 hora, 2 horas)

2. OFRECER (Menú del Senior)
   ├── A) Tour rápido — recorrer las fases SDD con un cambio trivial
   ├── B) Cambio guiado — hacer un cambio real pequeñito paso a paso
   └── C) Ciclo completo — init + explore + propose + spec + design + tasks + apply + verify + archive

3. ELEGIR → confirmación

4. HACER
   ├── Elegir un cambio chico y real en el proyecto actual
   ├── Recorrer cada fase SDD: explorar → proponer → especificar → diseñar → taskear → aplicar → verificar → archivar
   ├── Explicar el propósito de cada fase mientras se hace
   ├── Mostrar los artefactos que se generan en cada paso
   └── Al final: resumen de lo aprendido y referencia para próximos ciclos

5. VERIFICAR
   ├── El usuario completó el ciclo SDD
   ├── El cambio está mergeado (o listo para mergear)
   └── El usuario entiende cuándo y por qué usar SDD
