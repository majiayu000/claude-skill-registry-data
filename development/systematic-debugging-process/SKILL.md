---
name: Systematic Debugging Process
description: Processus de debugging systématique une fois la cause identifiée. MANDATORY pour bug fixing. À utiliser lors de correction de bugs, debugging, ou quand l'utilisateur demande de "corriger", "debugger", "réparer un bug".
allowed-tools: [Read, Edit, Write, Bash, Grep, Glob]
---

# Systematic Debugging Process

## 🎯 Mission

Appliquer un **processus de debugging systématique** pour corriger un bug de manière robuste et éviter sa réapparition.

## 🧐 Philosophie

**Debugging ≠ Quick Fix**

Un bon debugging :
1. ✅ Confirme la cause racine
2. ✅ Applique un fix minimal
3. ✅ Ajoute des protections (tests, guards, validations)
4. ✅ Documente la vraie cause
5. ✅ Évite la réapparition du bug

## 📋 Processus de Debugging en 10 Étapes

### Étape 1: Définir le Comportement Observé

**Objectif**: Documenter précisément le bug avant toute intervention.

**Template**:
```markdown
## Bug Definition

**Comportement Observé**:
[Description précise du bug]

**Environnement**:
- OS: [macOS, Linux, Windows]
- Browser: [Chrome, Safari, Firefox]
- Version: [Backend version, Frontend version]
- Database: [PostgreSQL version]

**Reproduction Steps**:
1. [Action 1]
2. [Action 2]
3. [Action 3]
→ Bug occurs

**Expected Behavior**:
[Ce qui devrait se passer]

**Actual Behavior**:
[Ce qui se passe réellement]

**Impact**:
- Severity: [Critical, High, Medium, Low]
- User Impact: [Bloquant, Gênant, Mineur]
- Business Impact: [Description]
```

**Exemple**:
```markdown
## Bug Definition

**Comportement Observé**:
Lors de la création d'un club, le formulaire se soumet mais aucun club n'est créé en base de données.

**Environnement**:
- OS: macOS 14
- Browser: Chrome 120
- Backend: v1.2.0
- Database: PostgreSQL 15

**Reproduction Steps**:
1. Se connecter en tant que Coach
2. Aller sur /signup/coach/club
3. Remplir le formulaire (nom, description)
4. Cliquer sur "Créer le club"
→ Bug: Requête retourne 201 mais aucune donnée en DB

**Expected Behavior**:
Club créé en base de données et redirection vers dashboard

**Actual Behavior**:
201 Created retourné, mais SELECT sur clubs table retourne 0 résultats

**Impact**:
- Severity: Critical
- User Impact: Bloquant (impossible de créer un club)
- Business Impact: Onboarding cassé pour tous les nouveaux coaches
```

### Étape 2: Reproduire le Bug Localement

**Objectif**: S'assurer de pouvoir reproduire le bug de manière fiable.

**Actions**:
1. Suivre les étapes de reproduction exactes
2. Observer le bug se produire
3. Noter toute variation ou condition nécessaire
4. Créer un test reproductible si possible

**Test Reproductible**:
```typescript
// tests/e2e/club-creation.spec.ts

describe('Club Creation Bug', () => {
  it('should create club in database when form is submitted', async () => {
    // Arrange
    const clubData = {
      name: 'Test Club',
      description: 'Test Description',
    };

    // Act
    const response = await request(app)
      .post('/api/clubs')
      .set('Authorization', `Bearer ${validToken}`)
      .send(clubData)
      .expect(201);

    // Assert - Vérifier que le club existe en DB
    const clubInDb = await prisma.club.findUnique({
      where: { id: response.body.id },
    });

    expect(clubInDb).toBeDefined();
    expect(clubInDb.name).toBe(clubData.name);
  });
});
```

### Étape 3: Formuler les 2-3 Causes Racines Probables

**Objectif**: Identifier les causes les plus probables (déjà fait avec bug-finder).

**Template**:
```markdown
## Root Causes (Prioritized)

### Cause #1: [Description] - Likelihood: 80%
**Hypothesis**: [Explication de pourquoi]
**Evidence**: [Preuves observées]
**Location**: [Fichier(s) + ligne(s)]

### Cause #2: [Description] - Likelihood: 50%
**Hypothesis**: [...]
**Evidence**: [...]
**Location**: [...]

### Cause #3: [Description] - Likelihood: 20%
**Hypothesis**: [...]
**Evidence**: [...]
**Location**: [...]
```

### Étape 4: Prioriser par Probabilité et Impact

**Objectif**: Décider dans quel ordre investiguer les causes.

**Matrice de Priorisation**:
```
Impact / Likelihood    | High (80%+) | Medium (50-80%) | Low (<50%)
-----------------------|-------------|-----------------|------------
Critical (Bloquant)    | P0          | P1              | P2
High (Gênant)          | P1          | P2              | P3
Medium (Mineur)        | P2          | P3              | P3
```

**Ordre d'Investigation**: P0 → P1 → P2 → P3

**Exemple**:
```markdown
## Investigation Priority

1. **P0**: Cause #1 (Transaction non committée) - Critical + 80% likelihood
2. **P1**: Cause #2 (Mapper retourne undefined) - Critical + 50% likelihood
3. **P3**: Cause #3 (Race condition) - Critical + 20% likelihood

**Plan**: Investiguer Cause #1 en premier.
```

### Étape 5: Log et Inspecter les Changements d'État

**Objectif**: Ajouter des logs stratégiques pour observer le comportement réel.

**Où Logger**:
1. **Avant** l'opération critique
2. **Après** l'opération critique
3. **Dans** les blocs catch
4. **Aux** points de transition (Controller → Handler → Repository)

**Pattern de Logs**:
```typescript
// ✅ BON - Logs structurés avec contexte

export class CreateClubHandler {
  async execute(command: CreateClubCommand): Promise<string> {
    console.log('[CreateClubHandler] START', {
      commandId: command.id,
      clubName: command.name,
      userId: command.userId,
    });

    try {
      // Log avant création entity
      console.log('[CreateClubHandler] Creating domain entity');
      const club = Club.create(command.name, command.description, command.userId);
      console.log('[CreateClubHandler] Domain entity created', { clubId: club.getId() });

      // Log avant save
      console.log('[CreateClubHandler] Saving to repository');
      const savedClub = await this.clubRepository.create(club);
      console.log('[CreateClubHandler] Saved successfully', {
        clubId: savedClub.getId(),
        clubName: savedClub.getName().getValue(),
      });

      // Log après save
      console.log('[CreateClubHandler] Verifying save...');
      const verification = await this.clubRepository.findById(savedClub.getId());
      console.log('[CreateClubHandler] Verification result', {
        found: !!verification,
        id: verification?.getId(),
      });

      return savedClub.getId();
    } catch (error) {
      console.error('[CreateClubHandler] ERROR', {
        error: error.message,
        stack: error.stack,
        command,
      });
      throw error;
    }
  }
}
```

**CRITICAL**: Supprimer tous les logs de debug avant de commit.

### Étape 6: Binary Search pour Réduire la Cause

**Objectif**: Utiliser la technique de binary search pour isoler le problème.

**Méthode**:
1. Identifier le point de départ (entrée) et point d'arrivée (sortie)
2. Tester le milieu du flow
3. Selon résultat, éliminer la moitié du flow
4. Répéter jusqu'à isoler la ligne/fonction exacte

**Exemple**:
```markdown
## Binary Search Process

**Flow Complet**:
Controller → Handler → Entity Creation → Repository → Mapper → Prisma → DB

**Iteration 1**: Test au milieu (Repository)
- Log avant: clubRepository.create()
- Log après: clubRepository.create()
→ Result: Log "avant" OK, Log "après" OK
→ Conclusion: Problème APRÈS repository (Mapper ou Prisma ou DB)

**Iteration 2**: Test Mapper
- Log avant: ClubMapper.toPrisma()
- Log après: ClubMapper.toPrisma()
→ Result: Log "avant" OK, Log "après" retourne undefined
→ Conclusion: Problème dans ClubMapper.toPrisma()

**Iteration 3**: Inspect ClubMapper.toPrisma()
- Line 42: return undefined si club.getSubscription() est null
→ ROOT CAUSE FOUND: Mapper ne gère pas le cas subscription null
```

### Étape 7: Écrire un Test Qui Fail

**Objectif**: Créer un test reproductible avant de fixer.

**Pattern**:
```typescript
// tests/unit/infrastructure/persistence/mappers/club.mapper.spec.ts

describe('ClubMapper', () => {
  describe('toPrisma()', () => {
    it('should handle club without subscription', () => {
      // Arrange
      const club = new Club(
        'club-123',
        ClubName.create('Test Club'),
        'Description',
        'user-123',
        null // Subscription is null
      );

      // Act
      const prismaData = ClubMapper.toPrisma(club);

      // Assert
      expect(prismaData).toBeDefined();
      expect(prismaData.name).toBe('Test Club');
      expect(prismaData.subscriptionId).toBeNull(); // Should handle null subscription
    });
  });
});
```

**Vérifier que le test FAIL**:
```bash
yarn test club.mapper.spec.ts

# Output:
# FAIL  ClubMapper › toPrisma() › should handle club without subscription
# Expected: defined
# Received: undefined
```

### Étape 8: Fixer avec Changement Minimal

**Objectif**: Appliquer le fix le plus simple et le plus ciblé possible.

**Principes**:
- ✅ **Minimal**: Changer uniquement ce qui est nécessaire
- ✅ **Focalisé**: Une seule responsabilité
- ✅ **Lisible**: Code clair et explicite
- ✅ **Testé**: Le test doit passer

**Exemple de Fix**:
```typescript
// infrastructure/persistence/mappers/club.mapper.ts

export class ClubMapper {
  static toPrisma(club: Club): Prisma.ClubCreateInput {
    // ❌ AVANT (bug)
    return {
      id: club.getId(),
      name: club.getName().getValue(),
      description: club.getDescription(),
      subscriptionId: club.getSubscription().getId(), // Crash si null
      userId: club.getUserId(),
    };

    // ✅ APRÈS (fix minimal)
    return {
      id: club.getId(),
      name: club.getName().getValue(),
      description: club.getDescription(),
      subscriptionId: club.getSubscription()?.getId() ?? null, // Handle null
      userId: club.getUserId(),
    };
  }
}
```

### Étape 9: Vérifier et Run Full Test Suite

**Objectif**: S'assurer que le fix ne casse rien d'autre.

**Actions**:
1. Vérifier que le test créé à l'étape 7 passe maintenant
2. Run toute la suite de tests
3. Vérifier qu'aucun test n'est cassé
4. Vérifier la couverture de code

**Commandes**:
```bash
# Test spécifique
yarn test club.mapper.spec.ts
# ✅ PASS  ClubMapper › toPrisma() › should handle club without subscription

# Full test suite
yarn test

# Coverage
yarn test:cov
```

### Étape 10: Ajouter Protection

**Objectif**: Empêcher le bug de réapparaître à l'avenir.

**Types de Protection**:
1. **Tests**: Tests unitaires, intégration, E2E
2. **Guards**: Runtime checks, type guards
3. **Validations**: Input validation, domain validation
4. **Documentation**: Commentaires sur edge cases

**Exemples**:

**Protection 1 - Tests**:
```typescript
// Tests complets pour edge cases
describe('ClubMapper', () => {
  it('should handle club without subscription', () => { /* ... */ });
  it('should handle club with subscription', () => { /* ... */ });
  it('should handle club with null description', () => { /* ... */ });
  it('should throw if club ID is missing', () => { /* ... */ });
});
```

**Protection 2 - Type Guard**:
```typescript
// domain/entities/club.entity.ts

export class Club {
  getSubscription(): Subscription | null {
    return this.subscription;
  }

  // Guard method
  hasSubscription(): boolean {
    return this.subscription !== null;
  }

  // Usage in mapper
  static toPrisma(club: Club): Prisma.ClubCreateInput {
    return {
      // ...
      subscriptionId: club.hasSubscription()
        ? club.getSubscription()!.getId()
        : null,
    };
  }
}
```

**Protection 3 - Validation**:
```typescript
// application/commands/create-club/create-club.handler.ts

export class CreateClubHandler {
  async execute(command: CreateClubCommand): Promise<string> {
    // Validation explicite
    if (!command.userId) {
      throw new ValidationException('User ID is required');
    }

    if (!command.name || command.name.trim().length === 0) {
      throw new ValidationException('Club name cannot be empty');
    }

    // ... reste du code
  }
}
```

**Protection 4 - Documentation**:
```typescript
// infrastructure/persistence/mappers/club.mapper.ts

export class ClubMapper {
  /**
   * Converts a domain Club entity to Prisma format.
   *
   * IMPORTANT: This mapper handles clubs without subscriptions.
   * When a club is first created, it may not have a subscription yet.
   * The subscriptionId field will be null in this case.
   *
   * @param club - Domain Club entity
   * @returns Prisma ClubCreateInput
   */
  static toPrisma(club: Club): Prisma.ClubCreateInput {
    return {
      id: club.getId(),
      name: club.getName().getValue(),
      description: club.getDescription(),
      subscriptionId: club.getSubscription()?.getId() ?? null,
      userId: club.getUserId(),
    };
  }
}
```

### Documentation de la Cause Racine

**Objectif**: Documenter pour l'équipe et pour l'avenir.

**Template**:
```markdown
## Root Cause Analysis

**Bug**: [Description courte]

**Root Cause**: [Cause racine identifiée]

**Why It Happened**:
[Explication de pourquoi le bug s'est produit]

**Fix Applied**:
[Description du fix]

**Prevention Measures**:
1. [Test ajouté]
2. [Guard ajouté]
3. [Validation ajoutée]
4. [Documentation ajoutée]

**Lessons Learned**:
[Ce qu'on a appris pour éviter ce type de bug à l'avenir]
```

**Exemple**:
```markdown
## Root Cause Analysis

**Bug**: Club creation returns 201 but club not saved to database

**Root Cause**: ClubMapper.toPrisma() was calling `club.getSubscription().getId()` without null check. When a club is created without a subscription, this throws an error that was silently caught somewhere in the stack, preventing the save.

**Why It Happened**:
- Initial implementation assumed all clubs have subscriptions
- No test coverage for the edge case of club without subscription
- Error was caught silently by NestJS exception filter

**Fix Applied**:
Changed `club.getSubscription().getId()` to `club.getSubscription()?.getId() ?? null` to handle null subscriptions gracefully.

**Prevention Measures**:
1. Added unit test: "should handle club without subscription"
2. Added type guard: Club.hasSubscription() method
3. Added validation in CreateClubHandler to ensure subscriptionId is explicitly set
4. Added JSDoc comment explaining the null case

**Lessons Learned**:
- Always handle nullable relations in mappers
- Add tests for edge cases during initial implementation
- Use optional chaining for potentially null properties
```

## ✅ Checklist Debugging

- [ ] **Étape 1**: Comportement observé documenté
- [ ] **Étape 2**: Bug reproduit localement (ou test reproductible créé)
- [ ] **Étape 3**: 2-3 causes racines formulées
- [ ] **Étape 4**: Causes priorisées par probabilité + impact
- [ ] **Étape 5**: Logs ajoutés aux points stratégiques
- [ ] **Étape 6**: Binary search appliqué pour isoler la cause
- [ ] **Étape 7**: Test qui fail écrit
- [ ] **Étape 8**: Fix minimal appliqué
- [ ] **Étape 9**: Full test suite run (tous passent)
- [ ] **Étape 10**: Protections ajoutées (tests, guards, validations, docs)
- [ ] **Documentation**: Root cause analysis rédigée

## 🚨 Erreurs Courantes

### 1. Fixer Sans Reproduire

```markdown
❌ MAUVAIS
Dev: "Je pense que c'est ça, je change le code"

✅ BON
Dev: "Je reproduis d'abord le bug localement"
Dev: "J'écris un test qui fail"
Dev: "ALORS je fixe"
```

### 2. Fix Large et Complexe

```typescript
// ❌ MAUVAIS - Fix trop large
function createClub(data) {
  // Refactor complet de toute la fonction
  // Ajout de 5 nouvelles fonctionnalités
  // Changement de l'architecture
  // ...
}

// ✅ BON - Fix minimal et ciblé
function createClub(data) {
  // Une seule ligne changée
  const subscriptionId = data.subscription?.id ?? null;
  // ...
}
```

### 3. Ne Pas Ajouter de Tests

```markdown
❌ MAUVAIS
Dev fixe le bug, commit, termine

✅ BON
Dev fixe le bug
Dev ajoute test pour empêcher régression
Dev commit avec test
```

### 4. Oublier de Run Full Test Suite

```markdown
❌ MAUVAIS
yarn test club.mapper.spec.ts
# ✅ Pass
git commit -m "Fix club creation"

✅ BON
yarn test club.mapper.spec.ts
# ✅ Pass
yarn test
# ✅ All pass
git commit -m "Fix club creation"
```

## 📚 Skills Complémentaires

- **bug-finder** : Méthodologie pour identifier la cause (étape précédente)
- **refactoring** : Refactoring après le fix pour améliorer le code
- **ddd-testing** : Standards de tests pour DDD bounded contexts

---

**Rappel CRITIQUE** : Toujours reproduire → tester → fixer → protéger → documenter.
