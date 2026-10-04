---
name: workflow-smell
description: >
  Deep-audit code, CI/CD pipelines, Dockerfiles, shell scripts, Makefiles, Python projects,
  and config files for half-baked workflows — patterns that add complexity without value.
  Trigger this skill whenever the user asks to "review my pipeline", "audit this config",
  "why is this so complicated", "is this over-engineered", "does this make sense",
  "clean up my workflow", "simplify this", "what's wrong with this", or pastes a
  CI/CD YAML, Dockerfile, Makefile, shell script, or multi-step config and asks for feedback.
  Also trigger on vague requests like "take a look at this" or "is this okay" when the input
  is a workflow artifact. Produces a compound-smell report with severity, confidence,
  effort estimate, diff-style fix, smell interaction map, and a phased refactor roadmap.
---

# Workflow Smell Auditor — Advanced

Identifies half-baked workflows: engineering effort that creates toil, confusion, or
maintenance debt without delivering proportional value.

**If files are present on disk**, run `scripts/prescan.py` first (see §Pre-Scan).  
**If input is pasted text**, skip to §Audit Protocol and do all analysis inline.

---

## Smell Taxonomy

Each smell has: **ID · Severity · Detection signal · Compounds with**

### 🔴 CRITICAL — Active harm, causes failures or data loss risk

| ID | Smell | Signal | Compounds With |
|---|---|---|---|
| C1 | **Silent Failure Masking** | `\|\| true`, `exit 0` on non-trivial ops, `2>/dev/null` on writes | C2, M4 |
| C2 | **Ouroboros Pipeline** | Job triggers a pipeline that re-includes or re-triggers the same job | C1 |
| C3 | **Accidental Idempotency Break** | Step appends/patches state it assumes is clean (file append without truncate, DB migration without guard) | M3 |
| C4 | **Credential Churn** | Auth token re-acquired per-step when it could be passed through; or rotated mid-pipeline causing race | M6 |
| C5 | **Phantom Parallelism** | `parallel:` or matrix defined, but all jobs share a mutex resource (DB, file lock, port) — effectively serial with overhead | H3 |

### 🔴 HIGH — Complexity that actively hurts

| ID | Smell | Signal | Compounds With |
|---|---|---|---|
| H1 | **Wrapper Theater** | Script/job whose entire body calls exactly one other script/job | H2, M1 |
| H2 | **Pipeline Ping-Pong** | Artifact produced → passed → consumed → re-derivable from original source in one step | H1 |
| H3 | **Cargo-Cult Config** | Options with no local relevance (32-core parallelism on 2-core runner, JVM flags in a Python job) | C5 |
| H4 | **Dead Branch** | `if/else` or `rules:` path unreachable given actual variable values or trigger conditions | M5 |
| H5 | **Abstract Nothingness** | Abstraction layer (base class, mixin, YAML anchor, shared template) with exactly one implementor and zero variation points | — |
| H6 | **Temporal Coupling Without Declaration** | Jobs that must run in order but no `needs:` / `depends_on` declares it — order is implicit, fragile | M3 |
| H7 | **Speculative Infrastructure** | Infra, stage, or abstraction built for a feature with no active code referencing it | — |
| H8 | **Thermometer Pattern** | Config reads 5+ env vars to decide between 2 code paths — env var explosion for binary logic | M2 |

### 🟡 MEDIUM — Toil generators

| ID | Smell | Signal | Compounds With |
|---|---|---|---|
| M1 | **Re-fetch Redundancy** | Artifact available via cache/pass but re-downloaded in later stage | H1 |
| M2 | **Phantom Variable** | Env var defined but never read, or read but never set in any reachable path | H8 |
| M3 | **Cache Miss Architecture** | Cache key so specific (includes commit SHA, timestamp) it never actually hits | C3, H6 |
| M4 | **Retry Loop Around Logic Error** | `retry: N` on a job failing due to code bug, not flakiness | C1 |
| M5 | **Step-Comment Mismatch** | Comment describes different action than code performs | H4 |
| M6 | **Multi-Stage Mirage** | Docker multi-stage with no size reduction: same base, same user, no `--from` selective copy | C4 |
| M7 | **Environment Leakage** | Env vars from one conceptual domain (build secrets) visible in unrelated stages (test, lint) | — |
| M8 | **Version Pin Drift** | Pinned deps with no automation to update them; >90 days stale | — |
| M9 | **Registry Roulette** | Pulling from multiple registries (DockerHub + ECR + Harbor) without fallback or mirror strategy | — |
| M10 | **Ownership Vacuum** | Critical step has no owner annotation, no runbook link, no `CODEOWNERS` entry | — |

### 🟢 LOW — Noise / mild overengineering

| ID | Smell | Signal | Compounds With |
|---|---|---|---|
| L1 | **Echo-Driven Debugging** | 5+ `echo`/`RUN echo` left in production config | — |
| L2 | **Redundant Gate** | Conditional that always evaluates to same branch | H4 |
| L3 | **Alias Maze** | alias → function → script → alias, all same transform | H1 |
| L4 | **TODO Workflow** | Stage/function that is a TODO stub with `exit 0` or `pass` | H7 |
| L5 | **Configuration Archaeology** | Large commented-out blocks of old config never deleted | — |
| L6 | **Makefile Tax** | `make foo` wraps single raw command with no variable expansion or dep tracking | H1 |
| L7 | **Hardcoded Assumption** | Magic number/string baked in where env var or config would suffice | H8 |

---

## Compound Smell Clusters

When 3+ smells interact, escalate to a **Cluster** — a named anti-pattern worth calling out explicitly.

| Cluster | Smells | Name | What's really happening |
|---|---|---|---|
| 🔴 | H1 + H2 + M1 | **Rube Goldberg Machine** | Chain of wrappers where each step passes data the previous step could have produced directly |
| 🔴 | C1 + M4 + H4 | **Confidence Theater** | Pipeline appears to pass but silently skips failures; retry masks the symptom |
| 🔴 | H3 + C5 + M3 | **Cargo-Cult Performance** | Parallelism and caching configured for show; actual runtime unchanged or worse |
| 🟡 | H5 + H7 + L4 | **Future-Proof Graveyard** | Abstractions and stubs for features that will never ship |
| 🟡 | H8 + M2 + M7 | **Variable Entropy** | Env var explosion with phantom and leaking vars — no one knows what controls what |
| 🟡 | M6 + M9 + C4 | **Docker Debt** | Multi-stage that adds no value, pulls from scattered registries, re-auths per stage |

---

## Audit Protocol

### Phase 0: Pre-Scan (files on disk only)

```bash
python scripts/prescan.py <file_or_dir>
```

Produces a JSON smell-hint map. Read it, then proceed to semantic analysis.  
If no filesystem access, skip and do full analysis inline.

### Phase 1: Artifact Classification

Identify all artifact types present:

```
[type] → [what to focus on]
GitLab CI YAML  → stages DAG, needs graph, rules reachability, artifact/cache config
Dockerfile      → layer count, FROM chain, --from usage, final image base, COPY patterns  
Shell/Bash      → error handling (set -e/o pipefail), exit codes, subshell leaks
Makefile        → .PHONY, dep tracking, variable expansion, external calls
Python project  → pyproject.toml, requirements*.txt, __init__ graph, entry points
Helm/K8s YAML   → value overrides, template logic, hook ordering
Generic config  → env var surface area, include depth, templating overhead
```

**Multi-file inputs**: build a cross-artifact map before analyzing individual files.  
A smell in one file may be caused by or amplify a smell in another.

### Phase 2: Dependency Graph (CI/pipeline inputs)

Mentally construct the DAG:

1. List all stages/jobs/targets
2. Map declared dependencies (`needs`, `depends_on`, `make deps`)
3. Map implicit dependencies (shared artifacts, shared env vars)
4. Identify:
   - **Orphaned nodes** — no caller, no downstream consumer
   - **Critical path bottlenecks** — long serial chains that could parallelize
   - **Undeclared edges** — implicit ordering without declaration (→ H6)
   - **Cycles** — any job that eventually triggers itself (→ C2)

### Phase 3: Variable Surface Scan

Track all variables across the artifact set:

```
Defined: WHERE it's set (default, CI var, .env, hardcoded)
Used:    WHERE it's referenced
State:   live | phantom | leaked | shadowed
```

- Phantom = defined, never used (→ M2)
- Leaked = scoped to one domain, visible in another (→ M7)  
- Shadowed = overridden before first use
- Thermometer = 5+ vars controlling binary logic (→ H8)

### Phase 4: Smell Scan

Apply taxonomy. For each finding:

```
ID   : <smell-id>  e.g. H1
Type : <smell-name>
Loc  : <file:line or job/stage>
Conf : HIGH | MED | LOW   (certainty of the diagnosis)
Effort: S | M | L | XL   (fix effort)
Diagnosis : <one sentence>
Evidence  : <trimmed snippet>
Compounds : <other smell IDs active in same scope>
Fix (diff):
  - <removed line(s)>
  + <replacement line(s)>
```

**Confidence rubric:**
- HIGH — pattern is unambiguous (dead branch with static condition, echo-only wrapper)
- MED — pattern likely but depends on undisclosed context (retry might be for real flakiness)
- LOW — speculative; flag for human verification

**Effort rubric:**
- S — delete or one-line change
- M — refactor within the file (<1hr)
- L — cross-file change or requires coordination (<1 day)
- XL — architectural change, affects multiple teams or systems

### Phase 5: Cluster Detection

After individual smells, check compound cluster table.  
If a cluster applies, emit a **Cluster Block** (see output format).

### Phase 6: Score

```
Complexity Score = Σ(weight × count)
  Critical = 4pts each
  High     = 3pts each
  Medium   = 2pts each
  Low      = 1pt each
  Cluster  = +2pts each (additive)
  Cap      = 20
```

| Score | Verdict |
|---|---|
| 0–3 | ✅ Lean |
| 4–7 | 🟡 Needs Trim |
| 8–13 | 🟠 Complexity Trap |
| 14–20 | 🔴 Rip It Down |

### Phase 7: Refactor Roadmap

Three-phase plan — don't just list fixes, sequence them:

```
Phase 1 — Stop the bleeding (Critical + Silent Failures) · <1 day
Phase 2 — Reduce surface area (High smells, clusters) · <1 sprint  
Phase 3 — Clean debt (Medium + Low) · ongoing
```

Each phase: ordered list of (SmellID → action → expected outcome).

---

## Output Format

```markdown
## Workflow Smell Report

**Files analyzed**: ...
**Artifact types**: ...

---

### Dependency Graph
[DAG summary — list nodes, edges, orphans, bottlenecks]

---

### Variable Surface
| Variable | Defined | Used | State |
|---|---|---|---|

---

### Smells Found

#### 🔴 C1 — Silent Failure Masking · Confidence: HIGH · Effort: S
- **Location**: `.gitlab-ci.yml:42 (deploy job)`
- **Diagnosis**: `|| true` on `kubectl apply` means failed deploys report success.
- **Evidence**:
  ```yaml
  script:
    - kubectl apply -f manifests/ || true
  ```
- **Fix**:
  ```diff
  - - kubectl apply -f manifests/ || true
  + - kubectl apply -f manifests/
  ```
- **Compounds with**: M4 (retry will mask the same failure 3x)

---

[...more smells...]

---

### Compound Clusters

#### 🔴 Cluster: Confidence Theater (C1 + M4 + H4)
> The pipeline appears healthy but silently absorbs failures. The retry on `deploy`
> masks `|| true` swallowing kubectl errors. The dead `when: manual` branch means
> no human gate exists either. A bad deploy ships automatically and invisibly.

---

### Score
**Complexity Score**: 14/20
**Verdict**: 🔴 Rip It Down

---

### Refactor Roadmap

**Phase 1 — Stop the bleeding** · target: today
1. C1 → Remove `|| true` from `deploy` job. Add `kubectl rollout status` after apply.
2. M4 → Remove `retry: 3` from `deploy`. Retry on deploy logic errors is dangerous.

**Phase 2 — Reduce surface area** · target: this sprint
3. H6 → Add explicit `needs: [build]` to `test` job.
4. H2 → Collapse `package → upload → download → install` into direct artifact pass.

**Phase 3 — Clean debt** · target: next sprint
5. M2 → Delete `DEPLOY_DRY_RUN` — set in 3 places, read nowhere.
6. L5 → Delete 60-line commented-out Helm block in `deploy.sh`.
```

---

## Heuristics

- **Don't flag necessary complexity**: multi-env deploys, real matrix builds, legitimate flakiness retries, security boundaries between stages
- **Speculative smells**: if complexity exists for a future feature, flag as `[speculative]` with MED confidence — don't assume it's wrong
- **Ecosystem conventions**: standard patterns that are misconfigured get a "correct usage" note, not a delete
- **Partial input**: if only one file is provided but cross-file smells are suspected, note what else to look at
- **Conflicting smells**: if two smells contradict (one says "add abstraction", one says "remove abstraction"), flag the tension explicitly

---

## References

- `references/antipatterns.md` — per-ecosystem examples (GitLab CI, Docker, shell, Python, Helm)
- `references/dag-analysis.md` — how to read and critique pipeline DAGs
- `references/variable-tracking.md` — phantom/leaked/shadowed variable patterns
- `scripts/prescan.py` — static grep-level pre-scan for files on disk
