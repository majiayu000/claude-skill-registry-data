---
name: make-skill
description: "Use when creating, improving, comparing, evaluating, reviewing or packaging Agent Skills following the agentskills.io specification. Also use when deciding whether a skill is the right solution vs MCP servers, Claude Rules Files, or AGENTS.md. Handles SKILL.md authoring, frontmatter optimization, description writing, progressive disclosure, platform targeting, invocation control, vendor-specific extensions, and distribution."
metadata:
  author: Serghei Iakovlev
  version: "2.3"
  category: meta
---

# Creating Agent Skills

Author Agent Skills against the agentskills.io specification. A skill is a self-contained directory of instructions, scripts, and resources that turns a general-purpose agent into a specialist for one focused domain.

## Core Philosophy

**Context is shared.** Your skill's tokens compete with the system prompt, conversation history, other skills, and the user's request. Once SKILL.md loads it stays in context for the rest of the turn. Every line must earn its place.

**The agent is already smart.** Add only context it lacks. Cut explanations of well-known concepts (PDFs, for-loops, HTTP, JSON) and any sentence whose absence would not confuse a competent agent.

**Reason over command.** Prefer "Use pdfplumber because it handles multi-column layouts and rotated text better than alternatives" to "ALWAYS use pdfplumber". The reasoning becomes the rubric for cases the skill did not anticipate.

**Write for the agent, not the human reader.** The audience is an LLM ingesting tokens, not a person browsing a wiki page. Optimize for density and clarity, not visual aesthetics. Visual decoration — hard wraps that imply meaningful line breaks, blockquotes around examples, redundant "why this works" paragraphs after every code block, three-deep ladders of indented bullets, decorative `Tip:`/`Note:` wrappers around single sentences — costs tokens and earns nothing. See [references/writing-patterns.md](references/writing-patterns.md) § Density for dense-vs-decorative examples.

## Skill Anatomy

```plaintext
skill-name/
├── SKILL.md       # required: YAML frontmatter + markdown body
├── scripts/       # optional: executable code; output enters context
├── references/    # optional: docs loaded on demand
├── assets/        # optional: templates, schemas, images
└── agents/        # optional: per-vendor sidecars, e.g. Codex's openai.yaml
```

Only `SKILL.md` is required. Drop empty directories. `agents/` holds vendor sidecar config rather than skill content; its one current occupant is Codex's `agents/openai.yaml`, described in [references/frontmatter-fields.md](references/frontmatter-fields.md).

## Running scripts bundled with this skill

Script paths are resolved relative to **this** SKILL.md, not the agent's CWD. If a relative command fails, prefix it with the directory the platform loaded SKILL.md from.

**Fallback.** If `python3` is missing or a script cannot be located, every procedure here ships a manual alternative — follow that instead.

## Workflow

### Phase 1: Scope the skill

Before writing, answer all of:

1. **Is a skill the right tool?** See [references/skills-ecosystem.md](references/skills-ecosystem.md). Live data, auth, write operations on external systems → MCP. Always-on rules → custom instructions. Project facts → AGENTS.md. User-triggered templates → prompt files. Reusable procedural how-to → skill.
2. **What single capability** does this skill provide? One focused domain. If the answer requires "and", split.
3. **Target platform(s).** Claude Code only? Codex only? Multiple? Determines which frontmatter fields are available — see § Platform targeting below.
4. **Invocation model.** Model-invoked (the agent decides when to load it), user-invoked only (`/skill-name` or `$skill-name`), or both? Determines how the description should be written and which fields you set — see § Invocation model below and Phase 3.
5. **What does the agent lack?** Add only that.
6. **What does success look like?** Output format, validation step, quality bar.

If the user is converting an existing workflow ("turn this into a skill"), extract: steps, tools, corrections, I/O formats. Confirm the four answers above before scaffolding.

If the user is porting a skill from another repository, treat the source as a structural template, not a text to translate. Before adapting a line of it, inventory the target's equivalents: its test runner and the exact flags that invoke it, the annotation or comment schema its existing artifacts already use, its CI gates and their thresholds, its dependency-automation config, and where durable rationale actually lives — a decisions directory, or whatever file stands in for one when none exists. Encode what the target already does. A faithful port of the source's conventions is a foreign body in the new repo: it will read as authoritative while contradicting every artifact around it, and the first agent to follow it produces work that matches nothing.

### Phase 2: Initialize

```bash
python3 scripts/init_skill.py <skill-name> --path <output-directory>
```

**Fallback.** Create the directory manually with the skill name; add a `SKILL.md` from the template in Phase 3 plus only the subdirectories you actually need.

### Phase 3: Frontmatter

```yaml
---
name: skill-name
description: "What this skill does AND when to use it. Max 1024 chars."
---
```

**`name` rules** (must match the parent directory):

- 1-64 chars; lowercase alphanumeric and single hyphens
- No leading/trailing/consecutive hyphens
- No reserved words (`anthropic`, `claude`)
- Prefer gerund: `processing-pdfs`, `analyzing-data`, `testing-code`

#### Description by invocation model

The description's *purpose* changes depending on who invokes the skill. Get this wrong and the description is either dead tokens or a missed trigger.

| Invocation             | What the description is for                                                                     | Style                                                                                          |
| ---------------------- | ----------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| Model-invoked          | The model scans descriptions of every installed skill at startup to decide which to load.       | What it does + explicit triggers ("Use when ..."). Edge cases. Slightly pushy. Negative triggers if it over-fires. |
| User-invoked only      | The slash-command picker / `$skill` autocomplete shows it to the user. The model never sees it. | Terse, accurate label of what the skill does. No "Use when ..." triggers. No marketing copy. The user already knows what they typed. |
| Both                   | The model decides whether to auto-load; the user can also force-invoke.                         | Triggers for the model, kept concise so the user-facing label is still readable.               |

**Invocation is a frontmatter decision, not a guess:**

- **Claude Code.** `disable-model-invocation: true` removes the description from the model's context entirely. Triggers in it are dead tokens. `user-invocable: false` does the inverse — only the model invokes; users do not see it.
- **OpenAI Codex.** `policy.allow_implicit_invocation: false` in `agents/openai.yaml` makes the skill explicit-only (`$skill-name`); triggers in the description are equally dead.
- **Cross-platform.** No standard equivalent. Either rely on description-driven discovery or ask the user to invoke explicitly.

**A skill that runs in its own context must say so in the description.** When a skill is configured to execute in an isolated context — forked into a subagent rather than inline in the caller's turn — it begins with none of the invoking conversation: not the task, not prior findings, not the files already read. Only the isolated copy ever reads the body, so an explanation buried there reaches no one who needs it. The description is the sole surface the caller sees, so it must state both that the skill starts fresh and what the caller has to hand over, or callers will invoke it expecting their task to carry across and pay for a run that does something unrelated. One sentence is enough:

```yaml
description: "... Runs in its own context and cannot see the calling conversation; name the target and the goal in the arguments."
```

**Always third person.** Descriptions are injected into the system prompt. "Processes PDFs", not "I can help you process PDFs".

**No XML tags, no `[TODO`, ≤ 1024 characters.**

**Negative triggers** for model-invoked skills that fire too broadly:

```yaml
description: "Advanced statistical analysis for CSV files. Use for regression, clustering, hypothesis testing. Do NOT use for basic data exploration, formatting, or simple aggregation."
```

**Debug a model-invoked description by asking the agent**: "When would you use the [skill] skill?" Compare the agent's quoted understanding with your intent.

For the full optional-field reference (`license`, `compatibility`, `metadata`, `allowed-tools`, plus Claude Code and Codex extensions), see [references/frontmatter-fields.md](references/frontmatter-fields.md).

### Phase 4: Body

The body loads when the skill activates and stays in context for the rest of the turn. Keep it under 500 lines; split surplus into reference files.

**Pick a structure:**

| Pattern     | Best for             | Key feature                              |
| ----------- | -------------------- | ---------------------------------------- |
| Workflow    | Sequential processes | Step-by-step with checklist              |
| Task-based  | Tool collections     | Grouped by operation type                |
| Reference   | Standards/specs      | Organized by domain                      |
| Conditional | Branching logic      | Decision tree pointing to references     |

See [references/writing-patterns.md](references/writing-patterns.md) for examples, freedom calibration, multishot prompting, checklists, script integration, and progressive disclosure.

**Match freedom to fragility:**

- High freedom (creative tasks, code review): general direction, trust the agent
- Medium freedom (reports, analysis): templates with adaptation guidance
- Low freedom (migrations, format ops): exact scripts, exact sequence

**Writing principles:**

- Imperative: "Extract text with pdfplumber", not "You can extract text"
- One default approach per task; mention alternatives only when context demands
- Concrete I/O examples beat verbal descriptions for teaching style
- Consistent terminology: pick one term ("field", not "field" / "control" / "box")
- Workflows: ship a checklist the agent can copy and tick off

**Feedback-loop pattern** for quality-critical operations:

```
1. Make the change
2. Validate: <command>
3. On failure: read error, fix, re-validate
4. Proceed only when validation passes
```

When a script is unavailable, give the agent a manual checklist with the same checks.

### Phase 5: Bundle resources

`scripts/` — executable code for deterministic operations. Output enters context; the source does not. Handle errors with helpful messages; document inputs, outputs, exit codes; test before bundling.

`references/` — markdown loaded on demand. Keep one level deep from SKILL.md (chained references read as `head -100` previews and lose information). Files over 100 lines need a table of contents. Split by domain, not by size.

`assets/` — templates, images, schemas used in output generation. Not loaded for reasoning.

### Phase 6: Validate

```bash
python3 scripts/validate_skill.py <path-to-skill>
```

The validator is invocation-aware: it skips trigger-keyword warnings when `disable-model-invocation: true` is set, and warns if a user-invoked-only description still contains `Use when ...` triggers.

Use `--warnings-as-errors` in CI to require every checked skill to be convention-clean. Keep warnings non-blocking during drafting when they help identify work still in progress.

**Fallback.** Manual check:

- Frontmatter parses; `name` and `description` valid
- `name` matches directory; ≤ 64 chars; lowercase + hyphens; no reserved words
- Description ≤ 1024 chars, third person, no XML tags
- Triggers present iff model-invoked
- Body ≤ 500 lines
- References one level deep
- Forward slashes only

### Phase 7: Test and iterate

A skill is not done until tested with real prompts.

1. **Single hard task.** Pick the worst case the skill must handle. Run it repeatedly. Fix what breaks. Faster signal than broad coverage.
2. **Triggering tests** *(model-invoked skills only)*. 10-20 queries: should-trigger obvious, should-trigger paraphrased, should-not-trigger. Target 80-90% correct activation. Under-trigger → add phrases. Over-trigger → narrow scope or add negative triggers.
3. **Functional tests.** Run the same request 3-5 times. Steps in correct order; tool calls succeed; output format correct. Variance reveals ambiguity.
4. **Performance comparison.** Same task with and without the skill. Messages exchanged, tool failures, total tokens. If no metric improves, simplify or delete.
5. **Iterate.** Read the agent's reasoning, not just the output. Wasted steps, missed instructions, confusion → tighten the relevant section. Generalize from feedback rather than overfitting.

For automated runs, place evals in `evals/evals.json`:

```json
{
  "skill_name": "my-skill",
  "evals": [
    {"id": 1, "prompt": "...", "expected_output": "...", "assertions": ["Output includes X"]}
  ]
}
```

## Progressive Disclosure

Skills load in three tiers:

1. **Metadata** (~100 tokens): `name` + `description` for every installed skill at startup
2. **Instructions** (< 5000 tokens recommended): SKILL.md body, loaded on activation, retained for the rest of the turn
3. **Resources**: bundled files loaded only when referenced

A model-invoked description fights at ~100 tokens. A user-invoked-only description fights for slash-menu legibility. The body should be comprehensive but lean.

## Invocation model

Three modes, controlled by frontmatter:

| Mode              | Set                                                                     | Effect                                                                                            |
| ----------------- | ----------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| Model + user      | nothing (default)                                                       | Description in model context; appears in slash menu; both can invoke.                             |
| User-only         | `disable-model-invocation: true` (Claude Code) / `policy.allow_implicit_invocation: false` (Codex) | Description **not** in model context; appears in slash menu; only user invokes.                   |
| Model-only        | `user-invocable: false` (Claude Code)                                   | Description in model context; **hidden** from slash menu; only the model invokes.                 |

**Pair invocation control with the right neighboring fields:**

- User-only skills (`/commit`, `/deploy`, `/send-slack-message`) often want `argument-hint` for autocomplete UX, `allowed-tools` to skip permission prompts, and `arguments` for positional args.
- Model-only skills (background context like `legacy-system-conventions`) want a strong description with triggers — that is the only thing the model will see at startup.
- Both-mode skills should keep the description tight enough to read in the slash menu while still containing triggers.

## Platform targeting

Which platform a skill targets decides which frontmatter fields exist for it, where it installs, and how it ships. The cross-platform versus single-vendor decision table, the per-vendor extension lists, the storage matrix, and precedence live in [references/platform-targeting.md](references/platform-targeting.md). Open it at Phase 1 question 3 and before setting any vendor-only field.

## Distribution

Three publishing channels carry a finished skill to other machines: skills.sh, the `.skill` package, and the Claude Code plugin marketplace. Their commands and layout requirements are in [references/platform-targeting.md](references/platform-targeting.md) § Distribution.

## Reviewing an existing skill

When the user asks to review or improve a skill, run the five-step audit in [references/reviewing-skills.md](references/reviewing-skills.md) in addition to mechanical validation. Its step order is load-bearing, so do not start midway.

## Anti-patterns

Failure modes are graded Critical, High impact, and Medium impact in [references/anti-patterns.md](references/anti-patterns.md). Load it before writing the description and again before finishing the body: the Critical tier names the three ways a skill fails to activate at all.
