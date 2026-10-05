---
name: "test-check"
description: "Vérifie que les changements de la PR n'ont pas cassé de tests existants (🔵 Angular/Jest + 🟠 Java/Maven). Lance les tests impactés et appelle /test-implement si des tests échouent."
---

# Test Check Skill

## Required configuration

Aucune variable d'environnement requise.

Prérequis :
- 🔵 Front : Jest configuré dans le projet (ou ng test avec jest runner)
- 🟠 Back : Maven installé (`mvn --version`)

## Available commands

### `/test-check`

Détecte les tests existants impactés par les changements de la PR, les lance, et déclenche `/test-implement` si des tests échouent.

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

#### Step 2a — Trouver les specs Angular existantes impactées

Pour chaque fichier `.ts` modifié, chercher les `*.spec.ts` **déjà existants** qui :
- Ont un nom correspondant au fichier modifié (convention Angular) :
  ```bash
  find src/ -name "<FILE_BASENAME>.spec.ts"
  ```
- Ou importent la classe ou le fichier modifié :
  ```bash
  grep -rl "<CLASS_NAME>\|<FILE_BASENAME>" src/ --include="*.spec.ts"
  ```

Combiner et dédupliquer (`sort -u`).

> ⚠️ **Ne pas créer de nouvelles specs** — seules les specs existantes sont concernées. La création est déléguée à `/test-implement`.

#### Step 3a — Lancer les specs Angular impactées

**Détecter le runner disponible :**
```bash
npx jest --version 2>/dev/null && echo "jest" || echo "ng"
```

**Avec Jest (préféré) :**
```bash
npx jest --testPathPattern="<spec1>|<spec2>|..." --no-coverage
```

**Avec ng test :**
```bash
ng test --watch=false --no-progress \
  --include="<spec1>" --include="<spec2>"
```

> ⚠️ **Toujours passer `--watch=false`** avec `ng test` — sans ce flag la commande bloque indéfiniment en mode watch.

---

### 🟠 Back — Java

#### Step 2b — Trouver les tests Java existants impactés

Pour chaque fichier `.java` modifié (ex: `src/main/java/com/dedalus/MyService.java`), chercher la classe de test correspondante dans `src/test/java/` :

```bash
# Convention : MyService.java → MyServiceTest.java
CLASS_NAME=$(basename <fichier.java> .java)
find src/test/java/ -name "${CLASS_NAME}Test.java"
```

> Si aucun test trouvé pour une classe modifiée, le signaler sans bloquer (délégué à `/test-implement`).

#### Step 3b — Lancer les tests Java impactés

```bash
mvn test -Dtest="<TestClass1>,<TestClass2>" -pl <module> --no-transfer-progress
```

> Si les classes de test sont dans des modules Maven différents, lancer une commande par module.

---

### Step 4 — Présenter les résultats

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 Test Check — Résultats
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔵 Front Angular
  📂 Fichiers modifiés analysés : <N>
  🎯 Specs existantes impactées  : <N>
  ✅ Tests passants : <N>
  ❌ Tests en échec : <N>

🟠 Back Java
  📂 Fichiers modifiés analysés : <N>
  🎯 Tests existants impactés   : <N>
  ✅ Tests passants : <N>
  ❌ Tests en échec : <N>

❌ Détail des échecs :
  Fichier  : <test-file>
  Classe   : <describe / class>
  Test     : <test name>
  Erreur   : <message d'erreur>
```

### Step 5 — Décision finale

- Si **tous les tests passent** → afficher :
  ```
  ✅ Aucune régression détectée. Tu peux continuer avec /code-lint.
  ```

- Si **des tests échouent** → afficher :
  ```
  ⛔ Des régressions détectées. Lancement de /test-implement pour corriger.
  ```
  Puis **appeler automatiquement `/test-implement`** pour corriger les tests en échec.

---

## Error handling

| Situation | Comportement |
|-----------|-------------|
| Aucun test existant trouvé | Signaler + continuer sans bloquer |
| Jest non installé | Tenter `ng test --watch=false` ; si absent aussi → `❌ Aucun runner Angular trouvé.` |
| Maven non installé | `❌ Maven introuvable. Vérifier l'installation.` |
| Tests en échec | Appeler automatiquement `/test-implement` |
