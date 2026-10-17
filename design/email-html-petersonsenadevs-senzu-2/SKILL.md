---
name: email-html
description: "Emails HTML que se ven bien en Gmail/Outlook/Apple Mail: transaccionales y newsletters con react-email/MJML o plantillas del framework, dark mode, texto plano y pruebas antes de enviar. Úsala al maquetar o arreglar cualquier email."
---

# email-html (Senzu)

Los emails NO son webs: el CSS moderno muere en Outlook y cada cliente renderiza distinto. Esta skill
cubre la CONSTRUCCIÓN de la plantilla; el envío (proveedor, colas, reintentos) es de `code-quality
§references/integrations.md` y el diseño de marca sale del design system del proyecto.

## Lectura mínima por tarea
| Tarea | Lee solo |
|---|---|
| Maquetar un email (transaccional o newsletter) | `references/build-emails.md` |
| "Se ve roto en Outlook/Gmail" o probar antes de enviar | `references/compatibility-testing.md` |

## Reglas duras
1. **Herramienta antes que HTML a mano**: react-email (proyectos TS/React), MJML (agnóstico), o las
   plantillas del framework (Laravel Markdown Mail) — compilan a HTML compatible por ti. Tablas a mano
   solo si el proyecto ya lo hace así.
2. **Ancho 600px, una columna** (o columnas que apilan en móvil). Diseño simple: los emails "creativos"
   son los que se rompen.
3. **Todo estilo inline o compilado a inline**; nada de flex/grid/JS/vídeo embebido/fuentes web como única
   opción (fallback a system font SIEMPRE).
4. **Imágenes**: alt SIEMPRE (medio mundo las bloquea), alojadas en URL absoluta https, con dimensiones;
   el mensaje debe entenderse SIN imágenes. Nada crítico dentro de una imagen.
5. **Un CTA principal** como botón "bulletproof" (padding en la celda, no solo en el `<a>`), enlaces
   absolutos con UTM si es marketing (medición: skill `marketing-seo`).
6. **Texto plano** generado siempre (multipart): mejora entregabilidad y accesibilidad.
7. **Preheader** controlado (el texto gris tras el asunto): primera línea oculta con el resumen, o se
   comerá el primer texto que pille.
8. Legales: newsletters con enlace de baja visible y dirección física (LSSI/CAN-SPAM); transaccionales no
   llevan baja pero sí motivo ("Recibes esto porque...").
9. **Probar antes de enviar** (referencia de compatibilidad): render en Gmail+Outlook+iPhone como mínimo,
   dark mode incluido. "En mi navegador se ve bien" no es una prueba.

## Relación con otras skills
- Envío, colas, webhooks de bounces → `code-quality` (`integrations.md`, `jobs-and-queues.md`).
- Colores/logo/tono → design system del proyecto (`BRAND.md`); copy → `ui-ux-pro-max` (`copywriting.md`).
- Medición de campañas (UTM, conversiones) → `marketing-seo`.
