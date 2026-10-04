---
name: sdd-propose
description: >
  Crea la propuesta de cambio: el qué y por qué. Declaración de intención
  antes de invertir tiempo en specs y diseño.
  Trigger: Después de exploration o con input directo del usuario, para formalizar una idea como change proposal.
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "2.0"
---

# Skill: sdd-propose

Propuesta de cambio. Alinear antes de invertir.

## Trigger

- La exploración está completa
- El usuario tiene una idea clara de lo que quiere
- Hay que formalizar un cambio antes de especificarlo

## Workflow LEND

1. ANALIZAR
   ├── Contexto: ¿qué problema resuelve? ¿para quién?
   ├── Alternativas: ¿hay otras formas de resolverlo?
   ├── Impacto: ¿qué módulos, usuarios, o procesos afecta?
   └── Urgencia: ¿es necesario ahora o puede esperar?

2. OFRECER (Menú del Senior)
   ├── A) Propuesta simple — título + descripción + motivación
   ├── B) Propuesta estructurada — problema, solución propuesta, alternativas, impacto
   └── C) Propuesta con análisis — lo mismo + estimación de esfuerzo + riesgos

3. ELEGIR → confirmación

4. HACER
   ├── Redactar: qué se quiere lograr y por qué
   ├── Incluir: contexto, motivación, descripción, alternativas consideradas
   ├── Definir: criterios de éxito medibles
   ├── Documentar: decisiones y tradeoffs
   └── Guardar: como entrada para sdd-spec

5. VERIFICAR
   ├── La propuesta es clara para alguien sin contexto previo
   ├── Los criterios de éxito son medibles
   └── Las alternativas están documentadas
