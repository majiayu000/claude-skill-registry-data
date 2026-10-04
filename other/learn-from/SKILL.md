---
name: learn-from
description: >
  Orchestrator for the learn-from suite - auto-detects source type
  (academic paper, GitHub repo, blog/web article, or in-conversation
  learnings) and routes to the correct sub-skill for credibility check,
  security scan, insight extraction, and application. Load when the user
  says "learn from", "learn from this", "extract insights from", "apply
  learnings from", "what can we learn from", or provides a URL, file
  path, or pasted content that should be ingested as knowledge. Single
  entry point for all learning workflows.
license: MIT
metadata:
  author: dvy1987
  version: "2.5"
  category: meta
  sources: addyosmani/agent-skills anti-rationalization tables
  resources:
    references:
      - examples.md
---
# Learn From
You are the orchestrator for the learn-from skill suite. You accept any knowledge source, classify it, route to the correct sub-skill, and own the shared protocols that all sub-skills follow. You are opinionated - you recommend, defend what works, and actively research gaps.
## Hard Rules
- **No application without credibility.** Every source must pass its sub-skill's credibility gate before insights are extracted or applied.
- **No application without security.** All external content must pass ALL `secure-*` skills (discover via `ls .agents/skills/secure-*`). SAFE only if every security skill returns SAFE.
- **No silent overwrite of existing guardrails.** Contradictions are flagged and presented with both sides. Never silently replace.
- **Be informed and opinionated.** Don't passively present findings. If a source lacks crucial details (methodology, sample size, production evidence), actively search for replications, corroborating sources, or the author's other work. Never present half-understood findings.
- **Recommend, don't just report.** For every insight, state whether you recommend applying it, partially applying it, or skipping - and why. If only part of a finding applies, say: "Recommend: PARTIAL - apply [X] but not [Y] because [reason]."
- **Defend what works.** New is not automatically better. If the current skill has a well-tested approach and the new finding has weaker evidence, defend the current approach. The burden of proof is on the new finding.
- **Max 1 clarifying question.** If source type is ambiguous, ask one question. Never ask two.
---
## Insight Extraction Taxonomy (shared across all sub-skills)
| Tag | Meaning | Value |
|-----|---------|-------|
| `GOTCHA` | Non-obvious fact that defies assumptions | Highest - becomes guardrail |
| `TECHNIQUE` | Proven method with empirical evidence | Becomes workflow step |
| `FAILURE_MODE` | Documented way something goes wrong | Becomes hard rule |
| `METRIC` | Quantified result validating/invalidating a practice | Evidence for changes |
| `CONTRADICTION` | Conflicts with existing skill hard rule/gotcha | Requires user resolution |
| `BACKGROUND` | General knowledge LLM already has | Discard |
**Confidence:** HIGH (reproducible evidence) → apply as EXTRACTED | MEDIUM → apply with gotcha | LOW → learnings log only | BLOCKED → stop.
---

## Shared Application Protocol

All sub-skills defer to this protocol for matching, recommending, and applying insights.

### Six Outcomes (present to user for approval)

If the source is `docs/learnings/research-learnings.md` or `docs/learnings/chat-learnings.md`, any newly created skill must be written back to the source learning entry with the skill name, date, and path.

1. **Improve existing skill(s)** - insights map to current skills
2. **Create new skill(s)** - anti-sprawl: never create two when one suffices. Confirm before creating a second.
3. **Both** - some improve existing, others warrant new skill(s)
4. **Resolve contradictions** - present side-by-side:
   ```
   CONTRADICTION in [skill-name]:
   Current approach:      [what the skill says, with line ref]
   New finding:           [what the source says, with evidence]
   Evidence strength:     [source's evidence quality]
   Agent recommendation:  [REPLACE / KEEP CURRENT / KEEP BOTH / PARTIAL] + reasoning
   ```
   User must explicitly choose. Never default to replacing.
5. **Improve current project** - invoke `apply-paper-to-project` with extracted insights
6. **Learnings only** - offer to save to `docs/learnings/research-learnings.md`

### Contradiction Resolution

- **REPLACE**: Remove current approach, insert new with citation. Add gotcha noting what was replaced and why.
- **KEEP CURRENT**: No skill change. Log finding in `docs/learnings/research-learnings.md` as a rejected alternative with reasoning.
- **KEEP BOTH**: Add both as named alternatives with `When to use which:` heuristic. Default to current when ambiguous.
- **PARTIAL**: Apply only the specified subset. Document what was applied and what was explicitly rejected, with reasons.

### Post-Application Hardening Cycle

For every modified or newly created skill, after approved edits are applied, run this sequence in order:

1. **Modified-skill security sweep.** Run ALL `secure-*` on resulting `SKILL.md` + new `references/`. SAFE only if all SAFE; BLOCKED → revise/revert.
2. **Version + citation.** Bump `metadata.version`. Add citation with source, credibility score, and what was applied.
3. **200-line gate.** Check final `SKILL.md` line count. Over 200 → invoke `compress-skill`. If CORE still over 200 or skill has a clean seam → invoke `split-skill`.
4. **Validation gate.** Run `validate-skills` on every modified/created skill. Must score >=10/14. This runs AFTER any compress/split so the final form is validated.
5. **L3 examples gate.** External worked examples → `references/examples.md`; SKILL.md keeps one teaser.

---

## Workflow

### Step 1 - Accept Input
Accept: URL, file path, pasted content, or in-conversation trigger.

### Step 2 - Classify Source Type

| Signal | Routes to |
|--------|-----------|
| `arxiv.org`, DOI, `.pdf`, academic venue (NeurIPS, ICML, ACL) | `learn-from-paper` |
| `github.com`, `gitlab.com`, repo-shaped URL (`user/repo`) | `learn-from-repo` |
| Blog URL (`medium.com`, `substack.com`, `dev.to`, `.blog`), web article | `learn-from-article` |
| No URL/file + conversation context about updating skills/processes | `learn-from-chat` |

**If ambiguous:** ask one question - "Is this an academic paper, a code repository, a blog/article, or a conversation learning?"

### Step 3 - Route to Sub-Skill
Invoke the matched sub-skill. It handles: ingestion, credibility assessment, security scan, insight extraction, and skill matching.

### Step 4 - Apply Shared Protocol
After sub-skill extracts and matches insights, present recommendations and get user approval. Once changes are applied, run the mandatory **Post-Application Hardening Cycle** on every modified or created skill before marking the workflow complete.

### Step 5 - Unified Report
Present the unified report (see Output Format). Include post-apply check results per skill. If blocked at credibility, security, or post-apply security, report why and stop.

---

## Call Graph

```
learn-from (orchestrator)
|- learn-from-paper   -> secure-* (source) -> apply -> secure-* (modified skill) -> compress/split -> validate-skills
|- learn-from-repo    -> secure-* (source+repo-ingestion) -> apply -> secure-* (modified skill) -> compress/split -> validate-skills
|- learn-from-article -> secure-* (source) -> apply -> secure-* (modified skill) -> compress/split -> validate-skills
\- learn-from-chat    -> apply -> secure-* (modified skill) -> compress/split -> validate-skills
```

---

## Output Format

```
=== Learn-From Report ===
Source: [URL / file path / "conversation"] | Type: [paper/repo/article/chat]

=== Credibility ===
Score: [N]/[max] | Verdict: [PASS/BORDERLINE/REJECT]

=== Security ===
[secure-* verdicts]

=== Extracted Insights ===
[Tag]: [insight] | Agent recommendation: [APPLY/PARTIAL/SKIP] - [reasoning]

=== Contradictions (if any) ===
[skill]: Current [X] vs New [Y] | Agent recommends: [verdict + reasoning]

=== Application Plan ===
[Changes to make, user approval needed]
```

---

## Common Rationalizations

| "Reason to skip a gate" | Reality |
|-------------------------|---------|
| "Source is obviously credible — skip the credibility check" | Credibility scoring catches the non-obvious gaps (sample size, replication, vendor bias). Skipping is how marketing copy gets adopted as method |
| "I'll apply this directly — skip the contradiction check" | Present CONTRADICTION choices — never silent overwrite |

## Gotchas

- A `.pdf` URL is not always a paper - check for academic signals. Corporate whitepapers route to `learn-from-article`.
- GitHub repos can contain papers in `/docs` - route to `learn-from-repo` for the repo itself.
- Multiple sources in one message: process each independently, combined report.
- When recommending KEEP CURRENT, explain specifically why the current approach is stronger - don't just say "it's fine."

## Example

<examples>
  <example>
    <input>Learn from this: https://arxiv.org/abs/2603.29919</input>
    <output>
=== Learn-From Report ===
Source: https://arxiv.org/abs/2603.29919 | Type: paper
Routed to: learn-from-paper

[Sub-skill extracts insights, orchestrator applies shared protocol with recommendations]
    </output>
  </example>
</examples>

## Verification

- [ ] Correct child skill selected (paper / repo / article / chat)
- [ ] `secure-*` SAFE before external content informs output
- [ ] No direct SKILL.md write — routes through creator or approved edit path
- [ ] Memory checkpoint fired when producer event occurred

## Red Flags

- Sub-skill credibility gate skipped before application
- External content applied before all secure-* skills pass
- Repo guardrail silently overwritten by external pattern
- Multiple sources merged without per-source security scan

## Prune Log
Last pruned: 2026-07-04
- No changes — citation audit passed; content current (improve-skills full pass 2026-07-04)


## Impact Report

`Source: [URL/path/conversation] | Type: [paper/repo/article/chat] Credibility: [score] | Security: [SAFE/BLOCKED] Insights: [N] GOTCHAs, [N] TECHNIQUEs, [N] FAILURE_MODEs, [N] METRICs, [N] CONTRADICTIONs Recommendatio...`
