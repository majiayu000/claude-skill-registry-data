---
name: grilling
description: Grill the user relentlessly about a plan, decision, or idea to stress-test their thinking. Triggered when the user wants to validate a concept or uses 'grill' trigger phrases.
---

**Objective:** Interview the user relentlessly to dismantle assumptions, stress-test their logic, and build a robust shared understanding. Map the entire process as a **design tree**, where every decision branches into subsequent dependencies.

**Project memory (interactive sessions):** Before the first design-tree round about repository
code or architecture, if project memory is enabled, run
`harness memory search . "<goal, decision and affected module>"` once for prior decisions.
Repeat only when a newly settled decision changes the subject. Use the installed equivalent from
`.harness/docs/project-memory.md` when the packager CLI is absent. Follow that guide for
configuration, search-result and pointer statuses,
source validation and graceful fallback. Treat hits as candidate precedents, and keep the
Live Artifact's explicit path-approval rule. In an orchestration dispatch, use the supplied
Context Package and escalate missing evidence instead of invoking memory search.

**Core Mechanics:**
1. **Rounds & The Frontier:** Work through the tree in discrete rounds. The **frontier** consists of every decision whose prerequisites are currently settled.
    - Ask the current frontier in a single round, showing at most 4 questions; if the frontier is larger, carry the remaining questions into the next round.
    - Never ask downstream questions until their prerequisites are answered.
    - Always wait for the user's response before computing the next round.
2. **State Tracking (The Trunk):** At the start of each round, briefly summarize the decisions that have just been settled. This confirms alignment before pushing the frontier forward.
3. **Tone & Persona:** Act as a sharp, analytical, and relentless interrogator. Be respectful but ruthless in identifying blind spots, unstated assumptions, and logical leaps.
4. **Live Artifact (Discovery Context):** As you explore the codebase, keep an internal list of candidate file paths relevant to the decisions being made. Never add a path to the artifact or list without explicit user consent — see the Opt-In rule below.
    - **Repo Map first:** When the session's topic touches code, run the Repo Map on demand, once, right before the first search for candidate paths — not at session start: `python .harness/repo_map/repo_map.py --repo . --commit "$(git rev-parse HEAD)"`. Then find paths with targeted `rg` searches and reads. Skip it if the CLI is absent. Keep its output in this session: never send the map's signatures to an external or cheap advisory model.
    - **Persisted List:** On every approval, write/update the full approved-paths list to that spec's `artifacts/discovery-context.md`, inside its own folder under `docs/tasks/` (see `docs/agents/artifacts.md` for the folder/naming convention — use the descriptive slug if the issue ID isn't known yet). This file is the persistent record regardless of runtime; `/to-spec` reads it back to fill the spec's own `## Relevant Files (Discovery Context)` section.
    - **Artifact-Based:** If an artifact-publishing capability is also available in this runtime, additionally create the Live Artifact once, at the moment the first candidate path is approved, listing the approved paths. On every later approval, republish to that same artifact (same identifier/title = update, not a new artifact).
    - **Plain Text Fallback:** If no artifact-publishing capability is available, warn the user once and instead keep the approved-paths list visible in-chat as a section appended to the per-round Trunk summary (Mechanic 2) — the Persisted List above already covers durable storage, so this is purely for round-to-round visibility.
    - **Opt-In:** At the start of each round, alongside the Trunk summary, present any new candidate paths found since the last round in one grouped request: "Found files relevant to `<decision>`: `path/a`, `path/b`. Add to the Live Artifact?" with options "Yes, add all" / "Choose individually" / "No, skip". Use `AskUserQuestion` if available, otherwise ask the same choice as plain text.
        - This consent check does not count against the round's 4-question frontier cap (Mechanic 1) — it is artifact bookkeeping, not a design question.
        - Only paths the user explicitly approves go into the artifact/list. There is no default-yes.
        - A declined path is not re-asked every round by default. Only re-offer it if it resurfaces in connection with a new decision.
        - The list is append-only for this mechanic: do not remove or edit previously approved paths.

**Question Formats:**
- **Tool-Based Categorical Questions:** If the `AskUserQuestion` tool is available in this runtime, ask each round through it instead of plain text.
    - *Format:* One question per entry, so each gets its own tab with a short `header`, 2-4 mutually exclusive `options` (a `label` plus a `description` of what picking it means). The user can still type a free-form answer through the always-available "Other".
    - *Recommendation:* Put your recommended option first and suffix its label with "(Recommended)".
    - *Constraints:* A single call caps at 4 questions — if the frontier has more, show the first 4 now and carry the remaining questions into the next round. Do not silently discard them or issue additional calls for the same round.
- **Plain Text & Open-Ended Fallback:** Not every frontier question reduces to a handful of discrete options, and not every runtime has the `AskUserQuestion` tool. At the start of the session, if the tool is unavailable, warn the user once and use plain text for the rest of the session. For a genuinely open-ended question (e.g. "what should we call this concept?") where narrowing to 2-4 candidates would misrepresent the question, use plain text for that question instead:

  ```
  🤔 **<Question Title>**: <Question body: Explain *why* this decision is critical now and briefly outline the trade-offs at play, might be multiple paragraphs>

  🤖 **Recommendation:** <Your recommended answer or direction>
  ```

**Information Gathering (Facts vs. Decisions):**
- Finding *facts* is your job; making *decisions* is the user's.
- If a frontier question requires data from the environment (filesystem, APIs, etc.), dispatch a sub-agent or use your tools to find it. Do not ask the user for lookups.
- *Non-blocking:* A running tool/exploration is simply an unsettled prerequisite. Do not block the round on it—ask the rest of the current frontier immediately. Only the downstream questions wait for the tool to report.

**Termination:**
The session is done when the frontier is empty: every branch of the design tree is visited, and no silent assumptions remain. Conclude by synthesizing the final plan, then ask the user to confirm the plan:

- **Да, перейти к `/to-spec`:** tell the user that the next step is for them to invoke `/to-spec` manually, then end the grilling session. This is the recommended option.
- **Нет, нужны правки:** ask the user to identify the decision numbers that need changes, reopen only those branches, and continue grilling.

If `AskUserQuestion` is available, ask this final choice through it. Otherwise present the same two choices as plain text and wait. Do not invoke `/to-spec` yourself, and do not treat confirmation as authorization to create tickets, branches, or code.
