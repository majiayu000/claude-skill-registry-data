---
name: 07-borrador
description: Úsala cuando el estudiante pida la skill 07 o el requisito R8 (continuar o descartar un registro interrumpido). Al abrir la app con un borrador pendiente, ofrece continuar o descartar, y al continuar lleva al paso donde quedó conservando lo escrito.
---

# Skill 07: Continuar o descartar el registro (R8)

## Lee antes
docs/CONTRATO.md secciones 1, 3, 5 y 6 (R8). Antes de modificarlos, lee src/store/draft.ts, src/store/session.ts, src/app/_layout.tsx, src/app/(tecnico)/_layout.tsx, src/services/photos.ts y las pantallas de src/app/(tecnico)/lectura/. Si existen ADR-001 y ADR-004 en docs/adr/, léelos.

## Instala
Nada.

## Crea o modifica
1. src/store/draft.ts: exporta el selector `selectHasDraft = (s) => s.meterCode !== null`. Comprueba que `clearDraft` reinicie TODOS los campos (meterCode, meter, step, valores, foto, clientId y, si existe, editingClientId) y que `hasHydrated` pase a true al terminar de hidratar.
2. src/app/(tecnico)/lectura/paso-2.tsx: sincroniza el formulario con el borrador en CADA cambio de valor (con la suscripción `watch` de react-hook-form dentro de un useEffect), no solo al pulsar "Continuar". Así lo escrito sobrevive aunque la app se cierre antes de continuar. Verifica que paso-1 guarde el estado al elegirlo y que paso-3 guarde la foto al tomarla.
3. src/services/drafts.ts: `discardDraft(db)`:
   - Si el borrador tiene photoUri y NO es una corrección: borra el archivo con deletePhoto.
   - Si existe `editingClientId` (skill 06b): relee la fila con getReadingByClientId; borra la foto del borrador SOLO si es distinta de la foto de esa fila. Si el store no tiene `editingClientId`, ignora esta parte.
   - Al final llama clearDraft().
4. src/components/ResumeDraftPrompt.tsx: componente sin interfaz que:
   - Espera a que draft.hasHydrated sea true.
   - Una sola vez por apertura de la app (bandera a nivel de módulo, no persistida), si selectHasDraft es true, muestra `Alert.alert` con `cancelable: false`: título "Registro sin terminar", mensaje con el código del medidor y el paso, y los botones "Descartar" (pide una segunda confirmación y llama discardDraft) y "Continuar".
   - "Continuar" reconstruye la pila para que el botón atrás funcione paso a paso: con `useRouter` hace push de /lectura/paso-1 hasta /lectura/paso-N, donde N es el paso guardado ANTES de empezar a navegar (guárdalo en una variable local). Verifica en la documentación de Expo Router el comportamiento de varios push seguidos y ajusta si hace falta.
5. src/app/(tecnico)/_layout.tsx: renderiza <ResumeDraftPrompt /> sin cambiar la protección de sesión del layout raíz.
6. src/app/(tecnico)/lectura/_layout.tsx: agrega en el encabezado un botón "Descartar" que pide confirmación, llama discardDraft y vuelve a "/" con replace.
7. docs/CONTRATO.md: agrega `selectHasDraft`, `src/services/drafts.ts` y `ResumeDraftPrompt.tsx`. Avísame.

## Reglas
- No navegar al paso pendiente antes de que el borrador haya hidratado.
- Todo borrador se guarda en el store; no usar parámetros de ruta para guardar el paso.
- No tocar src/db salvo para leer con funciones que ya existen. No enviar nada a MockAPI.
- Estilos solo desde src/theme/tokens.ts.

## Checklist
- [ ] npx tsc --noEmit sin errores.
- [ ] Ninguna dependencia nueva.
- [ ] Escribo una lectura en paso-2 SIN pulsar "Continuar", quito la app de recientes y la abro: aparece la pregunta; "Continuar" me deja en paso-2 con lo que escribí.
- [ ] Desde ahí, atrás va a paso-1 y luego a la pantalla principal, sin perder datos.
- [ ] En paso-3 con foto tomada, cierro y abro: "Continuar" me deja en paso-3 con la foto visible, y atrás va a paso-2 con los datos.
- [ ] "Descartar" (con confirmación) limpia el borrador, el siguiente registro empieza vacío y el archivo de la foto se borró.
- [ ] Sin borrador, al abrir la app no aparece ninguna pregunta.
- [ ] La pregunta aparece una vez por apertura, no cada vez que vuelvo a la pantalla principal.
- [ ] La sesión del técnico sigue persistiendo.
- [ ] Pídeme probar todos los casos anteriores.

## Al terminar
Actualiza MEMORY.md, escribe la explicación para la defensa y sugiere el mensaje de commit.