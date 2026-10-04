---
name: frontend-web-performance
description: >
  Optimización de rendimiento web — Core Web Vitals, Lighthouse, lazy loading,
  bundle splitting y métricas.
  Trigger: Cuando necesitás optimizar performance, mejorar Lighthouse scores, o reducir el bundle size.
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "2.0"
  model_tier: T3-balanced
---

# Skill: frontend-web-performance

Performance web. Medí antes de optimizar.

## Trigger

- Lighthouse da scores bajos
- La app tarda en cargar
- Las interacciones se sienten lentas
- Querés reducir el bundle de JS

## Workflow LEND

1. ANALIZAR
   ├── Core Web Vitals actuales: LCP, INP, CLS (Lighthouse o PageSpeed)
   ├── Bundle: ¿cuánto pesa? ¿qué librerías ocupan más?
   ├── Imágenes: ¿están optimizadas? ¿formatos modernos?
   └── Fuentes: ¿cargás fuentes custom? ¿con display swap?

2. OFRECER (Menú del Senior)
   ├── A) Quick wins — imágenes next-gen, lazy loading, fuentes display swap
   ├── B) Bundle optimization — code splitting, tree shaking, dynamic imports
   └── C) Full audit — todo + SSR/SSG, CDN, service worker, caching

3. ELEGIR → confirmación

4. HACER
   ├── LCP: optimizar imagen hero (WebP/AVIF, preload), reducir render-blocking resources
   ├── INP: evitar long tasks (>50ms), usar debounce en inputs, lazy load de handlers pesados
   ├── CLS: dimensiones explícitas en imágenes y iframes, no inyectar contenido arriba del fold
   ├── Dynamic imports: React.lazy + Suspense para rutas y componentes pesados
   ├── Bundle analysis: vite build --analyze o webpack-bundle-analyzer
   └── Service worker: Workbox para precaching y runtime caching

5. VERIFICAR
   ├── Lighthouse > 90 en mobile y desktop
   ├── LCP < 2.5s, INP < 200ms, CLS < 0.1
   └── El bundle JS principal es < 100KB (gzipped)
