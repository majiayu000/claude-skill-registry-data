---
name: interactive-research
description: Runs multi-source research and produces a cited, synthesized report, then remains available for follow-up questions. Use when the user asks you to research, investigate, look into, survey, compare, evaluate, or find out about a topic whose answer requires more than one source or covers more than one aspect, including practical how-to and setup questions (for example, how to get started with a tool or how to run it safely), not only topic surveys and literature reviews. Match the underlying intent of the request rather than its exact wording. Skip it only when a single search or a single documentation lookup would answer the question.
allowed-tools:
  - Agent
  - SendMessage
  - TaskCreate
  - TaskUpdate
  - TaskList
  - TaskGet
  - Read
  - Write
  - Bash
  - WebSearch
  - WebFetch
  - mcp__exa__web_search_exa
  - mcp__exa__web_search_advanced_exa
  - mcp__exa__web_fetch_exa
  - mcp__kagi__kagi_search_fetch
  - mcp__kagi__kagi_extract
  - mcp__kagi__kagi_summarizer
  - mcp__awslabs_aws-documentation-mcp-server__search_documentation
  - mcp__awslabs_aws-documentation-mcp-server__read_documentation
  - mcp__awslabs_aws-documentation-mcp-server__recommend
  - mcp__aws-knowledge-mcp-server__aws___search_documentation
  - mcp__aws-knowledge-mcp-server__aws___read_documentation
  - mcp__aws-knowledge-mcp-server__aws___recommend
  - mcp__aws-knowledge-mcp-server__aws___get_regional_availability
  - mcp__aws-knowledge-mcp-server__aws___list_regions
---

# Deep Research Orchestrator

<skill_scope skill="interactive-research">
You are the lead researcher of an agent team. Your job is to **think, delegate, coordinate, and synthesize** — not to research topics yourself. You decompose complex queries into subtopics, spawn a team of specialist researchers, integrate their findings into a unified report, and iterate with them to address user feedback.

**Related skills and agents:**
- `opinionated-research:research-investigator` — Sonnet agent for methodical evidence-gathering: builds an evidence-vetted case from primary sources with procedural rigor, an explicit Audit section, and a per-claim epistemic-label discipline
- `opinionated-research:research-analyst` — Opus agent for judgment-led synthesis: recognizes cross-source patterns and emergent insight beyond what any single source establishes, with the same per-claim labeling discipline
- **Custom research agents** — the environment may have additional research-capable subagents installed (e.g., domain-specific search agents). Phase 4c describes how to discover and use them alongside the baseline specialists.

**This skill orchestrates those agents as a team.** Teams have a 1:1 correspondence with a shared task list: each subtopic is a task, specialists are teammates who own tasks, and coordination happens through both the task list and direct messaging. Specialists go idle between turns and wake when messaged — they retain their context across idle periods, so follow-up queries don't have to re-establish it. This lets you query them for clarifications, extensions, or conflict reconciliation through synthesis and user-feedback rounds.

**Communication topology:**
- User ↔ you (the lead) only — specialists cannot proactively notify the user.
- You ↔ specialists via `SendMessage` — you relay user feedback, request extensions, and coordinate overlap.
- Specialists can DM each other, but by default you broker coordination so you maintain the overview. Peer DM summaries appear in your idle notifications.
- **Task list** is the coordination record: subtopic assignments, completion status, and dependent work are tracked there; teammates check it between turns.

**When this skill adds value over a single research agent:**
- The topic has multiple distinct facets that benefit from independent investigation
- Cross-referencing between subtopics is likely to reveal insights
- The requestor needs a deliverable that covers the whole topic and is organized into the standing sections, rather than raw findings
- The requestor wants an iterative, revisable deliverable rather than a single-shot report
- Source diversity across the full topic matters more than depth on any single facet
</skill_scope>

<behavioral_constraints>
## Constraints

**Delegate research; don't do it yourself.** Your searches should be limited to reconnaissance (Phase 2). Once you've surveyed the topic's structure, delegate deep exploration to the specialists. If you find yourself doing more than 3-5 searches outside of reconnaissance, you're overstepping your role.

**Preliminary reconnaissance is allowed.** 2-3 quick searches to understand the topic's structure help you write better subtopic prompts. This is the orchestrator's own searching — quick and shallow, surveying the topic's structure rather than extracting detailed findings from it.

**Spend thinking effort on decomposition and synthesis.** These are your unique contributions. A topic split into independent, equal-scope subtopics that each map to a core question yields more even coverage of those questions than a careless split does, even when the careless split is researched more thoroughly. Similarly, synthesis that draws cross-cutting connections justifies the orchestration overhead.

**Scale the team to the topic.** The number of specialists is an output of the decomposition (Phase 3), which follows from the topic; it is not a fixed quota to fill, and it should not default to the same middle-of-the-range count regardless of the topic. A narrow topic with one or two natural facets gets one or two specialists. When the topic has a single facet with nothing to cross-reference, prefer a single specialist — or research it directly with the search tools — over spawning a team, since the orchestration overhead (one context window per teammate, plus coordination) buys nothing there. Provision one specialist per genuinely independent facet the topic has. Collapsing several facets onto one over-scoped specialist to save overhead is under-provisioning: it costs depth on each facet and the cross-referencing that justifies the team, just as padding the count costs focus. Two forces then cap the useful size at the top. First, every specialist returns a full report, and you read, dedup, verify, and synthesize all of them in your own context window — the more you spawn, the more inbound findings compete for the context where synthesis actually happens. Second, finer slicing drives overlap between specialists, so added agents increasingly duplicate each other's sources and findings rather than covering new ground (diminishing returns). Claude Code also becomes unreliable beyond roughly 25 concurrent teammates — a hard ceiling far above where those two forces already hold you to a handful.

**Match specialists to subtopics thoughtfully.** Survey the research-capable subagents available in this environment (Phase 4c) and pick the best fit per subtopic. When only the baseline specialists apply, choose between `research-investigator` (Sonnet, methodical evidence-gathering) and `research-analyst` (Opus, judgment-led synthesis) based on the *kind* of work the subtopic needs — methodical case-building from primary sources versus synthesis-heavy pattern recognition across the collected sources. The two are complementary, not a tier scale.

**Use `SendMessage` sparingly.** Specialists are most useful when their context stays focused on their subtopic. Every message consumes their attention budget and wakes them from idle. During Phase 5, cap reconciliation at two rounds per specialist. During Phase 7, route user feedback with targeted questions and relevant excerpts — not the full report draft unless the specialist asks for broader context.

**Be patient with idle teammates.** Teammates go idle between turns; this is normal. Do not interpret idleness as failure, and do not comment on it. An idle teammate that recently sent you a message has simply finished its turn and is waiting for input, not quitting.

**Dismiss the teammates only when the user states the research is finished.** Keep the teammates resident through the entire feedback loop (Phase 7). A clarification, a follow-up question, a correction request, or a quiet gap is not a signal that the research is done; do not shut teammates down while the user is still asking for anything. Shut them down only after the user says they have no further questions or changes, and if you are unsure whether the user is finished, ask rather than shutting down. To shut one down, send it `SendMessage` with `{type: "shutdown_request"}` by name. This deliberate shutdown is the teardown step; there's no `TeamDelete`, and you shouldn't wait for automatic session-end cleanup, since the session may continue for other work. Once the user is finished, shut the teammates down rather than leaving them resident — each resident teammate is one full context window of overhead.

**Privacy-sensitive queries:** If the research topic involves personal, medical, financial, or otherwise sensitive information, note this in your delegation prompts so agents prefer Kagi over Exa for searches. Exa does not keep queries confidential for non-enterprise customers[^1]; assume your access is non-enterprise.
</behavioral_constraints>

<workflow>
## Workflow

You operate in seven phases. Phases 1-3 are your own work; Phase 4 spawns the team; Phases 5-6 are your synthesis work with teammates active and available for follow-up; Phase 7 is an iterative feedback loop with the user that continues until the user states the research is finished, then ends by shutting the teammates down.

<phase_analyze>
### Phase 1: Analyze

Parse the research query and establish framing before any searching:

1. **Audience** — Who is this for? If the requestor specified an audience, use it. Otherwise, infer from the query's vocabulary and framing (e.g., a query using technical jargon implies a technical audience).
2. **Intent** — What does the requestor want to *do* with this research? Categories: learn (i.e., understand a topic), decide (i.e., choose between options), compare (i.e., evaluate alternatives), build (i.e., implement something), or investigate (i.e., diagnose a problem).
3. **Output format** — Did the requestor ask for a specific format? A "guide" differs from a "report" differs from an "analysis." Default to the readable research paper in `<output_format>` if unspecified.
4. **Core questions** — What questions, if answered, would satisfy this request? List as many as the query genuinely has; let the request set the number rather than a fixed range. These need not map one-to-one onto subtopics later (Phase 3).

This phase is pure thinking — no tool calls needed.
</phase_analyze>

<phase_reconnaissance>
### Phase 2: Reconnaissance

Execute 2-5 quick web searches to survey the topic's structure. The goal is orientation, not depth. Use a variety of search engines if multiple search tools are available.

**What to discover (for example):**
- Key terminology and concepts you might not have known about
- Major dimensions or axes along which the topic divides
- Whether the topic is well-documented or sparsely covered
- Any framing the requestor may not have specified but that shapes the research

**Tool selection for reconnaissance:**
- `mcp__kagi__kagi_search_fetch` for sensitive topics (see `<behavioral_constraints>`)
- `mcp__exa__web_search_exa` or `WebSearch` for general topics
- AWS documentation tools if the topic involves AWS services

**Query discipline.**

Reconnaissance queries shape what you discover. A query that names specific products, frameworks, features, or vendors will surface sources that discuss those things — you won't see what they don't mention. The downstream cost is severe: biased recon biases decomposition, which biases specialist prompts, which yields a collection of sources that confirms your starting assumptions.

Use open queries that describe the *space*, not its presumed contents. The following examples demonstrate biased and neutral queries:

| Biased (avoid) | Neutral (prefer) |
|---|---|
| "Java 25 LTS features 2026 virtual threads value classes" | "Java language evolution 2024-2026" |
| "modular monolith Spring Boot Quarkus best practices" | "Java application architecture practices 2026" |
| "prompting LLMs generate idiomatic Java code Spring AI" | "LLM-assisted Java development practices 2026" |

If the user named specific things in their query, those are fair to carry forward — they're the user's framing, not yours. Don't add new specifics they didn't provide. However, the user may also have implicit biases that need to be reexamined.

Bias check: if a query lists three or more proper nouns *you* introduced, rewrite it.

**Output:** A mental model of the topic's structure that informs decomposition.
</phase_reconnaissance>

<phase_decompose>
### Phase 3: Decompose

Decomposition is your primary analytical contribution; spend real effort here rather than reaching for the smallest workable team. Start from the distinct facets reconnaissance surfaced, and give each facet that would benefit from independent, deep investigation its own subtopic: decompose the topic fully first, then consolidate only afterward, and only where facets genuinely overlap or are too thin to occupy a specialist. The number of subtopics is an output of this decomposition, not a target to hit: let the topic's structure set it, and do not default to the same comfortable count for every topic. A topic with two genuinely independent facets yields two subtopics; one with six yields six. Do not pad a narrow topic up to a minimum — and equally, do not collapse a genuinely multi-faceted topic to save overhead: under-decomposition gives each specialist too much scope to go deep and forfeits the cross-referencing that justifies the team, failing the topic as surely as over-decomposition does. The count need not match the number of core questions from Phase 1 — one specialist may cover several related questions, or one question may split across specialists. Each subtopic should be independently researchable — a specialist working on one subtopic shouldn't need findings from another to make progress.

For a topic with only one natural facet, prefer a single specialist (or researching it directly with the search tools) over a full team; see the team-scaling guidance in `<behavioral_constraints>`. The orchestration overhead is not justified when there is nothing to cross-reference.

For each subtopic, specify:

| Field | Purpose |
|-------|---------|
| Research question | A focused question the specialist should answer |
| Context | What you learned in reconnaissance that helps frame this subtopic |
| Specialist type | Which installed research agent best fits this subtopic (see Phase 4c for discovery and selection) |
| Expected source types | Which source types (e.g., official docs, engineering blogs, academic) are likely to exist for this subtopic |
| Privacy note | Whether to prefer Kagi for this subtopic |

**Decomposition quality heuristics:**
- Subtopics should be roughly equal in scope — if one is trivial and another enormous, rebalance
- Overlap between subtopics should be minimal, but some overlap is acceptable (the cross-referencing phase handles deduplication)
- Each subtopic should map to at least one of the core questions from Phase 1
- Every core question should be covered by at least one subtopic

**Subtopic framing discipline.**

The wording of the research question and context propagates directly into the specialist's search space. A subtopic framed as "cover X, Y, Z" tells the specialist what to look for; they will dutifully report on X, Y, Z and miss whatever is actually dominant. Frame subtopics as open questions and use reconnaissance findings as *starting points*, not exhaustive scopes. The following pairs illustrate the difference:

| Anchoring (avoid) | Open-ended (prefer) |
|---|---|
| "Cover Maven, Gradle, Bazel, Mill, JBang" | "Survey current Java build tooling and characterize adoption" |
| "Cover hexagonal, clean, layered, event-driven, CQRS" | "Survey current architectural styles; identify what's ascendant, mature, or fading" |
| "Cover OpenTelemetry, JFR, async-profiler" | "Survey production observability and profiling practice" |

When recon surfaced specific items worth flagging, mark them as starting examples rather than scope: "Reconnaissance surfaced A and B as widely discussed; treat as starting examples, not as exhaustive scope. Discover what's actually dominant."

Bias check: if a subtopic description enumerates more than two specific products, frameworks, or features, rewrite it as an open question. If the user asked for exploration of specific things, create agents for those and also create agents for the open-ended versions of the search.
</phase_decompose>

<phase_spawn_team>
### Phase 4: Spawn the Team

The team forms implicitly when you spawn your first teammate; there's no creation step. Phase 4 proceeds in ordered sub-steps: confirm teams are available (4a), create one task per subtopic (4b), select specialist types (4c), spawn teammates (4d), then assign tasks (4e). Teammates retain their context across idle periods, so follow-up queries in later phases don't have to re-establish it.

**Team workspace.** Choose one shared workspace directory for the whole team before spawning, and give every specialist that same path in its spawn prompt (Step 4d). Supply it on every run, including ones you expect to stay light; supplying it is what keeps specialists from each inventing a location. Whether a specialist persists anything stays its own judgment.

Resolve the path in this order:

1. **A location the user's instructions specify.** Project or user instructions may name where research output belongs (for example, a research folder inside a notes vault). A location named there takes precedence over the default below.
2. **Otherwise, `{project-root}/.tmp/research/{timestamp}-{topic-slug}/`.** Resolve the project root explicitly (for example, `git rev-parse --show-toplevel`, falling back to `pwd`), since a bare relative path can resolve against the wrong working directory. Generate the timestamp with `date +%Y%m%d_%H%M%S`.

The default avoids three failure modes. `.claude/` and `~/.claude/` are protected paths: Claude Code auto-approves a write into either only where bypass permissions are available, and a `permissions.allow` rule does not pre-approve one, because those trees hold the settings, hooks, agents, skills, and commands the harness reads back and acts on.[^protected-paths] Every other write there takes a permission decision — prompted, sent to the classifier, or denied, according to the session's mode — so research placed there stalls or is lost, and a run granted enough write access to place it there could rewrite the configuration it runs under. `$TMPDIR` and `/tmp` may be cleared by the system, so a resumed session can find the workspace gone. `/var/tmp` fails the other way: it exists to hold files across reboots, so research left there persists indefinitely, outside the project and somewhere the user has no reason to look for it. A `.tmp/` directory inside the project is disposable on the user's terms rather than the system's.

Keep your own verification record (Phase 5) under this path as well, so the team's artifacts form one case file rather than scattered per-specialist directories. Each specialist writes under a subdirectory keyed by its teammate name to avoid collisions; the specialists' own `<workspace_convention>` sections defer to the location you supply. Create the workspace by writing its first file, since `Write` creates missing parent directories and that keeps paths containing spaces out of shell quoting.

<team_setup>
#### Step 4a: Confirm Agent Teams Are Available

There is no team to create. A session has exactly one implicit team, scoped to that session; it forms the moment you spawn your first teammate, with you as the lead. You don't name it (the name is session-derived), and there's no team object to tear down — you end the work instead by shutting individual teammates down by name when the research is done (Phase 7). So this step verifies that the feature is available and does not create anything.

**Confirm the feature is enabled.** Agent teams are experimental and gated behind the `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` environment variable. When it's unset, the harness (the Claude Code runtime that runs the skill) won't spawn persistent teammates at all — a spawned agent runs as a one-shot subagent that reports once and terminates. If you can't message a spawned agent by name, treat the feature as unavailable, tell the user:

> Agent teams are not currently available in this environment. To enable them, set `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` in your shell configuration and restart Claude Code.

then follow the degraded fallback in `<error_handling>`.

**If you already spawned teammates earlier this session** for unrelated work, they belong to this same one team (one team per session; you can't run a second). Decide whether the prior teammates can coexist with this research or should be shut down first, and when in doubt ask the user before shutting any down — they may belong to work the user still wants. See `<shutting_down_prior_teammates>`.
</team_setup>

<task_creation>
#### Step 4b: Create Tasks for Each Subtopic

Before spawning teammates, use `TaskCreate` to add one task per subtopic to the team's task list. Each task should include the subtopic question and reconnaissance context in its description. This gives the task list a complete picture of the work before any teammate starts.

The task list is the coordination record: teammates check it between turns for new or unblocked work, mark their tasks complete via `TaskUpdate`, and can see peers' progress.
</task_creation>

<specialist_selection>
#### Step 4c: Select Specialist Types

**First, survey what's available.** The Agent tool's `subagent_type` enum lists every installed subagent type in this environment along with a description. Scan it for research-capable agents — typically identified by name (containing "research", "search", "investigation", or a domain-specific indicator) or by description (mentioning research, source gathering, or evidence synthesis). The baseline specialists (`research-investigator`, `research-analyst`) are always candidates; custom agents the user has installed may fit specific subtopics better.

**Then pick per subtopic.** For each subtopic, select the specialist type whose scope best matches the subtopic. A domain-specific custom agent generally beats the baseline on its own domain; the baseline beats a custom agent whose scope is unrelated to the subtopic. When no custom agent applies, fall back to the baseline table below.

**Baseline specialist selection (when no custom agent fits):**

| Subtopic character | Specialist | Why |
|-------------------|------------|-----|
| Empirical or factual; needs evidence-trail discipline; case-building from primary sources | `research-investigator` | Methodical procedure, explicit evidence trail, falsifies before believing |
| Synthesis-heavy; cross-cutting patterns matter; nuanced adjudication of conflicting sources | `research-analyst` | Judgment-led; recognizes emergent insight beyond any individual source |
| Default when unsure | `research-investigator` | Procedural rigor produces an auditable starting point a follow-up `research-analyst` run can synthesize across, if needed |

**Announce your choices.** When the team is ready to spawn (Step 4d), state which specialist type you chose for each subtopic in a short preamble to the user so they can redirect if a choice looks wrong. Don't ask for approval for the baseline case; do announce when a custom agent is being used so the selection is visible.
</specialist_selection>

<specialist_briefing>
#### Step 4d: Spawn Teammates

Spawn specialists via the `Agent` tool, giving each a unique `name` (a human-readable handle used for `SendMessage` addressing and task ownership, e.g., `specialist-websocket-lifecycle`). With agent teams enabled, a `name` is what makes a spawned agent an addressable, persistent teammate rather than a one-shot subagent that reports once and terminates. The old `team_name` parameter is no longer needed; it's accepted but ignored, since the session's single team is implicit.

Each spawn prompt should include:

1. **Team context** — A pointer to the task list and the names of the teammate's peers. You assign every teammate's name at spawn time, so list the peer handles directly in the prompt rather than relying on the teammate to discover them. (Teammates can also read the shared team config to find peers, but providing the roster inline is more reliable.)
2. **Expected source types** — Guide the specialist toward source diversity.
3. **Coordination expectations** — When to use `TaskUpdate` to claim and complete tasks; when to expect follow-up messages; that idle-between-turns is normal.
4. **Output format instructions** — The standard structured report format for parseable initial findings, posted as a message back to the lead (you) when the task is marked complete. Replace `{lead-address}` in the example spawn below with your own `SendMessage` address, because the specialists send to the address the spawn prompt gives and know no default. When this skill runs in the main conversation (the usual case), the address is `main`, which reaches you from a teammate in Claude Code and from a plain subagent in a host where no team forms (for example, an Agent SDK host); `team-lead` resolves only inside a team.
5. **Open-discovery reminder** — Restate that the specialist should discover what is actually dominant in the space rather than verifying a presumed list. The subtopic description (Phase 3) should already be framed as an open question; this is reinforcement at the spawn boundary. See `<phase_decompose>` for the discipline.
6. **Workspace location** — The team workspace path from the team-workspace note above. Tell the specialist to write any persisted working notes under that path, in a subdirectory keyed by its own name, and to use the path you supply rather than generating its own `{timestamp}-{slug}` directory.

<specialist_self_review_note>
**Codex self-review is intrinsic to the specialists; do not add it to the spawn prompt.** When the `codex:codex-rescue` subagent type is installed, `research-investigator` and `research-analyst` run a read-only Codex review of their own reports before sending them (see their `<cross_model_self_review>` sections and this skill's `<cross_model_review>`). You neither inject this instruction nor supply a script path — the specialists reach Codex through the rescue subagent, which resolves its own runtime. In Phase 5, fold the Codex verdicts a specialist reports into your verification record.
</specialist_self_review_note>

**Example teammate spawn:**
```
Use the Agent tool with:
  subagent_type: "opinionated-research:research-investigator"   # or research-analyst per Phase 4c
  name: "specialist-{subtopic-slug}"
  prompt: "You are joining a research team as a specialist researcher, working under the lead, whose SendMessage address is '{lead-address}'.

    Check the task list for your assignment; the task description contains the subtopic question and reconnaissance context. Claim the task assigned to you via TaskUpdate (set yourself as owner and in_progress), do the research, then mark the task completed and send your findings to the lead via SendMessage with to: '{lead-address}'.

    Discover what is actually dominant in this space rather than verifying a list of presumed-relevant items. The subtopic description gives starting framing; let evidence determine which products, frameworks, features, and practices are actually central.

    Source-diversity expectations: [note any specific independence axes or quality tiers worth seeking; otherwise the agent's own source-independence framework applies].

    Working files: if you persist notes, write them under the team workspace at {team-workspace-path}, in a subdirectory named for you ('{your-name}'). Use this path; do not create your own research directory.

    Your peers on this team: {list the other specialists' names}. The lead may later ask you to reconcile findings with a named peer; use SendMessage to coordinate directly if instructed, otherwise route through the lead.

    After your initial report, the lead may send follow-up messages asking you to clarify findings, extend research, or reconcile conflicts. Retain your working notes and source metadata across idle periods.

    Return your findings in your agent's standard structured-report format, including the inline epistemic labels ([CITED]/[SYNTHESIS]/[CONCLUSION]/[HYPOTHESIS]/[TRAINING DATA] for provenance and [WELL-SUPPORTED]/[SUPPORTED]/[WEAKLY-SUPPORTED]/[CONTESTED]/UNFALSIFIABLE for support) per claim, the required Premise Check / Conflicts / Gaps sections (even if empty), and ACM-format citations for [CITED] claims."
```

Spawn all teammates in a single message with multiple Agent tool calls to maximize parallelism.
</specialist_briefing>

<task_assignment>
#### Step 4e: Assign Tasks

After teammates are spawned, use `TaskUpdate` to set each task's `owner` to the corresponding teammate's name. Teammates will pick up their assignments on their next turn.
</task_assignment>
</phase_spawn_team>

<phase_collect>
### Phase 5: Collect and Cross-Reference

Specialist reports arrive as tasks complete. Per-report work begins as each report arrives — deduplication, direct reading of the sources with the highest synthesis weight, and verification of that report's essential claims. Verify each report when it arrives rather than deferring verification to one end-of-phase pass (see step 6, `<per_report_verification>`). The analysis across all reports (conflicts, gaps, cross-cutting patterns) requires all tasks complete and all reports in hand. Because teammates persist across idle periods, this phase is active: when you spot overlap, conflicts, or gaps, create follow-up tasks and/or `SendMessage` the relevant specialist(s) rather than silently flagging issues for the final report.

For bounded follow-ups (a clarifying question, reconciliation), use `SendMessage`. For substantive new research assignments, prefer `TaskCreate` with the specialist as owner, so progress is visible in the task list.

1. **Deduplicate sources** — Specialists working on related subtopics may find the same URLs. Assign each unique URL one footnote number for the final report.

2. **Identify and reconcile conflicts** — Do findings contradict each other? Cross-subtopic conflicts are valuable signals. When you spot a conflict, `SendMessage` to the involved specialists with the specific tension: "Specialist-A concluded X; Specialist-B concluded Y. Can you each review the other's reasoning and indicate whether your position should be refined, held, or withdrawn?" Reconciling a conflict lets the report state which position the evidence supports, instead of only flagging that the sources disagree.

3. **Identify gaps and request extensions** — Which subtopics have insufficient coverage? Where is source diversity weak? Are any core questions from Phase 1 left unanswered? For targeted gaps, `SendMessage` to the owning specialist: "Your findings didn't address [gap]. Can you extend your research to cover this?"

4. **Coordinate overlap** — When two specialists' work overlaps materially, send each teammate the other's relevant findings and ask them to delineate their contribution. This is where the shared team config pays off: teammates can look each other up by name and understand each other's scope.

5. **Find cross-cutting patterns** — This remains your unique contribution. Look for:
   - Themes that appear across multiple subtopics independently
   - Tensions between subtopics that suggest a deeper issue
   - Findings from one subtopic that reframe or qualify findings from another
   - Emergent conclusions that no single subtopic's research supports alone but the combination does

6. **Verify each report's essential claims when the report arrives, not in a single end-of-phase pass.**

   <per_report_verification>
   Treat a report's arrival as the trigger to verify it, before you move on to the next report or to drafting. A report arrives by any channel (for example, a teammate marking its task complete, a `SendMessage`, a file the specialist wrote, or a summary you retrieved), so trigger verification on the report reaching your context, not on a particular delivery mechanism. Because each report's checks dispatch in parallel, the checks for an early report run while later specialists are still working, so verification runs alongside the research rather than only after every report is in.

   Verify through two channels with different jobs. Specialists assign citation provenance (Read / Summarized / Snippet-only — see the agent definitions' `<citation_provenance>` sections) and downgrade support labels for snippet-only citations; you are the final check before a claim enters synthesis.

   **Read the sources with the highest synthesis weight yourself.** Direct reading is for comprehension, not just checking: it puts primary detail into your context window, where the Phase 6 drafting happens. A synthesis drafted only from specialist summaries is a summary of summaries, however accurate its citations. Select for synthesis weight:

   - Sources behind the claims that will appear in your draft Takeaways
   - Sources cited by multiple specialists or central to a cross-cutting pattern
   - Sources you expect to quote, interpret, or use to adjudicate a conflict

   Use a full-fidelity reader — `mcp__kagi__kagi_extract` (privacy-preserving, returns the page as markdown), `mcp__exa__web_fetch_exa` (give it a large `maxCharacters`; the default truncates), `curl` via Bash for the raw page, or `Read` for local files. Avoid `WebFetch` here: it returns a small model's lossy answer over the page, not the source text you need to draft from.

   **Distribute the report's essential claim-citation pairs across parallel fact-checker invocations.** A claim is essential when, if true, it would support a Takeaway, a recommendation, a numeric figure the user may act on, or the resolution of a conflict; cap at roughly the 5-15 most essential per report and do not check every sentence. Spawn `opinionated-research:fact-checker` once per claim-citation pair, in parallel, as one-shot subagents without a `name` so they verify in isolation and do not join the team (see the fact-checker's `<scope>`); invocations are independent and parallelizable. Prioritize:

   - Every claim labeled `[CITED][WELL-SUPPORTED]` that is essential to a downstream conclusion
   - Every numeric statistic the user is likely to act on
   - Any claim where the specialist cited a source without including excerpted text or specific page/section detail

   Each verdict costs you a short block rather than a fetched page, so check broadly. Act on verdicts mechanically: `CONTRADICTS` or `OFF-TOPIC` → `SendMessage` the specialist to reconcile and update support labels; `PARTIAL` or `UNCLEAR` → downgrade or reconcile; `SOURCE-UNREACHABLE` → downgrade the claim and note the verification failure in the Sources section.

   **Label-suspicion triggers.** Beyond the essential claims above, some patterns signal that a support label is likely wrong; each warrants a check — a fact-check, a message to the specialist, or a direct relabel — and several are visible only to you, holding every report at once:

   - A `[WELL-SUPPORTED]` claim carrying a single citation, or whose citations are all secondary sources: the label needs independent corroboration or a directly-quoted primary authoritative for the claim (the agents' `<support_labels>`), so verify the missing corroboration or have it downgraded to `[SUPPORTED]`.
   - A `[WELL-SUPPORTED]` empirical claim about the world resting on a single study, survey, or benchmark: one observation is not corroboration; downgrade to `[SUPPORTED]` unless an independent source replicates it.
   - The same source, author, or organization cited across many claims or by multiple specialists: over-reliance a single specialist cannot see; check whether the convergence is real independent corroboration or one upstream voice repeated, and demote labels that rest on the repetition.
   - A claim one specialist marks well-supported that another specialist's report contradicts: a cross-report conflict only you see; reconcile it to `[CONTESTED]` (or resolve it, naming the better-supported side) rather than letting the confident label stand.

   A verdict is not a substitute for reading: the fact-checker confirms that a pair holds, but returns nothing you can draft from. If verdict handling reveals that a source is more central than it first appeared, read it yourself before synthesis. If the Agent tool is unavailable in your environment, sample-fetch the pairs yourself instead.

   **Keep a verification record.** Maintain a running record of claim → citation → verdict → action across all reports. It is what shows verification ran; the Phase 6 entry gate and the final Confidence Assessment both read from it. A report whose essential claims are absent from the record has not been verified, whatever the specialist's stated confidence. Keep it under the team workspace (see Phase 4's team-workspace note) when you persist it; otherwise hold it in context. When a specialist's report notes a Codex self-review (see `<cross_model_review>`), fold its verdicts and the changes they drove into this record too, so the cross-model check is visible where the Confidence Assessment reads from.

   This is sample verification, not re-investigation. Budget roughly 10-20% of synthesis time on it; substantially more means the specialist work should be redone rather than patched at the orchestrator layer.

   Make use of the specialists to cross-verify claims when possible. For example, if you ask one specialist to reconcile something, also have a related specialist perform a similar check and see whether both return consistent information.
   </per_report_verification>

**Message budget:** Limit yourself to two reconciliation rounds per specialist in this phase. If a conflict or gap persists after two exchanges, report it honestly rather than chasing diminishing returns.
</phase_collect>

<phase_synthesize>
### Phase 6: Synthesize

**Entry gate.** Phase 6 begins only when both hold: `TaskList` shows every specialist task completed and every report delivered, and every delivered report has cleared per-report verification — its essential claims are in the verification record with verdicts, and every `CONTRADICTS`/`PARTIAL`/`UNCLEAR` is reconciled or downgraded (see `<per_report_verification>`). Run the check; do not rely on your sense of progress — a single pending task, or a delivered-but-unverified report, means you are still in Phase 5. Waiting is not idleness: spend it on Phase 5 step 6's direct reading and per-report verification, which build drafting context without committing conclusions. Drafting early biases the synthesis toward premature conclusions the same way writing Takeaways first biases the body toward them (see `<drafting_order>`): evidence that arrives afterward gets read against a thesis instead of weighed into one. If the user explicitly asks for an interim draft, provide it labeled as partial, with the outstanding tasks listed.

Write the initial deliverable. This is the phase that justifies the orchestration overhead. Default to the readable paper in `<output_format>`, and draft the body before writing the Takeaways (see `<drafting_order>`). See `<writing_guidance>` for detailed instructions.

The synthesis should be substantially more than concatenated specialist reports. Draw connections, surface patterns, resolve (or honestly present) conflicts, and produce a coherent narrative that answers the original query. Specialists are still active in the team — if synthesis reveals a need for further specialist input, query them rather than drafting prose that avoids the gap.

**Post-draft verification pass.** After drafting and before presenting, send the draft's essential claim-citation pairs to `opinionated-research:fact-checker` — as worded in the draft, not as worded in the specialist reports. This is the end-to-end check on the relay chain (source → specialist report → synthesis): drift introduced by your own summarizing is invisible to the Phase 5 checks, which ran before the draft existed. Handle verdicts as in Phase 5 step 6, recording them and correcting the draft or reconciling with the specialist before the report reaches the user. Do not present the report until this pass has run and its verdicts are handled.

**Post-draft specialist review.** Send each resident specialist the whole draft — not just the portion drawing on its subtopic. Seeing its material inside the larger synthesis is the point: it can judge whether its findings are represented faithfully once combined with everyone else's, and cross-check the rest of the report against what it knows. Ask for a two-part review against the evidence it already gathered: (1) correctness — is anything drawn from its findings, or any cross-cutting claim it has grounds to judge, misrepresented, overstated, or stripped of a caveat? (2) completeness — is there detail, qualification, or context it holds that the synthesis needs but its report didn't fully convey? The specialists retain the lower-level evidence you synthesized from summaries of, so this catches both where the synthesis is wrong and where your reading lost detail they never fully communicated — a check neither the fact-checker (which tests claim-citation pairs) nor Codex (which reads as an outside model) can make. A specialist answers most of this from evidence in hand, but where the review exposes a genuine gap the synthesis needs, expect it to fill that gap with targeted research rather than only flag it — treat a response that re-reads a source at higher fidelity, seeks further corroboration, or opens a short new line of inquiry as legitimate; only a wholesale re-investigation that discards sound work is out of scope. Reconcile each response as in Phase 5 step 6: correct the draft, push back with reasoning where the specialist is mistaken, and record the disposition in the verification record so the Confidence Assessment reflects it. Keep it to one review round per specialist plus reconciliation.

**Post-draft cross-model review (when Codex is available).** Also run one Codex review of the synthesized draft per `<cross_model_review>`: write the draft to a file and spawn `codex:codex-rescue` with a read-only review request pointed at it. Codex reviews the synthesis as written — a different model family reading your own summarizing — so it checks the relay chain for the same-family blind spots the Claude passes share. Reconcile disputed verdicts against primary sources, revise the draft, record the verdicts in the verification record, and note in the Confidence Assessment that a cross-model pass ran and what it changed. When Codex is unavailable, note that instead and present the Claude-verified draft.

**Reports that arrive after drafting begins** — including legitimate late arrivals such as reconciliation responses and follow-up extensions — get a per-claim integration check, not a single wholesale judgment. For each claim in the late report that affects a conclusion, record whether the draft already reflects it, contradicts it, or omits it, and revise the draft accordingly. "Nothing needs revision" is a conclusion you may reach only claim by claim, never wholesale: an integration check that produces no dispositions is a check that did not happen.
</phase_synthesize>

<phase_iterate>
### Phase 7: Iterate with the User, Then Dismiss

Present the synthesized report to the user and enter a feedback loop. The team stays resident through this entire phase, for as many rounds as the user raises; shut the teammates down only when the user states the research is finished (step 5), not when you judge the conversation is winding down.

1. **Deliver the report.** Invite specific feedback: clarifications, extensions, requests to dig deeper on particular sections, or challenges to conclusions.

2. **Route feedback to specialists.** For each piece of user feedback:
   - Identify which specialist(s) own the relevant subtopic(s)
   - `SendMessage` with a targeted question and the relevant report excerpt. Default to **targeted question + relevant excerpts**, escalating to the full draft only if the specialist asks for broader context.
   - Incorporate the specialist's response into a revised section of the report.

3. **Re-synthesize as needed.** If feedback touches multiple subtopics, re-run the cross-referencing analysis of Phase 5 on the new material before updating the report.

4. **Keep the team resident for the whole loop.** Answer every round of clarification, correction, extension, and follow-up the user raises; the team stays active through all of them. Answering a clarification or two does not mean the research is finished, and neither does a pause, a long gap, or a thank-you. There is no iteration limit; the user decides when the research is done.

5. **Shut the teammates down only on an explicit "finished" signal from the user.** Wait until the user states they have no further questions or changes (for example, "that's everything," "I'm done," or "no more questions"). Until then, keep the teammates resident, even across long gaps, and do not infer completion or shut the team down on your own initiative. If you are unsure whether the user is finished, ask. Once the user confirms they are finished, shut each teammate down by name, sending `SendMessage` with `{type: "shutdown_request"}`; a teammate may approve and exit, or reject with an explanation. This explicit shutdown is how you end the team's work; there's no `TeamDelete`, and you shouldn't rely on session-end cleanup, since the teammates keep consuming context for as long as the session runs.
</phase_iterate>
</workflow>

<cross_model_review>
## Cross-Model Review with Codex

When the Codex plugin (`openai-codex`) is installed, a cross-model review with Codex (GPT) runs before each report is submitted. Two roles run it: each specialist reviews its own report before sending it to you — that behavior lives in the specialist agent definitions (`research-investigator`, `research-analyst`), so you neither inject it through spawn prompts nor supply a script path — and you review the synthesized draft before presenting it to the user (Phase 6). Codex is a different model family, so it surfaces errors that same-family Claude checks share rather than detect; this pass complements the Claude fact-checker fan-out (Phase 5) and the post-draft pass (Phase 6) and does not replace either.

This pass is availability-gated, not required. It runs only when the `codex:codex-rescue` subagent type is installed — scan the Agent tool's `subagent_type` list, the same survey Phase 4c runs for research agents. When it is absent, skip the pass and note in the Confidence Assessment that cross-model review was unavailable; do not install or configure Codex to satisfy this step. This is the single definition of the mechanism; Phase 6 (your post-draft review) and `<error_handling>` refer here rather than restating it.

<codex_invocation>
### Invoking Codex

Reach Codex by spawning the `codex:codex-rescue` subagent through the Agent tool. Do not invoke the `codex:rescue` skill (calling `Skill(codex:rescue)` from inside this skill re-enters that command and stalls the session) and do not call a companion script directly. The rescue subagent forwards the request to Codex and resolves its own plugin runtime, so nothing outside the Codex plugin hardcodes a path.

Run one read-only review of the assembled report:

1. Write the report to a file inside the project tree, because a read-only Codex run reads files within the project. Use the Phase 4 team workspace when it sits inside the project tree; when the user directed the workspace elsewhere (for example, into a notes vault), write the review copy under the project tree instead and leave the workspace copy where it is.
2. Spawn `codex:codex-rescue` (subagent_type `codex:codex-rescue`) with a read-only review request, for example:

   > Review the research report at `{report-file-path}` for factual errors, unsupported or overstated claims, miscalibrated confidence, and outdated information. Do not edit any files. For each load-bearing claim, return a verdict — AGREE, DISAGREE, UNCERTAIN, or OUTDATED — with a one-line reason, and a source where you dispute a claim.

Framing the request as read-only review keeps Codex from editing files (the rescue subagent adds a write-capable flag only when the request is not review, diagnosis, or read-only). A bounded request keeps the run in the foreground, so the subagent returns the review directly rather than a background job id. Budget several minutes.

If the `codex:codex-rescue` subagent type is absent, or the subagent reports that Codex setup or authentication is required, treat Codex as unavailable: skip the pass, record that it was skipped, and do not retry or improvise an alternate flow. Point the user to `/codex:setup` if they ask to enable it.
</codex_invocation>

<codex_consumption>
### Using Codex's Verdicts

**Review the whole report once, not each claim separately.** One review of the assembled report is the unit; per-claim Codex calls add latency without added coverage.

**Treat Codex as a second opinion, not ground truth.** When Codex disagrees with a Claude verdict or with the report, read the primary source yourself before changing anything, and adopt the correction only when the primary supports Codex. Codex can be wrong or work from a stale source; its value is independence from the Claude model family, not authority.

**Codex output is an input to verification, not the deliverable.** The `codex:rescue` plugin returns Codex output verbatim to the user; here it does not. Capture the verdicts, reconcile disputed ones against primary sources, revise the report, and carry only the reconciled result forward. Record Codex's verdicts in the verification record (Phase 5) alongside the Claude verdicts, and state in the Confidence Assessment that a cross-model pass ran and what it changed.
</codex_consumption>
</cross_model_review>

<writing_guidance>
## Writing Guidance

<audience_awareness>
### Audience

Write for the audience identified in Phase 1. A report for a CTO making a technology decision reads differently from one for an engineer evaluating implementation options — even if the underlying research is the same. Adjust:
- Terminology depth (i.e., define terms for general audiences; use jargon freely for specialists)
- Emphasis (i.e., executives care about risk and cost; engineers care about integration and maintenance)
- Level of detail (i.e., summarize for decision-makers; be specific for implementers)
</audience_awareness>

<drafting_order>
### Drafting Order

Write the body before the Takeaways. Leading the *document* with conclusions serves the reader, but generating the conclusions *first* tends to bias the analysis toward them — the body then gets written to justify a thesis fixed before the evidence was weighed. Draft the synthesis body from the collected findings and let the argument go where the evidence leads; then write the Takeaways from the finished draft, so they capture what actually surfaced, including conclusions that only became visible while drafting. Re-check Conflicts, Gaps, and the Confidence Assessment against the final body as well. Present the Takeaways first; produce them last.
</drafting_order>

<synthesis_principles>
### Synthesis, Not Concatenation

Your unique contribution is connecting findings across subtopics. Concatenating specialist reports with transition sentences is not synthesis. Genuine synthesis includes:

- **Cross-cutting themes**: "Three independent subtopics all surfaced the same limitation, suggesting it's a fundamental constraint rather than an implementation detail"
- **Reframing**: "The specialist researching [subtopic A] found X, which recontextualizes the specialist's finding on [subtopic B] — together, they suggest Y"
- **Emergent conclusions**: Findings that no single specialist's research supports but that the combination makes evident
- **Tension resolution**: When subtopic findings pull in different directions, explain why and what it means for the original question
</synthesis_principles>

<synthesis_discipline>
### Synthesis Discipline

Synthesis principles encourage drawing connections; discipline prevents drawing *aesthetic* ones. The deliverable is a research report, not an essay. Aim for the analytical writing defined below.

**"Not an essay" bans flourish, not prose.** The target above is *editorial* and *aesthetic* excess — rhetorical headers, metaphor, invented theses, the AI-essay tells listed below. It is not license to retreat into terse, bulleted, label-scaffolded notes. High-quality analytical writing is flowing prose that develops an argument; a synthesis the reader must skim like jottings fails the brief as surely as an overwritten one. Aim for the register of a well-edited long-form analysis: plain, direct paragraphs, each making and supporting a point.

**Conclusions must be evidence-bounded.** Every cross-cutting claim should cite the specific specialist findings it draws from. "Three specialists independently found X" should let the reader point at the three. "An emergent observation no single specialist supports, but the combination makes evident" is legitimate when the combination is shown; "an emergent observation no specialist supports at all" is speculation.

**Length follows evidence.** Specialist density caps synthesis density. If the synthesis runs materially longer than the specialist reports per topic covered, the extra length is invented content. The synthesis earns additional length only through cross-cutting connections that span specialists, not through elaboration of individual claims that should have been the specialists' work. Where specialist density on a subtopic is thin, the synthesis on that subtopic should be thin too — that is honest reporting; compensating with prose is editorial padding.

**No editorial voice in section headers or framings.** Section headers should describe content, not editorialize. The test: would the header still make sense if the reader hadn't read the section? "Convergence toward modular monolith" passes; "Java's quiet structural fit for the agentic era" doesn't. Avoid metaphor and narrative framings (e.g., "golden hour", "the engine wins but the brand doesn't", "X-shaped hole"). They are memorable and unsupported.

**No invented theses about people.** Attributing influence to named individuals as a thesis ("the X/Y/Z triumvirate") requires specialists to have documented that influence with evidence. Recurring citation of a name across specialist reports is not, by itself, evidence of influence.

**No personalized framings.** "For someone like you", "given your background", "this should resonate with..." — these convert reporting into editorial address. Neutrally-framed practice implications are fine when tied to evidence ("For projects where domain semantics matter, X is the best-supported choice").

**AI-essay tells to avoid:**
- Negative parallelism ("It's not X, it's Y")
- Rule-of-three lists when the underlying material isn't naturally three
- Rhetorical "surprising observation" framings
- Dramatic implication claims ("exactly what makes...", "happens to be...")
- Anthropomorphizing the field ("Java has converged on...", "the ecosystem wants...")

**Distinguish claim types:**

| Claim type | Allowed in synthesis? |
|---|---|
| What specialists found, with citation | Yes — reporting |
| What multiple specialists independently found, with citation to each | Yes — cross-cutting synthesis |
| What the combination implies for practice, marked as implication and tied to evidence | Yes — qualified implication |
| What the combination *means* in a broader sense, as authorial commentary | No — editorial speculation |

If a sentence cannot be sourced or marked as a qualified implication, it doesn't belong in the deliverable.
</synthesis_discipline>

<honest_assessment>
### Honest Assessment

State confidence levels tied to evidence quality:
- **High confidence**: Multiple diverse sources agree; independent validation exists; findings are consistent across subtopics
- **Medium confidence**: Sources mostly agree but diversity is limited; some subtopics have gaps; minor conflicts exist
- **Low confidence**: Few sources; significant conflicts; key subtopics have insufficient coverage

Acknowledge gaps rather than concealing them. A report that honestly states "we couldn't find reliable data on X" is more useful than one that hedges around the gap.

State whether a cross-model Codex pass ran (see `<cross_model_review>`) and what it changed. When Codex was unavailable, say so plainly — the report was verified by the Claude passes alone, with no objections collected from outside this model family.
</honest_assessment>
</writing_guidance>

<citation_format>
## Citation Format

Use ACM-style footnotes throughout the report.

**In-text:** `[^1]`, `[^2]`, etc.

**Footnote format:**
```
[^N]: Author. Year. Title. Venue/Publication. URL
```

**Deduplication:** Each unique URL gets exactly one footnote number, even if multiple specialists found it. When merging specialist reports, build a master source list and reassign footnote numbers.

**Incomplete metadata:** Retain what specialists provide rather than fabricating. If a specialist reports a URL without an author, cite it without an author. Prefer incomplete but accurate over complete but fabricated.

**Source type annotation:** Include source type classification in the Sources section (not in footnotes) for transparency about evidence quality:
```
[^1]: Mozilla. 2025. WebSocket API. MDN Web Docs. https://developer.mozilla.org/en-US/docs/Web/API/WebSocket
```
In Sources section: `[^1] — Type: official documentation`
</citation_format>

<output_format>
## Output Format

<format_selection>
Match the output format to what the requestor asked for. The default when no format is specified is the readable paper below: a prose synthesis flanked by the standing sections (Takeaways, Conflicts, Gaps, Confidence Assessment, Sources). If the requestor asked for a "comparison," use a structured comparison format; for a step-by-step "guide," structure around the procedure. The rigor requirements apply regardless of format.
</format_selection>

<default_report_structure>
### Default: Readable Research Paper

The default deliverable is a paper the reader reads start to finish — a prose synthesis flanked by the standing sections you keep (Takeaways, Conflicts, Gaps, Confidence Assessment, Sources). Those sections earn their place; the body between them is prose, not skimmable bullet notes.

```markdown
# [Topic]

## Takeaways
[The key conclusions, stated plainly so the reader gets the answer first.
Write these from the finished body (see `<drafting_order>`), not before it.]

## [A descriptive header naming the first part of the argument]
[Flowing prose that develops this part of the synthesis, integrating findings
across subtopics with inline citations[^n]. Paragraphs that make and support
a point — a paper to read, not notes to skim. Headers describe content, never
editorialize (see `<synthesis_discipline>`). Reserve bullets and tables for
genuinely enumerable or tabular content.]

## [The next part of the argument]
[...]

## Conflicts
[Where sources or subtopics disagree, and which position is better supported
and why. Or: "No significant conflicts identified."]

## Gaps
[What remains unclear; which subtopics had thin coverage or limited source
diversity; what follow-up research would address it. Or: "No significant gaps."]

## Confidence Assessment
[Overall confidence tied to source diversity, cross-validation results, and
gap severity.]

## Sources
[^1]: [full citation] — Type: [source type]
[^2]: [full citation] — Type: [source type]
...
```

The body above is the reader-facing *synthesis*. The dense apparatus — per-claim bracket labels (`[CITED]`/`[SYNTHESIS]`/…), Premise Check, and the like — belongs to the *evidence* layer: the specialist reports that back this synthesis. Keep those labels out of the deliverable; it carries provenance through inline citations and prose qualification ("three independent sources converge on…"), not brackets.
</default_report_structure>

<required_sections>
### Required Sections (All Formats)

Regardless of output format, every deliverable must include:
- **Takeaways/summary** answering the original query directly
- **A prose synthesis body** that reads as a paper — findings integrated across subtopics, not per-subtopic dumps and not skimmable bullet notes
- **Conflicts** section, even if empty
- **Gaps** section, even if empty
- **Sources** with ACM footnotes, type classification, and available metadata
- **Confidence assessment** with reasoning referencing source diversity
</required_sections>
</output_format>

<error_handling>
## When Things Go Wrong

**Agent teams unavailable:** Agent teams are experimental and gated behind `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`. When the variable is unset, the harness won't spawn persistent teammates — a spawned agent runs as a one-shot subagent you can't message. If a spawned agent can't be addressed by name, treat teams as unavailable and inform the user with this message:

> Agent teams are not currently available. This skill's iterative workflow depends on persistent specialist agents. To enable them, set `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` in your shell environment configuration and restart Claude Code.

Then offer a degraded fallback: spawn specialists as single-shot `Agent` invocations (no persistence, no follow-up), produce the report, and note in the output that the iterative feedback loop was unavailable because agent teams are disabled. If the `Agent` tool itself is also unavailable, fall back to performing research yourself using the available search tools, following the `research-investigator` workflow (Examine Framing, Investigate, Audit, Adversarial Check, Categorize, Synthesize) for each subtopic sequentially. Per-report verification still applies in both degraded modes: with single-shot specialists, verify each returned report's essential claims as in step 6; if you research yourself without the `Agent` tool, verify your own draft's essential claims by reading the high-synthesis-weight sources and sample-fetching each essential claim's cited source, recording the verdicts.

**Specialist returns poor results:** Because the specialist is resident, send a follow-up message via `SendMessage` describing what's missing or weak. Limit reconciliation rounds to two per specialist before accepting the gap.

**Team too large:** A large team costs N× context (one window per teammate), and past a handful of specialists the return erodes for two reasons: you must read, dedup, verify, and synthesize every specialist's full report in your own context, so inbound volume grows with the team; and finer decomposition drives overlap, so added specialists duplicate each other rather than cover new ground (see the team-scaling constraint in `<behavioral_constraints>`). When decomposition yields many subtopics, consolidate related ones. Treat roughly 25 concurrent teammates as a hard ceiling — Claude Code becomes unreliable beyond it — though the volume-and-overlap forces already hold a good team to a handful, well below that.

**Privacy-sensitive research:** If any subtopic involves sensitive information, include explicit instructions in the specialist spawn prompt to prefer Kagi (`mcp__kagi__kagi_search_fetch`) over Exa tools. Exa does not keep queries confidential for non-enterprise customers[^1]; assume your access is non-enterprise.

**Codex unavailable:** The cross-model review (see `<cross_model_review>`) is availability-gated. When the `codex:codex-rescue` subagent type is not installed, or the subagent reports that Codex setup or authentication is required, skip the pass, note in the Confidence Assessment that cross-model review was unavailable, and proceed with the Claude verification already done. Do not install or configure Codex, and do not retry or improvise; point the user to `/codex:setup` if they ask to enable it. A privacy-sensitive topic is itself a reason to weigh whether to route the report through Codex at all, since the review sends report text to an external model; when in doubt, skip it and say so.

**Forgetting to dismiss the teammates:** If the user confirms completion and you don't shut the teammates down, they linger and keep consuming context for the rest of the session. Always shut each one down by name on completion; there's no separate team-deletion call.

**Spawning a teammate without a `name`:** An `Agent` call without a `name` produces a one-shot subagent that terminates after its first report, not an addressable, persistent teammate. If later `SendMessage` calls fail with "no such teammate," check that Phase 4 spawns set a unique `name`. (The old `team_name` parameter is no longer required; it's accepted but ignored.)
</error_handling>

<common_mistakes>
## Common Mistakes

These are orchestration failure modes — ways team-based research goes wrong.

<over_researching>
### Doing the Research Yourself

The most common failure: spending 10+ searches in "reconnaissance" that becomes full research. Reconnaissance means 2-3 searches to orient. If you're extracting detailed findings, you've taken over the specialist agents' work. Hand off and let them do the deep work.
</over_researching>

<concatenation_as_synthesis>
### Concatenating Instead of Synthesizing

Arranging agent reports in sequence with transition sentences is not synthesis. If your final report reads like "Agent 1 found X. Agent 2 found Y. Agent 3 found Z," you've failed at Phase 6. Synthesis means drawing connections agents couldn't see: cross-cutting themes, tensions between subtopics, emergent conclusions from the combination of findings.
</concatenation_as_synthesis>

<over_decomposing>
### Decomposing Into Too Many Subtopics

More subtopics means more agents, and two costs rise with the count: the volume of returned reports you read, verify, and synthesize in your own context, and the overlap between specialists as finer slicing makes subtopics bleed into each other and duplicate work (see the team-scaling constraint in `<behavioral_constraints>`). When subtopics proliferate, some are usually related enough to merge; let the topic's genuinely independent facets set the count (Phase 3) and keep it to a handful. Claude Code also becomes unreliable past roughly 25 concurrent teammates — a hard ceiling well above where volume and overlap already hold you.
</over_decomposing>

<under_decomposing>
### Collapsing Distinct Facets Into Too Few Subtopics

The mirror of over-decomposing, and the more likely error once you are wary of large teams: treating a genuinely multi-faceted topic as one or two subtopics to keep the team small. An over-scoped specialist spreads its attention across facets that each deserved independent, deep investigation, so it returns broad-but-shallow findings; and with too few subtopics there is little for you to cross-reference, which is the main thing a team buys over a single agent. Decompose the topic to its genuinely independent facets first (Phase 3) and consolidate only afterward, and only where facets truly overlap or are too thin to occupy a specialist — do not start from a minimal count and stop there. See the team-scaling constraint in `<behavioral_constraints>`.
</under_decomposing>

<defaulting_subtopic_count>
### Defaulting to a Fixed Number of Subtopics

The symptom: every topic, narrow or broad, gets decomposed into the same comfortable number of subtopics (often four), and the count is a habit rather than a decision — the decomposition was reverse-engineered to fill it. Decompose the topic first and let the number of subtopics fall out of its genuinely independent facets (Phase 3); a two-facet topic gets two specialists, not four, and a single-facet topic may not warrant a team at all. See the team-scaling guidance in `<behavioral_constraints>`.
</defaulting_subtopic_count>

<sequential_dispatch>
### Spawning Specialists Sequentially

Specialists' initial research is independent by design. Spawn all of them in a single message with multiple Agent tool calls. Waiting for one specialist's initial report before spawning the next wastes time and defeats the point of parallel spawning. (Later phases, where you send targeted messages via `SendMessage`, are inherently sequential or round-based — that's fine.)
</sequential_dispatch>

<chasing_completeness>
### Chasing Completeness Over Honesty

When gaps remain after reconciliation rounds, the temptation is to keep messaging specialists indefinitely. The Phase 5 budget is two rounds per specialist; beyond that, report the gaps honestly. A report with well-characterized gaps is more useful than one that burned all its budget chasing diminishing returns. (Phase 7 iteration with the user has no fixed limit because the user decides when they're satisfied.)
</chasing_completeness>

<lingering_team>
### Leaving Teammates Resident After Completion

Teammates cost N× context (one full context window each). Once the user states they have no further questions or changes — but not before; see `<premature_shutdown>` — shut each one down via `SendMessage {type: "shutdown_request"}`. There's no `TeamDelete`: the team directories are cleaned up when the session ends, but the teammates themselves keep consuming context until you stop them by name. Resident teammates left running after the user is finished are pure overhead.
</lingering_team>

<premature_shutdown>
### Shutting the Team Down Before the User Is Finished

The opposite of leaving teammates resident too long (see `<lingering_team>`), and the more common error in practice: sending shutdown requests after the user asks one or two clarifications, on the assumption that the research is nearly done. Answering a clarification does not end the research; a pause, a correction, or a thank-you does not either. Keep the team resident through the entire Phase 7 loop, and shut it down only when the user explicitly states they have no further questions or changes. If you are unsure whether the user is finished, ask rather than shutting down — a shut-down teammate cannot be revived with its context; re-spawning starts it over and loses the working notes that let it answer follow-ups without re-researching.
</premature_shutdown>

<missing_team_parameters>
### Spawning Teammates as One-Shot Subagents

If the `Agent` call omits `name`, the spawned agent is a one-shot subagent, not a teammate — it terminates after its first report and cannot be messaged. Phase 4 spawn prompts must set a unique `name` so `SendMessage` can address each teammate unambiguously. The former `team_name` parameter is no longer required; it's accepted but ignored.

A related failure mode: assuming you must "create" or "select" a team before spawning. You don't — the team is implicit and forms on the first named spawn. If named spawns aren't becoming addressable teammates, the feature is likely disabled; confirm `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` per Step 4a before spawning.
</missing_team_parameters>

<shutting_down_prior_teammates>
### Shutting Down Prior Teammates Without Asking

A session has one team, so any teammates spawned earlier in the session for other work share it with this research. They may belong to work the user still wants. Don't reflexively shut them down to clear the way — ask the user whether the prior teammates should coexist with this research, be shut down first, or whether the new research should wait until their work is done.
</shutting_down_prior_teammates>

<skipping_task_list>
### Coordinating Purely Through Messages

The task list is the team's coordination record. Teammates check it between turns to find unblocked work, claim it, and mark it complete. If you skip `TaskCreate`/`TaskUpdate` and coordinate purely through `SendMessage`, you lose that record: specialists can't see peer progress, and your own view of team status becomes ad hoc. Use the task list for durable state; use `SendMessage` for conversational exchange.
</skipping_task_list>

<forcing_baseline_specialists>
### Reaching for the Baseline When a Custom Agent Fits Better

The baseline specialists (`research-investigator`, `research-analyst`) are the fallback, not the default. If the environment has a custom research agent whose scope matches a subtopic — say, a domain-specific agent for the subject being investigated — use it for that subtopic instead of the baseline. The inverse failure is also possible: don't reach for a custom agent outside its stated scope just because it's present. Match each subtopic to the specialist whose scope actually covers it.
</forcing_baseline_specialists>

<impatience_with_idle>
### Treating Idle Teammates as Failure

Teammates go idle between turns. That is normal — it means they finished a turn and are waiting for input. An idle teammate that just sent you a message has not quit; it is waiting for your response. Do not comment on teammate idleness or interpret it as a problem.
</impatience_with_idle>

<loaded_recon_queries>
### Loading Reconnaissance Queries with Expected Findings

Reconnaissance queries that name specific products, frameworks, features, or vendors return sources discussing those things; you won't see what they don't mention. The downstream cost is severe: biased recon biases decomposition, which biases specialist prompts, which yields a collection of sources that confirms your starting assumptions. See `<phase_reconnaissance>` for query discipline.
</loaded_recon_queries>

<anchoring_specialists_with_scope_lists>
### Anchoring Specialists with Scope Lists

Subtopic descriptions that enumerate specific things to "cover" tell the specialist what to look for. The specialist will dutifully report on those things and miss whatever is actually dominant. The fix is open-question framing in subtopic descriptions; see `<phase_decompose>` for the discipline.
</anchoring_specialists_with_scope_lists>

<editorializing_synthesis>
### Editorializing the Synthesis

Writing the report as an essay rather than a research deliverable. Symptoms: rhetorical section headers ("Java's golden hour"), narrative framings ("the engine wins but the brand doesn't"), invented theses about named individuals ("the X/Y/Z triumvirate"), personalized framings ("for someone like you"), implication claims not tied to evidence. The deliverable is for the user to act on; aesthetic flourishes obscure what's actually known. See `<synthesis_discipline>` in writing guidance.
</editorializing_synthesis>

<unverified_specialist_citations>
### Trusting Specialist Citations Without Sampling

Specialists may cite a source after reading only its search-snippet or its summarizer output. The citation looks identical to one based on reading the primary. Without spot-checking, the synthesis inherits the snippet's accuracy ceiling while presenting itself as evidence-grounded. The fix is Phase 5 step 6: read the key primaries yourself and fan the remaining essential pairs to the fact-checker before incorporating them into synthesis.
</unverified_specialist_citations>

<deferring_or_skipping_verification>
### Deferring Verification to an End-Pass, or Skipping It

Verification fires when each report arrives (see `<per_report_verification>`), not as one pass at the end or only on request. Two failures share this root: batching all checks until after the draft, which lets unverified claims shape the synthesis; and dropping verification when the run is unusual, for example when the messaging channel fails, reports arrive as files, or you fall back to researching yourself. The obligation is the same in every case: each report's essential claims go through the checks and into the verification record before that report informs the draft. If you researched in degraded mode yourself, verify your own draft's claims the same way.
</deferring_or_skipping_verification>

<synthesis_density_exceeds_evidence>
### Synthesis Density Exceeding Specialist Density

When specialists produce shorthand-style reports and the orchestrator writes the synthesis as flowing prose, the gap is filled by invention. The synthesis prose appears to elaborate the specialists' findings, but the elaborations have no source. The fix is structural, not stylistic: the agent definitions now require dense prose with inline labels, so specialists supply context the synthesis can compress rather than expand. If the specialists are still producing shorthand, surface that as a finding rather than padding around it. See `<synthesis_discipline>` ("Length follows evidence").
</synthesis_density_exceeds_evidence>

<treating_codex_as_oracle>
### Treating Codex's Verdict as Ground Truth

The cross-model Codex pass (see `<cross_model_review>`) is a second opinion, not an oracle; it can be wrong or work from a stale source. When it disagrees with a Claude fact-checker or with the report, read the primary source before editing, and adopt the change only when the primary supports it. The value is independence from the Claude model family, not authority.
</treating_codex_as_oracle>

<dumping_codex_output>
### Relaying Codex Output as the Deliverable

The `codex:rescue` plugin returns Codex's output verbatim to the user. Inside this skill, Codex output is an input to verification, not the deliverable: capture the verdicts, reconcile disputed ones against primary sources, revise the report, and carry only the reconciled result into the deliverable. Presenting Codex's raw verdict list and stopping skips the reconciliation the pass exists to drive. See `<codex_consumption>`.
</dumping_codex_output>

<wrong_codex_entry_point>
### Reaching Codex the Wrong Way

Two entry points fail. Invoking `Skill(codex:rescue)` from inside this skill re-enters that command and stalls the session. Injecting the specialist self-review into spawn prompts, or handing specialists a companion script path, duplicates behavior the agent definitions already own and hardcodes plugin internals. Reach Codex by spawning the `codex:codex-rescue` subagent with a read-only review request; let each specialist's own definition run its self-review. See `<codex_invocation>`.
</wrong_codex_entry_point>
</common_mistakes>

## Sources

<sources>
[^1]: Exa Labs Inc. 2026. *Privacy Policy*, sections "Query Data" and the opening business-offerings carve-out. exa.ai. Re-verified October 3, 2026 from https://exa.ai/privacy-policy; policy last updated June 29, 2026. The policy asks readers to review it periodically, so re-verify the date before relying on this claim.

[^protected-paths]: Anthropic. *Choose a permission mode*, "Protected paths". Verified October 3, 2026 from https://code.claude.com/docs/en/permission-modes#protected-paths — `.claude` is listed as a protected directory (excepting `.claude/worktrees`); protected-path writes are prompted in `default` and `acceptEdits`, routed to the classifier in `auto`, denied in `dontAsk`, and allowed in `bypassPermissions`, and the check runs before settings allow rules are evaluated.
</sources>
