---
name: improve-self
description: "Detect when a missing Agent Skill would have made the current task faster or more reliable, then scaffold a candidate SKILL.md for user review. Use after a non-trivial task when one of these signals fires: the same procedure repeated 3+ times, error recovery required inventing a workflow, the user corrected the approach (not the answer), the agent realized mid-task that a playbook did not exist, or 5+ tool calls produced what should have taken 1-2. Detects which `.{vendor}/` directories exist on the host (project and home), reads every skill and slash command in them before proposing, and never duplicates. Writes candidates into the project's .{vendor}/skills/{name} directory that the running host actually loads, never the home folder. Do NOT use for first-attempt failures, one-off questions, fact gaps that belong in research, or style gaps that belong in rules files. Pass the trace and the signal that fired as arguments; the skill does not reconstruct them from the conversation."
context: fork
metadata:
  author: Serghei Iakovlev
  version: "1.1"
  category: meta
---

# Improving Self by Closing Skill Gaps

This skill turns the trace of just-completed work into a question: *was there a procedure I should have had written down?* When the answer is yes, it scaffolds a candidate Agent Skill into the current project — with the human approving every write.

The discipline is conservative by design. A skill created for a one-off question becomes long-term noise in the activation context of every future task. A skill created without checking existing skills becomes a duplicate and a confusion vector. A skill encoding version-specific or transient behavior becomes a permanent footgun. The bar for creation: a concrete, recurring, procedural gap that survived a check against every existing skill, with the user signing off on the draft.

## Running scripts bundled with this skill

Script paths are resolved relative to **this** SKILL.md, not the agent's CWD. If a relative command (for example `python3 scripts/discover_skills.py`) fails to resolve, prefix it with the directory the platform loaded SKILL.md from.

**Fallback.** If `python3` is missing or the script cannot be located, every procedure here ships a manual alternative — follow that instead.

## What counts as a gap

A gap is **procedural and recurring**. Not every difficulty is a gap.

| Pattern in the trace | Skill-shaped? |
|---|---|
| The agent repeated the same 3-step lookup three times in one task | Yes |
| The agent figured out a non-obvious investigation workflow from scratch and it worked | Yes |
| The agent recovered from an error by inventing a procedure that should be reusable | Yes |
| The user corrected the agent's *approach* with "no, here we always do X first" | Yes |
| The agent realized mid-task it lacked a playbook other agents would also face | Yes |
| The agent did not know a *fact* ("what is the Kafka default port?") | No — research gap, not skill gap |
| The agent failed once and recovered easily | No — one-off, not recurring |
| The task was complex but succeeded smoothly | No — complexity ≠ missing procedure |
| The agent had to consult unfamiliar library docs | No — that is what `research-it` is for |
| The task succeeded without struggle | No — nothing to fix |

Decision rule: **would the agent copy this procedure from memory next time, verbatim?** If yes, write it down. If no, it is not a skill.

## Trigger conditions

Self-assessment runs at the end of a task when **at least one** of these signals is observable in the trace. The signals are concrete; the agent does not need to guess.

1. **Repetition signal.** The agent invoked the same procedural pattern (sequence of tool calls or reasoning steps) three or more times in the task. The third occurrence is the trigger. Example: the agent re-derived "how to find the canonical Postgres source for a behavior" three times across the conversation.
2. **Recovery signal.** The agent hit an error (tool failure, wrong assumption, dead end) and only made progress after inventing a procedure not in any existing skill. The procedure that worked is the candidate. Example: the agent realized mid-task that a particular gRPC server returned proto3 fields with non-default zero-values in a non-obvious way, and worked out a verification pattern.
3. **Correction signal.** The user explicitly corrected the agent on *how* to approach something, not just on the answer. Quoted phrases like "no, here we do X" or "next time, start with Y" are strong. Pure answer corrections ("the value is 16, not 8") are *not* triggers — those are research gaps.
4. **Missing-affordance signal.** The agent noticed mid-task that a needed playbook did not exist anywhere across the `.{vendor}/skills/` directories that actually exist on this host (resolved in Phase 2 Step A). Phrasing in the agent's own reasoning like "I had to discover that …" or "it would help to have a documented procedure for …" is the marker.
5. **Effort-vs-payoff signal.** The task took five or more tool calls for a result that, with the right procedure, would have taken one or two. If the agent can describe the better skill concretely, that skill is the candidate.

If none of these fire, do not run self-assessment. False-positive gaps create churn in the skill library.

## Workflow

### Phase 1 — Restate the gap precisely

Write down, internally:

1. The trigger signal that fired (one of the five above), named.
2. The concrete evidence in the trace: specific tool calls, error messages, user quotes, or repeated patterns. A gap claim without trace evidence is fabricated.
3. The procedure as the agent would write it for itself: numbered steps, with inputs and outputs.

If the procedure runs to more than ten numbered steps before any branching, the gap is too broad. Split it into the narrowest reusable subprocedure. Monolithic skills do not activate precisely (see `make-skill` anti-patterns).

Restate the gap as a single sentence that names the procedural domain. Good: "investigation procedure for verifying Postgres MVCC behavior across major versions." Bad: "Postgres stuff." The narrower phrasing is also the working draft of the new skill's description.

### Phase 2 — Check existing skills (mandatory)

Phase 2 is mandatory. Discovery is three steps so the agent only consults the vendor prefixes it actually reads at runtime — not every `.{name}/skills/` directory that happens to exist on the filesystem.

**Step A — Identify the vendor directories THIS agent reads from.** Use [references/platform-vendors.md](references/platform-vendors.md) to resolve the comma-separated `--vendors` list. It holds the running-agent → vendor mapping, a filesystem-probe fallback for when self-identification fails, and the empty-result rule (skip Step B and treat as "no existing skills to deduplicate against").

**Step B — Hand the resolved list to the discovery script.** Save it into a variable for the script call:

```bash
vendors=<comma-separated names from Step A>
python3 scripts/discover_skills.py --vendors "$vendors"
```

`--vendors` is **mandatory**; unknown names exit `2` with the accepted set listed so the agent can self-correct.

Default output is XML, one `<skill>` element per skill, with `<name>`, `<category>`, `<description>` in a fixed order. For opt-in fields (`--with-type`, `--with-agent`, `--with-path`), alternative formats (`--format json|markdown|csv`), ordering, user-vs-project precedence, exit codes, and the no-python3 bash fallback, see [references/discover-skills-reference.md](references/discover-skills-reference.md).

**Step C — Enumerate the slash commands in the same vendor directories.** A procedure already codified as a command is not a gap, and the discovery script cannot see it: the script scans `.{vendor}/skills/` only, while the host loads `.{vendor}/commands/` alongside it. Skipping this step is how a candidate gets proposed as a skill while an equivalent command sits one directory over, and the report still says "no overlap".

```bash
for v in ${vendors//,/ }; do
  for d in "./.$v/commands" "$HOME/.$v/commands"; do
    [ -d "$d" ] && grep -H '^description:' "$d"/*.md 2>/dev/null
  done
done
```

A command with no `description:` key still counts - read its body before dismissing it.

Read each `description`, from Step B and Step C alike. For each, classify against the candidate gap:

| Comparison | Action |
|---|---|
| Exact or near-overlap with an existing skill or command | Do not create. Either use the existing one (re-read its body) or propose an *edit* to its SKILL.md or command file. Surface this to the user. |
| Partial overlap (existing covers half) | Narrow the candidate to the uncovered delta. Re-state the gap. Loop back to Phase 1. |
| No overlap | Proceed to Phase 3. |

If the existing skill is close but stale or wrong, **do not silently re-author it as a new skill**. Open the original SKILL.md and propose a patch. Duplication is worse than imperfection.

### Phase 3 — Decide whether a skill is the right shape

A skill is the right shape only when all four hold:

- **Procedural** — the answer is steps, not facts.
- **Reusable** — the procedure plausibly applies to at least two future tasks.
- **Self-contained** — it does not hardcode values that change between contexts (versions, paths, customer-specific tokens, ephemeral API endpoints).
- **Testable** — there is a concrete "this worked" condition the agent can check.

If any criterion fails, route the gap via [references/alternatives-to-a-skill.md](references/alternatives-to-a-skill.md). Default to **not creating**. The cost of a skill — its presence in the activation context forever, its description competing in the model's top-of-context scan — exceeds the benefit unless all four hold.

### Phase 4 — Draft the candidate SKILL.md

Use the `make-skill` skill for the authoring discipline (frontmatter rules, body structure, density). This skill is the gap-detection front end; `make-skill` is the authoring back end.

Path: `$PWD/.{vendor}/skills/{name}/SKILL.md` in the **current working project directory**, never the home folder. Pick `{vendor}` with this decision order:

1. **The directory the running agent actually loads.** A skill written where the host does not look is inert, so this outranks every other consideration. Resolve the running agent against [references/platform-vendors.md](references/platform-vendors.md). `.agents/skills/` is the cross-platform convention at project scope, adopted by Codex, Cursor, Gemini CLI, GitHub Copilot, OpenCode, Cline, Warp and Antigravity, and is the right choice when the running agent is one of those. **Claude Code is not one of them: it loads `.claude/skills/` and never reads `.agents/skills/`.** In a project shared across hosts, keep the source under `.agents/skills/` and symlink it into the directory of any host that does not read it, rather than duplicating the file.
2. **A vendor-specific directory** (`.claude/skills/`, `.opencode/skills/`, `.gemini/skills/`, `.github/skills/`, …) when the new skill genuinely depends on that vendor's frontmatter extensions — `disable-model-invocation`, `user-invocable`, `argument-hint`, `context: fork` for Claude; `policy.allow_implicit_invocation` companion file for Codex; `paths`-scoped activation for Cursor, etc. Document the dependency in the skill's own description.
3. **The same vendor directory that holds the currently-active `improve-self`**. Run `find . -path '*/skills/improve-self/SKILL.md' -not -path '*/node_modules/*' 2>/dev/null` to confirm where it lives — that location reflects the project's stated policy. If found in a vendor-specific directory, prefer the same vendor for the new skill so the library stays coherent.
4. **The user's explicit redirect** trumps the above three. If they say "put it in `.cursor/skills/`", do that.

NEVER write to `$HOME/.{vendor}/skills/` — self-generated skills belong to the project, not the user's global library.

Bootstrap the directory with `init_skill.py` from `make-skill`. Then follow the **Workflow** pattern from `make-skill › Phase 4: Body` — for gap-driven skills the natural sections are `Trigger`, `Procedure`, `Validation`, `Anti-patterns`, because they map one-to-one onto Phase 1 trace evidence (trigger signal → `Trigger`, inverted procedure → `Procedure`, success criterion → `Validation`, what went wrong → `Anti-patterns`).

The procedure must be exact enough that running it would have prevented the original difficulty observed in Phase 1's trace evidence. If not, the gap is not closed — refine before hand-off.

### Phase 5 — Hand off for user approval, then verify

Do not silently install. The agent is its own author, executor, and inspector for self-created skills; without an external checkpoint, deprecated APIs get frozen into procedural memory and transient failures become permanent avoidance. Two checkpoints before the skill counts as installed:

1. **Show the user the draft.** State, in this order:
   - The trigger signal that fired and the trace evidence (quote the messages or tool calls).
   - The Phase 2 result: which existing skills were checked, and why none of them covered the gap (or which one is close and should be edited instead).
   - The draft SKILL.md.

   Then ask explicitly whether to write the file. Do not write before the answer is yes.

2. **Validate** after writing:

Use the `validate_skill.py` script from `make-skill` to check the new SKILL.md against the style rules.

If the validator returns errors, fix and re-run. Manual fallback when no validator is reachable: frontmatter parses, `name` matches the directory, description ≤ 1024 chars and third person, body ≤ 500 lines, references one level deep, forward-slash paths only.

The gap is closed when the validator passes and the new SKILL.md sits in the chosen `.{vendor}/skills/<name>/` directory under the project root.

## Anti-patterns

These degrade the skill library and erode trust in the self-improvement loop:

- **Fabricated gaps.** Inventing a recurring pattern that did not actually occur. Defence: every gap claim cites a trace quotation in Phase 1.
- **Over-broad skills.** "Handles all Postgres questions" is monolithic and will not trigger precisely. Defence: name the *procedure*, not the *domain*. When loaded by investigation skills like `sleuth`, the typical gap is a narrow source catalogue or bias-detection pattern for one domain — not a skill called "investigating things" (that is what `research-it` already is).
- **Duplicate skills.** Failing to read existing descriptions - skills *and* slash commands - before proposing. Defence: Phase 2 is non-negotiable.
- **Self-validation.** Treating the agent's confidence in the draft as sufficient quality control. Defence: the user is the external validator before any write, the script-based validator after.
- **Encoding transient or version-specific behavior.** "Library X v2.3 returns a list" rots the moment v2.4 ships. Defence: skills capture *procedure* (how to find out, how to triangulate, how to verify), not facts that change.
- **Skill-shaped facts.** Information that belongs in `AGENTS.md` compressed into an unwieldy skill. Defence: route via [references/alternatives-to-a-skill.md](references/alternatives-to-a-skill.md).
- **Silent installation.** Writing the file before the user has seen the draft. Defence: Phase 5 explicitly forbids it.

