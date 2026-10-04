---
name: frontend-responsive-design
description: >
  Diseño responsive moderno — Container Queries, Grid, Flexbox, clamp().
  Mobile-first, adaptable a cualquier pantalla.
  Trigger: Cuando necesitás que un layout funcione en mobile y desktop, o un componente se adapte a su contenedor.
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "2.0"
  model_tier: T2-fast
---

# Skill: frontend-responsive-design

Responsive design moderno. Mobile-first, Container Queries, tamaños fluidos.

## Trigger

- Un layout no funciona en mobile
- Un componente debería adaptarse a diferentes contenedores (sidebar, main, modal)
- Querés tamaños de fuente que escalen sin media queries
- Necesitás breakpoints consistentes en todo el proyecto

## Workflow LEND

1. ANALIZAR
   ├── Contexto: ¿página completa o componente aislado?
   ├── Público: ¿mobile-first o desktop-first? (casi siempre mobile-first)
   ├── Estado actual: ¿ya hay breakpoints? ¿son consistentes?
   └── Contenedor: ¿el componente vive en diferentes anchos?

2. OFRECER (Menú del Senior)
   ├── A) Media Queries — breakpoints tradicionales, mobile-first (min-width)
   ├── B) Container Queries — responsive por contenedor, ideal para componentes reutilizables
   └── C) Híbrido — Container Queries para componentes, Media Queries para layout global

3. ELEGIR → confirmación

4. HACER
   ├── Mobile-first: estilos base para mobile, media queries con min-width para desktop
   ├── Container Queries: container-type: inline-size en el padre, @container en el hijo
   ├── clamp() para tamaños fluidos: font-size: clamp(1rem, 2.5vw, 2rem)
   ├── Grid + auto-fit para layouts que se adaptan solos
   ├── dvw/dvh para viewport dinámico (móviles con toolbar)
   └── Breakpoints consistentes: 480px, 768px, 1024px, 1280px

5. VERIFICAR
   ├── El componente se ve bien en 320px, 768px, 1280px
   ├── No hay scroll horizontal
   └── Los textos son legibles sin zoom
