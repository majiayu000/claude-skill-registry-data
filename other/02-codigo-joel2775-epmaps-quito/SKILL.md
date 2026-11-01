---
name: 02-codigo
description: Úsala cuando el estudiante pida la skill 02 o el requisito R2 (validación del código de medidor MED-######). Crea el esquema Zod y la pantalla de búsqueda que valida antes de cualquier consulta.
---

# Skill 02: Validación del código del medidor (R2)

## Lee antes
docs/CONTRATO.md secciones 1, 3 y 6 (R2). Si existe ADR-006 en docs/adr/, léelo; si no, manda el contrato.

## Instala
- zod con `npm install zod`. Nada más (@hookform/resolvers se instala en la skill 04).
- Verifica en la documentación de la versión instalada de Zod cómo se declara el mensaje de error de una regex.

## Crea o modifica
- src/schemas/meter.ts: `meterCodeSchema` con la regex `/^MED-\d{6}$/` exacta, sin transformaciones. Mensaje: "Código inválido. Use MED- seguido de 6 dígitos."
- src/app/(tecnico)/buscar.tsx: TextInput (autoCapitalize="characters", sin autocorrección) y botón "Consultar". Al pulsar, valida con `safeParse`. Si falla, muestra el mensaje y no hace nada más. Si pasa, muestra por ahora el texto "Código válido: <código>" (la consulta real llega en la skill 03).
- src/app/(tecnico)/index.tsx: agrega un botón "Nueva lectura" que navega a /buscar. No toques más.
- docs/CONTRATO.md sección 3: agrega `src/schemas/meter.ts` con `meterCodeSchema` y avísame.

## Reglas
- No crear services/api.ts ni llamar a MockAPI todavía: el código inválido nunca debe llegar a ninguna llamada.
- No usar react-hook-form todavía.
- Estilos solo desde src/theme/tokens.ts.

## Checklist
- [ ] npx tsc --noEmit sin errores.
- [ ] Solo zod como dependencia nueva.
- [ ] Prueba con: "", "MED-123", "MED-0000011", "MED000001", "med-000001" y "MED-00000A": todos muestran error.
- [ ] "MED-000001" muestra "Código válido".
- [ ] Pídeme probar en la app los casos anteriores.

## Al terminar
Actualiza MEMORY.md, escribe la explicación para la defensa y sugiere el mensaje de commit.