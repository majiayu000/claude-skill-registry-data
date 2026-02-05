---
name: generate-clients
description: Generates c# and typescript clients for BymseRead.Service.
---

1. Check current folder and go to root of the repository if needed
2. Ensure project dotnet tools are restored by running `dotnet tool restore`
2. Then run `dotnet run --project src/BymseRead.Tools/BymseRead.Tools.csproj GenerateClients`
3. If tool exited with error then report the issue to user and stop