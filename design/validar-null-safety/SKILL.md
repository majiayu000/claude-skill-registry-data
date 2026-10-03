---
name: validar-null-safety
description: Audita la interfaz UI y utilidades para garantizar renderizado seguro en valores nulos u opcionales.
---

# Skill: Control de Null-Safety

Analiza los componentes recién construidos para prevenir errores en tiempo de ejecución (`TypeError: Cannot read properties of undefined`):

1. **Evaluación de Campos Opcionales:**
   - Audita `youtube_video_id`, `effects_chain`, `lyrics` y métricas.
2. **Aplicación de Helper:**
   - Garantiza que `safeString()`, `hasValue()` o renderizado condicional (`&&` / ternarios) estén aplicados en los componentes visuales.
3. **Verificación de Tipos:**
   - Ejecuta `npx tsc --noEmit` para asegurar 0 advertencias estrictas en TypeScript.