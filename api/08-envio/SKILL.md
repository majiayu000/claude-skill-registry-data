---
name: 08-envio
description: Úsala cuando el estudiante pida la skill 08 o el requisito R9 (envío automático de lecturas pendientes al recuperar la conexión, sin duplicados, y banner de conexión y pendientes en todas las pantallas). También hace la verificación de lecturas registradas sin conexión (R4).
---

# Skill 08: Envío automático (R9)

## Lee antes
docs/CONTRATO.md secciones 1, 3, 4, 5 y 6 (R4, R9, R10 e idempotencia). Antes de modificarlos, lee src/db/readings.ts, src/services/api.ts, src/hooks/useNetworkStatus.ts, src/domain/consumption.ts, src/app/_layout.tsx, src/app/(tecnico)/index.tsx y lectura/paso-3.tsx. Si existe ADR-008, léelo; si no, manda el contrato.

## Instala
Nada (expo-network ya está). Verifica en la documentación del SDK 57 el uso de `useNetworkState` y la API de `AppState` de React Native.

## Crea o modifica
1. src/db/readings.ts (todas con parámetros preparados):
   - `listPending(db)`: filas con sync_status = 'pending', más antiguas primero.
   - `claimReading(db, clientId)`: UPDATE a 'sending' WHERE client_id = ? AND sync_status = 'pending'. Devuelve true solo si cambió 1 fila.
   - `markSent(db, clientId)`: sync_status = 'sent', sent_at y updated_at ahora, WHERE sync_status = 'sending'.
   - `releaseReading(db, clientId)`: 'sending' → 'pending'.
   - `resetSendingToPending(db)`: todas las 'sending' → 'pending'.
   - `applyVerification(db, clientId, { previousReading, averageMonthly, consumption, isAnomalous })`: actualiza esos campos y pone verification = 'verified', WHERE sync_status = 'sending'.
   - `countUnsent(db)`: cuántas tienen sync_status distinto de 'sent'.
2. src/services/api.ts: agrega `findReadingByClientId(clientId)` (GET /readings?clientId=<id>; devuelve el elemento con clientId IGUAL exacto, o null) y `postReading(dto)` (POST /readings con JSON). Ambas lanzan error si falla la red o la respuesta no es OK. El DTO sale de la fila según ReadingDTO del contrato, con status "sent".
3. src/domain/consumption.ts: `verifyWithMeter(row, meter)` pura: devuelve { previousReading: meter.lastReading, averageMonthly: meter.averageMonthlyConsumption, consumption (readingValue - lastReading, o null si no hay lectura), isAnomalous (consumption > 3 * average, estrictamente mayor, false si consumption es null) }.
4. src/store/sync.ts (Zustand, SIN persistir): { pendingCount, isSyncing, version } y acciones para actualizarlos.
5. src/services/sync.ts: `syncPending(db)`:
   - Exclusión: si ya hay una ejecución en curso, marca que se pidió otra y vuelve; al terminar, si se pidió otra, corre una vez más.
   - Para cada fila de listPending: (a) claimReading; si devuelve false, saltar. (b) Si verification = 'pending_verification': fetchMeterByCode(meterCode); con verifyWithMeter aplica applyVerification. Si el medidor no se puede consultar, releaseReading y seguir con la siguiente. (c) findReadingByClientId; si ya existe, markSent sin enviar. (d) Si no existe, postReading y luego markSent. (e) Ante cualquier error en (b), (c) o (d): releaseReading y DETENER el recorrido (probablemente no hay internet real).
   - Al terminar o fallar: actualiza pendingCount con countUnsent y suma 1 a `version`.
   - `refreshPendingCount(db)`.
6. src/components/SyncManager.tsx (sin interfaz), dentro de los providers del layout raíz: al montar, resetSendingToPending y luego syncPending; vuelve a llamar syncPending cuando isOnline pasa a true (hook useNetworkStatus), cuando la app vuelve a primer plano (AppState) y cada 30 s mientras haya pendientes y la app esté activa (limpia el temporizador al desmontar).
7. src/components/ConnectionBanner.tsx: franja fija arriba, visible en TODAS las pantallas, con "Sin conexión" o "Conectado", "Pendientes: N" y "Enviando…" si isSyncing. Colores solo desde tokens.
8. src/app/_layout.tsx: renderiza <ConnectionBanner /> sobre el Stack y <SyncManager />. Conserva SQLiteProvider, QueryClientProvider y la protección de sesión.
9. src/app/(tecnico)/lectura/paso-3.tsx: tras guardar o corregir una lectura, llama refreshPendingCount y syncPending(db) sin esperar.
10. src/app/(tecnico)/index.tsx: vuelve a cargar la lista cuando cambie `version` del store, además de al enfocar.
11. docs/CONTRATO.md: agrega sync.ts, store/sync.ts, SyncManager, ConnectionBanner y las funciones nuevas de readings.ts. Avísame.

## Reglas
- Nunca enviar una lectura sin pasar por claimReading y por findReadingByClientId.
- Una lectura 'sending' o 'sent' no se corrige.
- Si el POST falla, la lectura vuelve a 'pending' y nada se pierde.
- No usar setInterval para detectar la red; el temporizador de 30 s es solo para reintentar el envío.
- Solo api.ts llama a MockAPI. Estilos solo desde src/theme/tokens.ts.

## Checklist
- [ ] npx tsc --noEmit sin errores.
- [ ] Ninguna dependencia nueva.
- [ ] Con señal, guardo una lectura y en segundos aparece "Enviada", Pendientes: 0, y en el panel de MockAPI (readings) hay UN registro con ese clientId.
- [ ] En modo avión guardo una lectura: banner "Sin conexión" y Pendientes: 1. Apago el modo avión sin tocar la app: se envía sola y queda Pendientes: 0.
- [ ] Una lectura registrada sin conexión como "pendiente de verificar" pasa a verificada tras enviarse, con la lectura anterior del servidor.
- [ ] Guardo sin conexión, cierro la app desde recientes, recupero la señal y la abro: se envía.
- [ ] Enciendo y apago el modo avión varias veces seguidas: en MockAPI sigue habiendo UN solo registro por lectura.
- [ ] El banner se ve en login, lista, buscar y los tres pasos.
- [ ] Una lectura enviada ya no muestra "Corregir".
- [ ] Pídeme probar los casos anteriores.

## Al terminar
Actualiza MEMORY.md, escribe la explicación para la defensa y sugiere el mensaje de commit.