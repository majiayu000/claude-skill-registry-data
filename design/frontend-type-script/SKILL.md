---
name: frontend-type-script
description: >
  TypeScript 5.x strict — tipos, genéricos, satisfies, template literal types.
  Código tipado que no molesta, ayuda.
  Trigger: Cuando necesitás tipar componentes, definir interfaces, usar genéricos, o resolver errores de tipos.
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "2.0"
  model_tier: T3-balanced
---

# Skill: frontend-type-script

TypeScript strict. Que los tipos te ayuden, no que te estorben.

## Trigger

- Estás escribiendo una función o componente nuevo
- Un error de tipos no te deja compilar
- Tenés `any` en el código y querés sacarlo
- Necesitás un tipo complejo (intersección, unión discriminada, template literal)

## Workflow LEND

1. ANALIZAR
   ├── ¿strict mode está activado? tsconfig.json: strict: true
   ├── ¿Hay anys? contalos y planeá eliminarlos
   ├── ¿Los tipos reflejan el dominio o solo repiten la forma de los datos?
   └── ¿Hay tipos compartidos que deberían estar en una carpeta types/?

2. OFRECER (Menú del Senior)
   ├── A) Tipado simple — interface + type, sin genéricos complejos
   ├── B) Tipado genérico — utility types, genéricos, satisfies
   └── C) Tipado avanzado — template literal types, infer, conditional types

3. ELEGIR → confirmación

4. HACER
   ├── interface para objetos (extensible), type para uniones y primitivos
   ├── satisfies para validar que un valor cumple un tipo sin asumirlo
   ├── as const para objetos literales con tipos exactos
   ├── discriminated unions para estados (type State = Loading | Success | Error)
   ├── z.
   └── stricter: evitar `any`, preferir `unknown` si no sabés el tipo

5. VERIFICAR
   ├── tsc sin errores (o vite build)
   ├── No hay anys nuevos
   └── Los tipos ayudan al autocompletado sin ser una novela
