---
name: 03-consulta
description: Úsala cuando el estudiante pida la skill 03 o el requisito R3 (consultar los datos del medidor y guardarlos en caché durante la jornada). Crea el servicio de MockAPI, la caché con TanStack Query y muestra los 7 datos del medidor.
---

# Skill 03: Consulta y caché del medidor (R3)

## Lee antes
docs/CONTRATO.md secciones 1, 3, 4 y 6 (R2 y R3). Si existe ADR-003 en docs/adr/, léelo; si no, manda el contrato.

## Instala
- @tanstack/react-query con `npm install @tanstack/react-query`. Nada más.
- Verifica en su documentación actual el nombre de las opciones `staleTime` y `gcTime`.

## Crea o modifica
- src/services/api.ts: ÚNICO archivo que llama a MockAPI. Función `fetchMeterByCode(code)`: `GET {BASE}/meters?code=<code>` con `fetch`, usando la URL de src/constants/config.ts. Trata un 404 o una lista vacía como "medidor no encontrado". Del resultado, usa solo el elemento cuyo `code === code` EXACTO (el filtro puede ser parcial). Devuelve `MeterDTO`. Si falla la red, lanza un error distinguible.
- src/services/queryClient.ts: un QueryClient con `staleTime` de 12 horas y `gcTime` de 12 horas como mínimo. Importante: si gcTime es menor que staleTime, la caché se borra antes de tiempo. La caché vive solo en memoria (no persistas nada).
- src/hooks/useMeter.ts: `useMeter(code | null)` con useQuery, queryKey `["meter", code]`, habilitado solo si `code` no es null y pasa `meterCodeSchema`. Usa `retry: false` para que el error sin conexión aparezca rápido.
- src/app/_layout.tsx: envuelve la app con QueryClientProvider. Conserva el SQLiteProvider y la protección de sesión.
- src/app/(tecnico)/buscar.tsx: mantiene la validación de la skill 02. Si el código es válido, llama a useMeter y muestra: cargando, "Medidor no encontrado", "Sin conexión y este medidor no está en caché", o los 7 datos (dirección, sector, número de cuenta, estado, última lectura, fecha de última lectura y consumo promedio mensual).
- docs/CONTRATO.md sección 3: agrega queryClient.ts y useMeter.ts, y avísame.

## Reglas
- Un código inválido NUNCA llega a api.ts.
- No usar onlineManager ni expo-network todavía (llega en la skill 08).
- Solo api.ts llama a MockAPI. Estilos solo desde src/theme/tokens.ts.
- No crear la tabla ni el formulario de lectura todavía.

## Checklist
- [ ] npx tsc --noEmit sin errores.
- [ ] Solo @tanstack/react-query como dependencia nueva.
- [ ] La URL sale de .env a través de config.ts. Si la variable falta o la consulta falla por la URL, avísame antes de seguir.
- [ ] Con señal, MED-000001 muestra los 7 datos.
- [ ] Activo modo avión y consulto otra vez MED-000001 (sin recargar la app): muestra los datos sin error.
- [ ] En modo avión, un medidor que no consulté antes muestra el mensaje de sin conexión, sin cerrarse la app.
- [ ] MED-999999 muestra "Medidor no encontrado".
- [ ] Pídeme probar los casos anteriores en el teléfono.

## Al terminar
Actualiza MEMORY.md, escribe la explicación para la defensa y sugiere el mensaje de commit.