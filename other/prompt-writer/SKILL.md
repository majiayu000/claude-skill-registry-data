---
name: prompt-writer
description: "Write or audit a prompt another Claude will run: system prompts, subagent briefs, skill, command and agent bodies, CLAUDE.md and rules."
when_to_use: "Use whenever you author instruction text a model will follow, even when nobody says prompt."
disable-model-invocation: false
---

# Prompt Writer

You are about to write or edit a prompt another Claude will execute. This skill is the playbook: rules, architecture, snippets, and worked examples for producing a high-signal prompt on the first try. Primary target is Claude Opus 5.5 (`model: opus` on Claude Code 2.1.280), whose documented baseline is Opus 5; the same shapes work on Sonnet 5.5 (`model: sonnet` on 2.1.284) at lower cost and on Fable above it.

Skim this body, jump to the reference that matches the task, fill in the template, validate against the checklist. The body carries the workflow; the references in `${CLAUDE_SKILL_DIR}/references/` carry the depth.

## Ground before you write

Do not author a prompt from your own built-in knowledge alone. Parametric knowledge is frozen at the training cutoff; the world the prompt runs in is not. Two grounding passes come before the first line, every time.

- **Read the actual target.** When the prompt names an existing file, agent, skill, command, or symbol, open it first with Read, Grep, Glob, or `ac:explore`. Editing an existing prompt means reading its current body and the references it points at, not recalling what it likely says. A prompt built on a guessed file shape ships the guess.
- **Verify against fresh sources.** Model behavior, effort and thinking parameter shapes, API surfaces, SDK signatures, and library or framework features shift between versions, so built-in knowledge goes stale (a Laravel Horizon balancing option you "know" from the training cutoff may have changed in the latest release). Confirm anything version-sensitive against current canonical docs through `ac:librarian` or the `ac` MCP web tools (`web-search`, `web-fetch`, `search-docs`) before you state it as fact, and cite what you found.

When your built-in knowledge disagrees with the file or a fresh source, the file and the source win.

## Decision flow

Route by what you are about to produce. Each branch points at a reference for the depth.

```
Writing a SKILL.md body (any Claude Code skill)?
├── YES → use this skill for the prompt body, route the skill SHAPE
│         (frontmatter, scope, invocation, bundling) through `ac:skill-creator`.
└── NO  → continue
        ↓
Writing the body of a slash command (/name [args])?
├── YES → use this skill for the prompt body, route the command SHAPE
│         (arguments, allowed-tools, shell injection) through `ac:command-creator`.
└── NO  → continue
        ↓
Writing a custom subagent definition (.claude/agents/<name>.md)?
├── YES → use this skill for the system-prompt body, route the agent SHAPE
│         (tools, model, permissions, isolation) through `ac:agent-creator`.
│         Then read `${CLAUDE_SKILL_DIR}/references/subagent-prompts.md`.
└── NO  → continue
        ↓
Writing CLAUDE.md, CLAUDE.local.md, or .claude/rules/*.md?
├── YES → use this skill for content tone and structure, route the file SHAPE
│         (scope, paths:, @imports, loading order) through `ac:claude-md-rules-creator`.
└── NO  → continue
        ↓
Briefing a fresh Agent tool call (no custom subagent_type)?
├── YES → `${CLAUDE_SKILL_DIR}/references/subagent-prompts.md`
└── NO  → continue
        ↓
Auditing or improving an existing prompt?
├── YES → `${CLAUDE_SKILL_DIR}/references/anti-patterns.md` FIRST,
│         then `${CLAUDE_SKILL_DIR}/references/architecture.md`.
└── NO  → use the Quick template below; validate against the Quick checklist.
```

## Core principles

The ten rules that change outcomes the most. Detail lives in the references.

1. **Static in system, dynamic in user.** Persona, schema, examples, invariants go in the system prompt so prompt caching can amortize them. Per-request data (the document, the question, the file under review) goes in user messages.
2. **Wrap every distinct block in XML tags.** Claude is fine-tuned to parse XML. Tag boundaries are the only reliable way to separate instructions from data. Use descriptive, consistent names: `<role>`, `<context>`, `<examples>`, `<input>`, `<output_format>`. In a Claude Code body, markdown headings may mark the instruction sections instead; data still goes in tags.
3. **Tell the model what to do; to move it off a default, name the exact behavior.** "Provide concise responses" beats "do not be verbose." When a default must go, a category swaps one default for another; a named list works (Anthropic: 5.5 "is responsive to instructions that name the specific kinds of early stop", such as "a summary that announces the next step instead of taking it").
4. **State scope explicitly, in both directions.** Where a rule must span, say so: "apply to every X, not just the first." Where the task must not widen, say that too: current Opus models can expand scope and over-verify on their own, so name the boundary ("change only these files; report adjacent problems instead of fixing them").
5. **Examples are the highest-leverage tool for gray areas.** 3 to 5 diverse, labeled examples beat any abstract instruction. Wrap each in `<example>` inside `<examples>`. Cover edge cases.
6. **Repeat the top constraint right before generation.** Recency wins. End the prompt with the one or two rules the model must not break.
7. **No "CRITICAL: you MUST" language.** Modern Claude overtriggers on aggressive wording. Plain instructions work; if a rule needs weight, explain the why.
8. **Structured Outputs over prefill.** Prefilling the last assistant message returns a 400 error on Claude 4.6 and later. Use Structured Outputs, tool calls with enums, or wrap the output shape in XML tags inside the user turn.
9. **Set scope before length.** A short prompt with the right scope outperforms a long prompt with hedges. Hedges introduce ambiguity, the model fills it with priors.
10. **The colleague test.** Show the prompt to someone with no context. If they would be confused, the model will be too.

## Standard architecture

Place components in this order. Skipping any is a choice, not a default.

| # | Component | Location | Why this position |
|---|---|---|---|
| 1 | Persona, role, tone | system | Frames the lens. Without it the model defaults to baseline and may hallucinate. |
| 2 | Static rules, schemas, invariants | system | Cacheable; never changes per request. |
| 3 | Few-shot examples (3 to 5) | system | Format must be visible before dynamic input. |
| 4 | Dynamic content (documents, retrieved data, images) | user | Per-request; cannot be cached. |
| 5 | Step-by-step instructions | user | Order in which the model should process the dynamic content. |
| 6 | End-of-prompt reminders | user (last lines) | Top 1 to 3 constraints repeated for recency. |
| 7 | Output format lock | user (last) or Structured Outputs | Final shape of the response. |

For inputs above 20k tokens the order inside the user turn flips: long documents at the very top, instructions and the actual question at the bottom. This can move quality up to 30 percent on multi-document tasks. Full detail in `${CLAUDE_SKILL_DIR}/references/architecture.md`.

## Quick template

Fill this in. Strip components you do not need with intent.

```xml
<!-- SYSTEM PROMPT -->
<role>
You are [persona, one sentence: who, domain, tone].
</role>

<context>
[Static facts the model cannot derive: schemas, business rules, shape of the input. Cacheable.]
</context>

<examples>
  <example>
    <input>[representative input]</input>
    <expected_output>[exactly what the model should produce]</expected_output>
  </example>
  <!-- 2 to 4 more, diverse, covering edge cases -->
</examples>

<output_format>
[Shape: XML tags, JSON schema reference, plain prose, etc.]
</output_format>

<!-- USER MESSAGE -->
<input>
[The actual per-request data]
</input>

<instructions>
1. First, [process the structured part of the input].
2. Then, [interpret the ambiguous part using the structured baseline].
3. Finally, [produce the output in the shape specified above].
</instructions>

<reminders>
- [Top constraint, e.g., "cite the specific input region for every claim"]
- [Scope constraint, e.g., "apply to every section, not just the first"]
</reminders>
```

## Model tuning knobs (Opus 5.5 first)

Anthropic documents `claude-opus-5-5` as a delta over Opus 5: Opus 5 patterns hold unless this section says otherwise. Detail in `${CLAUDE_SKILL_DIR}/references/opus-5-5-tuning.md` (Opus 5.5 deltas), `${CLAUDE_SKILL_DIR}/references/sonnet-5-5-tuning.md` (Sonnet 5.5 deltas) and `${CLAUDE_SKILL_DIR}/references/opus-5-tuning.md` (Opus 5 baseline, Sonnet 5, Haiku 4.5, Fable).

| Knob | Opus 5.5 | Opus 5 | Sonnet 5.5 | Haiku 4.5 |
|---|---|---|---|---|
| Default effort | `medium` | `high` | `high` on the API, `medium` in Claude Code; levels recalibrated from Sonnet 5 | unsupported; never set it |
| Thinking | always on; `disabled` and manual `budget_tokens` both 400 | on; `disabled` only at `high` or below | always on; `disabled` and manual 400; `between_tools` at `high` or below is the floor | manual `budget_tokens` only; adaptive rejected |
| `tool_choice` `any` / `tool` | 400; use `auto` plus `strict: true`, or Structured Outputs | accepted | 400, same fix | - |
| `max_tokens`, long agentic turns | 128k | ~64k at `xhigh` / `max` | 128k | 64k cap |
| Price in / out per MTok | $4 / $20, cache read $0.20 | $5 / $25 | $2 / $10, cache read $0.20 | $1 / $5 |

**Effort is the cost lever, and labels do not port.** Opus 5.5 at `medium` matches Opus 5 at `high`, and at any given label it thinks more than Opus 5. Start at `medium`, try `low` for scoped work, step up only on a measured gain. Lower effort before writing "think less" prose, and drop "think carefully" lines. Change effort per turn with a per-message `output_config`; changing the top-level value breaks the cache.

**Sonnet 5.5 steers by effort level.** At `low` and `medium` it checks in before agentic work is done; at every level it adds tests, docs and small files nobody asked for; at `xhigh` and `max` it starts its own review rounds, with subagents where it can. Each has a one-paragraph fix in `sonnet-5-5-tuning.md`; pick by the level you run.

**Keep the prefix append-only.** Cache reads are 0.05x input on Opus 5.5 (0.1x on Sonnet 5.5) and the cache minimum is 512 tokens, so a long static system prompt is cheap and an edited one is expensive. On both 5.5 models, editing `system` or `tools` mid-session also invalidates earlier thinking blocks. Late rules go in a mid-conversation system message.

**Verbosity.** Not documented for 5.5's general replies. Keep the Opus 5 practice: a positive length target, and deliverable length stated separately from chat length. Effort is not a length lever.

**Scope and delegation.** Opus 5 widens scope, re-verifies finished work, and delegates readily; 5.5 documents no reversal. Name the upper bound, and say when NOT to spawn.

**Unattended runs (5.5).** A progress report can end the turn with no tool call. For loops with no human, name the early stops you do not want (the four-stop paragraph in the 5.5 reference), at the end of the system prompt from turn one. Anthropic scopes it to unattended runs; an interactive setup that measured these stops may adopt it as a stated override.

**No reasoning in the reply (5.5).** "Explain your reasoning, then answer" and `<thinking>` / `<answer>` scaffolds can draw a `reasoning_extraction` refusal. Read `display: "summarized"` thinking instead.

**Assumed unchanged.** Last-turn prefill and non-default sampling parameters return 400 (not restated for 5.5; assume so). 1M context, 128k output.

## When the prompt runs inside Claude Code

What the host already says depends on the model's prompt shape; restate only what that shape lacks. Verbatim inventory in `${CLAUDE_SKILL_DIR}/references/claude-code-conventions.md`.

- **LEAN shape (Opus 5.5, Opus 5, Fable, Mythos) already carries:** markdown rendering, permission denials as signal, hook output as user feedback, mid-conversation system turns as harness, `<pasted_content>` handling, dedicated tools over shell, parallel independent calls, `file_path:line_number`, matching the surrounding code's idiom, confirming hard-to-reverse actions, faithful outcome reports, acting without re-deriving settled facts. Do not restate these.
- **LEAN does not carry** the CLASSIC-only rules: no comments unless the why is non-obvious, no speculative abstraction, no compatibility shims, no handling for impossible cases, no unasked planning files, the exploratory-question rule, UI verification, and the tool-use communication contract. A body that needs one on 5.5 states it in one line.
- **Custom subagents get neither shape.** Their system prompt is the agent body plus environment notes, so every rule the agent follows lives in the body.
- **Delegation on 5.5.** The host no longer suppresses Agent use on 5.5 and its Agent description encourages it; any prompt that holds the Agent tool says when not to spawn.
- **Official examples: match the host's register.** `${CLAUDE_SKILL_DIR}/references/claude-code-builtin-prompts.md` holds Claude Code's own prompt text verbatim, with a Patterns section: `#` headings over short plain sentences, the reason in the same sentence as the rule, named behaviors, the wanted exception stated with the rule, no caps. Write standing instructions that way, and check a body against it so it neither repeats nor silently contradicts the host. Section markers can be headings or XML tags (follow the target's family); data always sits inside XML tags.

## Sibling skills (route the surrounding shape)

This skill stays focused on the prompt itself. The shape around the prompt routes through one of the following sibling skills.

| Producing | Route shape through | Use this skill for |
|---|---|---|
| A SKILL.md body | `ac:skill-creator` | The markdown body that loads when the skill triggers |
| A slash command body (`/name [args]`) | `ac:command-creator` | The body the model executes when the command runs |
| A subagent definition (`.claude/agents/<name>.md`) | `ac:agent-creator` | The system prompt the subagent reads |
| `CLAUDE.md` or `CLAUDE.local.md` | `ac:claude-md-rules-creator` | Project- or user-level standing instructions |
| `.claude/rules/<topic>.md` | `ac:claude-md-rules-creator` | Topic- or path-scoped rule content |
| Direct Agent tool call (no custom subagent type) | (none, just this skill) | The `prompt` field of the Agent call |

When the user request implies any of the rows above, do both: invoke the matching creator for shape, then keep this skill loaded for the prompt body.
## Quick template for common shapes

**Subagent briefing** (Agent tool call). Brief like a smart colleague who just walked in. Goal, what you already learned, surrounding context, length cap, response shape. Full detail in `${CLAUDE_SKILL_DIR}/references/subagent-prompts.md`.

```text
Audit `packages/*/src/**/*.ts` for unused exports.

Context: TypeScript monorepo. "Unused" means zero imports across the monorepo. Use ts-prune or write your own grep-based check.

I have already ruled out: ESLint's no-unused-vars (it does not cross packages).

Report: a list of `file_path:line_number` entries grouped by package. Under 500 words. If you cannot find unused exports with confidence, say so and explain what tooling you tried.
```

**Custom subagent definition** (`.claude/agents/<name>.md`): bounded description, explicit tools, decisional steps, a locked output contract, and every rule the agent needs restated in its body. For a reviewer or advisor on 5.5, ask for coverage-first findings that each carry their evidence or say "unverified"; the 5.5 system card names asserting unverified inferences as fact as the top epistemic issue. Full template in `${CLAUDE_SKILL_DIR}/references/worked-examples.md` Example 3, alongside document extraction, code-review briefing, long-document RAG, slash command body and meta-prompt.

## Snippet library (most useful starters)

Categorized copy-paste building blocks. Mix and match; each is a fragment, not a finished prompt. Full library in `${CLAUDE_SKILL_DIR}/references/snippets.md`.

**Hallucination control.**

```text
Never speculate about code you have not opened. If the user references a specific file, read it before answering. For every factual claim, cite the source: `file_path:line_number` for code, a document tag for retrieved data, or "general knowledge" for things not in the input.
```

**Verification.**

```text
Before you finish, verify your answer against:
- [criterion 1, specific and falsifiable]
- [criterion 2]
If verification fails, revise and verify again. Only return when all criteria pass.
```

Parallel tool use and context-compaction snippets live in the reference; inside Claude Code the lean prompt already carries both (`# Harness`, `# Context management`), so add them only to API prompts or subagent bodies.

## Anti-patterns (audit existing prompts for these)

Surface-level set; the full audit checklist with the why behind each fix is in `${CLAUDE_SKILL_DIR}/references/anti-patterns.md`.

| Anti-pattern | Fix |
|---|---|
| Negative-only instructions ("do not be verbose") | Positive scope: "Provide concise, focused responses." Naming the exact default to avoid is different and works (principle 3). |
| Aggressive "CRITICAL / MUST / ALWAYS" wording | Plain instructions; explain the why if a rule needs weight. |
| Prefilled last assistant message | Use Structured Outputs or wrap output in XML tags. |
| Unstated scope: "apply this rule" | "Apply to every X, not just the first." |
| No upper bound on scope | Name the boundary; current Opus models widen scope and over-verify on their own. |
| Vague verbs: "format properly", "handle errors" | State the format and the error contract exactly. |
| Hidden context (prompt relies on chat history) | Restate load-bearing facts inside the prompt itself. |
| Static and dynamic mixed in user message | Move static to system; dynamic stays in user. |
| Long documents at the bottom of the user turn | Move documents to the top for inputs over 20k tokens. |
| "Based on your findings, fix the bug" (in subagent prompts) | Specify file paths, line numbers, exact change; do not delegate synthesis. |
| Stale anti-laziness scaffolding from older models | Remove; trust current Opus defaults. |
| 4.8-era fan-out encouragement ("spawn multiple subagents when fanning out") | Invert it; Opus 5 and 5.5 already delegate readily. Say when NOT to spawn. |
| Lowering `effort` to shorten output | Effort is not a length lever. State a length target instead. |
| Effort label copied from an Opus 5 config onto 5.5 | Re-sweep from `medium`; 5.5 thinks more per label. |
| Effort label copied from a Sonnet 5 config onto Sonnet 5.5 | Re-sweep; the levels are recalibrated. `medium` for well-specified agentic coding, `high` for harder work. |
| "Think carefully" or "explain your reasoning, then answer" on 5.5 | Remove; raise effort. The second can draw a `reasoning_extraction` refusal. |
| `thinking: { type: "enabled", budget_tokens }` | Returns 400 on Opus 4.7 and later and on Sonnet 5 and 5.5; omit `thinking` or send `adaptive`. |
| `thinking: { type: "disabled" }` | 400 on both 5.5 models at every effort (Sonnet 5.5 takes `between_tools` instead, at `high` or below); on Opus 5 allowed only at `high` or below. |
| `tool_choice` `any` / `tool` on 5.5 | Returns 400; `auto` plus `strict: true`, or Structured Outputs. |
| Editing `system` or `tools` mid-session | Breaks the cache and, on 5.5, earlier thinking blocks; append a mid-conversation system message. |
| A body that assumes CC's classic code-style rules on 5.5 | State the rule in one line; the lean prompt does not carry it. |
| Top-level `output_format={...}` parameter | Move into `output_config={"format": {...}}`. |
| `betas=["effort-2025-11-24"]` header carried over | Drop it; effort is GA. |
| `client.beta.messages.create` for thinking or effort | Use `client.messages.create`. |

## Pre-flight checklist

Before shipping a prompt:

- [ ] Persona, domain, tone stated in the system prompt.
- [ ] Static content (schema, examples, invariants) in system; dynamic in user.
- [ ] Every data block in named XML tags; instruction sections marked consistently (tags or headings).
- [ ] 3 to 5 diverse examples covering edge cases.
- [ ] Instructions ordered: process structured input first, ambiguous second.
- [ ] End-of-prompt reminders restate the top 1 to 3 constraints.
- [ ] Scope stated explicitly ("every X, not just the first").
- [ ] No "CRITICAL / MUST / ALWAYS" language.
- [ ] If input above 20k tokens: documents at top, question at bottom.
- [ ] Effort set explicitly via `output_config={"effort": ...}`, chosen by measurement (from `medium` on Opus 5.5, by a fresh sweep on Sonnet 5.5), never copied across models.
- [ ] Thinking shape matches the model: omitted or `adaptive` on Opus 5.5, Opus 5, Sonnet 5.5, Sonnet 5 and Fable; `disabled` only on Opus 5 at `high` or below; `between_tools` only on Sonnet 5.5 at `high` or below; manual `budget_tokens` only on Haiku 4.5.
- [ ] On 5.5: no forced `tool_choice`, no reasoning-in-reply scaffold, `max_tokens` sized for thinking.
- [ ] Main-thread text (skill, command, CLAUDE.md) restates what the reader's shape lacks and nothing it carries. An agent body restates every rule it needs, except what the subagent Notes already give it (`claude-code-builtin-prompts.md`, section 5).
- [ ] No `effort` set for Haiku 4.5 (the parameter is unsupported on that model).
- [ ] Every fenced command in the body has been run, in the shell it will actually run in, and its output matches what the surrounding prose claims (see `${CLAUDE_SKILL_DIR}/references/claude-code-conventions.md`).
- [ ] Length controlled by an explicit target, not by lowering effort.
- [ ] Scope boundary named, not just scope span.
- [ ] Output shape lock uses `output_config.format` (Structured Outputs), tool call with enum, or XML wrap; not the deprecated top-level `output_format` or last-assistant prefill.
- [ ] No `effort-2025-11-24` beta header; `client.messages.create` (not `client.beta`).
- [ ] Colleague test passes.

## References

| File | Load when... |
|---|---|
| `${CLAUDE_SKILL_DIR}/references/architecture.md` | Designing message structure, XML tag names, long-context layout, example design. |
| `${CLAUDE_SKILL_DIR}/references/claude-code-builtin-prompts.md` | Official examples, and the duplicate check for anything that runs inside Claude Code: verbatim 2.1.280 system prompt text per shape and model, bundle sections, CLAUDE.md wrapper, subagent defaults, Agent tool text, plus the patterns worth copying. |
| `${CLAUDE_SKILL_DIR}/references/opus-5-5-tuning.md` | Targeting `claude-opus-5-5`: effort calibration, thinking always on, forced tool use, thinking-block binding, unattended early stops, time signals, pasted content, what Claude Code 2.1.280 gives 5.5. |
| `${CLAUDE_SKILL_DIR}/references/sonnet-5-5-tuning.md` | Targeting `claude-sonnet-5-5`: recalibrated effort, `between_tools`, early check-ins versus unrequested additions versus self-started review by effort level, search over training knowledge, JSON answers, what Claude Code 2.1.284 gives 5.5. |
| `${CLAUDE_SKILL_DIR}/references/opus-5-tuning.md` | Tuning effort, thinking, verbosity, scope, subagent spawning, code-review re-tuning; the 4.8-to-5 inversions; per-model deltas for Sonnet 5, Haiku 4.5, Fable 5. |
| `${CLAUDE_SKILL_DIR}/references/claude-code-conventions.md` | Writing prompts that run in the Claude Code harness: agents, slash commands, hooks, harness rules. |
| `${CLAUDE_SKILL_DIR}/references/subagent-prompts.md` | Briefing a fresh subagent, designing a `subagent_type`, lookup vs investigation, length caps. |
| `${CLAUDE_SKILL_DIR}/references/snippets.md` | Need a copy-paste building block (verbosity, parallel tools, hallucination control, output format, frontend, identity, scope). |
| `${CLAUDE_SKILL_DIR}/references/anti-patterns.md` | Auditing or debugging a prompt that produces wrong output. |
| `${CLAUDE_SKILL_DIR}/references/worked-examples.md` | Want a complete prompt as a starting template (document extraction, code review, custom agent, long-document RAG, slash command, meta-prompt). |

Source material for these references is Anthropic's canonical documentation served as raw markdown by appending `.md` to the URL (the suffix returns LLM-friendly raw markdown instead of the JS-rendered HTML page). Two hosts: API and model docs at `https://platform.claude.com/docs/en/<path>.md`, Claude Code docs at `https://code.claude.com/docs/en/<path>.md`. The former `docs.claude.com` host now redirects to `platform.claude.com` and does not serve the Claude Code pages. Anchor URLs cited inline in each reference file. When canonical docs conflict with observed CLI behavior, trust the live binary.
