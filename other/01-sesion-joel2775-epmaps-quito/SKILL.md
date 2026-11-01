---
name: 01-sesion
description: Úsala cuando el estudiante pida la skill 01 o el requisito R1 (identificación del técnico y sesión persistente). Crea el login con usuarios quemados, el store de sesión persistido y las rutas protegidas.
---

# Skill 01: Sesión persistente (R1)

## Lee antes
docs/CONTRATO.md secciones 1, 3 y 6 (R1). Si existen ADR-001 y ADR-004 en docs/adr/, léelos; si no, manda el contrato.

## Instala
- zustand con `npm install zustand`. Nada más.
- Persistencia: verifica en la documentación del SDK 57 si `expo-sqlite/kv-store` sirve como storage de `persist` (con createJSONStorage). Si sirve, úsalo: no agrega dependencias. Si no sirve, NO instales AsyncStorage: avísame.

## Crea o modifica
- src/constants/tecnicos.ts: lista fija de técnicos {code, password, name}. Usa TEC-001 / 1234 y TEC-002 / 5678.
- src/store/session.ts: Zustand con persist. Estado: { employeeCode, hasHydrated, login(code, password): boolean, logout() }. Persiste solo employeeCode (partialize). hasHydrated pasa a true al terminar de hidratar.
- src/app/login.tsx: formulario con useState (no uses react-hook-form ni zod todavía). Muestra error si las credenciales no coinciden. Al entrar, va a "/".
- src/app/(tecnico)/_layout.tsx: Stack del grupo del técnico.
- src/app/(tecnico)/index.tsx: mueve aquí el contenido de src/app/index.tsx y borra ese archivo para no duplicar la ruta "/". Muestra el código del empleado y un botón "Cerrar sesión".
- src/app/_layout.tsx: conserva el SQLiteProvider. Mientras hasHydrated sea false no navegues (pantalla de carga mínima). Luego protege las rutas: sin sesión va a /login; con sesión, al grupo (tecnico). Verifica en la documentación del SDK 57 el mecanismo recomendado (Stack.Protected o redirección) y úsalo.
- docs/CONTRATO.md sección 5: agrega `hasHydrated` al store de sesión y avísame.

## Reglas
- Guardar solo employeeCode, nunca la clave.
- Estilos solo desde src/theme/tokens.ts.
- No crear otras rutas ni tocar src/db.

## Checklist
- [ ] npx tsc --noEmit sin errores.
- [ ] Solo zustand como dependencia nueva.
- [ ] Credenciales incorrectas muestran error y no entran.
- [ ] Pídeme probar: iniciar sesión, quitar la app de recientes y abrirla: sigue identificado.
- [ ] Cerrar sesión devuelve a /login y vuelve a pedir código y clave.
- [ ] Con sesión activa, al abrir la app no se ve un parpadeo de /login.

## Al terminar
Actualiza MEMORY.md, escribe la explicación para la defensa y sugiere el mensaje de commit.