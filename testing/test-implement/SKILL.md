---
name: "test-implement"
description: "Écrit les tests manquants et corrige les tests en échec (🔵 Angular/Jest + 🟠 Java/JUnit). Appelé automatiquement par /test-check en cas de régression."
---

# Test Implement Skill

## Required configuration

Aucune variable d'environnement requise.

Prérequis :
- 🔵 Front : Jest configuré dans le projet (ou ng test avec jest runner)
- 🟠 Back : Maven installé (`mvn --version`)

Fichiers de référence :
- `.github/instructions/frontend/front-rules.instructions.md` — règles front Angular
- `.github/instructions/backend/java-unit-testing.instructions.md` — règles tests Java

## Available commands

### `/test-implement`

Écrit les tests manquants pour les fichiers modifiés sans couverture, et corrige les tests en échec détectés par `/test-check`.

---

## Detailed behaviour

### Step 1 — Lister les fichiers modifiés par domaine

```bash
# Fichiers Angular modifiés (hors specs)
git diff main...HEAD --name-only | grep '\.ts$' | grep -v '\.spec\.ts$'

# Fichiers Java modifiés (hors tests)
git diff main...HEAD --name-only | grep '\.java$' | grep -v 'Test\.java$'
```

---

### 🔵 Front — Angular

#### Step 2a — Extraire les noms des classes/services modifiés

Pour chaque fichier `.ts` modifié :

```bash
grep -oE 'export (default )?(abstract )?class [A-Za-z]+' <fichier.ts> | awk '{print $NF}'
basename <fichier.ts> .ts
```

#### Step 3a — Trouver les specs Angular impactées

```bash
find src/ -name "<FILE_BASENAME>.spec.ts"
grep -rl "<CLASS_NAME>\|<FILE_BASENAME>" src/ --include="*.spec.ts"
```

#### Step 4a — Créer les specs manquantes

Conventions issues de `front-rules.instructions.md` :
- Utiliser les fichiers `.sample.ts` existants pour les données de test (`<Domain>Sample.get()`, `<Domain>Sample.single()`)
- Tester le comportement des services (pas les interactions internes)
- Un fichier spec = une classe testée

Squelette Angular à générer :

```typescript
import { TestBed } from '@angular/core/testing';
import { <NomClasse> } from './<nom-fichier>';

describe('<NomClasse>', () => {
  let service: <NomClasse>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      // providers, imports...
    });
    service = TestBed.inject(<NomClasse>);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
```

#### Step 5a — Corriger les specs Angular en échec

Analyser l'erreur, corriger le test ou le mock. Utiliser les `.sample.ts` pour les données de test plutôt que des objets créés inline.

#### Step 6a — Relancer les specs Angular

```bash
npx jest --testPathPattern="<spec1>|<spec2>|..." --no-coverage
```

---

### 🟠 Back — Java

#### Step 2b — Trouver les tests Java impactés

```bash
CLASS_NAME=$(basename <fichier.java> .java)
find src/test/java/ -name "${CLASS_NAME}Test.java"
```

#### Step 3b — Vérifier la migration JUnit 4 → 5

Si un test existant utilise JUnit 4 (`@RunWith`, `import org.junit.Test`), **le migrer d'abord** avant d'ajouter des tests :

| JUnit 4 | JUnit 5 |
|---|---|
| `@RunWith(MockitoJUnitRunner.class)` | `@ExtendWith(MockitoExtension.class)` |
| `import org.junit.Test` | `import org.junit.jupiter.api.Test` |
| `import org.junit.Before` | `import org.junit.jupiter.api.BeforeEach` |
| `public void testXxx()` | `void shouldXxx_whenYyy()` |
| JUnit assertions | AssertJ `assertThat()` |

#### Step 4b — Créer les tests JUnit manquants

Conventions issues de `java-unit-testing.instructions.md` :
- **JUnit 5** + **Mockito** (`@ExtendWith(MockitoExtension.class)`) + **AssertJ** (`assertThat()`)
- Nommage : `should<ExpectedBehavior>_when<Condition>` (ex: `shouldReturnNull_whenApiIsNull`)
- Pattern **AAA** (Arrange / Act / Assert)
- Pas de modificateur `public` sur la classe ni les méthodes de test
- Utiliser `final var` pour les variables locales
- Utiliser `usingRecursiveComparison()` pour les mappers (pas de field-by-field)
- Tester le comportement (output), pas l'implémentation (éviter `verify()` sauf si l'interaction est le comportement attendu)
- Utiliser les `*BuilderForTest` existants pour les données de test, avec uniquement les champs pertinents
- Utiliser `@ParameterizedTest` + `@MethodSource` pour factoriser les cas similaires

Squelette JUnit 5 à générer :

```java
package <package>;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import static org.assertj.core.api.Assertions.assertThat;

@ExtendWith(MockitoExtension.class)
class <NomClasse>Test {

    // @Mock private <Dependency> dependency;

    @InjectMocks
    private <NomClasse> <nomVariable>;

    @Test
    void shouldBeInstantiated() {
        // Arrange & Act & Assert
        assertThat(<nomVariable>).isNotNull();
    }
}
```

#### Step 5b — Corriger les tests Java en échec

Analyser l'erreur, corriger le test ou les mocks. Respecter les règles de `java-unit-testing.instructions.md`.

#### Step 6b — Relancer les tests Java

```bash
mvn test -Dtest="<TestClass1>,<TestClass2>" -pl <module> --no-transfer-progress
```

---

### Step 7 — Présenter les résultats

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
�� Test Implement — Résultats
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔵 Front Angular
  ✅ Specs créées         : <N>
  ✅ Specs corrigées       : <N>
  ❌ Encore en échec       : <N>

🟠 Back Java
  ✅ Tests créés          : <N>
  ✅ Tests migrés JUnit 5  : <N>
  ✅ Tests corrigés        : <N>
  ❌ Encore en échec       : <N>

⚠️  Fichiers sans test :
  - <path>
```

### Step 8 — Décision finale

- Si tous les tests passent → afficher :
  ```
  ✅ Tous les tests passent. Tu peux continuer avec /code-lint.
  ```
- Si des tests sont encore en échec → afficher :
  ```
  ⛔ Des tests sont encore en échec. Vérification manuelle requise.
  ```

---

## Error handling

| Situation | Comportement |
|-----------|-------------|
| Test JUnit 4 trouvé | Migrer vers JUnit 5 avant d'ajouter des tests |
| Aucun test existant pour un fichier | Générer le squelette + signaler |
| Jest non installé | Tenter `ng test --watch=false` ; si absent → `❌ Aucun runner Angular trouvé.` |
| Maven non installé | `❌ Maven introuvable. Vérifier l'installation.` |
| Tests encore en échec | Bloquer `/code-lint`, afficher les détails |
