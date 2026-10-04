---
name: ai-skill-builder
description: Guides creation, audit, and improvement of portable Agent Skills using the shared
  SKILL.md format and Anthropic's established methodology, without confusing the portable
  specification with runtime-specific extensions. Use when the user wants to "create a skill",
  "create an agent skill", "build a skill", "make a new skill", "write a new skill",
  "improve an existing skill", "audit my skill", "audit a SKILL.md", "refine my skill",
  "test a skill", "test skill discovery", "install skills across harnesses", "package a skill
  for distribution", or needs guidance on skill structure, semantic XML regions, progressive
  disclosure, description quality, frontmatter, scripts, arguments, security, testing,
  cross-harness compatibility, or distribution.
allowed-tools: Read Write Edit Bash WebSearch WebFetch
metadata:
  version: 1.3.0
---

# AI Skill Builder

<purpose>

Build Agent Skills using the shared `SKILL.md` format and Anthropic's methodology: the smallest
portable core that works in every named target, plus explicit runtime adapters. Portability is a
tested compatibility claim, not a formatting style.
`references/sources.md` cites host documentation for Claude Code, Codex, and Qwen Code; every
other host is untested here, so verify the one you target (Step 1).

This methodology deliberately requires consistent semantic XML regions inside the Markdown body.
That is a quality policy for reducing ambiguity in complex operational instructions, supported by
current Anthropic prompting guidance and checked by the forward tests in Step 4. It is not a parser
requirement of the portable Agent Skills specification, an authorization boundary, or a claim that
XML alone prevents prompt injection.

**Primary methodology source**: "The Complete Guide to Building Skills for Claude"
(Anthropic, January 2026)
- PDF: https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf
- Extracted text: `references/ai-skill-builder-guide.md`

**Portable format source**: https://agentskills.io/specification

---

## Quick Start

To create a skill from scratch, follow the 4-phase process below.
To improve an existing skill, read `references/refining-skills.md`.
To validate structure, run `scripts/audit-skill.sh`.

**Invoke with:** ask for `ai-skill-builder`; hosts may expose it as
`/ai-skill-builder`, `$ai-skill-builder`, or through their skills picker.

</purpose>

<requirements>

## P0 requirements

Every skill this methodology produces meets all thirteen. Cite them by ID in audits and reviews.

1. **SKILL-REQ001-discover-target-runtimes.** Identify exact products, versions, invocation modes,
   install roots, trust boundaries, and filesystem semantics before authoring.
2. **SKILL-REQ002-separate-standard-from-extensions.** Keep the Agent Skills specification,
   runtime extensions, and project conventions in separate columns. Never present a
   Claude-, Codex-, Copilot-, Gemini-, or framework-specific field as universal.
3. **SKILL-REQ003-use-valid-portable-core.** Put a required `SKILL.md` in a directory whose name
   matches its portable `name`; include a specific `description` that says what the skill does and
   when to use it. Use standard optional fields only when needed.
4. **SKILL-REQ004-use-semantic-xml-regions.** Wrap every major operational region in consistent,
   descriptive XML tags inside the Markdown body, such as `<purpose>`, `<requirements>`,
   `<workflow>`, `<examples>`, and `<output_contract>`. Keep Markdown inside those regions and
   literal source in fenced code blocks. This mandatory methodology rule aims for the
   highest-quality instruction separation; it is not an Agent Skills parser requirement or a
   security boundary. `scripts/audit-skill.sh` fails a body with no region, an unbalanced or
   mis-nested tag, or a `## ` heading outside every region.
5. **SKILL-REQ005-design-progressive-disclosure.** Keep the activation description precise and the
   main workflow concise. Move genuinely conditional detail into focused, directly linked
   references; keep reusable automation in scripts and output materials in assets.
6. **SKILL-REQ006-preserve-operational-context.** Every reference or script must say when to use it,
   what inputs it accepts, what it returns or changes, and how failure is reported. Avoid deep
   reference chains.
7. **SKILL-REQ007-make-invocation-correct.** Test automatic activation and explicit invocation.
   Where a runtime supports parameters, test empty, positional, named, quoted, Unicode, invalid,
   and large inputs. Do not assume another runtime implements the same substitution syntax.
8. **SKILL-REQ008-minimize-tool-authority.** Treat skills and bundled scripts as executable
   dependencies. Request the least authority needed, validate inputs, preserve approval prompts
   where practical, and never describe prompt delimiters as prompt-injection prevention.
9. **SKILL-REQ009-validate-every-harness.** Validate discovery, load, references, scripts,
   arguments, symlinks, duplicate resolution, updates, and removal in each supported harness.
   Passing one parser does not prove cross-runtime compatibility.
10. **SKILL-REQ010-preserve-user-state.** Installation and uninstall must own exact generated
    paths, preserve manual edits, support multiple configured skill roots, and remove only
    installer-owned links or files.
11. **SKILL-REQ011-measure-context-and-runtime-cost.** Record discovery metadata size, loaded
    instruction size, conditional reference cost, script time/memory/I/O, and duplicate loading.
    Treat line and token targets as heuristics unless a target runtime makes them normative.
12. **SKILL-REQ012-forward-test-real-tasks.** Use realistic positive, negative, ambiguous, and
    adversarial prompts. Check task outcome, not merely whether the skill appeared in a list.
13. **SKILL-REQ013-separate-authoring-from-execution.** Classify whether the task is to change the
    skill, use the skill to produce an artifact or result, or evaluate the skill from evidence.
    Runtime inputs, generated outputs, examples, and dogfood observations do not become skill
    instructions unless an explicit authoring decision accepts and generalizes them.

Region names follow the task rather than one universal taxonomy: workflows use `<workflow>`,
reference skills may use `<decision_guide>`, multi-mode skills `<routing>`, strict result contracts
`<output_contract>`, inline reference material `<reference>`, and pointers to bundled files and
sources `<resources>`. Tags must be consistent, descriptive, balanced, and no more deeply nested
than the task requires. The standard-versus-extension matrix, the claim audit, and the per-host
validation receipt live in `references/portability-and-claim-audit.md`.

</requirements>

<workflow>

## How It Works

Four-phase methodology from the Anthropic guide. Each phase carries a **Definition of Done**:
the condition that must hold before the next phase starts.

| Phase | Activity | Definition of Done |
|-------|----------|--------------------|
| 1: Planning & Design | Define target hosts, use cases, category, success criteria | Criteria are measurable and the category is chosen |
| 2: Implementation | Create folder, write SKILL.md, add resources | `audit-skill.sh` reports no failures |
| 3: Testing | Triggering, functional, performance, compatibility, forward tests | Every named host passes with a validation receipt; baseline recorded |
| 4: Distribution | Package, document, publish | Install verified from a clean root |

Phase 1 covers Steps 1–2 below; Phases 2–4 correspond to Steps 3–5.

How long a phase takes depends on who or what runs it, so this skill states no wall-clock
estimates and the skills you build should not either.

---

## Skill Creation Workflow

### Step 1: Discover Requirements

**Research the domain first** — use the host's web tools to verify current best practices
before writing instructions. Outdated guidance is worse than none: an agent follows it
confidently.

**Retain all sources**: record every URL consulted with a note of what it confirmed.
Unsourced guidance cannot be verified or updated.

For research strategies, source quality standards, and the required Sources section
format: `references/research.md`

1. Classify the request: authoring (change the skill), execution (use the skill to produce a
   result), or evaluation (judge the skill from evidence). Name the artifact and the mutation
   boundary before using task content as design input (SKILL-REQ013).
2. Identify the problem and target users
3. Identify every target host and version, its discovery root, invocation form, and reload
   behavior. Mark unknowns as unknown rather than guessing. Inspect existing skill roots and
   project guidance before creating a parallel package.
4. Define 2-3 concrete use cases
5. Set measurable success criteria (time saved, errors reduced, quality improved)
6. Choose a skill category:

| Category | INPUT → OUTPUT | Examples |
|----------|---------------|---------|
| **1: Document & Asset Creation** | Data/specs → document, code, report | API test generator, meeting notes summarizer |
| **2: Workflow Automation** | Task params → completed multi-step process | Deploy pipeline, code review workflow |
| **3: MCP Enhancement** | MCP tool outputs → smarter orchestration | Smart file search, BigQuery assistant |

For in-depth category guidance: `references/categories.md`
For interactive discovery questions: `references/discovery.md`

### Step 2: Design Structure

Design using progressive disclosure — 3 loading levels:

| Level | When loaded | Target length | Content |
|-------|------------|---------------|---------|
| 1: Metadata | Always (~100 words) | name + description | Trigger conditions |
| 2: SKILL.md body | When skill triggers | under 5,000 words (ideally under 2,000) | Core workflow + pointers |
| 3: references/ files | As needed | Unlimited | Deep detail, schemas, examples |

For progressive disclosure writing tips and success metrics: `references/best-practices.md`

### Step 3: Implement

**Critical Rules:**
- ✅ File MUST be named `SKILL.md` (not README.md)
- ✅ Folder name MUST be **kebab-case** — no spaces, no capitals (`my-skill` not `My Skill`)
- ✅ YAML frontmatter MUST include `name` and `description`; put a version under `metadata`
- ✅ Description MUST include specific trigger phrases — what users SAY to activate the skill
- ✅ Description must be **under 1024 characters** (hard limit — longer descriptions are truncated)
- ✅ No XML angle brackets (`<` or `>`) in any frontmatter field — a host restriction from
  Anthropic's skill guide, not a YAML rule; the body is unaffected
- ✅ Body: every major section sits inside a balanced, descriptive XML region on its own line
  (`<purpose>`, `<requirements>`, `<workflow>`, `<examples>`, `<output_contract>`), Markdown
  inside, literal source in fenced code blocks (SKILL-REQ004). The H1 title may stay outside.
- ❌ NO README.md inside the skill folder — all docs go in SKILL.md or references/
  (Exception: a README.md at the GitHub repo ROOT, outside the skill folder, is fine for GitHub.)
- ❌ NO spaces or underscores in folder names (`my_skill` → `my-skill`)

**Frontmatter: required fields**:
```yaml
---
name: your-skill-name          # kebab-case only; no spaces, capitals, or underscores
description: What it does. Use when user asks to "specific phrase", "another phrase".
             # MUST include: what it does + when to use it (trigger conditions)
             # Under 1024 characters. No XML angle brackets.
             # Do NOT start with "claude" or "anthropic" (reserved namespaces).
---
```

For every optional field (`license`, `compatibility`, `allowed-tools`, `metadata`) with
host-portability notes: `references/best-practices.md`

**Positioning language** ("generate tests 87% faster") belongs in the repo README, never in
`description`. See `references/best-practices.md`.

**Folder structure** (annotated Claude Code standalone example: `references/best-practices.md`,
section "Folder Structure Patterns"):

| Directory | Load into context? | Use for |
|-----------|-------------------|---------|
| `references/` | Yes, as needed | Schemas, API docs, policies, workflow guides |
| `references/examples/` | As needed | Working code users copy and adapt |
| `scripts/` | No (run directly) | Validators, scaffolders, utilities |
| `assets/` | No (used in output) | Images, fonts, HTML templates the skill pastes into output |

Note: Plugin skills (in `plugin-name/skills/`) may place `examples/` at the top level — that is
plugin-dev convention. For standalone `~/.claude/skills/` skills, put examples inside `references/`.

To scaffold a new skill: `bash scripts/scaffold-skill.sh my-skill-name`
(set `SKILLS_DIR` to target another host's root)
To start from template: copy `references/examples/SKILL-template.md`

### Step 4: Test

Five testing approaches (run in order):

1. **Triggering tests** — verify the agent activates on expected phrases and not on unrelated requests
2. **Functional tests** — validate the skill's core workflow produces correct output for known inputs
3. **Performance tests** — measure improvement over baseline (time saved, error reduction, consistency)
4. **Compatibility tests** — verify discovery, explicit invocation, reference loading, script
   execution, and duplicate/name resolution on every named host and version. Start a clean
   session for each host, run the host's own validator where one exists (Codex ships
   `skill-creator/scripts/quick_validate.py`), test installer reruns, multiple roots, symlink
   targets, modified user files, and uninstall, and record a validation receipt per host
   (`references/portability-and-claim-audit.md`).
5. **Forward tests** — realistic positive, negative, ambiguous, and adversarial prompts; judge the
   task outcome, not whether the skill appeared in a list, and check that it does not
   over-trigger nearby tasks (SKILL-REQ012)

**Debugging trigger issues**:
```
Ask the agent: "When would you use the [skill name] skill?"
```
The agent should quote its description back. Adjust based on what's missing or too vague.

**Fixing undertriggering**: Add more specific trigger phrases and relevant technical terms.

**Fixing overtriggering**: Add negative triggers to the description:
```yaml
description: Processes PDF legal documents for contract review. Use for "review this contract",
  "analyze legal document", "extract contract clauses". Do NOT use for general PDF viewing,
  image extraction, or non-legal documents (use doc-converter skill instead).
```

For the full diagnosis-and-fix guide covering all four failure modes: `references/troubleshooting.md`

To validate structure:
```bash
bash scripts/audit-skill.sh /path/to/YOUR-SKILL
```

For automated quality review on a host that provides Anthropic's `skill-creator` skill:
```
"Use the skill-creator skill to review the skill I just built and suggest improvements"
```
Claude Code with the `plugin-dev` plugin installed also offers a `skill-reviewer` agent that checks description quality.

For detailed test case templates and the Testing Triangle methodology: `references/testing.md`

### Step 5: Distribute

Three channels — individual install into a host's skills root, organization-wide deployment,
and the Messages API — are described with commands in `references/distribution.md`, together
with the GitHub repo layout, the README template, versioning, and community channels.

An installer that places the skill must own exact generated paths, preserve manual edits,
support multiple configured skill roots, and remove only its own links or files
(SKILL-REQ010). Report the portable core and every runtime extension, the compatibility matrix
and its evidence status, install/update/uninstall ownership, validation and forward-test results,
and context/runtime costs. Do not claim "universal," "secure," or "supported" without a named
contract and direct evidence.

</workflow>

<pitfalls>

## Common Pitfalls

| Pitfall | ❌ Wrong | ✅ Correct |
|---------|---------|---------|
| File naming | `my_skill/README.md` | `my-skill/SKILL.md` |
| Description field | Outcome-focused: `"generates tests 87% faster"` | Trigger phrases: `"create a skill", "improve my skill"` |
| README positioning | Trigger phrases in GitHub README | Outcome-focused: `"generate tests 87% faster"` |
| No progressive disclosure | Monolithic wall of text | 3-level: hook (50-100w) → workflow (200-400w) → detail |
| No testing | Write → publish immediately | Triggering + functional + performance + compatibility + forward tests |
| Missing success criteria | "Build a skill that helps with APIs" | "Cut API test writing from 3 h to 45 min, median of 3 runs" |
| Feature-focused description | "Uses OpenAPI parser and Jinja2 templates" | Trigger phrases + concise capability summary |
| Unmeasured claim | "Works with any agent host", a bare "40% faster" | The hosts and versions you tested; the workload, baseline, and unit behind the number. The 87% in the rows above is correct placement only if it was measured |

---

## Refining Existing Skills

Signs a skill needs refinement:
- File named README.md or folder has underscores/capitals (P0 — Claude cannot find it)
- Missing YAML frontmatter (P0 — Claude cannot auto-activate it)
- Description is outcome-focused instead of trigger-phrase format (P1)
- SKILL.md is over 5,000 words (P0 on Claude hosts, where Anthropic's guide reports degraded quality above it; a heuristic elsewhere, per SKILL-REQ011)
- SKILL.md is over 2,000 words with no references/ files (P1 — detail belongs in references/)
- Wall of text with no progressive disclosure structure (P1)
- No semantic XML regions, an unbalanced tag, or a `## ` heading outside every region (P1 —
  `scripts/audit-skill.sh` fails it; see SKILL-REQ004)

For the 5-step refinement process (audit → prioritize → fix → validate → document), migration
scenarios, and before/after examples: `references/refining-skills.md`

</pitfalls>

<resources>

## Additional Resources

### Reference Files (loaded as needed by the agent — when to open it → what it gives back)

- **`references/research.md`** — before writing any domain instruction → source-tier judgement, `sources.md` entries
- **`references/discovery.md`** — when requirements are unclear → 22-question plan: name, triggers, use cases, inputs, outputs, tests
- **`references/categories.md`** — when Step 1's category is not obvious → category, structure, Level 2 template
- **`references/best-practices.md`** — while writing body and frontmatter → description format, every optional field, level targets, 6 anti-patterns
- **`references/patterns.md`** — when 4 phases are not enough → orchestration, multi-MCP, refinement loops, runtime branching, domain rules
- **`references/testing.md`** — at Step 4 → T1-T6 triggering cases, F1-F4 functional cases, baseline comparison, per-host compatibility steps, forward-test kinds
- **`references/troubleshooting.md`** — when a built skill misbehaves → fixes for no trigger, over-trigger, skipped instructions, context overload
- **`references/refining-skills.md`** — when improving an existing skill → P0-P3 audit, migration checklist
- **`references/distribution.md`** — at Step 5 → distribution channels, repo layout, README, versioning
- **`references/portability-and-claim-audit.md`** — when a skill targets more than one host, or a claim about frontmatter, XML, roots, symlinks, or security needs checking → standard-vs-extension matrix, claim audit table, per-host validation receipt
- **`references/sources.md`** — when checking what a claim rests on, or adding one → citations, and claims with no retrievable source
- **`references/changelog.md`** — when changing ai-skill-builder itself → its release history, not the history of the skill you are building

### Superseded package
- **`engineer-agent-skills`** — an earlier standalone skill. Its P0 requirements
  (SKILL-REQ001–013), portable-standard vs runtime-extension claim matrix, per-host validation
  receipt, and install/uninstall ownership rules now live in this skill; do not install both.

### Scripts (run directly — do not load into context)
- **`scripts/audit-skill.sh`** — structure smoke test. Gate on zero FAILs; the percentage
  scores only the mechanically decidable checks, and proxy checks are listed unscored.
  ```bash
  bash scripts/audit-skill.sh /path/to/YOUR-SKILL
  ```
- **`scripts/scaffold-skill.sh`** — create a skill directory that already passes the audit
  ```bash
  SKILLS_DIR=~/.claude/skills bash scripts/scaffold-skill.sh my-skill-name
  ```

</resources>
