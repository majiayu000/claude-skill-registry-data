---
name: security-bounty-hunter
description: "Use when hunting for exploitable, remotely reachable vulnerabilities in a PHP/Laravel codebase for responsible disclosure or a bounty submission, not a general best-practices review. Biases toward user-controlled attack paths that pay and discards low-signal noise."
license: MIT
metadata:
  author: "Petr Král (pekral.cz)"
---

## Constraints
- Apply `@rules/security/backend.md` and `@rules/security/frontend.md`
- If the project uses Laravel, also apply `@rules/laravel/laravel.md`
- Read the stack and its versions (framework, Filament, Livewire, database, cache) from `composer.json` per `@rules/general/general.md` *Project Context*
- Read-only investigation — never modify, stage, commit, or push code; output is the finding report only
- Never run an exploit against infrastructure you are not authorized to test; keep PoCs minimal and safe

## Scope
Find unknown, exploitable bugs reachable from a real network or user boundary, and write them up to a standard a bounty program will accept. Bias toward "does this actually pay?" over "is this theoretically unsafe?".

How this differs from neighbors:
- `@skills/security-review/SKILL.md` reviews a diff against best practices; this skill **hunts unknown exploitable bugs** across the whole reachable surface.
- `@skills/security-threat-analysis/SKILL.md` remediates a **known** advisory/CVE; this skill discovers the unknown one.

## Use when
- Sweeping a repository for exploitable vulnerabilities
- Preparing a Huntr / HackerOne / program submission
- Triage where the question is "is this reportable?" not "is this tidy?"

## In-Scope Patterns (mapped to PHP/Laravel sinks)

| Pattern | CWE | PHP/Laravel sink to chase | Impact |
| --- | --- | --- | --- |
| SSRF via user-controlled URL | CWE-918 | `Http::get($userUrl)`, Guzzle, `file_get_contents($userUrl)` | internal network / cloud metadata |
| SQL injection | CWE-89 | `whereRaw`/`orderByRaw`/`havingRaw`/`DB::statement`/`DB::raw` with interpolation | data exfiltration, auth bypass |
| Auth / access bypass | CWE-287/639 | gaps in middleware, policy/gate, Livewire actions, IDOR on route-model binding | unauthorized data access |
| Unsafe deserialization | CWE-502 | `unserialize($userInput)`, unsigned cookie/cache payloads, `ShouldQueue` from untrusted source | RCE / object injection |
| Path traversal | CWE-22 | `Storage::get`/`disk()->get`, `file_get_contents`, download routes with `../` in path | arbitrary file read/write |
| Command injection | CWE-78 | `exec`/`shell_exec`/`system`/`proc_open`, `Process::run("... {$input}")` | code execution |
| XSS (auto-triggered) | CWE-79 | `{!! $userInput !!}`, Alpine `x-html`, raw JSON in `<script>` | session/admin theft |
| Mass-assignment to privileged column | CWE-915 | `$guarded = []` or `fillable` exposing `role`/`is_admin` + `create($request->all())` | privilege escalation |

## Skip These
Usually low-signal or out of scope unless the program says otherwise:
- Local-only `unserialize`/`eval`/`exec` with no remote path (CLI tooling, artisan-only)
- Fully hardcoded shell commands with no user input
- Missing security headers on their own
- Generic rate-limiting complaints with no exploit impact
- Self-XSS requiring the victim to paste content manually
- CSRF where Laravel's default protection is intact and the route is in the `web` group
- Findings only in demo, example, seeder, test, or vendored code

## Workflow
1. **Scope first** — read program rules, `SECURITY.md`, disclosure channel, and exclusions. Confirm the target and version are in scope.
2. **Map entrypoints** — routes (`routes/*.php`, `php artisan route:list`), controllers, FormRequests, Livewire/Filament actions, queued jobs, webhooks, console commands reachable via HTTP, and API resources.
3. **Static triage (optional)** — run static triage with semgrep, larastan/phpstan, or psalm where available; treat every hit as a lead, not a finding.
4. **Trace the path end to end** — from the boundary input to the sink. Prove the input is genuinely user-controlled.
5. **Confirm the sink is meaningful** — interpolation reaches the query/command/URL/file path with no escaping or authorization between.
6. **Prove exploitability** — build the smallest safe PoC (a single request or short script) that demonstrates impact.
7. **Check duplicates** — search existing advisories, CVEs, open issues, and prior reports before drafting.

### Triage loop example
```bash
# optional — any one of these, treat output as leads only
vendor/bin/phpstan analyse --no-progress   # Larastan runs as a PHPStan extension
# or: semgrep --config=auto --severity=ERROR --json
```
Then manually filter: drop tests/demos/fixtures/vendored code and any non-reachable path; keep only findings with a clear network or user-controlled route to a meaningful sink.

### Quick grep starters
```bash
grep -rnE "whereRaw|orderByRaw|havingRaw|DB::(raw|statement|select)\(" app/
grep -rnE "Http::(get|post)\(|file_get_contents\(|exec\(|shell_exec\(|proc_open\(" app/
grep -rnE "\{!!|unserialize\(|x-html" app/ resources/
grep -rnE "guarded\s*=\s*\[\s*\]|->all\(\)" app/
```

## Report Structure
```markdown
## Description
[What the vulnerability is and why it matters]

## Vulnerable Code
[File path, line range, and a small snippet]

## Proof of Concept
[Minimal working request or script]

## Impact
[What the attacker can achieve]

## Affected Version
[Version, commit, or deployment target tested]
```

## Quality Gate — before submitting
- The code path is reachable from a real user or network boundary
- The input is genuinely user-controlled, all the way to the sink
- The sink is meaningful and exploitable (not theoretical)
- The PoC works and is the smallest safe demonstration possible
- The issue is not already covered by an advisory, CVE, or open ticket
- The target and version are actually in scope for the program

## Done when
- Each finding follows the Report Structure and passes every Quality Gate item
- Out-of-scope and low-signal patterns were filtered out, not reported
- No code was modified and no unauthorized exploit was run

## Related Skills
- `@skills/security-review/SKILL.md` — best-practices review of a known change set
- `@skills/security-threat-analysis/SKILL.md` — remediate a referenced advisory/CVE

## Output Humanization
- Use [blader/humanizer](https://github.com/blader/humanizer) for all skill outputs to keep the text natural and human-friendly.
