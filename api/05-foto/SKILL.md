---
name: 05-foto
description: Úsala cuando el estudiante pida la skill 05 o el requisito R7 (foto del medidor, permiso de cámara y conservación permanente de la imagen). Agrega la captura de foto al paso 3 del registro.
---

# Skill 05: Foto del medidor (R7)

## Lee antes
docs/CONTRATO.md secciones 1, 3, 5 y 6 (R7). Si existe ADR-007 en docs/adr/, léelo; si no, manda el contrato.

## Instala
- expo-image-picker y expo-file-system con `npx expo install`. Nada más. Sin expo-camera, sin Base64.
- Verifica en la documentación del SDK 57:
  - La forma vigente de `launchCameraAsync` (incluida la opción `mediaTypes`) y de pedir el permiso de cámara con su campo `canAskAgain`.
  - La API NUEVA de expo-file-system (`File`, `Directory`, `Paths`) para copiar un archivo a una carpeta permanente de documentos. No uses la API antigua `documentDirectory` salvo que la documentación diga que sigue vigente.
  - Cómo declarar el plugin de expo-image-picker en app.json con un texto de permiso de cámara en español, y agrégalo.

## Crea o modifica
- src/services/photos.ts:
  - `ensureCameraPermission()`: devuelve "granted", "denied" (se puede volver a pedir) o "blocked" (canAskAgain es false).
  - `takePhoto(clientId)`: abre la cámara con calidad media (quality 0.5), y si el técnico no cancela, copia el archivo a una carpeta permanente "evidencias" dentro de los documentos de la app con el nombre `evidencia-<clientId>.jpg`. Devuelve la ruta permanente, o null si canceló. Nunca devuelve la ruta temporal.
  - `deletePhoto(uri)`: borra el archivo si existe (sin lanzar error si no existe).
- src/store/draft.ts: agrega `clientId` (se genera UNA vez en startDraft con Date.now() y un sufijo aleatorio corto, sin librerías), la acción `setPhotoUri(uri | null)` y persiste `photoUri` y `clientId`. Al cambiar de foto, borra la anterior con deletePhoto.
- src/app/(tecnico)/lectura/paso-3.tsx: conserva el resumen y agrega la sección de foto:
  - Etiqueta "Foto obligatoria" o "Foto opcional" según `isPhotoRequired` de src/domain/consumption.ts.
  - Botón "Tomar foto" (o "Cambiar foto") y vista previa con Image.
  - Si el permiso es "denied": explica en un mensaje por qué se necesita ("La foto sirve como respaldo de la lectura ante reclamos") y deja reintentar.
  - Si es "blocked": mismo mensaje y un botón "Abrir ajustes" con `Linking.openSettings()` (viene con React Native).
  - Si la foto es opcional y el permiso no se concede, el técnico puede continuar sin foto. Si es obligatoria y no hay foto, muestra "Falta la foto obligatoria".
  - Muestra un estado "Listo para guardar" cuando no falte nada. No hay botón de guardar todavía (skill 06).
  - Mientras desarrollamos, muestra en texto pequeño la ruta de la foto guardada (se quitará en la skill 09).
- app.json: plugin de expo-image-picker con cameraPermission en español.
- docs/CONTRATO.md sección 5: agrega `clientId` y `setPhotoUri` al borrador, y la nota "la skill 06 usa draft.clientId al guardar". Avísame.

## Reglas
- La foto nunca queda en la carpeta temporal ni se guarda en Base64.
- No tocar src/db ni el envío. Estilos solo desde src/theme/tokens.ts.
- No borrar la foto al descartar el borrador todavía: eso se resuelve en la skill 07.

## Checklist
- [ ] npx tsc --noEmit sin errores.
- [ ] Solo expo-image-picker y expo-file-system como dependencias nuevas.
- [ ] MED-000001, normal, lectura 182: la foto es opcional y se puede continuar sin ella.
- [ ] Lectura 183: la foto es obligatoria y aparece "Falta la foto obligatoria" hasta tomarla.
- [ ] Estado dañado con lectura vacía: foto obligatoria.
- [ ] Al negar el permiso: aparece la explicación; con foto opcional se puede continuar; con foto obligatoria no.
- [ ] La ruta mostrada NO contiene "cache" y la imagen se ve en la vista previa al volver atrás y regresar.
- [ ] Pídeme probar los casos anteriores en el teléfono.

## Al terminar
Actualiza MEMORY.md, escribe la explicación para la defensa y sugiere el mensaje de commit.