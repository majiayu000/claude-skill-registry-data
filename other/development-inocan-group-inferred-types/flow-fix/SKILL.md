---
name: flow-fix
description: Corriger un bug ou etendre un flow d'automatisation existant. (project)
---

# flow-fix

Corrige un bug ou etend un flow d'automatisation existant.

## Declenchement

```
/flow-fix {platform} {product} "{description}"
```

Exemples :
- `/flow-fix alptis sante-select "Le dropdown ville ne se remplit plus"`
- `/flow-fix swisslifeone slsis "Ajouter support pour 3+ enfants"`
- `/flow-fix alptis sante-pro-plus "Erreur sur leads TNS"`

---

## Journal de bord

**IMPORTANT** : Tout au long du processus, maintenir un fichier journal qui documente chaque action.

### Fichier journal
```
.claude/flow-logs/{platform}-{product}-fix-{slug}.md
```

### Format du journal

```markdown
# Journal de fix : {platform} {product}

**Probleme** : {description originale}
**Debut** : {date et heure}
**Branche** : fix/{platform}-{product}-{slug}
**Status** : EN COURS | TERMINE | BLOQUE

---

## Phase 1 : Diagnostic
**Debut** : {timestamp}

### Reproduction du probleme
- Test LEAD_INDEX=0 : PASS
- Test LEAD_INDEX=1 : FAIL
- Test LEAD_INDEX=2 : PASS

### Lead problematique identifie
- Lead #1 : Jean DUPONT
- Caracteristiques : TNS, profession "consultant senior"

### Analyse des logs
```
Error: Unable to find element matching selector "#profession-select"
  at Section2Fill.fillProfession (Section2Fill.ts:45)
```

### Cause identifiee
**Type** : Selector casse
**Fichier** : `selectors/section2.ts`
**Ligne** : 23
**Detail** : L'ID du dropdown profession a change de "#profession-select" vers "#categories-socio-professionnelles-adherent"

**Fin** : {timestamp}
**Duree** : 8 min

---

## Phase 2 : Correction
**Debut** : {timestamp}

### Fichiers modifies
1. `src/main/flows/platforms/{platform}/products/{product}/steps/form-fill/selectors/section2.ts`
   - Ligne 23 : Changement du selector profession
   - Ajout d'un selector alternatif

### Code modifie
```typescript
// AVANT
profession: {
  primary: '#profession-select',
  stability: 'UNSTABLE',
},

// APRES
profession: {
  primary: '#categories-socio-professionnelles-adherent',
  alternative: "select[name*='profession']",
  stability: 'STABLE',
},
```

**Fin** : {timestamp}
**Duree** : 5 min
**Commit** : fix(alptis/sante-select): update profession selector

---

## Phase 3 : Validation
**Debut** : {timestamp}

### Test cas specifique
- LEAD_INDEX=1 : PASS

### Bulk validation
- Premier run : 22/22 PASS
- Non-regression : OK

**Fin** : {timestamp}
**Duree** : 3 min
**Commit** : test(alptis/sante-select): verify fix with bulk validation

---

## Phase 4 : Finalisation
**Debut** : {timestamp}

### Resume
- **Probleme** : Selector profession casse
- **Cause** : Changement d'ID sur le site Alptis
- **Solution** : Mise a jour du selector avec alternative
- **Impact** : Aucune regression

### Tests finaux
- Lead specifique : PASS
- Bulk validation : 22/22 PASS
- Non-regression : PASS

**Fin** : {timestamp}
**Status** : PRET POUR MERGE

---

## Resume
- **Temps total** : 18 min
- **Commits** : 2
- **Fichiers modifies** : 1
- **Tests** : 22/22 PASS
- **Status** : TERMINE
```

### Regles du journal

1. **Creer le fichier au debut** de la Phase 1
2. **Mettre a jour en temps reel** a chaque action
3. **Documenter la cause** du probleme en detail
4. **Inclure le code modifie** (avant/apres)
5. **Noter tous les resultats de tests**
6. **Conserver le journal** meme apres merge (historique)

---

## Workflow

### Phase 1 : Diagnostic

1. **Creer la branche de fix**
   ```bash
   # Slug = 3-4 premiers mots de la description, kebab-case
   git checkout -b fix/{platform}-{product}-{slug}
   ```

   Exemples :
   - `fix/alptis-sante-select-dropdown-ville`
   - `fix/swisslifeone-slsis-support-3-enfants`

2. **Reproduire le probleme** (headless)
   ```bash
   LEAD_INDEX=0 npx playwright test e2e/{platform}/{product}/single-lead-journey.spec.ts
   ```

   Si le test passe, essayer avec d'autres leads :
   ```bash
   LEAD_INDEX=1 npx playwright test e2e/{platform}/{product}/single-lead-journey.spec.ts
   LEAD_INDEX=2 npx playwright test e2e/{platform}/{product}/single-lead-journey.spec.ts
   ```

3. **Identifier la cause**

   | Symptome | Cause probable | Fichiers a verifier |
   |----------|---------------|---------------------|
   | Element not found | Selector casse | `platforms/{platform}/products/{product}/steps/form-fill/selectors/*.ts` |
   | Wrong value selected | Mapper incorrect | `platforms/{platform}/products/{product}/transformers/mappers/*.ts` |
   | Validation error | Transformer ou validator | `transformers/LeadTransformer.ts`, `validators/*.ts` |
   | Timeout | Timing issue | `steps/form-fill/operations/*.ts`, config timeouts |
   | Champ manquant | Nouveau champ sur le formulaire | Cartographie + selectors |
   | Test passe mais mauvaise valeur | Verifier le mapping | `mappers/*.ts`, `LeadTransformer.ts` |

4. **Analyser les logs**
   ```bash
   # Les screenshots sont captures en cas d'erreur
   ls -la test-results/
   ls -la artifacts/
   ```

5. **Inspecter le formulaire si necessaire** (headless)
   ```bash
   npx playwright test e2e/{platform}/{product}/.detailed/explore-selectors.spec.ts
   ```

---

### Phase 2 : Correction

**Appliquer le fix minimal** selon le cas identifie :

#### Cas 1 : Selector casse

Le site a change et l'ID ou la classe n'existe plus.

```typescript
// selectors/section2.ts

// AVANT (UUID qui a change)
nom: {
  primary: '#f2d8ce6f-b18a-4f27-900d-1c10eb9bf440',
  stability: 'UNSTABLE',
},

// APRES (selector plus stable)
nom: {
  primary: "input[class*='totem-input__input'][placeholder*='nom']",
  alternative: "label:has-text('Nom') + input",
  fallback: "#nom",
  stability: 'MODERATE',
},
```

**Fichiers a modifier :**
- `src/main/flows/platforms/{platform}/products/{product}/steps/form-fill/selectors/*.ts`

#### Cas 2 : Mapper incorrect

Une valeur du lead n'est pas correctement mappee.

```typescript
// mappers/profession-mapper.ts

const PROFESSION_MAPPING: Record<string, string> = {
  // ...existing mappings

  // AJOUTER le nouveau cas
  'consultant independant': 'PROFESSIONS_LIBERALES',
  'auto-entrepreneur': 'ARTISANS_COMMERCANTS',
};
```

**Fichiers a modifier :**
- `src/main/flows/platforms/{platform}/products/{product}/transformers/mappers/*.ts`

#### Cas 3 : Timing issue

Le formulaire a besoin de plus de temps pour charger.

```typescript
// operations/DropdownOperations.ts

// AVANT
await page.click(selector);
await page.waitForTimeout(300);

// APRES (attente explicite)
await page.click(selector);
await page.waitForSelector('.dropdown-options', { state: 'visible', timeout: 5000 });
await page.waitForTimeout(500); // Animation
```

**Fichiers a modifier :**
- `src/main/flows/platforms/{platform}/products/{product}/steps/form-fill/operations/*.ts`
- `src/main/flows/config/{platform}.config.ts` (pour les timeouts globaux)

#### Cas 4 : Nouveau champ sur le formulaire

Le site a ajoute un nouveau champ obligatoire.

1. **Mettre a jour la cartographie** :
   ```json
   // cartography/{platform}/{platform}-{product}-exhaustive-mapping.json
   {
     "fields": [
       // ... existing
       {
         "field_id": "nouveau_champ",
         "section": "Section X",
         "type": "text",
         "selector": {
           "primary": "#nouveau-champ",
           "stability": "STABLE"
         },
         "validation": { "required": true }
       }
     ]
   }
   ```

2. **Ajouter le selector** :
   ```typescript
   // selectors/sectionX.ts
   export const SECTION_X_SELECTORS = {
     // ... existing
     nouveau_champ: {
       primary: '#nouveau-champ',
       stability: 'STABLE',
     },
   };
   ```

3. **Etendre les types** :
   ```typescript
   // transformers/types.ts
   export type FormData = {
     // ... existing
     nouveau_champ?: string;
   };
   ```

4. **Mettre a jour le transformer** :
   ```typescript
   // transformers/LeadTransformer.ts
   return {
     // ... existing
     nouveau_champ: lead.subscriber.nouveau_champ ?? 'valeur_defaut',
   };
   ```

5. **Mettre a jour le SectionFill** :
   ```typescript
   // sections/SectionXFill.ts
   if (data.nouveau_champ) {
     await page.locator(SELECTORS.nouveau_champ.primary).fill(data.nouveau_champ);
   }
   ```

**Fichiers a modifier :**
- `src/main/flows/cartography/{platform}/*.json`
- `src/main/flows/platforms/{platform}/products/{product}/steps/form-fill/selectors/*.ts`
- `src/main/flows/platforms/{platform}/products/{product}/transformers/types.ts`
- `src/main/flows/platforms/{platform}/products/{product}/transformers/LeadTransformer.ts`
- `src/main/flows/platforms/{platform}/products/{product}/steps/form-fill/sections/*.ts`

#### Cas 5 : Extension (nouveau cas d'usage)

Exemple : supporter 3+ enfants au lieu de 2.

1. **Identifier les limites actuelles**
2. **Modifier la logique dans FormFillOrchestrator**
3. **Ajouter des tests pour le nouveau cas**
4. **Generer des leads de test si necessaire**

COMMIT : `fix({platform}/{product}): {description courte}`

---

### Phase 3 : Validation

1. **Tester le cas specifique** (headless)
   ```bash
   LEAD_INDEX={index_du_lead_problematique} npx playwright test e2e/{platform}/{product}/single-lead-journey.spec.ts
   ```

2. **Non-regression : bulk test** (headless)
   ```bash
   npx playwright test e2e/{platform}/{product}/bulk-validation.spec.ts
   ```

3. **Si modification dans du code partage** (engine, config commune) :
   ```bash
   # Tester TOUS les flows affectes
   npx playwright test e2e/alptis/sante-select/bulk-validation.spec.ts
   npx playwright test e2e/alptis/sante-pro-plus/bulk-validation.spec.ts
   npx playwright test e2e/swisslifeone/slsis/bulk-validation.spec.ts
   ```

COMMIT : `test({platform}/{product}): verify fix with bulk validation`

---

### Phase 4 : Finalisation

Quand tous les tests passent :

```
Fix applique pour {platform}_{product}.

Probleme: {description originale}
Cause: {cause identifiee}
Solution: {description de la solution}

Tests:
- Lead specifique: PASS
- Bulk validation: {n}/{n} PASS
- Non-regression: PASS

Prochaine etape: merge de la branche
```

Demander a l'utilisateur s'il veut :
1. Merger la branche
2. Voir les details du fix
3. Faire des ajustements supplementaires

---

## Patterns de debug courants

### Ajouter des logs
```typescript
logger?.debug('Filling field', { selector, value, fieldIndex });
logger?.info('Section completed', { sectionName, duration });
```

### Prendre un screenshot pour debug
```typescript
await page.screenshot({ path: `debug-${stepId}-${Date.now()}.png` });
```

### Afficher l'etat du DOM
```typescript
const html = await page.locator(selector).innerHTML();
console.log('DOM state:', html);
```

### Verifier existence et visibilite
```typescript
const count = await page.locator(selector).count();
const isVisible = await page.locator(selector).isVisible();
console.log({ selector, count, isVisible });
```

### Inspecter tous les elements similaires
```typescript
const inputs = await page.locator('input').all();
for (const [i, input] of inputs.entries()) {
  const id = await input.getAttribute('id');
  const name = await input.getAttribute('name');
  const visible = await input.isVisible();
  console.log(`Input ${i}: id=${id}, name=${name}, visible=${visible}`);
}
```

---

## Fichiers de reference

| Type | Fichier |
|------|---------|
| Selectors | `src/main/flows/platforms/alptis/products/sante-pro-plus/steps/form-fill/selectors/` |
| Mappers | `src/main/flows/platforms/alptis/products/sante-pro-plus/transformers/mappers/` |
| Operations | `src/main/flows/platforms/alptis/products/sante-pro-plus/steps/form-fill/operations/` |
| Transformer | `src/main/flows/platforms/alptis/products/sante-pro-plus/transformers/LeadTransformer.ts` |
| Verification helpers | `e2e/alptis/helpers/verification/` |
| Config timeouts | `src/main/flows/config/alptis.config.ts` |
| Cartographie | `src/main/flows/cartography/alptis/alptis-sante-select-exhaustive-mapping.json` |

---

## Conventions

### Format branche
```
fix/{platform}-{product}-{slug}
```
Le slug = 3-4 premiers mots de la description, en kebab-case.

### Format commits
```
fix({platform}/{product}): {description courte}

- Detail du probleme
- Solution appliquee

Generated with Claude Code

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

---

## Checklist

- [ ] Branche `fix/{platform}-{product}-{slug}` creee
- [ ] Probleme reproduit
- [ ] Cause racine identifiee
- [ ] Fix minimal applique
- [ ] Test du cas specifique: PASS (headless)
- [ ] Bulk validation: 100% PASS (headless)
- [ ] Non-regression verifiee (si code partage)
- [ ] Commits descriptifs
- [ ] Cartographie mise a jour (si nouveau champ)
