---
name: context-budget
description: Audits Claude Code context window consumption across agents, skills, MCP servers, rules, and CLAUDE.md files — identifies bloat and redundant components and produces prioritized token-savings recommendations. Use when a session feels sluggish or degraded, after adding skills/agents/MCP servers, before adding more components, or when the user runs /context-budget or asks how much context headroom remains. Do NOT use for API billing/spend questions or for shortening a single response — this audits loaded-component overhead, not output length or account cost.
origin: ECC
---

# Context Budget

Analyze token overhead across every loaded component in a Claude Code session and surface actionable optimizations to reclaim context space.

## When to Use

- Session performance feels sluggish or output quality is degrading
- You've recently added many skills, agents, or MCP servers
- You want to know how much context headroom you actually have
- Planning to add more components and need to know if there's room
- Running `/context-budget` command (this skill backs it)

**When NOT to use:** API token billing or per-call cost questions (that is account spend, not context overhead) · trimming one long response (that is output style) · auditing a repo you have not read — every number in the report must come from a measurement run this session, never from memory of a past audit.

## Inputs

Required before starting — verify each root actually exists (`ls -d`), never assume:

- **Component roots**: project-level `.agents/`, `.claude/`, and `.Codex/` trees, each scanned for `agents/`, `skills/`, and `rules/` subdirectories
- **MCP config**: `.mcp.json` (project) and/or user-level MCP settings — only top-level `mcpServers` is read
- **CLAUDE.md chain**: project + user-level CLAUDE.md files
- Optional: a verbosity request from the user (`--verbose`)

Absent-input rule (fail closed, bug-230): a root that does not exist is reported as **ABSENT** in the report — never estimated, never silently skipped, never given an invented number. If *no* root exists at all, stop and report that there is nothing to audit; zero components found is a finding, not a pass.

## Procedure

### Step 1 — Inventory

Scan all component directories and estimate token consumption. Run the measurement command in **Verification** below — every number in the report traces to that run, not to recall.

**Agents** (`agents/*.md`)
- Count lines and tokens per file (words × 1.3)
- Extract `description` frontmatter length
- Flag: files >200 lines (heavy), description >30 words (bloated frontmatter)

**Skills** (`skills/*/SKILL.md`)
- Count tokens per SKILL.md
- Flag: files >400 lines
- Check for duplicate copies in `.agents/skills/` — skip identical copies to avoid double-counting

**Rules** (`rules/**/*.md`)
- Count tokens per file
- Flag: files >100 lines
- Detect content overlap between rule files in the same language module

**MCP Servers** (`.mcp.json` or active MCP config)
- Count configured servers and total tool count
- Detect whether tool search/deferred loading is enabled before estimating resident overhead
- Use ~500 tokens per tool only as potential upfront schema overhead when deferral is disabled
- Flag: servers with >20 tools, servers that wrap simple CLI commands (`gh`, `git`, `npm`, `supabase`, `vercel`)

**CLAUDE.md** (project + user-level)
- Count tokens per file in the CLAUDE.md chain
- Flag: combined total >300 lines

### Step 2 — Classify

Sort every component into a bucket:

| Bucket | Criteria | Action |
|--------|----------|--------|
| **Always needed** | Referenced in CLAUDE.md, backs an active command, or matches current project type | Keep |
| **Sometimes needed** | Domain-specific (e.g. language patterns), not referenced in CLAUDE.md | Consider on-demand activation |
| **Rarely needed** | No command reference, overlapping content, or no obvious project match | Remove or lazy-load |

### Step 3 — Detect Issues

Identify the following problem patterns:

- **Bloated agent descriptions** — description >30 words in frontmatter loads into every Task tool invocation
- **Heavy agents** — files >200 lines inflate Task tool context on every spawn
- **Redundant components** — skills that duplicate agent logic, rules that duplicate CLAUDE.md
- **MCP over-subscription** — >10 servers, or servers wrapping CLI tools available for free
- **CLAUDE.md bloat** — verbose explanations, outdated sections, instructions that should be rules

### Step 4 — Report

Produce the context budget report:

```
Context Budget Report
═══════════════════════════════════════

Total estimated overhead: ~XX,XXX tokens
Context model: Claude Sonnet (200K window)
Effective available context: ~XXX,XXX tokens (XX%)

Component Breakdown:
┌─────────────────┬────────┬───────────┐
│ Component       │ Count  │ Tokens    │
├─────────────────┼────────┼───────────┤
│ Agents          │ N      │ ~X,XXX    │
│ Skills          │ N      │ ~X,XXX    │
│ Rules           │ N      │ ~X,XXX    │
│ MCP tools       │ N      │ ~XX,XXX   │
│ CLAUDE.md       │ N      │ ~X,XXX    │
└─────────────────┴────────┴───────────┘

WARNING: Issues Found (N):
[ranked by token savings]

Top 3 Optimizations:
1. [action] → save ~X,XXX tokens
2. [action] → save ~X,XXX tokens
3. [action] → save ~X,XXX tokens

Potential savings: ~XX,XXX tokens (XX% of current overhead)
```

In verbose mode, additionally output per-file token counts, line-by-line breakdown of the heaviest files, specific redundant lines between overlapping components, and MCP tool list with per-tool schema size estimates.

Tag every number in the report with its evidence scope: measured this session = `[repro]`; word-count estimate = `[inferred]` (the ×1.3 heuristic is an approximation, not a token count). Present estimates as estimates — never as measured readings.

## Verification

1. **The inventory numbers come from a run, not from memory.** From the repo root:

   ```bash
   python3 - <<'EOF'
   import json
   from pathlib import Path

   total = 0
   for root in (Path(".agents"), Path(".claude"), Path(".Codex")):
       if not root.is_dir():
           print(f"{root}: ABSENT — report as absent, do not estimate")
           continue
       for component in ("agents", "skills", "rules"):
           component_root = root / component
           if not component_root.is_dir():
               print(f"{component_root}: ABSENT — report as absent, do not estimate")
               continue
           files = list(component_root.rglob("*.md"))
           est = int(sum(len(p.read_text(errors="ignore").split()) for p in files) * 1.3)
           total += est
           print(f"{component_root}: {len(files)} .md files, ~{est:,} estimated tokens")

   mcp = Path(".mcp.json")
   if mcp.is_file():
       servers = json.loads(mcp.read_text()).get("mcpServers", {})
       print(f".mcp.json: {len(servers)} servers configured")
   else:
       print(".mcp.json: ABSENT — report as absent, do not estimate")
   print(f"TOTAL (file overhead estimate): ~{total:,} tokens")
   EOF
   ```

   **PASS:** exits 0 and prints one line per root plus a `TOTAL` line; every root count/token figure in the report matches this output, and any root printed as `ABSENT` appears as absent in the report. `[repro]`

2. **Estimates are labeled as estimates.** The ×1.3 word heuristic is `[inferred]`. The authoritative loaded-context reading is the session's own `/context` output (a Claude Code built-in the *user* runs) — when a `/context` reading is available, cross-check the report against it and prefer it; when it is not, the report must say "estimate", never present the heuristic as a measured reading. **PASS:** no unlabeled number in the report — each carries `[repro]` or `[inferred]`.

3. **Savings claims are falsifiable.** After the user applies a recommendation (e.g., removes a component), re-run the step-1 command. **PASS:** `TOTAL` drops by approximately the claimed saving (±20%). A recommendation whose removal produces no delta was a false finding — retract it and log it.

## Examples

### Worked example (this repo, run 2026-07-29)

Step-1 command executed from `/Users/theceo/DevSkyy/.claude/worktrees/glimmering-crafting-shannon` — observed output:

```
.claude/agents: 19 .md files, ~22,629 estimated tokens
.claude/skills: 350 .md files, ~584,239 estimated tokens
.claude/rules: 5 .md files, ~2,108 estimated tokens
.mcp.json: 2 servers configured
TOTAL (file overhead estimate): ~608,976 tokens
```

Reading: `.claude/skills` dominates at ~96% of file overhead `[repro]` — but raw file size is *potential* load, not *loaded* load: skills load on invocation, while every agent `description` and MCP tool schema is resident in-session. So the actionable lever here is agent-description and MCP-schema trimming, not deleting skill files. That distinction is exactly what step 2 of Verification protects.

### Illustrative dialogues (format only — numbers are placeholders, never reuse them)

**Basic audit**
```
User: /context-budget
Skill: Scans setup → 16 agents (12,400 tokens), 28 skills (6,200), 87 MCP tools (43,500), 2 CLAUDE.md (1,200)
       Flags: 3 heavy agents, 14 MCP servers (3 CLI-replaceable)
       Top saving: remove 3 MCP servers → -27,500 tokens (47% overhead reduction)
```

**Verbose mode**
```
User: /context-budget --verbose
Skill: Full report + per-file breakdown showing planner.md (213 lines, 1,840 tokens),
       MCP tool list with per-tool sizes, duplicated rule lines side by side
```

**Pre-expansion check**
```
User: I want to add 5 more MCP servers, do I have room?
Skill: Current overhead 33% → adding 5 servers (~50 tools) would add ~25,000 tokens → pushes to 45% overhead
       Recommendation: remove 2 CLI-replaceable servers first to stay under 40%
```

## Failure modes

- **Numbers from memory instead of measurement** — quoting token counts from a past audit or from training-data intuition. Every figure must trace to a step-1 run this session; a stale count is a hallucination with a decimal point.
- **Fail-open on an absent root** (bug-230 pattern) — a missing `.claude/agents/` silently contributing 0 reads as "no agent overhead" when the truth is "not measured". Absent = reported ABSENT, never zero.
- **Estimate presented as measurement** (bug-287 pattern — evidence scope must cover claim scope) — the ×1.3 heuristic is `[inferred]`; claiming "your MCP servers cost exactly N tokens" requires the session's real `/context` reading, not arithmetic on file sizes.
- **Double-counting mirrored skills** — identical copies under `.agents/skills/` counted twice inflate the total and manufacture fake savings. De-duplicate by content before summing.
- **Conflating potential load with resident load** — a 500-line skill that never triggers costs ~0 in-session; a 40-word agent description costs its full weight in *every* Task invocation. Ranking by raw file size alone inverts the real priority (see Worked example).
- **Recommending removal of a component that is actually load-bearing** — a "rarely needed" classification from step 2 is `[inferred]` until grepped: a component referenced by CLAUDE.md, an active command, or another skill is not removable. Cite the grep before recommending deletion.
- **A counting run that dies is not a count** — if the step-1 script errors mid-scan, its partial TOTAL is an artifact, not a result. Fix and re-run; never report a partial as the audit.

### Callability model

The report must treat all discovered roots as callable inventory, not implicit resident context.
Do not report zero as success for a missing root; report `ABSENT` and keep commands explicit.

## Best Practices

- **Token estimation**: use `words × 1.3` for prose, `chars / 4` for code-heavy files
- **MCP is the biggest lever only without deferral**: with tool search enabled, registered tools remain callable while full schemas load on demand
- **Agent descriptions are loaded always**: even if the agent is never invoked, its description field is present in every Task tool context
- **Verbose mode for debugging**: use when you need to pinpoint the exact files driving overhead, not for regular audits
- **Audit after changes**: run after adding any agent, skill, or MCP server to catch creep early
