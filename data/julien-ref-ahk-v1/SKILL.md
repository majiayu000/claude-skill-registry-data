---
name: julien-ref-ahk-v1
description: Best practices AutoHotkey v1. Use when writing AHK v1 scripts to avoid critical errors like auto-execute section issues, includes order, and COM object handling.
triggers:
  - autohotkey v1
  - ahk v1
  - autohotkey script
  - ahk script
  - autohotkey best practices
  - ahk best practices
  - autohotkey gui
  - ahk hotkey
---

# AutoHotkey v1 - Guide de Référence Optimisé LLM

*Guide structuré des bonnes pratiques AutoHotkey v1 pour développeurs et assistants IA*

---

## Structure du Guide

## Observability

**First**: At the start of execution, display:
```
🔧 Skill "julien-ref-ahk-v1" activated
```

**PARTIE I - RÈGLES CRITIQUES** : Erreurs fatales à éviter absolument
**PARTIE II - STANDARDS FONDAMENTAUX** : Encodage, nommage, architecture
**PARTIE III - DÉVELOPPEMENT** : Patterns, GUI, performance
**PARTIE IV - VALIDATION** : Tests et déploiement

---

# PARTIE I - RÈGLES CRITIQUES

## Erreur #0 : Section Auto-Execute - LA RÈGLE LA PLUS CRITIQUE

### QU'EST-CE QUE L'AUTO-EXECUTE?

La section auto-execute est le code qui s'exécute **automatiquement** au démarrage du script. C'est la source #1 des bugs incompréhensibles en AutoHotkey!

### CE QUI TERMINE L'AUTO-EXECUTE

L'auto-execute se termine dès qu'AutoHotkey rencontre:
1. Un `return` explicite
2. Un `Exit`
3. **UNE FONCTION** (ligne commençant par `NomFonction() {`)
4. **UN HOTKEY/HOTSTRING** (ligne contenant `::`)
5. **UN LABEL** (ligne se terminant par `:`)
6. La fin physique du fichier

### ERREUR FATALE - Code après une fonction

```autohotkey
#SingleInstance Force
global myVar := "value"

MyFunction() {  ; CETTE FONCTION TERMINE L'AUTO-EXECUTE!
    MsgBox, Function
}

; CE CODE NE S'EXÉCUTERA JAMAIS AU DÉMARRAGE!
MsgBox, Script started  ; Jamais affiché!
Menu, Tray, Icon, icon.ico  ; Jamais chargé!
return
```

### STRUCTURE CORRECTE

```autohotkey
#SingleInstance Force
global myVar := "value"

; Code d'initialisation (s'exécute au démarrage)
MsgBox, Script started
Menu, Tray, Icon, icon.ico

; FIN EXPLICITE de l'auto-execute
return

; Fonctions (après le return)
MyFunction() {
    MsgBox, Function
}

; Hotkeys (après les fonctions)
^a::
    MyFunction()
return
```

### STRUCTURE DE FICHIER OBLIGATOIRE

```
#Directives (#SingleInstance, #Persistent, etc.)
↓
Variables globales
↓
AUTO-EXECUTE (code qui s'exécute au démarrage)
↓
return  ← FIN EXPLICITE de l'auto-execute
↓
Fonctions
↓
Labels
↓
Hotkeys/Hotstrings
↓
#Include (À LA TOUTE FIN!)
```

### PLACEMENT DES #INCLUDE - RÈGLE ABSOLUE

Les `#Include` **DOIVENT être À LA TOUTE FIN** du fichier, après:
- Toutes les fonctions
- Tous les labels
- Tous les hotkeys

**POURQUOI?** Les modules appellent souvent des fonctions du fichier principal (comme `Logger_Info`). Si l'include est placé avant la définition de ces fonctions, le script plantera!

---

## Erreur #1 : Includes Manquants ou Incorrects

### SOLUTION OBLIGATOIRE
```autohotkey
#Include %A_ScriptDir%\VA.ahk      ; Chemin absolu TOUJOURS
```

### RÈGLE ABSOLUE
- Tous les includes doivent utiliser `%A_ScriptDir%\` pour les chemins absolus

---

## Erreur #2 : Syntaxe Variables dans %var%

### SYNTAXE INVALIDE
```autohotkey
MsgBox, Device: %devices[1].name%     ; ERREUR FATALE
```

### SOLUTION OBLIGATOIRE
```autohotkey
deviceName := devices[1].name         ; Extraire la propriété
MsgBox, Device: %deviceName%          ; Utiliser la variable simple
```

---

## Erreur #3 : Usage Incorrect de `global`

### USAGE CORRECT
```autohotkey
MyFunction() {
    global ; En DÉBUT de fonction seulement
    ; OU global var1, var2 pour variables spécifiques
}

MyLabel:
    ; Les variables sont globales par défaut dans les labels
    ; PAS de déclaration global nécessaire
return
```

---

## Erreur #4 : Gestion Tableaux Vides

`.MaxIndex` retourne `""` (chaîne vide) pour un tableau vide, pas `0`.

### VÉRIFICATION CORRECTE
```autohotkey
ArrayCount := Array.MaxIndex
if (ArrayCount = "") {
    ArrayCount := 0         ; Conversion explicite
}
Loop % ArrayCount {
    Element := Array[A_Index]
}
```

---

# PARTIE II - STANDARDS FONDAMENTAUX

## Encodage : UTF-8 avec BOM OBLIGATOIRE

Sans UTF-8 avec BOM, les caractères accentués deviennent illisibles.

### SOLUTION UNIQUE
1. **Éditeur** : Sauvegarder en UTF-8 AVEC BOM
2. **Lecture** : `FileRead, var, *t *p65001 %file%`
3. **Écriture** : `FileAppend, content, %file%, UTF-8`

---

## Architecture de Projet

### PROJET SIMPLE (≤ 200 lignes)
```
MonScript.ahk                      # Tout en un seul fichier
```

### PROJET MODULAIRE (200-1000 lignes)
```
Projet/
├── Main.ahk                       # Point d'entrée
├── Config.ahk                     # Variables globales
├── Modules/
│   ├── Module1.ahk               # Fonctionnalités
│   └── Module2.ahk
└── logs/                         # Logs (auto-créé)
```

---

## Standards de Nommage

```autohotkey
; Fichiers et dossiers : PascalCase
MyModule.ahk, Utils/, Core/

; Variables globales : MAJUSCULES
global LOG_ENABLED := true
global EMAIL_ADDRESS := "user@domain.com"

; Fonctions : PascalCase
SendEmailGmail()
GetAudioDevicesList()

; Variables locales : camelCase
local deviceName := "Speakers"
currentTime := A_Now
```

---

# PARTIE III - DÉVELOPPEMENT

## Gestion des Objets COM (Audio/System)

### PATTERN OBLIGATOIRE
```autohotkey
FunctionWithCOM() {
    ; 1. Créer les objets
    if !(enumerator := VA_GetDeviceEnumerator()) {
        return "Erreur création enumerator"
    }

    VA_IMMDeviceEnumerator_EnumAudioEndpoints(enumerator, 0, 1, devices)

    ; 2. Traitement
    VA_IMMDeviceCollection_GetCount(devices, count)
    Loop, %count% {
        VA_IMMDeviceCollection_Item(devices, A_Index - 1, device)
        ; Traiter device...
        ObjRelease(device)    ; LIBÉRER CHAQUE OBJET
    }

    ; 3. Nettoyage OBLIGATOIRE
    ObjRelease(devices)
    ObjRelease(enumerator)
}
```

Chaque objet COM créé DOIT être libéré avec `ObjRelease()`.

---

## Interface Graphique

### SOLUTIONS SIMPLES ET ROBUSTES

#### Edit Control avec Scroll Natif
```autohotkey
Gui, Add, Edit, x10 y10 w500 h300 ReadOnly VScroll HScroll vContentArea
GuiControl,, ContentArea, %LongText%  ; Scroll automatique
```

### RÈGLES GUI ESSENTIELLES
- **Simplicité** : Privilégier les contrôles natifs (Edit, ListBox)
- **Séparation** : GUI distinctes pour différentes fonctions
- **Scroll natif** : Laisser AutoHotkey gérer le scroll
- **Boutons fixes** : Placer les boutons hors des zones scrollables

---

# PARTIE IV - VALIDATION

## Checklist Pré-Déploiement

### VALIDATION TECHNIQUE OBLIGATOIRE
- [ ] **Encodage** : UTF-8 avec BOM sur tous les fichiers .ahk
- [ ] **Includes** : Tous les chemins utilisent `%A_ScriptDir%\`
- [ ] **Tableaux** : Vérification `MaxIndex = ""` pour tableaux vides
- [ ] **COM** : Tous les objets libérés avec `ObjRelease()`
- [ ] **Global** : Utilisé uniquement en début de fonctions
- [ ] **Variables** : Pas d'accès propriétés dans `%var%`

---

## Règles d'Or à Retenir

1. **UTF-8 avec BOM** : Obligatoire pour les accents
2. **Includes absolus** : Toujours avec `%A_ScriptDir%\`
3. **Variables simples** : Dans `%var%`, pas de propriétés d'objets
4. **Global correct** : Fonctions seulement, jamais dans labels
5. **Tableaux vides** : Vérifier `MaxIndex = ""`
6. **COM cleanup** : `ObjRelease()` obligatoire
7. **Log unique** : Un seul fichier actif par session
8. **Hotkeys à la fin** : Convention et bonne pratique
9. **Auto-execute** : Toujours terminer par `return` explicite
10. **Includes en dernier** : À la fin du fichier principal
