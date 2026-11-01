---
name: upstream-dependency-debug
version: "1.1.0"
user-invocable: true
description: "When a bug involves a named third-party library/framework, or symptoms correlate strongly with a platform/library-specific behavior, evaluate 'upgrade the dependency' BEFORE piling on local workarounds. Walks through a 4-step decision (is it upstream? → check Changelog/Release Notes → upgrade at low semver risk → only workaround if upgrade is infeasible), the upgrade engineering discipline (package-manager consistency, post-upgrade verification chain, semver risk, dedup check), and a result table. Use this skill whenever a bug smells like an upstream library issue — symptoms tied to a specific framework version, silent failures where code looks correct, workarounds that keep growing, or platform-specific rendering bugs that CSS cannot fix. Triggers — 「升级依赖」「依赖升级修复」「这个 bug 升级依赖能解决吗」「查 changelog 修复」「优先升级依赖」「升级依赖还是堆 workaround」 / dependency upgrade, upgrade to fix bug, changelog fix, avoid workaround, upgrade library to fix."
---

# Dependency Upgrade as Bug Fix

> **Role**: A decision-and-execution methodology for the case where the cleanest fix for a bug is *upgrading a dependency* rather than writing a local workaround. It is a methodology enhancement: it can be invoked standalone, and it is **referenced by** PDCA hosts during their technical-analysis phase (as the optimistic counterpart to the "no viable solution" branch).

## Why this skill exists

When engineers (and AI agents) hit a bug, the reflex is to patch it locally — add a guard, tweak a timer, hide an element, override a CSS rule. This reflex is often wrong when the root cause lives in an **upstream dependency**: the local patch becomes a *workaround* that papers over someone else's bug, and workarounds compound.

The pattern that this skill exists to break:

> A bug's real fix is "upgrade the library," but nobody checks the upstream Changelog. Instead, three layers of local workarounds get stacked — a magic-number timer, a UX degradation, a CSS override that the platform silently ignores. Each layer fails in a slightly different way on real devices. Weeks later, someone finally reads the Changelog, finds the fix shipped two minor versions ago, and a one-line `package.json` bump replaces all three workarounds.

Anchored case (sanitized): a rich-text editor's task-list item showed an abnormal selection highlight during IME composition on iOS. Three local workarounds were attempted and each failed on real devices — the last one because iOS forcibly renders the native `::selection` background during composition and **no CSS can override it**. The actual fix was upgrading the editor library two minor versions, where the upstream had already patched the widget-reuse behavior near composition. Zero local code changes.

The meta-lesson:

> **Before writing a workaround, ask: "Is this bug already fixed upstream?" A one-line dependency upgrade is often cheaper, more correct, and more durable than any local patch.**

## When to use

Strong signals (any one is enough — this skill is meant to be invoked readily, because the "check upstream first" instinct is the thing people forget):

- The bug involves a **named third-party library, framework, or API** and correlates with a specific version.
- Symptoms are **platform/library-specific** — the bug reproduces on iOS but not desktop Chrome, or only with a particular framework's rendering path, or only after a recent dependency bump.
- **Silent failure**: the call chain looks complete, parameters are correct, logs show execution — but the behavior is wrong. This often points to a platform/runtime interception that the library is supposed to handle.
- **Workarounds are piling up**: you've already written one or two local patches and they each only partially work, or they introduce new degradation (magic-number timing, UX downgrades, CSS that doesn't take effect).
- A CSS/layout bug where `!important` overrides **silently fail** on a specific platform — a strong sign of platform-enforced rendering that no CSS can fix.

## The 4-step decision order

When the signals above fire, walk this order **before** writing any local patch:

1. **Attribute the bug**: is it more likely upstream or in our code? Signals of upstream: symptoms tied to a platform/library-specific behavior; reproduces only in a specific environment; the library owns the misbehaving layer (selection, composition, rendering).
2. **If likely upstream — check the dependency's Changelog / Release Notes / Issues** for a matching fix. Search the dependency's changelog for keywords matching the symptom (e.g. `composition`, `selection`, `Safari`, `iOS`, `widget`, `cursor`). Confirm whether a fix version exists and whether the project is currently below it.
3. **Prefer upgrading the dependency** (patch/minor, low semver risk) over writing a local workaround. For libraries that follow semver, minor/patch upgrades within the same major version carry no breaking changes by contract.
4. **Only consider a workaround when upgrade is infeasible** — breaking change in the only available fix version, the project is version-locked, or upstream hasn't fixed it yet. If you must workaround, **annotate it as temporary** with its trigger condition and the upstream issue it tracks.

## Anti-patterns (forbidden moves)

1. **Stacking workarounds before checking the Changelog** — the #1 failure mode. The upstream fix may already exist.
2. **Assuming "CSS `!important` will handle it"** on a platform-enforced rendering path — some platform behaviors (e.g. iOS composition-time `::selection`) ignore CSS entirely.
3. **Magic-number timing workarounds** (`setTimeout` 120ms after `compositionend`) — they mask the symptom, break under load, and never address the cause.
4. **UX-degradation workarounds** (downgrade a widget to a source-code marker during composition) — they hide the bug at the cost of the user experience, and often don't even fully hide it.
5. **Treating "upgrade feels risky" as reason enough to workaround** without actually reading the Changelog's breaking-change notes — the risk is usually lower than the workaround's maintenance cost.

## Upgrade engineering discipline

Once the decision to upgrade is made, execute it safely. These checks exist because each one corresponds to a real failure observed in practice:

- **Package-manager consistency**: use the package manager the project actually uses — determine it by which lockfile is tracked (`git ls-files package-lock.json yarn.lock pnpm-lock.yaml`), **not** by the system-level `packageManager` field. The system may force pnpm while the project uses npm; mixing them produces lockfile pollution and duplicate package versions. Do not mix.
- **Post-upgrade verification chain**: `typecheck` + `build` + full unit-test suite + real-device/target-environment verification. A dependency bump that passes typecheck but breaks runtime on the target device is not done.
- **semver risk assessment**: patch/minor within the same major is low-risk **for libraries that follow semver** (verify the library actually follows semver — most do, some don't). A major-version bump requires reading the breaking-change list and assessing each one.
- **Dedup check**: after upgrading, run `npm ls <pkg>` (or the equivalent for the project's package manager) to confirm a single resolved version. Multi-version coexistence (e.g. an old 1.5.0 entity lingering alongside a new 1.5.2) causes type incompatibilities and mysterious failures that are hard to trace back to the upgrade.

## Result table

| Conclusion | Action |
|------------|--------|
| ✅ Upstream already fixed, upgrade is low-risk | Upgrade the dependency as the **preferred solution**. Enter solution-exploration with the upgrade as the recommended option. |
| ⚠️ Upgrade carries risk (major / breaking) | Present upgrade and workaround side-by-side in solution-exploration; let risk tradeoff decide. |
| ❌ Upstream not fixed, or upgrade infeasible (version-locked / breaking) | Fall back to a workaround — but annotate it as temporary, with its trigger condition and the upstream issue it tracks. |

## Relationship to other skills

| Skill | Relationship |
|-------|--------------|
| PDCA hosts | **Referenced by** PDCA hosts at technical-analysis (optimistic counterpart to the "industry-wide no-viable-solution" branch). When invoked through a host, start from the 4-step decision order using the host's already-established root cause. Hosts are SoT for that edge. |
| `effective-web-research` | Step 2 (checking the Changelog) benefits from this skill's research discipline — official sources first (the library's own changelog site), check recency, cross-validate non-trivial claims. |
| `runtime-evidence-debug` | If root-cause confidence is still fuzzy after checking the Changelog, this skill's escape hatch (web research for known platform/framework issues) overlaps with step 2 here. This skill is the *fix-strategy* decision; `runtime-evidence-debug` is the *evidence-gathering* methodology. |

## Domain-specific knowledge boundary

This skill carries **general methodology only**. Library-specific knowledge — e.g. which versions of a particular editor framework fixed which composition bugs, or a UI library's version-specific rendering quirks — belongs in **each project's own docs** (its `AGENTS.md` or fix logs), not in this skill. The reason: library-specific changelog keywords and version numbers go stale and are only relevant to projects using that library; polluting a general skill with them creates maintenance burden and topic drift.

When applying this skill, if the project's docs contain library-specific changelog keywords for the dependency in question, consult them for the search terms — this skill tells you *to check the changelog*; the project docs tell you *what to search for*.

## Standalone invocation

When invoked directly (not through a workflow), start from **When to use** — confirm the signals apply, then walk the 4-step decision order. The output is the result-table conclusion plus the upgrade engineering discipline checklist if upgrade is chosen.
