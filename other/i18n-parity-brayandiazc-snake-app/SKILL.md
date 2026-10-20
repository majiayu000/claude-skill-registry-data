---
name: i18n-parity
description: Verifica la paridad de internacionalización — que cada clave de traducción exista en todos los idiomas y que no haya cadenas visibles para la persona usuaria codificadas de forma fija — siguiendo las convenciones de i18n del proyecto. Úsalo cuando la persona pida revisar las traducciones, verificar la paridad entre idiomas, encontrar cadenas faltantes/codificadas o auditar la i18n (p. ej. "revisa la i18n", "¿están todos los idiomas sincronizados?").
---

Verifica la paridad entre idiomas y detecta cadenas visibles para la persona usuaria codificadas de forma fija.

1. Lee `docs/conventions/i18n.md` para conocer el formato de los archivos de idioma, dónde viven los archivos de traducción, el idioma por defecto/de referencia y la regla sobre qué debe traducirse.
2. Lista los archivos de idioma y trata el idioma de referencia como la fuente de verdad para el conjunto de claves.
3. Compara las claves entre idiomas:
   - Claves presentes en la referencia pero faltantes en otro idioma → repórtalas como faltantes.
   - Claves presentes en un idioma pero no en la referencia → repórtalas como huérfanas.
   - Valores vacíos o sin traducir pero idénticos → márcalos para revisión.
4. Escanea el código fuente de la UI en busca de cadenas visibles para la persona usuaria codificadas de forma fija que deberían pasar por el sistema de i18n (según las reglas de la convención), y enumera cada una con archivo:línea.
5. Opcionalmente, ejecuta el ayudante incluido `scripts/check.sh` (relativo a este skill) para una pasada automatizada rápida — pero ten en cuenta que es un STUB que la persona debe adaptar a su formato real de i18n antes de confiar en él.
6. Informa un resumen: claves faltantes por idioma, claves huérfanas y cadenas sospechosas de estar codificadas de forma fija.

NO traduzcas automáticamente ni inventes texto de traducción — reporta las brechas para que una persona/traductora las complete. Da siempre prioridad a `docs/conventions/i18n.md`.
