---
name: winget-pr-retry
description: WinGet PR（microsoft/winget-pkgs）のCI/CDパイプラインを空プッシュで再トリガーすることで、リリースをリトライする。使用タイミング：(1) WinGet PRの自動実行がエラーになった場合、(2) microsoft/winget-pkgsへのPRでCI/CDを再実行したい場合、(3) リリースプロセスでWinGet検証を再トリガーする必要がある場合
---

# WinGet PR Retry

## Overview

WinGet PR（microsoft/winget-pkgs）の自動実行（CI/CD）がエラーになった場合、空コミットをプッシュしてパイプラインを再トリガーします。

## Usage

Run the PowerShell script to retry a WinGet PR:

```powershell
./skills/winget-pr-retry/scripts/Retry-WinGetPR.ps1
```

### Parameters

- `-BranchName` (optional): 再実行するブランチ名。省略時は現在のブランチ
- `-Message` (optional): 空コミットのメッセージ。デフォルト: "Empty commit to retrigger CI/CD pipeline"

### Examples

Current branch:
```powershell
./skills/winget-pr-retry/scripts/Retry-WinGetPR.ps1
```

Specific branch:
```powershell
./skills/winget-pr-retry/scripts/Retry-WinGetPR.ps1 -BranchName NuitsJp.GistGet-1.2.0
```

Custom message:
```powershell
./skills/winget-pr-retry/scripts/Retry-WinGetPR.ps1 -Message "Retry: Fix validation error"
```

## How It Works

1. Navigate to `external/winget-pkgs` submodule
2. Checkout specified branch (or use current)
3. Create empty commit with `git commit --allow-empty`
4. Push to origin to trigger CI/CD pipeline

## Resources

### scripts/

- `skills/winget-pr-retry/scripts/Retry-WinGetPR.ps1` - PowerShell Core script for retrying WinGet PRs
