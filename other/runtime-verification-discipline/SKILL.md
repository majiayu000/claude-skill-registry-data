---
name: runtime-verification-discipline
version: "1.2.0"
user-invocable: false
description: "Hard discipline for runtime verification in PDCA workflows: the AI executes verification itself in an environment — real preferred over simulated, subject to determinism + safety — never defaulting to a human checklist. Attempt-first, resolve a pluggable provider (project script/skill → shared capability skill), and hand to a human only at a true hard boundary with a stated reason. Use at any workflow verify/check stage (bug fix or feature) to decide WHERE verification runs, WHO runs it, WHETHER it suffices. Referenced by PDCA hosts via frontmatter dependencies. Triggers — 「环境验证」「真实环境验证」「真机验证」「真机测试」「模拟环境验证」「AI 验证」「验证分层」「验证充分性」 / runtime verification, environment verification, real vs simulated. When a check opens a UI, cite a saved non-empty screenshot; non-UI checks do not. Do NOT alias completion-evidence-discipline (evidence freshness) or runtime-evidence-debug (debug instrumentation)."
---

# Runtime Verification Discipline

> Internal shared skill. Single source of truth for **how verification gets executed** in PDCA workflows: the AI runs verification itself, in the right environment, and only hands to a human at a genuine hard boundary. Hosts declare it in `dependencies` and abort if missing — no silent fallback.
>
> This is the **rule layer**. It decides *where* verification runs, *who* runs it, and *whether it is sufficient*. It does **not** contain environment-driving recipes (channel selection, CDP calls) — those live in capability skills such as `browser-debug-toolkit`. Concrete examples and per-host integration snippets are in [reference.md](reference.md).

## Why this skill exists

Workflows used to treat verification as "AI runs Bash test commands; everything else is handed to the user as a checklist." That posture wastes the AI's ability to drive real and simulated environments, and it turns "hand to the user" into an unexamined default — sometimes used because the AI did not try, not because it genuinely could not. The result is avoidable manual verification labor and, worse, occasional false confidence when a low-fidelity check is reported as if it were conclusive.

The meta-lesson this skill enforces:

> **Verification is the AI's job, done in an environment. Prefer the highest-fidelity environment the AI can drive safely and deterministically; hand to a human only at a true hard boundary, and say exactly why.**

## When this applies

At any workflow's verify/check stage, for any change with observable behavior — bug fix or feature development alike. If nothing about the change can be exercised in any environment, this skill does not apply (a pure docs/comment change may need no runtime verification).

## Iron law

**VERIFICATION IS EXECUTED BY THE AI IN AN ENVIRONMENT, NOT DELEGATED TO THE HUMAN AS A CHECKLIST.**

Attempt execution first — that is the default, not an option. Only a classified true hard boundary justifies handing a step to a human, and the reason must be stated.

## Environment tier model

Classify an environment by how faithfully it matches the app's **production runtime target**. "Real" vs "simulated" is relative to that target, not absolute:

| Production target | Real environment | Simulated environment |
|-------------------|------------------|------------------------|
| Web app | A real browser (CDP-driven, e.g. ego-browser / chrome-devtools-mcp) | Headless DOM / jsdom-style fake DOM |
| Electron app | The Electron application itself | A plain browser |
| Mobile app | A physical device | An emulator / simulator / browser |

A bug that is platform-specific can only be conclusively verified at the tier where that platform's runtime actually executes.

## Tier selection rule

Choose the **highest-fidelity tier that the AI can drive with zero human intervention AND that is sufficiently deterministic and safe for the assertion being made**. Fidelity is traded against confidence-per-cost, not maximized blindly:

- **Determinism** — a real environment carries real network and timing, so it is flakier. When you need a stable, re-runnable signal, verify in simulation first.
- **Safety / side effects** — a real environment can mutate real backends, real user data, or send real pushes. For a verification that writes, simulate first (sandbox) and confirm in the real environment after.
- **Fidelity by bug class** — a platform-specific bug needs the tier where that platform runs; a platform-agnostic logic bug does not.

So: **read-only, highly deterministic check → real environment directly. Write-involving or flaky-prone check → simulate first for a stable signal, then confirm in the real environment, and label both.**

## Provider resolution (pluggable)

Resolve *how* to verify in this project's environment by lookup, in order — convention over configuration:

1. **The project's own verification script or skill** — preferred. Projects SHOULD expose verification through a discoverable convention (e.g. a known-location verify script or a project skill) so the AI can find it without being told.
2. **A shared capability skill** from this library (e.g. `browser-debug-toolkit` for web, `android-webview-debug` for Android WebView) — the fallback.
3. **Neither exists** — proceed to the handoff classification below.

## Attempt-first, then classify the blocker (A/B/C)

When the AI cannot execute a verification, classify why before doing anything else:

- **A — unwired automation.** The check is automatable but no script exists yet. Wire it (write the script) or offer to wire it. Do **not** hand it off.
- **B — missing one-time setup.** The check is automatable but a toolchain/environment is not installed. Give the exact install/setup command and let the user decide; once set up, the AI takes over.
- **C — true hard boundary.** Hand to the human, and state the reason. C has three kinds: the AI **cannot act** (physical device, captcha, biometrics), the AI **cannot judge the result** (subjective UX, exploratory assessment), or the action has **real-world side effects**.

Never use a vague "no Bash / environment limits" hand-wave to hand off without classifying. The classification is what keeps "minimize human labor" honest — it forces the distinction between "I didn't wire it" and "it genuinely cannot be automated."

**Pixel geometry is not category C.** A numeric comparison of laid-out frames to a design spec is not subjective UX, and it is not a physical-device step when a document channel or a layout probe can run. A missing probe is category A: write and run the probe in this turn, mounted in the shipping parent. Category C "physical device" stays for an action no command can perform. A lower-tier label ("real-environment smoke recommended") does not turn those rows into a human step and does not replace the measurement.

**An opened UI keeps a screenshot file.** When a check opened a UI, the evidence cites a path to a non-empty png, jpg, jpeg, or webp saved this run. Unit tests, spec validation, and a layout probe that only prints numbers and cannot open a UI do not require an image and must not invent one. The image does not replace that check's own pass condition. Do not restate a Figma report's channel names here. Before an opened-UI image supports the check, inspect it per `completion-evidence-discipline`. This look is not category C.

## Sufficiency check

Verification is sufficient only if it exercises the change's **exact behavior the way the software is really used**. The bar is not "the app boots" but "the fixed bug's specific symptom is gone on the real usage path" or "the new feature's real usage path works." If the assertion does not cover the changed behavior, the verification is insufficient regardless of which environment ran it.

## UI verification face precheck

Before verifying, decide whether the verification face includes UI behavior. Two command outputs decide it. Wording in the goal, task card, or fix description is not an input.

The change set is the tracked diff plus every untracked, non-ignored path. Run from `git rev-parse --show-toplevel`. Untracked paths are `git ls-files --others --exclude-standard`. An empty tracked diff does not drop those paths.

Resolve one base, in order:

1. `origin/HEAD`, when `git rev-parse --verify --quiet origin/HEAD` succeeds.
2. Otherwise, when `git branch --show-current` is non-empty, read that branch's reflog, not `HEAD`'s. Linked worktrees share the branch reflog, and `git branch -m` keeps it on the new name. The command is `git reflog show --date=unix --format='%H%x09%gd%x09%gs' <current>`. Keep a line whose subject is `branch: Created from <src>`. The base is the `%H` commit on the line whose `%gd` braces hold the smallest unix time. `%H` must pass `git rev-parse --verify --quiet`, and `git merge-base --is-ancestor <commit> HEAD` must succeed. If it does not, drop that line and take the next smallest time. Do not resolve `<src>`. Equal times use the commit that is an ancestor of the other; if neither is, use the lexicographically smallest SHA.
3. Otherwise, list `git for-each-ref --format='%(refname:short) %(committerdate:unix)' refs/heads refs/remotes`. Keep a ref when its name is not the current branch, `git rev-parse <ref>` is not `git rev-parse HEAD`, and `git merge-base --is-ancestor <ref> HEAD` succeeds. From `git reflog show --format=%gs <current>`, collect old names: start with the current name, and on each line `Branch: renamed refs/heads/<old> to refs/heads/<new>` add `<old>` when `<new>` is already collected. Drop a kept ref when `git reflog show --format=%gs <ref>` contains `branch: Created from <name>` for a collected name. Also drop it when that reflog contains `branch: Created from HEAD`, `git rev-parse <ref>` equals the `%H` on that line, and another kept ref is an ancestor of `<ref>`. Choose the greatest committer timestamp among the refs that remain. Equal timestamps use the lexicographically smallest ref name.
4. Otherwise there is no base, and the tracked diff is `git diff HEAD`.

When a base resolved, the tracked diff is `git diff --merge-base <base>`.

- **Path-suffix signal** — a path in that change set ends in `.html`, `.css`, `.scss`, `.less`, `.vue`, `.svelte`, `.tsx`, or `.jsx`. Names are `git diff --name-only` on the tracked diff, plus the untracked list.
- **View-markup signal** — an added or removed line in `git diff -U0` on the tracked diff matches the diff pattern below, or any line of an untracked file matches the tag pattern below. Both are case-sensitive.

Diff pattern (`grep -E` on `git diff -U0`):

```
^[+-].*</?(div|span|button|input|img|svg|path|ul|li|form|label|textarea|canvas|section|header|footer|nav|table|video|iframe|h[1-6])([[:space:]]|>|/)
```

Tag pattern (`grep -E` on each untracked file):

```
</?(div|span|button|input|img|svg|path|ul|li|form|label|textarea|canvas|section|header|footer|nav|table|video|iframe|h[1-6])([[:space:]]|>|/)
```

Either hit means the face includes UI behavior. The verify stage then includes at least one check that opens a UI — real environment first per the tier rules; a simulated UI still counts as opening a UI. That check triggers the screenshot clause above. Non-UI checks stay screenshot-free, and fabricating an image is still forbidden.

When `figma-pixel-verify` owns this verify and its report channel is `layout-probe` with `Screenshot: not-openable`, that recorded line is the UI-evidence outcome for the pixel check and it closes this precheck. An openable channel under that skill opens a UI and keeps a screenshot, which satisfies this precheck.

If a signal hits and this run still cannot open a UI, classify the blocker under the A/B/C rule before writing the report. Class A wires a UI-opening check this turn. A limitation entry is for class C, and for class B while the one-time setup is still pending. The entry states why it is blocked, which tier is blocked, and the follow-up action that will cover the gap, and it states that non-UI checks do not cover the UI behavior.

When neither signal hits, this precheck does not fire. Non-UI checks satisfy verification as before.

## Honest tier labeling (non-blocking)

The verification report MUST state which tier each check actually used. When the tier used is below the production target, label it: "verified in simulation; real-environment smoke test recommended." This is a labeling duty, not a gate — it never blocks the AI from verifying at the reachable tier, but it forbids presenting a simulated result as real-environment confirmation.

## Boundaries

- **`completion-evidence-discipline`** — orthogonal axis. It governs evidence *freshness* (did you actually run it this turn); this skill governs *environment and executor* (which tier, who ran it, sufficient?). A pass claim must satisfy both.
- **`runtime-evidence-debug`** — that skill is debug *forensics*: instrument to find a root cause. This skill is verification *execution*: confirm a fix or feature works in an environment. Different purpose, despite the similar name.
- **Capability skills** (`browser-debug-toolkit`, `android-webview-debug`, future Electron/mobile skills) — they own channel selection and driving recipes. This skill only decides where/who/sufficiency and delegates the *how* to them.

## Integration guide (for hosts)

- Declare `runtime-verification-discipline` in frontmatter `dependencies`; abort at startup if missing.
- At the verify stage, add one thin line: "Verification execution follows `runtime-verification-discipline`" plus the host's own scope conditions. Keep the host's own orchestration and exits.
- Do **not** restate the tier model, selection rule, provider resolution, or A/B/C prose in the host — this skill is the single source.

Per-host edit shapes and worked examples are in [reference.md](reference.md).
