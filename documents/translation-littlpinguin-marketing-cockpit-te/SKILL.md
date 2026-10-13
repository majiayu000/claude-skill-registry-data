---
name: translation
description: Pipeline de traduction multi-agents vérifiée pour les contenus {{COMPANY_NAME}} — campagnes, landing pages, emails, articles, documents commerciaux. Traduction avec préservation de structure, vérification terminologique web parallèle (glossaire de marque avec scores de confiance), revue indépendante anti-fabrication, révision, mise en forme. La voix de marque se préserve dans la langue cible. Utiliser pour « traduis », « version anglaise/française de », « localise cette campagne », traduction de documents officiels ou techniques, ou quand une traduction précédente a fabriqué/omis du contenu. Vendorisée depuis claude-translation-skill (MIT, senshinji) — voir docs/vendored-design2.md.
---

# translation — traduction professionnelle multi-agents

Cette skill orchestre un pipeline complet : traduction avec préservation de structure, vérification terminologique par recherche web, revue qualité indépendante, révision, mise en forme. Une traduction une-passe sans vérification n'est acceptable que pour un texte court et sans enjeu — pour tout le reste, dérouler ce pipeline.

## Étape 0 — Contexte de marque (OBLIGATOIRE)

1. **Charger `01-brand/voice.md` et `01-brand/checklist-pre-composition.md`** : la voix de marque doit survivre à la traduction. Le vocabulaire interdit s'applique **dans les deux langues** (liste EN et FR de la checklist §2a + {{BRAND_VOCABULARY_BANNED}}) ; les règles anti-style-IA (cadratin, parallélismes négatifs) s'appliquent au texte cible.
2. **Formules signature** : elles ne se traduisent pas littéralement. Chercher l'équivalent validé dans le glossaire de marque ; s'il n'existe pas, proposer une adaptation et la faire valider avant de la figer.
3. **Glossaire de marque persistant** : `01-brand/glossaire-traduction.md`. S'il existe, il PRIME sur toute recherche web pour les termes qu'il couvre (noms de produits, claims, terminologie maison). Chaque mission de traduction l'enrichit : les nouveaux termes vérifiés à confiance haute y sont proposés à l'ajout après validation humaine.
4. Configuration bilingue : lire `.setup-completed` (`language`, `bilingual`). Un projet bilingue a souvent déjà des contenus dans la langue cible — les archives par canal sont un corpus de référence pour le ton cible.

## Architecture

```
            Demande de traduction
                     │
          Lead (cette session) : analyse,
          manifeste structurel, contrats
                     │
      ┌──────────────┼──────────────────┐
  traducteur    chercheur(s)         relecteur
  (subagent)    terminologie          (subagent,
      │         (subagent(s),          attend)
  Phase 1A :    parallèles)              │
  premier jet   Phase 1B : glossaire     │
      │         vérifié web              │
      ├──────────────┴──────────────────┤
      │        Phase 2 : revue          │
      │     ← feedback de revue ←       │
  Phase 3 : révision
      │
  Phase 4 : validation lead + mise en forme
```

Les agents se lancent via l'outil Agent (subagents `general-purpose`), **traducteur et chercheur(s) en parallèle dans un même message**. Le relecteur ne démarre qu'une fois les deux terminés.

## Phase 0 — Préparation (lead)

### 0.1 Analyser la source
- Langues source et cible ; type de document (post, email, landing, article, plaquette, contrat, programme d'événement…) ; longueur ; présence de terminologie spécialisée.
- **Format source (critique pour la structure)** : un `.doc`/`.docx` se convertit avec `textutil -convert html` (JAMAIS en txt — le texte brut détruit les tableaux que le traducteur doit préserver). Un livrable du template (md/html) se traduit dans son format natif, frontmatter et balisage intacts.
- **Manifeste structurel** (obligatoire avant de lancer les agents) : inventorier les tableaux (colonnes × lignes), les cellules multi-items (ex. « 10 interventions dans une seule ligne d'agenda »), la hiérarchie de titres. Sauver dans le workspace.
- **Découpage** si > 10 pages : chunks aux frontières de chapitres, jamais au milieu d'un tableau ; un traducteur par chunk, en parallèle.

### 0.2 Workspace et contrats

Workspace temporaire : `/tmp/translation-workspace/` (source.html, structure-manifest.md, first-pass.md, terminology-glossary.json, review-feedback.md, final-translation.md).

- **Contrat 1 — glossaire terminologique** (chercheur → traducteur, relecteur) : JSON, un objet par terme : `original`, `translation`, `category` (organization / person / place / venue / title / technical / product / event / brand), `confidence` (**high** = 2+ sources concordantes, **medium** = 1 source, **low** = meilleur jugement), `sources` (URLs). Les termes issus de `01-brand/glossaire-traduction.md` entrent avec `confidence: high, sources: ["glossaire de marque"]` et ne se re-vérifient pas.
- **Contrat 2 — feedback de revue** (relecteur → traducteur) : issues par priorité **FABRICATION > OMISSION > TERMINOLOGIE > EXACTITUDE > STRUCTURE > VOIX/REGISTRE**, chacune localisée avec citation source, texte fautif et correction proposée.

### 0.3 Dimensionnement
Estimer le nombre de termes propres (~8-10 par page : organisations, personnes avec titres, lieux, produits, événements, acronymes). ≤ 50 termes → un chercheur ; > 50 → deux chercheurs parallèles (fast : personnes/lieux/produits ; deep : organisations/technique/événements), le lead fusionne et déduplique les deux glossaires avant la revue.

## Phase 1 — Exécution parallèle

### Prompt du traducteur (subagent)

Consignes à inclure intégralement :

- Lire le manifeste structurel, puis la source (version .html si disponible). Traduire de [SOURCE] vers [CIBLE]. Sauver le premier jet dans le workspace.
- **Préservation de structure (critique)** : mêmes colonnes, même ordre, mêmes fusions de cellules ; correspondance 1:1 des lignes ; JAMAIS tableau→liste ni liste→tableau ; le contenu d'une cellule reste dans sa cellule, même long ; hiérarchie de titres niveau pour niveau ; listes ordonnées restent ordonnées ; ordre des paragraphes intact, pas de fusion/scission ; frontmatter, liens, balises et placeholders (`{{...}}`) intacts.
- **Rapport de structure obligatoire** avant de sauver : pour chaque tableau, `source [R]×[C] → traduction [R]×[C]` ; pour chaque cellule multi-items, confirmer que les items sont restés dedans. Toute violation se corrige AVANT de livrer.
- **Anti-fabrication** : ne JAMAIS inventer de contenu absent de la source ; marquer les passages illisibles `[peu clair dans l'original]` ; marquer la terminologie incertaine `[? terme ?]` pour le chercheur ; noms de personnes translittérés, jamais substitués ; noms de salles/lieux propres à un bâtiment translittérés, pas traduits comme le monument homonyme ; chiffres, dates, références copiés exactement.
- **Voix de marque** : appliquer `voice.md` dans la langue cible — registre, adresse (tu/vous ↔ you), vocabulaire interdit des deux langues, zéro cadratin. La traduction d'un post doit sonner comme un post écrit nativement dans la langue cible, pas comme une traduction.
- **Révision (phase 3)** : appliquer TOUTES les corrections critiques et majeures du feedback + les corrections de glossaire, **sans restructurer** — remplacement en place uniquement, jamais sortir du contenu d'une cellule, jamais changer le nombre de lignes/colonnes (violation observée en test réel : 13 échecs de structure). Sauver la version finale.

### Prompt du chercheur terminologie (subagent)

- Extraire TOUS les termes propres de la source : organisations, personnes avec titres, lieux et salles, événements, termes techniques, produits, marques, acronymes.
- Vérifier d'abord `01-brand/glossaire-traduction.md` (prime sur le web), puis pour chaque terme restant : recherche web du nom officiel dans la langue cible (site officiel → bases bilingues institutionnelles → nom publié de la personne). Par lots de 5.
- Scorer la confiance (high/medium/low), consigner les URLs. **Fallback** : après 2 échecs de recherche sur un terme, le marquer `low` avec note « recherche indisponible » et PASSER — ne jamais bloquer le glossaire pour quelques termes injoignables.
- Sauver le JSON, puis signaler la fin.

### Prompt du relecteur (subagent — modèle le plus capable disponible)

- Pré-check : le glossaire existe et son volume est plausible (~8-10 termes/page) ; sinon alerter avant de continuer.
- Revue systématique, priorités décroissantes :
  a. **FABRICATION (critique)** : paragraphe par paragraphe de la traduction, vérifier la correspondance source ; signaler tout contenu, chiffre, nom absent ou différent.
  b. **STRUCTURE (critique)** : recompter indépendamment lignes/colonnes de chaque tableau et le contenu des cellules multi-items ; produire un tableau comparatif `| Élément | Source | Traduction | OK ? |` — tout « NON » est critique.
  c. **OMISSION (critique)** : paragraphe par paragraphe de la SOURCE, vérifier que tout a sa traduction.
  d. **TERMINOLOGIE (majeur)** : chaque terme du glossaire utilisé conformément.
  e. **EXACTITUDE (majeur)** : chiffres, dates, noms propres exacts ; lieux translittérés correctement.
  f. **VOIX / REGISTRE (mineur→majeur si marque)** : registre conforme au type de document ET à `voice.md` ; aucun vocabulaire interdit dans la langue cible ; aucun tell IA introduit (cadratin, parallélisme négatif) ; formules signature correctement adaptées.
- Livrer le feedback structuré (issues critiques/majeures/mineures localisées et corrigées) + statistiques (compteurs, fabrication oui/non, conformité terminologique N/M, conformité structure).

## Phases 2-3 — Revue et révision

Automatiques : le relecteur démarre quand traduction + glossaire sont livrés ; le traducteur applique ensuite toutes les corrections critiques/majeures et sauve la version finale. Si le document était chunké, le lead concatène les chunks (et lisse titres/numérotations aux coutures) avant la revue.

## Phase 4 — Validation lead et livraison

1. **Vérification finale** : 5 paragraphes au hasard contre la source (fabrication) ; 10 termes du glossaire échantillonnés dans la version finale ; tout « NON » du tableau de structure corrigé ; premier et dernier paragraphe de chaque section présents.
2. **Brand-check** : le contenu traduit est un livrable comme un autre — le gate `brand-check` s'applique avant livraison.
3. **Mise en forme** :
   - Livrable du template (post, email, landing, article) → format natif, rangé dans le dossier du canal, calendrier éditorial mis à jour.
   - Document formel → si demandé, produire `.docx` et/ou `.pdf` via les skills docx/pdf : mise en page sobre (titre centré gras, hiérarchie 16/14/12pt, tableaux à bordures fines pleine largeur, A4 marges 2,5 cm, interligne 1,25, zéro décoration).
4. **Capitalisation** : proposer l'ajout des nouveaux termes à confiance haute dans `01-brand/glossaire-traduction.md` (avec validation humaine).

## Checklist anti-fabrication (rappel permanent)

- Ne jamais ajouter de contenu absent de la source ; ne jamais changer chiffres/noms/dates.
- Traducteur : correspondance paragraphe par paragraphe, incertitudes marquées, jamais résolues par invention.
- Relecteur : passe avant (traduction→source, attrape la fabrication) ET passe arrière (source→traduction, attrape l'omission).
- Pièges connus : inflation de chiffres, substitution de noms, confusion de lieux homonymes, remplissage de contenu, résumé substitué à la traduction intégrale.

---

*Vendorisée et adaptée depuis [claude-translation-skill](https://github.com/senshinji/claude-translation-skill) de senshinji (skill `translation-quality`, licence MIT) — orchestration portée d'Agent Teams (expérimental) vers les subagents standard, contexte marketing multilingue et glossaire de marque ajoutés. Attribution et procédure de re-synchronisation : `docs/vendored-design2.md`.*
