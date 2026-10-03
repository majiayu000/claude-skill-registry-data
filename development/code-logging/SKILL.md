---
name: code-logging
description: Use when the user wants the log statements in code standardized — audit and fix existing logging, correct log level / message shape / context keys, fill in missing log points, or restore a broken distributed traceId so that humans and AI can locate a problem from the logs alone. Trigger on 日志规范 / 规范日志 / 日志格式 / 日志标准化 / 日志规范化 / 补日志 / 加日志 / 日志打得太乱 / 日志看不出问题在哪 / 排查全靠猜 / traceId 断了 / 链路追不下去 / logging standards / structured logging / make logs debuggable / fix our logging. Confirms scope and every risky change interactively before editing. Do not use for 日志框架配置（logback/log4j）与采集端管道、监控指标与告警规则设计（用 observability-setup）、从既有日志定位具体故障（用 systematic-debugging）、性能测量（用 performance-investigation）。
---

# Code Logging

Standardize the log statements in code — **where** to log, at **what level**, how the **message** reads, and which **context keys** ride along — so a human or an AI reading the logs can locate a problem without reading the source.

The subject is the **log call sites in code**. Appenders, encoders, log platforms and collection pipelines are out of scope; see the single assumption in `references/standard.md`.

## Modes and Flow

| Mode | Trigger | Flow |
|---|---|---|
| **Path** | user names a file or directory | scan → tiered findings → tiered confirmation → edit → report |
| **Git Uncommitted** | user wants just-written / uncommitted code standardized | discover repo → collect changed source → scan → tiered confirmation → edit → report |
| **Repo Audit** | user wants whole-repo governance | scope guard → scan → offer report file → tiered confirmation → edit → report |
| **New Code** | user asks to add logging while code is being written | apply the standard directly — no audit, no findings list, no confirmation round |

Resolve the mode before reading anything. When the user is ambiguous between Path and Git Uncommitted, ask with the platform's interactive question tool (e.g. AskUserQuestion), recommended option first.

References (in this skill's directory, read on demand):
- `references/standard.md` — the standard itself: message shape, context keys, the five mandatory log points, level rules, exception rules. **Read before writing or rewriting any log statement, in every mode.**
- `references/checks.md` — the numbered violation checks (F/S/P/T/PII), judgment rules, and the redlines that must never be touched. **Read before any audit mode.**
- `references/lang-java.md` · `lang-python.md` · `lang-go.md` · `lang-typescript.md` — logger API, context mechanism, and break-point idioms per language. Read one per language present in scope.
- `references/few-shots.md` — before/after anchors for each tier. **Read before the first edit.**
- `assets/claude-md-snippet.md` — condensed clauses for the user to paste into a project `CLAUDE.md`.

Do NOT use this skill for: credential-leak auditing (`audit-remote-secret-leaks`), adding comments (`code-annotating`), removing redundancy (`code-slimming`), full multi-dimension review (`code-review-deep`), or configuring logback / log4j2 / encoders / collection.

## Scope Rules

### Path
Scan only the named file or directory. Never expand into callers or callees unless the user asks.

### Git Uncommitted
1. **Repo discovery** — cwd inside a git repo → use it. Otherwise scan child directories for repos with uncommitted changes: exactly one → use it and say so; several → interactive pick; none → report and stop.
2. **Change collection** — staged + unstaged + untracked (`git status --porcelain`). Keep program source only (`.java` `.kt` `.py` `.go` `.rs` `.js` `.ts` `.tsx` `.vue` …); exclude config, resources, generated code, and test files (tests are exempt from this standard). Locate changes with `git diff HEAD -- <file>`; an untracked file counts as entirely new.
3. Scan only the changed hunks plus the enclosing method/function of each hunk. Untouched members stay untouched.

### Repo Audit
1. **Scope guard** — count candidate source files first. Over 20 files: report the count and ask continue / batch / narrow. Batching is about 10 files per batch with a progress summary after each. Process sequentially; no parallel subagents.
2. **Report file** — before scanning, ask whether to also write `log-audit-report.md`; default location is the repo root, confirm the path before writing. Never write it unasked.

### New Code
No scan, no findings list, no confirmation. Apply `references/standard.md` while writing, then state in one line which points were logged and why. If the project has no traceId context at all, say so once — do not open an audit.

## Findings and Confirmation

Every finding carries its check id from `references/checks.md`. Findings are grouped into five tiers, and **each tier has its own confirmation gate** — never merge them into one list.

| Tier | Contents | How it lands |
|---|---|---|
| **F — Format** | placeholder vs concatenation, non-self-contained message, missing mandatory context key, message language/shape | one list, one confirmation, batch edit |
| **S — Semantic** | level changes, duplicate recording, the four exception rules | per-item confirmation — each changes runtime or alerting behavior |
| **P — Missing points** | the five mandatory log points not covered | own section; give the insertion site and the proposed statement; per-item confirmation |
| **T — Trace continuity** | context lost across thread pool / async / MQ / outbound call | per-site preview, per-site confirmation; only context propagation is added |
| **PII** | privacy leaked into logs | **report only, never edit** — high priority, with a suggested masking rewrite the user applies |

Rules that hold across tiers:
- Nothing is edited before its tier's gate. A user saying "全改" up front collapses F, but S / P / T still surface their previews.
- **T only ever adds context propagation** — a filter/interceptor, a thread-pool decorator, an MQ header carry, an outbound header injection. Never appenders, encoders, collection config, or a tracing dependency the project does not already have.
- If the project has no traceId source at all, do not invent one silently: report the gap, name the language-appropriate mechanism from the `lang-*.md` file, and let the user decide.
- Respect the redlines in `references/checks.md` — some log lines are asserted by tests or matched by alert rules and must not be reworded.

## Reporting

Terminal output, always:
1. **Counts table** — findings per tier, files touched, files skipped.
2. **One section per tier**, in F / S / P / T / PII order, each finding as `file:line` + check id + one-line reason.
3. **PII section** — highest visual priority even when small; state plainly that nothing was edited there.
4. **Trace gaps** — break points found but not fixed, and why.
5. **Observations, report only** — bug-like findings, log lines whose text contradicts the code, statements left alone because of a redline.

In Repo Audit mode the same content also goes to the report file when the user accepted one.

## Common Mistakes

- Editing before the tier's confirmation gate
- Merging all five tiers into one "确认全改" list — level changes and new log statements get buried
- Editing a PII finding instead of reporting it
- Touching logback.xml / log4j2.xml / encoder / collection config — always out of scope
- Introducing a tracing framework the project does not have, under the name of "fixing traceId"
- Rewording a log message that a test asserts on or an alert rule matches
- Adding log statements inside loops or hot paths to satisfy the mandatory-point rule
- Applying the Java MDC idiom to Go or TypeScript instead of that language's context mechanism
- Reformatting or refactoring adjacent code; this skill changes log statements and context propagation only
- Running `git commit`
