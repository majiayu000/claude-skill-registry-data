---
name: suite-de-animacion-gsap
description: Ofrece herramientas de animación esenciales, incluyendo ScrollToPlugin, Flip, Draggable, SplitText, SVG y Physics. Extiende las capacidades principales de GreenSock para crear animaciones web complejas y de alto rendimiento.
---

# Suite de Animación GSAP

## Propósito
Ofrece herramientas de animación esenciales, incluyendo ScrollToPlugin, Flip, Draggable, SplitText, SVG y Physics. Extiende las capacidades principales de GreenSock para crear animaciones web complejas y de alto rendimiento.

## Flujo de trabajo
1. Definir audiencia, objetivo, contenido, plataforma, formato y criterios de éxito.
2. Inspeccionar referencias, tokens, accesibilidad, permisos y datos antes de modificar.
3. Diseñar una propuesta editable, consistente y reversible.
4. Validar responsive, contraste, teclado, legibilidad, rendimiento y coherencia visual.
5. Entregar artefactos, decisiones, supuestos y límites.

## Entradas
Brief, contenido, referencias visuales, código, tokens o archivos proporcionados por el usuario.

## Salida
Maqueta, HTML/CSS/SVG/JSON editable, sistema de tokens, diagrama o informe de revisión.

## Guardrails
- No afirmar que se generó una imagen, video, captura o archivo binario sin producirlo y revisarlo.
- No usar logos, fuentes, datos o assets sin permiso o licencia clara.
- No enviar contenido a APIs de imagen, diseño, MCP o navegador sin solicitud explícita.
- Mantener accesibilidad, privacidad y reversibilidad como criterios de aceptación.

## Plantilla de solicitud
Objetivo: [resultado]
Audiencia: [usuarios]
Contenido: [texto o archivo]
Estilo: [referencia]
Formato: [HTML, CSS, SVG, JSON, Markdown]
Restricciones: [accesibilidad, plataforma, licencia]

## Runner asociado

- **Runner:** `toolkit/phase-5-negocios/suite-de-animacion-gsap/run.py`
- **Motor:** `toolkit/phase_5_engine.py`
- **Entrada de ejemplo:** `toolkit/phase-5-negocios/suite-de-animacion-gsap/input.example.json`
- **Esquema de salida:** `toolkit/phase-5-negocios/suite-de-animacion-gsap/output.schema.json`
- **Prueba smoke:** `toolkit/phase-5-negocios/suite-de-animacion-gsap/tests/test_smoke.py`

La documentación debe mantenerse sincronizada con el runner, el catálogo de la fase y el contrato JSON. El runner local no debe interpretarse como una ejecución externa, publicación o despliegue.

## Lista de control

- [ ] El objetivo, la audiencia y el formato están definidos.
- [ ] Las entradas y sus permisos o fuentes están identificados.
- [ ] La salida corresponde al runner y al esquema JSON de esta herramienta.
- [ ] Los supuestos, advertencias y límites fueron revisados.
- [ ] No se afirmó una ejecución externa, publicación o despliegue sin evidencia.
- [ ] No se incluyeron credenciales ni datos sensibles.
