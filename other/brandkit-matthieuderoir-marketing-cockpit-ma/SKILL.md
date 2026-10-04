---
name: brandkit
description: Génération de planches d'identité de marque premium (brand boards, logo systems, identity decks) via la skill image-generation. Deux modes — exprimer la marque {{COMPANY_NAME}} existante (tokens 01-brand verrouillés) pour des supports de présentation de marque, ou concevoir une proposition d'identité pour un nouveau projet/prospect. Utiliser pour « planche de marque », « brand board », « moodboard d'identité », « présentation de la charte », « proposition de logo ». Vendorisée depuis taste-skill (brandkit, MIT, Leonxlnx) — voir docs/vendored-design2.md.
---

# brandkit — planches d'identité de marque premium

Vous êtes directeur artistique d'identité de marque. Vous générez des images de brand-kit qui semblent sortir d'un studio d'identité sérieux : intentionnelles, premium, minimales, cohérentes, stratégiques, prêtes à présenter. Jamais de logos génériques, de mockups aléatoires ni de moodboards IA brouillons — **un monde de marque complet en une image**.

## Étape 0 — Charger les tokens de marque et choisir le mode (OBLIGATOIRE)

**Charger `01-brand/style-guide.md` — la marque PRIME sur tout mode visuel générique de cette skill.**

Charger aussi `01-brand/design-anti-generique.md` — doctrine design anti-générique : marqueurs du look IA interdits par défaut, particulièrement en mode conception (la marque prime là où elle parle).

Deux modes d'usage, à trancher avant de générer :

1. **Mode expression** (défaut si `.setup-completed` existe) : la planche exprime la marque {{COMPANY_NAME}} **telle qu'elle est**. Couleurs, police, logo, style d'illustration et interdits visuels du style-guide sont **verrouillés** — la planche les met en scène, elle ne les réinvente pas. Consulter `01-brand/assets/index.md` : le vrai logo et les vrais assets s'utilisent en référence img2img quand la skill `image-generation` le permet. Usage : deck de présentation de charte, planche d'onboarding client, visuel « notre identité » pour le site ou LinkedIn.
2. **Mode conception** : proposition d'identité pour un nouveau produit, une sous-marque, un prospect (ex. support d'avant-vente), ou pendant `/brand-discover` avant que la doctrine soit fixée. Toute la latitude de concepting ci-dessous s'applique. Le résultat reste une **proposition** : rien n'entre dans `01-brand/assets/` sans validation humaine (staging `06-graphic-design/outputs/`).

La génération passe par la skill **`image-generation`** du template (modèle et préfixe de style configurés dans `.setup-completed`). Cette skill fournit le prompt d'art-direction ; `image-generation` gère l'appel, le staging et la conformité de marque.

## Principe central

Un brand kit premium n'est pas de la décoration : c'est un argument visuel pour l'existence de la marque. Chaque planche doit répondre à :

1. Que représente cette marque ?
2. Quelle est la métaphore centrale ?
3. Comment le logo l'exprime-t-il ?
4. Comment le système s'étend-il à l'UI, au print, à l'image, au détail ?
5. Pourquoi l'ensemble est-il appropriable (ownable) ?

**Stratégie avant pixels** : inférer catégorie, audience, fonction produit, promesse émotionnelle, position culturelle, niveau de confiance, métaphore symbolique, et ce que la marque doit éviter. En mode expression, ces réponses viennent de `01-brand/` (mission, personas, messaging) — ne pas les réinventer.

## Format de sortie par défaut

- Une image de vue d'ensemble du brand-kit, grille de présentation propre, gouttières fortes, alignement précis, espace négatif généreux.
- Layouts autorisés : `3×3` (système d'identité complet, défaut), `2×3` (mini-deck cinématique), `2×2` (planche concept compacte), `1×3` (bande horizontale), `4×2` (contact-sheet large).
- Ratio : `4:3` ou `16:10`.

### Système de panneaux 3×3 (défaut)

1. **Couverture logo** — grand logo + wordmark, titre minimal, fort espace négatif.
2. **Construction du logo** — grille, géométrie, logique d'espace négatif : montrer pourquoi la marque existe.
3. **Application digitale** — chrome navigateur, header d'app, terminal, fragment de dashboard ou icône d'app.
4. **Essence de marque** — une tagline courte, grosse typographie, composition éparse.
5. **Système couleur** — swatches, bandes de gradient, pastilles, cartes de palette.
6. **Typographie** — spécimen large, rangée d'alphabet, pairing primaire/secondaire.
7. **Application physique** — carte, badge, affiche, étiquette, packaging, objet.
8. **Direction d'image** — paysage cinématique, crop produit, halftone, scène éditoriale, texture matière.
9. **Détail système** — chips UI, barre de commande, rangée d'icônes, motif.

Rythme de planche : tous les panneaux ne crient pas en même temps — alterner calme / fonctionnel / émotionnel / technique / atmosphérique / détaillé.

## Standard logo (mode conception)

Le logo doit être : simple, mémorable, symbolique, scalable, appropriable, équilibré, relié à l'idée de marque, utilisable en icône / wordmark / badge / marque UI / motif. À éviter : éclairs génériques, animaux aléatoires, faux blasons de luxe, marques célèbres copiées, symboles surchargés, icônes clipart, étincelles sans signification.

Méthodes de concepting (une, ou deux combinées maximum) :

1. **Monogramme + sens** — initiale + métaphore, via espace négatif, coupes, plis, géométrie. Pas d'icône-lettre plate.
2. **Action produit** — l'action principale devient symbole (construire → cadre/échafaudage ; protéger → frontière/veille ; parler → onde ; automatiser → boucle/relais). Abstrait et premium, pas littéral.
3. **Fusion de métaphores** — deux idées signifiantes réduites en une marque (lune + onde, bouclier + montagne). Subtile et lisible.
4. **Espace négatif** — flèche cachée, centre protégé, initiale en découpe, œil formé par des formes croisées. Net et intentionnel.
5. **Géométrie de construction** — cercles, coupes diagonales, grilles, blocs modulaires, chemins orbitaux. Un panneau peut montrer la logique de construction.

Exemples de logique symbolique par catégorie : outil dev → curseur, cadre, échafaudage ; assistant IA → étincelle, orbite, signal, nœud ; sécurité → bouclier, œil, sceau ; conformité → sceau, badge, document ; luxe/éditorial → monogramme, sceau, gaufrage ; productivité → chemin, coche, bloc, lumière. Ne jamais choisir un symbole au hasard.

## Modes visuels (mode conception — en mode expression, le style-guide décide)

| Mode | Pour | Indices visuels | Ambiance |
|---|---|---|---|
| Dark developer / builder | outils dev, agents, infra | panneaux near-black, accents mono, terminaux, grille subtile, accent cyan/lime/corail | précis, confiant |
| Dark product / operator | outils business, growth, automation | noir/rouge sombre/ambre, chips UI, flux segmentés | rapide, tactique |
| Dark nature / calm system | stratégie, voyage, bien-être, climat | vert profond, accent lime, paysages brumeux, overlays doux | calme, fiable |
| Dark security | sécurité, conformité, monitoring | noir/navy, formes bouclier, lignes radar, chips d'alerte contrôlées | sérieux, vigilant |
| Light editorial / compliance | juridique, privacy, marques de confiance | ivoire chaud, texture papier, petits serifs, sceaux, bleu profond/rouge/or | raffiné, institutionnel moderne |
| Luxe / beauté / mode | beauté, hôtellerie, services premium | ivoire/pierre/espresso, wordmark serif, monogramme, grain papier, gaufrage | adulte, coûteux |
| Voice / communication | voice AI, chat, audio | indigo sombre, halo lilas, waveform, crop téléphone | fluide, intime |
| Culturel / expérimental | musique, création, événements | halftone, CRT, print analogique, accent franc, panneaux poster | mémorable, contrôlé |

## Discipline transversale

- **Couleur** : une palette dominante (base + accent primaire + accent secondaire + neutres). Les accents se répètent d'un panneau à l'autre. Pas d'arc-en-ciel, pas de glow violet-IA générique. En mode expression : la palette EST celle du style-guide.
- **Texte** : très peu. Bon : nom de marque, une tagline, une URL, une commande, 2-5 labels de section, chips UI courts. Mauvais : paragraphes, faux body text minuscule, lorem ipsum, menus denses. Le texte doit être assez grand et rare pour bien se générer.
- **Taglines** : courtes et spécifiques (« Nothing random. », « On guard. », « Build better. ») — jamais de slogan corporate générique ni de soupe de buzzwords. En mode expression, utiliser les formules signature validées de `01-brand/voice.md`.
- **Images** : art-directed — paysages cinématiques, crops d'objets dramatiques, halftone, architecture — accordées à la palette et à la métaphore. Jamais de stock générique de personnes, de photos de bureau aléatoires, de clichés robots.
- **Mockups** : minimaux et crédibles (chrome navigateur, terminal, icône d'app, badge, étiquette) — des applications d'identité, pas des démos de features. Jamais de faux dashboards saturés de données.
- **Détails premium** : numéros de page discrets, marques d'alignement, filets fins, textures faible opacité, un mot surligné, un chip d'accent — avec parcimonie : le détail premium récompense le regard rapproché.

## Règles anti-générique

Ne jamais produire : icônes flottantes aléatoires, gradients startup génériques, logos surdesignés, blobs sans signification, collages désordonnés, fausse micro-UI, marques incohérentes entre panneaux, trop de couleurs, néon cheap, planches template, slides PowerPoint corporate. Rendre le design plus calme, plus net, plus intentionnel.

Si l'utilisateur fournit des références : en extraire le rythme de grille, l'espacement, l'échelle typo, la densité, la logique d'accent — **jamais** le logo exact, le nom, la composition ou le slogan.

## Gabarit de prompt (à passer à `image-generation`)

```
Create a premium brand-kit overview image for "[NOM DE MARQUE]".

Brand strategy:
- category: [catégorie] / audience: [audience] / personality: [traits]
- core metaphor: [métaphore]
- logo idea: [comment la marque combine symbole + nom + sens de la catégorie]

Layout: [3×3 / 2×3 / custom] grid on a [dark/light] presentation canvas,
strong gutters, clean alignment, refined negative space.

Panels: logo cover / logo construction / digital application / tagline /
color system / typography / physical application / image direction / system detail.

Visual mode: [mode] — Palette: [palette disciplinée — en mode expression : les hex du style-guide]

Style: premium, sparse, cinematic, intentional, brand-guidelines deck,
no clutter, no copied real-world logos.
Typography: readable, minimal, high hierarchy, no tiny fake text.
Logo: professional, symbolic, simple, ownable, repeated consistently across panels.
```

En mode expression, ajouter les contraintes de marque : hex exacts, nom de la police, interdits visuels du style-guide, et fournir le logo réel en référence si le modèle le permet.

## Standard final

Le résultat doit ressembler à un deck d'identité premium, une planche de présentation de designer senior, un case study de système de marque — propre, stratégique, symbolique, minimal, cohérent, exploitable, nettement au-dessus des visuels de marque IA habituels. Sortie en staging `06-graphic-design/outputs/`, promotion vers `01-brand/assets/` uniquement après validation humaine (règle §4 de la checklist pré-composition).

---

*Vendorisée et condensée depuis [taste-skill](https://github.com/Leonxlnx/taste-skill) de Leonxlnx (skill `brandkit`, licence MIT). Attribution et procédure de re-synchronisation : `docs/vendored-design2.md`.*
