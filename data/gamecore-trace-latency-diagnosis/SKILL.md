---
name: gamecore-trace-latency-diagnosis
description: "Diagnose HttpCore endpoint latency in the gamecore repo from OTEL trace waterfalls — span attribution (CONNECT = Npgsql physical opens, Steam calls in SteamAuth), code call-site pinning, and the docs/ diagnosis-doc convention."
---

# Diagnosing HttpCore endpoint latency from trace waterfalls

Procedure proven on POST /user/login (~840 ms → root cause: sequential uncached Steam Web API calls + pool-minted DB connections). User supplies the trace waterfall + log lines from the analytics page.

## 1. Bucket the waterfall
- **External HTTP GET/POST spans**: match to log lines (sent/received timestamps confirm duration and single-attempt vs retry). These are usually the dominant cost.
- **CONNECT spans** (e.g. `CONNECT Handball-predev-origin`): physical Postgres connection opens, emitted by Npgsql tracing wired in `Library/GameCore.DAL/Databases/DatabaseContextPoolShared.cs` (`ConfigureQueryTracing`). Multiple CONNECTs to the SAME database in one request = separate pools/contexts each opening cold — the AGENTS.md scoped-session anti-pattern. Sum them as "connection churn", distinct from query time.
- **SELECT/INSERT/UPDATE/DELETE spans**: in this stack each is 0.4–4 ms; DB queries are essentially never the cause.
- **Internal spans**: match literal names to `StartActivity("...")` calls. Nesting inflates parents (e.g. `Authenticating` looked heavy only because CONNECT opens sat inside it).

## 2. Attribute spans to code (known map, handball01 worktree)
- `Logging in` → `Container/HttpCore/Controllers/user/UserController.cs` (~:509, inside `Login1_1`, the POST /user/login endpoint).
- `Authenticating` → `GameCore2/Services/Identity/UserService.cs` (~:191, `AuthenticateAsync`).
- `Lookup/Create User` → `UserService.cs` (~:263).
- Steam Web API calls → `GameCore2/Services/PlatformAuth/SteamAuth.cs`: `ValidateAsync` calls `GetPublisherAppOwnership` (~:244) then `AuthenticateUserTicket` (~:314) **sequentially**, uncached, per login. `AuthenticateUserTicket`'s response carries only result/steamid/vacbanned/publishedbanned (no entitlements) — the ownership call cannot be replaced by it, only cached (per steamId+appId, TTL hours, existing primitive `CacheLogic.GetOrSetLayeredMessagePackCacheAsync`) or parallelized (`Task.WhenAll`; watch the Soft-fail early-return that skips ticket validation for non-owners).
- HttpClient names: `quickretry` (Polly 1s/2s/4s waits — tail-latency risk only), defined in `GameCore2/Extensions/HttpClientExtension.cs`.

## 3. Gotchas
- **Trace log categories can lie**: login traces logged under `...dynasty.Centurion.CenturionController` but the endpoint is `UserController.Login1_1`. Match on route + log message text, not category.
- `IsValidIpAsync` runs twice per login (`UserController` + `UserService`) → duplicate `SELECT gc_configuration.ip_filters`. Immaterial; note and move on.
- Some internal spans (`SettingDapperRead`) don't exist verbatim in source — DAL session bookkeeping; don't chase them.

## 4. Write the deliverable
`docs/<endpoint>-latency-diagnosis.md` with sections: Summary (bucket table with ms + % of total) / Trace evidence (span durations + log timestamps) / Root cause / Code call-sites (file:line table) / Ranked fixes (each with expected ms saved derived from the trace) / Observations.
- Pin EVERY code claim to file:line from actual reads — no invented citations.
- Diagnosis only unless asked: `git status --porcelain` must show only the new doc.
- Median math: total − external-call time ≈ post-fix estimate; recommend p50/p95 over many traces for before/after.
