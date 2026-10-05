---
name: "task-implement"
description: "Implémente le code (Angular front et/ou Java/Jakarta EE back) en s'appuyant sur les règles du projet, les leçons passées et le plan validé lors de /task-start"
---

# Task Implement Skill

## Required configuration

Aucune variable d'environnement requise.

Fichiers de référence attendus dans le repo :
- `.copilot/lessons.md` — erreurs passées à ne pas reproduire
- `.github/instructions/frontend/front-rules.instructions.md` — règles de code front Angular
- `.github/instructions/backend/java-coding-style.instructions.md` — règles de code back Java

## Available commands

### `/task-implement`

Implémente les changements (front Angular et/ou back Java/Jakarta EE) décrits dans le plan validé lors de `/task-start`.
Détecte automatiquement depuis l'ANALYZE.md quelles parties sont concernées (front, back, ou les deux).

---

## Detailed behaviour

### Step 1 — Charger le contexte avant d'écrire la moindre ligne

#### 1a. Lire `.copilot/lessons.md`

Si le fichier n'existe pas, le créer avec ce contenu initial :
```markdown
# Lessons
```
Et continuer.

#### 1b. Charger les règles du projet selon les parties concernées

Lire les fichiers de règles suivants (si présents) :
- `.github/instructions/frontend/front-rules.instructions.md`
- `.github/instructions/backend/java-coding-style.instructions.md`

Si un fichier est absent, afficher un avertissement et continuer :
```
⚠️  <fichier> introuvable — implémentation sans règles custom pour cette partie.
```

#### 1c. Relire le plan validé depuis l'ANALYZE.md

Déduire le ticket depuis la branche courante :

```bash
git branch --show-current
# ex: main/presc/bugfix/ORBISBUG-177176 → ticket = ORBISBUG-177176
```

Extraire le ticket = dernier segment du nom de branche (après le dernier `/`).

Lire le fichier :
```
<repo_root>/.copilot/analyses/<TICKET>-ANALYZE.md
```

Si le fichier est absent, afficher :
```
⚠️  Aucun ANALYZE.md trouvé pour <TICKET> — contexte limité.
    Lance /task-analyze <TICKET> pour générer l'analyse.
```
Et continuer avec le contexte disponible en mémoire.

#### 1d. Détecter les parties à implémenter

À partir de l'ANALYZE.md (sections "Composants / fichiers identifiés", "Hypothèses de fix"), déterminer :
- 🔵 **FRONT** : changements dans des fichiers `.ts`/`.html`/`.scss` Angular
- 🟠 **BACK** : changements dans des fichiers `.java` Jakarta EE
- 🔵🟠 **LES DEUX** : story full-stack

Afficher clairement :
```
🔍 Périmètre détecté : [FRONT uniquement | BACK uniquement | FRONT + BACK]
```

---

### Step 2 — [BACK] Implémenter les changements Java / Jakarta EE

> *(Sauter cette étape si périmètre FRONT uniquement)*

> ## 🚫 RÈGLE ABSOLUE — ZÉRO FICHIER DE TEST JAVA
> **Il est strictement interdit de :**
> - Créer ou modifier un fichier `*Test.java`
> - Ajouter des imports depuis `org.junit`, `org.mockito`, `org.assertj`
> - Écrire des méthodes annotées `@Test`
>
> **Les tests Java sont écrits par un skill dédié.**
> Si le besoin d'écrire un test se présente → l'ignorer et le noter dans le résumé final sous "⚠️ Tests à créer".

Appliquer les changements décrits dans le plan :
- Créer ou modifier les classes, services, mappers, DTOs, resources JAX-RS concernés
- Respecter la structure de packages existante du projet
- Respecter le style de code des fichiers voisins

**Auto-vérification Java avant de finaliser chaque fichier :**

#### Style (règles `java-coding-style.instructions.md`)
- [ ] Toutes les variables locales sont `final` (sauf réassignation nécessaire)
- [ ] `final var` utilisé quand le type est évident
- [ ] Pas de chaînage > 2-3 appels sur une ligne — extraire en variables intermédiaires
- [ ] Pas d'appel multiple à la même méthode — mettre en cache dans une variable
- [ ] `try-with-resources` pour tout `AutoCloseable` (ex: `Response`)
- [ ] Expressions complexes extraites du `try-with-resources`
- [ ] Guard clauses avec early return plutôt que nesting profond
- [ ] Conditions complexes extraites dans des variables ou méthodes nommées
- [ ] Nommage descriptif — pas de `r`, `tmp`, `x`, `data`
- [ ] Booléens préfixés par `is`, `has`, `should`, `can`
- [ ] Aucune méthode > 20-30 lignes (si dépassé, découper en helpers privés)

#### Règles `.github/instructions/backend/java-coding-style.instructions.md`
- [ ] Aucune règle du fichier n'est violée

#### Leçons `.copilot/lessons.md`
- [ ] Aucune erreur listée dans le fichier n'est reproduite

#### Clean code
- [ ] Pas de code commenté laissé en place
- [ ] Logique métier dans les services, pas dans les resources JAX-RS

---

### Step 3 — [FRONT] Implémenter les changements Angular

> *(Sauter cette étape si périmètre BACK uniquement)*

> ## 🚫 RÈGLE ABSOLUE — ZÉRO FICHIER DE TEST ANGULAR
> **Il est strictement interdit de :**
> - Créer ou modifier un fichier `.spec.ts`
> - Ajouter des imports depuis `@angular/core/testing`, `jasmine`, `jest`
> - Écrire des blocs `describe()`, `it()`, `beforeEach()`, `expect()`
> - Modifier un `TestBed.configureTestingModule()`
>
> **Les tests Angular sont écrits par un skill dédié : `/test-implement`.**
> Si le besoin d'écrire un test se présente → l'ignorer et le noter dans le résumé final sous "⚠️ Tests à créer".

Appliquer les changements décrits dans le plan :
- Créer ou modifier les composants, services, modèles, pipes, guards concernés
- Respecter la structure de fichiers Angular du projet (feature modules, standalone components, etc.)
- Respecter le style de code existant dans les fichiers voisins

**Auto-vérification Angular avant de finaliser chaque fichier :**

#### TypeScript
- [ ] Aucun `any` — si nécessaire, créer une interface dans `src/app/models/`
- [ ] Aucun `as` cast non justifié
- [ ] Toutes les propriétés de classe sont initialisées ou marquées `!`
- [ ] `readonly` sur les propriétés qui ne changent pas après init

#### Angular — Observables
- [ ] Toute subscription utilise `takeUntilDestroyed()` ou le `async` pipe en template
- [ ] Aucun `.subscribe()` imbriqué (utiliser `switchMap`, `combineLatest`, etc.)
- [ ] Aucun `Subject` exposé publiquement — exposer uniquement `.asObservable()`

#### Angular — Composants
- [ ] `ChangeDetectionStrategy.OnPush` présent sur les composants présentationnels
- [ ] Aucun appel HTTP direct dans un composant
- [ ] Logique métier dans les services, pas dans les composants

#### Règles `.github/instructions/frontend/front-rules.instructions.md`
- [ ] Aucune règle du fichier n'est violée

#### Leçons `.copilot/lessons.md`
- [ ] Aucune erreur listée dans le fichier n'est reproduite

#### Clean code
- [ ] Aucune méthode > 20 lignes (si dépassé, découper)
- [ ] Nommage explicite (pas de `data`, `res`, `tmp`, `obj`)
- [ ] Pas de code commenté laissé en place

---

### Step 4 — Résumer les changements

Afficher un résumé final unifié :

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Implémentation terminée  [FRONT | BACK | FRONT + BACK]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🟠 Back-end :
📁 Fichiers créés :
  - <path> — <description courte>
✏️  Fichiers modifiés :
  - <path> — <ce qui a changé>

🔵 Front-end :
📁 Fichiers créés :
  - <path> — <description courte>
✏️  Fichiers modifiés :
  - <path> — <ce qui a changé>

💡 Choix techniques notables :
  - <choix 1 et justification>
  - <choix 2 et justification>

➡️  Prochaine étape : /code-review
⚠️  Tests à créer (le cas échéant) :
  - <fichier> — <comportement à tester>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Error handling

| Situation | Comportement |
|-----------|-------------|
| `lessons.md` absent | Créer le fichier vide avec `# Lessons` et continuer |
| `front-rules.instructions.md` absent | Avertir et continuer sans règles custom front |
| `java-coding-style.instructions.md` absent | Avertir et continuer sans règles custom back |
| Périmètre non détectable depuis l'ANALYZE.md | Demander à l'utilisateur : "Cette story touche-t-elle le front, le back, ou les deux ?" |
| Auto-vérification échoue | Corriger le problème avant de finaliser le fichier |
