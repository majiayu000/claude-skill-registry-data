---
name: renommer-fichiers-rencontre
description: >-
  Rename meeting transcript (.docx) and summary (.md) files to the user's naming conventions. Use
  when given a file path with "renomme ce fichier", "renomme la transcription", "renomme le
  résumé", "rename this summary", "renomme-le", "donne-lui le bon nom", or a name like "Temps
  Chantier_.docx".
---

# Renommer Fichiers de Rencontre

Ce skill lit un fichier de transcription (.docx) ou de synthèse de rencontre (.md), en extrait la date et le sujet principal, puis le renomme en suivant les conventions personnelles de l'utilisateur.

---

## Conventions de nommage

### Transcriptions (.docx)
```
Transcription_Rencontre_YYYY-MM-DD - [Sujet en Title Case].docx
```
- Date : format ISO **YYYY-MM-DD** (ex. `2026-04-15`)
- Sujet : phrase française courte en Title Case décrivant le sujet principal
- Exemples réels :
  - `Transcription_Rencontre_2026-04-15 - Révision Modèle Temps Employé, Temps Machine et Sous-traitants.docx`
  - `Transcription_Rencontre_2026-03-12 - Prototype Canvas - Karolane Gauthier.docx`
  - `Transcription_Rencontre_2026-04-14 - Validation fonctionnelle, sous-traitants et extrait excel.docx`
  - `Transcription_Rencontre_2026-02-27 - Prototype Canvas et Logique d'Affectation.docx`

### Synthèses (.md)
```
DD-MM-YYYY-synthese-[mots-cles-minuscules-sans-accents].md
```
- Date : format **DD-MM-YYYY** (ex. `15-04-2026`)
- Mots-clés : 3 à 5 mots français en minuscules séparés par des tirets, **sans accents**
- Table de conversion des accents :
  | Caractère | Remplacé par |
  |-----------|-------------|
  | é, è, ê, ë | e |
  | à, â | a |
  | ô | o |
  | û, ù | u |
  | ç | c |
  | î, ï | i |
  | œ | oe |
- Exemples réels :
  - `15-04-2026-synthese-modelisation-temps-employe-temps-machine.md`
  - `02-10-2025-synthese-rencontre-vincent-tremblay-filtrage-equipements.md`
  - `03-13-2025-synthese-karolane-gauthier-prototype-canvas.md`

---

## Workflow

### Étape 1 — Identifier le type de fichier

Regarde l'extension du chemin fourni :
- `.docx` → mode transcription
- `.md` → mode synthèse
- Autre → informer l'utilisateur et demander une clarification

### Étape 2 — Lire le contenu du fichier

**Fichiers .docx** (binaires — ne pas utiliser le tool Read) :

Extraire le texte avec Python via Bash. Remplace `PATH_ICI` par le chemin absolu entre guillemets :

```bash
python3 -c "
import zipfile, xml.etree.ElementTree as ET
with zipfile.ZipFile('PATH_ICI', 'r') as z:
    with z.open('word/document.xml') as f:
        tree = ET.parse(f)
        root = tree.getroot()
        texts = []
        for para in root.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p'):
            line = ''.join(t.text or '' for t in para.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t'))
            if line.strip():
                texts.append(line)
        print('\n'.join(texts[:60]))
"
```

Les 60 premiers paragraphes suffisent — ils contiennent toujours la date, les participants et les sujets principaux.

**Fichiers .md** : Utiliser le tool Read. Les 30 premières lignes suffisent — l'en-tête contient toujours la date et les sujets.

### Étape 3 — Extraire la date et le sujet

**Date :**
- Chercher une date explicite dans l'en-tête du fichier (ex. : "15 avril 2026", "April 15 2026", "2026-04-15", "20260415", timestamp comme "20260415_143646")
- Si introuvable dans le contenu, vérifier le nom du fichier lui-même
- Si toujours introuvable, demander à l'utilisateur

**Sujet :**
- Lire le résumé exécutif (pour les .md) ou les premiers échanges (pour les .docx)
- Identifier 2 à 4 concepts clés qui décrivent le mieux la réunion
- Pour les .docx : composer une phrase Title Case française concise (conserver noms propres et termes techniques)
- Pour les .md : extraire 3 à 5 mots-clés en minuscules, supprimer les accents, remplacer les espaces par des tirets

**Longueur du sujet :** Viser 3 à 6 mots significatifs — assez pour être descriptif, pas assez pour être verbeux.

### Étape 4 — Construire le nouveau nom de fichier

Appliquer la convention selon le type de fichier.  
Conserver le répertoire d'origine (même dossier, nouveau nom).

### Étape 5 — Renommer

```bash
mv "/chemin/ancien-nom.ext" "/chemin/nouveau-nom.ext"
```

Toujours mettre les chemins entre guillemets (gère les espaces et les accents).  
Confirmer à l'utilisateur avec le nouveau nom complet.

---

## Plusieurs fichiers à la fois

Si l'utilisateur fournit plusieurs chemins (ex. une transcription ET sa synthèse) :
- Lire les deux fichiers en parallèle
- Ils partagent la même date de réunion — croiser pour vérifier la cohérence
- Dériver le sujet du fichier le plus riche en contenu (la synthèse est généralement plus structurée)
- Appliquer la bonne convention à chaque fichier
- Renommer les deux et confirmer les deux nouveaux noms

---

## Cas limites

| Situation | Comportement |
|-----------|-------------|
| Date introuvable dans le contenu | Vérifier le nom du fichier, sinon demander à l'utilisateur |
| Sujet ambigu (réunion multi-sujets) | Retenir le sujet le plus prominent ou celui mentionné en premier |
| Fichier déjà bien nommé | Signaler que le nom respecte déjà la convention — pas de renommage |
| Fichier introuvable | Rapporter l'erreur avec le chemin fourni |
| Chemin avec espaces/accents | Toujours utiliser des guillemets dans les commandes shell |
