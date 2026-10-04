---
name: klassci-emploi-temps-deploy
description: Déploiement coordonné cross-branch + pull + cache:clear + migrate + permissions:fix sur les 6 tenants KLASSCI en 1 commande, avec dry-run + rollback automatique en cas d'échec
---

# Skill: klassci-emploi-temps-deploy

## When to use this skill

- Après merge d'une PR sur `presentation` qui doit être propagée aux 5 autres tenants
- Pour un rollback d'urgence sur 1 ou plusieurs tenants
- Pour exécuter la séquence complète : push + pull + cache:clear + migrate + smoke tests

## Workflow

### Step 0 — Pré-requis

```bash
# Vérifier que les 6 tenants sont config dans klassci-cli
klassci config:list

# Si esbtp-yakro, hetec, ephrata manquent → les ajouter
klassci config:set-token <tenant> <URL> <TOKEN>
```

### Step 1 — Dry-run obligatoire

```powershell
.\scripts\lmd\deploy-coordinated.ps1 -DryRun -Tenants @('presentation', 'esbtp-abidjan')
```

Vérifier la sortie : aucune commande destructive sans confirmation.

### Step 2 — Déploiement coordonné

```powershell
# 1. Push presentation (si pas déjà fait)
git push origin presentation

# 2. Cross-branch push (séquentiel pour catch erreurs précoces)
$tenants = @('esbtp-abidjan', 'esbtp-yakro', 'ephrata', 'hetec', 'rostan')
foreach ($t in $tenants) {
    Write-Host "=== Cross-branch push to $t ===" -ForegroundColor Cyan
    git push origin presentation:$t
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Push failed for $t — abort" -ForegroundColor Red
        exit 1
    }
}

# 3. Pull + cache:clear sur les 6 tenants
$allTenants = @('presentation', 'esbtp-abidjan', 'esbtp-yakro', 'ephrata', 'hetec', 'rostan')
foreach ($t in $allTenants) {
    Write-Host "=== Deploy to $t ===" -ForegroundColor Cyan
    klassci pull $t
    if ($LASTEXITCODE -ne 0) {
        Write-Host "⚠️ Pull failed for $t — manual intervention" -ForegroundColor Yellow
        continue
    }
    klassci cache:clear $t
    if ($LASTEXITCODE -ne 0) {
        Write-Host "⚠️ cache:clear failed for $t — manual intervention" -ForegroundColor Yellow
        continue
    }
}
```

### Step 3 — Migrations (si applicable)

```powershell
foreach ($t in $allTenants) {
    Write-Host "=== Migrate $t (dry-run first) ===" -ForegroundColor Cyan
    klassci migrate $t --dry-run
    if ($LASTEXITCODE -eq 0) {
        klassci migrate $t
    }
}
```

### Step 4 — Permissions fix

```powershell
foreach ($t in $allTenants) {
    klassci permissions:fix $t
}
```

### Step 5 — Smoke tests

```powershell
.\scripts\lmd\post-deploy-smoke-test.ps1 -AllTenants
```

Vérifier sortie : aucun 500 sur les routes critiques (/login, /esbtp/emploi-temps, /esbtp/lmd/planning, /esbtp/lmd/jurys).

### Step 6 — Visual-check (optionnel mais recommandé)

```powershell
.\scripts\lmd\visual-check-screenshots.ps1 -Compare
```

Compare screenshots vs baseline. Toute différence visuelle inattendue → investigation.

## Rollback en cas d'échec

### Rollback simple (revert PR sur presentation)

```bash
# Trouver le commit pré-merge
git log presentation --oneline -10

# Revert sur presentation
git checkout presentation
git revert <commit-merge> --no-edit
git push origin presentation

# Cross-branch revert aux 5 autres tenants
$tenants = @('esbtp-abidjan', 'esbtp-yakro', 'ephrata', 'hetec', 'rostan')
foreach ($t in $tenants) {
    git push origin presentation:$t
}

# Re-deploy 6 tenants
foreach ($t in @('presentation', $tenants)) {
    klassci pull $t
    klassci cache:clear $t
}
```

### Rollback un tenant spécifique seul

```bash
# Si un tenant a un bug spécifique, force-push à un commit antérieur
git push origin <commit-pre-deploy>:tenant-X --force-with-lease

# Pull sur ce tenant
klassci pull tenant-X
klassci cache:clear tenant-X
```

## Voir aussi

- Script : `scripts/lmd/deploy-coordinated.ps1`
- Script : `scripts/lmd/post-deploy-smoke-test.ps1`
- Script : `scripts/lmd/visual-check-screenshots.ps1`
- Rule projet : `tenant-branches.md`
- Rule globale : `multi-agent-git-safety.md` (commandement 13)
- Master plan : `docs/MASTER-PLAN-emploi-temps-lmd-unification.md` (PR17)
