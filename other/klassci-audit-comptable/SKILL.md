---
name: klassci-audit-comptable
description: Audit E2E du module comptable KLASSCI (multi-tenant) — UI + code + CLI. À utiliser pour "audit compta", "vérifier les KPIs", "rapprocher dashboard et CLI", "trouver des bugs sur les pages comptables", "audit OHADA". Enrichit automatiquement docs/audits/<date>-audit-comptable-klassci.md et propose des rules nouvelles si nécessaire.
---

# KLASSCI Audit Comptable E2E

Audit reproductible du module comptable KLASSCI couvrant les 3 axes : UI, code et CLI. Pensé pour être relancé d'une session sur l'autre, en enrichissant un document d'audit central + en proposant des rules / commands `klassci-cli` quand un manque est détecté.

## Quand utiliser ce skill

- L'utilisateur dit « audite la compta », « vérifie le module compta », « refais un audit comptable »
- Une feature compta est livrée et il faut vérifier qu'elle n'a rien cassé sur les KPIs / réconciliations / verrouillages
- Avant un déploiement multi-tenant pour vérifier que toutes les pages compta tiennent
- Pour préparer une feature de réconciliation, audit fiscal, ou export OHADA
- Pour identifier de nouvelles règles à capitaliser (`.claude/rules/...`)

## Principes (à respecter en toute session)

1. **Tenant de test par défaut : `esbtp-yakro`** — c'est l'environnement réel le plus dense (1 561 étudiants, 1 429 paiements, 200M+ FCFA encaissés). Les bugs/observations s'appliquent à TOUS les tenants.
2. **Toujours 3 sources de preuves** pour chaque finding : UI (dev-browser) + code (Read / Grep) + CLI (api/cli).
3. **Enrichir le doc d'audit en cours**, pas en créer un nouveau à chaque run, sauf si > 1 mois entre runs.
4. **Identifier les manques en commands `klassci-cli`** et créer des endpoints `api/cli/*` quand nécessaire.
5. **Ne JAMAIS muter les paiements en prod en mode audit** — audit = read-only sauf bugfix explicite avec accord utilisateur.
6. **Capturer les nouvelles règles** : si l'audit révèle un pattern qui mérite une rule projet, l'écrire dans `.claude/rules/`.

## Boucle d'audit standard (à dérouler systématiquement)

### Phase 1 — Cadre du run

1. Identifier le tenant cible (par défaut `esbtp-yakro`).
2. Vérifier les credentials :
   - **Login UI** : `Admin` / `Kaam@2022` (yakro). Tester via `--browser admin-audit`.
   - **Token CLI** : `klassci config:list` → token déjà configuré.
3. Vérifier l'année universitaire courante via `klassci-cli annee <tenant>` + `api/cli/annee`.
4. Lire le doc d'audit en cours : `docs/audits/<dernière_date>-audit-comptable-klassci.md`.
   - Si > 30j d'écart : créer nouveau doc `docs/audits/<aujourd_hui>-audit-comptable-klassci.md` et lier les findings actifs.
   - Sinon : enrichir l'existant.

### Phase 2 — Diagnostic CLI

Lancer en batch tous les diagnostics disponibles :

```bash
YAKRO_TOKEN=$(python -c "import json; d=json.load(open('C:/Users/PAVILION/.klassci/config.json')); print(d['tenants']['esbtp-yakro']['token'])")

# Stats globaux
curl -sS "https://esbtp-yakro.klassci.com/api/cli/stats" -H "Authorization: Bearer $YAKRO_TOKEN" --max-time 30 | python -m json.tool

# Paiements par status
for s in valide en_attente rejete; do
  echo "=== $s ==="
  curl -sS "https://esbtp-yakro.klassci.com/api/cli/payments?per_page=1&status=$s" -H "Authorization: Bearer $YAKRO_TOKEN" --max-time 30 | python -c "import json,sys; print(json.load(sys.stdin)['data']['pagination']['total'])"
done

# Analytics diagnose
curl -sS "https://esbtp-yakro.klassci.com/api/cli/analytics/diagnose" -H "Authorization: Bearer $YAKRO_TOKEN" --max-time 60 | python -m json.tool

# Logs récents (chercher 500 ou ERROR)
curl -sS "https://esbtp-yakro.klassci.com/api/cli/logs?lines=50" -H "Authorization: Bearer $YAKRO_TOKEN" --max-time 30 | python -c "import json,sys; [print(l['timestamp'], l['level'], l['message'][:100]) for l in json.load(sys.stdin)['data']['entries']]"
```

**Quand un diagnostic manque** (par exemple « pas d'endpoint pour les soldes de caisse par mode/date ») :

1. Identifier le besoin précis.
2. Proposer la commande CLI : `klassci compta:cash-balance <tenant> --date=2026-06-04`.
3. Créer l'endpoint `api/cli/comptabilite/cash-balance` (méthode dédiée dans `app/Http/Controllers/API/CLI/CLIDataController.php` ou nouveau `CLIComptabiliteController`).
4. Ajouter la commande au wrapper `klassci-cli.ps1`.
5. Documenter dans la rule `.claude/rules/klassci-cli-tool.md`.

### Phase 3 — Audit code (lecture)

Pour chaque page compta du plan (Dashboard / Frais / Config Frais / Paiements / Recouvrement / Analytics / Journal Caisse / Audit Compta / Relances / Export détaillé / Suivi par Catégorie), lire :

1. Le controller (`app/Http/Controllers/ESBTP*Controller.php`)
2. L'Action ou Service principal (`app/Actions/Comptabilite/*Action.php`, `app/Services/*Service.php`)
3. La vue (`resources/views/esbtp/comptabilite/*.blade.php`)

Chercher (grep) :
- `whereNull('deleted_at')` cohérence (soft-delete partout)
- Filtres par `annee_universitaire_id` cohérents
- Permissions `comptabilite.*` correctes
- Pas de HAVING + colonne non agrégée (ONLY_FULL_GROUP_BY)
- Pas de string littérale `'validé'` au lieu de constante
- N+1 queries (whereHas dans foreach)
- Audit log absent sur mutations critiques (status, montant, mode, date)

### Phase 4 — UI audit avec dev-browser (recette canonique)

**⚠️ Ne PAS utiliser de scripts `/tmp/*.js` séparés** — yakro est protégé par LWS DDoS Protection qui détecte les fingerprints Playwright headless. Utiliser EXCLUSIVEMENT le pattern inline heredoc + UA spoof + `--browser <nom>` persistent :

```bash
npx dev-browser --browser admin-audit --timeout 120 <<'EOF' 2>&1 | tail -80
const page = await browser.getPage("main");
await page.setExtraHTTPHeaders({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
});

// Login (si pas déjà fait dans la session admin-audit)
await page.goto("https://esbtp-yakro.klassci.com/login?_t=" + Date.now(), { waitUntil: "domcontentloaded", timeout: 30000 });
await new Promise(r => setTimeout(r, 1500));
const needsLogin = await page.evaluate(() => !!document.querySelector('input[name="username"]'));
if (needsLogin) {
    await page.fill('input[name="username"]', "Admin");
    await page.fill('input[name="password"]', "Kaam@2022");
    await page.click('button[type="submit"]');
    await new Promise(r => setTimeout(r, 5000));
}

// Test pages
const pages = [
  ["Dashboard Compta", "/esbtp/comptabilite/dashboard"],
  ["Frais", "/esbtp/frais"],
  ["Frais Config", "/esbtp/frais/configure"],
  ["Paiements", "/esbtp/paiements"],
  ["Recouvrement", "/esbtp/comptabilite/recouvrement"],
  ["Analytics", "/esbtp/comptabilite/analytics"],
  ["Journal Caisse", "/esbtp/comptabilite/journal-caisse"],
  ["Audit Compta", "/esbtp/audit/comptabilite"],
  ["Relances", "/esbtp/comptabilite/relances"],
];
const results = [];
for (const [name, path] of pages) {
  try {
    await page.goto("https://esbtp-yakro.klassci.com" + path + "?_t=" + Date.now(), { waitUntil: "domcontentloaded", timeout: 60000 });
    await new Promise(r => setTimeout(r, 2000));
    const info = await page.evaluate(() => ({
      title: document.title.slice(0, 60),
      hasErrors: (document.body.innerText.match(/Whoops|Erreur serveur|Exception|undefined/g) || []).slice(0, 3),
      tableRows: document.querySelectorAll('table tbody tr').length,
      kpis: document.querySelectorAll('[class*="kpi"], [class*="stat-card"]').length,
      hasHero: !!document.querySelector('[class*="hero"]'),
      h1: document.querySelector('h1')?.innerText.slice(0, 80) || '',
    }));
    results.push({ name, path, status: 200, ...info });
  } catch (e) {
    results.push({ name, path, error: e.message.slice(0, 100) });
  }
}
console.log(JSON.stringify(results, null, 2));
EOF
```

**Recette à respecter** :
- `--browser admin-audit` persiste les cookies (login une fois, audit plusieurs fois)
- `--timeout 120` pour les pages lentes (Dashboard Compta a été observé à 33s)
- `_t=Date.now()` cache-bust pour éviter Varnish edge cache
- Heredoc `<<'EOF'` pour passer le script inline (PAS de fichier temporaire JS)

### Phase 5 — Croisement UI ↔ CLI

Pour chaque KPI affiché à l'UI, comparer avec la valeur CLI :

| KPI | UI valeur | CLI valeur | Cohérence |
|---|---|---|---|
| Total paiements | (lire dashboard) | `api/cli/stats` | ✅ / ❌ |
| Validés | (dashboard) | `payments?status=valide` total | ✅ / ❌ |
| En attente | (dashboard) | `payments?status=en_attente` total | ✅ / ❌ |
| Encaissé total | (dashboard) | `stats.revenue.total` | ✅ / ❌ |
| Étudiants actifs | (dashboard) | `stats.active_students` | ✅ / ❌ |
| Risk saturation | (analytics) | `analytics/diagnose.risk_saturation` | ✅ / ❌ |

Toute divergence est un **finding à investiguer** : différence de scope (année / filière / mode), différence de status canonique, différence de soft-delete.

### Phase 6 — Lecture logs prod

```bash
# Erreurs récentes (50 dernières lignes filtre level=ERROR)
curl -sS "https://esbtp-yakro.klassci.com/api/cli/logs?lines=100" -H "Authorization: Bearer $YAKRO_TOKEN" --max-time 30 \
  | python -c "import json,sys; data=json.load(sys.stdin)['data']['entries']; [print(e['timestamp'], e['level'], e['message'][:140]) for e in data if e['level']=='ERROR'][-30:]"
```

Chaque erreur trouvée :
1. Tracer le fichier source (stacktrace)
2. Évaluer impact (bloquant / log spam / sub-feature cassée)
3. Si bloquant → fix + commit + déploy + verify
4. Si log spam → noter pour batch fix

### Phase 7 — Enrichissement docs + rules

À la fin du run, mettre à jour systématiquement :

1. **`docs/audits/<date>-audit-comptable-klassci.md`** :
   - Mettre à jour le statut de chaque page (🟢 / 🟡 / 🔴 / ⚪)
   - Ajouter les nouveaux findings
   - Mettre à jour la table KPIs avec dernières valeurs UI vs CLI
   - Marquer les bugs résolus comme « ✅ Fixé `<commit>` »

2. **`.claude/rules/<nouvelle-rule>.md`** si l'audit révèle un pattern nouveau :
   - Pattern cassé répété 3+ fois (ex: `'validé'` vs `'valide'` typo)
   - Anti-pattern récurrent (ex: HAVING avec colonne non agrégée)
   - Best practice à capitaliser (ex: source unique de vérité pour scope dashboard)

3. **`.claude/rules/reconciliation-paiements-caisse.md`** si nouvelle observation pertinente pour la feature réconciliation.

## Pages couvertes (référence)

| Page | URL | Permission | Status historique |
|---|---|---|---|
| Dashboard Compta | `/esbtp/comptabilite/dashboard` | `comptabilite.dashboard.view` | 🟡 discrepancy count_pending (2026-06-04) |
| Gestion Frais | `/esbtp/frais` | `comptabilite.frais.view` | 🟢 |
| Configuration Frais | `/esbtp/frais/configure` | `comptabilite.frais.configure` | 🟢 |
| Paiements | `/esbtp/paiements` | `paiements.view` | 🟢 |
| Recouvrement | `/esbtp/comptabilite/recouvrement` | `comptabilite.recouvrement.access` | 🟢 |
| Analytics | `/esbtp/comptabilite/analytics` | `comptabilite.analytics.view` | 🟢 |
| Journal Caisse | `/esbtp/comptabilite/journal-caisse` | `comptabilite.journal_caisse.view` | 🟢 |
| Audit Compta | `/esbtp/audit/comptabilite` | `comptabilite.audit.view` | 🟢 |
| Relances | `/esbtp/comptabilite/relances` | `comptabilite.relances.view` | 🟢 |
| Export détaillé | `/esbtp/comptabilite/export` | `comptabilite.reports.export` | ⚪ à tester |
| Suivi par Catégorie | `/esbtp/paiements/suivi-categories` (PAS `/esbtp/comptabilite/...`) | `comptabilite.dashboard.view` | 🟢 |
| Export détaillé | `/esbtp/paiements/export-detaille/*` (groupe consolidé) | `paiements.export` | 🟡 routes vérifiées |

## Endpoints CLI à privilégier

### Génériques
- `api/cli/stats` — KPIs globaux (filtre annee_courante par défaut)
- `api/cli/payments` — liste paiements (filtre status, mode, annee_courante par défaut)
- `api/cli/analytics/diagnose` — état échéancier + risk
- `api/cli/annee` — années universitaires
- `api/cli/logs?lines=N&search=X` — logs prod
- `api/cli/users` — liste users
- `api/cli/permissions/audit` — audit registre permissions

### Compta dédiés (commit `9f1416cd` — utilisez-les en priorité)

- **`api/cli/comptabilite/dashboard-kpis`** `[?annee_id&filiere_id&classe_id]`
  → Mirror EXACT des KPIs du Dashboard Compta UI. Utiliser pour reproduire bugs UI.
- **`api/cli/comptabilite/cash-balance`** `[?date_debut&date_fin&status]`
  → Solde caisse par mode pour réconciliation physique.
- **`api/cli/comptabilite/payments-summary`**
  → Breakdown par année × status. Identifier les paiements résidus d'années passées.
- **`api/cli/comptabilite/period-locks`**
  → État verrouillage période + nb paiements modifiables vs verrouillés.
- **`api/cli/comptabilite/reconciliation-candidates`** `[?pending_days]`
  → Anomalies suspectes (montant=0, sans inscription, sans année, en_attente vieux).

**Si endpoint manquant** :
1. Ajouter à `app/Http/Controllers/API/CLI/CLIComptabiliteController.php` (existant)
2. Route dans `routes/api.php` sous `Route::prefix('comptabilite')->name('comptabilite.')->group(...)`
3. Test : `curl -sS .../api/cli/comptabilite/<nouveau> -H "Authorization: Bearer $TOKEN"`
4. Mettre à jour cette section du skill avec le nouveau endpoint

## Pattern de sortie standard

Toujours rendre :

```markdown
## Statut

Validé partiellement | Validé de bout en bout | Bloqué

## Pages auditées (cycle)

- Page X : 🟢/🟡/🔴 + 1 ligne preuve
- ...

## Bugs identifiés

- Bug X (sévérité) : preuve UI + CLI + extrait code
- ...

## Bugs fixés pendant l'audit

- `<commit>` Sujet — résolution
- ...

## Docs enrichis

- `docs/audits/<date>-audit-comptable-klassci.md` (sections X, Y mises à jour)
- `.claude/rules/<nouvelle-rule>.md` (si applicable)

## Endpoints CLI ajoutés

- `api/cli/<nouveau>` — usage : ...

## Prochaines étapes recommandées

- ...
```

## Questions à poser à l'utilisateur si manque d'info

- **Périmètre** : tous tenants ou un tenant spécifique ? (default = `esbtp-yakro`)
- **Scope** : full audit (11 pages) ou cible précise ? (default = full)
- **Fix vs report-only** : fixer les bugs trouvés ou seulement reporter ? (default = fix les critiques, report les mineurs)
- **Date du doc** : utiliser le doc existant ou créer nouveau (si > 30j) ?

## Pièges à éviter

1. **Scripts `/tmp/*.js`** : LWS bloque le fingerprint Playwright → toujours heredoc inline
2. **`--headless`** : détection immédiate → toujours navigateur visible avec `--browser <nom>`
3. **Pas de `_t=Date.now()`** : Varnish edge cache servira l'ancienne version
4. **CLI sans token** : redirect 302 vers login → toujours `-H "Authorization: Bearer $TOKEN"`
5. **Fixer en prod sans vérifier le tenant cible** : push presentation → tenant cible explicite
6. **Oublier `klassci cache:clear`** après pull (rule `feature-delivery-methodology` cmd #10)
7. **Comparer KPIs sans préciser le scope** : Dashboard sans filtre vs CLI avec annee_courante → écart attendu, pas un bug

## Voir aussi

- `.claude/rules/reconciliation-paiements-caisse.md` — feature future (déclenchée par cet audit)
- `.claude/rules/no-god-code-compta.md` — discipline extraction Domain/Actions
- `.claude/rules/analytics-pitfalls.md` — 10 pièges courants
- `.claude/rules/permissions.md` — conventions `comptabilite.*`
- `.claude/rules/feature-delivery-methodology.md` — méthodologie 13 phases
- `docs/audits/<dernière_date>-audit-comptable-klassci.md` — doc principal
- Skill sœur : `klassci-test-e2e` — audit académique (résultats, bulletins)
- Skill sœur : `klassci-jury-lifecycle` — audit jury LMD
