---
name: anthill-k8s-deploy-verify
description: "Validate AntHill's k8s/ manifests, the Gitea deploy workflow, and tools/publish-server.ps1 locally without a cluster — kubeconform schema checks, docker runtime smoke of the SDK container image, PowerShell script/help checks — including the environment traps (kubectl 1.36 offline dry-run fails, PEP 668, PS comma-list concat). Use when editing k8s/*.yaml, .gitea/workflows/deploy-server.yml, or the publish script, or when asked to prove the server deployment works."
---

# Verify AntHill K8s deployment artifacts locally (no cluster)

This box (Windows, Docker Desktop, kubectl 1.36, no cluster context, no helm) cannot run `kubectl apply` for real. This is the offline proof stack that caught real bugs twice in one session.

## 1. Schema validation — kubeconform, not kubectl
`kubectl apply/create --dry-run=client --validate=false` FAILS offline on kubectl 1.36: recognition still needs API discovery (`couldn't get current server API group list`). Do not burn time on it.

Single-exe kubeconform works:
```
mkdir -p "$TEMP/kc" && curl -fsSL -o "$TEMP/kc/kc.zip" \
  https://github.com/yannh/kubeconform/releases/download/v0.6.7/kubeconform-windows-amd64.zip
unzip -o "$TEMP/kc/kc.zip" -d "$TEMP/kc"
"$TEMP/kc/kubeconform.exe" -strict -verbose k8s/namespace.yaml k8s/postgres.yaml k8s/web.yaml k8s/optional/loreserver.yaml
```
Expect one "is valid" line per resource.

## 2. YAML syntax — pip is PEP 668 locked
`python -m pip install --user --break-system-packages pyyaml`, then `yaml.safe_load_all` over `k8s/**/*.yaml` + the workflow. (Document counts: namespace 1, postgres 3, web 4, optional/loreserver 2, workflow 1.)

## 3. Runtime smoke — the strongest proof
The CI path is SDK container publish (no Dockerfile exists; do not add one):
```
dotnet publish src/AntHill.Web/AntHill.Web.csproj -c Release -t:PublishContainer -p:ContainerImageTag=<tag>
```
Base image resolves to `mcr.microsoft.com/dotnet/aspnet:10.0`; app listens on 8080. Then mirror the pod flow on a scratch network:
```
docker network create anthill-smoke
docker run -d --name anthill-smoke-pg --network anthill-smoke \
  -e POSTGRES_USER=anthill -e POSTGRES_PASSWORD=smoke -e POSTGRES_DB=AssetLibrary postgres:17
# wait like the init container does:
until docker exec anthill-smoke-pg pg_isready -U anthill -d AssetLibrary; do sleep 1; done
docker run -d --name anthill-smoke-web --network anthill-smoke -p 18080:8080 \
  -e ConnectionStrings__AssetLibrary="Host=anthill-smoke-pg;Port=5432;Database=AssetLibrary;Username=anthill;Password=smoke" \
  -e ASPNETCORE_ENVIRONMENT=Production anthill-web:<tag>
# poll http://localhost:18080/alive (expect 200) and /health (expect "Healthy")
```
Startup runs EF migrations; success looks like "Now listening on: http://[::]:8080" in `docker logs`. Clean up containers + network after. `Auth:Mode` unset → standalone auth; `Lore:RepositoryPath` unset → in-memory FakeLoreClient, both by design.

## 4. tools/publish-server.ps1 checks
- Parse: pass the check code through an env var — bash eats `$vars` inside double-quoted `-Command` strings. `powershell -NoProfile -Command '$env:CHECK | Invoke-Expression'` with CHECK containing the `[System.Management.Automation.Language.Parser]::ParseFile(...)` snippet.
- Help binding: `powershell -NoProfile -Command 'Get-Help D:\AntHill\tools\publish-server.ps1 -Full'`. Do NOT use `-File script -?` — it prints nothing.
- Prove the build path, not just exit code: after a smoke run, `docker image inspect anthill-web:<tag>` must succeed. A plain-publish success (exit 0, no "Building image" line) is NOT container success.

## 5. Traps that actually bit
- **PowerShell comma-list concat**: `@('a', 'b', '-p:x=' + $var)` parses as `('a','b','-p:x=') + $var` — array concat, so the tag becomes a stray positional arg (MSB1008 "Only one project can be specified"). Always use expandable strings: `"-p:x=$var"`.
- **Anchored multi-hunk edits on this script went wrong twice** (overlapping ranges, truncated echo). Prefer a full `write` of the file; re-read after any edit.
- `-p:ContainerRegistry` must be hostname only (no scheme); `-Registry <host>` in the script means build AND push (SDK pushes when a registry is set) — there is no separate push switch.

## Pipeline test suites that run hermetically (mirrors deploy-server.yml)
`tests/AntHill.Client.Tests` (271✓/3 skip), `tests/AntHill.Data.Tests` (31✓, Testcontainers), `tests/AntHill.Web.Tests` (729✓, bUnit). Deliberately excluded: Lore.Tests (needs live loreserver), Layout.Tests (needs Playwright browsers).
