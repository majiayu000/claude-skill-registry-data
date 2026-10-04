---
name: frontend-state-management
description: >
  Manejo de estado global en React — Zustand, Redux Toolkit, Context.
  Elige la solución según la complejidad del estado.
  Trigger: Cuando necesitás estado global, compartir datos entre componentes lejanos, o decidir qué herramienta de estado usar.
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "2.0"
  model_tier: T3-balanced
---

# Skill: frontend-state-management

Estado global. Elegí la herramienta correcta y no overengineeres.

## Trigger

- Dos componentes lejanos necesitan compartir datos
- El prop drilling ya es insoportable (5+ niveles)
- Querés persistir estado (localStorage, URL)
- Necesitás devtools para debuggear estado

## Workflow LEND

1. ANALIZAR
   ├── Tipo: ¿estado del servidor (API) o estado del cliente (UI)?
   ├── Server state → TanStack Query (no va acá)
   ├── Client state: ¿global o local? ¿persistente?
   ├── Frecuencia: ¿cambia en cada click o solo al cargar?
   └── ¿Cuánto estado? 2 variables o 50?

2. OFRECER (Menú del Senior)
   ├── A) Zustand — liviano, simple, middleware, suficiente para el 80% de los casos
   ├── B) Context — built-in, para estado simple (theme, auth)
   └── C) Redux Toolkit — estructurado, slices, devtools, para apps grandes

3. ELEGIR → confirmación

4. HACER
   ├── Zustand: store simple con set() y get(), selectors para rerenders controlados
   ├── Context: Provider en el nivel correcto (no en el root si no hace falta)
   ├── Redux: createSlice + configureStore + useAppSelector/useAppDispatch tipados
   ├── Devtools: habilitados en desarrollo, desactivados en producción
   ├── Persist: zustand/middleware persist o redux-persist para localStorage
   └── Selectors: memoizados con createSelector (Redux) o selectores por referencia (Zustand)

5. VERIFICAR
   ├── No hay rerenders innecesarios (React DevTools)
   ├── El estado persiste si es necesario
   └── Los devtools muestran el estado correctamente
