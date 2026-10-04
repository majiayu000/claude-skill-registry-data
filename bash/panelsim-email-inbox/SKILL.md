---
name: panelsim-email-inbox
description: >
  PANELSIM — bandeja multi-cuenta (repo conexion-cuentas-email-agentes-bmc): sync IMAP,
  clasificación, reporte PANELSIM-ULTIMO-REPORTE.md, borradores con aprobación. Usar cuando
  el usuario pide PANELSIM y correo, actualizar bandeja, resumen de mails, estado del inbox,
  panelsim-update, o consultas sobre emails operativos BMC.
---

# PANELSIM — Email inbox (multi-cuenta)

Skill **canónica** para que **PANELSIM / SIM** tenga un procedimiento **cerrado y repetible** para consultar correos sin adivinar rutas. El código vive en un **repo hermano**; esta skill define **cómo resolver la ruta**, **qué ejecutar**, **qué leer** y **qué hacer si falta config**.

---

## Cuándo usar (invocación)

- Frases como: “PANELSIM actualizame el correo”, “qué hay en la bandeja”, “resumen de mails”, “estado inbox”, “correos últimos días”, “prioridades del mail”.
- Cualquier tarea donde el usuario quiera **datos reales de IMAP** ya clasificados y reportados.

**No usar** para inventar contenido de correos sin haber corrido el sync y leído los artefactos.

---

## Resolución de la ruta del repo de correo (orden estricto)

1. **`BMC_EMAIL_INBOX_REPO`** (variable de entorno): si está definida, es la ruta absoluta al repo `conexion-cuentas-email-agentes-bmc`. El agente puede leerla con `echo $BMC_EMAIL_INBOX_REPO` en shell o asumirla si el usuario la configuró en el sistema / Cursor.

2. **Raíz del workspace multi-root**: si existe una carpeta cuyo nombre es exactamente **`conexion-cuentas-email-agentes-bmc`**, usar esa ruta como `EMAIL_REPO`.

3. **Hermano de Calculadora-BMC** (layout típico de Matias): si el workspace solo tiene `Calculadora-BMC`, construir:
   - `EMAIL_REPO = <padre de Calculadora-BMC>/conexion-cuentas-email-agentes-bmc`
   - Ejemplo: `.../Panelin calc loca/Calculadora-BMC` → `.../Panelin calc loca/conexion-cuentas-email-agentes-bmc`.

4. Si **no** se encuentra el repo: **no inventar correos**. Decir al usuario que agregue la carpeta con **File → Add Folder to Workspace** o que defina `BMC_EMAIL_INBOX_REPO`, y enlazar esta skill.

---

## Configuración inicial (una vez — humano)

En `EMAIL_REPO` (el repo de correo, no Calculadora-BMC):

```bash
cd "$EMAIL_REPO"
npm install
cp .env.example .env
cp config/accounts.example.json config/accounts.json
cp config/classification.example.json config/classification.json
cp config/reports.example.json config/reports.json
```

- Completar **`config/accounts.json`**: `host`, `port`, `user`, `passwordEnv` por casilla; `daysBack` (default 30).
- Completar **`.env`**: una variable por cada `passwordEnv` (contraseñas de aplicación IMAP).
- Ajustar **`config/classification.json`** cuando quieras reglas de categorías.
- Opcional: **`config/reports.json`** — título, secciones del Markdown, límites de detalle y orden de tablas (ver README del repo de correo).

**Nunca** commitear `.env` ni datos bajo `data/`.

---

## Comando único que debe ejecutar el agente (sync)

Si el usuario quiere **sesión completa** (planillas + correo + API + informe por áreas), desde la **raíz de Calculadora-BMC**:

```bash
npm run panelsim:session
```

(Ver `AGENTS.md` y `docs/team/panelsim/AGENT-SIMULATOR-SIM.md` §5.1 — opción A.)

**Solo bandeja de correo** (sin tocar el resto): desde la **raíz de Calculadora-BMC**:

```bash
npm run panelsim:email-ready
```

Resuelve `EMAIL_REPO` igual que `scripts/resolve-email-inbox-repo.sh` / `BMC_EMAIL_INBOX_REPO`, instala dependencias del repo de correo si hace falta, y ejecuta `panelsim-update`.

Ventana opcional (ej. últimos 5 días):

```bash
npm run panelsim:email-ready -- --days 5
```

**Alternativa** (si ya estás en `EMAIL_REPO`): `npm run panelsim-update` (mismos flags `--days`).

Equivale a: fetch IMAP + clasificar + generar reporte.

### Artefactos que debe leer PANELSIM tras éxito

| Archivo (relativo a `EMAIL_REPO`) | Uso |
|-------------------------------------|-----|
| `data/reports/PANELSIM-ULTIMO-REPORTE.md` | **Principal:** resumen legible por categoría |
| `data/reports/PANELSIM-STATUS.json` | Conteos `byCategory` y `byAccount`, **`syncHealth`** por casilla (`ok` / `auth_error` / `network` / …), fechas, rutas absolutas |
| (opcional) línea stdout `PANELSIM_EMAIL_RESULT:{...}` | Mismo resumen en JSON |

No cargar en el chat el **`data/snapshot-latest.json` completo** salvo petición explícita (es grande).

### Bridge a CRM (repo Calculadora-BMC)

Con snapshot ya generado y la API BMC arriba (`npm run start:api` o `BMC_API_BASE` apuntando a Cloud Run), se puede enviar correos **clasificados como ventas** a `POST /api/crm/ingest-email` vía:

```bash
cd /ruta/Calculadora-BMC
npm run email:ingest-snapshot -- --dry-run --limit 5
```

Dedupe en `.email-ingest/` (gitignored). Ver `AGENTS.md` (`email:ingest-snapshot`) y `server/lib/emailSnapshotIngest.js`.

### Resumen PANELSIM vía API (GPT / Thunderbird mismo IMAP)

Con la API BMC local (o host que tenga acceso al disco del repo IMAP) y **`API_AUTH_TOKEN`** configurado:

- **`GET /api/email/panelsim-summary`** — Header `Authorization: Bearer <API_AUTH_TOKEN>`. Devuelve JSON con `status` (PANELSIM-STATUS), `reportPreview` (Markdown del último reporte, truncable con `?reportMaxChars=`), y `workflow` (comandos sugeridos). **No** sustituye leer el `.md` en el repo si la API no ve el filesystem (p. ej. Cloud Run sin volumen).
- **`POST /api/email/draft-outbound`** — Borrador asunto/cuerpo para **proveedor** o **cliente**; **no envía** correo (copiar a Thunderbird).

Doc: [`docs/team/panelsim/EMAIL-GPT-THUNDERBIRD-WORKFLOW.md`](../../../docs/team/panelsim/EMAIL-GPT-THUNDERBIRD-WORKFLOW.md).

---

## Respuesta al usuario (formato)

1. Breve **estado**: cuántos mensajes, rango de fechas si aparece en STATUS.
2. **Por categoría** (tabla o bullets según `PANELSIM-ULTIMO-REPORTE.md` / STATUS).
3. **3–5 prioridades** inferidas del reporte (sin alucinar fuera del texto leído).
4. **Privacidad:** no pegar cuerpos largos ni datos sensibles innecesarios.

Si el sync **falla**: copiar el error, indicar si falta `config/accounts.json`, `.env`, red, o credencial IMAP.

---

## Borradores y envío

- **Responder** un hilo: usar en `EMAIL_REPO` → `npm run draft -- --match <índice|messageId> --instruction "..."` — requiere interacción de aprobación del usuario para guardar.
- **No** enviar correo automáticamente desde esta skill (v0.1 del repo de correo no incluye SMTP por defecto).

---

## Resumen con LLM (opcional)

Si en el `.env` de `EMAIL_REPO` existe `OPENAI_API_KEY`:

```bash
npm run summary -- --instruction "Prioridades y riesgos de la bandeja"
```

Leer el `data/reports/resumen-*.md` generado y sintetizar para el usuario.

---

## Documentación duplicada (repo de correo)

- `docs/PANELSIM-EMAIL-PROMPT.md` en el repo de correo — mismo flujo; esta skill es la versión **orientada a agente** dentro de Calculadora-BMC.

---

## Checklist rápido para el agente

1. Resolver `EMAIL_REPO` (sección arriba).
2. `test -f "$EMAIL_REPO/package.json"` o listar directorio; si falla → avisar al usuario.
3. Ejecutar `npm run panelsim-update` con `working_directory` = `EMAIL_REPO`.
4. Leer `data/reports/PANELSIM-ULTIMO-REPORTE.md` (y STATUS si hace falta).
5. Responder en español según “Respuesta al usuario”.
