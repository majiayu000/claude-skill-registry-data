---
name: klassci-pre-merge-emploi-temps
description: Audit pre-merge complet pour une PR du chantier emploi-temps — grep canonical patterns + lint Blade compiled + tests pass + visual-check screenshots diff + audit 4 axes
---

# Skill: klassci-pre-merge-emploi-temps

## When to use this skill

- Juste avant un `gh pr create` ou `gh pr merge` sur une PR du chantier emploi-temps LMD unification
- Pour valider qu'une PR est prête à merger sur `presentation`
- Combine `klassci-lmd-bts-audit` + `klassci-test-bts-lmd-matrix` + visual-check + audit 4 axes

## Workflow checklist

### 1. Code hygiene (grep + lint)

```powershell
# Audit canonical patterns LMD/BTS
.\scripts\lmd\audit-callsites.ps1

# Si NOUVEAUX hits BTS-only ajoutés par la PR → BLOQUE merge
```

```bash
# Lint Blade compiled views (catch syntax errors silencieux)
rm storage/framework/views/*.php
php artisan view:cache
for f in storage/framework/views/*.php; do
    php -l "$f" 2>&1 | grep -v "No syntax errors"
done
# Si output non vide → erreur Blade silencieuse, BLOQUE merge
```

```bash
# Détecter <x-au-*> dans commentaires (rule blade-pitfalls Pitfall #3)
grep -rEn '/\*[^*]*<x-[a-z]' resources/views/
grep -rEn '<!--[^>]*<x-[a-z]' resources/views/
grep -rEn '//[^\n]*<x-[a-z]' resources/views/
grep -rEn '\{\{--[^-]*<x-[a-z]' resources/views/
```

### 2. Tests pass

```powershell
# Matrice BTS/LMD complète
.\scripts\lmd\run-bts-lmd-matrix.ps1

# Tests régression spécifiques
php artisan test --filter=VolumeBudgetRegressionShow
php artisan test --filter=SeanceCoursAuditPreserved
php artisan test --filter=BulkEditLmd
```

### 3. Visual-check

```powershell
.\scripts\lmd\visual-check-screenshots.ps1 -Compare -Baseline baseline-2026-05-22-pre
```

Diff screenshots vs baseline. Tout changement visuel attendu (intentionnel par la PR) → mettre à jour baseline. Tout changement inattendu → BLOQUE merge.

### 4. Audit 4 axes (rule `pre-commit-quality-gate.md`)

Re-vérifier mentalement la diff :

| Axe | Question |
|---|---|
| **Architecture** | Pattern existant (MatiereTreeBuilder) honoré ? Pas de god-class aggravée ? |
| **Quality vs Speed** | Tests prévus ? Pas de N+1 ? Pas de copy-paste ? |
| **Production-grade** | Audit log preserve ? rate limiting OK ? secret handling OK ? |
| **SOLID** | OCP extensibilité ? interfaces ? dependency inversion ? |

### 5. Multi-tenant compatibility

```bash
# Si la PR ajoute une migration ou modifie un schema
# Vérifier que la migration a un down() testable
php artisan migrate --pretend
php artisan migrate
php artisan migrate:rollback
php artisan migrate
```

### 6. AJAX no-reload (si UI premium)

```bash
# Détecter window.location.reload() dans les vues touchées
grep -rEn "window.location.reload" resources/views/esbtp/

# Détecter forms sans @submit.prevent
grep -rEn "method=['\"]POST['\"]" resources/views/esbtp/lmd/ | grep -v "@submit.prevent"
```

### 7. Embedded styles (si vue embed-compatible)

```bash
# Détecter @section('styles') dans vues embed
grep -rEl "layouts\.embedded|boolean\('embed'\)" resources/views/ | \
    xargs grep -l "@section('styles')"
# Si hits → fix vers @push('styles') AVANT merge
```

### 8. Documentation

- [ ] CHANGELOG.md interne mis à jour
- [ ] klassci-landing changelog (FR + EN) mis à jour si user-visible
- [ ] Memory files associés mis à jour
- [ ] Rules transverses respectées (no-god-code, premium-redesign, etc.)

### 9. PR description

- Title court (<70 chars)
- Body avec :
  - ## Summary (1-3 bullets)
  - ## Test plan (checkbox liste)
  - Lien master plan doc + PR number
  - Liste tests ajoutés

## Verdict final

- ✅ **GO** : tous les axes PASS → `gh pr merge --admin`
- ⚠️ **GO-WITH-CHANGES** : 1-2 WARN mineurs → fix puis merge
- ❌ **REJECT** : 1+ BLOCK → fix obligatoire AVANT merge

## Output

```markdown
# Pre-merge audit — PR #XXX — 2026-05-22 15:42

## Checks
- [x] Code hygiene
- [x] Tests pass (Matrix 4 combos)
- [x] Visual-check (no unexpected diff)
- [x] 4-axes audit
- [x] Multi-tenant compat
- [x] AJAX no-reload
- [x] Embedded styles
- [x] Documentation

## Verdict : ✅ GO

Ready to merge.
```

## Voir aussi

- Skill : `klassci-lmd-bts-audit`
- Skill : `klassci-test-bts-lmd-matrix`
- Rule globale : `pre-commit-quality-gate.md`
- Rule projet : `pre-merge-checklist.md`
- Rule projet : `feature-delivery-methodology.md`
- Master plan : `docs/MASTER-PLAN-emploi-temps-lmd-unification.md`
