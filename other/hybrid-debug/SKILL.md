---
name: hybrid-debug
version: "1.0.0"
user-invocable: true
description: "Hybrid app (native shell + WebView/WKWebView/Electron + H5) full-stack debugging methodology — forces analysis across four layers (web runtime, native-web bridge, native config, platform runtime) instead of stopping at a single layer, preventing whack-a-mole surface fixes. Use when debugging hybrid app UI/theme/behavior issues, especially platform discrepancies (one platform reproduces, the other does not), repeated single-end fix failures, or silent failures involving native-H5 communication, theme switching, or platform runtime behavior. Triggers — 「hybrid 调试」「跨端调试」「全链路调试」「平台差异调试」「WebView 问题」「WKWebView 问题」「native 和 H5 交互问题」「单端修复失败」「跨端主题问题」「跨端样式不一致」 / hybrid debug, cross-platform debug, webview issue, native-web bridge, full-stack debugging, RN/Electron debugging."
---

# Hybrid Fullstack Debugging

> **Role**: Provides a four-layer analysis model and a domain knowledge base for debugging hybrid applications (native shell + embedded web). It is a methodology + knowledge enhancement, not a standalone end-to-end workflow — **referenced by** PDCA hosts via frontmatter `dependencies` (invoked after a prerequisite check), and it delegates runtime inspection to `browser-debug-toolkit`.
>
> **Domain knowledge** (technical pitfalls, native↔H5 contract templates, anchored case) is in [reference.md](reference.md).

## Why this skill exists

Hybrid apps have a **layer-gap blindness** problem. Pure frontend engineers tend to hunt causes only in the H5 layer (CSS/JS); pure native engineers tend to hunt only in native code. The **platform runtime layer** (WebView's `prefers-color-scheme`, WKWebView gesture handling, Electron IPC) is a grey zone neither side knows well.

The result: problems get "fixed" repeatedly without resolving, or fixing one element leaks the same hidden bug across sibling elements, or a surface patch introduces new cross-platform inconsistency. The meta-lesson this skill exists to enforce:

> **For hybrid apps, you must analyze across native / web / platform-runtime — the full chain — to find the root fix. Single-layer analysis produces whack-a-mole patches.**

## When to use

Strong signals (any one is enough):

- A hybrid app (WebView / WKWebView / Electron / React Native + H5) has a UI, theme, or behavior problem.
- **Platform discrepancy** — the problem reproduces on Android but not iOS (or vice versa), or on one Electron version but not another. This is the strongest signal: platform differences almost always originate in L2/L3/L4 (bridge / native config / platform runtime), never in L1 (H5 code is shared across platforms and cannot produce a platform difference by itself).
- A single-end fix was attempted but the problem returned, or sibling elements with the same root cause were missed.
- Silent failure: the call chain looks complete, parameters are correct, logs show execution — but the runtime behavior is wrong. This points to platform-runtime interception (L4) or an incomplete native↔H5 contract (L2).

## Relationship to other skills

| Skill | Responsibility | Relationship to this skill |
|-------|---------------|----------------------------|
| PDCA hosts | Host workflows | **Referenced by** PDCA hosts via frontmatter `dependencies` (missing → host aborts). Hybrid-specific deep-dive of their technical-analysis phase. Hosts are SoT for that edge. |
| `browser-debug-toolkit` | Browser DevTools tool-selection decision table | This skill's **runtime evidence** step delegates to it — four-layer analysis tells you *what* to verify; `browser-debug-toolkit` tells you *which tool* to verify it with. |
| `essence-diagnosis` | General essence diagnosis (SOAP + multi-hypothesis + adversarial debate) | For hybrid problems that are still foggy after four-layer analysis, escalate to `essence-diagnosis` for heavyweight multi-hypothesis verification. |
| `android-webview-debug` | Toggle Android WebView remote debugging on/off | Often a prerequisite step — enables chrome-devtools inspection of an Android WebView before this skill's runtime-evidence step can run. |

## The Four-Layer Model

Analyze any hybrid issue by locating it across these four layers. The layers are ordered from where symptoms *appear* (L1) toward where root causes often *hide* (L4).

| Layer | Focus | Typical signals |
|-------|-------|-----------------|
| **L1 — Web runtime** | H5 code logic, CSS rules, DOM structure, JS state | The symptom is observable here (a wrong color, a missing class, a broken layout). This is where the problem *shows up*, rarely where it *starts*. |
| **L2 — Native↔web bridge** | How native notifies H5 (attribute injection vs class switch vs JS API call), what gets injected, timing/sequencing | `setAttribute('data-theme','dark')` but no class change; `evaluateJavascript` called before DOM ready; native sets state H5 never reads. |
| **L3 — Native configuration** | Activity/theme config, WebView settings (`forceDarkAllowed`, `algorithmicDarkening`), Manifest, Info.plist | Activity locked to a Light theme; `forceDarkAllowed=false`; WebView dark-mode settings contradict H5 assumptions. |
| **L4 — Platform runtime** | Platform-specific WebView/WKWebView/Electron behavior that differs from a desktop browser | Android WebView's `prefers-color-scheme` follows `isLightTheme`, not the system dark mode; WKWebView gesture quirks; Electron IPC serialization limits. |

### The one discipline that matters: never stop at L1

Finding a cause at L1 is the **starting point**, not the finish line. After identifying an L1 cause, always ask: *"Why is the L1 state like this?"* — and trace it toward L2 → L3/L4 until root-cause confidence is **high**.

Stopping at L1 is the single most common failure mode in hybrid debugging. A typical trap: L1 shows `--color-canvas-subtle` resolves to a light value, so you patch the element that uses it. But the deeper question — *"why does that variable resolve to light on this platform?"* — leads to L3/L4 and a fix that covers every element sharing the variable, not just one.

### Platform discrepancy is a full-chain signal

When a problem reproduces on platform A but not platform B, **do not analyze only platform A**. The difference originates in L2/L3/L4 — compare the bridge path, native config, and platform runtime behavior *across both platforms*. L1 H5 code is shared; it cannot by itself explain a platform difference.

Example shape: iOS calls `setTheme('dark')` → switches H5 class → WKWebView `prefers-color-scheme` follows system. Android calls `setAttribute('data-theme','dark')` → no class change → WebView `prefers-color-scheme` stays light. The difference lives in L2 (bridge mechanism) + L4 (platform runtime), not L1.

## Investigation flow

1. **Locate the symptom layer** (usually L1). Observe the visible wrong behavior and the exact CSS/DOM/state that produces it.
2. **Ask "why is L1 in this state?"** and trace toward L2 → L3/L4. Do not propose a fix yet. The goal of this step is to raise root-cause confidence to *high*.
3. **Cross-check known pitfalls.** Consult [reference.md](reference.md) — the five technical pitfalls cover the most common hybrid traps (platform `prefers-color-scheme` quirks, dual theme-variable systems, incomplete native↔H5 contracts, CSS same-specificity source-order, dev/build CSS processing differences). If a known pitpit matches, it shortcut-confirms the root cause.
4. **Anchor the root cause with runtime evidence.** CSS variable resolution, rule precedence, and platform media-query return values are **only observable at runtime** — static code reading will mislead you. Delegate tool selection to `browser-debug-toolkit`: use the "disable rules one-by-one" technique to find the winning rule, emulate the platform environment (mobile UA + `prefers-color-scheme` + injected classes) to reproduce the device behavior, and use pixel sampling on screenshots to confirm the actual rendered color.
5. **Scan for same-root-cause elements.** Once the root cause is known, find every element/scenario that shares it (e.g. every element consuming the same broken CSS variable). Fixing one and missing the rest guarantees a return visit.
6. **Assess cross-layer side effects** before choosing a fix. Ask: does this fix change the existing behavior of another layer? (An H5-only patch may alter iOS's existing visuals; a native-only patch may break a web-only code path.) The fix must cover the root cause across all affected layers without introducing new inconsistency.
7. **Gate on root-cause confidence.** If confidence is *fuzzy* or *unknown* after step 2, do not jump to a fix — keep tracing, or escalate to runtime instrumentation. Entering execution on a low-confidence root cause is how the first attempt becomes a discarded surface patch.

> The general discipline behind steps 4–7 (runtime evidence, same-root scan, side-effect assessment, confidence gating) is provided by the `runtime-evidence-debug` skill (also a solve-workflow `dependencies` entry). This skill focuses on how to apply them *within the four-layer model* — when used standalone, follow the spirit of those disciplines even without the full workflow.

## Anti-patterns (forbidden moves)

These are the moves that produce whack-a-mole fixes. Recognize and refuse them:

1. **Stopping at L1** — finding a web-layer cause and fixing it without asking why L1 is in that state. The #1 cause of repeated fix failures.
2. **Analyzing a platform-discrepancy problem on a single end only** — the difference lives in L2/L3/L4; single-end analysis is looking in the wrong place.
3. **Guessing CSS rule precedence by reading source** — cascade and variable resolution are runtime behaviors; always verify with DevTools.
4. **Single-point fix without scanning siblings** — fixing `pre` and missing `thead`/`kbd`/`code` that share the same broken variable.
5. **Choosing a fix without cross-layer side-effect assessment** — an H5 patch that silently changes another platform's existing visuals.
6. **Entering execution on low root-cause confidence** — "probably this" leads to a discarded first attempt and wasted cycles.
7. **"Defensive fallback" self-justification** — keeping a known-superficial fix by inventing a "backwards compatibility" rationale that doesn't hold up under scrutiny. A half-fix creates more confusion than no fix.

## Domain knowledge reference

The following live in [reference.md](reference.md) to keep this file lean:

- **Five technical pitfalls** — Android WebView `prefers-color-scheme` quirk, dual theme-variable system conflict, incomplete native↔H5 theme-sync contract, CSS same-specificity source-order trap, dev/build CSS processing divergence. Each with behavior, official basis, and avoidance guidance.
- **native↔H5 communication contract template** — the three things native must keep in sync (class + attribute + persistent storage) when notifying H5 of a state change, and why a unified H5-exposed API beats direct DOM manipulation.
- **Anchored case summary** — a sanitized reference case (dark-mode code-block background not following theme on one platform) demonstrating the four-layer model end-to-end, including a failed L1-only first attempt and the successful full-chain root fix.
