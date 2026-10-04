---
name: pre-release-audit
description: Systematic pre-release audit that walks the codebase area-by-area, triages findings honestly, and files them to Linear (Baan team). Use when asked for a "pre-release audit", "release audit", "リリース前監査", "監査", or equivalent. Picks one area per session, files one or more Linear tickets, then hands back to the user.
---

# Pre-Release Audit

Walk the codebase area by area, surface issues with honest risk
assessment, and file them to Linear (team: Baan). This skill is the
multi-session workflow that accumulates findings like
BAA-5〜BAA-17. It complements:

- `release-check` — one-shot pass/fail matrix
- `security-scan` — security-only report
- This skill — deep read per area → Linear tickets → iterate

---

## Scope arguments

| Argument | Area |
|----------|------|
| `lib` | `lib/**` |
| `scripts` | `scripts/**` |
| `tests` | `tests/**`, vitest / playwright config |
| `components` | `components/**`, client-side React |
| `api` | `app/**/api/**` |
| `proxy` | `proxy.ts` + related middleware |
| `docker` | `Dockerfile`, `docker-compose*.yml`, `docker-entrypoint.sh`, `.dockerignore` |
| `config` | `tsconfig*.json`, `next.config.ts`, `vercel.json`, `vitest.config.*` |
| `deps` | `package.json`, `npm audit`, GitHub Dependabot alerts |
| `policy` | `SECURITY.md`, `LICENSE`, `.env.example`, `.gitignore` |

No argument → list the areas and ask which to run. Never auto-run all
at once; each area is a focused session.

---

## Per-area workflow

### 1. Read, don't skim

- Enumerate files in the area (`find`, `ls`, or Explore agent)
- Read every file once. Don't stop at "looks fine" — read the
  actual control flow, error paths, and imports
- For large files (>800 lines), read in segments; never rely on head
  or grep alone

### 2. Watch for reality-vs-report gaps

Examples of the class of finding we care about:

- Coverage reports that hide untested modules (only show files
  imported by tests)
- Config comments describing behaviour that no longer matches
- Dead entries in include/exclude lists
- Deprecation warnings silently suppressed
- `skipAuthPaths` entries that no longer point at existing routes
- CVE alerts whose upstream has already released a fix the project
  hasn't picked up
- Tests asserting HTTP 200/429 but also accepting 500 (mask real
  failures)

### 3. Per-finding triage

For each candidate issue:

- **実害シナリオ**: who, doing what, can break what. Concrete.
- **発火条件**: default config, or special path required?
- **既存防御**: is another layer already blocking this?
- **`.claude/rules/` との整合**: rule violation, or stricter-than-rule
  recommendation?
- **ルール自体の妥当性**: if a rule looks stale, flag it separately

### 4. Severity & blocker decision

| Severity | Criteria | Priority |
|----------|----------|----------|
| 🔴 Release blocker | Default config allows auth bypass, info leak, or data loss | Urgent (1) |
| 🟠 High | Exploitable only under special conditions; fix before release preferred | High (2) |
| 🟡 Medium | Defense-in-depth, consistency, correctness — fine to land post-release | Medium (3) |
| 🟢 Low | Cleanup, dead code, doc tidy | Low (4) |

If unsure, default **down** (Medium/Low) and explain the reasoning.
Alarmism corrodes the signal.

### 5. File to Linear

Use `mcp__linear-server__save_issue` against team `Baan`. Format below.

---

## Linear issue format

### Title

`[Category] <target> — <summary>`

| Category | Use |
|----------|-----|
| `[Security]` | Auth, injection, traversal, secret handling, origin checks |
| `[Cleanup]` | Non-security tidy (dead config, doc drift) |
| `[Refactor]` | Structure change without behaviour change |

Keep titles under ~80 chars. Observed good examples:

- `[Security] proxy.ts (Next.js middleware) hardening` (BAA-13)
- `[Cleanup] tsconfig / SECURITY.md / vercel.json audit fixes` (BAA-16)
- `[Refactor] proxy.ts data/logic separation + 7-file bot-definition dedup` (BAA-14)

### Body template

Match the observed house style (Japanese primary, English identifiers
verbatim, code fences with language hints):

```markdown
## 背景

<What was audited, what surfaced. One paragraph.>

## 該当箇所

- `path/to/file.ts:123-130` — <what the problem is>

<code snippet with language hint>

(repeat per finding inside the same area)

## リスク評価

<Concrete attack / failure scenario>

**影響**: 小 / 中 / 大。<specific description>
**発火条件**: <who, which operation, which config>
**既存防御**: <other layers that mitigate, if any>
**結論**: リリースブロッカー / 非ブロッカー

## 修正方針

<Proposal with code snippets>

## ルールとの整合性

<Relationship to `.claude/rules/xxx.md` — rule violation, or
stricter-than-rule defense-in-depth>

## 検出元

<Related issue IDs (BAA-N) if any>
```

For multi-finding tickets, group by severity sub-heading
(`### Medium`, `### Low`) — see BAA-9, BAA-10, BAA-11, BAA-13 for
the pattern.

### Priority mapping

- 🔴 Release blocker → `priority: 1` (Urgent)
- 🟠 High → `priority: 2`
- 🟡 Medium → `priority: 3`
- 🟢 Low → `priority: 4`

### Labels

Apply `Improvement` for non-blocker findings (consistent with
BAA-9〜BAA-16). Leave blockers unlabeled unless a specific label
exists.

---

## Split vs. bundle

| Situation | Action |
|-----------|--------|
| Several findings in the **same file or tight subsystem** | One issue, severity-sectioned body (BAA-17) |
| Same area, but release-blockers coexist with low-priority items | One issue, but explicitly split into "before release" vs "backlog" sections (BAA-13) |
| Independent fix that can ship alone | Separate issue (BAA-15 split from BAA-13) |
| Refactor discovered during security audit | Separate issue, security issue references it (BAA-14 ← BAA-13) |

If a split boundary is ambiguous, propose both options to the user
and let them pick.

---

## Temperature rules

### Honest risk assessment

- Write "実際の攻撃成立確率は低い" when true. Don't inflate severity
  to push a fix
- Name the existing defense layer when one exists
- Prohibit alarmist language (`critical!`, `urgent fix needed!`)
  unless genuinely critical

### Verify every finding against reality

- Read the actual source every time. Never cite a file:line from
  memory or speculation
- If a rule says "must use X", confirm X exists and is imported
  before citing the rule
- Beware stale memory — prior-conversation facts can be out of date

### Check upstream before proposing a fix

For dependency CVEs specifically:

1. Identify the vulnerable package + version range
2. Check if a newer version of the **direct** dependency drops /
   upgrades it
3. Check the upstream repo for open PRs / issues on the dep bump
4. Prefer waiting for upstream over `package.json` overrides. Cover-up
   fixes (overrides that force an API-incompatible version) are a
   last resort

"Waiting for upstream" with a clear why is a legitimate outcome.

### No silent scope creep

- While auditing, do not modify source code
- Do not amend or close existing Linear issues without approval
- "Found it, fixed it along the way" is prohibited — separate file
  Linear issue + get approval + implement as its own commit

### Null findings are results

If a thorough read produces no issues, say so and move on. Don't
manufacture a finding to justify the pass.

### Rule staleness

If `.claude/rules/*.md` itself seems wrong (e.g., cites a file that
moved, recommends a deprecated pattern), file a separate issue
against the rule rather than working around it silently.

---

## Session flow

1. **Scope**: confirm which area to audit (scope argument or
   explicit user choice)
2. **Read**: enumerate and read all files in the area
3. **Draft findings**: present a table of candidate issues with
   severity / blocker / file:line, before any Linear write
4. **Triage with user**: confirm the split (one issue vs. several)
   and the severity of each finding
5. **File to Linear**: write the issue(s), report the IDs + URLs
6. **Stop**: do not start implementing. The implementation phase is
   a separate session (usually `/implement` against the filed issue)

### Pre-write preview

Before calling `save_issue`, always show the user:

```
## Linear 起票案

| # | Title | Priority | Labels |
|---|-------|----------|--------|
| 1 | [Security] ... | High | Improvement |
| 2 | [Cleanup] ...  | Low  | Improvement |

起票してよいですか？
```

Wait for explicit approval.

---

## Output formats

### Candidate findings (before Linear write)

```
## <area> 監査レポート

### 読んだ範囲
- N files, M lines

### 発見
| # | File:line | Issue | Severity | Blocker? |
|---|-----------|-------|----------|----------|
| 1 | lib/foo.ts:42 | <desc> | 🟡 Medium | no |

### 起票案
- (A) まとめて 1 issue
- (B) security 系と cleanup 系で分割

どれで進めますか？
```

### Area summary (after Linear write)

```
## <area> 監査完了

Linear:
- BAA-NN: <title>
- BAA-MM: <title>

Blocker 数: 0
次の区画: <suggest next area>
```

### Full-sweep summary (optional)

When multiple areas have been audited within a release cycle:

```
## リリース前監査 総括

| 区画 | Issue | Blocker | Medium | Low |
|------|-------|---------|--------|-----|
| lib/ | BAA-9 | 0 | 4 | 2 |
| ...  |       |   |   |   |

リリースブロッカー: 合計 N 件
```

---

## Reference: good past issues

Read these before writing a new audit ticket if the house style is
unclear:

| Issue | Why it's a good example |
|-------|-------------------------|
| BAA-13 | Clear blocker / non-blocker split; defense-in-depth framing |
| BAA-11 | Honest "実際の攻撃成立確率は低い" language |
| BAA-17 | Three related problems bundled; impact scope called out |
| BAA-9 | Medium/Low severity subsections, cleanly ordered |
| BAA-16 | Minimal cleanup ticket; no over-justification |

---

## Prohibited

- Writing code during the audit phase
- Filing a ticket without reading the actual file
- Citing a `.claude/rules/` rule without quoting the relevant line
- Elevating severity to pressure a fix
- `overrides` / other cover-up patches proposed before upstream check
- Running `npm audit fix` or similar auto-fix without user approval
- Bundling refactor findings with security findings in one ticket
