---
name: maw-reason
description: |
  Expensive, human-invoked adversarial deliberation over a QUESTION (not a task). Runs a five-role chain — premise check, generator, compressor, attacker, synthesizer — as real isolated spawns, and returns a synthesis with an explicit disagreement ledger and what-would-change-my-mind.
  Use when the cost of being wrong is high and genuine uncertainty exists: architecture forks, irreversible migrations, "should we X or Y" with real stakes. Do NOT use for lookups, trivia, or questions a single careful answer settles — it costs roughly 200-350k tokens and several minutes.
  Supports flags: --fast (lower compressor/attacker/synthesizer effort for speed, at the cost of a thinner attack surface), --keep (persist the trace for audit), --passes N (extra attack passes, default 1), --high-assurance (dual independent generators on distinct profiles, +1 spawn), --seed N (reproduce a previous run's role assignment), --force-premise (run the full chain even if the premise check flags the question).
  Model-invocation is guarded: if the model reaches for this rather than the user typing it, the auto-invoke guard applies — the human sees the question, profile, and cost estimate and confirms before anything spawns.
---

# MAW Reason — adversarial deliberation as a chain, not a performance

This skill answers a **question**. It does not create tasks, branches, worktrees, or commits, and it never moves anything on the task board.

## The one invariant that makes this worth its cost

**The calling session must not author the chain's prompts.**

The caller has an opinion. It formed one the moment it read the question. If the same agent writes the question, picks which facts are "relevant", and composes the generator prompt, then every downstream role inherits the caller's frame and the chain degenerates into an expensive way to agree with yourself. The review that gated this design named it the blocking defect: the sealer already knows the sealed value and controls the only channel.

So the work is split across a trust boundary:

- **The calling session (you, right now)** does exactly four things: capture the human's input verbatim into files, resolve profiles, spawn the coordinator, relay the result. It writes no role prompt and reads no role artifact until the synthesis exists.
- **The coordinator** — a fresh agent with no view of the calling conversation — builds every downstream prompt from the installed role bodies plus the verbatim input files, runs the roles as **real isolated spawns**, validates their artifacts, and produces the synthesis.

Call this what it is: an **auditable exclusion protocol**, not a mechanical seal — and be precise about how much it actually excludes, because the honest boundary is narrower than the framing suggests.

**What it closes:** the caller does not compose the role prompts. The chain's questions to the generator, compressor, attacker, and synthesizer are built by an agent that never saw the calling conversation.

**What it does not close**, and no prompt can:

- The caller still authors `FACTS.md` and `CONSTRAINTS.md` and chooses which paths the allowlist grants. Omitting a contrary path, or restating a conclusion as a "fact", contaminates the chain through a channel no downstream role can detect. This matters most on the model-chosen path, where a human never sees those fields — so the guard confirmation shows the **question, facts, and constraints**, not just the question.
- The coordinator is an LLM told to route `CALLER_POSITION.md` to the attacker only. Nothing enforces it. To make a deviation *visible* rather than merely forbidden, the coordinator records the file list and prompt hash it fed each role in `SPAWNS.jsonl` — a generator line listing `CALLER_POSITION.md` is then evidence, not speculation. That is auditability after the fact, not prevention.
- The coordinator is a Claude Code subagent and therefore carries this project's ambient instructions. It is fresh from the *conversation*, not context-sterile. Only the external role spawns get real isolation (`--setting-sources ""`).

So the invariant is "the opinionated caller does not write the chain's prompts", not "the chain is uncontaminated". Claiming the second would be the same overreach the chain exists to catch.

**Roles are spawned, never simulated.** Writing all five role outputs yourself in one context, however faithfully, is not a cheaper version of this chain — it is the failure mode the chain exists to prevent. A simulated run and a real one look identical in the output text and differ completely in worth. If spawning is unavailable, the honest move is to say so and stop, not to role-play the chain.

## Scope of v1

- **Host:** Claude Code only — this skill is not installed on the `.agents/` surface, so the orchestrating session is always Claude Code. **Roles are not** restricted that way: any role can resolve to `codex` and run through `codex exec`, which is how a conforming independence profile is reached at all. Host and role providers are different questions; only the first is pinned in v1.
- **Depth:** exactly 1, enforced two ways. Role spawns run with `--setting-sources ""`, so they load no project settings and therefore no skills — a role **cannot** invoke this skill even if it decides to. The coordinator can (it keeps the `Skill` tool), so it is stopped by the file marker in Step 1 instead. Note that a subagent never has the Task tool at all — Claude Code strips `Agent` from every subagent — which is why the chain runs through the external runner rather than nested subagents.
- **No code changes.** No role may edit a file in the repo. Roles read the repo and write exactly one artifact each into the run directory.

## The chain

```
QUESTION.md (verbatim)
  → PREMISE CHECK      is the question well-posed? loaded? falsely dichotomous?
  → GENERATOR          position paper with stable claim IDs
  → COMPRESSOR         non-author claim map: load-bearing flags + proposed attack_vector
  → ATTACKER           works the vector as a FLOOR + mandatory off-vector scan
  → SYNTHESIZER        answer + confidence + disagreement ledger + what-would-change-my-mind
```

Five spawns. The Compressor is not optional decoration: without a non-author deciding what is load-bearing, the Attacker picks its own exemption surface and the chain grades its own homework.

`--high-assurance` adds a second independent Generator (six spawns) whose paper the Compressor must reconcile across branches. There is no separate `generator-b` role: the second generator runs the **same `generator.md` body** under a **different resolved profile**, writing `POSITION_B.md`. If no second distinct profile is available, `--high-assurance` is refused — running one profile twice produces two correlated papers and calling them independent is the failure the flag exists to avoid.

## Profiles and effort

Profiles resolve through the same machinery as `maw-execute-task` — `maw/settings.json` (schema v2), `providers`, `agents`, the capability catalog, and the Step 0.65-style preflight. Role names for `settings.agents.<name>` are the file stems: `premise-check`, `generator`, `compressor`, `attacker`, `synthesizer`, `coordinator`.

There is no `task.md` here, so the per-task override layer of the pipeline does not exist. Resolution is: `settings.agents.<stem>` → `providers.<p>.default_*` → `default_provider` → host. The profile sets effort **only where settings did not**: an explicit `settings.agents.attacker.effort` wins over the profile table, because an explicit value is a decision and a profile is a default.

**Zero-config behaviour, stated plainly:** with `default_provider: "host"` every role resolves to claude, which is `reduced-independence` — and that now requires approval on every run. To get cross-provider deliberation, put a second provider in the pool:

```json
{ "default_provider": "host",
  "providers": { "codex": { "default_model": "gpt-6.1-sol" } } }
```

Note what this does *not* say: which role goes to which provider. That is the seed's job.

### Seeded role assignment

Whoever decides that the generator is claude and the attacker is codex has quietly decided what the chain's blind spot will be — and if that decision is a standing preference, the blind spot is the same on every run and therefore invisible. So the assignment is drawn, not chosen.

- **Step 1 draws a 32-bit `seed`** from the OS entropy source (POSIX: `od -An -N4 -tu4 < /dev/urandom`; PowerShell: `Get-Random`) and records it in `RUN.json`. Never ask a model to "pick randomly" — that yields preferences with a random-sounding label.
- **Explicit pins are not drawn.** A role with `provider` set in `settings.agents.<stem>` is a decision the human made and it stands. The draw only distributes roles that resolved by inheritance.
- **With two or more providers in the pool**, `seed mod 2` decides the orientation: whether the generator gets provider A and the compressor/attacker get B, or the reverse. Both orientations are conforming, and they fail differently — which is the entire point of drawing rather than settling.
- **Extra passes** consume successive bits of the same seed for compressor rotation, so the rotation requirement is satisfied by construction rather than by the coordinator's judgment.
- `--seed <n>` reproduces a previous run exactly. The seed is printed in the synthesis, so "run it again the other way" and "run it again identically" are both available, and a reader can tell which orientation produced the answer they are holding.

With one provider there is nothing to draw: the run is `reduced-independence` and needs approval regardless of the seed.

### Two effort profiles

Latency compounds across five sequential spawns, so speed is a real axis — but not every role can be cheapened without changing what the chain *is*. Two named profiles, and the synthesis always prints which one ran:

| Role | `deep` (default) | `fast` (`--fast`) |
|---|---|---|
| premise-check | low | low |
| generator | medium | low |
| compressor | **medium** | low |
| attacker | **high** | **medium** |
| synthesizer | **medium** | low |

**`fast` has a named weak link, and it is not the attacker.** The compressor decides which claims are load-bearing and what the attacker is pointed at; the synthesizer decides what the attack established. Those are adjudication tasks, not formatting — the compressor body itself calls the role "the first adversarial act". At `low` they are done thinly, which means a `fast` run can miss a problem by *never aiming at it*, and no amount of attacker effort recovers a target that was never selected.

So `deep` is the default, and `fast` is a shortcut taken knowingly. An earlier revision had this backwards: it argued in this very section that `--deep` was the honest default for the questions this skill is *for*, and then shipped `fast` as the default anyway. If latency matters more than depth for a particular question, that is a legitimate call — but it should be the one you have to type.

Per-role `Effort:` in settings still overrides both profiles. Whatever runs, the synthesis prints it: a `low` attacker's silence is much weaker evidence than a `high` attacker's silence, and the reader cannot calibrate without knowing which happened.

**The two providers do not respond to effort the same way** (measured 2026-07-28 on one reasoning-heavy task, single sample per level):

| | low | high | xhigh | max |
|---|---|---|---|---|
| claude `sonnet`, output tokens | 218 | — | — | 1034 |
| codex `gpt-5.6-sol`, reasoning tokens | 510 | 516 | 1552 | — |

Read that table as a **smoke test, not a response curve**. One task, one draw per level, and the two rows count different things — claude's figure is total output tokens (reasoning is not itemised there), codex's is the itemised reasoning field. They are not directly comparable, and a single sample cannot distinguish a flat band from ordinary variance.

What it does establish: effort reaches both transports. The flags are accepted, codex rejects an invalid effort value outright rather than ignoring it, and claude's output volume moves by nearly 5× between the extremes. What it *suggests*, pending repeated measurement: `gpt-5.6-sol` may be flat across low→high and only step up at `xhigh`, which would mean **the `fast`/`deep` split barely moves a codex role**. If that matters for your run, set the codex role's effort to `xhigh` explicitly rather than trusting the profile.

This also bears on a claim from the first live run, whose synthesis reported `attacker: medium requested (not enforced — ran at provider default)`. That was inference — the synthesizer cannot see the transport. But the retraction has its own limit worth stating plainly: measuring that the **flag works in isolation** does not establish that the **coordinator actually passed it** during that run, and nothing in that run's ledger records the argv. Both the claim and its retraction are unproven for that specific run; only the general capability is measured.

**Independence.** A conforming run puts the Generator on a different provider than the Compressor/Attacker, with all three execution profiles distinct. The coordinator **verifies** this against the resolved profile table rather than trusting the label it was handed — a caller that passes three same-provider profiles and the word `conforming` must not get a conforming claim in the output.

When only one provider is available the run is a named **`reduced-independence`** profile, and that downgrade needs **explicit human approval before the first spawn** — invoking the command authorizes a deliberation, not a topology the user has not been shown. Declined, the run stops. Approved, the synthesis says so prominently and makes no cross-provider claim. Never substitute silently.

## Cost

**200–350k tokens** for the five-spawn default and **240–420k** for `--high-assurance`, several minutes either way. These are the concept review's figures, derived from this repo's own per-spawn prose, and they stand until real traces replace them.

It is tempting to advertise less for `fast` on the reasoning that low effort spends fewer reasoning tokens. That is directionally true and it is not evidence — input tokens dominate here and do not shrink with effort. An earlier revision of this file did exactly that and quietly published a 120–250k range with nothing behind it. Measure first, then narrow the range.

Report deliberation spawns, retries, and host overhead separately rather than as one grand total, and never sum tokens across providers.

---

# Step 0 — Invocation and guard

**Human-typed** (`/maw-reason "<question>"`): the human is the authorization. Proceed to Step 1.

**Model-chosen:** the auto-invoke guard applies. Read `maw/settings.json` → `auto_invoke_guard["maw-reason"]`:

- absent or `true` (default) — present the question you would delegate **verbatim as you would send it**, plus the exact `FACTS.md` and `CONSTRAINTS.md` you would write, the resolved profiles, and the cost estimate; get explicit confirmation before anything spawns. Showing all three authored fields is the point: a slanted question is the obvious laundering channel, but a curated fact list and a conclusion dressed as a constraint work just as well and are easier to miss.
- `false` — unattended invocation allowed, subject to **one auto-run per session** and a visible preflight disclosure (providers, data transfer, cost range). A token ceiling applies only if `maw/settings.json` defines `reason_budget_tokens`; without that key there is no enforceable ceiling, so say plainly that the run is uncapped rather than implying a limit that does not exist. Retries and probes count against a ceiling when one is set. A prompt-level budget is advisory: usage is known only after a spawn returns, so the honest guarantee is "stop before the next spawn once the ceiling is passed", not "never exceed it".
- `"never"` — decline model invocation and tell the user they can type the command.

# Step 1 — Capture verbatim (the trust boundary)

Create the run directory **under the user's home, not in the OS temp tree**:

- POSIX: `RUN_DIR="$HOME/.maw/reason-runs/maw-reason-$(date +%s)-$$"; mkdir -p "$RUN_DIR"`
- PowerShell: `$RunDir = Join-Path $env:USERPROFILE ".maw\reason-runs\maw-reason-$([System.IO.Path]::GetRandomFileName())"; New-Item -ItemType Directory -Force $RunDir`

**The location is load-bearing, not a preference.** Measured on this machine: a role granted `--add-dir` to one subdirectory can still read anything else under the OS temp tree, grant or no grant, while the same layout outside temp refuses the read. Putting the run dir in temp silently voids the per-role input scoping — which is exactly how the first live run's compressor read `CALLER_POSITION.md` it was never given. Traces stay ephemeral by being deleted at the end (Step 4), not by living in temp.

Write a pointer at `maw/.reason-last-run` containing the absolute run path (one line). This is what the optional gate hook reads; add it to `.gitignore` if `maw/` is tracked.

**Depth guard — check before writing anything.** If `maw/.reason-active` already exists, a chain is already running and you are a nested invocation: stop and report, do not create a run dir. Otherwise write the marker, and delete it in Step 4 or Step 5 on every exit path including failure. A stale marker from a crashed run blocks the surface until removed, which is the safe direction — tell the user the file and the run it names rather than silently deleting it yourself.

The marker carries **two** lines, and the second one matters more than it looks:

```
maw-reason-<id>
session=<the value of $CLAUDE_CODE_SESSION_ID>
```

The obligation to finish a chain belongs to the session that started it, but the marker file is project-wide. Without the `session=` line the gate hook blocks the turn of **every** Claude Code session working in that repo — observed live: a second session, doing unrelated work in the same project, could not end its turn because a chain was running in the first one. The hook fails open when the line is absent, so omitting it silently disables enforcement rather than breaking other people's sessions.

Then write these files. **Verbatim means verbatim** — you are a scribe here, not an editor:

| File | Content | Rule |
|---|---|---|
| `QUESTION.md` | the human's question, character for character | no rephrasing, no "clarifying", no splitting into sub-questions, no appending your reading of it |
| `FACTS.md` | the fact/path allowlist the human supplied | paths and stated facts only; if the human gave none, write `(none supplied)` — do not go find some |
| `CONSTRAINTS.md` | stated constraints (budget, deadline, must-keep, must-not) | only what the human said is a constraint |
| `CALLER_POSITION.md` | your own tentative answer, if you have one | see below |

**`CALLER_POSITION.md` is exposed to the Attacker only.** The Premise Check, Generator, and Compressor never see it. This is not to protect your position — it is so the Attacker can treat it as one more position to attack. If you have a view, write it here honestly and completely; smuggling it into `QUESTION.md` or curating `FACTS.md` to support it is the exact failure this structure exists to catch, and it will be visible in the trace. If you have no view, write `(none)`.

Record the SHA-256 of each input file in `INPUTS.sha256`, and write a **run manifest** `RUN.json` naming what this run is supposed to be:

```json
{ "run_id": "...", "profile": "fast|deep", "passes": 1, "high_assurance": false,
  "seed": 2751937183, "seed_source": "urandom|--seed",
  "independence": "conforming|reduced-independence",
  "expected_spawns": 5, "expected_artifacts": ["PREMISE.md","POSITION.md","CLAIM_MAP.md","ATTACK.md","SYNTHESIS.md"] }
```

`expected_spawns` is 5 for the default, 6 with `--high-assurance`, plus 2 per extra pass. The manifest is what lets the gate hook check the topology you actually asked for instead of assuming the default — without it, a five-spawn run passes as a claimed high-assurance one.

**Then stop touching the run.** From here until the synthesis exists, you do not write prompts, do not read role artifacts, and do not "help" a role along.

# Step 2 — Preflight

Same shape as the orchestrator's Step 0.65, scoped to the providers this run will actually use: binary present, authenticated, and one transport+isolation probe through the full external-runner path.

**The probe must write its canary into `RUN_DIR`, through the same `--add-dir` grant the real roles get.** This is the whole point of the probe here: `claude -p` runs with cwd at the repo and `acceptEdits`, which authorizes writes in cwd and additional directories only — a child asked to write to an un-granted temp path is refused with "I don't have permission to write outside the project directory" (verified live). A canary that writes inside the workspace instead would pass while every real role fails on a different target, which is exactly how a probe manufactures false confidence.

A failed preflight means the chain does not start — report and stop, after deleting `maw/.reason-active`, the pointer file, and the run dir. Leaving an artifact-less run dir behind makes the gate hook block the very turn that reports the failure.

Disclose once, before the first spawn: which providers will see the question and any repo content the allowlist grants, under which auth mode. For a private repo this is a transfer to a second processor and the disclosure must say so.

# Step 3 — Spawn the coordinator

Spawn `maw-coordinator-<effort>` via the Task tool with a **fixed launch prompt**. Fixed means: paths and flags, nothing about the question and nothing about what you think.

```
You are the MAW Reason coordinator. Run dir: {RUN_DIR_ABS}. Repo root: {REPO_ROOT_ABS}.
Profile table: {resolved profiles, one line per role: stem provider model effort}.
Run manifest: {RUN_DIR_ABS}/RUN.json  (flags and expected topology live there, not here)
Installed role bodies: {SKILL_DIR}/agents/<stem>.md
Read your instructions from your own body. Do not ask the calling session for anything.
```

**Do not include the question in this prompt.** The coordinator reads `QUESTION.md` itself. If you paste the question here you have re-opened the channel this whole design closes.

The independence label in `RUN.json` is a **claim, not a fact**: the coordinator re-derives it from the profile table and overwrites it if it does not hold. You cannot label a same-provider run `conforming` and have it print that way.

# Step 3.5 — The premise halt

If the coordinator returns with `HALTED.md` instead of a synthesis, the premise check found the question itself mis-posed and stopped the chain after one spawn. Relay it to the human and ask which they want:

1. **Proceed anyway** on the original question — re-launch with `--force-premise`; the chain skips the halt and runs all five roles. The synthesis carries the `QUESTION SUSPECT` verdict prominently, because an answer to a question somebody flagged as mis-posed needs to be read with that attached.
2. **Restart** with a reworded question — a new run with a new `RUN.json` and a new seed. The reframing is a **proposal**: the human writes the new question, not you and not the premise role.
3. **Drop it.**

Do not pick for them, and do not quietly adopt the reframing — silently answering a better question than the one asked is the failure this whole gate exists to prevent. Delete `maw/.reason-active` before handing back; keep the run dir so the halt is auditable, and say where it is.

# Step 4 — Relay

When the coordinator returns, read **only** `SYNTHESIS.md` and relay it. Present it as the chain's output, not as your own conclusion, and preserve:

- the answer and its confidence,
- the **disagreement ledger** — unresolved conflicts stay unresolved in your relay; flattening them into a clean recommendation is the one thing that destroys the artifact's value,
- what-would-change-my-mind,
- the independence profile and the efforts that ran.

If you disagree with the synthesis, say so **as a separate, labelled opinion after it**. Do not edit the synthesis to match your view.

Delete `maw/.reason-active` — on this path and on every failure path. If `--keep` was passed, copy the run dir to `maw/reasoning/{RUN_ID}/` and tell the user the path. Otherwise delete the run dir and leave the pointer file naming a path that no longer exists — that is the expected end state, not an error. Benchmark export is a **separate, explicitly consented action**, never a side effect of `--keep`.

# Step 5 — Failure

The chain fails loudly and never partially. If a role spawn fails twice, or an artifact fails its contract, the coordinator writes `CHAIN_FAILURE.md` (role, resolved profile, failure class, stderr tail) and stops. Relay that verbatim.

A failed chain produces **no answer**. Do not fill the gap with your own reasoning presented as the chain's output — that is the simulation failure mode arriving through the back door. Say the chain failed, say why, and offer to answer directly as yourself if the user wants that.

Delete `maw/.reason-active` here too. A failed run that leaves the marker behind locks the surface for every later invocation. Keep the run dir on failure regardless of `--keep` — it is the only evidence of what went wrong — and name its path in the report.

## Role artifact contracts

Checked by the coordinator as each spawn returns. Fresh = created by this spawn.

| Stem | Artifact | Contract |
|---|---|---|
| premise-check | `PREMISE.md` | fresh, non-empty; verdict `QUESTION WELL-POSED` or `QUESTION SUSPECT` |
| generator | `POSITION.md` (`POSITION_B.md` for the second generator) | fresh, non-empty; every claim carries a stable ID `C-<n>` |
| compressor | `CLAIM_MAP.md` | fresh, non-empty; contains `attack_vector:` with at least one target claim ID |
| attacker | `ATTACK.md` | fresh, non-empty; covers every vector target; contains an off-vector line (a finding or exactly `NO_OFF_VECTOR_FINDING`) |
| synthesizer | `SYNTHESIS.md` | fresh, non-empty; contains `Answer:`, `Confidence:`, `## Disagreement ledger`, `## What would change my mind` |

## Optional enforcement hook

`hooks/maw-reason-gate.sh` (installed with `--with-hooks`) is a `Stop` hook. It reads `maw/.reason-last-run` and, when a run is active, verifies that all five artifacts exist, are newer than `QUESTION.md`, and that the spawn ledger records real external spawns. Missing or stale artifacts → `decision: "block"` with the reason, and the turn cannot end.

The hook does not make the chain honest. It makes a dishonest chain **fail visibly** instead of reading like an honest one — which, for a surface whose only output is prose, is the difference that matters.
