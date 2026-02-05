---
name: deployment
description: Deployment & preview management. Auto-activates after project build completed. Handles port assignment, PM2 process management, preview URL generation. Keywords "deploy", "preview", "lance", "start project".
allowed-tools: Bash, Read, Write, Edit
---

# Deployment Skill

> **Auto-deployment + Preview URL pour projets buildés**
>
> Inspiré de : Vercel DX, PM2 Best Practices, Zero-Config Deployment

---

## Scope & Activation

**Chargé par:** EXECUTOR agent (après build complété)

**Auto-activé si:**
- `npm run build` success
- Tests E2E passés (TESTER validé)
- User demande "preview", "deploy", "lance projet", "start"
- Frontend + Backend complétés

**Gère:**
- Port assignment unique (évite conflits)
- PM2 process management
- Preview URL generation
- Health checks
- Process monitoring
- .build/context.md update

---

## Architecture Port Assignment

### Règle: 1 Projet = 1 Port PERSISTANT

**Principe clé:** Un projet garde SON port à vie (même après redeploy/restart)

**Base port:** 3001 (3000 réservé dev local)
**Strategy:**
1. Check si projet a déjà un port (dans .env ou PM2)
2. Si OUI → Réutilise ce port (JAMAIS changer)
3. Si NON → Assign prochain port libre

---

### Workflow Complet (PERSISTANCE GARANTIE)

```bash
#!/bin/bash
# get-or-assign-port.sh - Port assignment avec persistance

PROJECT_NAME=$(basename "$PWD")

# ═══════════════════════════════════════════════
# ÉTAPE 1: Check si projet a déjà un port
# ═══════════════════════════════════════════════

# 1a. Check .env (source de vérité)
if [ -f ".env" ] && grep -q "^PORT=" .env; then
  EXISTING_PORT=$(grep "^PORT=" .env | cut -d'=' -f2)
  echo "✅ Port trouvé dans .env: $EXISTING_PORT"
  echo "$EXISTING_PORT"
  exit 0
fi

# 1b. Check PM2 (si process existe déjà)
PM2_PORT=$(pm2 jlist 2>/dev/null | jq -r ".[] | select(.name == \"$PROJECT_NAME\") | .pm2_env.PORT" 2>/dev/null | head -1)

if [ -n "$PM2_PORT" ] && [ "$PM2_PORT" != "null" ]; then
  echo "✅ Port trouvé dans PM2: $PM2_PORT"
  # Save dans .env pour persistance
  echo "PORT=$PM2_PORT" >> .env
  echo "$PM2_PORT"
  exit 0
fi

# ═══════════════════════════════════════════════
# ÉTAPE 2: Aucun port existant → Assign nouveau
# ═══════════════════════════════════════════════

echo "📍 Pas de port existant, assignment nouveau port..."

# Get tous ports utilisés (PM2 + autres projets .env)
USED_PORTS=$(pm2 jlist 2>/dev/null | jq -r '.[] | select(.pm2_env.PORT != null) | .pm2_env.PORT' 2>/dev/null | sort -n)

# Find highest port
HIGHEST_PORT=$(echo "$USED_PORTS" | tail -1)

# Calculate next port
if [ -z "$HIGHEST_PORT" ]; then
  NEXT_PORT=3001  # Premier projet
else
  NEXT_PORT=$((HIGHEST_PORT + 1))
fi

# Save dans .env (PERSISTANCE)
echo "PORT=$NEXT_PORT" >> .env

echo "✅ Nouveau port assigné: $NEXT_PORT"
echo "$NEXT_PORT"
```

---

### Pourquoi Persistance Importante?

**Sans persistance (❌ MAUVAIS):**
```
Projet: task-timer
1er deploy → Port 3001
2ème deploy → Port 3002 (NOUVEAU! Mauvais!)
3ème deploy → Port 3003 (ENCORE NOUVEAU! Chaos!)
```

**Avec persistance (✅ CORRECT):**
```
Projet: task-timer
1er deploy → Port 3001 (assigné)
2ème deploy → Port 3001 (réutilisé)
3ème deploy → Port 3001 (réutilisé)
Toujours: http://89.116.27.88:3001
```

**Avantages:**
- Preview URL stable (bookmarkable)
- Firewall rules simples
- Nginx config persist
- Logs centralisés même port
- User experience cohérente

---

### Script Intelligent (Usage dans Deployment)

```bash
#!/bin/bash
# Deployment workflow avec persistance port

PROJECT_NAME=$(basename "$PWD")

# Get or assign port (SMART)
PORT=$(bash get-or-assign-port.sh)

echo "🔧 Using port: $PORT for $PROJECT_NAME"

# Vérifier .env synchronized
if ! grep -q "^PORT=$PORT" .env 2>/dev/null; then
  # Update .env si désynchronisé
  if grep -q "^PORT=" .env; then
    sed -i "s/^PORT=.*/PORT=$PORT/" .env
  else
    echo "PORT=$PORT" >> .env
  fi
fi

echo "✅ Port verified: $PORT"
```

---

### Port Registry (Alternative Avancée - Optionnel)

**Si besoin tracking centralisé, créer registry:**

```bash
# /var/pm2/port-registry.json (global VPS)
{
  "task-timer": 3001,
  "ecommerce-app": 3002,
  "blog-platform": 3003
}
```

**Update registry:**
```bash
#!/bin/bash
REGISTRY_FILE="/var/pm2/port-registry.json"
PROJECT_NAME=$(basename "$PWD")
PORT=$1

# Create registry if absent
if [ ! -f "$REGISTRY_FILE" ]; then
  echo "{}" | sudo tee "$REGISTRY_FILE" > /dev/null
  sudo chmod 666 "$REGISTRY_FILE"
fi

# Update registry
jq --arg project "$PROJECT_NAME" --argjson port "$PORT" \
  '.[$project] = $port' "$REGISTRY_FILE" > /tmp/registry.tmp
sudo mv /tmp/registry.tmp "$REGISTRY_FILE"

echo "✅ Registry updated: $PROJECT_NAME → $PORT"
```

**Check registry:**
```bash
PROJECT_NAME=$(basename "$PWD")
REGISTRY_PORT=$(jq -r --arg project "$PROJECT_NAME" '.[$project] // empty' /var/pm2/port-registry.json 2>/dev/null)

if [ -n "$REGISTRY_PORT" ]; then
  echo "Found in registry: $REGISTRY_PORT"
fi
```

**Note:** Registry optionnel. `.env` + PM2 suffisent pour 90% cas.

---

## PM2 Process Management

### Phase 1: Install PM2 (si absent)

```bash
# Check PM2 installed globally
if ! command -v pm2 &>/dev/null; then
  echo "📦 Installing PM2..."
  npm install -g pm2

  # Setup startup script (auto-start on reboot)
  pm2 startup

  echo "✅ PM2 installed"
fi
```

---

### Phase 2: Create Ecosystem Config

**ecosystem.config.js (production-ready):**

```bash
PROJECT_NAME=$(basename "$PWD")
PORT=$(grep "^PORT=" .env | cut -d'=' -f2)

cat > ecosystem.config.js <<EOF
module.exports = {
  apps: [{
    name: '$PROJECT_NAME',
    script: 'npm',
    args: 'start',
    cwd: '$PWD',
    env: {
      NODE_ENV: 'production',
      PORT: $PORT
    },
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: '500M',
    error_file: './.pm2/logs/err.log',
    out_file: './.pm2/logs/out.log',
    log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
    merge_logs: true,
    time: true
  }]
}
EOF

echo "✅ ecosystem.config.js créé"
```

**Options explained:**
- `instances: 1` - Single instance (pas cluster mode pour MVP)
- `autorestart: true` - Auto-restart si crash
- `max_memory_restart: '500M'` - Restart si mémoire > 500MB (évite leaks)
- `watch: false` - Pas de hot reload (production)
- Logs dans `.pm2/logs/` (centralisé)

---

### Phase 3: Start PM2 Process

```bash
PROJECT_NAME=$(basename "$PWD")

# Stop si déjà running (redeploy)
if pm2 list | grep -q "$PROJECT_NAME"; then
  echo "⚠️ Process existant détecté, restart..."
  pm2 delete "$PROJECT_NAME" 2>/dev/null
fi

# Start via ecosystem config
pm2 start ecosystem.config.js

# Save config (persist reboot)
pm2 save

echo "✅ PM2 process started: $PROJECT_NAME"
```

---

### Phase 4: Health Check

**Vérifier process démarré correctement:**

```bash
#!/bin/bash

PROJECT_NAME=$(basename "$PWD")
PORT=$(grep "^PORT=" .env | cut -d'=' -f2)

# Wait for process to start (max 10s)
for i in {1..10}; do
  if pm2 list | grep -q "$PROJECT_NAME.*online"; then
    echo "✅ Process online"
    break
  fi
  sleep 1
done

# Check if process is running
if ! pm2 list | grep -q "$PROJECT_NAME.*online"; then
  echo "❌ Process failed to start"
  echo ""
  echo "Logs (last 30 lines):"
  pm2 logs "$PROJECT_NAME" --lines 30 --nostream
  exit 1
fi

# Check HTTP response (wait max 15s)
echo "🔍 Checking HTTP response..."
for i in {1..15}; do
  HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:$PORT 2>/dev/null)

  if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ HTTP 200 OK"
    break
  fi

  if [ $i -eq 15 ]; then
    echo "⚠️ HTTP $HTTP_CODE (expected 200)"
    echo "Preview may not be fully ready yet. Check logs:"
    echo "  pm2 logs $PROJECT_NAME"
  fi

  sleep 1
done
```

---

## Preview URL Generation

### Option A: VPS IP Direct (Default)

```bash
VPS_IP="89.116.27.88"
PORT=$(grep "^PORT=" .env | cut -d'=' -f2)
PROJECT_NAME=$(basename "$PWD")

PREVIEW_URL="http://$VPS_IP:$PORT"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Projet $PROJECT_NAME déployé"
echo ""
echo "Preview URL: $PREVIEW_URL"
echo ""
echo "PM2 Status:"
pm2 describe "$PROJECT_NAME" 2>/dev/null | grep -E "status|uptime|cpu|memory" || pm2 list | grep "$PROJECT_NAME"
echo ""
echo "Commandes utiles:"
echo "  pm2 logs $PROJECT_NAME       # Voir logs"
echo "  pm2 restart $PROJECT_NAME    # Restart"
echo "  pm2 stop $PROJECT_NAME       # Stop"
echo "  pm2 monit                    # Monitoring real-time"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
```

### Option B: Nginx Subdomain (Advanced - Optionnel)

**Si Nginx installé et user veut subdomain:**

```bash
PROJECT_NAME=$(basename "$PWD")
PORT=$(grep "^PORT=" .env | cut -d'=' -f2)

# Check if nginx installed
if command -v nginx &>/dev/null; then
  echo "📝 Creating Nginx config..."

  # Create nginx site config
  sudo tee /etc/nginx/sites-available/$PROJECT_NAME > /dev/null <<EOF
server {
  listen 80;
  server_name $PROJECT_NAME.vps.local;

  location / {
    proxy_pass http://localhost:$PORT;
    proxy_http_version 1.1;
    proxy_set_header Upgrade \$http_upgrade;
    proxy_set_header Connection 'upgrade';
    proxy_set_header Host \$host;
    proxy_cache_bypass \$http_upgrade;
    proxy_set_header X-Real-IP \$remote_addr;
    proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto \$scheme;
  }
}
EOF

  # Enable site
  sudo ln -sf /etc/nginx/sites-available/$PROJECT_NAME /etc/nginx/sites-enabled/

  # Test config
  if sudo nginx -t 2>/dev/null; then
    sudo nginx -s reload
    echo "✅ Nginx configured: http://$PROJECT_NAME.vps.local"
  else
    echo "⚠️ Nginx config error, using direct IP"
  fi
fi
```

---

## Update .build/context.md

**Ajouter section Deployment:**

```bash
PROJECT_NAME=$(basename "$PWD")
PORT=$(grep "^PORT=" .env | cut -d'=' -f2)
VPS_IP="89.116.27.88"
DEPLOY_DATE=$(date "+%Y-%m-%d %H:%M:%S")

# Check if Deployment section exists
if grep -q "## Deployment" .build/context.md 2>/dev/null; then
  # Update existing section
  sed -i '/## Deployment/,/^##/c\
## Deployment\
- Port: '$PORT'\
- PM2 Process: '$PROJECT_NAME'\
- Preview URL: http://'$VPS_IP':'$PORT'\
- Status: ✅ Running\
- Last Deploy: '$DEPLOY_DATE'\
\n' .build/context.md
else
  # Add new section
  cat >> .build/context.md <<EOF

## Deployment
- Port: $PORT
- PM2 Process: $PROJECT_NAME
- Preview URL: http://$VPS_IP:$PORT
- Status: ✅ Running
- Last Deploy: $DEPLOY_DATE
EOF
fi

echo "✅ .build/context.md updated"
```

---

## Anti-Bug: Dev vs Production

### Problème Fréquent (404 CSS/JS)

**Symptôme:**
```
Failed to load resource: 404
cbd55ab9639e1e66.js:1  Failed to load resource: 404
106a94478e937589.css:1  Failed to load resource: 404
turbopack-37a8d006c3393c75.js:1  Failed to load resource: 404
```

**Root Cause:**
- Build existe (`.next/`) MAIS c'est un dev build (Turbopack)
- Dev build génère hash dynamiques (change à chaque hot reload)
- Production attend build optimisé (static hash)

**Confusion:**
```
npm run dev → Turbopack (dev server, hash volatils)
npm run build → Next.js production (hash stables)
npm start → Serve production build
```

**Solution:** TOUJOURS clean + rebuild AVANT deploy

---

### Build Validation (OBLIGATOIRE)

**Check si build est production-ready:**

```bash
# ✅ CORRECT (production build)
ls -la .next/BUILD_ID
# Output: -rw-r--r-- 1 user user 12 Jan 11 12:00 .next/BUILD_ID

# ✅ CORRECT (static chunks)
ls .next/static/chunks/
# Output: hash stables (cbd55ab9639e1e66.js)

# ❌ MAUVAIS (dev build)
ls .next/BUILD_ID
# Output: file not found (dev build n'a pas BUILD_ID)

# ❌ MAUVAIS (turbopack)
grep -r "turbopack" .next/
# Output: found (= dev mode)
```

**Workflow sécurisé:**

```bash
# 1. CLEAN (remove old builds)
rm -rf .next
rm -rf node_modules/.cache

# 2. BUILD (fresh production)
npm run build

# 3. VERIFY
if [ ! -f ".next/BUILD_ID" ]; then
  echo "❌ Not a production build"
  exit 1
fi

# 4. DEPLOY
pm2 start ecosystem.config.js
```

---

## Workflow Complet

### Step-by-Step Deployment

```bash
#!/bin/bash
# deploy.sh - Workflow automatique complet

set -e  # Exit on error

PROJECT_PATH=$(pwd)
PROJECT_NAME=$(basename "$PROJECT_PATH")

echo "🚀 Deploying $PROJECT_NAME..."
echo ""

# 1. CLEAN + REBUILD (évite 404 dev/prod mismatch)
echo "🧹 Cleaning old builds..."

# Remove old builds (CRITICAL - évite hash conflicts)
rm -rf .next
rm -rf node_modules/.cache

# Fresh production build
echo "📦 Building production bundle..."
npm run build

# Verify build succeeded
if [ ! -d ".next" ]; then
  echo "❌ Build failed. Check errors above."
  exit 1
fi

# Verify production build (pas dev)
if [ ! -f ".next/BUILD_ID" ]; then
  echo "❌ Invalid build (missing BUILD_ID). Not a production build."
  exit 1
fi

echo "✅ Production build ready"

# 2. Get or assign port (SMART PERSISTANCE)
echo "📍 Getting/Assigning port..."

# Check si projet a déjà un port
if [ -f ".env" ] && grep -q "^PORT=" .env; then
  # Port existant dans .env → Réutilise
  PORT=$(grep "^PORT=" .env | cut -d'=' -f2)
  echo "✅ Port existant réutilisé: $PORT"
else
  # Check PM2 (si process existe)
  PM2_PORT=$(pm2 jlist 2>/dev/null | jq -r ".[] | select(.name == \"$PROJECT_NAME\") | .pm2_env.PORT" 2>/dev/null | head -1)

  if [ -n "$PM2_PORT" ] && [ "$PM2_PORT" != "null" ]; then
    # Port trouvé dans PM2 → Réutilise
    PORT=$PM2_PORT
    echo "PORT=$PORT" >> .env
    echo "✅ Port récupéré depuis PM2: $PORT"
  else
    # Nouveau projet → Assign nouveau port
    HIGHEST_PORT=$(pm2 jlist 2>/dev/null | jq -r '.[] | select(.pm2_env.PORT != null) | .pm2_env.PORT' | sort -n | tail -1)
    PORT=${HIGHEST_PORT:-3000}
    PORT=$((PORT + 1))
    echo "PORT=$PORT" >> .env
    echo "✅ Nouveau port assigné: $PORT"
  fi
fi

# 3. Create ecosystem config
echo "📝 Creating PM2 config..."
cat > ecosystem.config.js <<EOF
module.exports = {
  apps: [{
    name: '$PROJECT_NAME',
    script: 'npm',
    args: 'start',
    cwd: '$PROJECT_PATH',
    env: {
      NODE_ENV: 'production',
      PORT: $PORT
    },
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: '500M',
    error_file: './.pm2/logs/err.log',
    out_file: './.pm2/logs/out.log',
    time: true
  }]
}
EOF

# 4. Start PM2
echo "🔄 Starting PM2 process..."
pm2 delete "$PROJECT_NAME" 2>/dev/null || true
pm2 start ecosystem.config.js
pm2 save

# 5. Health check
echo "🔍 Health check..."
sleep 3

if ! pm2 list | grep -q "$PROJECT_NAME.*online"; then
  echo "❌ Failed to start"
  pm2 logs "$PROJECT_NAME" --lines 20 --nostream
  exit 1
fi

# Check HTTP
for i in {1..10}; do
  HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:$PORT 2>/dev/null)
  if [ "$HTTP_CODE" = "200" ]; then
    break
  fi
  sleep 1
done

# 6. Update .build/context.md
if [ -f ".build/context.md" ]; then
  echo "📝 Updating .build/context.md..."

  if grep -q "## Deployment" .build/context.md; then
    # Update existing
    sed -i '/## Deployment/,/^$/d' .build/context.md
  fi

  cat >> .build/context.md <<EOF

## Deployment
- Port: $PORT (PERSISTANT)
- PM2 Process: $PROJECT_NAME
- Preview URL: http://89.116.27.88:$PORT
- Status: ✅ Running
- Last Deploy: $(date "+%Y-%m-%d %H:%M:%S")
EOF
fi

# 7. Display results
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Projet $PROJECT_NAME déployé"
echo ""
echo "Preview: http://89.116.27.88:$PORT"
echo "Port: $PORT (PERSISTANT - ne changera jamais)"
echo ""
echo "PM2 Status:"
pm2 list | grep "$PROJECT_NAME"
echo ""
echo "Commandes:"
echo "  pm2 logs $PROJECT_NAME"
echo "  pm2 restart $PROJECT_NAME"
echo "  pm2 stop $PROJECT_NAME"
echo "  pm2 monit"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
```

---

## Troubleshooting

### 404 CSS/JS Files (FRÉQUENT)

**Symptôme:**
```
Failed to load resource: 404
cbd55ab9639e1e66.js:1  Failed to load resource: 404
106a94478e937589.css:1  Failed to load resource: 404
turbopack-*.js:1  Failed to load resource: 404
```

**Diagnostic:**
```bash
cd /path/to/project

# Check si BUILD_ID existe (production build)
ls -la .next/BUILD_ID

# Si absent → Dev build (MAUVAIS)
# Si présent → Production build (CORRECT)
```

**Fix:**
```bash
# 1. Clean everything
rm -rf .next
rm -rf node_modules/.cache

# 2. Fresh production build
npm run build

# 3. Verify BUILD_ID created
if [ -f ".next/BUILD_ID" ]; then
  echo "✅ Production build OK"
else
  echo "❌ Build failed"
fi

# 4. Restart PM2
pm2 restart [project-name]

# 5. Verify preview URL
curl -I http://89.116.27.88:[PORT]
# Expected: HTTP/1.1 200 OK
```

**Prévention:**
- JAMAIS `npm run dev` puis deploy
- TOUJOURS `rm -rf .next` avant build
- Deployment skill fait ça automatiquement maintenant

---

### Process ne démarre pas

```bash
# Check logs détaillés
pm2 logs [project-name] --lines 100

# Common issues:
# - Port déjà utilisé: change PORT in .env
# - Dependencies manquantes: npm install
# - Build absent: npm run build
# - .env DATABASE_URL invalide
```

---

### HTTP 502/503

```bash
# Check si Next.js écoute sur bon port
netstat -tlnp | grep [PORT]

# Check .env PORT correspond à ecosystem.config.js
cat .env | grep PORT
cat ecosystem.config.js | grep PORT

# Force rebuild + restart
cd /path/to/project
rm -rf .next
npm run build
pm2 restart [project-name]
```

---

### Memory leaks

```bash
# Monitor mémoire
pm2 monit

# Si mémoire monte continuellement:
# - Check max_memory_restart configuré
# - Analyser code (useEffect cleanup, event listeners)
```

---

### Preview URL ne répond pas

```bash
# 1. Check PM2 status
pm2 list
# Expected: status "online"

# 2. Check port listening
lsof -i :[PORT]
# Expected: node process

# 3. Check firewall (VPS)
sudo ufw status
# Si port bloqué: sudo ufw allow [PORT]

# 4. Test local d'abord
curl http://localhost:[PORT]
# Si OK local mais pas public → firewall issue

# 5. Check logs erreurs
pm2 logs [project-name] --err --lines 50
```

---

## Best Practices

### 1. Port Range
- **3001-3100:** Projets Next.js/React
- **4001-4100:** Projets Node.js/Express backend
- **8001-8100:** Projets Python/FastAPI

### 2. PM2 Monitoring
```bash
# Setup monitoring (1x global)
pm2 install pm2-logrotate

# Configure log rotation (avoid disk full)
pm2 set pm2-logrotate:max_size 10M
pm2 set pm2-logrotate:retain 7
```

### 3. Memory Limits
- **Frontend (Next.js):** 500MB
- **Backend API:** 300MB
- **Full-stack:** 700MB

### 4. Auto-restart Strategy
```javascript
// ecosystem.config.js
{
  autorestart: true,
  max_restarts: 10,        // Max 10 restarts in...
  min_uptime: '10s',       // ...10 seconds (évite restart loops)
  max_memory_restart: '500M'
}
```

---

## Commandes Utiles

### PM2 Management
```bash
# List all processes
pm2 list

# Logs en temps réel
pm2 logs [project-name]

# Logs dernières 100 lignes
pm2 logs [project-name] --lines 100

# Restart projet
pm2 restart [project-name]

# Stop projet
pm2 stop [project-name]

# Delete projet
pm2 delete [project-name]

# Monitoring real-time
pm2 monit

# Describe process (détails)
pm2 describe [project-name]
```

### Port Management
```bash
# Check quel process utilise port
lsof -i :3001

# Kill process sur port
kill -9 $(lsof -t -i:3001)

# Liste tous ports PM2 utilisés
pm2 jlist | jq -r '.[].pm2_env.PORT' | sort -n
```

---

## Conventions Non-Negotiables

1. **Port PERSISTANT par projet** (.env source de vérité, jamais changer)
2. **Check .env AVANT assign** (réutilise si existe, sinon auto-increment)
3. **PM2 obligatoire** (jamais npm start direct en prod)
4. **ecosystem.config.js** (config centralisée, pas CLI args)
5. **Health check systématique** (process + HTTP 200)
6. **.build/context.md updated** (traçabilité deployment)
7. **PM2 save après start** (persist reboot VPS)
8. **Logs dans .pm2/logs/** (centralisé, pas console)
9. **max_memory_restart configuré** (évite leaks)
10. **Preview URL stable** (bookmarkable, ne change jamais)

---

**Inspiré de:**
- PM2 Documentation (pm2.keymetrics.io)
- Vercel Zero-Config Deployment
- Twelve-Factor App (process management)
- Google SRE (health checks, monitoring)

---

**Version**: 1.2.0
**Last updated**: 2025-01-11
**Maintained by**: EXECUTOR agent
**Changelog**:
- v1.2.0: Clean + rebuild automatique (évite 404 dev/prod mismatch), validation BUILD_ID, troubleshooting 404 CSS/JS
- v1.1.0: Port persistance garantie (.env source vérité, check avant assign, preview URL stable)
- v1.0.0: Version initiale (PM2 deployment, auto port assignment)
