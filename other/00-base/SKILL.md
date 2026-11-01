---
name: 00-base
description: Úsala cuando el estudiante pida la skill 00 o la base del proyecto. Prepara tokens de tema, configuración, tipos, inicialización de SQLite y el layout raíz. Se ejecuta una sola vez, antes de las skills de requisitos.
---

# Skill 00: Base

## Lee antes
docs/CONTRATO.md secciones 1, 3, 4 y 5. ADR-001 y ADR-002 en docs/adr/ (si falta alguno, avísame). Si un ADR y el contrato difieren, manda el contrato (por ejemplo, la tabla se llama `readings`).

## Instala
- expo-sqlite, con `npx expo install`. Nada más.

## Crea o modifica
- tsconfig.json: comprueba que exista el alias `@/*` apuntando a `./src/*`; si falta, agrégalo.
- src/theme/tokens.ts: colores, espaciados, radios y tamaños de fuente neutros, exportados como constantes.
- src/constants/config.ts: URL base de MockAPI (contrato sección 4).
- src/types/index.ts: los tipos y DTOs de las secciones 4 y 5 del contrato, tal cual.
- src/db/init.ts: función idempotente que ejecuta el SQL de la sección 5 del contrato.
- src/app/_layout.tsx: Stack raíz que inicializa la base al arrancar. Verifica en la documentación del SDK 57 cómo hacerlo (SQLiteProvider con onInit o apertura manual) y usa la forma recomendada.
- src/app/index.tsx: pantalla mínima de prueba que muestre "Base lista".

## Reglas
- El SQL queda idéntico al del contrato, sin columnas extra.
- No crear rutas ni carpetas de otras skills.
- No agregar librerías de estilos.

## Checklist
- [ ] npx tsc --noEmit sin errores.
- [ ] Solo se instaló expo-sqlite.
- [ ] El SQL coincide con la sección 5 del contrato.
- [ ] El alias `@/` funciona en un import.
- [ ] Pídeme abrir la app para confirmar que arranca y muestra "Base lista".

## Al terminar
Actualiza MEMORY.md, escribe la explicación para la defensa y sugiere el mensaje de commit.