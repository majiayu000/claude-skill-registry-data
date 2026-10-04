---
name: "source-command-deploy"
description: "Build locale + deploy su Vercel + verifica post-deploy"
---

# source-command-deploy

Use this skill when the user asks to run the migrated source command `deploy`.

## Command Template

# Deploy sicuro su Vercel

Segui questi step nell'ordine esatto. Non saltare nessuno.

## 0. Contatore deploy (ogni 5 deploy → cleanup automatico)

Leggi il contatore in `.Codex/deploy-count.json` e incrementalo:

```bash
node -e "
  const fs = require('fs');
  const path = '.Codex/deploy-count.json';
  const data = fs.existsSync(path) ? JSON.parse(fs.readFileSync(path)) : {count: 0};
  data.count = (data.count || 0) + 1;
  fs.writeFileSync(path, JSON.stringify(data, null, 2));
  console.log(data.count);
"
```

**Se il numero è multiplo di 5** (5, 10, 15…): esegui subito tutti gli step del `/cleanup` prima di continuare. Non chiedere conferma, procedi in automatico:

1. Cerca e rimuovi import inutilizzati nei file `src/` e `api/`
2. Rimuovi dead code (funzioni/variabili mai usate)
3. Esegui `npm run build` — se fallisce, correggilo prima di andare avanti
4. Controlla ogni file in `api/` (escluso `_lib/`): CORS, try/catch, env vars
5. Elimina file spazzatura: `find . -name ".DS_Store" -not -path "./node_modules/*" -delete`
6. Esegui `npm ls --depth=0 2>&1 | grep "UNMET\|invalid\|missing"` e segnala eventuali problemi
7. Produci un report sintetico di ciò che hai trovato e risolto

Dopodichè continua con gli step normali del deploy.

## 1. Annota il deploy corrente
```
vercel ls --prod
```
Prendi nota dell'URL del deploy attivo (serve per rollback).

## 2. Build locale
```
npm run build
```
Se la build fallisce, blocca tutto e risolvi prima di continuare.

## 3. Deploy in produzione
```
vercel --prod
```

## 4. Verifica post-deploy
- Apri l'URL del deploy appena completato
- Testa la chat (manda un messaggio e verifica risposta)
- Controlla che l'admin panel sia accessibile
- Se qualcosa è rotto → rollback immediato con `vercel rollback`

## 5. Rollback (solo se necessario)
```
vercel rollback
```

## Note
- Le env vars non si deployano automaticamente: vanno aggiunte manualmente su Vercel Dashboard se sono nuove
- Non usare mai `vercel --prod` senza aver fatto la build locale prima
- File critici da non toccare durante il deploy: `.env`, `api/_lib/`

---

## Regole specifiche — Gravity Prototipi

Queste regole si applicano quando si lavora nel progetto **Gravity** (`/Desktop/gravity`).
Sostituiscono completamente gli step 1–5 precedenti — non usare `vercel --prod` direttamente.

**Deploy tramite GitHub (flusso corretto):**

Il deploy avviene automaticamente tramite GitHub → Vercel. Non eseguire mai `vercel --prod` su questo progetto.

### Step 1 — Verifica stato
```bash
cd /Users/gloriabonanno/Desktop/gravity
git status
```
Mostra i file modificati prima di procedere.

### Step 2 — Commit
```bash
git add .
git commit -m "descrizione breve delle modifiche"
```
Il messaggio deve descrivere cosa è cambiato (es. "feat: aggiorna login screen SSO").

### Step 3 — Push
```bash
git push
```
Vercel rileva il push su `main` e deploya automaticamente in 10–20 secondi.

### Step 4 — Verifica post-deploy
Apri https://gravity-prototipi-codesour.vercel.app e verifica che le modifiche siano visibili.
In caso di problemi controlla i log su: https://vercel.com/codesour-projects/gravity-prototipi

**Rollback:** vai su Vercel Dashboard → seleziona il deploy precedente → **Promote to Production**

---

**Riferimenti:**
- Repo GitHub: https://github.com/codesour-design/gravity
- URL produzione: https://gravity-prototipi-codesour.vercel.app
- Vercel Dashboard: https://vercel.com/codesour-projects/gravity-prototipi
- Account Vercel: `bonnyb` / team `codesour-projects` (MAI usare l'account personale `pianobdesign20`)
- Struttura: tutti i prototipi in `prototype/` — un solo progetto, path separati per modulo
