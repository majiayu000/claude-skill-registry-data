---
name: harness-door-pattern
description: Build a Skill Heaven door for a new AI coding harness. Use when adding support for any harness (claude, pi, codex, hermes, grok, or a new one) — covers the four suppression-mechanism classes, how to probe without being lied to, the door package shape, and the traps that have already cost time.
---

# The Harness Door Pattern

A **door** boots a harness into a chosen posture. Five have been built. The work is the same
shape every time, and most of the cost is in the probe, not the code.

This skill exists so door six is cheap.

---

## The core insight

**Every harness hides its skills somewhere different, but there are only about four places.**
Identify which class you are dealing with and you have most of the answer. Guess wrong and you
will burn a probe campaign proving a flag does nothing.

### Class 1 — Allowlist flags that read like suppression flags

The flag takes a list of scopes to **load**. Naming a scope *keeps it alive*. The instinct to
"name the thing you want to suppress" is exactly backwards, and it looks correct in a diff.

| harness | flag | the trap |
|---|---|---|
| claude | `--setting-sources` | naming `project` **keeps** project-scope skills. Empty string is the suppression. |
| hermes | `--toolsets` | naming a set that omits `skills` is what drops the skill index. |

This class has bitten twice in this repo — KC4 on `curated`, then P8 on `product-floor` (#24),
which shipped with the same defect for a month because the fix was applied to one posture and
not its sibling. **When you fix an allowlist, grep for every other posture using the same flag.**

### Class 2 — Native evict / readmit

The harness has a real primitive: one flag clears skills, another admits specific ones. Cleanest
class to build against; a curated posture falls out almost for free.

| harness | evict | readmit |
|---|---|---|
| pi | `--no-skills` | `--skill <path>` (repeatable, takes a **path**) |

### Class 3 — Config-home scoping

An env var relocates the harness's whole config root. Point it at the session dir and the
harness sees an empty world.

| harness | var |
|---|---|
| codex | `CODEX_HOME` |
| hermes | `HERMES_HOME` |
| grok | `GROK_HOME` |

**The auth trap — this has cost time on every harness in this class.** A scoped config home has
no credentials, so the session cannot authenticate and every probe fails in a way that looks
like the suppression broke. Copy `auth.json` (or equivalent) in via an `fsPlan`
`copyFileIfExists` before concluding anything. `compileCodex()` is the reference.

### Class 4 — Skills seeded onto disk

The skills are **already files** in the profile before the session starts. **No runtime flag can
remove a file.** Flags that claim to suppress "preloaded skills" will not, because by the time
the process starts there is nothing to preload — there is only a directory.

| harness | what is on disk | lever |
|---|---|---|
| hermes | 108 bundled skills seeded into the profile | `.no-bundled-skills` marker in `HERMES_HOME`, or omit the `skills` toolset entirely |
| grok | reads the **`.claude` project and user skill dirs** | `GROK_HOME` for user scope; project scope follows the cwd |

Class 4 is the one that wastes a campaign, because the flags *look* right and the docs *say*
they work. If suppression flags do nothing, stop probing flags and go look at the filesystem.

**Grok's case generalises further:** a harness may read *another* harness's skill directories.
Do not assume a harness only loads its own.

---

## Probing without being lied to

### Never trust self-report

Asking a model to list its skills **confabulates**. Proven on pi: identical argv, different
answers across runs, including skill names that appear nowhere in the real listing. A model that
has genuinely lost its skills will often invent a plausible list rather than say NONE.

**A free-text self-report is not evidence.** It is fine as a smoke test; it may never be the
load-bearing measurement.

### Hard signals, in order of preference

1. **A disk-enumerating subcommand.** `grok inspect` reports what the harness discovers from
   disk, with sources. Best possible instrument — look for one first.
2. **A cache or snapshot file.** Hermes writes `.skills_prompt_snapshot.json`; counting its
   entries gave exactly the 108 the CLI reported.
3. **Token counts.** pi's `--mode json` emits a real `usage` object. `totalTokens` is stable
   across repeats of the same argv even when the input/cache split is not. Baseline 11,271 →
   `--no-skills` 4,371 is unarguable.
4. **A canary skill.** Place a skill containing a unique marker string, then ask for the marker.
   A model can invent a skill *name*; it cannot invent `HERMES_PATH_SKILL_LOADED`. This proved
   Hermes admits skill directories placed into a scoped home — the technique that turned a
   "cannot do curated" into "can do curated".

### Discipline

- **Run every cell at least twice** and report whether repeats agreed. Disagreement is itself a
  finding (pi showed an intermittent discovery race that way).
- **Hold reasoning effort constant.** `--thinking` / `model_reasoning_effort` / `--reasoning` are
  **model-scoped** dials and are NOT the Skill Heaven ladder, which is skill- and
  context-scoped. They share level names by coincidence. Reasoning is a control variable; varying
  it across arms makes the comparison meaningless.
- **Use one cheap model throughout.** Probes are about the harness, not the model.
- **Run every harness invocation in a herdr pane** (Rule 0) with the argv on screen.
- **Commit `PROBE.md` before any door code.** It is the evidence that licenses the route.

### Read the source, not the docs

Hermes' `--ignore-rules` help text claims it skips "preloaded skills". It does not — it maps only
to `skip_context_files` and `skip_memory`, and never touches toolsets. **The documentation was
wrong about the implementation**, and no amount of flag-probing would have revealed why.

When a documented flag does not do what it says, **go read the source.** Most of these harnesses
ship their own code locally (`~/.hermes/hermes-agent`, `~/.grok/docs`). One grep beats an hour of
black-box probing. Web search over the harness's repo works too and has been called out by the
founder as a gold mine for exactly this class of problem.

---

## The door package shape

Identical across `pi-zero`, `codex-zero`, `hermes-zero`, `grok-zero`. Copy the nearest
existing door rather than starting fresh — pick by mechanism class, not alphabetically.

```
packages/<name>-heaven/
  package.json          name, bin entry, launch script
  bin/<name>-heaven.mjs  tsx shim
  src/launcher.ts       planLaunch()
  src/cli.ts            flag parsing, --print, exec
  PROBE.md              the evidence
```

`src/cli.ts` supports: `--posture floor|product-floor|curated|native`,
`--level off|low|med` (`med` maps to native; the summon-line rungs
`high|xhigh|max|ultra` route users to `/skill-hell <rung>` or `/skill-ultra` —
a redirect, never a gate, and **match an existing door's wording and exit code
exactly**), `--skill <path>` repeatable, `--model`, `--print`, and `--`
passthrough.

The compile route goes in `packages/core/src/compile.ts`: add the harness to `HARNESSES`, add a
`compile<Name>()` case to the switch, and return `execSupport: "exec"` **only if your probe
licenses it**. `"recipe"` — emit a plan, never spawn — is an honest, acceptable outcome and is
where codex-zero sat for weeks.

### Posture definitions

- **`floor`** — doorless absolute zero, the benchmark placebo-of-record. Internal ruler, **never
  product vocabulary**. For a new harness you are *defining* this, so define it as everything
  your probe shows actually suppresses.
- **`product-floor`** — the nearest zero a user can actually launch at, door still reachable.
  This is what `off` means to a user.
- **`curated`** — suppress everything, then readmit exactly the named skills.
- **`native`** — untouched.

Price the two floors **separately and never average them**. The gap between them *is* the door's
cost (claude +515 tok; pi ~1,762 tok).

---

## Traps, each of which has already cost time

1. **Naming a scope in an allowlist keeps it.** Class 1. Cost: two separate incidents.
2. **A scoped config home cannot authenticate.** Class 3. Copy `auth.json` first.
3. **Flags cannot delete files.** Class 4. Check the filesystem before probing flags harder.
4. **Self-report confabulates.** Use a hard signal.
5. **Docs can be wrong about their own implementation.** Read the source.
6. **A harness may read another harness's skill dirs.** Grok reads `.claude`.
7. **`herdr pane run` splits argv** and destroys quoted prompts. Use `pane send-text` with a
   trailing newline inside the quotes.
8. **A prompt to a freshly-started `pi` agent can be swallowed by its startup banner.** Use
   `herdr agent prompt … --wait --until working --timeout 60000` and verify it started.
9. **Never claim a harness limitation when you have only shown an account limitation.** A
   free-tier account is not the harness.

---

## Honest disclosure

Non-negotiable in this repo.

- Never state a token dose you did not measure.
- A negative result is a **first-class finding** (D8). Record it plainly; never paper over it.
- Never overwrite an earlier negative finding when a later probe succeeds — **append**. The
  record of why the obvious approach failed is worth as much as the approach that worked.
- If a later fix invalidates earlier numbers, say so explicitly rather than leaving stale figures
  in place.
