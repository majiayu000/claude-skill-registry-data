---
name: skill-health
description: "Scan the skill library for dangling references and build a per-skill health table."
license: MIT
metadata:
  author: shimo4228
  version: "0.1"
  created: "2026-06-25"
origin: shimo4228
disable-model-invocation: true
---

# skill-health — Skill-Library Structural Debt Scan

Detect **skill technical debt** — library-level defects that do not break a
single skill in isolation but degrade the library over time (SkillOps, Pu/Song/
Zhao 2026, [arXiv:2605.13716](https://arxiv.org/abs/2605.13716)). This skill
owns the one debt pattern no other harness skill checks: **missing artifacts**
— a SKILL.md that references a `scripts/` module, a `bash` script, an agent, or
a sibling skill that no longer exists on disk (it silently dangles after a
rename or delete).

This is a **structural** property — decidable from the literal text plus a
filesystem `exists()` check — so deterministic code owns it. The semantic, risk,
and validation dimensions are **delegated, never re-implemented here**.

### Only `dangling` is a defect claim

The scanner (`--help` lists flags, `--json` the keys) reports three lists:

- **`dangling`** (exit code 1) — a written path that does not exist. This is the
  only defect claim.
- **`unresolved_names`** — skill / command names written without a path that match
  no file under the skills root. **An enumeration handed to judgment, not a
  defect**: the name may be a CLI builtin, a plugin command, or a skill in another
  repo, and the slash-command namespace is not enumerable from disk.
  `_KNOWN_NON_FILE_SKILLS` in the scanner is noise reduction, not an authority.
- **`external`** — skills whose directory is a symlink out of the skills root.
  **Also an enumeration, not a defect**: it answers "would a fix applied here
  survive?" — it would not, since the owning tree overwrites it on upgrade. Route
  these upstream (issue / PR). References inside them are still scanned.

## Boundary (read first — this skill does not overlap its neighbours)

SkillOps frames library health as four dimensions. This harness already covers
three; `skill-health` adds the missing structural one and federates the rest:

| Dimension (SkillOps) | Owner | `skill-health` does |
|---|---|---|
| **Compatibility** (refs resolve) | **`skill-health`** ← here | the deterministic scan (Phase 2) |
| **Utility** (frequency, value) | `skill-stocktake` (holistic Keep/Improve/Retire/Merge) | read its signal; flag over-specialized (LLM) |
| **Risk** (security, side effects) | `/claude-security` plugin | delegate; prompt to run if stale |
| **Validation** (tests/consistency) | `skill-comply` / `skill-creator` | note which skills lack a validator |

## Phase 1 — Inventory

Enumerate skill definitions with Glob (`~/.claude/skills/*/SKILL.md`; plus
`{cwd}/.claude/skills/*/SKILL.md` if the project has local skills). State up
front how many skills will be scanned.

## Phase 2 — Compatibility scan (the deterministic core)

Run the structural reference scanner. It extracts every explicit local
reference from each SKILL.md (`python -m scripts.X`, `bash …/x.sh`,
`~/.claude/agents/X.md`, and Markdown links to local files / sibling skills) and
reports those whose target does not exist:

> Paths below start at `${CLAUDE_SKILL_DIR}`, the directory holding this SKILL.md; an agent that does not substitute the variable reads it as that directory.

```bash
uv run --frozen --project "${CLAUDE_SKILL_DIR}" \
  python -m scripts.scan_refs ~/.claude/skills --json
```

`--external-urls` on the same scanner lists the external URLs the corpus names,
fence- and placeholder-aware, and exits 0 — it is the input to this skill's other
probe, `python -m scripts.url_liveness --urls-from -` (URL reachability as
`live` / `dead` / `blocked` / `skip`; **`blocked` is not `dead`**). Reachability is
checked by whoever owns the audit, once and serially, never inside parallel batch
agents — `skill-stocktake` Phase 1 is the caller.

Exit code is the code-owned gate: `0` clean, `1` dangling references found, `2`
scan root missing. The scanner is **conservative by design** — it skips template
placeholders (`<your-repo>/x.sh`), illustrative example links (`[](url)`), and
`--directory`-overridden commands, because a false "missing artifact" is worse
than a missed one. Run `--help` for flags; omit `--json` for a human report.

The same run also reports **external skills** (`external` in JSON). Surface these
before any repair is proposed — they set *where* a fix can go — and name the
owner of each (handling per `external` above).

Present each dangling reference with: skill, ref type, the raw reference, the
resolved path, and the line. Do not auto-fix — a dangling reference may mean the
artifact was deleted (remove the reference) **or** renamed (repoint it) **or**,
for a `../`-escaping link, that the skill was authored in a repo and vendored
into the harness (a portability issue per the `skill-creator` skill's
`references/portability.md`). The
repair is a human judgment; surface the fact, let the user decide.

## Phase 3 — Federate the other three dimensions (read, don't re-implement)

For the scanned skills, surface the existing signals so the report is a single
health view — **labelling each value's source**:

- **Utility** — do not read `~/.claude/metrics/skill-usage.jsonl` by hand. The corrections
  that decide whether its numbers mean anything
  live in `usage_stats` (in the sibling `skill-stocktake` skill, when it is installed
  next to this one); run the script once per window:

  ```bash
  uv run --frozen --project "${CLAUDE_SKILL_DIR}/../skill-stocktake" python -m scripts.usage_stats --days 90
  ```

  Where a skill is rarely or never triggered, judge **[LLM]** whether the cause is
  *over-specialized* scope (a trigger so narrow it never fires) versus simply *new* —
  `last_used` is not clipped to the window, so "used 100 days ago" is distinguishable
  from "never". If `measurable` is false, or `span_shorter_than_window` is true, render
  usage as `unmeasured` — never `0`.

  **Enumerate residency-fold candidates**: skills with nonzero `context` (the
  `/skill-doctor` residency column; `-` means the description is already off the listing
  and there is nothing left to fold) and zero `deliberate` use in the window. Their
  description resides in every system prompt without having driven a single selection —
  the description is the fold candidate. Hand the list to the author with the decision axis attached
  (default: add an explicit one-line reference from a related skill / rule, then
  `disable-model-invocation: true` — even a one-line description still resides in the
  system prompt as an unaudited instruction; a one-line description is the
  fallback only when no reference site exists); exclude skills whose window is
  shorter than their age would need (`span_shorter_than_window`, or added days ago).
  This is an enumeration, not a verdict — folding is the author's call.

- **Size** — enumerate SKILL.md bodies over the 500-line limit
  (`wc -l ~/.claude/skills/*/SKILL.md | sort -rn`; limit per skill-creator §3, sourced
  from Anthropic's official best practices as of 2026-08-29 — re-check on doc updates).
  Growth after creation is the case the creation-time gate cannot catch. The verdict on
  whether an oversized body is bloat or load-bearing belongs to skill-stocktake's
  Hygiene question, not here.
- **Risk** — point to the latest `CLAUDE-SECURITY-*/CLAUDE-SECURITY-RESULTS.md`
  if present; if none/stale, recommend running `/claude-security`. Do not
  re-scan for vulnerabilities here.
- **Validation** — note (**missing validators** debt) which scanned skills have
  no `skill-comply` spec and no record of passing `skill-creator`'s gates — the
  fresh-context draft verdict (its §4) and, for a skill with verifiable output, the
  native ablation screen `claude plugin eval <skill dir> --ablation with-without --runs 3`
  (its §5) — i.e. no way to verify their behaviour. Judge **[LLM]** trigger↔body
  consistency only where it is in doubt.

> Not measured: skill *success rate* (did using the skill improve the outcome,
> not just fire?). It needs counterfactuals the harness does not capture; left as
> a known gap rather than a fabricated number.

## Phase 4 — Report & ledger

Render a `skill × dimension` table: `Skill | Compatibility | Utility | Risk |
Validation`, where Compatibility shows the dangling-reference count (the only
hard number), the others show the federated signal or `unmeasured`. List each
dangling reference with its repair options (remove / repoint / portability).

Persist the scan to `${CLAUDE_SKILL_DIR}/results.json` (the `--json`
output) with a real UTC `scanned_at` (`date -u +%Y-%m-%dT%H:%M:%SZ`), so the
next run can diff. Update it inline with Read/Write.

## Related

- Your publish step (the author's harness uses `harness-sync`) — use it to publish this skill to a public repo.
