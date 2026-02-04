---
name: note-manager
description: Gestionnaire de notes Google Keep pour rechercher, créer, modifier, archiver, épingler et dupliquer des notes. Permet de gérer des notes texte et des listes avec tri automatique des notes épinglées en premier.
---

# Note Manager

Skill de gestion des notes Google Keep en français.

## Objectif

Permettre une gestion complète des notes Google Keep :
- Rechercher des notes (avec notes épinglées en priorité)
- Créer des notes texte ou listes
- Modifier des notes existantes
- Archiver/désarchiver des notes
- Épingler/désépingler des notes
- Supprimer des notes
- Dupliquer des notes avec un nouveau nom

## Quand utiliser cette skill

Utiliser cette skill quand l'utilisateur demande :
- "Cherche mes notes Keep sur [sujet]"
- "Crée une note avec [contenu]"
- "Modifie la note [titre]"
- "Archive cette note"
- "Épingle cette note"
- "Duplique cette note"
- Toute demande de gestion de notes Google Keep

## Configuration initiale

### Première utilisation

⚠️ **Important :** Google Keep n'a pas d'API officielle publique. Cette skill utilise `gkeepapi` (bibliothèque non officielle) qui nécessite un **master token** Google.

**Authentification via OAuth2 Token :**

L'authentification se fait en 2 étapes :
1. Obtenir un **OAuth2 token** depuis votre navigateur
2. Échanger ce token contre un **master token** (valable indéfiniment)

**Instructions complètes :** Voir `scripts/README.md` pour les étapes détaillées avec le script de génération du master token.

**Résumé rapide :**
1. Allez sur : https://accounts.google.com/EmbeddedSetup
2. Connectez-vous avec votre compte Google
3. Ouvrez Developer Tools (F12) > Application > Cookies > `accounts.google.com`
4. Copiez la valeur du cookie `oauth_token` (commence par `oauth2_4/`)
5. Utilisez le script dans `scripts/README.md` pour générer le master token
6. Le master token sera sauvegardé dans `~/.claude/credentials/gkeep_credentials.json`

**Référence :** https://github.com/rukins/gpsoauth-java#receiving-an-authentication-token

## Opérations disponibles

### 🔍 Rechercher des notes

#### Recherche simple (liste)
```bash
cd ~/.claude/skills/note-manager/scripts
./run.sh search_notes --query "mot clé"
```

**Résultat :** Affiche les notes avec :
- 📌 pour les notes épinglées (toujours en premier)
- [ARCHIVED] pour les notes archivées
- Aperçu du contenu (100 premiers caractères)

#### Recherche détaillée (JSON complet)
```bash
./run.sh search_notes --query "mot clé" --full
```

**Inclut :** ID, titre, texte, statut épinglé/archivé, couleur, labels, dates, items de liste

#### Options de recherche
```bash
# Rechercher dans toutes les notes (sans filtre)
./run.sh search_notes

# Inclure les notes archivées
./run.sh search_notes --include-archived

# Inclure les notes dans la corbeille
./run.sh search_notes --include-trashed

# Limiter le nombre de résultats
./run.sh search_notes --query "réunion" --max-results 10
```

**Tri automatique :** Les notes épinglées apparaissent TOUJOURS en premier, suivies des notes par date de modification.

### 📝 Créer des notes

#### Créer une note texte
```bash
./run.sh manage_notes --action create-text --title "Titre de la note" --text "Contenu de la note"
```

#### Créer une note texte épinglée
```bash
./run.sh manage_notes --action create-text --title "Note importante" --text "Contenu" --pinned
```

#### Créer une note avec couleur
```bash
./run.sh manage_notes --action create-text --title "Note rouge" --text "Contenu" --color red
```

**Couleurs disponibles :** red, blue, green, yellow, gray, white, pink, orange, teal, brown

#### Créer une liste
```bash
./run.sh manage_notes --action create-list --title "Ma liste" --items '[
  {"text": "Item 1", "checked": false},
  {"text": "Item 2", "checked": true},
  {"text": "Item 3", "checked": false}
]'
```

#### Créer une liste simple (non cochée)
```bash
./run.sh manage_notes --action create-list --title "Courses" --items '["Lait", "Pain", "Œufs"]'
```

### 📖 Récupérer une note

#### Obtenir les détails complets d'une note
```bash
./run.sh manage_notes --action get --note-id "NOTE_ID"
```

**Résultat :** JSON avec toutes les informations (titre, texte, items si liste, couleur, dates, etc.)

### ✏️ Modifier des notes

#### Modifier le titre d'une note
```bash
./run.sh manage_notes --action update --note-id "NOTE_ID" --title "Nouveau titre"
```

#### Modifier le contenu d'une note texte
```bash
./run.sh manage_notes --action update --note-id "NOTE_ID" --text "Nouveau contenu"
```

#### Modifier les items d'une liste
```bash
./run.sh manage_notes --action update --note-id "NOTE_ID" --items '[
  {"text": "Nouveau item 1", "checked": true},
  {"text": "Nouveau item 2", "checked": false}
]'
```

**⚠️ Important :** La modification des items remplace TOUS les items existants.

### 📌 Épingler/Désépingler

#### Épingler une note
```bash
./run.sh manage_notes --action pin --note-id "NOTE_ID"
```

#### Désépingler une note
```bash
./run.sh manage_notes --action unpin --note-id "NOTE_ID"
```

### 📦 Archiver/Désarchiver

#### Archiver une note
```bash
./run.sh manage_notes --action archive --note-id "NOTE_ID"
```

#### Désarchiver une note
```bash
./run.sh manage_notes --action unarchive --note-id "NOTE_ID"
```

### 🗑️ Supprimer

#### Mettre une note à la corbeille
```bash
./run.sh manage_notes --action delete --note-id "NOTE_ID"
```

**Note :** Les notes supprimées vont dans la corbeille Google Keep (récupérables pendant 7 jours).

### 📋 Dupliquer

#### Dupliquer une note avec nouveau titre
```bash
./run.sh manage_notes --action duplicate --note-id "NOTE_ID" --new-title "Copie - Nouveau nom"
```

#### Dupliquer avec titre automatique
```bash
./run.sh manage_notes --action duplicate --note-id "NOTE_ID"
```

**Résultat :** Crée "Copy of [titre original]" avec le même contenu, couleur et labels.

## Workflow typique

### Exemple : Chercher et modifier une note

```bash
cd ~/.claude/skills/note-manager/scripts

# 1. Chercher la note
./run.sh search_notes --query "réunion"

# Résultat :
# 1. 📌 Réunion équipe 2025
#    ID: abc123xyz
#    Notes de la réunion hebdomadaire...

# 2. Récupérer les détails
./run.sh manage_notes --action get --note-id "abc123xyz"

# 3. Modifier le titre
./run.sh manage_notes --action update --note-id "abc123xyz" --title "Réunion équipe - 10 Nov 2025"

# 4. Épingler pour retrouver facilement
./run.sh manage_notes --action pin --note-id "abc123xyz"
```

### Exemple : Créer une liste de courses et la gérer

```bash
# 1. Créer la liste
./run.sh manage_notes --action create-list \
  --title "Courses semaine" \
  --items '["Lait", "Pain", "Fromage", "Tomates"]' \
  --pinned

# Résultat : ✓ List note created: Courses semaine
#            ID: xyz789abc
#            Items: 4

# 2. Mettre à jour (cocher des items)
./run.sh manage_notes --action update --note-id "xyz789abc" --items '[
  {"text": "Lait", "checked": true},
  {"text": "Pain", "checked": true},
  {"text": "Fromage", "checked": false},
  {"text": "Tomates", "checked": false}
]'

# 3. Dupliquer pour la semaine prochaine
./run.sh manage_notes --action duplicate --note-id "xyz789abc" --new-title "Courses semaine prochaine"

# 4. Archiver l'ancienne liste
./run.sh manage_notes --action archive --note-id "xyz789abc"
```

### Exemple : Créer un pense-bête de voyage

```bash
# Quand l'utilisateur dit : "Créer une note voyage pour l'Inde"

# 1. Dupliquer le template de voyage
./run.sh manage_notes --action duplicate \
  --note-id "1683e96bc1c.b2b65bc687febb09" \
  --new-title "Pense bête - Voyage Inde"

# Résultat : ✓ Note duplicated: Pense bête - Voyage Inde
#            New note ID: abc123xyz

# 2. Épingler la nouvelle note
./run.sh manage_notes --action pin --note-id "abc123xyz"

# 3. Fournir l'URL à l'utilisateur
echo "✓ Note créée et épinglée"
echo "🔗 Ouvrir : https://keep.google.com/u/0/#NOTE/abc123xyz"
```

**Résultat :** Une copie complète du pense-bête voyage (tous les items à cocher) prête à être utilisée pour le voyage spécifique.

## Notes importantes et spécifiques

**Ce gestionnaire de notes inclut des notes spécifiques pour :**

📋 **Gestion de voyages :**
- **Pense-bête voyage** - Template duplicable pour créer une liste d'affaires à emporter pour chaque voyage
- **Passeports & Info** - Informations centralisées des passeports famille pour enregistrements rapides

🔍 **Comment les utiliser :**
- Rechercher : `./run.sh search_notes --query "Voyages"`
- Consulter passeports : Ouvrir directement https://keep.google.com/u/0/#NOTE/18cbf5a516e.8f52bba149ee57fc
- Créer pense-bête voyage : Dupliquer le template, épingler, et ouvrir l'URL (voir exemple ci-dessus)

Cette section liste les notes Google Keep importantes qui doivent être connues et accessibles rapidement.

### Notes configurées

- **Buffer** (ID: `1733387285569.619963495`)
  - Type : Note texte
  - Statut : Épinglée (📌)
  - Description : Note buffer utilisée pour des notes temporaires rapides
  - Créée : 5 décembre 2024
  - Dernière mise à jour : 21 octobre 2025
  - Couleur : Blanche
  - **Commandes spéciales disponibles** (voir section "Commandes Buffer" ci-dessous)
  - 🔗 **URL Web :** https://keep.google.com/u/0/#NOTE/1733387285569.619963495

- **TODO** (ID: `172ed7a8e25.8c8374346cc64685`)
  - Type : Note liste avec hiérarchie
  - Statut : Épinglée (📌)
  - Description : Liste de tâches principale avec sous-éléments hiérarchiques
  - **⚠️ PROTÉGÉE - NE PAS MODIFIER VIA SCRIPT**
  - **Raison :** Les notes de type "liste" dans Google Keep ne préservent PAS la hiérarchie/indentation lors de modifications via l'API. Toute modification via script aplatira la structure et mélangera les éléments.
  - **Action recommandée :** Pour toute modification, ouvrir directement dans Google Keep Web
  - 🔗 **URL Web :** https://keep.google.com/u/0/#NOTE/172ed7a8e25.8c8374346cc64685
  - **Lecture seule OK :** Vous pouvez lire la note via `--action get` pour consulter les items, mais NE PAS utiliser `--action update`

- **Pense bête Voyages** (ID: `1683e96bc1c.b2b65bc687febb09`)
  - Type : Note liste (template)
  - Statut : NON épinglée (c'est un modèle)
  - Description : Liste complète de choses à prendre pour un voyage (vêtements, accessoires, documents, etc.)
  - **Usage spécial - Template de voyage :**
    - Quand l'utilisateur dit : "Créer une note voyage pour [destination]" ou "Pense-bête pour le voyage [destination]"
    - **Actions à effectuer :**
      1. Dupliquer cette note : `--action duplicate --note-id "1683e96bc1c.b2b65bc687febb09" --new-title "Pense bête - Voyage [destination]"`
      2. Récupérer l'ID de la nouvelle note dupliquée
      3. Épingler la nouvelle note : `--action pin --note-id "NEW_NOTE_ID"`
      4. Fournir l'URL à l'utilisateur : `https://keep.google.com/u/0/#NOTE/NEW_NOTE_ID`
  - 🔗 **URL Web (template original) :** https://keep.google.com/u/0/#NOTE/1683e96bc1c.b2b65bc687febb09
  - **Ne pas modifier le template original** - Toujours dupliquer pour créer une nouvelle liste de voyage

- **Voyages Passeports & Info** (ID: `18cbf5a516e.8f52bba149ee57fc`)
  - Type : Note texte
  - Statut : Épinglée (📌)
  - Description : Informations des passeports de la famille pour enregistrements rapides lors de voyages
  - **Format standardisé pour chaque passeport :**
    ```
    --- Passeport [INITIALES]
    Nom: [Prénom NOM]
    Num: [Numéro passeport]
    Date naissance: [JJ/MM/AAAA]
    Lieu de naissance: [Ville, Pays]
    Date délivrance: [JJ/MM/AAAA]
    Date expiration: [JJ/MM/AAAA]
    Compte Flying Blue: [Numéro] (optionnel)
    ```
  - **Initiales :** 1ère lettre du prénom + 2 premières lettres du nom (ex: Sébastien MORAND = SMO)
  - **Contenu actuel :** SMO (Sébastien MORAND), LCH (Lamya CHRIF)
  - 🔗 **URL Web :** https://keep.google.com/u/0/#NOTE/18cbf5a516e.8f52bba149ee57fc
  - **Modification OK** - Note texte, pas de problème de hiérarchie

### Ajouter d'autres notes

**Format suggéré :**
```
- **[Titre de la note]** (ID: `NOTE_ID`)
  - Type : Note texte / Note liste
  - Description : Usage de cette note
  - Accès rapide : Épinglée / Archivée / etc.
  - 🔗 **URL Web :** https://keep.google.com/u/0/#NOTE/NOTE_ID
  - **Protection :** Si applicable, marquer comme PROTÉGÉE avec raison
```

## Commandes Buffer / Buffer Commands

La note **Buffer** (`1733387285569.619963495`) est une note spéciale pour des notes temporaires rapides. Des commandes spécifiques sont disponibles.

The **Buffer** note (`1733387285569.619963495`) is a special note for quick temporary notes. Specific commands are available.

### 🇫🇷 Commandes en français

L'utilisateur peut utiliser ces formulations naturelles :

#### Ajouter du contenu au buffer
```
Utilisateur: "Dans la note buffer ajoute ceci : [contenu]"
Utilisateur: "Ajoute dans le buffer : [contenu]"
Utilisateur: "Mets ça dans le buffer : [contenu]"
```

**Action :** Ajouter le contenu à la note Buffer (ajout, pas remplacement).

**Implémentation :**
```bash
# 1. Récupérer le contenu actuel
./run.sh manage_notes --action get --note-id "1733387285569.619963495"

# 2. Ajouter le nouveau contenu
# Si la note est vide : utiliser le nouveau contenu
# Si la note a du contenu : ajouter une ligne vide puis le nouveau contenu

./run.sh manage_notes --action update --note-id "1733387285569.619963495" --text "[contenu existant]\n\n[nouveau contenu]"
```

#### Vider le buffer
```
Utilisateur: "Vide la note buffer"
Utilisateur: "Efface le buffer"
Utilisateur: "Clear le buffer"
```

**Action :** Supprimer tout le contenu de la note Buffer.

**Implémentation :**
```bash
./run.sh manage_notes --action update --note-id "1733387285569.619963495" --text ""
```

#### Copier le buffer
```
Utilisateur: "Copie la note buffer"
Utilisateur: "Copy le buffer"
Utilisateur: "Mets le buffer dans le clipboard"
```

**Action :** Copier le contenu de la note Buffer dans le clipboard système (avec `pbcopy`).

**Implémentation :**
```bash
# 1. Récupérer le contenu
CONTENT=$(./run.sh manage_notes --action get --note-id "1733387285569.619963495" | jq -r '.text')

# 2. Copier dans le clipboard
echo "$CONTENT" | pbcopy

# 3. Confirmer à l'utilisateur
echo "✓ Contenu du buffer copié dans le clipboard"
```

### 🇬🇧 English Commands

Users can use these natural formulations:

#### Add content to buffer
```
User: "In the buffer note add this: [content]"
User: "Add to the buffer: [content]"
User: "Put this in the buffer: [content]"
```

**Action:** Add content to the Buffer note (append, not replace).

**Implementation:**
```bash
# 1. Get current content
./run.sh manage_notes --action get --note-id "1733387285569.619963495"

# 2. Add new content
# If note is empty: use new content
# If note has content: add blank line then new content

./run.sh manage_notes --action update --note-id "1733387285569.619963495" --text "[existing content]\n\n[new content]"
```

#### Clear the buffer
```
User: "Clear the buffer note"
User: "Empty the buffer"
User: "Erase the buffer"
```

**Action:** Delete all content from the Buffer note.

**Implementation:**
```bash
./run.sh manage_notes --action update --note-id "1733387285569.619963495" --text ""
```

#### Copy the buffer
```
User: "Copy the buffer note"
User: "Copy buffer"
User: "Put buffer in clipboard"
```

**Action:** Copy the Buffer note content to the system clipboard (using `pbcopy`).

**Implementation:**
```bash
# 1. Get content
CONTENT=$(./run.sh manage_notes --action get --note-id "1733387285569.619963495" | jq -r '.text')

# 2. Copy to clipboard
echo "$CONTENT" | pbcopy

# 3. Confirm to user
echo "✓ Buffer content copied to clipboard"
```

### 💡 Exemples d'utilisation / Usage Examples

#### Exemple 1 : Ajouter une note rapide
```
🇫🇷 Utilisateur: "Dans le buffer ajoute : Appeler Marie demain à 14h"
Assistant: [Ajoute le texte au buffer]
✓ Ajouté au buffer
```

#### Exemple 2 : Vider après utilisation
```
🇫🇷 Utilisateur: "Vide le buffer"
Assistant: [Vide la note]
✓ Buffer vidé
```

#### Exemple 3 : Copier pour utiliser ailleurs
```
🇬🇧 User: "Copy the buffer"
Assistant: [Copies content to clipboard]
✓ Buffer content copied to clipboard
```

#### Exemple 4 : Workflow complet
```
🇫🇷 Utilisateur: "Ajoute dans le buffer : Idée pour le projet X"
Assistant: ✓ Ajouté au buffer

[Plus tard...]
Utilisateur: "Copie le buffer"
Assistant: ✓ Contenu du buffer copié dans le clipboard

Utilisateur: "Vide le buffer"
Assistant: ✓ Buffer vidé
```

### ⚠️ Important Notes

**🇫🇷 Pour Claude :**
- **TOUJOURS utiliser l'ID exact** : `1733387285569.619963495`
- **Ajouter = append**, ne pas remplacer le contenu existant
- **Vider = mettre le text à ""**, pas supprimer la note
- **Copier = utiliser `pbcopy`** pour le clipboard système
- **Confirmer chaque action** avec un message clair à l'utilisateur

**🇬🇧 For Claude:**
- **ALWAYS use the exact ID**: `1733387285569.619963495`
- **Add = append**, don't replace existing content
- **Clear = set text to ""**, don't delete the note
- **Copy = use `pbcopy`** for system clipboard
- **Confirm each action** with a clear message to the user

## Références

- [gkeepapi Documentation](https://gkeepapi.readthedocs.io/) - API Python pour Google Keep
- Scripts dans `scripts/src/` :
  - `auth.py` - Authentification Google Keep
  - `search_notes.py` - Recherche de notes
  - `manage_notes.py` - CRUD des notes

## Limitations

- Google Keep n'a pas d'API officielle, cette skill utilise `gkeepapi` (API non officielle)
- Seuls les formats **texte** et **liste** sont supportés
- Les images, dessins et enregistrements audio ne sont pas gérés
- La synchronisation peut prendre quelques secondes
- **⚠️ LIMITATION MAJEURE - Hiérarchie dans les listes :**
  - Les notes de type "liste" **NE PRÉSERVENT PAS** la hiérarchie/indentation lors de modifications via l'API
  - Toute modification via `--action update` sur une note liste **aplatira la structure** et mélangera les éléments
  - **Solution :** Pour les notes avec hiérarchie complexe, les marquer comme PROTÉGÉES et les modifier uniquement via l'interface Web Google Keep
  - Les URLs Google Keep Web suivent le format : `https://keep.google.com/u/0/#NOTE/{note_id}`
