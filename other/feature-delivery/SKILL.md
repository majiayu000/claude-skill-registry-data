---
name: feature-delivery
description: Livrer une feature non-triviale KLASSCI multi-instance en suivant la méthodologie 13-phases validée par Marcel (10 mai 2026). Du brief utilisateur au déploiement vérifié — explore mémoire/code, état des lieux tenant, /plan-and-confirm depth N, /simplify, /pr-review-toolkit, merge cross-branch, déploiement klassci-cli, validation visuelle. Use when implementing any feature touching ≥ 3 files, schema DB, production tenant, or user flow. Rule #1 — never skip a phase.
---

# Feature Delivery — Méthodologie KLASSCI multi-instance

## Quand t'invoquer

L'utilisateur t'invoque via `/feature-delivery` (ou si une feature non-triviale est demandée sans skill explicite, propose-toi).

**Tu déclines** si :
- C'est une typo / fix unique fichier sans regression → `/commit` direct
- C'est juste un refactor interne sans impact UX → /commit direct
- L'utilisateur veut juste explorer / lire du code → pas de skill, juste répondre

**Tu prends le lead** si :
- Feature touche ≥ 3 fichiers OU schéma DB
- Cible un tenant en production
- Impacte un flow utilisateur
- Demande au moins 1 PR vers `presentation`

---

## Séquence des 13 phases

Tu **DOIS** annoncer chaque phase avant de l'exécuter. Tu **NE PEUX PAS** sauter une phase. Tu **NE PEUX PAS** refusionner deux phases.

### Phase 0 — Exploration mémoire + code (zéro question utilisateur)

```
1. Read mémoires pertinentes (memory/MEMORY.md puis fichiers thématiques) — en PARALLÈLE
2. Glob fichiers cibles potentiels (app/Models/<scope>*.php, etc.)
3. Grep symboles clés
4. Read rules projet existantes pertinentes (.claude/rules/<scope>.md)
```

Avant la fin de cette phase : annoncer en 2 phrases ce que tu as compris du contexte.

---

### Phase 1 — État des lieux tenant cible (si applicable)

Si la feature cible un tenant identifié, lance un audit live :

```bash
klassci stats <tenant>
klassci classes:list <tenant>
klassci annee <tenant>
klassci users:list <tenant>
```

Note les anomalies (tokens manquants, données aberrantes, dates typo).

Si pas de tenant cible explicite → skip à Phase 2.

---

### Phase 2 — Collecte sources métier

Si l'utilisateur a fourni :
- **PDF / Document** → l'extraire ENTIÈREMENT (toutes les pages) avant d'avancer.
  - Tool Read PDF natif d'abord
  - Si Windows + échec `pdftoppm` → Python : `py -m pip install pypdf` + script ci-dessous

```bash
PYTHONIOENCODING=utf-8 py -c "
import pypdf
r = pypdf.PdfReader(r'<absolute_path>')
for i, p in enumerate(r.pages):
    print(f'\n===== PAGE {i+1} =====')
    print(p.extract_text())
"
```

- **Excel** → utiliser `pandas` ou `openpyxl` pour lecture complète
- **Captures d'écran** → analyser visuellement, citer les éléments précis

Si l'utilisateur **corrige** ta compréhension : pivote IMMÉDIATEMENT, ne discute pas.

---

### Phase 3 — Recherche standard externe

Si le métier a un standard documenté (UEMOA, IFRS, ISO, normes professionnelles), valide avec :
- `Agent` `websearch` pour les conventions du domaine
- `Agent` `explore-docs` (ctx7) pour les patterns Laravel safe

Cite tes sources dans le commit message / PR description.

---

### Phase 4 — Analyse schéma vs gap fonctionnel

Lis en parallèle :
- Migrations existantes pertinentes
- Models concernés (fillable, casts, relations)
- Controllers liés (validation, business logic)

Output un tableau :
| Concept | État DB | Action |
|---|---|---|
| ... | ✅ Existe / ⚠️ Nullable / ❌ Manque | Garder / Migrer / Skip |

Le « salt » du plan futur sort directement de cette analyse.

---

### Phase 5 — Discussion archi avec utilisateur

Présente les questions structurantes (jamais plus de 4 à la fois) :
1. Décisions DB
2. Décisions UI
3. Décisions UX
4. Décisions scope (bulk import maintenant ou en PR séparée ?)

**Attends validation explicite** avant de passer à Phase 6. Cite les validations dans le PR description plus tard.

---

### Phase 6 — /plan-and-confirm (depth auto-détecté ou bumped)

Invoque la skill `plan-and-confirm` avec un prompt riche qui :
- Récap le contexte déjà validé (ne pas re-débattre)
- Liste les enjeux critiques à challenger
- Demande N alternatives avec confidence scores
- Force le pré-mortem détaillé

**Auto-bump depth** :
| Signal | Score |
|---|---|
| Multi-PR | floor=4 |
| Schema migration table partagée multi-instance | floor=4 |
| Mot « ultrathink » | =5 |

**À depth=5** :
- 5 agents en parallèle (Critic, Codebase explorer, Docs research, Web search, Devil's Advocate)
- 4 reflexions toi-même (Premortem, Simplification 30%, Future-Marcel, Opposite-day)
- 3 alternatives (A minimal / B balanced / C ambitieux) avec confidence per-file
- Recommandation explicite ancrée dans evidence

**Phase 4 OKAY gate** : pas de code tant que pas de OKAY explicit.

---

### Phase 7 — Implémentation PR foundation

```bash
git fetch origin presentation
git checkout -b feat/<scope>-<short-name>
git rebase origin/presentation
```

Discipline :
- **1 concern = 1 commit** atomique (bug fix incident → commit séparé)
- **`git add <fichier1> <fichier2>`** explicite, jamais `git add -A`
- **Migrations** via `php artisan make:migration <nom>`
- **Validation enum atomique** : `Rule::in(EnumClass::values())` + cast `=> EnumClass::class`
- **Tests Unit** sans DB pour BTS regression sur tables partagées
- **Pas de Co-Authored-By**

Lint + tests avant chaque commit :
```bash
php -l <file>
php vendor/bin/phpunit tests/Unit/<TestFile>.php --testdox
```

---

### Phase 7.5 — /thermo-review (garde-fou bloquant)

Avant `/simplify`, avant la fusion, avant le déploiement : lance `/thermo-review`
**en sous-agent** sur `git diff origin/presentation...HEAD`. C'est le
commandement 0 de `pre-merge-checklist.md`, et il passe avant les deux revues
qui suivent : elles cherchent des défauts dans ce qui est écrit, celle-ci
demande d'abord **s'il fallait l'écrire** — et, côté produit, si la pertinence
est sourcée, l'écran prouvé par capture, le travail réparti à la source, et le
parcours fluide (liens profonds, modales, aucun rechargement).

Verdict `BLOCK` → on corrige et on relance la revue sur le nouveau diff. On ne
passe pas à la phase 8 sur un `BLOCK`.

---

### Phase 8 — /simplify cleanup

Invoque la skill `/simplify` (ou `/pr-review-toolkit:code-simplifier`) — 3 agents parallèles :
1. **Reuse** — duplication, helpers existants
2. **Quality** — dead code, copy-paste, stringly-typed, comments redundants
3. **Efficiency** — N+1, hot-path bloat

Applique tous les findings (sauf faux positifs justifiés) dans 1 commit `refactor(<scope>): /simplify cleanup — <résumé>`.

---

### Phase 9 — /pr-review-toolkit:review-pr

Invoque la skill `/pr-review-toolkit:review-pr` — 4 agents specialisés :
1. **code-reviewer** — CLAUDE.md compliance + general bugs
2. **pr-test-analyzer** — coverage, BTS regression
3. **silent-failure-hunter** — error handling
4. **type-design-analyzer** — encapsulation, invariant, enforcement

Sévérités :
- 🚨 **MUST FIX** (blocks merge)
- ⚠️ **SHOULD CONSIDER**
- 💡 **NIT**
- ✅ **STRENGTHS** (cite-les dans PR description)

**Tout fix dans 1 commit** `fix(<scope>): address PR review findings — <résumé>`.

---

### Phase 10 — Merge + cross-branch sync

Pattern PR-via-gh (rule `multi-agent-git-safety` commandement 13) :
```bash
gh pr merge <pr-number> --merge --admin
git fetch origin presentation
git merge --ff-only origin/presentation     # JAMAIS git pull
git push origin presentation:<tenant>       # cross-branch sync (rule tenant-branches)
git branch -d feat/<scope>-<short-name>
```

Si plusieurs tenants concernés :
```bash
for t in <tenant1> <tenant2>; do
    git push origin presentation:$t
done
```

---

### Phase 11 — Hotfixes UX itératifs (déclenchés par utilisateur)

Quand l'utilisateur teste et trouve un bug :
1. Lui demander screenshot ou description précise
2. Branche `hotfix/<scope>-<short-name>`
3. Fix minimal (1-3 lignes idéalement)
4. Commit + push + PR + `gh pr merge --admin` direct (pas de plan-and-confirm pour 3 lignes)
5. Cross-branch sync
6. Deploy via klassci-cli
7. L'utilisateur re-teste

**Règle** : 1 PR = 1 concern. Pas de PR « cleanup général ».

---

### Phase 12 — Déploiement multi-instance via klassci-cli

```bash
klassci pull <tenant>           # 1. git pull + Laravel cache_clear interne
klassci cache:clear <tenant>    # 2. ⚠️ ESSENTIEL : opcache reset
klassci migrate <tenant>        # 3. apply pending migrations
klassci permissions:fix <tenant> # 4. sync registry → DB
```

**Si CLI timeout (>30s)** : curl direct vers `/api/cli/<endpoint>` avec `--max-time 120`.

```bash
curl -s -X POST -H "Authorization: Bearer <token>" -H "Accept: application/json" \
    --max-time 120 https://<tenant>.klassci.com/api/cli/<endpoint>
```

---

### Phase 13 — Validation fonctionnelle

Demande à l'utilisateur de tester l'UI sur le tenant cible avec **étapes précises et résultats attendus visuels** :

```
Va sur https://<tenant>.klassci.com/<route>, hard-refresh (Ctrl+F5) :

1. <action 1> → <résultat attendu visuel>
2. <action 2> → <résultat attendu visuel>
3. <action 3> → <résultat attendu visuel>
```

Si bug remonté → Phase 11 (hotfix).
Si tout passe → annoncer la phase suivante (PR LMD-2 par ex) et demander OK pour continuer.

---

## Cas particulier : saisie en masse par utilisateur (X UE / Z ECUE)

Quand un utilisateur (directrice, secrétaire) doit saisir manuellement des dizaines/centaines d'entrées, applique CES patterns UX :

1. **Auto-fill** quand champ optionnel + champ dépendant rempli
2. **Empty state ladder** (4 cas distincts adaptés)
3. **Bulk import** comme PR séparée future (parser dédié)
4. **Hiérarchie expandable** (Alpine `x-show` + caret)
5. **Saisie progressive** (sauvegarde par entité, KPIs visibles)

---

## Discipline mémoire

- **Avant de coder** : sauvegarder contexte décisionnel
- **Après chaque grand jalon** : update la mémoire
- **À chaque correction utilisateur** : noter la préférence
- **Index dans MEMORY.md** : 1 ligne par fichier, < 200 chars

---

## Anti-patterns absolus à BLOQUER

1. ❌ Coder sans /plan-and-confirm pour une feature multi-PR
2. ❌ Présenter 1 seul plan à depth ≥ 4
3. ❌ Coder sans OKAY explicit (rule #1 absolue)
4. ❌ Hardcoder une liste de valeurs dans 3+ endroits — utiliser `Enum::cases()`
5. ❌ Sauter le `cache:clear` entre `pull` et `migrate`
6. ❌ Force push direct sur `presentation` / `master` sans PR
7. ❌ `git pull` au lieu de `git fetch + git merge --ff-only`
8. ❌ Accumuler 5 « petits » fixes dans 1 PR
9. ❌ Dire « c'est fait » sans demander à l'utilisateur de vérifier visuellement
10. ❌ Filtrer le critic / argumenter au lieu de fixer

---

## Voir aussi

- **Rule** : `.claude/rules/feature-delivery-methodology.md` — la rule projet associée
- **Mémoire** : `feature-delivery-methodology.md` (project memory) — version exhaustive avec exemples
- **Skill** : `/plan-and-confirm` — pierre angulaire de la phase 6
- **Skill** : `/simplify` — phase 8
- **Skill** : `/pr-review-toolkit:review-pr` — phase 9
- **Rules transverses appliquées** : `multi-agent-git-safety.md`, `tenant-branches.md`, `pre-commit-quality-gate.md`, `parallel-agents.md`, `marcel-global-preferences.md`, `migrations.md`, `permissions.md`, `premium-redesign.md`, `premium-selects.md`, `no-god-code.md`, `customizable-roles.md`, `klassci-classe-matieres.md`
