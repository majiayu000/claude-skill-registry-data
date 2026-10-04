---
name: skill-creator
description: >
  Crea nuevas skills para el ecosistema siguiendo el estándar Agent Skills.
  Template, estructura de carpetas y registro automático.
  Trigger: Cuando querés crear una skill nueva, agregar instrucciones para la IA, o documentar patrones.
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "2.0"
  model_tier: T3-balanced
---

# Skill: skill-creator

Creador de skills. Mantené el ecosistema creciendo con orden.

## Trigger

- Un patrón se repite y el agente necesita guía
- El proyecto tiene convenciones propias que difieren de las prácticas genéricas
- Un workflow complejo necesita pasos detallados
- Un árbol de decisión ayuda al agente a elegir el approach correcto

## Workflow LEND

1. ANALIZAR
   ├── ¿Ya existe una skill similar? (buscar en skills/ y AGENTS.md)
   ├── ¿Qué problema resuelve? ¿es específico de un agente o transversal?
   ├── ¿Es para Data, Frontend, DevOps o Transversal?
   └── Formato: ¿sigue el estándar LEND? (trigger → workflow → patrones → anti-patrones)

2. OFRECER (Menú del Senior)
   ├── A) Skill simple — SKILL.md con trigger + workflow básico, sin assets
   ├── B) Skill completa — SKILL.md + assets/ (templates, schemas)
   └── C) Skill con references — SKILL.md + references/ a docs locales

3. ELEGIR → confirmación

4. HACER
   ├── skills/{nombre}/SKILL.md con frontmatter: name, description, trigger, license, metadata
   ├── Template: trigger, workflow LEND, patrones, anti-patrones
   ├── Si necesita: assets/ para templates, references/ para docs locales
   ├── Nombre: corto con guiones (tecnología, proyecto-componente)
   └── Registrar en AGENTS.md

5. VERIFICAR
   ├── La skill existe en skills/
   ├── El manifest del agente la referencia si aplica
   └── Está registrada en AGENTS.md
