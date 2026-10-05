---
name: deploy-production
description: Workflow unificato per deploy Docker+Traefik su VPS. Supporta deploy backend-only, frontend-only, full, e no-cache per tutti i progetti con Docker Compose + Traefik + Let's Encrypt.
---

# Deploy Production Skill

## Quando usare questa skill
- Deploy di qualsiasi progetto su VPS Linux con Docker Compose
- Troubleshooting container Docker in produzione
- Setup nuovo progetto su VPS esistente
- Migrazione tra VPS

## Infrastruttura VPS (esempio di organizzazione multi-VPS)

| Ruolo | Provider tipo | Shell di default | Note |
|-------|---------------|------------------|------|
| **VPS-A** (es. produzione principale) | Provider economico Europa | spesso `fish` su immagini default — usare `bash -c` | Configurare SSH su porta non standard (es. 2222) |
| **VPS-B** (es. produzione secondaria) | Provider premium Europa | `bash` | SSH key + porta non standard |
| **Edge** (es. IoT / dev locale) | Raspberry Pi / NUC | `bash` | LAN o tunnel SSH |

> Adatta la tabella al tuo setup. La logica della skill è agnostica rispetto al provider.

## REGOLA FONDAMENTALE

```
deploy.sh è LOCALE (sul PC Windows), NON sul VPS!
```

## Workflow Deploy Standard

### 1. Pre-deploy: Commit e Push

```bash
# SEMPRE: modifiche devono essere su Git PRIMA del deploy
cd D:/progetti/PROGETTO
git add -A && git commit -m "fix: descrizione" && git push origin main
```

### 2. Scelta Flag Deploy

```bash
# Solo backend (PHP/Node.js) — 15 secondi
./deploy.sh --backend-only

# Solo frontend (Vue/React rebuild) — 30-60 secondi
./deploy.sh --frontend-only

# Full deploy (entrambi) — 1-2 minuti
./deploy.sh

# Nuove dipendenze (composer/npm install) — 3-5 minuti
./deploy.sh --no-cache

# REGOLA: NON usare --no-cache per semplici modifiche codice!
```

### 3. Post-deploy: Verifica

```bash
# VPS_PORT="<porta-ssh>" (es. 22 o porta custom del VPS)

# Provider A (fish shell — SEMPRE bash -c)
ssh -p "$VPS_PORT" root@<VPS_A_IP> "bash -c 'cd /root/PROGETTO && docker compose ps'"

# Provider B (bash diretto)
ssh -p "$VPS_PORT" root@<VPS_B_IP> "cd /opt/PROGETTO && docker compose ps"

# Verifica logs
ssh -p "$VPS_PORT" root@VPS_IP "bash -c 'docker logs CONTAINER --tail 50'"

# Test endpoint
curl -s https://api.DOMINIO.com/api/health
```

## Docker Compose Template

```yaml
version: "3.8"

services:
  traefik:
    image: traefik:v3.1
    command:
      - "--api.insecure=true"
      - "--providers.docker=true"
      - "--providers.docker.exposedbydefault=false"
      - "--entrypoints.web.address=:80"
      - "--entrypoints.websecure.address=:443"
      - "--certificatesresolvers.letsencrypt.acme.httpchallenge.entrypoint=web"
      - "--certificatesresolvers.letsencrypt.acme.email=${ACME_EMAIL}"
      - "--certificatesresolvers.letsencrypt.acme.storage=/letsencrypt/acme.json"
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - letsencrypt:/letsencrypt

  backend:
    build: ./backend
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.backend.rule=Host(`api.${DOMAIN}`)"
      - "traefik.http.routers.backend.entrypoints=websecure"
      - "traefik.http.routers.backend.tls.certresolver=letsencrypt"
    env_file: ./backend/.env
    depends_on:
      - db

  frontend:
    build:
      context: ./frontend
      args:
        VITE_API_URL: "https://api.${DOMAIN}/api"
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.frontend.rule=Host(`${DOMAIN}`) || Host(`www.${DOMAIN}`)"
      - "traefik.http.routers.frontend.entrypoints=websecure"
      - "traefik.http.routers.frontend.tls.certresolver=letsencrypt"

  db:
    image: mysql:8.0  # o postgres:16 o mongo:7
    volumes:
      - db-data:/var/lib/mysql
    environment:
      MYSQL_ROOT_PASSWORD: ${DB_ROOT_PASSWORD}
      MYSQL_DATABASE: ${DB_NAME}

volumes:
  letsencrypt:
  db-data:
```

## deploy.sh Template

```bash
#!/bin/bash
set -e

# Configurazione
VPS_HOST="root@<VPS_A_IP>"
VPS_PORT="<porta-ssh>"
PROJECT_DIR="/root/progetto"
SSH_CMD="ssh -p $VPS_PORT $VPS_HOST"

# Parse flags
BACKEND_ONLY=false
FRONTEND_ONLY=false
NO_CACHE=false

for arg in "$@"; do
    case $arg in
        --backend-only) BACKEND_ONLY=true ;;
        --frontend-only) FRONTEND_ONLY=true ;;
        --no-cache) NO_CACHE=true ;;
    esac
done

echo "🚀 Deploy in corso..."

# Pull latest code
$SSH_CMD "bash -c 'cd $PROJECT_DIR && git pull origin main'"

# Build e restart
if $NO_CACHE; then
    $SSH_CMD "bash -c 'cd $PROJECT_DIR && docker compose build --no-cache && docker compose up -d'"
elif $BACKEND_ONLY; then
    $SSH_CMD "bash -c 'cd $PROJECT_DIR && docker compose up -d --build backend'"
elif $FRONTEND_ONLY; then
    $SSH_CMD "bash -c 'cd $PROJECT_DIR && docker compose up -d --build frontend'"
else
    $SSH_CMD "bash -c 'cd $PROJECT_DIR && docker compose up -d --build'"
fi

# Laravel: config cache (se applicabile)
if ! $FRONTEND_ONLY; then
    $SSH_CMD "bash -c 'cd $PROJECT_DIR && docker compose exec -T backend php artisan config:cache 2>/dev/null || true'"
fi

echo "✅ Deploy completato!"
```

## Troubleshooting

### Container non parte
```bash
# Controlla logs
docker logs CONTAINER --tail 100

# Controlla risorse
docker stats --no-stream

# Ricostruisci da zero
docker compose down && docker compose up -d --build
```

### Errore 502 Bad Gateway
```bash
# Backend non raggiungibile da Traefik
# 1. Verifica che il container backend sia running
docker ps | grep backend

# 2. Verifica network Docker
docker network inspect PROGETTO_default

# 3. Verifica labels Traefik
docker inspect CONTAINER | grep traefik
```

### SSL non funziona
```bash
# Verifica acme.json
ls -la /letsencrypt/acme.json

# Se corrotto, rigenerare
rm /letsencrypt/acme.json
docker compose restart traefik
# Aspettare 1-2 minuti per nuovo certificato
```

### Frontend non aggiornato
```
Le variabili VITE_* sono BAKED nel bundle durante build.
Modifiche .env frontend richiedono: ./deploy.sh --frontend-only
Solo git pull NON basta per il frontend!
```
