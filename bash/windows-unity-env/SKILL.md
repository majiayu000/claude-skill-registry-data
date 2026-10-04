---
name: windows-unity-env
description: Use when building the Windows player, running the smoke test, invoking Unity.exe from the command line on this Windows machine, or when a build fails with "Acceso denegado", hangs on exit, or leaves files modified.
---

# Unity en esta máquina Windows

- **Unity**: `"/c/Program Files/Unity/Hub/Editor/6000.3.2f1/Editor/Unity.exe"` (6000.3.2f1).
- **Shell**: Git Bash para los scripts de `.superpowers/`. PowerShell 5.1 no tiene `&&`.
- Cierra el editor antes de usar batchmode: el proyecto se bloquea.

## Build de Windows y prueba de humo

```bash
U="/c/Program Files/Unity/Hub/Editor/6000.3.2f1/Editor/Unity.exe"
"$U" -batchmode -nographics -quit -projectPath . -executeMethod BuildScript.BuildWindows \
     -buildPath Builds/Windows-final/Detectives.exe -logFile Logs/build.log
grep "\[Build\]" Logs/build.log            # "Succeeded · … · errores 0"
rm -f Logs/smoke.log
./Builds/Windows-final/Detectives.exe -batchmode -nographics -smoketest -logFile "$(pwd -W)/Logs/smoke.log"
grep SMOKE Logs/smoke.log                   # "SMOKE OK" (o "SMOKE FAIL", con salida 1)
```

## Casos reales

| Síntoma | Qué hacer |
|---|---|
| `Copying the file failed: Acceso denegado` en `Builds/Windows/` | Windows bloquea esa ruta, sin ningún proceso vivo que la use. Usa **`-buildPath`** (no `-out`) hacia `Builds/Windows-final/`. No toques permisos ni el antivirus. |
| La build deja `ArtCatalog.asset` y `ProjectSettings.asset` modificados | Si `git diff` no tiene líneas `+`/`-` reales, son solo finales de línea: `git checkout --` de esos archivos. |
| `UnityConnectSettings.asset` modificado | `git checkout --`: el editor lo activa solo. |
| El proceso no sale con `-nographics` (1 de cada 4 a 12 veces) | En bucles, `timeout 45`. En la build no pasa. |
| La prueba de humo "pasa" sin haberse ejecutado | Borra el log antes y busca `SMOKE OK` en el log recién creado. |
| `GC.GetAllocatedBytesForCurrentThread` da 0 | Es Mono de Unity: mide el heap. |

Las rutas de `-logFile` para el `.exe` van en formato Windows (`$(pwd -W)`). Ver también la skill `batchmode-capture`.
