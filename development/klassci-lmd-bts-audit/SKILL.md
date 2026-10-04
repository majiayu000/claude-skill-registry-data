---
name: klassci-lmd-bts-audit
description: Audit complet des sites consommateurs de matières d'une classe — grep canonical patterns (whereHas filieres/niveaux, $classe->matieres direct) + verdict LMD-aware ou BTS-only, génère rapport tableau croisé
---

# Skill: klassci-lmd-bts-audit

## When to use this skill

- Avant de coder une nouvelle vue qui liste les matières d'une classe
- Après un refactor multi-controllers pour vérifier qu'aucun nouveau hardcode BTS-only ne s'est glissé
- En pré-merge audit (rule `pre-merge-checklist.md`) pour un PR qui touche les controllers emploi-temps / seances-cours / bulletins / notes
- Pour suivre la progression de la rule `lmd-bts-matieres-single-source.md`

## Workflow

### Step 1 — Grep canonical patterns

```bash
# Pattern 1 : $classe->matieres direct (BTS-only)
grep -rEn '\$classe->matieres\b' app/Http/Controllers/

# Pattern 2 : whereHas('filieres') sur ESBTPMatiere (BTS-only)
grep -rEn "whereHas\\('filieres'\\)" app/Http/Controllers/

# Pattern 3 : whereHas('niveaux') sur ESBTPMatiere (souvent BTS-only)
grep -rEn "whereHas\\('niveaux'\\)" app/Http/Controllers/

# Pattern 4 : Source canonique correctement utilisée (LMD-aware)
grep -rEn "MatiereTreeBuilder|loadLmdMatieresForClasse" app/Http/Controllers/

# Pattern 5 : ESBTPPlanificationAcademique direct
grep -rEn "ESBTPPlanificationAcademique" app/Http/Controllers/
```

### Step 2 — Pour chaque hit, déterminer le verdict

Lire le contexte (5-10 lignes autour) et classer :

- **✅ LMD-aware** : utilise `MatiereTreeBuilder` OU applique override conditionnel `if ($classe->systeme_academique === 'LMD')`
- **⚠️ Hybride** : a un fallback BTS legacy mais le primaire utilise `ESBTPPlanificationAcademique`
- **❌ BTS-only** : utilise `whereHas('filieres')` direct sans override LMD, ou `$classe->matieres` sans check

### Step 3 — Générer rapport tableau

Format tableau Markdown :

```markdown
## Audit LMD/BTS — {{ date }}

| File:Line | Pattern | Verdict | Action |
|---|---|---|---|
| ESBTPEmploiTempsController:711 | getPlanificationDataForClasse | ❌ BTS-only | PR2 : appliquer override LMD |
| ESBTPEmploiTempsController:871 | getPlanificationDataForClasse + override | ✅ LMD-aware | OK |
| ESBTPSeanceCoursController:229 | getPlanificationDataForClasse + override | ✅ LMD-aware | OK |
| ESBTPSeanceCoursController:828 | getPlanificationDataForClasse | ❌ BTS-only | PR3 : appliquer override LMD |
| ESBTPEmploiTempsController:1492 | whereHas('filieres') BTS-only | ❌ BTS-only | PR3 : refactor MatiereTreeBuilder |
| ESBTPBulletinController:184 | $classe->matieres direct | ❌ BTS-only (guard PR7) | PR7 : abort_if LMD |
| ESBTPBulletinController:874 | $classe->matieres direct | ❌ BTS-only (guard PR7) | PR7 : abort_if LMD |
| ESBTPBulletinController:1189 | $classe->matieres() direct | ❌ BTS-only (guard PR7) | PR7 : abort_if LMD |
| ESBTPAttendanceController:1871 | getMatieresClasse() helper | ✅ LMD-aware | OK |

**Score** : X/Y LMD-aware (XX%)
```

### Step 4 — Suggérer fixes

Pour chaque site `❌`, proposer le diff exact (avant/après) :

```php
// AVANT (BTS-only)
$matieresLiees = ESBTPMatiere::where('is_active', true)
    ->whereHas('filieres', fn ($q) => $q->where('esbtp_filieres.id', $classe->filiere_id))
    ->whereHas('niveaux', fn ($q) => $q->where('esbtp_niveau_etudes.id', $classe->niveau_etude_id))
    ->get();

// APRÈS (LMD-aware via service)
$planificationData = $this->getPlanificationDataForClasse($classe, $annee, $semestre);
if (($classe->systeme_academique ?? '') === 'LMD') {
    $planificationData = app(MatiereTreeBuilder::class)
        ->buildForPlanning($planificationData, $classe);
}
$matieresLiees = collect($planificationData['matieres_planifiees'] ?? []);
```

### Step 5 — Vérifier exécution

Si possible, créer une migration de test data + lancer un test Feature qui assertSee les matières d'une classe LMD :

```php
// tests/Feature/Audit/LmdMatieresVisibleTest.php
test('all controllers return matieres for LMD classes', function () {
    // ... seed LMD classe + planifs ...
    // Visit toutes les routes critiques
    // assertSee matiere name dans response
});
```

## Output attendu

Un fichier Markdown `tmp/audit-lmd-bts-{{ date }}.md` avec :
- Tableau des sites
- Score global
- Diffs suggérés pour chaque site bugged
- Liste des memoires/rules à consulter

## Voir aussi

- Rule projet : `.claude/rules/lmd-bts-matieres-single-source.md`
- Memory : `feedback_matiere_tree_builder_canonical.md`
- Script : `scripts/lmd/audit-callsites.ps1` (version PowerShell automatisée)
- Master plan : `docs/MASTER-PLAN-emploi-temps-lmd-unification.md`
