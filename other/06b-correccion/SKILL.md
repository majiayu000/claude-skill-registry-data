---
name: 06b-correccion
description: Úsala cuando el estudiante pida la skill 06b o la parte de corrección de R10 (corregir una lectura pendiente de envío y bloquear la corrección de una ya enviada). Agrega el botón Corregir en la lista y el modo edición del formulario.
---

# Skill 06b: Corrección de lecturas pendientes (R10)

## Lee antes
docs/CONTRATO.md secciones 1, 5 y 6 (R10). Antes de modificarlos, lee src/db/readings.ts, src/store/draft.ts, src/services/photos.ts, src/app/(tecnico)/index.tsx, buscar.tsx y las pantallas de src/app/(tecnico)/lectura/.

## Instala
Nada.

## Crea o modifica
1. src/db/readings.ts:
   - `getReadingByClientId(db, clientId)`.
   - `updateReading(db, row)`: `UPDATE ... WHERE client_id = ? AND sync_status = 'pending'`, con parámetros preparados. Devuelve cuántas filas cambió. Si cambió 0, la lectura ya no es corregible (enviada o enviándose).
2. src/store/draft.ts: agrega `editingClientId: string | null` (persistido) y la acción `startEditDraft(row)`, que carga el borrador desde la fila: mismo clientId, meterCode, condition, readingText, reasonOrDamage, anomalyConfirmed, photoUri, step = 1. Para `meter`: si row.previousReading no es null, arma un MeterDTO con code, lastReading = previousReading y averageMonthlyConsumption = averageMonthly, y '' en los demás campos de texto; si es null, meter = null. `clearDraft` también limpia editingClientId.
3. src/services/photos.ts: `takePhoto` nombra el archivo `evidencia-<clientId>-<Date.now()>.jpg` para que una foto nueva nunca pise la original. Actualiza la nota correspondiente en el contrato (R7).
4. src/store/draft.ts, `setPhotoUri`: si `editingClientId` no es null, NO borra la foto anterior (sigue siendo la de la base de datos hasta guardar).
5. src/app/(tecnico)/index.tsx: cada lectura con sync_status 'pending' muestra el botón "Corregir". Al pulsarlo:
   a. Relee la fila con getReadingByClientId. Si ya no está 'pending', muestra "Esta lectura ya no se puede corregir" y refresca la lista.
   b. Si hay un borrador sin terminar, pregunta con Alert "Hay un registro sin terminar. ¿Reemplazarlo?" (Cancelar / Reemplazar).
   c. Llama startEditDraft(row) y navega a /lectura/paso-1.
   Las lecturas 'sent' muestran "Enviada (no editable)" y las 'sending' "Enviando…", ambas sin botón.
6. src/app/(tecnico)/buscar.tsx: cuando ya existe una lectura de ese medidor en el mes: si está 'pending', el mensaje mantiene el rechazo de un segundo registro y agrega el botón "Corregir lectura pendiente" (mismo flujo del punto 5); si no, solo "Ya enviada: no se puede modificar".
7. Pantallas de lectura/ en modo edición (`editingClientId` no es null):
   - paso-1 resalta el estado actual y permite cambiarlo. Si setCondition ya limpia los campos que dejan de aplicar, no lo cambies.
   - paso-3 muestra "Guardar corrección" en lugar de "Guardar lectura" y no chequea duplicado. Al pulsarlo: relee la fila; arma la fila corregida conservando clientId, monthYear, createdAt y sentAt; actualiza updatedAt; recalcula consumo, isAnomalous y la foto con las mismas reglas de la skill 06. `verification` queda 'pending_verification' si ya lo era; si no, (online && meter !== null) ? 'verified' : 'pending_verification'.
   - Llama updateReading. Si cambió 0 filas, muestra "Esta lectura ya no se puede corregir" y no borra nada. Si salió bien: si la foto cambió, borra la foto anterior con deletePhoto; luego clearDraft() y navega a "/".
8. docs/CONTRATO.md: agrega `editingClientId` y `startEditDraft` a la sección 5 y la regla de nombre de foto a R7. Avísame.

## Reglas
- Solo readings.ts escribe SQL. La corrección jamás crea una fila nueva ni cambia client_id, meter_code ni month_year.
- No enviar a MockAPI ni tocar la red (skill 08). El descarte de borradores llega en la skill 07.
- Estilos solo desde src/theme/tokens.ts.

## Checklist
- [ ] npx tsc --noEmit sin errores.
- [ ] Ninguna dependencia nueva.
- [ ] Guardo MED-000001 con 182 y la corrijo a 183: aparecen la advertencia y la foto obligatoria; al guardar la lista muestra consumo 55 y sigue habiendo UNA sola fila de ese medidor.
- [ ] Corrijo una lectura normal a "dañado" con la lectura vacía: se guarda.
- [ ] Cambio la foto en una corrección: la miniatura muestra la nueva.
- [ ] Empiezo una corrección y salgo sin guardar: la lectura original conserva sus datos y su foto.
- [ ] En buscar, un segundo registro del mismo medidor se rechaza y ofrece corregir la pendiente.
- [ ] Pídeme probar los casos anteriores.

## Al terminar
Actualiza MEMORY.md, escribe la explicación para la defensa y sugiere el mensaje de commit.