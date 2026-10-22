---
name: Codebase Navigator & Analyst
description: Expert instructions for analyzing project structure, dependencies, code statistics, and architecture.
---

# Codebase Navigator & Analyst

This skill provides tools and methods to quickly understand the health, structure, and statistics of the Android codebase.

## Dependency Inspection
To understand what libraries are used:
```bash
./gradlew app:dependencies
```
*Tip*: Look for strictly versioned libraries vs dynamic versions (bad practice).

## Architecture Detective
- **AndroidManifest.xml**: The entry point. Look here to find the **Launcher Activity**, defined Services, and Receivers.
- **Package Structure**:
    - `ui/`: Often contains Activities, Fragments, ViewModels.
    - `data/` or `repo/`: Repository pattern implementation.
    - `network/` or `api/`: Retrofit/OkHttp definitions.

## Code Statistics (PowerShell)
To count lines of code (LOC) for Java files recursively:
```powershell
Get-ChildItem -Recurse -Filter *.java | Get-Content | Measure-Object -Line
```

To find the largest files (potential monoliths):
```powershell
Get-ChildItem -Recurse -Filter *.java | Sort-Object Length -Descending | Select-Object Name, Length -First 10
```

## Health Checks
- **Giant Classes**: If a file > 1000 lines, it likely needs refactoring.
- **Deep Nesting**: If indentation levels > 5, consider simplifying logic.
