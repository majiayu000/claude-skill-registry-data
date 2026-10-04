---
name: frontend-css-styling
description: >
  Estilos CSS modernos — Tailwind, CSS Modules, Grid, Flexbox, Container Queries.
  Elige la estrategia correcta según el proyecto.
  Trigger: Cuando necesitás estilar componentes, decidir entre Tailwind y CSS puro, o hacer layouts responsive.
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "2.0"
  model_tier: T2-fast
---

# Skill: frontend-css-styling

CSS moderno. Seleccioná la estrategia correcta y no mezcles todo.

## Trigger

- Necesitás maquetar un componente o página
- No sabés si usar Tailwind, CSS Modules o CSS-in-JS
- Un layout no se comporta como esperás en mobile
- Hay estilos duplicados o que se pisan entre componentes

## Workflow LEND

1. ANALIZAR
   ├── Stack: ¿Tailwind ya está en el proyecto? ¿CSS Modules?
   ├── Tipo: ¿layout global o componente aislado?
   ├── Estado: ¿estilos dinámicos (prop-driven) o estáticos?
   └── Escala: ¿proyecto chico o grande? Tailwind brilla en equipos grandes

2. OFRECER (Menú del Senior)
   ├── A) Tailwind CSS — utility-first, consistente, ideal para equipos
   ├── B) CSS Modules — scoped por componente, CSS puro, sin runtime
   └── C) CSS Global + BEM — para proyectos chicos o landing pages

3. ELEGIR → confirmación

4. HACER
   ├── Tailwind: config con colores, fonts, spacing en tailwind.config
   ├── CSS Modules: un archivo .module.css por componente
   ├── Layout: Grid para 2D, Flexbox para 1D. Container Queries para responsive por componente
   ├── Variables CSS para temas (--color-primary, --spacing-md)
   └── Mobile-first: min-width en media queries, no max-width

5. VERIFICAR
   ├── El layout se ve bien en mobile y desktop
   ├── No hay estilos que se pisan entre componentes
   └── Los breakpoints son consistentes (no 5 media queries distintos)
