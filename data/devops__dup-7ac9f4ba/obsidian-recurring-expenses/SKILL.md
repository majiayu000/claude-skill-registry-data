---
name: obsidian-recurring-expenses
description: "Identifica y registra gastos recurrentes desde correos y adjuntos con validacion estricta y trazabilidad."
---
# Obsidian Recurring Expenses

## Cuando usar
- Audito gastos recurrentes a partir de correos y adjuntos.
- Necesito actualizar tablas de gastos en el vault.

## Entradas esperadas
- Carpetas de correo (por ejemplo `Mail/Outlook/**`, `Mail/Gmail/**`).
- Carpeta de gastos (por ejemplo `Finance/Expenses/`).
- Adjuntos en subcarpetas `99-Adjuntos/` o equivalente.

## Procedimiento
1. **Lectura obligatoria**
   - Leo el correo y el adjunto original.
   - Registro la lectura en `cache/lecturas.json`.
2. **Validacion estricta**
   - Solo registro cargos reales (factura, confirmacion de pago, total cobrado).
   - Excluyo promociones o notificaciones sin cargo.
3. **Normalizar proveedor**
   - Creo o actualizo una nota por proveedor con una sola tabla consistente.
4. **Formato de tabla (base)**
   - `| Fecha | Importe | Moneda | Factura | Asunto | Fuente |`
   - Separador `|---|---|---|---|---|---|` (sin `:`).
   - `Fuente` con wikilinks relativos sin alias.
5. **Trazabilidad**
   - Dejo registro de cambios y lecturas en la carpeta de contexto del vault.

## Reglas
- No creo notas para proveedores con evidencia insuficiente.
- Si el adjunto es PDF/HTML, convierto a texto con la herramienta disponible.
- Mantengo orden cronologico por fecha.

## Entrega
- Tabla actualizada y referencias verificables.
- Resumen de cambios y fuentes usadas.

