---
name: sdd-init
description: >
  Inicializa el ciclo SDD en un proyecto — detecta stack, testing, convenciones
  y configura el backend de persistencia.
  Trigger: "sdd init", "iniciar sdd", o al arrancar un proyecto nuevo en el ecosistema.
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "2.0"
---

# Skill: sdd-init

Inicialización SDD. Sin init bien hecho, todas las fases siguientes operan a ciegas.

## Trigger

- Arrancás un proyecto nuevo
- Alguien dice "sdd init" o "iniciar sdd"
- El orquestador detecta que no hay SDD configurado en el proyecto

## Workflow LEND

1. ANALIZAR
   ├── Stack: lenguaje, framework, testing setup, linter
   ├── Estado: ¿ya tiene git? ¿ya tiene CI?
   ├── Convenciones: ¿cómo se estructuran los archivos?
   └── Persistencia: ¿dónde guardar los artefactos SDD?

2. OFRECER (Menú del Senior)
   ├── A) SDD mínimo — solo specs/ + tasks/, sin registro
   ├── B) SDD completo — specs/ + design/ + tasks/ + archive/ + registro
   └── C) SDD + Engram — todo + integración con Engram para auditoría

3. ELEGIR → confirmación

4. HACER
   ├── Crear estructura de carpetas SDD
   ├── Detectar stack y configurar templates
   ├── Configurar backend de persistencia
   └── Documentar convenciones detectadas

5. VERIFICAR
   ├── La estructura SDD existe
   ├── El stack se detectó correctamente
   └── Los templates se generaron sin errores
