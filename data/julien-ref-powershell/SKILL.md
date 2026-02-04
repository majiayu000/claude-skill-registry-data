---
name: julien-ref-powershell
description: PowerShell naming conventions and organization best practices. Covers Verb-Noun functions, variable naming, module structure, and documentation standards.
triggers:
  - aide-moi avec mon powershell
  - mon powershell ne marche pas
  - help with my powershell script
  - write powershell function
  - powershell style guide
  - powershell
  - powershell script
  - ps1
  - powershell best practices
---

# PowerShell - Conventions de Nommage et Organisation

## Vue d'Ensemble

## Observability

**First**: At the start of execution, display:
```
🔧 Skill "julien-ref-powershell" activated
```

Ce document définit les conventions de nommage et d'organisation pour les projets PowerShell, garantissant cohérence, maintenabilité et scalabilité.

## Structure d'Organisation Générique

### Structure de Base
```
PowerShell-Project/
├── Core/                    # Scripts essentiels et infrastructure
├── Modules/                 # Modules PowerShell organisés
├── Scripts/                 # Scripts par domaine fonctionnel
│   ├── Administration/      # Scripts d'administration système
│   ├── Development/         # Outils de développement
│   ├── Network/            # Scripts réseau
│   ├── Security/           # Scripts sécurité
│   └── Utilities/          # Utilitaires génériques
├── Config/                  # Fichiers de configuration
├── Templates/               # Templates et modèles
├── Tests/                   # Tests automatisés
├── Docs/                    # Documentation
└── Resources/               # Ressources (JSON, XML, etc.)
```

## Conventions de Nommage

### 1. Fichiers PowerShell

#### Scripts (.ps1)
**Format :** `Verb-Noun-Context.ps1`

```powershell
# CORRECT
Get-SystemInfo.ps1
Set-EnvironmentPath.ps1
Start-ServiceMonitor.ps1
Remove-TempFiles.ps1
Test-NetworkConnectivity.ps1
Backup-UserProfiles.ps1

# ÉVITER
get_system_info.ps1          # snake_case
systemInfo.ps1               # camelCase
SystemInformationScript.ps1  # trop long
sys-info.ps1                 # pas descriptif
GetSysInfo.ps1              # PascalCase sans tiret
```

#### Modules (.psm1)
**Format :** `ModuleName.psm1` (PascalCase)

```powershell
# CORRECT
SystemAdministration.psm1
NetworkUtilities.psm1
SecurityTools.psm1
DatabaseConnector.psm1

# ÉVITER
system_admin.psm1
networkUtils.psm1
security-tools.psm1
```

### 2. Fonctions PowerShell

#### Convention Standard PowerShell
**Format :** `Verb-Noun` (verbes approuvés PowerShell)

```powershell
# CORRECT - Verbes approuvés
function Get-UserPermissions { }
function Set-NetworkConfiguration { }
function Start-BackupProcess { }
function Stop-RunningServices { }
function Test-DatabaseConnection { }
function New-SecurityPolicy { }
function Remove-TempDirectories { }
function Update-SystemConfiguration { }

# ÉVITER - Verbes non-standard
function Fetch-UserData { }         # Utiliser Get-
function Configure-Network { }      # Utiliser Set-
function Launch-Application { }     # Utiliser Start-
function Destroy-TempFiles { }      # Utiliser Remove-
```

#### Verbes PowerShell Approuvés par Catégorie

**Données :**
- `Get-`, `Set-`, `Clear-`, `Copy-`, `Move-`, `Remove-`

**Lifecycle :**
- `New-`, `Start-`, `Stop-`, `Restart-`, `Suspend-`, `Resume-`

**Diagnostic :**
- `Test-`, `Trace-`, `Measure-`, `Debug-`, `Repair-`

**Sécurité :**
- `Block-`, `Grant-`, `Revoke-`, `Protect-`, `Unprotect-`

**Changements :**
- `Add-`, `Update-`, `Install-`, `Uninstall-`, `Register-`, `Unregister-`

### 3. Variables

#### Variables Locales
**Format :** `camelCase`

```powershell
# CORRECT
$userName = "admin"
$connectionString = "Server=localhost"
$maxRetryCount = 3
$isConfigurationValid = $true
$systemServices = Get-Service

# ÉVITER
$UserName = "admin"              # PascalCase pour locales
$connection_string = "..."       # snake_case
$max-retry-count = 3            # kebab-case
```

#### Variables Globales
**Format :** `PascalCase` avec préfixe explicite

```powershell
# CORRECT
$Global:ApplicationSettings = @{}
$Global:ModuleConfiguration = @{}
$Global:SystemEnvironment = @{}
$Script:ModulePrivateData = @{}

# ÉVITER
$Global:settings = @{}           # camelCase pour globales
$appConfig = @{}                 # sans préfixe Global
```

#### Variables d'Environnement
**Format :** `UPPER_CASE`

```powershell
# CORRECT
$env:POWERSHELL_PROFILE_LOADED = "1"
$env:APPLICATION_LOG_LEVEL = "INFO"
$env:DATABASE_CONNECTION_TIMEOUT = "30"
```

### 4. Paramètres de Fonctions

**Format :** `PascalCase`

```powershell
function Get-UserInformation {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [string]$UserName,

        [Parameter(Mandatory = $false)]
        [string]$DomainName = "localhost",

        [switch]$IncludeGroups,

        [ValidateRange(1, 100)]
        [int]$MaxResults = 50
    )
}
```

### 5. Alias

**Format :** `[Domaine][Action]` (2-4 caractères)

```powershell
# Navigation
Set-Alias -Name "nf" -Value "Navigate-ToFolder"
Set-Alias -Name "nh" -Value "Navigate-ToHome"

# Recherche
Set-Alias -Name "sf" -Value "Search-Files"
Set-Alias -Name "sc" -Value "Search-Content"

# Système
Set-Alias -Name "ss" -Value "Show-SystemStatus"
Set-Alias -Name "sl" -Value "Show-SystemLogs"
```

### 6. Constantes

**Format :** `UPPER_CASE` avec préfixe de module

```powershell
$MODULE_VERSION = "1.0.0"
$DEFAULT_TIMEOUT = 30
$MAX_RETRY_ATTEMPTS = 3
$LOG_LEVEL_DEBUG = "DEBUG"
```

## Documentation Standard

### En-tête de Script
```powershell
<#
.SYNOPSIS
    Description courte et précise du script (max 80 caractères)

.DESCRIPTION
    Description détaillée du script, de son fonctionnement et de ses objectifs.
    Explique les dépendances, les prérequis et les effets de bord.

.PARAMETER ParameterName
    Description détaillée du paramètre et de son utilisation

.EXAMPLE
    Script-Name -Parameter "Value"
    Description du résultat attendu

.NOTES
    Author: Nom de l'auteur
    Version: X.Y.Z
    Created: YYYY-MM-DD
    Last Updated: YYYY-MM-DD
    Dependencies: Liste des dépendances requises
#>
```

## Validation et Tests

### Checklist de Validation
- [ ] Nommage respecte les conventions `Verb-Noun`
- [ ] Variables suivent les conventions de casse
- [ ] Documentation complète avec exemples
- [ ] Gestion d'erreur implémentée
- [ ] Tests unitaires présents
- [ ] Performance acceptable
- [ ] Sécurité validée

### Obtenir les Verbes Approuvés
```powershell
# Obtenir la liste complète des verbes approuvés
Get-Verb | Sort-Object Verb | Format-Table -AutoSize

# Vérifier si un verbe est approuvé
$verb = "Configure"
if ($verb -notin (Get-Verb).Verb) {
    Write-Warning "Verbe non-standard: $verb"
    Write-Host "Verbes suggérés: Set, Update, Install"
}
```

## Outils de Formatage

- **PSScriptAnalyzer** : Analyse statique et conventions
- **Plaster** : Templates de projets PowerShell
- **Pester** : Framework de tests
- **PowerShell-Beautifier** : Formatage automatique
