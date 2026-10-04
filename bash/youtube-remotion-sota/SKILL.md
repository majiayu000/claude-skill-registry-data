---
name: youtube-remotion-sota
display_name: "Síntesis Programática SOTA de Vídeo React/Remotion"
description: "Renderizado programático de vídeo SOTA utilizando React y Remotion engine. Dispara con \"youtube remotion\", \"remotion render\", \"react video synthesis\", \"renderizar vídeo remotion\"."
---

# Habilidad SOTA: Generación y Animación Programática de Vídeo con Remotion (React Video Engine)

Esta habilidad rige el diseño, arquitectura, composición e invoice de motores de vídeo programáticos utilizando **Remotion** (React para vídeo) en el ecosistema macOS.

## 🎯 Criterios de Activación
- Solicitudes de creación de plantillas de vídeo animadas en React / TypeScript.
- Renderizado programático mediante CLI (`npx remotion render`, `remotion lambda`, `remotion studio`).
- Animaciones basadas en frames (`useCurrentFrame`, `useVideoConfig`, `interpolate`, `spring`).
- Integración de audio sincrónico, subtítulos dinámicos o capas de datos JSON en vídeo.

---

## 🛠️ Protocolo de Ejecución en 4 Fases

### Fase 1: Ingesta y Verificación del Entorno Remotion
1. **Verificar Dependencias:** Comprobar existencia de `node`, `npm` y paquete `remotion` en el directorio de trabajo.
2. **Estructura del Proyecto:** Asegurar la presencia de:
   - `src/Root.tsx`: Registro de composiciones (`<Composition />`).
   - `src/Composition.tsx`: Componente visual principal.
   - `remotion.config.ts`: Configuración de renderizado (fps, codec, concurrencia).

### Fase 2: Desarrollo de Composiciones (Invariantes React/Remotion)
1. **Paso del Tiempo Basado en Frames:** NUNCA usar `setTimeout` o `setInterval`. Toda animación debe derivar de `useCurrentFrame()` y `useVideoConfig()`.
2. **Interpolaciones Suaves:** Usar `interpolate(frame, [start, end], [valA, valB], { extrapolateRight: 'clamp' })` o animaciones físicas mediante `spring({ frame, fps, config })`.
3. **Gestión de Recursos Multimedia:**
   - Usar `<Img src={staticFile("image.png")} />` y `<Audio src={staticFile("audio.mp3")} />` para activos estáticos.
   - Para secuencias de audio o vídeo dinámicas, usar `<Sequence from={startFrame} durationInFrames={length}>`.

### Fase 3: Invariantes de Calidad y Rendimiento SOTA
- **Resoluciones Estándar:** 1920x1080 (Horizontal / YouTube), 1080x1920 (Vertical / Shorts / Reels).
- **Framerate:** 30fps o 60fps estables.
- **Audio Timing:** Sincronización milimétrica con forma de onda usando metadatos JSON.

### Fase 4: Invariantes de Realismo Cinemático SOTA (YouTube High Retention)
1. **Cero Partículas Estroboscópicas / Neón Psicodélico:** Salvo petición explícita, PROHIBIDO incluir partículas flotantes aleatorias o bucles de luces parpadeantes.
2. **Fondos y Entornos Reales:** Usar fotografía real tratada con contraste (`1.15-1.20`), viñeteado ambiental y desenfoque de profundidad de campo (`blur(2-3px)`).
3. **Sombras de Caída Naturales:** Aplicar `drop-shadow(0 35px 60px rgba(0,0,0,0.92))` sobre avatares y elementos superpuestos para integrarlos de forma orgánica.
4. **Cámara de Retención Dinámica (60 FPS Push-in):** Aplicar interpolación lenta `interpolate(frame, [0, 1800, 3600], [1.0, 1.06, 1.02])` a 60 FPS para mantener la retención de audiencia en YouTube.
5. **Soporte Dual Panorámico / Shorts:** Diseñar composiciones adaptativas que respondan a la relación de aspecto (1920x1080 Landscape y 1080x1920 Shorts).
6. **Subtítulos Cinéticos & Marca de Agua TV:** Incluir insignias de emisión (`4K ULTRA HD 60FPS`) y banners de estudio con indicador de directo en vivo.

### Fase 5: Renderizado y Entrega de Salida (Invariante macOS QuickTime / Safari)
1. **Vista Previa:** Ofrecer comando para previsualización local:
   ```bash
   npx remotion render src/index.ts <CompositionId> out/video.mp4 --codec=h264 --pixel-format=yuv420p
   ```
2. **Directorio de Ejecución Obligatorio (CWD):** Ejecutar el CLI `remotion render` SIEMPRE dentro del directorio raíz del subproyecto donde residen `package.json` y `node_modules` (ej: `video-engine/`).
3. **Formato de Píxeles Obligatorio:** Incluir SIEMPRE `--pixel-format=yuv420p` en renderizados H.264 para garantizar compatibilidad con macOS QuickLook, QuickTime Player y navegadores Safari/Chromium.
4. **Verificación del Output:** Comprobar la existencia del archivo `.mp4` y verificar su reproducción con `ffprobe` / QuickLook.