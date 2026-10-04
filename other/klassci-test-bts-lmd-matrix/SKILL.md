---
name: klassci-test-bts-lmd-matrix
description: Exécute la matrice complète de tests BTS/LMD (4 combos × Unit + Feature + Browser) avec rapport tableau croisé pass/fail par combo et par couche
---

# Skill: klassci-test-bts-lmd-matrix

## When to use this skill

- Pré-merge d'une PR qui touche emploi-temps / seances-cours / lmd / bulletin / examens / rattrapage / jury
- Audit post-deploy pour vérifier qu'aucune régression BTS/LMD ne s'est glissée
- Régulièrement (cron quotidien) pour catch les régressions silencieuses

## Matrice 4 combos × 3 couches

```
┌────────────────────┬─────────────────┬─────────────────┬─────────────────┬─────────────────┐
│                    │ BTS pivot       │ BTS pivot       │ LMD avec        │ LMD tronc       │
│                    │ peuplé          │ vide            │ parcours        │ commun mention  │
├────────────────────┼─────────────────┼─────────────────┼─────────────────┼─────────────────┤
│ Unit               │ ✅ ✅ ✅ ✅       │ ✅ ✅ ✅ ✅       │ ✅ ✅ ✅ ✅       │ ✅ ✅ ✅ ✅       │
│ Feature            │ ✅ ✅ ✅ ✅       │ ✅ ✅ ✅ ✅       │ ✅ ✅ ✅ ✅       │ ✅ ✅ ✅ ✅       │
│ Browser            │ ✅ ✅ ✅ ✅       │ ✅ ✅ ✅ ✅       │ ✅ ✅ ✅ ✅       │ ✅ ✅ ✅ ✅       │
└────────────────────┴─────────────────┴─────────────────┴─────────────────┴─────────────────┘
```

## Workflow

### Step 1 — Setup fixtures par combo

```php
// tests/Fixtures/MatieresMatrixFixture.php
class MatieresMatrixFixture
{
    public static function bts_pivot_peuple(): ESBTPClasse
    {
        $classe = ESBTPClasse::factory()->create(['systeme_academique' => 'BTS']);
        $matieres = ESBTPMatiere::factory()->count(5)->create();
        $classe->matieres()->attach($matieres->pluck('id'));  // pivot rempli
        // + planifs cohérentes
        return $classe;
    }

    public static function bts_pivot_vide(): ESBTPClasse
    {
        $classe = ESBTPClasse::factory()->create(['systeme_academique' => 'BTS']);
        // PAS d'attach pivot — mais planifs présentes
        $matieres = ESBTPMatiere::factory()->count(5)->create();
        foreach ($matieres as $m) {
            ESBTPPlanificationAcademique::factory()->create([
                'filiere_id' => $classe->filiere_id,
                'niveau_etude_id' => $classe->niveau_etude_id,
                'matiere_id' => $m->id,
            ]);
        }
        return $classe;
    }

    public static function lmd_avec_parcours(): ESBTPClasse
    {
        $parcours = ESBTPLMDParcours::factory()->create();
        $classe = ESBTPClasse::factory()->create([
            'systeme_academique' => 'LMD',
            'parcours_id' => $parcours->id,
            'filiere_id' => $parcours->filiere_id,
        ]);
        // UEs liées + ECUEs
        // ...
        return $classe;
    }

    public static function lmd_tronc_commun(): ESBTPClasse
    {
        $mention = ESBTPLMDMention::factory()->create();
        $classe = ESBTPClasse::factory()->create([
            'systeme_academique' => 'LMD',
            'parcours_id' => null,
            'filiere_id' => $mention->id,  // filiere_id sert sémantiquement de mention_id (rule classe-lmd-filiere-as-mention)
        ]);
        return $classe;
    }
}
```

### Step 2 — Tests Unit critiques (4 combos)

```php
test('MatiereTreeBuilder::buildForPlanning works for all 4 combos', function () {
    foreach (['bts_pivot_peuple', 'bts_pivot_vide', 'lmd_avec_parcours', 'lmd_tronc_commun'] as $combo) {
        $classe = MatieresMatrixFixture::$combo();
        $planifData = ['matieres_planifiees' => []];

        $result = app(MatiereTreeBuilder::class)->buildForPlanning($planifData, $classe);

        expect($result['matieres_planifiees'])->not->toBeEmpty(
            "Combo $combo: matières devraient être présentes"
        );
    }
});
```

### Step 3 — Tests Feature par vue critique

```php
test('bulkEdit shows matieres for all 4 combos', function () {
    foreach (['bts_pivot_peuple', 'bts_pivot_vide', 'lmd_avec_parcours', 'lmd_tronc_commun'] as $combo) {
        $classe = MatieresMatrixFixture::$combo();
        $emploiTemps = ESBTPEmploiTemps::factory()->for($classe)->create();
        $user = User::factory()->withRole('superAdmin')->create();

        $response = $this->actingAs($user)
            ->get("/esbtp/emploi-temps/bulk-edit?ids={$emploiTemps->id}");

        $response->assertStatus(200);
        $response->assertDontSee('Planification non configurée');
    }
});
```

### Step 4 — Tests Browser E2E sur les 4 combos

```php
test('user can navigate emploi-temps for LMD class without 0 matières', function () {
    $classe = MatieresMatrixFixture::lmd_avec_parcours();
    $emploiTemps = ESBTPEmploiTemps::factory()->for($classe)->create();

    $browser->visit("/esbtp/emploi-temps/{$emploiTemps->id}")
        ->assertSee('Mathématiques')  // matière LMD
        ->click('.tab-suivi-heures')
        ->assertSee('Heures planifiées')
        ->assertDontSee('0 matières disponibles');
});
```

### Step 5 — Rapport tableau croisé

```bash
php artisan test --testsuite=Unit --filter=BtsLmd
php artisan test --testsuite=Feature --filter=BtsLmd
php artisan test --testsuite=Browser --filter=BtsLmd
```

Output script ParsePestResults.ps1 :

```
Matrix Result — 2026-05-22 14:32

| Couche  | BTS pivot peuplé | BTS pivot vide | LMD parcours | LMD tronc commun |
|---------|-------------------|----------------|--------------|------------------|
| Unit    | ✅ 8/8 PASS       | ✅ 8/8 PASS    | ✅ 8/8 PASS  | ✅ 8/8 PASS      |
| Feature | ✅ 12/12 PASS     | ✅ 12/12 PASS  | ✅ 12/12 PASS| ✅ 12/12 PASS    |
| Browser | ✅ 4/4 PASS       | ✅ 4/4 PASS    | ✅ 4/4 PASS  | ✅ 4/4 PASS      |
```

## Quand FAIL

Si un combo fail :
1. Identifier la couche (Unit / Feature / Browser)
2. Identifier la régression (`git bisect` si récent)
3. Reproduire localement avec `--filter=` ciblé
4. Fix + ré-exécuter

## Voir aussi

- Script : `scripts/lmd/run-bts-lmd-matrix.ps1`
- Master plan : `docs/MASTER-PLAN-emploi-temps-lmd-unification.md` (section Tests)
- Rule projet : `pre-merge-checklist.md`
- Rule projet : `lmd-bts-matieres-single-source.md`
