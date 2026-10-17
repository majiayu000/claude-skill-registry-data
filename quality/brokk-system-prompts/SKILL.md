---
name: brokk-system-prompts
description: Write precise, structured agent definitions, system prompts, and skill files that produce reliable, controllable agent behavior.
---

# System Prompts

## Purpose

Write system prompts (agent definitions, role prompts, SKILL.md files) that produce reliable, controllable agent behavior. A prompt is a program, not an essay — judge it by behavioral coverage, not prose aesthetics.

The core insight: **structure first; style second.** A prompt can be concise, precise, and imperative and still be catastrophically incomplete; a prompt that covers all structural dimensions but is verbose is merely suboptimal. Be complete on behavioral constraints, scope, failure handling, and I/O contracts; be concise on redundancy and narrative. Length is a consequence of required coverage, not a target.

## When to Use

- When authoring, editing, or evaluating a system prompt, agent definition, or role prompt.
- When writing or revising a SKILL.md file (a SKILL.md is itself a system prompt).
- When reviewing a prompt for completeness before it ships.
- **Not** for user-facing chat messages or one-shot instructions — only for the standing prompt that defines an agent.

## Workflow

Apply the 23 principles below in order: **define scope → cover structure → order and draft → refine style → add conditional layer → context and validate → self-exemplify.** Tiers A–B (structure) are mandatory; C is the finishing pass; D is conditional; E–F always apply.

### A. Structural Coverage (apply first)

- **1. Define scope before writing instructions.** State the role in one sentence, its inputs, its outputs, and at least three things it must NOT do. Use these as a checklist: every instruction must map to the role; anything outside scope must be explicitly excluded.
- **2. Specify input and output contracts explicitly.** Define what the agent receives (format, source, fields) and produces (format, structure, required elements, length bounds, delimiters). The output contract is the agent's interface to its consumer — treat it like an API. Without I/O contracts, the agent cannot be tested, integrated, or debugged.
- **3. Specify behavior for each input class — and a default for the unanticipated.** Enumerate distinct input classes (at minimum: primary, out-of-scope, ambiguous) and map each to a behavior. For unanticipated inputs, specify a default: ask for clarification, decline, or fall back to a defined behavior.
- **4. Specify failure, degradation, and escalation.** For every major action, state what the agent does when the action fails, a tool is unavailable, or input is malformed. Define explicit escalation triggers — conditions under which the agent stops and requests intervention. Default failure behavior is honesty: state inability rather than fabricate.
- **5. State hard boundaries as prohibitions, early.** What the agent must NEVER do matters more than what it should do — negative constraints prevent catastrophic failure. Place them prominently early in the prompt where attention is strongest.
- **6. Specify invariants — properties that must hold for every output.** State what must be true of every output without exception (e.g., "never fabricate sources," "always include a confidence level"). The agent has no durable state of author intent beyond the prompt — every invariant must be stated, never assumed.
- **7. Make decision points explicit and specify the rule.** Identify every point where the agent must choose between options (clarify vs. proceed, format A vs. B) and specify the rule. Unspecified decision points are where behavior diverges most from author intent — the agent defaults to its training prior.
- **8. Review the constraint set for conflicts.** For each pair of constraints, ask: "Is there an input for which both apply?" If yes, specify precedence, or redefine the constraints to apply to disjoint input classes.

### B. Ordering and Structure (apply during drafting)

- **9. Order by behavioral priority, not chronology.** Identity and hard boundaries first (primacy — strongest attention); decision rules and behavioral specs second; operational procedures third; reference material last. Within a tier, chronological order is fine for genuinely procedural workflows. Never bury a critical constraint in the middle.

  Before: "First, the agent receives input. Then it validates. Then it checks permissions. Then it processes. Do not modify production data."

  After:

  ```markdown
  ## Boundaries
  - Never modify production data.

  ## Role
  You are a processing agent. You receive validated input and produce structured output.

  ## Workflow
  1. Validate input format and fields.
  2. Check caller permissions.
  3. Process and return result.
  ```

- **10. Structure with named, hierarchical sections.** Use markdown headers for major sections (## Role, ## Inputs, ## Outputs, ## Rules, ## Boundaries, ## Failure Handling). Separate identity, behavior, constraints, and failure modes — do not interleave them. No instruction should be buried in a paragraph longer than three lines.
- **11. Minimize instruction coupling.** Each instruction section should be self-contained. If an instruction depends on another, inline the dependency rather than cross-reference ("see step 3 above") — the model attends to nearby tokens more reliably than distant ones.
- **12. Match voice to function.** Never refer to the agent in the third person ("the agent," "it") — address it as "you." Drop the hedge "possibly"; apply voice by rule, not suggestion.
  - Imperative for actions and procedures (default): "Validate inputs."
  - Declarative for identity and scope: "You are a code-review agent. Your scope is correctness."
  - Conditional for context-dependent rules: "If the input is malformed, mark it invalid."
  - Prohibitive for hard boundaries: "Never modify production data."
  - Explanatory for rationale that must be understood, not just followed: "Never resume a prior review session — prior reviews anchor the reviewer to intermediate judgments."

### C. Style and Refinement (apply to structurally complete drafts)

- **13. Maximize signal density.** Every sentence must carry a constraint or decision rule the agent would not otherwise infer. Test: if removing a sentence changes nothing about behavior, remove it; if it leaves a behavior unspecified, keep it.
- **14. Be precise operationally: what, when, output.** Every instruction must specify what to do, under what condition, and what the output looks like. Avoid abstract verbs (handle, manage, process) without specifying the action. Test: "How many different outputs could satisfy this instruction?" If "many," narrow it.

  Before: "Handle errors gracefully."

  After: "If an API call returns an error, log the message, retry once after 2 seconds, and if the retry fails, return `{"status": "error", "detail": "<error message>"}`."

- **15. One instruction per line — do not compound.** Compound instructions (multiple verbs per sentence) reduce adherence — the LLM may skip the middle action. Split atomically; use a numbered list for sequential steps.
- **16. State positive alternatives for prohibitions.** "Use formal, professional language" beats "Do not use informal language." Reserve pure prohibitions for hard boundaries where no acceptable alternative exists.
- **17. Include examples for non-obvious behaviors and output formats.** Lead with constraints; use examples to disambiguate what prose alone cannot. Never rely on examples alone — generalization from examples is uncontrolled. One annotated example communicates more than five rules for behaviors that resist concise description.
- **18. Annotate non-obvious constraints with brief rationale.** One sentence per constraint — the agent doesn't need to agree, but understanding why helps it apply the constraint in unanticipated situations. This also serves maintainers.

### D. Conditional Layer (apply when the agent is user-facing)

- **19. If the agent interacts with human users, additionally specify**: tone (register, formality, address); uncertainty transparency (distinguish known from inferred; flag speculation); ambiguity consultation (ask rather than silently choose when interpretations diverge materially); downstream-impact awareness (parties affected by outputs who did not interact directly). Mandatory for user-facing agents; optional for machine-facing subagents with pure contract interfaces.

### E. Context and Validation (apply always)

- **20. Read existing exemplars before writing.** Read at least two existing system prompts in the target system. Follow the established structural pattern (sections, formatting, conventions); do not invent structure when one exists.
- **21. Be aware of context-window and model constraints.** If the target model is known, check context window, tool/function-calling support, and system-prompt length limits. If unknown, keep under ~2000 tokens. Place critical constraints at the top and bottom (primacy/recency), never buried mid-prompt.
- **22. Simulate before finalizing.** Walk the prompt through three scenarios: (1) normal case, (2) edge case (tool failure, ambiguity, missing input), (3) worst case (contradictory instructions, impossible request). For each, ask: "What would the agent do? Is that intended?" Patch wherever simulation reveals a gap. A prompt is a program — verify it before shipping.

### F. Meta-Consistency

- **23. The skill file must embody these principles.** A SKILL.md is itself a prompt processed by an implementation agent's attention mechanism. It must be structured with headers, attention-ordered (critical first), signal-dense, and free of the defects it prohibits (hedges, compounding, buried constraints). A skill that preaches structure but is a wall of text will not be followed.

## Quality Criteria

- **Removability**: Can you remove any sentence without losing information? If yes, remove it.
- **Precision**: How many outputs could satisfy each instruction? If "many," narrow it.
- **Coverage**: Specifies scope, I/O contracts, input-class behavior, failure behavior, boundaries, invariants, decision rules.
- **Conflict-free**: For each constraint pair, precedence is specified where inputs overlap.
- **Simulated**: Walked through normal, edge, and worst cases — agent does what's intended in all three.
- **Voice**: Imperative for actions, declarative for identity, conditional for logic, prohibitive for boundaries; no third-person references to the agent.
- **Failure behavior**: Every major action states what the agent does on failure.
- **Boundaries**: Stated as prohibitions and placed early.
- **Exemplar-conformance**: Follows the structural pattern of existing prompts in the target system.

## Anti-Patterns

- **Style-first drafting**: Polished prose before scope, contracts, and failure behavior are defined. Style cannot rescue missing structure.
- **"Possibly" hedges**: Suggestions give the agent license to ignore inconsistently. Commit or abstain — never hedge.
- **Third-person voice**: "The agent validates inputs" introduces referential ambiguity. Address the agent as "you," always.
- **Chronological ordering for non-procedural workflows**: Buries critical constraints mid-prompt where attention is weakest. Order by behavioral priority.
- **Buried constraints**: Critical prohibitions hidden mid-paragraph. Place boundaries first.
- **Missing failure behavior**: An agent without failure handling either crashes or hallucinates.
- **Missing boundaries**: No prompt is safe without explicit prohibitions on what the agent must NEVER do.
- **Missing I/O contracts**: Without explicit input and output contracts, the agent is untestable and unintegrable.
- **Compound instructions**: Multiple verbs per sentence cause middle actions to be skipped. Split atomically.
- **Examples without rules**: Generalization from examples is uncontrolled. Lead with constraints; use examples to disambiguate.
- **Abstract verbs**: "Handle," "manage," "process" without specifying action, condition, and output format.
- **Verbose redundancy**: Restating the same constraint in different words. Maximize signal density — remove redundancy, not specification.
- **Cross-referenced dependencies**: "See step 3 above" is attention-fragile. Inline the dependency.
- **Invented structure**: Inventing a novel section pattern when the target system has an established convention. Follow existing exemplars.
