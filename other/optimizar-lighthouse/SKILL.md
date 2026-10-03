---
name: optimizar-lighthouse
description: Audita el rendimiento del bundle de Next.js, imágenes y componentes multimedia para garantizar métricas de Lighthouse elevadas.
---

### Instrucciones para el Agente:
1. Ejecuta `pnpm build` y analiza la salida del build para comprobar que el first-load JS no supere los 250 KB.
2. Revisa los componentes multimedia (`VideoShowcase`, `GlobalAudioPlayer`, `StemsPlayer`) y confirma que se utilice el patrón fachada (Facade Pattern) para diferir scripts de terceros (como IFrames de YouTube/Vimeo).
3. Verifica que las imágenes utilicen `next/image` con propiedades de `priority` o `loading="lazy"` según su ubicación en la pantalla (viewport).
4. Confirma que no existan re-renders innecesarios en componentes que usen Web Audio API o `<canvas>`.