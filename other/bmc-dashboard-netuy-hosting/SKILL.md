---
name: bmc-dashboard-netuy-hosting
description: >
  Guía el deploy del BMC Dashboard en un VPS de Netuy (Uruguay): requisitos,
  subida del proyecto, .env, PM2/systemd, nginx + HTTPS. Usar cuando pidan
  hostear el dashboard en Netuy, desplegar en Netuy, configurar el dashboard
  en mi servidor Netuy, o deploy VPS Uruguay. Requiere VPS (no hosting compartido).
---

# BMC Dashboard — Hosting en Netuy (VPS)

Guía el despliegue del BMC Dashboard (Sheets API + UI) en un **VPS de Netuy** (netuy.net). Los datos quedan en Uruguay (Tier III, Ley 18.331).

## Cuándo usar este skill

- Usuario pide **hostear el dashboard en Netuy**, **desplegar en Netuy**, **poner el dashboard en mi servidor Netuy**.
- Usuario tiene o va a contratar un **VPS** en Netuy (no hosting compartido; en compartido no se puede correr Node).

## Requisitos en el VPS Netuy

- **Node.js 18+** (instalar con `nvm` o paquete de la distro).
- **Acceso SSH** al VPS.
- (Opcional) Dominio apuntando al VPS y **certbot** para HTTPS.

## Pasos que el skill orquesta

1. **Confirmar tipo de host:** Si el usuario tiene solo hosting compartido (cPanel), indicar que debe usar **VPS** Netuy o seguir con ngrok desde local. Si tiene VPS, continuar.

2. **Subir el proyecto al VPS:**
   - **Opción A:** En el VPS, `git clone` del repo + `npm install`.
   - **Opción B:** En local, crear tarball con `package.json`, `package-lock.json`, `docs/bmc-dashboard-modernization/sheets-api-server.js`, `docs/bmc-dashboard-modernization/dashboard`; subir y descomprimir en el VPS; en la raíz del proyecto ejecutar `npm install`.

3. **Configurar `.env` en el VPS:**
   - `BMC_SHEET_ID` = ID de la hoja de cálculo.
   - `GOOGLE_APPLICATION_CREDENTIALS` = ruta **en el servidor** al archivo JSON de la cuenta de servicio (ej. `/opt/bmc-dashboard/secrets/service-account.json`). El usuario debe subir el `service-account.json` a una ruta segura en el VPS.

4. **Probar:** En el VPS, `npm run bmc-dashboard` (o `node docs/bmc-dashboard-modernization/sheets-api-server.js`). Verificar que el dashboard responda en el puerto configurado (por defecto 3849).

5. **Dejarlo corriendo:** PM2 (`pm2 start ... --name bmc-dashboard`, `pm2 save`, `pm2 startup`) o systemd (servicio `bmc-dashboard.service` con `WorkingDirectory`, `EnvironmentFile`, `ExecStart`). Ver [reference.md](reference.md).

6. **HTTPS (opcional):** Nginx como reverse proxy al puerto 3849 + `certbot --nginx -d tudominio.com`. Ver [reference.md](reference.md).

## Referencia

- **Guía completa:** [docs/bmc-dashboard-modernization/HOSTING-EN-MI-SERVIDOR.md](../../../docs/bmc-dashboard-modernization/HOSTING-EN-MI-SERVIDOR.md).
- **Comandos y ejemplos:** [reference.md](reference.md) en este skill.

## Relación con otros skills

- **bmc-dashboard-one-click-setup** / **bmc-dashboard-setup:** Setup **local** (env, API, dashboard, ngrok). Este skill es para **deploy en VPS Netuy** una vez que el proyecto funciona en local.
- Si el usuario no tiene el dashboard funcionando en local, sugerir primero configurar con bmc-dashboard-setup y luego seguir con este skill para desplegar en Netuy.

## Output esperado

- Lista de pasos numerados con estado (✓/✗ o pendiente).
- Comandos concretos para ejecutar en el VPS (SSH) y, si aplica, en local (tarball).
- Recordatorio de no commitear ni exponer `service-account.json`; subirlo por canal seguro al VPS.
- Si el usuario tiene hosting compartido, mensaje claro: "Para Node necesitás un VPS en Netuy; en compartido usá ngrok o pasá a VPS."
