---
name: pair-capability-setup-harness
description: "Configures an agent harness (pi, opencode, Claude Code) to execute pair's process: resolves the harness explicitly (never inferred), verifies its fitness against the project's declared harness/access-path requirements before writing anything, provisions access path / skill paths / context / model provider per the harness's guide, and confirms rather than rewrites on re-run. Invoke directly to configure a harness ('configure pi for this project', 'set up opencode'). Optionally composed by /pair-process-bootstrap in its finalization phase."
version: 0.2.0
author: Foomakers
---

# /pair-capability-setup-harness — Agent Harness Configuration

Configure an agent harness so it becomes a valid environment for pair's process. Reads the [agent-harness framework](../../../.pair/knowledge/guidelines/technical-standards/ai-development/agent-harness/README.md) and `adoption/tech/automation.md`'s Harness/Model Policy declarations, verifies the requested harness is fit before touching any configuration, then provisions it. Shaped after `/pair-capability-setup-pm` and `/pair-capability-setup-gates`: read adoption → verify → provision → idempotent → HITL.

## Arguments

| Argument   | Required | Description                                                                                                   |
| ---------- | -------- | --------------------------------------------------------------------------------------------------------------- |
| `$harness` | No       | Harness to configure: `pi`, `opencode`, or `claude-code`. If omitted, the developer is asked. **Never inferred** from environment variables, present binaries, or filesystem markers — see Step 1. |

## Composed Skills

| Skill              | Type       | Required                                                              |
| ------------------ | ---------- | ---------------------------------------------------------------------- |
| `/pair-capability-record-decision` | Capability | Optional — only if provisioning surfaces a decision worth recording (e.g. a project's first `tech/automation.md` Harness declaration). Most runs provision without one. |

## Algorithm

### Step 1: Resolve the Harness — Ask, Never Infer

1. **Check**: Is `$harness` provided and one of `pi`, `opencode`, `claude-code`?
2. **Skip**: If valid, proceed to Step 2 with that harness.
3. **Act**: If `$harness` is omitted, ask the developer directly:

   > **Which harness do you want to configure?**
   >
   > | Harness | Guide |
   > | --- | --- |
   > | **pi** | [pi.md](../../../.pair/knowledge/guidelines/technical-standards/ai-development/agent-harness/pi.md) — no MCP by design |
   > | **opencode** | [opencode.md](../../../.pair/knowledge/guidelines/technical-standards/ai-development/agent-harness/opencode.md) — MCP-native, has a headless server |
   > | **claude-code** | [claude-code.md](../../../.pair/knowledge/guidelines/technical-standards/ai-development/agent-harness/claude-code.md) — `claude -p` and `Workflow` as two layers |

4. **Act**: If `$harness` is provided but unrecognized, or names a harness with no guide in the framework → **HALT**:

   > `$harness: [value]` has no guide in the agent-harness framework. Available: `pi`, `opencode`, `claude-code`. To add one: one new markdown file at `technical-standards/ai-development/agent-harness/<name>.md`, following the fixed nine-section index — zero code.

5. **Verify**: Exactly one harness resolved, by explicit argument or by direct question. **Never** by detecting a binary on `PATH`, an environment variable, or a filesystem marker — a fragile, harness-specific heuristic this skill deliberately does not implement (decision recorded during story #450's refinement).

### Step 2: Read the Project's Declared Requirements

1. **Act**: Read `adoption/tech/automation.md`. Does it exist, and does it carry a `## Harness` section (see [automation-policy.md](../../../.pair/knowledge/guidelines/collaboration/automation/automation-policy.md))?
2. **Skip** (absent file, or present with no `## Harness` heading): Zero-configuration path — every harness in the framework is presumed supported, and no declared access-path requirement exists to check against. Proceed to Step 3.
3. **Act** (present): Parse the comma-separated harness list. Is the resolved harness (Step 1) in it?
   - **Not in the list** → **HALT** before any write:

     > `$harness: [value]` is not among this project's supported harnesses (`tech/automation.md` → `## Harness` declares: [list]). Add it there first if this project should support it, or choose one of the declared harnesses.

4. **Act**: Does the `## Harness` section carry a second line, `Requires: <access-path>` (see automation-policy.md)? This is the only source of an access-path requirement — **never inferred** from the project's tooling, way-of-working, or any other file.
   - **No `Requires:` line** → nothing to check; skip to Step 3. A project that never declared a requirement has none, by construction — not an unchecked gap.
   - **`Requires:` declared, and the resolved harness cannot satisfy it** (today, the only case the framework defines: `Requires: mcp` and `pi` — which has none by design — is the one requested) → **HALT** before any write, naming the precise gap:

     > `pi` has no MCP access path (by design — see [pi.md](../../../.pair/knowledge/guidelines/technical-standards/ai-development/agent-harness/pi.md) § Access Paths), and `tech/automation.md` declares `Requires: mcp`. Either use a harness with MCP (`opencode`, `claude-code`), or resolve the requirement through pi's CLI-first path (see the [agent-harness framework](../../../.pair/knowledge/guidelines/technical-standards/ai-development/agent-harness/README.md) § CLI-First).

5. **Verify**: The resolved harness is either confirmed fit (declared and access-path-compatible, or nothing declared at all) or the skill has already HALTed — **no configuration write has happened yet** at this point, in either outcome.

### Step 3: Verify the Harness Is Actually There

1. **Act**: Check whether the resolved harness's binary/CLI is present and runnable (e.g. `pi --version`, `opencode --version`, `claude --version`) — every spawn with stdin closed (`pi -p` with an open stdin hangs, observed in #503's probe).
2. **Act** (not installed, `opencode` / `claude-code`) → **HALT**, stated as an environment fact, not a project error:

   > `[harness]` is not installed on this machine. This is an environment gap, not a configuration issue — install it first (see the harness's own install instructions; this KB describes what pair needs from it, not how to install it), then re-run.

3. **Act** (`pi` — install or verify; this branch runs standalone, for `pi` only, long after pair was installed, and is the only harness this skill ever installs):
   - `pi` absent ⇒ propose the install command from [pi.md](../../../.pair/knowledge/guidelines/technical-standards/ai-development/agent-harness/pi.md) § 9 Setup and run it only on an explicit **yes**; on no, stop with the Step 3.2 message. Nothing is installed without that yes.
   - `pi` present ⇒ read `pi --version` and compare it with the minimum pi.md § 9 states (`0.86.1`, required by `pi-subagents`' dynamic tool activation):
     - older than `0.86.1` ⇒ propose the update command from pi.md § 9 Setup (again, run only on yes); declined ⇒ continue, reporting the version as below the minimum for the in-pi cycle;
     - at or above it ⇒ **confirmed**, nothing written.
   - An install or update that fails (no network, registry refused) ⇒ report the command's own error and stop — npm installs a global package atomically, so there is no half-installed state to clean; never retry silently, never fall back to another install path.
4. **Verify**: The harness binary responds (and, for `pi`, its version was reported against the minimum). Proceed to Step 4 only once confirmed present.

### Step 3b: `pi-subagents` — Only on Request (pi only)

1. **Check**: Did the developer ask for `pi-subagents` (the package the in-pi delivery cycle dispatches its stages through)? It is set up only when the developer asks for it — never as part of a plain `pi` setup, never inferred.
2. **Skip**: Not asked ⇒ go to Step 4.
3. **Act**: Read the pin and the current install from the bridge the cycle uses, so both speak one version:

   ```bash
   node "$SKILL_DIR/../workflow-cycle/scripts/pi-bridge.mjs" pin
   node "$SKILL_DIR/../workflow-cycle/scripts/pi-bridge.mjs" probe --project "$PWD"
   ```

   - `missing` ⇒ ask **global or project-local** (never chosen silently), then propose the matching install line the probe printed (`install.user` / `install.project`) and run it only on yes. For project-local, explain the project-trust step first: pi does not load packages of an untrusted project, so the package stays inert until this project is trusted (Step 5.5).
   - `pinned` ⇒ **confirmed**, nothing written.
   - `drift` ⇒ report both versions and propose aligning to the pin with the same install line; declined ⇒ leave it, reporting the version as unverified.
   - A failed install ⇒ the command's own error, reported; nothing retried.
4. **Verify**: Re-run `probe`: `pinned` after a yes. Report the pinned version as the `verifiedAgainst` pi.md § 9 records for `pi-subagents` — the bridge's pin and that line are kept equal by a test, so this skill reads them and never edits the KB.

### Step 4: Verify Authentication — Report, Never Touch

1. **Act**: Following the resolved harness's guide § Authentication, check whether a usable credential is resolvable (an expected env var is set, or the harness's own auth-check command reports readiness — e.g. `pi auth check`, `opencode auth list`, `claude`'s own login state). **Never read, print, store, or transmit the credential's value** — check readiness only, the way the harness's own tooling reports it.
2. **Act** (no usable credential found): Report which auth path is missing and how to obtain it, quoting the guide's own § Authentication section, and state plainly whether the missing path is CI-viable (API key) or local-interactive-only (OAuth subscription — never presented as a CI option).
3. **Check**: Is authentication required to complete provisioning (Step 5), or can provisioning proceed and the auth gap be reported alongside a successful configuration?
   - Config/skill-path/context provisioning (Step 5, points 1–3) does not require a working credential — proceed with those regardless.
   - Model-provider provisioning (Step 5, point 4) requires a resolvable credential path — if none exists, report the gap and continue with the rest of provisioning; do not HALT the whole run over an auth gap that provisioning can partially complete around.
4. **Verify**: Either a usable auth path was confirmed present (existence only, never its value), or its absence was reported with an actionable next step — and in neither case did the skill touch a credential.

### Step 5: Provision

For the resolved, fitness-checked, present harness:

1. **Config file** — per the guide's § Config File Locations, confirm (or, for a genuinely new/never-configured harness, create) the project-local config file at its documented path. Never touch the global/credential files (§ Authentication).
2. **Skill paths** — per the guide's § Skill-Path Declaration: for harnesses that already discover pair's skills with no wiring (pi, opencode — confirmed in their guides), verify discovery works (the project's `.agents/skills/` or `.claude/skills/` is reachable from the harness's search paths) rather than writing anything. Only write a skill-path entry when the guide documents one as required (e.g. pointing at another harness's directory).
3. **Context** — per the guide's § Project Context Loading: nothing to provision for any of the three current harnesses (each guide's context-loading finding confirms no duplication and no reduced-variant emission is needed today). If a future harness's guide reports duplication, this step regenerates the `@<harness>-skip-*` variant via the existing content-transform pipeline — never new transform code (Business Rule 4).
4. **Model provider** — per the guide's § Model Provider Configuration and `tech/automation.md`'s `## Model Policy` (if declared): report which model class (`cheap`/`balanced`/`frontier`) applies to which `risk:*` tier, and which concrete provider/gateway configuration in the harness's own guide realizes that class today (e.g. an opencode Zen free model for `cheap`). **Never write a credential** — name the environment variable or auth command the developer runs themselves.
5. **Headless readiness (pi only, today)** — pi's guide documents a load-bearing headless/trust gate: a headless run ignores project resources unless a trust decision exists for it. If the resolved harness is `pi` and headless execution is in scope for this configuration, report this gate explicitly and offer, **in this order**:
   1. **Default: a per-directory entry in `~/.pi/agent/trust.json`, scoped to this project's canonical path only** (a trust-configuration write, not a credential — permitted) — or point at the interactive `/trust` step to write the same scoped entry.
   2. **Only if the developer explicitly asks for it**: `defaultProjectTrust: "always"` in `~/.pi/agent/settings.json` — state plainly that this trusts every project pi opens headlessly on this machine, not just this one, before writing it.
   Never silently assume a headless run will see project skills, and never default to the global setting when the scoped one solves the same problem.

### Step 6: Idempotent Re-Run

1. **Check**: Was this harness already provisioned by this skill (its config file and skill-path setup already match what Step 5 would produce)?
2. **Act** (already configured): Confirm the existing configuration rather than rewriting it — report what is already in place, matching `/pair-capability-setup-pm` and `/pair-capability-setup-gates`'s own re-run behavior.
3. **Act** (partially configured, or drifted from what the guide now documents for a newer harness version): Report the diff and ask before overwriting.
4. **Verify**: A second run on an already-configured harness produces a confirmation, never a silent rewrite.

## Output Format

```text
HARNESS CONFIGURED:
├── Harness:     [pi | opencode | claude-code]
├── Fitness:     [Declared and compatible | No tech/automation.md declaration — zero-config path]
├── Installed:   [version observed | installed on yes: <version> | declined — HALTed] (pi: vs minimum 0.86.1)
├── pi-subagents: [n/a — not requested | confirmed <version> | installed <version> (<scope>) | drift <installed> vs pinned <version> — unverified] (pi only)
├── Auth:        [Ready — <path> | Missing — <what to obtain, and CI-viability>]
├── Config:      [file written/confirmed]
├── Skills:      [already discovered — no write | path added: <entry>]
├── Context:     [no action needed | reduced variant emitted: <path>]
├── Model policy: [class → provider mapping reported | tech/automation.md has no ## Model Policy — none applied]
├── Headless:    [n/a | trust gate reported — <action>] (pi only)
└── Status:      [Configured | Already configured (unchanged) | HALTed — <reason>]
```

## HALT Conditions

- **Harness argument unrecognized or has no guide** (Step 1.4).
- **Harness not among the project's declared supported harnesses** (Step 2.3) — before any write.
- **Harness cannot satisfy a project-required access path** (Step 2.4) — before any write, e.g. MCP required and `pi` (no MCP by design) requested.
- **Harness not installed on this machine** (Step 3.2) — reported as an environment fact, not a project error; for `pi`, only after the developer declined the proposed install (Step 3.3).
- **An install the developer approved failed** (Step 3.3, Step 3b) — the command's own error, nothing retried.

None of these HALTs follow a configuration write — fitness (Step 2) and presence (Step 3) are both checked before Step 5 provisions anything. The only writes before Step 5 are the `pi` / `pi-subagents` installs the developer explicitly approved.

## Composition Interface

When composed by `/pair-process-bootstrap` (optional, finalization phase):

- **Input**: `/pair-process-bootstrap` reaches its finalization phase and offers `/pair-capability-setup-harness` alongside `/pair-capability-setup-pm`, as a **skippable** step — most projects decline and stay on the harness already in use, which needs no `tech/automation.md` declaration (the zero-configuration path, Step 2's skip branch).
- **Output**: Returns the harness name, fitness result, and configuration status. `/pair-process-bootstrap` includes any adoption changes in the next commit.

When invoked **independently**:

- Interactive: full Step 1–6 flow. Developer commits any adoption changes when satisfied.

## Edge Cases

- **Developer carries a personal global config** (e.g. `~/.pi/agent/AGENTS.md`, opencode's `~/.config/opencode/AGENTS.md`): report that it brings context the project does not control (each guide states this); this skill neither reads nor modifies it.
- **`tech/automation.md` exists but has no `## Harness`/`## Model Policy` heading**: treated identically to the file being absent (zero-configuration path) — presence of the file alone does not turn on fitness-checking; presence of the specific heading does.
- **Multiple harnesses configured over time**: each run configures exactly one harness (the resolved `$harness`); running again with a different value configures that one too — this skill does not deduplicate or reconcile across harnesses, and a project's `## Harness` list is not a limit on how many a developer configures, only on which ones the project accepts as supported.

## Graceful Degradation

See [graceful degradation](../../../.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/graceful-degradation.md) (adoption file missing → proceed with the zero-configuration path) for the standard scenarios. Additional cases:

- `tech/automation.md` missing entirely → Step 2's skip branch: every harness in the framework is presumed supported, nothing to HALT against.
- `/pair-capability-record-decision` not installed → provisioning (Step 5) still completes; only a decision record (rare — most runs need none) is skipped, with a warning.
- A harness's guide is missing a section the fixed nine-section index requires → that is a framework defect, not something this skill works around; report it and stop rather than guessing the missing section's content.

## Notes

- **Credentials never pass through this skill (the hard constraint)**: it reads readiness, never a value; it reports what is missing and how a human obtains it. Rationale: pi persists sessions as JSONL and shares them via `/share` — a token that entered a session's context is a token that can leave the machine through that channel.
- **Adding a harness is one markdown file and zero skill changes** (Business Rule 4): a new `<name>.md` guide following the fixed index is immediately resolvable by `$harness: <name>` — nothing in this file's algorithm names a harness by special case.
- This skill provisions configuration and reports readiness; it installs nothing without an explicit yes, and the only things it can install are `pi` (Step 3.3) and, on request, `pi-subagents` at the pinned version (Step 3b) — every other harness's binary is verified and HALTed on (Step 3.2). It does not perform the functional smoke run (that is the separate smoke scenario in `scripts/smoke-tests/`).
