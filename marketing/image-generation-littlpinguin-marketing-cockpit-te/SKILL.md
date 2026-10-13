---
name: image-generation
description: Génération de visuels brand-compliant pour {{COMPANY_NAME}} — via Gemini direct (nano-banana, défaut) ou le MCP Magnific si connecté (Nano Banana 2.1, Seedream, upscaling). Étape obligatoire avant toute génération - consulter 01-brand/assets/index.md et proposer la réutilisation d'assets existants. Chaque prompt est automatiquement préfixé par les contraintes du style-guide (palette, typo, style d'illustration, interdits visuels). Règle d'or - générer la matière, composer le visuel final en HTML.
---

# image-generation — visuels brand-compliant {{COMPANY_NAME}}

Tu produis les visuels (heros, bannières, illustrations, icônes, portraits, bases de cartes sociales) de {{COMPANY_NAME}}. **Ta règle : jamais de requête brute.** Tu injectes la charte dans chaque prompt pour garantir la cohérence visuelle, et tu réutilises l'existant avant de générer.

## Étape 0 — Doctrine + assets (OBLIGATOIRE, avant toute génération)

1. Charger `01-brand/checklist-pre-composition.md` — règle assets, règle réutilisation, interdits visuels.
2. Lire `01-brand/style-guide.md` — palette, typographie, style d'illustration, éléments obligatoires, interdits.
3. **Lire `01-brand/assets/index.md`** — le catalogue navigable par rôle et cas d'usage — et **proposer d'abord la réutilisation ou la déclinaison d'un asset existant** (recadrage, recoloration, img2img à partir de l'asset) avant toute génération from scratch. Générer du neuf est le dernier recours.
4. **Analyser les vrais visuels publiés** (`01-brand/assets/`, `03-social-media/*/visuals/`, `06-graphic-design/outputs/`) — pas seulement les specs — pour capter la signature visuelle réelle. Sinon le rendu est « générique » et ne ressemble pas à la marque.
5. Charger `01-brand/design-anti-generique.md` — marqueurs du look IA interdits par défaut (gradient violet par réflexe, clusters génériques, faible densité) : à neutraliser dans chaque prompt, la marque primant là où elle parle.

**Ne jamais générer sans.** Si le style-guide contient encore des `{{...}}`, arrêter et lancer `/start-cockpit`.

## Règle d'or : GÉNÉRER POUR COMPOSER

Le modèle d'image produit la **matière visuelle** (illustrations, scènes, fonds, mockups au style de la marque) — **jamais la composition finale**. Le **texte, le vrai logo, les stats et les chiffres** sont ajoutés ensuite en **composition HTML → screenshot** (voir plus bas). On se comporte comme un graphiste : l'IA fournit les briques, on assemble.

- Texte généré par IA = générique + fautes possibles ; logo généré ≠ vrai logo ; composition entièrement générée = « n'importe quelle marque ».
- La génération full-texte reste possible pour un brouillon d'exploration rapide uniquement.

## Providers — abstraction

Deux chemins de génération, **mêmes règles de préfixage marque dans les deux cas** :

### A. Gemini direct (défaut — « nano-banana »)

- `GOOGLE_AI_API_KEY` dans `.env` ; modèle `GOOGLE_AI_IMAGE_MODEL` (défaut `gemini-nano-banana-2.1`).

```python
import os, requests
API_KEY = os.environ["GOOGLE_AI_API_KEY"]
MODEL = os.environ.get("GOOGLE_AI_IMAGE_MODEL", "gemini-nano-banana-2.1")
url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"
payload = {
    "contents": [{"parts": [{"text": full_prompt}]}],   # + part image inline pour l'img2img
    "generationConfig": {
        "responseModalities": ["IMAGE"],
        "temperature": 0.4,
        "imageConfig": {"aspectRatio": "3:4", "imageSize": "2K"},
    },
}
r = requests.post(url, params={"key": API_KEY}, json=payload, timeout=120)
```

- **Temperature** : `0.4` fidèle au prompt (portraits, mockups) · `0.7` créatif (illustrations) · `1.0+` expérimental.
- **Ratios supportés** : `1:1`, `2:3`, `3:2`, `3:4`, `4:3`, `4:5`, `5:4`, `9:16`, `16:9`, `21:9` (+ formats bannières). **Tailles** : `1K` (défaut), `2K`, `4K`.
- Mentionner le ratio **dans le texte du prompt ET dans `imageConfig`** (le paramètre seul peut être ignoré).

### B. MCP Magnific (si connecté)

Si un serveur MCP Magnific est configuré (vérifier ses outils en session), l'utiliser comme routeur multi-modèles :

- **Génération** : Nano Banana 2.1, Seedream, et tout modèle exposé par le MCP — choisir selon le besoin (photoréalisme, illustration, texte dans l'image).
- **Upscaling / amélioration** : passer les sorties destinées à l'impression ou au zoom par l'upscaler Magnific plutôt que régénérer en 4K.
- **Même préfixage automatique** du prompt par les contraintes du style-guide qu'en voie A — l'abstraction ne change que le transport, jamais la doctrine.

Si le MCP n'est pas connecté, ne pas le suggérer comme prérequis : la voie A couvre tout. Mentionner qu'il s'active via `/tools-setup`.

#### Discipline de dépense (le MCP consomme des crédits réels)

- **Itérer là où c'est inclus, produire par le MCP.** Certains abonnements incluent des générations illimitées en basse résolution **dans l'application web uniquement** — via le MCP, tout se facture (le serveur le signale : `unlimitedAppliesHere: false`). Toute exploration (cadrage, style, formulation du prompt) se fait côté web ; le MCP sert au rendu final validé.
- **Vérifier le solde en direct avant de chiffrer ou lancer une série** (`account_balance`) — jamais de solde de mémoire : un chiffre périmé fait proposer des plans infinançables.
- **Simuler le coût avant de générer** (`simulate_cost`) quand l'outil le permet ; s'il échoue pour un type de génération, lancer **un** exemplaire pour connaître le tarif réel avant la série.
- **Jamais de série avant qu'un exemplaire soit validé** par l'utilisateur — générer en lot sur un prompt non validé, c'est jeter des crédits.
- **Itérer par édition** (repasser la sortie en référence + instruction courte), jamais en re-roll complet.

## Workflow

### 1. Parser la demande

Extraire de la demande utilisateur :
- **Format** : ratio (carré / 16:9 / 9:16 / 4:5 / bannière)
- **Usage** : où le visuel sera placé (post LinkedIn, hero web, cover, infographie)
- **Sujet** : description du contenu visuel
- **Contraintes** : texte à intégrer (→ composition, pas génération), éléments imposés

### 2. Construire le prompt final (préfixage automatique)

Concaténation structurée envoyée au provider (A ou B) :

```
[BRAND CONSTRAINTS — NON-NEGOTIABLE]
- Color palette: primary {{BRAND_COLOR_PRIMARY}}, accent {{BRAND_COLOR_ACCENT}}, dark {{BRAND_COLOR_DARK}}, light background {{BRAND_COLOR_LIGHT}}
- Signature gradient: {{BRAND_GRADIENT}}
- Typography (if any text): {{BRAND_FONT_PRIMARY}}
- Illustration style: {{BRAND_ILLUSTRATION_STYLE}}
- MUST include: [éléments obligatoires du style-guide]
- MUST NOT include: {{BRAND_BANNED_VISUALS}}, no stock photos, no generic office imagery

[USER REQUEST]
[demande utilisateur, reformulée en scène complète]

[FORMAT]
Aspect ratio: [16:9 / 1:1 / etc.]
High resolution, no text watermark, suitable for [usage].
```

**Règles de prompting** :
- Penser « directeur artistique » : décrire une **scène** (phrases complètes), pas une liste de tags.
- Spécifier les hex exacts, l'éclairage, la composition (angle, profondeur de champ, espace négatif).
- Pas de tags boosters (« 4K, ultra-realistic, best quality ») — inopérants.
- Pas de négations (« no office ») — formuler positivement ce qu'on VEUT.
- Prompt < 20 mots = trop court.
- Résultat à 80% satisfaisant → affiner en **img2img**, pas régénérer le même prompt.

### 3. img2img — décliner un asset existant (recette validée)

Pour tout objet/picto qui doit ressembler aux illustrations de la marque, **partir d'un asset existant comme référence de style** :

1. Rendre un asset vectoriel de marque en PNG de référence (ex. `qlmanage -t -s 700 <scene>.svg -o <tmp>` sur macOS).
2. img2img avec ce PNG en entrée + prompt qui demande de **n'emprunter QUE le style** : « Using the EXACT illustration style of the reference image ({{BRAND_ILLUSTRATION_STYLE}}), draw a single <OBJET>. Do NOT keep the subjects or props from the reference; only borrow its drawing style. Color it with the brand palette (hex...). Center it with generous negative space on a plain background. No text, no logo, no people. »
3. Le modèle ramène souvent des éléments de la référence : les retirer en post (recadrage + fond transparent par **flood-fill depuis les 4 coins** — préserve les blancs intérieurs, contrairement à un color-key global).

### 4. Sauvegarder image + métadonnées (provenance)

```
06-graphic-design/outputs/
├── YYYY-MM-DD-<slug>.png              ← image générée (staging)
└── YYYY-MM-DD-<slug>.png.gen.json     ← fiche de génération (sidecar)
```

Juste après l'écriture des octets renvoyés par le modèle, appeler
`genmeta.finalize_output(chemin, meta)` (`06-graphic-design/scripts/genmeta.py`, aucune
dépendance réseau). En un geste, il :

- **remet l'extension d'aplomb** : l'API renvoie parfois du JPEG sous un nom `.png` ; le
  fichier est renommé, jamais réencodé (un réencodage efface le manifeste C2PA) ;
- **pose un tag PNG** `ai:generated_by` (chunk `tEXt`), sauf si le fichier porte déjà un
  manifeste C2PA, qui vaut mieux que le tag et qu'une resauvegarde effacerait ;
- **écrit la fiche** `<image>.gen.json` en dernier, pour que son sha256 décrive le fichier
  livré.

```python
import sys; sys.path.insert(0, "06-graphic-design/scripts")
import genmeta
final = genmeta.finalize_output(chemin, {
    "model": "gemini-nano-banana-2.1",
    "prompt": full_prompt,                 # le prompt intégral envoyé, préfixe de marque compris
    "prompt_file": None, "input_images": [],   # images d'entrée d'un img2img
    "temperature": 0.4, "aspect_ratio": "16:9", "image_size": "2K",
    "script": "<script ou session de génération>",
    "provider": "gemini-direct",           # clés libres conservées : provider, use, format…
    "use": "landing page hero",
})
print(final)   # chemin final : l'extension a pu changer
```

En mode série, tester l'existence d'une sortie avec `genmeta.existing_variant(chemin)`
(elle a pu sortir en `.jpg`) avant de relancer une génération facturée. Les fiches
`*.gen.json` ne sont pas versionnées : elles suivent leur image.

**Provenance, ce qui survit** : la fiche de génération suit l'asset à la promotion ; le tag
PNG survit à une copie octet à octet mais pas à un réencodage ; le manifeste C2PA des sorties
JPEG du modèle (`has_c2pa`, heuristique) survit tant que personne ne réencode le fichier.

### 5. Check de conformité

Avant livraison, inspecter visuellement :
- ✅ Palette respectée (dominantes = primaire/accent)
- ✅ Style conforme à `{{BRAND_ILLUSTRATION_STYLE}}`
- ✅ Aucun élément visuel interdit
- ✅ Ratio correct

Échec sur un point → **régénérer avec un prompt renforcé** sur l'axe fautif. Max 3 tentatives, puis remonter à l'utilisateur.

### 6. Promotion en asset officiel (après validation humaine)

Une sortie validée et réutilisable migre de `06-graphic-design/outputs/` (staging) vers `01-brand/assets/` : catégoriser, nommer selon la convention du catalogue, **ajouter sa fiche dans `01-brand/assets/index.md`** (rôle, palette, quand l'utiliser / ne pas l'utiliser). Un asset généré non promu reste en staging et n'est jamais référencé comme officiel.

Le geste est outillé, et c'est le seul admis :

```bash
python3 06-graphic-design/scripts/promote-asset.py 06-graphic-design/outputs/<fichier> \
  --dest <categorie>/<sous-dossier>/<categorie>_<sujet>_<variante>.<ext> \
  --droits "<licence ou base légale>" --auteur "<qui l'a produit>" \
  --role "..." --usage "..." [--not "..."] [--copy]
```

Il refuse un nom non conforme, une catégorie inconnue, un écrasement, et une fiche sans les trois champs de droits (`--source`, `--droits`, `--auteur` ; `--droits "à confirmer"` est une valeur admise et signalée). Avec une fiche de génération à côté de la source, il renseigne d'office `généré-par-ia: oui`, le modèle et un extrait du prompt, déduit `--source`, et fait suivre la fiche. Le catalogue `01-brand/assets/index.md` doit exister (une section `## <categorie>/` par catégorie).

## Composer un visuel fini (générer → composer)

Pour tout visuel **avec texte, data ou logo** (la majorité des cas) :

1. **Générer ou réutiliser la matière** — uniquement l'illustration / le fond / la scène, **sans texte ni logo** (fond uni → intégration facile). Souvent, aucun besoin de générer : un asset du catalogue suffit.
2. **Réutiliser les vrais assets** depuis `01-brand/assets/index.md` : logo SVG **inliné** (jamais le nom de marque tapé au clavier), portraits réels, motifs, textures.
3. **Composer en HTML** en linkant `06-graphic-design/lib/compose.css` : il importe la police de marque en **local** (`01-brand/assets/fonts/fonts.css`, voir `06-graphic-design/lib/README.md` pour l'installer et vérifier sa licence) et les tokens de marque (`presentations/tokens.css`), plus quelques aides `compo-`. Jamais de webfont CDN pour un screenshot : Chrome headless capture avant le chargement → texte rendu en Helvetica.
4. **Penser en grille** : dimensionner les éléments les uns par rapport aux autres (déco = largeur du logo, modules de hauteur partagés). Préférer une disposition asymétrique/organique au miroir rigide.
5. **QA avant capture** : `python3 06-graphic-design/scripts/qa-visuel.py <compo.html> --viewport <L>x<H>` (couleurs contre `tokens.json`, police, plancher, contraste, zone de protection du logo). Zéro erreur avant de capturer.
6. **Screenshot** : `06-graphic-design/scripts/compose-screenshot.sh <compo.html> <sortie.png> <L> <H>` (Chrome headless, rendu 2× puis redimensionné → texte net), puis `qa-visuel.py <sortie.png>` sur l'image (couleurs seules : il n'y a plus de DOM).
7. **Livrer** dans le dossier du canal (+ archiver le `.html` source dans `outputs/`).

### Checklist qualité (avant de livrer)

- [ ] Police de marque effective (zoomer sur un mot bas-de-casse — pas de Helvetica de substitution)
- [ ] **Vrai logo** SVG inliné (jamais généré ni tapé)
- [ ] Couleurs hex exactes ; gradient signature présent si la charte l'exige
- [ ] Tailles calées sur une grille (rien « au hasard »)
- [ ] Aucune photo stock, aucun trope interdit
- [ ] Un seul chiffre héros pour un visuel social ; texte net, zéro faute
- [ ] Format/ratio conforme à l'usage ; export à la bonne dimension

## Règles d'usage

### Autorisé
- Prompts directs avec description de sujet
- Séries de variations (3-5 appels avec variantes de prompt)
- img2img de déclinaison d'assets existants

### Interdit
- Générer un visage reconnaissable (deepfake) sans consentement
- Générer le logo d'un concurrent
- Reproduire un style sous copyright (artiste vivant nommé, franchise)
- Générer du contenu qui contredit la doctrine de voix

### Limites techniques des modèles
- **Texte dans l'image** : rendu incertain, fautes possibles → composer le texte en HTML (règle d'or)
- **Visages humains** : plausibles mais artefacts possibles
- **Logos** : le modèle ne connaît pas le vôtre → toujours composer avec le vrai SVG
- **Négation inopérante** : « no office » peut produire un bureau → reformuler positivement

## Divulgation IA

La politique de divulgation IA de la marque vit dans `01-brand/divulgation-ia.md` : la lire avant de livrer un visuel destiné à la publication. Elle donne le type de contenu qui se mentionne, la formulation exacte par canal, et le champ `généré-par-ia:` à renseigner dans la fiche d'asset. Avant de publier un logo tiers, une photo ou un portrait d'une personne réelle, vérifier son statut dans `01-brand/droits.md`.

## Après livraison

Indexer le visuel final dans `_templates/inventory.md` (skill `inventory`, type `image`) — et consulter ce même inventaire avant de générer, pour réutiliser un asset existant plutôt que produire un doublon.

## Personnalisation par marque

{{IMAGE_GEN_SPECIFIC_RULES}}

## Exemples de prompts qui fonctionnent

{{IMAGE_GEN_EXAMPLES}}

## Skills associées

- `carousel` / `slides` / `social-content` — consommateurs des visuels produits ici
- `brand-check` — validation de conformité sur le sidecar en cas de doute
