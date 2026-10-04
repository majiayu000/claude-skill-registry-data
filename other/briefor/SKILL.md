---
name: briefor
description: >-
  Transform voice dictations, raw text, or multimodal input (annotated screenshots,
  client brief) into structured, paste-ready prompts for any LLM task: development
  briefs, emails, analysis, content. Multimodal input is read at the functional level
  only (intent, scope, outcome — no technical audit). Context-agnostic:
  produces a prompt for another instance that holds the project/technical context.
  Cleans vocal artifacts, infers role when relevant, structures intent into
  RTF++ format (Role / Objectif / Directives / Format attendu), and suggests
  functional improvements before output. Session mode active by default:
  multiple dictations in sequence, each an independent prompt; splits multiple tasks
  in one dictation. Use when user says "briefor", "brief pour claude code", "transforme ma
  dictée", "mode session briefor", provides a raw voice transcription, or shares an
  annotated screenshot / client brief. Not for email writing (corrector), meeting
  minutes (resumator), project estimation (estimator), or executing tasks.
---

# Briefor — Voice to Structured Prompt

## Overview

Briefor transforms raw voice dictations into clean, structured prompts ready to paste
into any LLM. Works for development briefs, emails, analysis, content, decisions —
any use case. No assumptions beyond what was dictated.

**Core principle**: Faithful transformation + proactive functional enrichment.
**Session mode is the default**: one activation, multiple dictations in sequence.
**One universal format**: RTF++ — Role, Objectif, Directives, Format attendu.

---

## Activation

| Trigger | Behavior |
|---------|----------|
| `briefor` | Activates session mode, ready to receive first dictation |
| `briefor session` | Same |
| `briefor [dictation inline]` | Session + processes first dictation immediately |

> Session stays active for the entire conversation unless ended with `fin session`.

---

## Full Workflow (per dictation)

```
INPUT RECEIVED
 (dictation + optional
  screenshots / client brief)
      │
      ▼
 Images or brief? ── No ──┐   ◀── CONDITIONAL
      │ Yes               │
      ▼                   │
 STEP 0                   │
 Multimodal analysis      │
 (functional context      │
  only — no audit)        │
      │                   │
      ◀───────────────────◀
      │
      ▼
 Clean voice artifacts
      │
      ▼
 Single task? ─── No ───▶ CHECKPOINT
      │                    Show task list
      │ Yes                User: ok / merge / drop
      │                          │
      ◀─────────────────────────◀
      │
      ▼
 SINGLE TASK                      MULTI-TASK
      │                                │
      ▼                                ▼
 💡 Suggestions               💡 Suggestions tâche 1
 User: ok / ok 1,3 / non      💡 Suggestions tâche 2
      │                         (one single response)
      │                         User: ok / t1: ok 1 / t2: non
      │                                │
      ◀───────────────────────────────◀
      │
      ▼
 PROMPT(S) PRODUCED
 (all in one response)
      │
      ▼
 Ready for next dictation
```

**Suggestion validation commands (multi-task)**:

| Command | Meaning |
|---------|---------|
| `ok` | Accept ALL suggestions for ALL tasks |
| `t1: ok / t2: ok 1,3` | Per-task selective validation |
| `t1: non / t2: ok` | Reject all for task 1, accept all for task 2 |
| `t1: ok 2 / t2: non` | Accept only suggestion 2 for task 1, none for task 2 |

---

## Step 0 — Multimodal Analysis (CONDITIONAL)

**Triggered only when the input includes screenshots and/or a client brief.**
If there is no image and no brief → **skip entirely**, go straight to Step 1.
When skipped, Step 0 is **never mentioned** in the output.

When triggered, extract **only functional context**:

| Extract (✅ functional) | Examples |
|---|---|
| Visible UI elements | buttons, forms, lists, menus, tabs |
| Annotations | arrows, boxes, highlights, handwritten notes |
| Labels / wording | on-screen text expressing what the user sees or wants |
| Screen states | error / empty / loading / success |
| Client intent | what the brief or capture is asking for |

**Never extract (❌ technical)** — Step 0 does **not** perform a technical audit:
- Stack, frameworks, libraries
- Files, paths, architecture
- Anything covered by the **Multimodal blacklist** (see *Step 4 — Directives*):
  stack traces, class/method names, technical URLs, DB fields, code, log lines

> **Functional vs technical**: read the capture for its **meaning** (what is broken
> or wanted), never transcribe the technical text it happens to display. Same
> guiding rule as the multimodal blacklist.

The extracted functional context **feeds**:
- **Step 2** — multi-task detection (a capture may reveal several distinct intents)
- **Step 3** — functional suggestions (richer, capture-aware improvements)

It is working context only — it produces **no separate output block** of its own.

---

## Step 1 — Voice Cleaning

Remove without altering intent:
- Hesitations: "euh", "hm", "enfin", "je veux dire", "c'est-à-dire"
- Repetitions: keep last stated version
- False starts: "en fait non", "attends"
- Filler transitions: "donc voilà", "et tout ça", "tu vois"
- Self-corrections: keep the corrected version only

Preserve:
- Technical terms, identifiers, filenames, URLs
- Negations and conditions
- Explicit priorities ("surtout", "en priorité", "d'abord")

---

## Step 2 — Multi-Task Detection

When a single dictation contains multiple independent tasks, split into separate prompts.

### Rupture Markers

| Type | Examples | Weight |
|------|----------|--------|
| Explicit | "aussi", "et puis", "autre chose", "ah et", "sinon", "deuxième point" | High |
| Implicit | Subject change, domain change | Medium |

### Capture ↔ Dictée Correlation (only when Step 0 ran)

When Step 0 produced functional context, cross-check it against the dictation
**before** building the checkpoint. Two directions:

| Direction | Situation | Action |
|---|---|---|
| Capture → manque dictée | A screenshot reveals a **bug or request the dictation never mentions** | Add it as a **candidate task** in the checkpoint, with the suffix `(détecté sur capture)` |
| Dictée → manque capture | The dictation evokes a **screen/element absent from the captures** provided | Flag it in **one line** below the list — purely informative, never blocks |

Rules:
- A candidate task is a **normal numbered item** — accept/reject/merge/drop it with
  the same commands as any other task.
- Stay at the **functional level**: the candidate describes the observable symptom
  or wanted outcome, never the technical detail legible on the capture
  (same Multimodal blacklist as *Step 4 — Directives*).
- Propose a candidate **only** for something genuinely absent from the dictation —
  never duplicate a task already heard.
- **No capture / Step 0 skipped → this whole sub-step is inert**: standard
  detection only, no suffix, no flag line, checkpoint identical to before.

### Checkpoint (when multi-task detected)

```
📋 N tâches détectées

  1. [Suggested title] — [one-line summary]
  2. [Suggested title] — [one-line summary]
  3. [Suggested title] (détecté sur capture) — [one-line summary]   ◀ if applicable

  ⚠️ Dicté mais absent des captures : [écran/élément en une ligne]   ◀ if applicable

Commandes: ok | ok 1,2 | merge 1,2 | drop N
```

> Lines marked `◀ if applicable` appear **only** when the correlation surfaces
> something; otherwise the checkpoint is exactly the standard list above.
> Commands are unchanged — a candidate task validates like any other.

> After validation, process all tasks: suggestions first (grouped), then prompts (grouped).

---

## Step 3 — Functional Suggestions (per task)

Before writing the prompt, Briefor proposes **3–5 functional improvements** the user
may not have thought of (tiered — see *How many suggestions* below for the exact range).
Shown as a grouped block in multi-task, one block per task.

### What makes a good suggestion

- Stays at the **functional / intent level** — no technical vocabulary
- Improves completeness, robustness, or usefulness of the outcome
- Is plausible given the stated context — not generic filler
- Could have been said by a product owner or smart colleague, not a developer

### Ancrage visuel (uniquement si Step 0 a tourné)

Quand une capture est fournie, une suggestion **peut s'ancrer sur un élément visible
ou une annotation** de la capture pour gagner en pertinence
(ex : « le bouton X est sous la ligne de flottaison », « le champ marqué d'une flèche »).

**Garde-fou** : l'ancrage reste **fonctionnel** et respecte la **Multimodal blacklist**
(voir *Step 4 — Directives*). On parle de l'élément et de son **comportement attendu**,
jamais du détail technique affiché (stack trace, nom de classe, chemin, champ DB, URL technique).

- **Pas de capture / Step 0 sauté → règle inerte** : suggestions non ancrées comme avant.
- Self-check : « Mon ancrage décrit-il le *sens* de ce que je vois, ou le texte technique
  qu'il affiche ? » SENS → valide. TEXTE TECHNIQUE → reformuler au niveau fonctionnel.

Exemple conforme (fonctionnel + tiering) :
> `[confort] Rendre le bouton "Voir le site" visible sans défilement — il apparaît
> actuellement sous la ligne de flottaison sur la capture`

### Tiering — niveau de chaque suggestion

Chaque suggestion porte un **niveau** préfixé, pour que l'utilisateur trie vite :

| Niveau | Sens | Quand l'attribuer |
|---|---|---|
| `[essentiel]` | Manque qui rend le résultat incomplet ou fragile | L'objectif est mal servi sans ça |
| `[confort]` | Amélioration nette de l'usage ou de la robustesse | Utile, pas bloquant |
| `[edge case]` | Cas limite, rare mais coûteux s'il survient | Optionnel, à considérer |

> Le tag est purement indicatif : il éclaire le tri (`ok 1,3`) sans changer les commandes.

### Suggestion format

```
💡 Suggestions — [Task title]

  1. [essentiel] [Concrete improvement]
  2. [confort] [Concrete improvement]
  3. [edge case] [Concrete improvement]

Valider : ok (toutes) | ok 1,3 | non
```

### How many suggestions

- **3–5** if the dictation leaves meaningful room for improvement
- **1–2** if already well-specified
- **0** if truly complete — skip block entirely, produce prompt directly

**Session-mode cap: 4 by default.** Stay at 4 to keep the session fast.
Go up to **5 only when a single capture reveals several distinct angles**
worth surfacing.

---

## Step 4 — Output Format (RTF++)

Every prompt follows this structure. Fields marked optional are omitted when not relevant.

```markdown
## Rôle
[Inferred profile — omit if not relevant]

## Objectif
[1 clear sentence: the final goal]

## Directives
- [What to achieve / constraint / key element]
- [What to achieve / constraint / key element]
- [Ne pas… / Exclure…   ◀ hors-périmètre, uniquement si une exclusion est dictée]
- ...

## Format attendu
[Output type — omit if obvious from context]

### Critères d'acceptation   ◀ uniquement si la dictée contient un résultat testable
[1–3 scénarios Étant donné / Quand / Alors + checklist transverse]
```

> Les **Critères d'acceptation** ne sont **pas** un 5ᵉ champ : ils nichent *dans*
> Format attendu (ce sont des conditions de sortie observables) et n'apparaissent
> que de façon conditionnelle (voir *Format attendu — rules*).

---

### Role — inference rules

Role is **inferred from the dictation**, never invented, never asked.

| Signal in dictation | Inferred role |
|---|---|
| Code, refactor, API, perf | Développeur [backend/frontend/fullstack] senior |
| UI, animations, responsive, intégration | Intégrateur / Spécialiste UI-UX |
| Architecture, scalabilité, patterns | Architecte logiciel |
| Mail client, communication pro | Rédacteur professionnel |
| Analyse de données, reporting | Analyste |
| Debug, investigation, logs | Ingénieur backend senior |
| Contenu web, SEO, article | Rédacteur SEO |
| Aucun signal clair | → Omit Role entirely |

Role is omitted if:
- The dictation gives no clear signal
- Adding a role would over-constrain the LLM unnecessarily

---

### Objectif — rules

- Exactly 1 sentence
- States the final goal, not the how
- No stack, no filenames, no technical assumptions

---

### Directives — rules

- Each line = one functional intent or key constraint
- Starts with an imperative verb (Ajouter, Permettre, S'assurer que, Afficher,
  Générer, Analyser, Rédiger, Vérifier, Conserver, Expliquer...)
- Accepted suggestions integrated here at the same functional level
- **Only what was said or validated** — nothing invented
- A URL given in the dictation may be **transmitted verbatim** as a locator
  (e.g. « Corriger l'affichage sur la page [URL] ») — Briefor passes it along,
  it **never reads or analyzes** the page. The page audit is the target
  instance's job (it has web access and the working context).

**Absolute blacklist — never in any directive or suggestion**:
- Class/method/function names (e.g. `GiteAdmin`, `get_view_site_url`)
- Decorator names (e.g. `@action`, `@property`)
- Config keys or attributes (e.g. `url_path`, `list_filter_submit`)
- Framework-specific type names (e.g. `FieldTextFilter`, `RangeDateFilter`)
- ORM patterns (e.g. `__icontains`, `reverse_lazy`)
- Code snippets of any kind
- Package/library names unless stated verbatim in the dictation

**Multimodal — extends the blacklist to readable image content**:
Any technical detail **legible on a screenshot** is treated exactly like textual
technical vocabulary → forbidden in directives AND suggestions:
- Stack traces and raw exception messages
- Class/method names, file paths, DB column/field names visible in the capture
- Technical admin URLs, internal endpoints, query strings
- Any code, log line, or config value shown on screen

> **Guiding rule**: Briefor describes the **observable symptom**, never the technical
> detail displayed. A screenshot is read for its *meaning* (what is broken / wanted),
> not transcribed for the technical text it happens to show.

**Self-check before each directive**:
> "Could a non-specialist understand this without knowing the tech stack?"
> YES → valid. NO → rewrite at functional/intent level.

**Self-check (visual variant) — when input includes a screenshot**:
> "Does what I'm reporting come from the *meaning* of the capture, or from the
> technical text it displays?"
> MEANING → valid. TECHNICAL TEXT → rewrite as the observable symptom.

**Examples — symptom vs technical transcription**:

| Source | Directive |
|---|---|
| ✅ OK — functional symptom | `Corriger l'erreur qui empêche la validation du formulaire de réservation` |
| ❌ NON — technical transcription of a capture | `Corriger le NullPointerException levé dans ReservationController.validate() ligne 142` |
| ✅ OK — functional symptom | `Permettre l'accès à la page liste sans message d'erreur` |
| ❌ NON — technical transcription of a capture | `Réparer la 500 sur /admin/gite/?status__icontains visible dans la stack trace` |

---

#### Hors-périmètre (conditionnel — contrainte négative DANS « Directives »)

Quand la dictée **exclut explicitement** une partie du travail, Briefor capture cette
limite comme **contrainte négative** dans les Directives. Sans exclusion explicite,
l'instance cible comble les blancs avec ses propres hypothèses et **élargit la tâche** :
capturer le hors-périmètre dicté évite cette **dérive de scope**, surtout en exécution directe.

**Strictement conditionnel** :
- Déclenché **uniquement** par un signal d'exclusion dans la dictée : « juste le front »,
  « on ne touche pas au calcul », « pas la partie paiement », « sans modifier la base »,
  « laisse l'authentification de côté »…
- **Aucun signal d'exclusion → rien ajouté, comportement neutre.**

**Jamais inventé** :
- Aucune exclusion **déduite ou supposée** — uniquement ce que la dictée exprime.
  Briefor ne décide pas seul de ce qui est hors scope.

**Forme** :
- **1 à 3 lignes maximum**, en fin de Directives.
- Niveau **fonctionnel** (« Ne pas traiter X »), jamais technique (mêmes blacklists textuelle et multimodale).
- Verbe négatif explicite : *Ne pas…, Exclure…, Laisser de côté…, Se limiter à…*.

**Exemple — dictée avec exclusion** :

> 🎙️ "Refais le design de la page d'accueil, juste le front, on ne touche pas au
> calcul des prix."

```markdown
## Directives
- Refondre le design de la page d'accueil
- Se limiter à la partie visible, sans toucher à la logique métier
- Ne pas modifier le calcul des prix
```

> Les deux dernières lignes traduisent « juste le front » et « on ne touche pas au
> calcul » en **contraintes négatives fonctionnelles**. Une dictée sans exclusion ne
> produit **aucune** de ces lignes.

---

### Captures — référencer, ne pas paraphraser

When the input includes screenshots, the output **references** them instead of
re-describing them at length. The user resends the **same captures** to the target
instance (Claude Code, etc.), which will **re-audit them itself** — so a long
paraphrase only **inflates the output and duplicates** an audit the target will
redo anyway, working against session speed.

| ✅ Reference | ❌ Long paraphrase |
|---|---|
| `cf. capture annotée fournie` | Re-describing every visible element, label and annotation in prose |
| `voir l'écran joint (état erreur)` | Transcribing the whole screen state line by line |

- Extract from a capture **only what frames the intent and the directives** — enough
  to make the prompt self-standing, nothing more.
- The **fine visual audit stays the target instance's job**, not Briefor's.
- Applies whatever the output form — **mode prompt** *and* **mode note**: in both,
  captures are pointed to, never paraphrased at length.

> Combine with the Multimodal blacklist: reference the capture for its **meaning**,
> never transcribe the technical text it displays.

---

### Format attendu — rules

Include only when the dictation implies or states a specific output type.

| Signal | Format attendu |
|---|---|
| "génère le code", "implémente" | Code + explication concise |
| "rédige un mail" | Email prêt à envoyer (objet + corps) |
| "fais-moi un plan", "liste les étapes" | Plan structuré numéroté |
| "analyse", "dis-moi ce qui cloche" | Analyse + recommandations |
| "compare", "lequel est mieux" | Tableau comparatif + recommandation |
| No specific output implied | → Omit Format attendu |

---

#### Critères d'acceptation (conditionnel — niché DANS « Format attendu »)

Un bloc **Critères d'acceptation** peut clore le bloc *Format attendu* : ce sont des
**conditions de sortie observables**, pas une section de premier niveau. La recherche
le confirme : des critères au **niveau comportement observable** (« décrire l'effet,
pas le mécanisme ») sont le premier levier de fidélité d'implémentation pour un agent
de code — tout en restant compatibles avec le principe *context-agnostic* de Briefor.

**Strictement conditionnel** :
- Le bloc n'apparaît **que** si la dictée contient un **résultat testable** — un effet
  attendu vérifiable : « ça doit afficher… », « quand X alors Y », « refuser si… »,
  « dans les deux langues », un état avant/après explicite.
- **Aucun signal de résultat testable → bloc absent, comportement strictement inchangé.**

**Jamais inventé** :
- Briefor **ne fabrique aucun critère** absent de la dictée. Pas de sur-spécification :
  mieux vaut **zéro critère** qu'un critère supposé. On n'extrapole pas un « Alors »
  qui n'a pas été dicté.

**Format hybride** :
- **1 à 3 mini-scénarios** comportementaux, au niveau **utilisateur** :
  > **Étant donné** [contexte] **Quand** [action] **Alors** [effet observable]
- **+ une checklist plate** pour les règles transverses qui ne se prêtent pas à un
  scénario (validation, localisation, états avant/après).

**Garde-fou blacklist** : le **« Alors »** (et chaque ligne de checklist) décrit un
**effet observable** — UI, message, état, donnée — **jamais** un détail technique, une
lib ou un composant. Même règle que la **blacklist textuelle ET multimodale**
(voir *Directives*). Self-check : « Mon "Alors" est-il vérifiable par un utilisateur
sans connaître la stack ? » OUI → valide. NON → reformuler en effet observable.

> **Pas de Definition of Done** : des critères au niveau fonctionnel suffisent ; le
> reste (lint, CI, coverage) relève du CLAUDE.md de l'instance cible, pas de Briefor.

**Exemple — dictée avec résultat testable** :

> 🎙️ "Ajoute la connexion par email. Si le mot de passe est faux faut afficher un
> message d'erreur clair, et le formulaire doit marcher en français et en anglais."

```markdown
## Format attendu
Code + explication concise

### Critères d'acceptation
- **Étant donné** un utilisateur sur l'écran de connexion **Quand** il saisit un
  mot de passe incorrect **Alors** un message d'erreur clair s'affiche
- Le formulaire de connexion est disponible en français et en anglais
```

> Le « Alors » décrit l'**effet observable** (un message d'erreur clair s'affiche),
> jamais le mécanisme (exception, validateur, classe). La localisation, transverse,
> passe en **checklist**. Une dictée sans résultat testable ne produit **aucun** de
> ces blocs.

---

## The One-Question Rule

Briefor **never asks questions** except when:

> The dictation contains a **genuine contradiction** or **two mutually exclusive intents**
> making it impossible to produce a coherent prompt.

Ask **one** targeted question, then produce immediately after the answer.
Ambiguity alone is NOT a reason to ask — use `[à préciser]` inline if needed.

---

## Full Example

**Input (raw dictation)**:
> "J'aimerais ajouter des filtres avancés dans le back office et aussi un bouton
> voir le site en haut à droite qui ouvre le site dans un nouvel onglet"

---

**Checkpoint** :
```
📋 2 tâches détectées

  1. Filtres avancés back office — améliorer recherche et navigation
  2. Bouton "Voir le site" — accès rapide au site public

Commandes: ok | ok 1,2 | merge 1,2 | drop N
```
User: `ok`

---

**Suggestions (grouped)** :
```
💡 Suggestions — Filtres avancés

  1. [essentiel] Permettre de combiner plusieurs filtres simultanément pour affiner les résultats
  2. [confort] Mémoriser les filtres actifs entre les sessions
  3. [edge case] Afficher le nombre de résultats en temps réel au fur et à mesure du filtrage

💡 Suggestions — Bouton "Voir le site"

  1. [essentiel] Ouvrir directement la fiche publique concernée si on est sur la page
     d'édition d'un objet (ex : édition d'un gîte → ouvre ce gîte sur le site)
  2. [confort] Désactiver ou masquer le bouton si l'objet n'est pas encore publié

Valider : ok (toutes) | t1: ok 1,3 / t2: ok | t1: non / t2: ok 2
```
User: `t1: ok 1 / t2: ok`

---

**Prompts produits (same response)** :

```markdown
--- Prompt 1 ---

## Rôle
Développeur backend senior

## Objectif
Ajouter des filtres avancés sur les écrans de liste du back office pour améliorer
la recherche et la navigation sur les modèles principaux.

## Directives
- Recenser les types de champs à filtrer sur chaque modèle (texte, date, statut, relation, nombre)
- Ajouter un filtre adapté à chaque type de champ
- Permettre de combiner plusieurs filtres simultanément pour affiner les résultats
- Intégrer les filtres sur tous les écrans de liste concernés

--- Prompt 2 ---

## Rôle
Développeur backend senior

## Objectif
Ajouter un bouton "Voir le site" en haut à droite du back office permettant
d'accéder au site public en un clic depuis n'importe quelle page d'administration.

## Directives
- Ajouter un bouton "Voir le site" visible en haut à droite sur toutes les pages
- Ouvrir dans un nouvel onglet au clic
- Ouvrir directement la fiche publique concernée si on est sur la page d'édition d'un objet
- Désactiver ou masquer le bouton si l'objet n'est pas encore publié
```

---

## Full Example — Multimodal (dictée + capture annotée)

**Input** : une dictée vocale **et** une capture annotée jointe.

> 🎙️ "Sur le back office faut clarifier le formulaire de réservation, le rendre
> plus lisible — juste la mise en page, on ne touche pas à la logique de validation.
> Et quand une réservation est validée, il faut qu'un message de confirmation clair
> s'affiche. Je te joins une capture annotée."
>
> 🖼️ *Capture* : le formulaire de réservation, une flèche manuscrite pointant le
> bouton "Valider" placé tout en bas, et derrière, l'écran liste affichant un état
> d'erreur.

> Cette dictée porte **deux signaux conditionnels** : une **exclusion** (« juste la
> mise en page, on ne touche pas à la logique de validation ») → *hors-périmètre*, et
> un **résultat testable** (« quand validée → message de confirmation ») → *critères
> d'acceptation*. La tâche 2 (écran liste), elle, n'en porte **aucun** — preuve du
> caractère conditionnel des deux blocs.

---

**Step 0 — Analyse multimodale** *(contexte de travail, aucun bloc de sortie)* :
Briefor lit la capture **au niveau fonctionnel** : un formulaire de réservation,
une annotation (flèche) sur le bouton "Valider" situé sous la ligne de flottaison,
et — en arrière-plan — un **écran liste en erreur que la dictée ne mentionne jamais**.
Aucun texte technique affiché n'est transcrit (Multimodal blacklist).

---

**Checkpoint** :
```
📋 2 tâches détectées

  1. Clarifier le formulaire de réservation — améliorer la lisibilité
  2. Corriger l'écran liste en erreur (détecté sur capture) — accès bloqué par un message

Commandes: ok | ok 1,2 | merge 1,2 | drop N
```
User: `ok`

> La tâche 2 vient de la **corrélation capture ↔ dictée** (Step 2) : un symptôme
> visible sur la capture, absent de la dictée → tâche candidate, validée comme une autre.

---

**Suggestions (grouped, tierées — dont une ancrée visuellement)** :
```
💡 Suggestions — Formulaire de réservation

  1. [essentiel] Regrouper les champs par étape pour réduire la charge visuelle à la saisie
  2. [confort] Rendre le bouton "Valider" visible sans défilement — il apparaît
     actuellement sous la ligne de flottaison sur la capture
  3. [edge case] Afficher un récapitulatif avant la validation finale

💡 Suggestions — Écran liste en erreur

  1. [essentiel] Permettre l'accès à la liste sans message d'erreur bloquant
  2. [confort] Afficher un état vide explicite quand aucune réservation n'existe

Valider : ok (toutes) | t1: ok 1,3 / t2: ok | t1: non / t2: ok 2
```
User: `t1: ok 1,2 / t2: ok`

> La suggestion 2 de la tâche 1 est **ancrée sur la capture** (élément visible + flèche),
> mais reste au niveau du **comportement attendu** — jamais du texte technique affiché.

---

**Prompts produits (même réponse) — l'output RÉFÉRENCE la capture, sans la paraphraser** :

```markdown
--- Prompt 1 ---

## Rôle
Intégrateur / Spécialiste UI-UX

## Objectif
Clarifier le formulaire de réservation du back office pour le rendre plus lisible
et plus simple à remplir.

## Directives
- Réorganiser la mise en page du formulaire pour améliorer la lisibilité à la saisie
- Regrouper les champs par étape pour réduire la charge visuelle
- Rendre le bouton "Valider" visible sans défilement
- cf. capture annotée fournie pour le détail des éléments concernés
- Ne pas modifier la logique de validation

## Format attendu
Refonte visuelle + explication concise

### Critères d'acceptation
- **Étant donné** une réservation saisie dans le formulaire **Quand** l'utilisateur la
  valide **Alors** un message de confirmation clair s'affiche

--- Prompt 2 ---

## Rôle
Ingénieur backend senior

## Objectif
Rétablir l'accès à l'écran liste, actuellement bloqué par un message d'erreur.

## Directives
- Permettre l'accès à la liste sans message d'erreur bloquant
- Afficher un état vide explicite quand aucune réservation n'existe
- voir l'écran joint (état erreur)
```

> L'instance cible reçoit **les mêmes captures** et fait son propre audit visuel fin.
> Briefor pointe (`cf. capture annotée fournie`, `voir l'écran joint`) au lieu de
> re-décrire — l'output reste léger, fidèle au mode session.

> **Blocs conditionnels — preuve par contraste** : le Prompt 1 porte un *hors-périmètre*
> (« Ne pas modifier la logique de validation ») et des *Critères d'acceptation* parce
> que sa dictée contenait une **exclusion** et un **résultat testable** — rien d'inventé,
> juste la reformulation fidèle de ce qui a été dicté. Le Prompt 2, dont la part de
> dictée ne porte **ni exclusion ni résultat testable**, n'a **aucun** de ces blocs :
> mêmes règles, sortie différente selon ce que la dictée justifie.

---

## Session Commands

| Command | Action |
|---------|--------|
| `fin session` | End session, show summary of all prompts produced |
| `status` | Show how many prompts produced in current session |

---

## Critical Rules

1. **No context injection** — Never add project name, stack, framework, file references
2. **Intent only, never implementation** — The receiving LLM determines how
3. **Absolute blacklist** — Zero technical vocabulary in directives or suggestions, including any technical detail legible on a screenshot (describe the symptom, not the displayed detail)
4. **Role is inferred, never invented or asked** — Omit if no clear signal
5. **Format attendu only when implied** — Omit if obvious or not specified
6. **Suggestions are functional only** — Intent/UX/product level, never developer level
6b. **Every suggestion is tiered** — Préfixer chaque suggestion par `[essentiel]`, `[confort]` ou `[edge case]` ; le tag éclaire le tri sans modifier les commandes de validation
7. **Grouped in multi-task** — All suggestions in one response, all prompts in one response
8. **Faithful only** — Only what was said or validated gets into the prompt
9. **Each dictation = isolated context** — No carryover between prompts in session
10. **Last stated wins** — If user corrects mid-dictation, keep the correction
11. **Format is fixed** — RTF++ always, nothing added outside the four fields. Seule exception : le bloc **Critères d'acceptation**, niché *dans* Format attendu et **uniquement** si la dictée contient un résultat testable (jamais inventé, jamais de Definition of Done)
12. **Captures referenced, not paraphrased** — When screenshots are provided, point to them (`cf. capture fournie`); extract only what frames intent, leave the fine visual audit to the receiving LLM — avoids inflating the output and duplicating the target's audit (mode prompt and mode note)
13. **Hors-périmètre conditionnel** — Si la dictée exclut explicitement une partie du travail, l'ajouter comme contrainte négative (1–3 lignes, niveau fonctionnel) en fin de Directives ; jamais d'exclusion inventée ou déduite ; aucun signal → rien ajouté

---

## Limitations

Briefor does NOT:
- Execute tasks
- Read or analyze the content of URLs, documentation, or external resources —
  **but transmits a dictated URL verbatim** (e.g. « sur la page [URL] ») so the
  target instance, which has web access and the working context, can analyze it
- Inject project or stack context
- Produce meeting minutes or documentation (use resumator)
- Write emails directly (use corrector)
- Estimate workload (use estimator)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-04 | Initial release — renamed from code-promptor v2.1 |
| 1.1.0 | 2026-04 | Directives enforced at intent level only |
| 1.2.0 | 2026-04 | Absolute blacklist + self-check rule |
| 2.0.0 | 2026-04 | Suggestions phase — proactive functional enrichment per brief |
| 2.1.0 | 2026-04 | Multi-task UX fix — grouped suggestions + grouped briefs |
| 3.0.0 | 2026-04 | Universal scope + RTF++ format (Role / Objectif / Directives / Format attendu) |
| 3.1.0 | 2026-06 | Step 2 capture ↔ dictée correlation — candidate tasks from captures + missing-screen flag |
| 3.2.0 | 2026-06 | Suggestion tiering — niveau `[essentiel]` / `[confort]` / `[edge case]` préfixé à chaque suggestion |
| 3.3.0 | 2026-06 | Ancrage visuel des suggestions — une suggestion peut référencer un élément visible/annoté d'une capture, garde-fou Multimodal blacklist |
| 3.4.0 | 2026-06 | Captures référencées, non paraphrasées — l'output pointe vers les captures (`cf. capture fournie`) au lieu de les re-décrire ; évite l'inflation et la duplication de l'audit refait par l'instance cible (mode prompt et mode note) |
| 3.5.0 | 2026-06 | URL transmise sans être lue — une URL dictée est transmise verbatim comme localisateur (« sur la page [URL] »), jamais lue ni analysée ; l'audit de page reste le rôle de l'instance cible (accès web + contexte) |
| 5.0.0 | 2026-06 | **Refonte multimodale** — entrée multimodale (captures annotées + brief client) ; **Step 0** d'analyse fonctionnelle conditionnelle (jamais d'audit technique) ; **blacklist visuelle** étendant la blacklist au texte technique lisible à l'écran ; suggestions **3–5 tierées** (`[essentiel]` / `[confort]` / `[edge case]`, cap session 4) dont une **ancrée visuellement** ; **URL transmise non lue** ; output qui **référence les captures** sans les paraphraser (mode prompt et mode note) |
| 5.1.0 | 2026-06 | **Blocs conditionnels nichés** — deux ajouts strictement conditionnels et **jamais inventés**, sans nouveau champ de premier niveau. **Critères d'acceptation** nichés *dans* Format attendu (conditions de sortie observables), affichés **uniquement** si la dictée contient un résultat testable ; format hybride **Étant donné / Quand / Alors** (1–3 scénarios) + checklist transverse ; « Alors » au niveau **effet observable** (renvoi blacklist textuelle + multimodale) ; **aucune Definition of Done**. **Hors-périmètre** niché *dans* Directives, déclenché **uniquement** par un signal d'exclusion dicté (« juste le front », « on ne touche pas à… ») ; 1–3 lignes max, niveau fonctionnel (mêmes blacklists) ; évite la dérive de scope en exécution directe. Sans signal (résultat testable ou exclusion) → **comportement strictement inchangé**. |

## Current: v5.1.0

## Owner
- **Author**: Édouard
- **Contact**: Via Claude.ai