---
name: frontend-api-integration
description: >
  Consumo de APIs en el frontend — TanStack Query, fetch, Axios.
  Caché, refetch, optimistic updates y manejo de errores.
  Trigger: Cuando necesitás consumir APIs desde el frontend, cachear respuestas, o manejar estados de carga/error.
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "2.0"
  model_tier: T3-balanced
---

# Skill: frontend-api-integration

APIs en el frontend. Que los datos lleguen sin romper la UI.

## Trigger

- Un componente necesita traer datos de una API
- Las llamadas se repiten sin cachear
- Querés hacer optimistic update (cambiar la UI antes de la respuesta)
- Hay que manejar loading, error y retry

## Workflow LEND

1. ANALIZAR
   ├── Stack: ¿TanStack Query ya está en el proyecto?
   ├── Tipo: ¿GETs, POSTs, suscripciones? ¿REST o GraphQL?
   ├── Caché: ¿los datos cambian seguido? ¿pueden ser stale?
   └── Errores: ¿cómo se muestran? ¿toast, inline, página de error?

2. OFRECER (Menú del Senior)
   ├── A) TanStack Query — caché, refetch, paginación, mutations
   ├── B) fetch nativo — sin dependencias, para apps chicas
   └── C) SWR — liviano, stale-while-revalidate, si no necesitás mutations complejas

3. ELEGIR → confirmación

4. HACER
   ├── TanStack Query: useQuery + useMutation con queryClient central
   ├── Caché: staleTime configurado (no dejar defaults de 0)
   ├── Errores: onError global + retry con backoff
   ├── Optimistic updates: onMutate actualiza caché, onError rollback
   ├── Loading: useQuery isLoading vs isFetching (la primera carga vs refetch)
   └── Tipado: respuesta tipada con genéricos (useQuery<Datos>)

5. VERIFICAR
   ├── Las llamadas se cachean correctamente (Network tab)
   ├── Los errores se muestran al usuario
   └── El refetch funciona después de una mutación (invalidateQueries)
