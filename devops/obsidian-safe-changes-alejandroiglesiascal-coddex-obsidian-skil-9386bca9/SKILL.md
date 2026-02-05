---
name: obsidian-safe-changes
description: "Cambios seguros en archivos del vault: mover, renombrar, editar o eliminar con trazabilidad y recuperacion."
---
# Obsidian Safe Changes

## Cuando usar
- Necesito mover, renombrar, editar o eliminar archivos.
- La tarea tiene impacto potencial en enlaces.

## Guardrails
- Si hay ambiguedad o impacto alto (>=10 archivos o multiples carpetas), pregunto antes.
- Siempre dejo reversibilidad (papelera o backup) antes de borrar o mover.
- Valido wikilinks despues de cambios relevantes.

## Procedimiento
1. **Definir alcance**
   - Confirmo rutas origen/destino y cantidad de archivos.
2. **Preparar reversibilidad**
   - Creo copia en `context/trash/YYYYMMDD/` o ruta equivalente del vault.
3. **Ejecutar cambios**
   - Mover/renombrar/editar/eliminar segun el plan minimo seguro.
4. **Registrar**
   - Registro en `context/migrations/YYYYMMDD/` lo movido, renombrado o borrado.
5. **Validar**
   - Reviso wikilinks principales y documento si hubo degradaciones.

## Entrega
- Lista de cambios con rutas afectadas.
- Evidencia de reversibilidad y validacion de enlaces.

