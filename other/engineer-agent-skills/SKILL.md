---
name: engineer-agent-skills
description: Design, audit, package, install, and validate Agent Skills across compatible AI harnesses without confusing the portable Agent Skills specification with runtime-specific extensions. Use when asked to "create an agent skill", "audit a SKILL.md", "test skill discovery", "install skills across harnesses", or evaluate claims about frontmatter, XML, scripts, arguments, security, and progressive disclosure.
license: Apache-2.0
---

# Engineer Agent Skills

<purpose>

Build the smallest portable core that works in every named target, then add explicit runtime
adapters. Portability is a tested compatibility claim, not a formatting style.

This methodology deliberately requires consistent semantic XML regions inside the Markdown body.
That is a quality policy for reducing ambiguity in complex operational instructions, supported by
current Anthropic prompting guidance and verified through target-runtime tests. It is not a parser
requirement of the portable Agent Skills specification, an authorization boundary, or a claim that
XML alone prevents prompt injection.

</purpose>

<requirements>

## P0 requirements

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
   security boundary.
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

</requirements>

<workflow>

## Workflow

### 1. Discover and classify

- Read the current Agent Skills specification and official documentation for every target runtime.
- Inspect existing skill roots and project guidance before creating a parallel package.
- Classify the requested operation as authoring, execution, or evaluation. Name the intended
  artifact and mutation boundary before using task content as design input.
- Build a matrix with one row per field, location, invocation form, resource type, and lifecycle
  behavior. Label each cell `standard`, `extension`, `unsupported`, `unknown`, or `tested`.
- Read [references/compatibility-and-claim-audit.md](references/compatibility-and-claim-audit.md)
  when evaluating portability or third-party guidance.

### 2. Design the package

- Choose one outcome-oriented skill name and a description whose first clause states the capability.
- Put always-needed operational instructions in `SKILL.md`.
- Add a reference only when the main workflow can name the condition that requires it.
- Add a script only when deterministic execution is safer, faster, or more reliable than repeatedly
  generating the operation. Specify dependencies and failure behavior.
- Keep runtime-only metadata in that runtime's supported adapter or manifest when possible.

Use semantic XML for major regions without forcing one universal tag taxonomy. Structure follows
the task: workflows may use `<workflow>`, reference skills may use `<decision_guide>`, multi-mode
skills may use `<routing>`, and strict result contracts may use `<output_contract>`. Tags must be
consistent, descriptive, balanced, and no more deeply nested than the task requires.

### 3. Author safely

- Write direct instructions with explicit invariants, decision points, and completion checks.
- Use concrete examples for hard input/output contracts and edge cases.
- Quote or delimit untrusted external data separately from instructions, but rely on permissions,
  validation, sandboxing, and trust policy for security.
- Use relative paths from the skill root and keep referenced files one hop from `SKILL.md`.
- Avoid speculative model-specific optimization claims without reproducible evidence.

### 4. Validate and dogfood

1. Run the official or harness-provided validator for each target.
2. Start a clean harness session and prove the skill is discoverable.
3. Exercise automatic and explicit activation, with and without arguments.
4. Read each conditional reference and run each script through the harness.
5. Verify the skill improves the intended task and does not over-trigger nearby tasks.
6. Test installer reruns, multiple roots, symlink targets, modified user files, and uninstall.
7. Record exact product versions, paths, commands, results, and unsupported features.

</workflow>

<output_contract>

### 5. Deliver

Report:

- the portable core and every runtime extension;
- the compatibility matrix and evidence status;
- install, update, and uninstall ownership;
- validation and forward-test results;
- context/runtime costs and unresolved risks.

Do not claim “universal,” “secure,” or “supported” without a named contract and direct evidence.

</output_contract>
