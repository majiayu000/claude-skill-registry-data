---
name: cursor-sobredimensionado
description: Proporciona una técnica de puntero de macOS sobredimensionado de estilo propio para vídeos de lanzamiento.
---

# Cursor sobredimensionado

## Propósito
Proporciona una técnica de puntero de macOS sobredimensionado de estilo propio para vídeos de lanzamiento.

## Flujo de trabajo
1. Definir objetivo, audiencia, derechos de uso, formato, duración, plataforma y criterio de éxito.
2. Inspeccionar material, codecs, metadatos, licencias, identidad y restricciones antes de modificar.
3. Crear un storyboard, prompt, subtítulo, receta o plan de producción editable.
4. Validar sincronización, accesibilidad, calidad, continuidad, derechos y exportación.
5. Entregar el artefacto y registrar supuestos, fuentes y límites.

## Entradas
Brief, audio, video, imagen, texto, guion, subtítulos y referencias proporcionados por el usuario.

## Salida
Storyboard, prompt audiovisual, SRT/VTT, HTML/SVG, receta de edición, plan de render o informe verificable.

## Guardrails
- No se genera ni publica audio, video o imagen sin solicitud explícita y revisión.
- No se clona voz, rostro, identidad o estilo protegido sin autorización.
- No se usa material con derechos dudosos ni se presenta una maqueta como render final.
- No se llaman APIs de video, música, TTS, transcripción o imágenes por defecto.

## Plantilla de solicitud
Objetivo: [resultado]
Material: [ruta o descripción]
Audiencia: [público]
Formato: [MP4, WAV, SRT, HTML]
Duración: [segundos]
Derechos y restricciones: [autorizaciones]

## Runner asociado

- **Runner:** `toolkit/phase-6-medios/cursor-sobredimensionado/run.py`
- **Motor:** `toolkit/phase_6_engine.py`
- **Entrada de ejemplo:** `toolkit/phase-6-medios/cursor-sobredimensionado/input.example.json`
- **Esquema de salida:** `toolkit/phase-6-medios/cursor-sobredimensionado/output.schema.json`
- **Prueba smoke:** `toolkit/phase-6-medios/cursor-sobredimensionado/tests/test_smoke.py`

La documentación debe mantenerse sincronizada con el runner, el catálogo de la fase y el contrato JSON. El runner local no debe interpretarse como una ejecución externa, publicación o despliegue.

## Lista de control

- [ ] El objetivo, la audiencia y el formato están definidos.
- [ ] Las entradas y sus permisos o fuentes están identificados.
- [ ] La salida corresponde al runner y al esquema JSON de esta herramienta.
- [ ] Los supuestos, advertencias y límites fueron revisados.
- [ ] No se afirmó una ejecución externa, publicación o despliegue sin evidencia.
- [ ] No se incluyeron credenciales ni datos sensibles.
