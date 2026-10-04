---
name: video-editing
description: Montage vidéo assisté par IA pour {{COMPANY_NAME}} — du brief à l'export par plateforme. Pilote Palmier Pro via MCP (macOS Apple Silicon) ou produit un plan de montage ffmpeg en fallback, structure les vidéos courtes (hook 3 s, rythme, formats 9:16/16:9/1:1), habille aux couleurs de la marque (tokens 01-brand) et exporte selon les specs de 08-video/formats.md. À utiliser dès que l'utilisateur demande un montage, une vidéo courte, un Reel, un TikTok, un Short, une vidéo LinkedIn, une déclinaison vidéo d'un contenu existant. Pour le sous-titrage seul → skill `captions`. Pour un visuel fixe → `image-generation`.
---

# video-editing — montage vidéo pour {{COMPANY_NAME}}

Vous transformez un brief en vidéo montée, habillée aux couleurs de la marque et exportée aux bons formats. Le travail vit dans `08-video/` — lire `08-video/CLAUDE.md` et `08-video/README.md` (outillage) avant la première production.

## Références à charger avant de commencer

1. `08-video/formats.md` — ratios, durées, zones de sécurité de la plateforme cible
2. `01-brand/style-guide.md` — tokens (couleurs, police, style, tropes bannis)
3. `01-brand/voice.md` — pour tout texte à l'écran
4. `03-social-media/<canal>/examples/` — calibrer hooks et ton sur ce qui a déjà marché

## Étape 1 — Brief

Créer/valider `08-video/briefs/<slug>.md` :

```markdown
# <slug>
- Objectif : (notoriété / trafic / conversion)
- Canal(aux) : (tiktok / reels / shorts / linkedin) → format cible selon formats.md
- Durée cible : (ex. 30 s)
- Persona : (cf. 01-brand/personas.md)
- Message unique : une seule idée par vidéo
- Matière : rushes existants ? à générer ? screencast ? face caméra ?
- CTA final : ...
```

Pas de brief validé → pas de montage.

## Étape 2 — Structure (le script minuté)

Écrire `08-video/scripts/<slug>.md` avec un tableau minuté. Les règles du format court — actionnables, pas décoratives :

- **Hook ≤ 3 secondes** : la première frame doit poser une tension (question, chiffre surprenant, résultat avant/après, contradiction). Si le hook ne tient pas en une phrase lisible à l'arrêt sur image, il est raté. Proposer **3 variantes de hook**, validation humaine obligatoire.
- **Un cut toutes les 2–4 s** : jamais plus de 5 s sur le même plan sans changement (zoom, plan, texte). Le rythme se voit dans le tableau minuté.
- **Texte à l'écran en permanence** : la majorité regarde sans le son. Chaque segment a son texte (repris par la skill `captions`).
- **Une idée, une vidéo** : si le script contient « et aussi », couper — c'est la vidéo suivante.
- **CTA en fin, une seule action** : commenter, suivre, cliquer — pas les trois.
- **Boucle** : si possible, la dernière seconde renvoie visuellement à la première (relecture = signal fort sur TikTok/Reels).

```markdown
| t | Plan | Texte à l'écran | Audio/VO |
|---|---|---|---|
| 0-3 s | ... (HOOK) | ... | ... |
| 3-8 s | ... | ... | ... |
```

## Étape 3 — Montage

### Voie A — Palmier Pro via MCP (préférée, macOS Apple Silicon)

Si le serveur MCP Palmier Pro est configuré (dans le `.mcp.json` local, non versionné) :

1. Vérifier que l'app est ouverte et le serveur répond (un appel de listing simple d'abord).
2. Créer le projet au format cible (ex. 1080×1920 pour 9:16).
3. Importer les rushes (`08-video/rushes/<slug>/`). S'il manque de la matière : modèles intégrés (Seedance, Kling — abonnement) ou Magnific MCP, cf. `08-video/README.md`. Vérifier `01-brand/assets/` avant de générer.
4. Poser les cuts selon le script minuté, plan par plan.
5. Laisser l'humain faire les ajustements fins dans l'UI ; ne jamais écraser une modification manuelle sans le signaler.

Les noms exacts des outils MCP dépendent de la version de Palmier Pro : les découvrir en session, ne pas les inventer.

### Voie B — Plan de montage ffmpeg (fallback)

Sans Palmier Pro, produire un **plan de montage** : une suite de commandes ffmpeg commentées dans `08-video/scripts/<slug>-montage.sh`, exécutées après validation humaine. Briques types :

```bash
# Découper un segment (sans ré-encodage si les points tombent sur des keyframes)
ffmpeg -ss 00:00:12 -to 00:00:18 -i rushes/plan1.mp4 -c copy tmp/seg1.mp4

# Recadrer un 16:9 en 9:16 (crop centré puis mise à l'échelle)
ffmpeg -i tmp/seg1.mp4 -vf "crop=ih*9/16:ih,scale=1080:1920" tmp/seg1-vertical.mp4

# Concaténer les segments (fichier liste.txt : file 'tmp/seg1-vertical.mp4' …)
ffmpeg -f concat -safe 0 -i liste.txt -c:v libx264 -crf 18 -c:a aac tmp/montage.mp4

# Poser un clip sur fond de marque (déclinaison 1:1 LinkedIn)
ffmpeg -i tmp/montage.mp4 -vf "scale=608:1080,pad=1080:1080:236:0:color={{BRAND_COLOR_DARK}}" tmp/carre.mp4
```

## Étape 4 — Habillage aux couleurs de la marque

Tout élément graphique utilise les tokens de `01-brand/style-guide.md` :

- **Textes à l'écran** : police `{{BRAND_FONT_PRIMARY}}`, couleurs `{{BRAND_COLOR_LIGHT}}` / `{{BRAND_COLOR_PRIMARY}}`, jamais plus de 2 niveaux de texte simultanés.
- **Fonds, bandeaux, transitions** : `{{BRAND_COLOR_DARK}}` / `{{BRAND_COLOR_PRIMARY}}` / `{{BRAND_GRADIENT}}` — pas de couleurs hors palette.
- **Logo** : plan de fin uniquement (ou discret en zone sûre), depuis `01-brand/assets/`.
- **Interdits** : les tropes de `{{BRAND_BANNED_VISUALS}}`, les templates d'habillage génériques, les emojis en pluie.
- **Zones de sécurité** : aucun texte dans les marges définies par `08-video/formats.md`.

Sous-titres : déléguer à la skill **`captions`** (transcription, segments, `.srt` + burn-in stylé marque).

## Étape 5 — Export par plateforme

Un export par canal cible, nommé `08-video/exports/<slug>-<plateforme>.mp4`, aux specs exactes de `formats.md` :

```bash
# Export final H.264 + AAC, 1080×1920, qualité sociale
ffmpeg -i tmp/final.mp4 -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p \
  -c:a aac -b:a 192k -movflags +faststart exports/<slug>-tiktok.mp4
```

## Checklist avant livraison

- [ ] Hook lisible à l'arrêt sur image, validé par un humain
- [ ] Aucun plan > 5 s sans changement
- [ ] Sous-titres présents (skill `captions`), hors zones de sécurité
- [ ] Habillage 100 % tokens de marque, zéro trope banni
- [ ] Un export conforme par plateforme (`formats.md`)
- [ ] Disclosure IA si clips générés (politique de la marque)
- [ ] `brand-check` sur le script + textes à l'écran
- [ ] Statut mis à jour dans le calendrier éditorial

## Règles état de l'art (2026)

Voir `docs/etat-de-lart/video-courte.md` pour le détail sourcé :

1. **Gabarit de script imposé** : Hook 0-3 s → Value drop 4-15 s → Payoff → CTA dans les 5 dernières secondes, avec un beat visuel ou narratif toutes les 5-7 secondes.
2. **Jamais de logo, jingle ou plan d'installation en ouverture** — 50-60 % des abandons ont lieu dans les 3 premières secondes.
3. **Couper 20-30 % du script au montage** (intros, transitions, redites) : la complétion bat la durée — 45 s complétée à 70 % surperforme 15 s complétée à 40 %.
4. **Durées cibles par plateforme** : TikTok 60-180 s (substance) / Reels 15-30 s (portée) ou 60-90 s (storytelling) / Shorts 25-40 s / LinkedIn < 60-90 s vertical 9:16 ou 4:5, upload natif uniquement.
5. **Une déclinaison par plateforme, jamais de repost brut** (watermark TikTok sur Reels = sous-distribution) — adapter au minimum hook, sous-titres, ratio, son.
6. **Rendu « créateur », pas corporate** en organique : smartphone, face caméra, imperfections assumées ; tout contenu promotionnel TikTok exige le label contenu commercial natif activé.

## Ce que cette skill ne fait pas

- ❌ Publier (→ validation humaine, publication via le module social)
- ❌ Le sous-titrage (→ skill `captions`)
- ❌ Les visuels fixes (→ `image-generation`)
