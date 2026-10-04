---
name: frontend-react-development
description: >
  Desarrollo de componentes React con hooks, patrones y mejores prácticas.
  Componentes reutilizables, estado local y composición.
  Trigger: Cuando necesitás crear componentes React, hooks, manejar estado local, o decidir entre patrones de componentes.
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "2.0"
  model_tier: T3-balanced
---

# Skill: frontend-react-development

Componentes React que escalan. No es magia, es patrones.

## Trigger

- Necesitás crear un componente nuevo
- Un componente se está volviendo muy grande y hay que partirlo
- No sabés si usar prop drilling, contexto, o estado local
- Querés decidir entre Server Component o Client Component

## Workflow LEND

1. ANALIZAR
   ├── ¿Es servidor o cliente? ¿necesita interactividad, useState, useEffect?
   ├── ¿Composición o herencia? React prefiere composición siempre
   ├── Estado: ¿local, lifting, contexto, o externo?
   └── Props: ¿cuántas? ¿tipadas? ¿con valores default?

2. OFRECER (Menú del Senior)
   ├── A) Componente simple — function + props, sin estado, puro render
   ├── B) Componente con estado — hooks internos (useState, useReducer)
   └── C) Compound component — varios sub-componentes que comparten estado vía contexto

3. ELEGIR → confirmación

4. HACER
   ├── TypeScript estricto, props tipadas con interface
   ├── Componente pequeño (< 100 líneas). Si crece, partilo.
   ├── Custom hooks para lógica reutilizable (useDatos, useAuth)
   ├── useMemo/useCallback solo si hay rerenders demostrables (no premature optimization)
   ├── Server Component por defecto, Client Component solo cuando necesitás interactividad
   └── Estados: loading, empty, error, success — siempre cubiertos

5. VERIFICAR
   ├── El componente funciona en aislamiento
   ├── Los tipos son correctos (tsc sin errores)
   └── No hay warnings de React en consola

## Patrones

- **Composición > Props**: pasá componentes como children en vez de 15 props booleanas
- **Custom hooks**: extraé lógica repetida a hooks (useFetch, useLocalStorage)
- **Server Component first**: menos JS en el cliente, mejor performance
- **Estados visibles**: loading, empty, error, success — no dejés ningún estado sin cubrir
- **Props con defaults**: destructuring con valor default, no && encadenados

## Anti-patrones

- ❌ Componentes de 300 líneas — partí en componentes chicos
- ❌ useEffect sin dependencias — "solo al montar" casi nunca es correcto
- ❌ Prop drilling de 5 niveles — usá contexto o composición
- ❌ useMemo/useCallback en todos lados — midamos primero
- ❌ Cero estados intermedios — la pantalla no puede quedarse en blanco mientras carga
