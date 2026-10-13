---
name: video-matting
description: Détourage vidéo local pour {{COMPANY_NAME}} — isole une personne d'une vidéo et produit un calque alpha exploitable au montage (remplacement de décor, incrustation sur fond généré). S'appuie sur RobustVideoMatting en local (ONNX, gratuit, privé). À utiliser pour remplacer un décor, incruster un sujet sur un fond de marque, ou isoler un premier plan. L'incrustation et la lumière relèvent de `video-editing`.
---

# video-matting — détourer une vidéo en local

**Gratuit et privé** : tout tourne en local (ONNX Runtime, pas de PyTorch requis, accélération CoreML sur Apple Silicon).

## Le principe qui décide de tout

Un détourage « se voit » quand le masque est **binaire** (bord franc) ou **instable** (contour qui frémit d'une image à l'autre). RobustVideoMatting règle les deux : alpha **continu** (vraies demi-transparences dans les cheveux) et **état récurrent** propagé d'une image à l'autre — mesuré plusieurs fois plus stable que les segmentations image-par-image des frameworks systèmes.

## Méthode

Poids publics : `rvm_resnet50_fp32.onnx` (~100 Mo) ou `rvm_mobilenetv3_fp32.onnx` (~14 Mo), dépôt officiel PeterL1n/RobustVideoMatting.

1. **Prendre `resnet50`** : meilleur détail capillaire, moins d'artefacts (et souvent plus rapide via CoreML, meilleure couverture d'opérateurs).
2. `downsample_ratio` : viser ~512 px sur le petit côté réduit (0,5 pour une source verticale ~576×1024 ; 0,25 pour de la 4K).
3. Composer **`fgr` + `pha`** (les deux sorties du modèle), pas `source × alpha` : le premier plan rendu est décontaminé du spill du décor.
4. Les 4 états récurrents s'initialisent à zéro et se repassent tels quels d'une frame à l'autre.

## ⚠️ RVM ne segmente QUE les personnes

Ni le bureau, ni le micro, ni les objets tenus. Deux compléments, légitimes tant que **la caméra est fixe** :

- **Meuble/bureau** : bande pleine en bas de cadre avec un dégradé vertical (~50 px) pour que la jonction ne se lise pas.
- **Objets tenus** : seuillage de luminance dans une **bande centrale** (sur toute la largeur, le seuillage ramasse le décor).

**Piège de lecture** : sur le masque seul, une manche ressemble à un meuble. **Toujours contrôler en compositant sur un fond uni**, jamais sur le masque brut.

## Contrôle qualité — systématique

Extraire l'alpha (`alphaextract`) et suivre sa moyenne par frame (`signalstats`) : chercher les décrochages (masque quasi vide → clignotement), les sauts brusques, le jitter. Normaliser selon la profondeur de pixel (12 bits = échelle 0-4095). Si un frémissement se voit : lissage temporel `tmix` sur 3 images.

## Export

- **ProRes 4444 avec `-alpha_bits 8`** (≈ 1 Go/min en 1080×1920). `-alpha_bits 16` décuple le débit pour rien.
- ⚠️ Certains encodeurs matériels **perdent silencieusement l'alpha** (sortie en `yuv420p` malgré la demande) : **vérifier le `pix_fmt` du fichier de sortie**.
- Garder la **résolution native** : tout upscale est de l'invention de détail — le faire une seule fois, au plus tard dans la chaîne.

## ⚠️ La leçon la plus chère : régénérer plutôt que rattraper une source molle

Quand la source est en basse définition et que le montage la recadre fortement (zooms ×2-3), le calque détouré restera **mou face à des plans générés en HD** — et aucun rattrapage (matte pleine résolution, débruitage, upscale IA) ne comblera l'écart de définition. **Vérifier la définition effective de la source avant de bâtir une architecture sur son détourage.** Le détourage garde son sens entre sources de définition équivalente ; sinon, régénérer le plan entier (→ `video-generation`) est la voie qui tient.

Autre échec documenté : un compositing sujet/fond sans **light wrap** « se voit » toujours. L'incrustation et la lumière (halo, vignette, grain commun) se règlent au montage (→ `video-editing`) : dans une composition HyperFrames, où le calque détouré se pose comme une vidéo à canal alpha au-dessus du fond et où vignette et grain vont sur un calque commun (skills `hyperframes:hyperframes-core` et `hyperframes:hyperframes-media`), ou par des filtres ffmpeg dans le plan de montage (voie B). Jamais une simple superposition du calque sur le fond. Pour une composition HyperFrames, le calque se livre en WebM VP9 avec alpha, le format que Chrome lit en transparence ; le ProRes 4444 sert aux échanges et à ffmpeg.

## Ce que cette skill ne fait pas

- ❌ Incruster le fond et régler la lumière (→ `video-editing` : glow, vignette, grain commun, étalonnage)
- ❌ Générer le fond (→ `image-generation`)
- ❌ Le chroma key sur fond vert : un fond uni se découpe au montage, par le filtre ffmpeg `chromakey` dans le plan de montage de `video-editing` (voie B), sans modèle de détourage. La documentation d'HyperFrames ne propose pas de keyer : sa commande `remove-background` (skill `hyperframes:hyperframes-media`) détoure une personne, comme cette skill
