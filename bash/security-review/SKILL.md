---
name: security-review
description: Revisar seguridad de un área (secrets|android-permissions|components|location|privacy|logging|ci) con findings por severidad, sin editar; para dependencias usa dependency-maintenance.
argument-hint: "[secrets|android-permissions|components|location|privacy|logging|ci]"
allowed-tools: Read, Grep, Glob
---

# security-review

Revisión de solo lectura del área `$ARGUMENTS`. Checklist por área: [checklist.md](checklist.md).

## Cuándo usarla
- Antes de cerrar un cambio que toca migraciones Room, secretos/firma, permisos del manifest, componentes exportados, el servicio de ubicación, trazas grabadas, logs o CI.
- Revisión periódica de un área concreta.

## Cuándo NO usarla
- Buscar secretos en árbol e historial → usa `security-secret-scan`.
- Licencias o dependencias → usa `dependency-maintenance`.
- Arreglar los findings → agente de dominio correspondiente (esta skill no modifica nada).

## Precondiciones
- Leídos `CLAUDE.md` y `docs/DECISIONES.md` (offline por defecto, sin backend propio, datos del usuario solo en el móvil).
- Valor de `$ARGUMENTS` válido. Si falta: inferir las áreas de los archivos cambiados (que aporta el llamador, p. ej. `git diff --name-only`); si no hay cambios, pedir el área y parar.
- Sin Bash: no lee `.env*`, `*.pem`, `*.key`, `*.jks`, `*.keystore`, `local.properties` ni `~/.rallycopilot/*` (solo cita su nombre).

## Pasos
1. Acotar el alcance con la tabla de rutas y abrir solo esos archivos.
2. Recorrer las filas del área en [checklist.md](checklist.md); cada incumplimiento es un finding con la severidad de la fila (subir o bajar solo con motivo escrito).
3. Verificar con `Grep` antes de afirmar (p. ej. `using \(true\)`, `exported="true"`, `Log\.`, `allowBackup`). Citar `archivo:línea` reales.
4. Si el hallazgo implica un secreto: reportar archivo, línea y tipo; **nunca** el valor ni fragmentos.
5. BLOCKER/HIGH en secrets o release, o cambio sensible → recomendar revisión por un revisor de seguridad [opus] con las rutas.
6. Cerrar con totales por severidad y dudas (lo no verificable se marca `VERIFICAR`).

| Área | Rutas |
|------|-------|
| secrets | `.gitignore`, `app/build.gradle.kts`, `scripts/**`, `.claude/settings.json` |
| android-permissions, components | `app/src/main/AndroidManifest.xml` |
| location | servicio de ubicación, repositorio de posiciones y grabación de tramos en `app/src/main/**` |
| privacy, logging | `app/**`, `motor/**` |
| ci | `.github/workflows/**` |

## Validaciones / tests
- Cada `archivo:línea` citado existe (releer la línea) y ningún finding contiene un valor de secreto.
- Formato, uno por línea, ordenado BLOCKER > HIGH > MEDIUM > LOW, máx. 20: `SEVERIDAD | archivo:línea | problema | corrección propuesta`
- Sin hallazgos → `Sin findings` más lo comprobado.

## Definition of Done
- [ ] Todas las filas del área revisadas; findings en el formato indicado.
- [ ] Ningún secreto reproducido; ningún archivo modificado.
- [ ] Cambios sensibles derivados a revisión [opus].
- [ ] Riesgos aceptados anotados en docs/ESTADO.md por el agente principal.

## Docs a actualizar
- Ninguno desde esta skill (solo lectura); el agente principal registra riesgos en docs/ESTADO.md (skill `session-handoff`).
