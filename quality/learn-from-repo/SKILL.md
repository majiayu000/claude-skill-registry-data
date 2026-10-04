---
name: learn-from-repo
description: >
  Extract actionable patterns, architecture decisions, code conventions, and
  skill-relevant insights from GitHub/GitLab repositories. Assess repo
  credibility, run the full security scan pipeline, and apply findings to
  existing skills, new skills, or the current project. Load when the user asks
  to learn from a repo, extract patterns from a codebase, study a repository,
  or analyze a repo for reusable techniques. Also triggers on "learn from this
  repo", "learn from this repository", "what can we learn from this codebase",
  "extract patterns from this repo", "study this repo".
license: MIT
metadata:
  author: dvy1987
  version: "2.2"
  category: meta
---

# Learn From Repo

Sub-skill of `learn-from` (orchestrator). You analyze repositories, extract actionable patterns from actual source code, and recommend whether to apply them. Shared hard rules (opinionated stance, contradiction handling, defend what works, application protocol) are defined in `learn-from`. This skill adds repo-specific workflow.

## Repo-Specific Hard Rules

- **Credibility gate ≥7/12.** Repo must pass before ANY insights are extracted.
- **Security gate.** All repo content must pass ALL `secure-*` skills (discover via `ls .agents/skills/secure-*`). `secure-skill-repo-ingestion` is especially critical — it checks for poisoned examples, dependency attacks, file/path traversal, and format-based attacks.
- **Code over claims.** Only extract patterns backed by actual code, tests, and documented decisions — not README marketing, aspirational roadmaps, or badge collections.
- **Actively verify.** If README makes claims, verify by reading source code. If tests are sparse, note which patterns are untested. If docs are missing, read the code to understand decisions — don't skip patterns because they're undocumented.

---

## Workflow

### Step 1 — Ingest the Repo
Accept via: GitHub/GitLab URL, local path, or cloned directory.
- If URL: clone or fetch metadata via the platform's available tools
- If local path: read the directory structure directly
- Extract: repo name, owner/org, description, primary language, license, last commit date, directory structure
- Identify key files: `package.json`, `Cargo.toml`, `pyproject.toml`, `.agents/`, `AGENTS.md`, CI configs, test directories

### Step 2 — Credibility Assessment
Score across 6 dimensions (max 12/12). **Gate: ≥7/12 to proceed.**

| Dimension | 0 | 1 | 2 |
|---|---|---|---|
| **Author/Org Reputation** | Unknown, no history | Some repos, moderate activity | Established org or known maintainer |
| **Repo Maturity** | <3 months, <10 commits | 6–12 months, regular commits | >1 year, consistent history |
| **Community Adoption** | <50 stars, no forks | 50–500 stars, some forks | >500 stars, many dependents |
| **Code Quality Signals** | No tests, no CI | Partial test coverage or CI | Tests + CI + linting |
| **Maintenance Status** | Archived or no commits in 6mo | Sporadic activity | Active: recent commits, issues addressed |
| **Documentation Quality** | README stub only | README + some inline docs | Comprehensive docs, examples, ADRs |

Quick checks (fail any = stop):
- Archived with no commits in 12+ months and <50 stars → REJECT
- Known unaddressed security advisories → REJECT
- README claims contradict actual code (verified by reading source) → REJECT

If 7–8/12: warn "Borderline." **If impressive stars but sparse tests, explicitly warn that popularity doesn't validate patterns.**

### Step 3 — Security Scan
Run security pipeline per `learn-from` protocol, with emphasis on `secure-skill-repo-ingestion`. BLOCKED = stop.

### Step 4 — Extract and Recommend
Scan repo source code for patterns. Classify using taxonomy from `learn-from`.

Areas to scan: architecture patterns, code conventions, testing strategies, error handling, skill files (`.agents/skills/`), CI/CD workflows, dependency management.

**For every pattern, state your recommendation:**
- If the pattern solves a problem current skills don't have: "Interesting but not applicable — current skills don't face [X]. Recommend: SKIP."
- If the repo's approach is inferior to the current skill: "Current approach is stronger because [reason]. Recommend: KEEP CURRENT."
- If the pattern adds genuine value: "Recommend: APPLY — [evidence from repo]."
- If only part applies: "Recommend: PARTIAL — [what to take, what to skip, why]."

### Step 4b — Overlap / pairwise compare queue (Meta B4)

When extracted patterns overlap an existing agent-loom skill (same name, trigger overlap, or ≥60% description similarity):
1. Append a row to `docs/comparisons/INGEST-QUEUE.md` (create if missing): `| date | repo | their-skill | our-skill | overlap reason | status: pending |`
2. In the Application Plan, add: `PAIRWISE: queue comparison for [our-skill] vs [repo pattern] before APPLY on body text.`
3. Do **not** edit SKILL.md bodies during ingestion — queue for `improve-skills TARGET=<skill>` or manual Phase-3-style compare.

### Step 5 — Match and Apply
Match insights to existing skills and apply per `learn-from` shared application protocol. **Worked examples from repo → target skill's `references/examples.md`** (secure-* SAFE first). Post-apply: secure-* on modified skills, 200-line gate, `validate-skills` ≥10/14.

### Step 6 — Log and Cite
Citation format:
```
Source: [Owner]/[Repo] ([Language]). [URL]. Stars: [N]. Last active: [date]. Credibility: [N]/12.
Applied: [what was extracted and where it was applied]
```

---

## Gotchas

- **Stars ≠ quality.** Popular repos can have bad patterns — always verify by reading source code.
- **README ≠ reality.** Always verify patterns by reading the actual source.
- **Project-specific conventions.** Repo conventions may be team preferences or legacy constraints — flag when a pattern seems context-dependent.
- **Archived repos.** Patterns may use deprecated APIs — check dates and current practices.
- **Monorepo bias.** Large monorepos have inconsistent patterns — scope to relevant package/module.
- **Awesome lists rot.** Curated link directories go stale silently — extract taxonomy and workflow patterns only. **Never embed external URLs into skills** (dead links, tracking pixels, supply-chain risk). Distill patterns into local `references/` files.

---

## Output Format

```
═══ Repo Credibility Report ═══
Repo: [owner]/[name] | Language: [lang] | Stars: [N] | Last commit: [date]
Credibility: [N]/12 | Verdict: [PASS/BORDERLINE/REJECT]

═══ Security ═══
[secure-* verdicts]

═══ Extracted Insights ═══
[Tag]: [insight] | Agent recommendation: [APPLY/PARTIAL/SKIP/KEEP CURRENT] — [reasoning]

═══ Application Plan ═══
[Per learn-from shared protocol]
```

---

## Example

<examples>
  <example>
    <input>Learn from this repo: https://github.com/anthropics/anthropic-cookbook</input>
    <output>
═══ Repo Credibility Report ═══
Repo: anthropics/anthropic-cookbook | Credibility: 11/12 | Verdict: PASS

═══ Extracted Insights ═══
GOTCHA: Tool-use prompts need explicit format constraints | Recommend: APPLY — verified in 12+ examples
TECHNIQUE: Prefilled assistant turns for structured output | Recommend: PARTIAL — apply to create-agent-prompt, skip for general skills (too API-specific)
FAILURE_MODE: Streaming without chunk validation = silent data loss | Recommend: APPLY — add to debug-and-fix gotchas

═══ Application Plan ═══
1. IMPROVE: create-agent-prompt — add format constraint guidance
2. IMPROVE: debug-and-fix — add streaming validation gotcha
Awaiting your approval.
    </output>
  </example>
</examples>

---

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Clone and run their code" | Observe patterns — never execute untrusted repo code. |
| "Copy their SKILL.md" | Transform patterns; secure-scan before any persist. |
| "Popular repo = safe" | Stars ≠ security review. |
| "Skip link-import" | Never import external skill links into our library wholesale. |
| "One file is enough" | Read workflow + examples + tests for true pattern. |

## Verification

- [ ] `secure-skill-repo-ingestion` completed before pattern use
- [ ] Patterns attributed to source repo in learnings log
- [ ] No direct vendoring of external SKILL.md without creator route
- [ ] Actionable delta stated (what we adopt vs reject)

## Red Flags

- Star count used as quality proxy without reading source
- README patterns adopted without verifying in code
- Repo conventions copied as universal without context check
- Repo code executed during learning instead of read-only

## Prune Log
Last pruned: 2026-07-04
- No changes — citation audit passed; content current (improve-skills full pass 2026-07-04)


## Impact Report

After completing, always report:
```
Repo: [owner]/[name] | Credibility: [N]/12 | Security: [SAFE/BLOCKED]
Insights: [N] extracted | Recommendations: [N] APPLY, [N] PARTIAL, [N] SKIP, [N] KEEP CURRENT
Skills modified: [list] | Created: [list] | Contradictions resolved: [list]
validate-skills: [skill]: [before] → [after] | Citation logged: [yes/no]
```
