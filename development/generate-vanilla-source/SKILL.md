---
name: generate-vanilla-source
description: Generate vanilla Minecraft source code.
---

1. Run genSources
   ```shell
   ./gradlew genSources
   ```
2. Source jars will be generated under following paths:

   - `./.gradle/loom-cache/minecraftMaven/net/minecraft/minecraft-common-<hash>/<version>/minecraft-common-<hash>-<version>-sources.jar`
   - `./.gradle/loom-cache/remapped_mods/<mapping_version>/net/fabricmc/fabric-api/<module>/<version>/<module>-<version>-sources.jar`

3. Inspect JAR contents in memory (no extraction to disk)

   ```powershell
   # Example: Read LivingEntity.java from minecraft-common sources JAR
   $jarPath = ".gradle\loom-cache\minecraftMaven\net\minecraft\minecraft-common-<hash>\<version>\minecraft-common-<hash>-<version>-sources.jar"
   Add-Type -AssemblyName System.IO.Compression.FileSystem
   $zip = [System.IO.Compression.ZipFile]::OpenRead($jarPath)
   $entry = $zip.Entries | Where-Object { $_.FullName -eq "net/minecraft/entity/LivingEntity.java" }
   $stream = $entry.Open()
   $reader = New-Object System.IO.StreamReader($stream)
   $content = $reader.ReadToEnd()
   $reader.Close()
   $stream.Close()
   $zip.Dispose()

   # Search for specific methods or patterns
   $content | Select-String -Pattern "methodName" -Context 5,10

   # Extract specific line ranges
   $lines = $content -split "`n"
   $startIndex = ($lines | Select-String -Pattern "public void methodName" | Select-Object -First 1).LineNumber - 1
   $lines[$startIndex..($startIndex + 20)] -join "`n"
   ```
