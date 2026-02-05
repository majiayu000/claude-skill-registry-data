---
name: julien-ref-ahk-v2
description: Best practices AutoHotkey v2. Use when writing AHK v2 scripts - covers global variable declarations, SetTimer usage, event handlers, and GUI positioning.
triggers:
  - raccourci clavier windows
  - automatiser une tâche windows
  - mon script ahk ne marche pas
  - aide pour mon script ahk
  - help with my ahk script
  - create a hotkey
  - autohotkey v2
  - ahk v2
  - ahk2
  - autohotkey tutorial
---

# AutoHotkey v2 - Best Practices pour LLM

## RÈGLE CRITIQUE - VARIABLES GLOBALES

## Observability

**First**: At the start of execution, display:
```
🔧 Skill "julien-ref-ahk-v2" activated
```

### DÉCLARATION OBLIGATOIRE DANS CHAQUE FONCTION
```autohotkey
; INCORRECT - Cause erreur "variable not assigned"
SomeFunction() {
    g_MyGlobalVar := "value"  ; ERREUR!
}

; CORRECT - Déclaration explicite requise
SomeFunction() {
    global g_MyGlobalVar      ; OBLIGATOIRE
    g_MyGlobalVar := "value"  ; OK
}
```

### LISTE COMPLÈTE DES VARIABLES À DÉCLARER
```autohotkey
FunctionUsingGlobals() {
    ; Déclarer TOUTES les variables globales utilisées
    global g_AppVersion, g_IsInitialized, g_ConfigFile
    global g_CachedPhrases, g_SavedSelections, g_CurrentProject

    ; Maintenant on peut les utiliser
    g_IsInitialized := true
    return g_AppVersion
}
```

## STRUCTURE MODULAIRE AUTOHOTKEY V2

### En-tête Standard
```autohotkey
; Module.ahv2 - Description du module
; Encodage : UTF-8 avec BOM
; AutoHotkey v2

; Variables globales du module (si nécessaire)
global g_ModuleVar := ""
```

### Ordre d'Inclusion Critique
```autohotkey
; 1. Configuration TOUJOURS EN PREMIER
#Include "Config\Settings.ah2"
#Include "Config\Paths.ah2"

; 2. Modules Core
#Include "Core\Logger.ah2"
#Include "Core\FileManager.ah2"

; 3. Modules Features (qui dépendent de Core)
#Include "Features\PhraseManager.ah2"

; 4. GUI en dernier
#Include "GUI\MainInterface.ah2"
```

## TIMERS ET ÉVÉNEMENTS - NOUVELLES ERREURS CRITIQUES

### SetTimer vs Timer() - ERREUR CRITIQUE
```autohotkey
; INCORRECT - Timer() n'existe pas en AHK v2
g_TooltipTimer := Timer(GUI_TooltipCheckMouse, 100)
g_TooltipTimer.Start()

; CORRECT - Utiliser SetTimer
SetTimer(GUI_TooltipCheckMouse, 100)

; CORRECT - Arrêter timer
SetTimer(GUI_TooltipCheckMouse, 0)  ; 0 = arrêter

; CORRECT - Timer périodique avec variable de contrôle
g_TimerActive := true
SetTimer(MyFunction, 100)

StopMyTimer() {
    global g_TimerActive
    g_TimerActive := false
    SetTimer(MyFunction, 0)
}
```

### Event Handlers GUI - Signatures Correctes
```autohotkey
; INCORRECT - Signature trop spécifique peut échouer
GUI_HandleResize(GuiObj, MinMax, Width, Height) {
    ; Cette signature peut ne pas correspondre à l'événement réel
}

; CORRECT - Signature flexible avec paramètres variables
GUI_HandleResize(*) {
    ; Récupérer dimensions via la GUI elle-même
    global g_MainGui
    g_MainGui.GetPos(, , &Width, &Height)
    ; ... traitement
}

; CORRECT - Event handlers standards
g_MainGui.OnEvent("Close", (*) => GUI_Hide())
g_MainGui.OnEvent("Size", GUI_HandleResize)  ; Fonction sans parenthèses
g_MainGui.OnEvent("Escape", (*) => GUI_Hide())
```

### ListView Event Handlers
```autohotkey
; CORRECT - Signatures standard ListView
ListView_OnItemCheck(ListViewObj, Item, Checked) {
    ; Item = numéro ligne, Checked = true/false
}

ListView_OnItemFocus(ListViewObj, Item) {
    ; Item = numéro ligne qui a le focus
}

; CORRECT - Assignment
g_ListView.OnEvent("ItemCheck", ListView_OnItemCheck)
g_ListView.OnEvent("ItemFocus", ListView_OnItemFocus)
```

## INTERFACE UTILISATEUR - POSITIONNEMENT CRITIQUE

### Calculs de Positionnement d'Interface
```autohotkey
; PROBLÈME COURANT - Interface mal dimensionnée
CreateGUI() {
    ; Boutons positionnés trop bas, pas visibles
    g_Button1 := g_Gui.Add("Button", "x10 y450 w80 h30", "OK")
    g_ListView := g_Gui.Add("ListView", "x10 y70 w620 h400", cols)
    ; Total height = 70 + 400 + 30 = 500px mais fenêtre fait 480px
}

; SOLUTION - Calculs cohérents
CreateGUI() {
    ; Définir dimensions fenêtre d'abord
    windowHeight := 450
    headerHeight := 70
    footerHeight := 80  ; boutons + marge

    ; ListView adaptatif
    listViewHeight := windowHeight - headerHeight - footerHeight
    g_ListView := g_Gui.Add("ListView", "x10 y" . headerHeight . " w620 h" . listViewHeight, cols)

    ; Boutons dans footer calculé
    buttonY := headerHeight + listViewHeight + 10
    g_Button1 := g_Gui.Add("Button", "x10 y" . buttonY . " w80 h30", "OK")
}
```

## GESTION DONNÉES STRUCTURÉES ET NUMÉROTATION

### Objets avec Propriétés Multiples
```autohotkey
; STRUCTURE ENRICHIE POUR CACHE
Cache_LoadData() {
    global g_CachedPhrases

    currentTitleNumber := 0
    currentPhraseNumber := 0

    ; Créer objets avec métadonnées complètes
    for lineNum, currentLine in lines {
        if (InStr(currentLine, ";;#") = 1) {
            currentTitleNumber++
            currentPhraseNumber := 0
            titleText := Trim(SubStr(currentLine, 4))

            g_CachedPhrases.Push({
                Type: "Title",
                Text: "[" . currentTitleNumber . "] === " . titleText . " ===",
                OriginalText: titleText,
                TitleNumber: currentTitleNumber
            })
        } else {
            currentPhraseNumber++
            g_CachedPhrases.Push({
                Type: "Phrase",
                Text: "[" . currentTitleNumber . "." . currentPhraseNumber . "] " . currentLine,
                OriginalText: currentLine,
                TitleNumber: currentTitleNumber,
                PhraseNumber: currentPhraseNumber
            })
        }
    }
}
```

### Accès Propriétés Sécurisé
```autohotkey
GUI_ProcessPhrases() {
    global g_CachedPhrases

    for phraseObj in g_CachedPhrases {
        ; Vérification existence propriété
        originalText := phraseObj.HasProp("OriginalText") ? phraseObj.OriginalText : phraseObj.Text

        ; Traitement conditionnel par type
        if (phraseObj.Type = "Title") {
            ; Traitement spécial titres
        } else if (phraseObj.Type = "Phrase") {
            ; Traitement phrases normales
        }
    }
}
```

## ERREURS CRITIQUES À ÉVITER

1. **Variables globales sans déclaration** - Cause systématiquement des erreurs
2. **Timer() au lieu de SetTimer** - Timer() n'existe pas en AutoHotkey v2
3. **Event handlers avec signatures incorrectes** - Utiliser (*) pour flexibilité
4. **Calculs interface incohérents** - Boutons hors limites fenêtre
5. **Chemins relatifs incorrects** dans les tests
6. **Ordre d'inclusion** - Settings.ah2 TOUJOURS en premier
7. **Initialisation dans le désordre** - Logger avant Cache
8. **Variables non initialisées** - Toujours initialiser avant usage

## CONVENTIONS DE NOMMAGE

```autohotkey
; Variables globales
global g_AppVersion := "1.0.0"
global g_IsInitialized := false
global g_ConfigFile := ""

; Fonctions - Module_Action
Logger_Write()
Cache_Initialize()
PhraseManager_LoadData()

; Constantes en majuscules
global MAX_CACHE_SIZE := 1000
global DEFAULT_TIMEOUT := 5000
```

## CHECKLIST VALIDATION

Avant de déployer un script AutoHotkey v2 :

- [ ] Toutes les fonctions ont des déclarations `global` appropriées
- [ ] SetTimer utilisé correctement (pas Timer())
- [ ] Event handlers avec signatures flexibles (*)
- [ ] Calculs interface cohérents (boutons dans limites fenêtre)
- [ ] Ordre d'inclusion respecté (Config → Core → Features → GUI)
- [ ] Chemins relatifs corrects dans les tests (`..\..\`)
- [ ] Variables globales initialisées avant usage
- [ ] Tests de compilation passent sans erreur
- [ ] Gestion d'erreurs implémentée
- [ ] Logging configuré pour debug
