---
name: skill-registry
description: >
  Gestiona el registro central de skills — sync skills/ con AGENTS.md y
  registry/AGENT_REGISTRY.md, detecta skills huérfanas o faltantes.
  Trigger: "update skills", "skill registry", "actualizar skills", o después de instalar/remover skills.
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "2.0"
  model_tier: T2-fast
---

# Skill: skill-registry

Registro de skills. Que no haya skills huérfanas ni manifiestos rotos.

## Trigger

- Instalaste o removiste una skill
- AGENTS.md está desactualizado
- Querés verificar que todas las skills tienen su registro
- Necesitás auditar el ecosistema de skills

## Workflow LEND

1. ANALIZAR
   ├── skills/ actual: ¿qué skills existen?
   ├── AGENTS.md: ¿qué skills están registradas?
   ├── Diferencias: ¿skills sin registro? ¿registros sin skill?
   └── Manifiestos: ¿skills sin manifest correspondiente?

2. OFRECER (Menú del Senior)
   ├── A) Sync rápido — agregar skills faltantes a AGENTS.md
   ├── B) Auditoría completa — skills/ vs AGENTS.md vs manifests, reporte de discrepancias
   └── C) Registry cleanup — marcar skills deprecadas, unificar duplicadas

3. ELEGIR → confirmación

4. HACER
   ├── skills/ vs AGENTS.md: agregar skills faltantes a la tabla
   ├── AGENTS.md vs skills/: marcar skills deprecadas que ya no existen
   ├── skills/ vs manifests: skills sin manifest → agregar a known_without_manifest
    ├── Guardar reporte en registry/AGENT_REGISTRY.md
   └── Guardar en engram el resultado de la auditoría

5. VERIFICAR
   ├── skills/ y AGENTS.md están sincronizados
   ├── No hay skills huérfanas sin registrar
   └── El registry está guardado
