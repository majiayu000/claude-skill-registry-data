---
name: 04-formulario
description: Úsala cuando el estudiante pida la skill 04 o los requisitos R5 y R6 (estados del medidor, reglas de lectura, cálculo de consumo y alerta del triple del promedio). Crea el borrador, los pasos del formulario con React Hook Form y Zod, y el cálculo de consumo.
---

# Skill 04: Formulario de lectura (R5 + R6)

## Lee antes
docs/CONTRATO.md secciones 1, 3, 5 y 6 (R5 y R6). Si existen ADR-004, ADR-005 y ADR-006 en docs/adr/, léelos; si no, manda el contrato.

## Instala
- react-hook-form y @hookform/resolvers con `npm install`. Nada más (zod ya está).
- Verifica en la documentación del resolver que la versión instalada soporta la versión de zod instalada, y usa la importación correcta. Si hay conflicto, avísame antes de seguir.

## Crea o modifica
- src/domain/consumption.ts (funciones puras, sin React): `calculateConsumption(reading, lastReading)` = reading - lastReading; `isAnomalous(consumption, average)` = consumption > 3 * average (estrictamente mayor); `isPhotoRequired(condition, anomalous)` = anomalous || condition === "dañado".
- src/store/draft.ts: Zustand con persist, el mismo storage que usa src/store/session.ts. Estado: { step, meterCode, meter (MeterDTO), condition, readingText, reasonOrDamage, anomalyConfirmed, photoUri, hasHydrated } y acciones: startDraft(meter) (reinicia todo), setStep(n), setCondition(c), setReadingData({...}), clearDraft(). Persiste todo menos hasHydrated y las acciones.
- src/schemas/reading.ts: `buildReadingSchema({ condition, lastReading, average })` con Zod sobre campos string:
  - normal: lectura obligatoria.
  - inaccesible: motivo obligatorio; la lectura debe quedar vacía.
  - dañado: descripción obligatoria; lectura opcional.
  - La lectura debe ser un número no negativo (permite coma o punto decimal; conviértelo a número al calcular).
  - Si hay lectura y es anómala, `anomalyConfirmed` debe ser true.
- src/app/(tecnico)/lectura/_layout.tsx: Stack sencillo.
- src/app/(tecnico)/lectura/paso-1.tsx: tres botones (normal, inaccesible, dañado). Al elegir uno, guarda con setCondition y navega a paso-2.
- src/app/(tecnico)/lectura/paso-2.tsx: useForm con zodResolver y Controller. Campo de lectura (oculto o deshabilitado y vacío si es inaccesible) y un campo de texto de motivo o descripción (la etiqueta cambia según el estado). Con una lectura escrita, muestra el consumo calculado en vivo; si es anómalo, muestra la advertencia y un Switch "Revisé el medidor" obligatorio. Si la lectura es menor que la anterior, muestra un aviso informativo sin bloquear (la rúbrica no define ese caso). Al continuar, guarda en el store y navega a paso-3.
- src/app/(tecnico)/lectura/paso-3.tsx: solo un resumen de lo guardado en el borrador y un texto "La foto y el guardado se implementan en las skills 05 y 06". Sin botón de guardar.
- src/app/(tecnico)/buscar.tsx: cuando hay datos del medidor, agrega un botón "Registrar lectura" que llama startDraft(meter) y navega a /lectura/paso-1.
- Cada paso llama setStep(n) al montarse. Los valores del store son los valores iniciales del formulario, para que al volver atrás no se pierdan.
- docs/CONTRATO.md: agrega src/domain/ a la sección 3, los campos reales de draft.ts a la sección 5, y aclara que la advertencia y la confirmación de R6 están en paso-2. Avísame de cada cambio.

## Reglas
- Todo el cálculo vive en src/domain/consumption.ts; las pantallas no calculan.
- No tocar src/db ni crear la cámara. Estilos solo desde src/theme/tokens.ts.
- Los campos de texto son string; el resolver valida strings.

## Checklist
- [ ] npx tsc --noEmit sin errores.
- [ ] Solo react-hook-form y @hookform/resolvers como dependencias nuevas.
- [ ] MED-000001 (anterior 128, promedio 18): lectura 182 → consumo 54, sin advertencia; 183 → consumo 55, advertencia y confirmación obligatoria.
- [ ] MED-000002 (anterior 356, promedio 24): 428 → sin advertencia; 429 → advertencia.
- [ ] Normal sin lectura no avanza. Inaccesible sin motivo no avanza y no permite lectura. Dañado sin descripción no avanza; dañado con la lectura vacía sí avanza.
- [ ] Al volver de paso-2 a paso-1 y regresar, los datos siguen.
- [ ] Pídeme probar todos los casos anteriores.

## Al terminar
Actualiza MEMORY.md, escribe la explicación para la defensa y sugiere el mensaje de commit.