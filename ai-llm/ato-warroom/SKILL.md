---
name: ato-warroom
version: 1.3.0
description: |
  Before any material decision — code chunk, plan, strategy, design,
  scope cut, push to GitHub — convene a war-room. The session driver
  takes the CEO seat: frame the tradeoff, summon specialist seats from
  whatever agent roster the user has built, dispatch a cross-family
  voice via `ato dispatch` so priors actually disagree, decide. A
  failure-mode filter (wrong assumptions / overcomplexity / orthogonal
  edits / imperative-over-declarative — Karpathy's four are one good
  default, swap in your own) runs on every dispatch.

  Place in the v2.16 stack: war-rooms DECIDE before code starts;
  `ato-mission` EXECUTES the work between decisions (multi-step,
  goal-driven, persisted across days); `ato-review` VERIFIES the
  resulting commits. Use a war-room for the design verdict, hand the
  verdict to a Mission, review the merged result.

  Fires before: sending a code draft to the user as final, opening a
  PR, pushing to a remote-tracking branch, committing >50 LOC of
  behavior change, or delivering a plan or strategic recommendation as
  the final answer.
allowed-tools:
  - Bash
  - Read
  - Edit
  - Write
  - Skill
---

## What this skill is

A **tool**, not a stack-specific procedure. The war-room mechanism
works with whatever agent roster you've built (via `ato-make-agent` or
hand-authored) and whatever methodology you want layered on top. It
doesn't assume gstack, Claude Code, or any specific specialist set —
those are useful starting points referenced as examples below, not
requirements.

The mechanism in one paragraph: when a material decision is in front
of you, frame it as a tradeoff (A vs B with named costs), summon two
or more agents whose domain the decision touches, force at least one
to run on a different model family so priors diverge, apply a
failure-mode filter to the prompt template, then pick a position and
record the audit trail in your deliverable.

## War room ≠ session — pick the right shape for the question

ATO captures multi-AI work under **two distinct shapes**. Picking the
wrong one wastes the round.

|  | **Session (sequential)** | **War room (parallel)** |
|---|---|---|
| **How it stores** | One `sessions` row + N `session_turns` rows | N `execution_logs` rows sharing a `war_room_id` UUID |
| **Conversation shape** | Turn 2 sees turn 1's reply via history replay. Turn 3 sees both. Each new turn can react to and build on prior turns. | Each seat fires standalone — **no seat sees any other seat's reply**. Independent first-pass priors. |
| **What it captures** | Decision evolution: how a proposal sharpened across rounds | Variance: how N different LLMs view the same question cold |
| **Cross-runtime** | One anchor runtime; turns from other runtimes append as cross-runtime turns (Phase 6 Slice B) | Each seat IS a different runtime — that's the whole point |
| **Lifecycle** | `Open → Closed`; `ato sessions close` runs a coordinator LLM over the transcript and emits `auto_title` + `summary` + `tags` + `category` + `team` + `project_id` | No lifecycle. Each dispatch is done the moment it returns. No close, no summary. |
| **Concurrent inserts** | Sequential by definition — `session_turns` has `PRIMARY KEY (session_id, turn_index)` so two parallel inserts would collide on `max+1` | No shared-table race — every dispatch writes to its own `execution_logs` row |
| **Use this when** | Refinement, escalation, ratification, "let me see what each seat would say *given* the prior seat's reply" | Wedge discovery, falsifier-finding, "what would these LLMs say *without* seeing each other" |
| **CLI** | `ato sessions new --runtime <r>` → `ato dispatch <r> --session <sid>` (one at a time) | `WR=$(uuidgen)` → `ato dispatch <r> --war-room-id $WR` (N in parallel) |
| **Desktop card** | Coord ★ + participants badges, persona cluster, summary, lifecycle chip, category/team/project | `⚔ war room` marker, **co-equal** seat badges (no Coord/+), participant count, sum cost |
| **Click-into** | Full transcript view (WhatsApp bubbles + cost-receipts panel) | Vertical stack of per-seat cards (one runtime + one agent + one prompt + one response per card) |

**The picking heuristic:** ask whether you want each seat to *react* to the others (session) or each seat to *not be influenced* by the others (war room). If the answer is "I don't know yet — I want to see both," run the **hybrid**: war room first for breadth, then a session with the synthesis as the opening turn for depth. That's the default for any non-trivial decision.

**Symptom-to-shape table:**

| Symptom | Pick |
|---|---|
| "I want variance — what would these LLMs say from cold?" | War room |
| "Every seat agreed in R1 and that worries me" | War room with a generalist (no `--agent`) added — its raw priors break agreement-by-anchoring |
| "I need to ratify a decision; each seat should react to the prior ones" | Session |
| "The conversation needs to converge — the last turn should be the synthesis" | Session |
| "I'm comparing one model vs another on the same task" | War room of size 2 |
| "I'm running a multi-day decision with multiple rounds" | One session, multiple rounds. Don't fragment. |
| "I want to see if all the LLMs hallucinate the same thing" | War room — independence is the whole signal |
| "I want to capture cost/quality variance for a procurement decision" | War room — receipts side-by-side |

**The `session_turns` PRIMARY KEY constraint is why we have both shapes.** If you try to fire N parallel `ato dispatch --session <id>` calls simultaneously, two of them will compute the same `max(turn_index) + 1` and one will fail on PK violation. War rooms exist as a separate topology *because* the parallel pattern doesn't fit the session storage model. Don't try to force it.

**Audit recordkeeping:** PR descriptions and decision docs should NAME which shape was used and which session/war-room id, e.g. *"War room (4 seats, war_room_id `7D7FC9AF…`) for breadth; sequential session (`b1547c69…`, 3 seats, 6 turns) for synthesis. Verdict tag `[APPROVE]` unanimous in R2."* This makes the strength of the conclusion legible to whoever inherits the decision — independent agreement (war room) is stronger evidence than built agreement (session).

## Why have a war-room at all

Three principles, stack-agnostic:

1. **Specialist personas catch what generalist prompts miss.** A
   security review prompt that explicitly says "you are a security
   reviewer, look for OWASP-class issues" surfaces different findings
   than a generic "review this." Same idea as gstack's virtual team
   pattern; same idea as YC's office hours; same idea as code review
   itself.

2. **Cross-family disagreement raises the floor.** Two turns from the
   same model family confirm each other's blind spots. Cross-family
   pairs (e.g., Claude + MiniMax, Claude + Gemini, Claude + DeepSeek)
   raise the chance that an embedded assumption fails one of them.

3. **Filter every turn through known failure modes.** Karpathy's four
   (wrong assumptions / overcomplexity / orthogonal edits /
   imperative-over-declarative) is one well-tested default. You can
   swap in any framework — SPADE, RICE, OWASP, STRIDE, your own — as
   long as it forces commitment to specific categories of risk per
   turn.

## CEO seat + specialists on standby

The **CEO seat is user-configurable** — it's whichever LLM the user has
chosen to coordinate the war-room. If the user is in a Claude Code
session, Claude is the CEO. If they're driving from Codex, Codex is the
CEO. Same applies to Gemini, OpenClaw, Hermes, or any future runtime.

The CEO seat is set by **whoever is running this skill**. There is no
hardcoded coordinator — that would lock users into a specific stack and
defeat the point of a tool-shaped war-room.

CEO responsibilities (whichever LLM holds the seat):
- Frame the question as a specific tradeoff. "How should I X?" gets
  generic essays; "A vs B, costs C and D, pick one" gets commitment.
- Pick which specialists to summon, matched to the decision class.
  Two or more per war-room. At least one cross-family from the CEO.
- Don't defer. Form a position; let the war-room overturn it if it
  should. Picking "I'll just ask the user" is abdication.
- Read every summoned specialist's reply, surface disagreements, and
  pick a position. Record the decision and the rejected options in
  the deliverable's audit trail. No audit = the rule was skipped.

Specialists are summoned by name from the agent roster the user has
built — whatever that contains. There is no required set; build only
what your decisions actually need.

Two summons mechanisms, both available, often both used:
- **In-session subagent** via the host runtime's subagent mechanism
  (Claude Code's `Task` tool, Codex's agent invocation, Gemini's
  sub-agent call, etc.). Reads the persona from your agent file.
- **`ato dispatch <runtime>`** to a cross-family runtime so priors
  actually disagree. "Cross-family" = a different model family from
  the one holding the CEO seat (e.g., if CEO is Claude, cross-family
  is MiniMax / Gemini / DeepSeek / Codex / etc.).

Default pattern per material decision: at least one in-session
specialist + at least one cross-family dispatch.

## When this skill fires

Run a war-room before any of these. The trigger is "the decision is
real and reversing it is expensive."

### Code

- New SQL migration / schema column / index
- New service, daemon, module
- New public surface: CLI subcommand, Tauri command, MCP tool, REST endpoint
- Security boundary: encryption at rest, auth, key handling, IPC trust
- Cross-runtime contract: event shape, IPC protocol, dispatch envelope
- Anything that took >1 hour the last time you did something similar
- Anything you'd describe as "architectural"

### Non-code

- Plan or roadmap recommendation about to land in the user's hands
- Pricing / packaging / positioning choice
- Scope cut (deferring feature X to ship Y)
- UI / UX / IA / naming with multiple reasonable answers
- "Should we build this at all" / "is this the right wedge"
- Strategic question the user asked where you have a view

### Delivery moments — never skip

- About to send a code diff or implementation as final answer
- About to `git commit` with >50 LOC of behavior change
- About to `git push` to a branch with a remote
- About to `gh pr create`
- About to deliver a multi-paragraph plan or recommendation as final

If you hit a delivery moment and the war-room hasn't happened, **stop**
and run it retroactively. Apply or record the findings. Then proceed.

### Skip rules

- Trivial fixes (1–2 line bug, typo, comment-only)
- Edits the user dictated verbatim
- Pure formatting / lint / dependency bump
- Mechanical changes the trigger heuristics caught as a false positive

Skip silently is wrong. Skip with a one-line note in the deliverable
("war-room skipped: trivial typo fix") is right.

## Procedure

### 1. CEO frames the question

Bad: "How should I build the provider-key encryption?"
Good: "For encrypting provider keys at rest in Node, I'm choosing
between (A) `crypto.createCipheriv('aes-256-gcm')` built-in vs
(B) `@noble/ciphers`. A is zero-dep but easy to misuse (iv reuse, auth
tag handling); B adds a dep but the API is misuse-resistant. Pick one
and justify against the rejected option."

A specific tradeoff prompt forces commitment. "How should I X?" gets
generic essays.

Before you dispatch, draft your own CEO position in one paragraph. If
the war-room arrives at your position, you'll know it wasn't just
the loudest voice winning. If it overturns your position, that's the
catch you needed.

### 2. Summon specialists from YOUR roster

War-rooms summon agents YOU built — not a fixed list. Different
installs have different skill stacks and different agent rosters;
your war-room voices should reflect what you've actually adopted.

**Build the roster** with the companion `ato-make-agent` skill, or
hand-author agent files directly. Any source works — a gstack skill,
a custom SKILL.md you wrote, a third-party persona file, an OpenAI
Agents SDK definition, anything you can express as a system prompt.
The agent file lands at `.claude/agents/<slug>.md` (project) or
`~/.claude/agents/<slug>.md` (global), with a model roster (primary
+ cross-family alts) declared in frontmatter.

Below is one example roster shape — names borrowed from gstack's
specialist taxonomy because it's a well-known reference, NOT because
it's required. Substitute your own personas freely.

| Domain                | Example agent slug   | Cross-family alt notes    |
|-----------------------|----------------------|---------------------------|
| Strategy / scope      | `founder`            | Any non-primary family    |
| Product framing       | `forcing-questions`  | Any non-primary family    |
| Architecture / tests  | `eng-manager`        | Any non-primary family    |
| Visual / UX / IA      | `designer`           | Any non-primary family    |
| Developer surface     | `dx-lead`            | Any non-primary family    |
| Security / threat     | `cso`                | Any non-primary family    |
| Debug / root-cause    | `debugger`           | Any non-primary family    |
| Adversarial critic    | `adversary`          | Already off-family        |

You can build none of these and instead create entirely different
specialists (`@compliance`, `@perf`, `@user-empathy`, `@ml-eval`, etc.).
The war-room mechanism doesn't care what the personas are — only that
at least two distinct specialists are summoned and at least one runs
cross-family.

**Summon a built agent** two ways, both load the same persona file:

- `Task(<slug>)` — in-session via Claude Code's Task tool. Loads the
  agent file at `.claude/agents/<slug>.md` (or `~/.claude/agents/`).
- `ato dispatch <runtime> --agent <slug>` — cross-family voice via
  ATO. (Caveat: until the agent-loading fix lands in ATO, this flag
  is "label only" per the CLI help — see fallback below.)

Two or more summons per war-room. The cross-family leg must use a
different model FAMILY from Claude (not Sonnet-vs-Opus) — that's the
whole point.

CEO presides. Specialists advise. CEO decides.

**Fallback for label-only `--agent`.** Today (v2.6 PR-A era) ATO's CLI
treats `--agent <slug>` as a label only — the agent's system_prompt
isn't loaded into the dispatch. Until v2.6 PR-A.5 ships the fix,
prepend the persona text manually. Use Python so multiline YAML
frontmatter (e.g. gstack's `description: |` blocks containing `---`)
parses correctly — naive `awk '/^---$/'` splits at the wrong place:

```bash
AGENT_FILE=".claude/agents/<slug>.md"
[ -f "$AGENT_FILE" ] || AGENT_FILE="$HOME/.claude/agents/<slug>.md"
PERSONA=$(python3 - "$AGENT_FILE" <<'PY'
import sys, re
text = open(sys.argv[1]).read()
# Strip a leading "---\n...\n---\n" frontmatter block only when it's
# the first non-blank construct. Body is everything after.
m = re.match(r'^---\n(.*?)\n---\n', text, re.DOTALL)
print(text[m.end():] if m else text)
PY
)
ato dispatch minimax "$PERSONA

---

<your war-room prompt>" --agent <slug> --session "$SID" --human
```

When the CLI fix lands, drop the prefix and rely on `--agent` alone.

**Verification note on the Task-tool leg.** Claude Code's `Task` tool
reads agent files from `~/.claude/agents/<slug>.md` (verified: Will's
install has `code-reviewer`, `code-writer`, etc. there). Project-scoped
`.claude/agents/<slug>.md` follows the same precedence pattern as
project-scoped skills (override global). If on your first agent the
Task tool can't see a project-scoped agent, fall back to `--global`
scope in `ato-make-agent` for that persona.

**Default if you have no agents built yet.** Run `ato-make-agent` on
one skill matching the decision class before opening the war-room
(~5 min per agent). Or fall back to invoking the source skill
in-session (e.g. `Skill(<skill-name>)` for Claude Code; equivalent
for other runtimes) for the specialist leg + a generic
`ato dispatch <cross-family-runtime>` (no agent) for the cross-family
leg. The generic path works but loses persona depth; build the agent
the first time a war-room voice recurs.

### 3. Apply a failure-mode filter to each prompt

Embed the filter framework you've chosen into the prompt template
handed to each summoned seat. Karpathy's four (wrong assumptions /
overcomplexity / orthogonal edits / imperative-over-declarative) is a
good default; you can substitute SPADE, RICE, OWASP, STRIDE, or any
domain-appropriate framework — as long as the framework forces
specific risk categories to be addressed per turn.

Default prompt template (Karpathy's four):

```
You are the <seat-role> for this project. The coordinator (CEO) is
convening a war-room. Decision under debate: <one-line>.
Tradeoff: <specific A-vs-B from step 1>.

Filter — comment on each of the four explicitly:
1. WRONG ASSUMPTIONS — what is the CEO assuming that may not hold?
2. OVERCOMPLEXITY — what simpler shape would ship 80% of the value?
3. ORTHOGONAL EDITS — what's in the proposed scope that doesn't
   belong to the stated goal?
4. IMPERATIVE-OVER-DECLARATIVE — is the goal expressed as verifiable
   outcomes + tests, or as a sequence of steps? Push for outcomes.

Then: pick A or B. Justify against the rejected option. Brief —
three to six bullets, not a wall of text.
```

If a seat declines to commit, ask again with the wedge sharpened. A
seat that won't commit isn't a seat, it's a participant.

### 4. Dispatch the cross-family seat(s) via `ato dispatch`

Route each cross-family seat through ATO so the work flows through
your dispatch + session primitives.

**Pick a tool-capable runtime when the seat needs to walk the code.**
This is the most-bitten failure mode in 2026-05-15 sessions. ATO's
`dispatch` targets split into THREE classes (the second was added in
v2.9 grounded mode — see `docs/agent-playbook.md` in the OSS repo for
the full briefing, and blog Parts 1-7 for the build log):

- **CLI-native runtimes** (run their own tool loop unconditionally,
  no flag needed): `claude`, `codex`, `gemini` (when CLI installed),
  `openclaw`, `hermes`. Check live status with `ato runtimes health`.
  Pass a brief, they walk the source themselves.
- **API providers with function-calling tool loop available** (v2.9+
  prod binary; engaged by passing `--require-tools <comma-list>` or
  `--require-paths`): `openai`, `gemini` (when CLI absent → Google API
  fallback), `minimax`, `anthropic` (API path). The check is
  `provider_supports_tools()` at `apps/cli/src/api_dispatch_tools.rs:243`.
  With the flag, the dispatch routes through `dispatch_with_tools()`
  and the model can call `read_file`, `grep`, `git_log`; receipts land
  in `execution_logs.tool_calls_summary`.
- **API-only providers without a tool loop wired yet** (one-shot HTTP
  request → text response): `grok`, `deepseek`, `qwen`, `openrouter`.
  These can only reason from what's in the prompt. If you need a
  cross-family voice from this class on a code-touching question,
  inline the source bytes in the prompt (cap ~30 KB).

**Today's prod-binary caveat (2026-06-10).** The shipped
`/Applications/ATO.app/Contents/MacOS/ato` is v2.7.4, which predates
the `--require-tools` flag (v2.9 PR-1). Until the next prod app
build, gemini-via-API dispatches from the prod binary run text-only.
For code-review war-rooms on the prod binary TODAY, prefer `codex`
(CLI-native, tool loop always on). Gemini is still the right second
cross-family voice for scope / strategy / positioning seats where
file access isn't required.

Match the seat to the question class:

| Question class | Tool access needed? | Pick |
|---|---|---|
| Code review, security audit, PR diff scrutiny | YES | tool-capable (`codex` is the canonical cross-family choice when CEO is Claude) |
| Scope / strategy / positioning / pricing | NO | either works; API-only is fine + cheaper + faster |
| Plan / roadmap review | Sometimes — only if the plan cites specific files the seat should verify | tool-capable if "yes," otherwise API-only |
| Adversarial challenge / 10-star reframe | NO | API-only is fine; the value is the model's priors, not file access |

**Pitfall to avoid.** If a code-touching war-room dispatches to an
API-only runtime with a summary instead of the raw code, the seat
can only validate against your paraphrase — it cannot catch what
you missed. The 2026-05-15 v2.6 security sweep hit this directly:
a Claude in-session seat reviewed the provider-keys path, an
API-only minimax dispatch was attempted (failed on prompt size
anyway), and the sweep shipped 5 fixes. Switching the cross-family
seat to `codex` (tool-capable) immediately surfaced a 6th — a TOCTOU
race on `MAX_ACTIVE_PROVIDER_KEYS` the Claude seat had read past.
The cross-family value comes from a different model FAMILY *and*
tool access; same-family-with-tools beats different-family-without-
tools for code review.

If the obvious tool-capable runtime is unavailable (not installed,
broken auth, etc.) and you must use an API-only fallback for a
code-touching question, COMPENSATE by sending the actual source
in the prompt (cap ~30 KB to fit `ato dispatch`'s command-line
arg ceiling — chunk by PR if larger, or use `--prompt-file` once
ATO supports it). Note the methodology gap in the audit trail so
it's visible.

```bash
# Stable per-decision session so context carries across follow-ups.
SLUG="pr-b-encryption"
# Pick whichever runtime you're driving as CEO for the session anchor.
CEO_RUNTIME="${ATO_CEO_RUNTIME:-claude}"
SID=$(ato sessions list --limit 20 2>/dev/null | python3 -c '
import sys, json
slug = sys.argv[1]
sessions = json.load(sys.stdin)
for s in sessions:
    if s.get("title", "") == "warroom/" + slug:
        print(s["id"]); break
' "$SLUG" 2>/dev/null)
if [ -z "$SID" ]; then
    SID=$(ato sessions new --runtime "$CEO_RUNTIME" --title "warroom/$SLUG" 2>/dev/null \
          | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")
fi

QUESTION="<the filter-wrapped prompt from step 3>"

# Cross-family seat #1 — DIFFERENT family from the CEO runtime.
# Pick per the table above. Default for code-touching war-rooms when
# CEO is Claude: `codex` (tool-capable, can walk the source itself).
# Default for strategy / scope / positioning: any API-only provider
# is fine (`minimax`, `grok`, `deepseek`, `qwen`, `openrouter`).
#
# When the seat has a named role (Positioning, Devex, CEO, Designer,
# Office Hours, security-specialist, etc.) pass `--agent <slug>` so the
# persona is recorded in `execution_logs.agent_slug` for the audit
# trail. See section 4a for when to skip the flag (generalist voice).
ato dispatch codex --agent positioning "$QUESTION" --session "$SID" --human | tee /tmp/wr-cf1-$$.txt
# (optional) second cross-family seat for breaking ties / adversarial pass.
# Use a third family — e.g. minimax — so you have Claude + GPT + MiniMax priors.
ato dispatch minimax --agent devex "$QUESTION" --session "$SID" --human | tee /tmp/wr-cf2-$$.txt 2>/dev/null
# Generalist seat — no --agent, raw model priors. Drop one of these in
# when you want a falsification voice that isn't anchored to the seat's
# pre-set frame. Healthy default: 3 specialist + 1 generalist per round.
ato dispatch grok "$QUESTION" --session "$SID" --human | tee /tmp/wr-gen-$$.txt 2>/dev/null
```

**Agent records to create once (per ATO install).** The gstack PMF war-room shipped with these 5 — `positioning` / `devex` / `ceo` / `designer` / `office-hours`. To use one on a runtime other than where the canonical record lives, create a sibling record with the same slug and a different runtime (the schema's `UNIQUE (runtime, slug)` accepts it). The `ato agents list` command shows what's installed.

For the in-session specialist seats, invoke the source skill directly
via your runtime's subagent / skill mechanism (e.g. Claude Code's
`Skill(<name>)` or `Task(<agent-slug>)`; Codex's agent invocation).

If `ato dispatch` fails (network, quota, key missing, runtime not
configured), stop and note it — friction IS feedback. Fall back to a
second in-session specialist or a manual cross-perspective prompt and
record the dispatch failure in the deliverable so it gets fixed.

### 4a. Pick the seat type per voice — generalist vs specialist vs adaptive

A war-room is a mix of voices, not a panel of identical experts. The same dispatch invocation can produce three legitimate seat types, each useful for different reasons. Mix them deliberately.

| Seat type | How to dispatch | What you trade | Use when |
|---|---|---|---|
| **Generalist** | `ato dispatch <runtime> "<prompt>"` (no `--agent`, no skill) | Pure model priors, no persona overlay. **Cost**: no domain expertise, no audit-trail persona slug. **Value**: untainted answer, useful as a sanity-check voice or for "what would a smart outsider say?" | You want variance, a falsification voice, or to test whether the project's framing survives a fresh read. At least one generalist per war-room is healthy; four specialists who already agree is noise. |
| **Agent-backed specialist** | `ato dispatch <runtime> --agent <slug> "<prompt>"` — agent record's `system_prompt` is prepended deterministically; slug lands in `execution_logs.agent_slug` | Cross-runtime portable (an agent record works for any runtime where you've defined it). Persistent — mutate the persona in one place, every future dispatch picks it up. Captured in the audit trail. **Cost**: setup-once per persona × runtime. | **Default for named seats** (Positioning, Devex, CEO, Designer, Office Hours, security specialist, etc.). Reproducibility and audit-trail legibility outweigh the setup cost the first time you create the record. |
| **Skill-loaded (Claude in-session only)** | Claude Code's `Skill(<name>)` or `Task(<agent-slug>)` invocation, loading a `.claude/skills/<name>/SKILL.md` | Rich tool grant rules + version-control via markdown. **Cost**: Claude-only — doesn't transfer to `ato dispatch <other-runtime>`. | You're already in a Claude Code session and need the specialist's full procedural depth (steps, decision trees, examples). For cross-runtime seats, mirror the skill's persona into an agent record (see below). |
| **Hook-driven adaptive** | `ato dispatch <runtime> "<prompt>"` against an agent that has a pre-call context hook attached — the hook resolves persona / context at fire time based on a rule (project type, prompt keyword, etc.) | Adaptive — same dispatch line becomes a different persona in different contexts. **Cost**: harder to reason about "did the right specialist fire?"; audit trail records the hook ran but not the resolved persona name as cleanly as `--agent`. | You want context-aware specialists (e.g., "use security-specialist when the prompt contains 'auth' or 'crypto'"). Power-user pattern; not the default for war-rooms. |

**Recommendation hierarchy (when in doubt, top wins):**

1. **Named seat with a known role** → agent-backed (`--agent <slug>`). The 5 gstack agents shipped with this skill — `positioning`, `devex`, `ceo`, `designer`, `office-hours` — are the canonical defaults; create more for specialized domains (security-specialist, infra-reviewer, etc.) the same way.
2. **Untainted-prior voice** → generalist. Don't apologize for it; one generalist per room is feature, not bug.
3. **Claude Code session already loaded with the skill** → use it directly. The agent record is for cross-runtime portability; if you're staying inside Claude, the SKILL.md is already richer.
4. **Adaptive context-dependent persona** → hook-driven, but only if you've already mastered patterns 1-3.

**Don't force the choice.** Mixing seat types in one war-room (e.g., 3 agent-backed specialists + 1 generalist) usually produces sharper outputs than 4 of the same kind.

**Compare patterns when in doubt.** Run the same question through two seat types on the same runtime and compare receipts (the dispatch JSON has cost, tokens, response). Specialists tend to win on positioning / design / framing-heavy questions; generalists tend to win on "is this problem even real?" tests. Your mileage will vary by domain — measure, don't assume.

**Creating an agent record from an existing skill.** When a gstack-style `SKILL.md` already captures the persona well, distill the *seat identity* (~150-300 words: who they are, what frame they apply, how they commit) into the `system_prompt` field. Don't paste the whole skill — procedural steps and examples bloat the prompt without sharpening the persona. See the 5 gstack agents shipped with this skill for templates.

### 4b. Pick the multi-seat shape — parallel for breadth, sequential session for depth

Two patterns produce very different outputs. Picking the wrong one wastes both rounds.

| Pattern | How | What it produces | Use when |
|---|---|---|---|
| **Parallel** (Round 1) | Dispatch each seat to its OWN dispatch (no `--session`). Each seat sees the same shared context but NOT each other's answers. | Breadth — no anchoring bias, every seat answers from priors. Convergence (if any) is independent evidence. | Initial wedge discovery, falsifier-finding, getting variance on a question. The CEO synthesizes by hand after all seats land. |
| **Sequential session** (Round 2+) | Create one session: `ato sessions new --runtime <primary>`. Dispatch each seat with `--session <id>`. Each subsequent seat sees prior turns via history replay and can react to them. | Depth — amendments stack, escalations become explicit ("I agree with seat 1 — and here's why we should go further"). The last turn IS the synthesis. | Ratification, escalating fixes, getting confrontational disagreement visible, deepening a synthesis the first round produced. |
| **Hybrid** (R1 parallel → R2+ sequential) | Run R1 parallel for breadth, then R2 sequential in a fresh session passing the R1 synthesis as context. | Both — diversity in R1, convergence with bite in R2. | The default for any non-trivial decision. Cost: ~2× a single round. Cheaper than skipping R2 and shipping the wrong answer. |

**Concrete signal that R1 parallel produced what it should:** seats disagree on framing but converge on substance, or every seat surfaces a different risk you hadn't considered. If they agree on framing AND substance, the question was leading and R1 didn't add signal.

**Concrete signal that R2 sequential is needed:** at least one R1 seat used a verb like "could" / "might" / "worth considering" — that's a hedge the seat would sharpen if it saw a prior seat commit. Run R2 to force the sharpening.

**Pitfall: confusing parallel for "real chat".** Parallel multi-seat outputs LOOK like a debate but no seat saw another's reply. If you write "the room agreed X," verify whether the agreement was independent (R1 parallel) or built (R2 sequential). The former is stronger evidence for X being true; the latter is stronger evidence for X being the room's best joint conclusion. Both are useful — confusing them isn't.

**Recording the shape in the audit trail.** PR descriptions and decision docs should name which pattern was used and which session (if R2+). Example: *"R1 parallel via 5 ato dispatch (no --session); R2 sequential in session b1547c69 (3 seats, history-replay). Verdict tag [AMEND] unanimous in R2."* This makes the strength of the conclusion legible to whoever inherits the decision.

### 4c. Session discipline — one subject per session, never overload, never re-open off-topic

> Full reference: [`docs/SESSIONS.md`](../../../docs/SESSIONS.md). This section is the war-room-specific summary; SESSIONS.md covers the lifecycle, data model, dispatch types, and cross-runtime mechanics in depth.

This rule cost ATO a strategic session preview during the 2026-05-16 dogfood; don't repeat the mistake.

**Sessions are how the local DB structures decision history by subject, date, and work session.** The Sessions list in the desktop app is meant to be readable months later by a human (you, your teammate, your future self) asking *"what was decided about X, and when?"*. That only works if each session row is a coherent unit. Overload a session with off-topic dispatches and the row title, summary, and preview stop describing what's in it — the trail goes dark.

**The rules:**

1. **One session per subject / decision / work block.** A PMF war-room and an unrelated code review go in different sessions. A war-room about pricing and a war-room about onboarding go in different sessions. Sequential rounds *of the same war-room* (R1, R2, R3 ratifying the same decision) belong in the *same* session — that's the value of history replay.

2. **Never re-open a closed session for a different topic.** `ato sessions reopen <id>` is for genuinely continuing the same conversation (new evidence, follow-up question, related amendment). It is NOT a "scratch buffer." If you find yourself reaching for an old session to ask a new question, create a new session instead. The old one's coordinator-generated summary already committed an interpretation of the conversation; piling new turns on rots that summary in place.

3. **Smoke tests, schema verification, ack pings — separate session always.** Anything you'd later regret seeing as the preview of a strategic session is the wrong dispatch to send to that session. `ato sessions new --runtime <X> --title "smoke test 2026-05-16"` is one command; type it. The same holds for "I just want to verify --agent wires through" or "let me see what the table looks like" — all of these dispatches change `sessions.last_used_at`, refresh the `lastAssistantPreview`, and (on close) influence the coordinator's auto-summary.

4. **Title and summary are part of the deliverable, not metadata.** When `ato sessions close <id>` runs, the coordinator generates `auto_title`, `summary`, `tags`, and `project_id` from the conversation. That summary is the row's identity going forward — it's what someone (or you, in 3 weeks) reads to decide whether the session is worth opening. A war-room session whose summary becomes "Ack." because the last turn was an unrelated smoke test is permanently degraded as a navigation artifact. Either keep the smoke-test dispatches out, or re-close the session with explicit context so the regenerated summary captures the real decision.

4b. **Close-time `category` + `team` are part of the deliverable, too.** As of PR 3 of the Sessions UX polish wave (v2.7.3), `ato sessions close` also asks the coordinator for a `category` (strict vocabulary: Business / Marketing / Dev / Frontend / Backend / Design / Security / Compliance / Ops / Other) and a `team` (free-form band label: founder / frontend / backend / ops / design / etc.). These power the Sessions tab filters — a session that closes without them is a session future-you can't find. The CLI warns to stderr when either field is missing; do NOT ignore the warning unless you genuinely intend a context-free close (in which case pass `--force-close-without-context` to make the omission explicit). An out-of-vocab category is a hard fail at close time, so an LLM that hallucinates "Whatever" gets caught immediately rather than rotting the row with a silent SQL CHECK failure later.

5. **Naming the session at creation time is cheap insurance.** `ato sessions new --runtime claude --title "PMF war-room — wedge + pitch + hero ratification 2026-05-16"` reads correctly even before a single turn lands. A session that grows past its original scope (e.g. "Round 2 ratification" that ends up holding Rounds 2-7) should be renamed when you notice — `ato sessions ... ` doesn't expose rename today, but you can `UPDATE sessions SET title = ?` directly while the right command lands.

6. **When the war-room spans a multi-day decision, prefer one session over splitting by day.** Continuity of history beats date-bucketing. Use the title and tags to mark the cadence (e.g. `tags: ["round-1", "round-5", "ratified"]`).

7. **When in doubt, create a new session.** Sessions are free; you can always link them via tags or a meta-doc that references both ids. Cluttering one session is the irreversible cost.

**Convention for war-room session titles:**

```
<topic> war-room — <scope summary> <YYYY-MM-DD>
```

Examples:
- `PMF war-room — wedge / pitch / hero ratification 2026-05-16`
- `Pricing war-room — tier collapse vs sign-in capture 2026-05-12`
- `Security audit war-room — provider-keys path 2026-05-15`

**What this skill should make you do automatically:**

- Before dispatching, check: *does this question belong in the open session I'm about to target, or does it deserve a fresh one?* If the answer is anywhere short of "yes, this is the same subject," create new.
- Before closing, scroll the last 3-5 turns and confirm they would make a coherent summary. If not, dispatch one final "summarize this round in 80 words" turn so the coordinator has clean material to work with.
- After closing, glance at the row in the Sessions list. The title + preview should describe the session in a way that's legible to someone who didn't run it.

### 5. CEO synthesizes

Read every seat's response. Force the disagreement to the surface:

- If two seats agree completely, the question was too easy or too
  leading. Reframe or proceed with a flag noting the war-room added
  no signal.
- If seats split, that's the signal. As CEO, pick a position and
  justify it against each loser.
- Apply your filter framework to your OWN draft answer one more time
  before committing.

You may overrule any single seat. You may not overrule unanimous
disagreement without recording why.

### 6. Record the war-room — audit trail

This is what closes the loop. No audit trail = the rule was skipped.

**PR description**:

```
## War-room (pre-decision)
- Question: <the specific tradeoff>
- Seats: <in-session specialists> + <runtimes dispatched via ato>
- Disagreement: <one-line summary>
- CEO decision: <what won, and the rejected option(s) with reasons>
- Filter pass (<framework name, e.g. Karpathy>):
  - <category 1>: <what was surfaced>
  - <category 2>: <what was cut>
  - <category 3>: <what was kept out of scope>
  - <category 4>: <how the goal is verifiable>
- Session id: <warroom session uuid>
```

**Plan / recommendation** sent to user, prepend:

```
## War-room
- Seats: <…>
- CEO decision: <…>
- Filter pass: <one-line per category>
- (Transcript: <session id>)
```

**Commit body** for >50 LOC behavior change:

```
### War-room (pre-code)
<one paragraph: what was debated, what won, which filter category caught
something>
```

Missing section ⇒ rule skipped ⇒ skill failed ⇒ retroactive war-room
required before next delivery moment.

### 7. Cleanup + close-with-summary

```bash
rm -f /tmp/wr-cf1-$$.txt /tmp/wr-cf2-$$.txt
```

**Close the session so it lands in the Sessions tab with a coordinator-
generated title, summary, tags, and project_id.** Without this, every
war-room session shows up as `warroom/<slug>` with no searchable text —
which defeats the "I want to find that one architecture discussion from
three weeks ago" use case and makes the post-merge audit trail useless.

```bash
ato sessions close "$SID" --human
```

The coordinator agent (whichever LLM is configured as the session's
summarizer; defaults to the CEO runtime) reads the full transcript,
generates the four fields, and persists them on the session row. A
closed session can be reopened later with `ato sessions reopen "$SID"`
and the next dispatch continues the conversation; the next close
refreshes the summary with the added turns.

Code paths that drive war-rooms in scripts (e.g. `ato review
--consensus`) auto-close on success as of 2026-05-15 — verify by
checking that the Sessions tab row shows a real title instead of
`review/<short-id>`. If your custom dispatch script bypasses
`ato review`, call `ato sessions close` explicitly at the end. The
auto-close is best-effort: if the close fails (no turns landed,
already closed, summarizer dispatch error), the review still
succeeds and surfaces a warning telling you to retry the close
manually.

If you intentionally want to keep the session OPEN (rare — e.g.
you're in the middle of a multi-day decision and tomorrow's turn
will continue the same conversation), skip the close. Closing then
reopening is the only path that overwrites a prior summary.

## Anti-patterns

- **Skipping the CEO frame.** "Let me ask the agents what to do" — no.
  Form a position first, let the war-room overturn it if it should.
- **Single-seat dispatch.** Second opinion ≠ war-room. Always ≥2 seats
  with cross-family disagreement potential.
- **Generic "reviewer" for every question.** Match specialist to
  domain (security agent for crypto, founder-mode agent for strategy,
  whichever specialists your roster contains).
- **Asking "is this OK?"** A sign-off prompt is not a war-room. Ask
  "A vs B, pick one and justify against the loser."
- **Filter as boilerplate.** If a seat returns "no concerns on
  <category>" for every prompt, re-ask with a sharper wedge or the
  seat isn't earning its seat.
- **Hiding the war-room from the deliverable.** No audit trail = the
  rule was skipped, period.
- **Skipping because "I already know the answer."** That's exactly when
  the war-room catches what you're missing. The CEO has a position;
  the war-room tests it.

## Pairs with

- **`ato-make-agent`** — the companion tool. Converts source skills
  into ATO agent files with model rosters so war-rooms can summon
  them by name.
- **`ato-review`** — post-code diff review (the AFTER half). Run both
  on the same chunk: war-room before drafting, review after drafting.
  Neither replaces the other.
- **Whatever specialist skills your stack provides** — gstack, custom,
  third-party, or hand-authored. The war-room mechanism doesn't care
  which stack populates your roster.

## Origin

This skill records a discipline gap: pre-code design decisions were
landing without multi-specialist review while post-code diffs were
getting full multi-LLM consensus passes. The pre-decision filter
catches a different class of error (assumptions, scope, framing) than
the post-code diff review catches (bugs, missed edges). Both need to
exist; this skill is the pre-decision half.
