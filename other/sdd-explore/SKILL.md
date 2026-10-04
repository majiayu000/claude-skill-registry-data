---
name: sdd-explore
description: >
  Investiga el código y el dominio del problema ANTES de proponer un cambio.
  Entender antes de actuar.
  Trigger: Investigar una idea, feature, bug o área del código antes de decidir si amerita un cambio formal.
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "2.0"
---

# Skill: sdd-explore

Exploración SDD. Entendé el terreno antes de proponer cambio alguno.

## Trigger

- Tenés una idea o feature que investigar
- Hay que entender un bug antes de proponer el fix
- El orquestador necesita contexto del código antes de decidir

## Workflow LEND

1. ANALIZAR
   ├── ¿Qué área del código? (buscar archivos relevantes)
   ├── ¿Hay contexto en Engram? (consultar antes de leer código)
   ├── Dependencias: ¿qué módulos afecta?
   └── Riesgo: ¿qué tan profundo es el cambio potencial?

2. OFRECER (Menú del Senior)
   ├── A) Lectura rápida — entender la superficie, sin profundizar
   ├── B) Análisis de impacto — qué archivos cambiarían, dependencias
   └── C) Investigación completa — código + tests + documentación + historial

3. ELEGIR → confirmación

4. HACER
   ├── Leer archivos clave del área afectada
   ├── Identificar patrones, convenciones y deuda técnica
   ├── Consultar Engram por decisiones previas
   ├── Documentar hallazgos: lo que funciona, lo que no, lo que falta
   └── Recomendar: ¿amerita un cambio formal? ¿sí, no, o tal vez?

5. VERIFICAR
   ├── El reporte de exploración es claro
   ├── Las recomendaciones están justificadas
   └── Engram tiene el contexto actualizado
