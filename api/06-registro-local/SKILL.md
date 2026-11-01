---
name: 06-registro-local
description: Úsala cuando el estudiante pida la skill 06 o los requisitos R4 y R10 (guardar la lectura en SQLite, también sin conexión, marcarla pendiente de verificar y rechazar un segundo registro del mismo medidor en el mismo mes). Agrega el guardado, la lista de lecturas locales y el chequeo de duplicados.
---

# Skill 06: Registro local (R4 + duplicados de R10)

## Lee antes
docs/CONTRATO.md secciones 1, 3, 5 y 6 (R4 y R10). Antes de modificarlos, lee src/store/draft.ts, src/domain/consumption.ts, src/schemas/reading.ts, src/app/(tecnico)/buscar.tsx e index.tsx y las pantallas de src/app/(tecnico)/lectura/.

## Instala
- expo-network con `npx expo install`. Nada más.
- Verifica en la documentación del SDK 57: `useNetworkState`, `getNetworkStateAsync` y sus campos `isConnected` e `isInternetReachable`; y la API async de expo-sqlite (`runAsync`, `getAllAsync`, `getFirstAsync`) con parámetros preparados.

## Crea o modifica
1. src/hooks/useNetworkStatus.ts: hook `useNetworkStatus()` que devuelve `{ isOnline }` y función `isOnlineNow()` async. isOnline = isConnected === true && isInternetReachable !== false.
2. src/domain/date.ts: `currentMonthYear(date = new Date())` devuelve "MM-YYYY" con la hora LOCAL.
3. src/db/readings.ts: ÚNICO archivo con SQL de lecturas. Todas las funciones reciben `db` y usan parámetros preparados, nunca texto concatenado:
   - `insertReading(db, row)` con las columnas del contrato; sync_status = 'pending'.
   - `getReadingByMeterMonth(db, meterCode, monthYear)`.
   - `listReadings(db)`: más recientes primero.
   - Define el tipo `ReadingRow` (camelCase) en src/types/index.ts y mapea desde y hacia las columnas snake_case dentro de este archivo.
4. Medidor sin datos (R4, sin señal): `draft.meter` puede ser null (el medidor no estaba en caché). `startDraft` pasa a recibir (meterCode, meter | null). Con meter null no se calcula consumo ni anomalía, y paso-2 muestra "Sin la lectura anterior: se verificará al recuperar la conexión". Adapta src/domain/consumption.ts, src/schemas/reading.ts, src/store/draft.ts y paso-2 para aceptar null sin romper los casos existentes (182 sin advertencia, 183 con advertencia).
5. src/app/(tecnico)/buscar.tsx:
   - Antes de "Registrar lectura", comprueba con getReadingByMeterMonth(code, currentMonthYear()). Si existe una lectura (en cualquier estado), muestra "Ya existe una lectura de <código> en <mes>" y NO navegues.
   - Si la consulta falla por falta de conexión y el medidor no está en caché, conserva el mensaje actual y agrega el botón "Registrar sin datos del medidor", que llama startDraft(code, null) (con el mismo chequeo de duplicado).
6. src/app/(tecnico)/lectura/paso-3.tsx: agrega el botón "Guardar lectura", deshabilitado mientras falte algo (por ejemplo, la foto obligatoria). Al pulsarlo:
   a. `online = await isOnlineNow()`.
   b. Arma la fila: clientId del borrador, meterCode, monthYear = currentMonthYear(), condition, readingValue (número o null), reasonOrDamage, previousReading = meter?.lastReading ?? null, averageMonthly = meter?.averageMonthlyConsumption ?? null, consumption (null si falta la lectura o la lectura anterior), isAnomalous (false si no hay meter), anomalyConfirmed, photoUri, verification = (online && meter !== null) ? 'verified' : 'pending_verification', createdAt = updatedAt = ISO de ahora, sentAt = null.
   c. Repite el chequeo de duplicado y captura además el error UNIQUE de SQLite, mostrando el mismo mensaje.
   d. insertReading. Si sale bien: clearDraft() SIN borrar la foto (ahora pertenece a la lectura) y navega a "/" reemplazando la pila del registro.
7. src/app/(tecnico)/index.tsx: lista desde listReadings, refrescada cada vez que la pantalla toma foco (verifica en la documentación de Expo Router el hook adecuado). Cada ítem muestra: meterCode, mes, estado (condition), consumo ("—" si es null), miniatura de la foto (48x48) si hay photoUri, y etiquetas "Pendiente de envío" (sync_status distinto de 'sent'), "Pendiente de verificar" (verification) y "Enviada". Conserva "Nueva lectura" y "Cerrar sesión".
8. docs/CONTRATO.md secciones 3 y 5: agrega useNetworkStatus.ts, domain/date.ts, db/readings.ts y que draft.meter puede ser null. Avísame.

## Reglas
- Solo readings.ts escribe SQL de lecturas; ninguna pantalla importa SQL.
- No enviar a MockAPI, no corregir lecturas, no usar listener de red ni banner (skill 08). El estado de red solo se consulta al guardar.
- La edición llega en la skill 06b-correccion.
- Estilos solo desde src/theme/tokens.ts.

## Checklist
- [ ] npx tsc --noEmit sin errores.
- [ ] Solo expo-network como dependencia nueva.
- [ ] Con señal, MED-000001, lectura 182, guardar: aparece en la lista como "Pendiente de envío" y NO como pendiente de verificar.
- [ ] Consulto MED-000002 con señal, activo modo avión y registro una lectura: se guarda como "Pendiente de verificar".
- [ ] En modo avión, MED-000003 sin haberlo consultado: "Registrar sin datos del medidor" permite guardar; consumo "—" y "Pendiente de verificar".
- [ ] Un segundo registro del mismo medidor en el mismo mes es rechazado.
- [ ] Cierro la app desde recientes y la abro: las lecturas y sus miniaturas siguen en la lista.
- [ ] Con 183 y foto obligatoria no deja guardar sin foto.
- [ ] Pídeme probar todos los casos anteriores.

## Al terminar
Actualiza MEMORY.md, escribe la explicación para la defensa y sugiere el mensaje de commit.