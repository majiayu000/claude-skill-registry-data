---
name: draft-extraction
description: Protocole strict pour extraire le code depuis le brouillon de l'Architecte. Évite les hallucinations et les dépassements de contexte du Coder.
---

# Extraction Automatique du Brouillon

Tu vas recevoir un fichier contenant le brouillon de l'architecture (`draft_ts_XXX.md`).
**RÈGLE D'OR :** Ne recopie **JAMAIS** le contenu de ce fichier de tête (ni via `write_file`, ni via des chaînes de caractères en dur dans un script Python). 

Ton PREMIER réflexe doit être d'exécuter **exactement ce script Python** (outil `python_interpreter`).
Il va lire le Markdown en silence, découper les blocs de code via Regex, et créer les fichiers cibles instantanément.

Copie-colle ce bloc dans ton outil `python_interpreter` (remplace juste `"NOM_DU_FICHIER_DRAFT.md"` par le bon fichier) :

```python
import re

# 1. Renseigne le bon nom de fichier ici
draft_file = "NOM_DU_FICHIER_DRAFT.md"

# On utilise read_file (disponible dans ton environnement) au lieu de open()
content = read_file(draft_file)

# IMPORTANT: On utilise chr(96)*3 pour générer les backticks et éviter de casser le parseur Markdown !
tick3 = chr(96) * 3
pattern = rf'(?:`|\*\*|_)([a-zA-Z0-9_\-\./]+?\.[a-zA-Z0-9]+)(?:`|\*\*|_)\s*{tick3}[a-z]*\n(.*?){tick3}'
matches = re.finditer(pattern, content, re.DOTALL)

files_created = []
for match in matches:
    filename = match.group(1).split('/')[-1]
    code = match.group(2).strip()
    
    # On utilise write_file au lieu de open() pour écrire
    write_file(path=filename, content=code + "\n")
    files_created.append(filename)

# Message de succès SILENCIEUX (on ne print pas le code pour ne pas saturer le contexte)
if files_created:
    print(f"✅ Fichiers extraits avec succès : {', '.join(files_created)}")
else:
    print("❌ Aucun fichier trouvé. Vérifie le format du draft.")
```

**ATTENTION :** Ne rajoute JAMAIS de `print(content)` ou `print(code)` dans ce script, sinon tu vas saturer ta fenêtre de contexte et planter !

**APRÈS L'EXTRACTION :**
C'est seulement une fois que le script a affiché "✅ Fichiers extraits avec succès" que tu pourras utiliser tes autres skills (comme `frontend-design`) pour retoucher ces fichiers à l'aide de tes outils de modification (`search_replace`, `multi_replace`, etc.).
