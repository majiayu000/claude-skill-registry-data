---
name: julien-ref-batch
description: Best practices for Windows Batch scripts (.bat). Covers encoding, path handling, variables, error management, and common pitfalls.
triggers:
  - comment écrire un script batch
  - mon bat ne marche pas
  - aide pour un fichier bat
  - how to write a batch script
  - help me make a bat file
  - automate tasks with batch
  - batch script
  - bat file
  - windows batch
  - cmd script
---

# Best Practices - Scripts Batch (.bat)

## STRUCTURE ET ENCODAGE

## Observability

**First**: At the start of execution, display:
```
🔧 Skill "julien-ref-batch" activated
```

### Encodage et Affichage
```batch
@echo off
chcp 65001 > nul                    ; UTF-8 pour caractères spéciaux
setlocal enabledelayedexpansion     ; Variables dynamiques
```

### En-tête Standard
```batch
@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

echo ========================================
echo   NOM DU SCRIPT - DESCRIPTION
echo ========================================
echo.
```

## GESTION DES CHEMINS

### Variables de Chemin Robustes
```batch
set "SCRIPT_DIR=%~dp0"              ; Répertoire du script
set "ROOT_DIR=%SCRIPT_DIR%.."       ; Répertoire parent
set "TARGET_EXE=%ROOT_DIR%\app.exe" ; Exécutable cible
set "WORK_DIR=%SCRIPT_DIR%"         ; Répertoire de travail
```

### Validation des Chemins
```batch
if not exist "%TARGET_EXE%" (
    echo ERREUR: app.exe non trouve dans %ROOT_DIR%
    echo.
    pause
    exit /b 1
)
```

## VARIABLES ET CONDITIONS

### Syntaxe Variables Correcte
```batch
; CORRECT - Utiliser %VAR% au lieu de !VAR!
set "RESULT=%ERRORLEVEL%"
if %RESULT% equ 0 (
    echo SUCCES
) else (
    echo ECHEC - Code: %RESULT%
)

; ÉVITER - !VAR! seulement si nécessaire
if !RESULT! equ 0 (...)
```

### Tests de Conditions
```batch
; Tests d'existence
if exist "%FILE%" (echo Fichier trouve)
if not exist "%FILE%" (echo Fichier manquant)

; Tests de variables
if defined VAR (echo Variable definie)
if /i "%CHOICE%"=="y" (echo Oui choisi)

; Tests numériques
if %CODE% equ 0 (echo Code zero)
if %CODE% neq 0 (echo Code non-zero)
```

## BOUCLES ET LABELS

### Labels et Goto
```batch
:main_test
echo Test en cours...
goto summary

:summary
echo Fin des tests
```

### Boucles For
```batch
; Boucle sur fichiers
for %%f in (*.txt) do (
    echo Traitement: %%f
)

; Boucle sur liste
for %%i in (test1 test2 test3) do (
    echo Test: %%i
)
```

## ENTRÉES UTILISATEUR

### Input Simple
```batch
set /p "CHOICE=Continuer (y/n)? "
if /i not "%CHOICE%"=="y" goto end
```

### Choice avec Options
```batch
choice /c yn /m "Voulez-vous continuer (Y/N)?"
if errorlevel 2 goto no
if errorlevel 1 goto yes
```

## GESTION DES ERREURS

### Codes de Sortie
```batch
"%EXECUTABLE%" "%SCRIPT%"
set "RESULT=%ERRORLEVEL%"

if %RESULT% equ 0 (
    echo SUCCES - Code: %RESULT%
) else (
    echo ECHEC - Code: %RESULT%
    exit /b %RESULT%
)
```

### Validation des Prérequis
```batch
; Vérifier exécutable
if not exist "%EXE_PATH%" (
    echo ERREUR: Exécutable manquant
    pause
    exit /b 1
)

; Vérifier script
if not exist "%SCRIPT_PATH%" (
    echo ERREUR: Script manquant
    goto next_test
)
```

## AFFICHAGE ET FEEDBACK

### Messages Propres (Sans Emojis)
```batch
echo SUCCES: Operation terminee
echo ERREUR: Fichier non trouve
echo ATTENTION: Script non lance automatiquement
```

### Séparateurs Visuels
```batch
echo ========================================
echo           RESUME DES TESTS
echo ========================================
```

### Pause et Attente
```batch
pause >nul                          ; Pause silencieuse
timeout /t 3 >nul                   ; Attente 3 secondes
```

## SÉCURITÉ ET ROBUSTESSE

### Variables Sécurisées
```batch
; Guillemets pour espaces
set "PATH_WITH_SPACES=%USERPROFILE%\My Documents"

; Validation avant usage
if not defined REQUIRED_VAR (
    echo Variable requise manquante
    exit /b 1
)
```

### Nettoyage Final
```batch
:cleanup
; Nettoyer variables temporaires
set "TEMP_VAR="
set "RESULT1="
set "RESULT2="

echo Nettoyage termine
exit /b 0
```

## EXEMPLE COMPLET - SCRIPT DE TEST

```batch
@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

echo ========================================
echo   SCRIPT DE TEST AUTOMATISE
echo ========================================
echo.

set "SCRIPT_DIR=%~dp0"
set "ROOT_DIR=%SCRIPT_DIR%.."
set "TARGET_EXE=%ROOT_DIR%\app.exe"

; Validation prérequis
if not exist "%TARGET_EXE%" (
    echo ERREUR: app.exe non trouve
    pause
    exit /b 1
)

; Test 1
echo Test 1: Compilation...
"%TARGET_EXE%" "test1.ahk"
set "RESULT1=%ERRORLEVEL%"

if %RESULT1% equ 0 (
    echo SUCCES: Test 1 passe
) else (
    echo ECHEC: Test 1 - Code %RESULT1%
)

; Résumé
echo.
echo ========================================
echo           RESUME
echo ========================================

if %RESULT1% equ 0 (
    echo Test 1: SUCCES
) else (
    echo Test 1: ECHEC
)

pause >nul
```

## ERREURS COMMUNES À ÉVITER

1. **Encodage** - Toujours utiliser `chcp 65001` pour UTF-8
2. **Variables** - Préférer `%VAR%` à `!VAR!` sauf cas spéciaux
3. **Chemins** - Toujours utiliser des guillemets pour les espaces
4. **Emojis** - Éviter dans les scripts batch (problèmes d'encodage)
5. **PowerShell** - Utiliser `cmd /c` pour forcer CMD au lieu de PS
6. **Caractères spéciaux** - Attention aux accents dans les echo
