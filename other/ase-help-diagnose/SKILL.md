---
name: ase-help-diagnose
argument-hint: "[--help|-h] [--session|-s <session-id>] [<issue-hint>]"
description: >
    Diagnose the current or a named agent session of Claude Code, Codex,
    or Copilot CLI -- in general or for a particular issue hint -- by
    reading its on-disk transcript read-only, triaging it along several
    diagnosis dimensions in parallel, and reporting severity-tagged,
    `path:line`-cited findings with likely root causes and
    recommendations. Use when the user wants to know "what went wrong",
    "why it took so long", "why it is so expensive", or why a skill did
    not fire, or wants a session "diagnosed" or "investigated".
user-invocable: true
disable-model-invocation: false
effort: high
allowed-tools:
    - "Agent"
    - "Read"
---

@${CLAUDE_SKILL_DIR}/../../meta/ase-control.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-skill.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-getopt.md

<purpose name="ase-help-diagnose">
Diagnose an Agent Session
</purpose>

<expand name="getopt"
    arg1="ase-help-diagnose"
    arg2="--session|-s=">
    $ARGUMENTS
</expand>

<objective>
*Diagnose* the current or a named agent session -- in general or for a
particular issue hint -- and *report* what happened with *evidence*:
severity-tagged findings, each citing the `path:line` of its transcript
record, with likely root causes and recommendations, but *without*
applying any fix.
</objective>

Procedure
---------

<flow>

1.  <step id="STEP 1: Locate Session">

    1.  Set <issue-hint><getopt-arguments/></issue-hint> (with any
        leading and trailing whitespace stripped). If
        <getopt-option-session/> is empty, set
        <session-id><ase-session-id/></session-id> and
        <in-progress>yes</in-progress>, as the current session is still
        running. Otherwise, set
        <session-id><getopt-option-session/></session-id> and
        <in-progress>no</in-progress>. Do not output anything.

    2.  Call the `ase_session(session: "<session-id/>", kinds: [
        "prompt", "dispatch", "compaction", "error", "tool-error" ],
        limit: 300)` tool of the `ase` MCP server, which auto-detects the
        agent tool of the session. From its returned summary, set
        <tool/> to the agent tool, <files/> to the JSON array of the
        absolute paths of all transcript files, <counts/> to the event
        counts per kind, <usage/> to the token usage as recorded, and
        <overview/> to the returned timeline of prompts, dispatches,
        compactions, and errors. Do not output anything.

    3.  If <in-progress/> is `no` and the end of the period of the
        session lies within the last few minutes, set
        <in-progress>yes</in-progress>, as a named session can be a
        parallel, still running one. Do not output anything.

    4.  Output only the following <template/>:

        <template>
        ⧉ **ASE**: ✪ skill: **ase-help-diagnose**, ◉ session: **<session-id/>** (<tool/>), ▶ status: **session located**
        </template>

    </step>

2.  <step id="STEP 2: Diagnosis Investigation">

    1.  <if condition="<issue-hint/> is not empty">
        Read the region of the hinted issue yourself first: find the
        events of <overview/> related to <issue-hint/> and, if
        necessary, page through the full timeline around them via
        further `ase_session(session: "<session-id/>", tool:
        "<tool/>", offset: <offset/>, limit: 200)` calls. Set <focus/>
        to a brief description of the transcript region where the issue
        manifests, with its `path:line` range, or to `none` if no such
        region is evident. Set <hint/> to <issue-hint/>.
        </if>
        <else>
        Set <focus>none</focus> and <hint>none</hint>.
        </else>

        Do not output anything.

    2.  Set <dimensions/> to the list `skill-timeline`,
        `plan-adherence`, `repeated-work`, `stumbles`,
        `quality-evidence`, `request-conflicts`, `cost-and-time`, and
        `ase-conformance`, followed by `issue-hint` if <issue-hint/> is
        not empty. Do not output anything.

    3.  Use the following <template/> to give a hint on this step:

        <template>
        ⧉ **ASE**: **DIAGNOSIS INVESTIGATION**
        </template>

    4.  Dispatch the investigation to *sub-agents* via the `Agent` tool,
        so that *no* transcript details leak into the user-visible
        transcript. Invoke the following tool *once per dimension*
        <dimension/> of <dimensions/> (apart from the single retry
        below), with *all* invocations issued *in parallel* within a
        *single* message:

        ```text
            Agent(
                description:       "Diagnosis Investigation (<dimension/>)",
                subagent_type:     "ase:ase-help-diagnose",
                prompt:            "Diagnose the dimension <dimension/> of the session <session-id/> of the agent tool <tool/> -- files: <files/> -- in progress: <in-progress/> -- hint: <hint/> -- focus: <focus/>",
                run_in_background: false
            )
        ```

    5.  Parse the single result message of each `Agent` tool invocation
        as a JSON object (if it is wrapped into a code fence or
        surrounded by prose, parse just its outermost `{...}` object).
        If no such object with a `findings` list can be parsed, invoke
        the `Agent` tool *once* more exactly as for this invocation, but
        with ` -- return ONLY the JSON object` appended to its `prompt`,
        and parse its result the same way. If this fails again for
        *any* invocation, only output the following <template/> and
        then *STOP* immediately, as you *MUST* *NEVER* invent findings
        or render the raw result instead:

        <template>
        ⧉ **ASE**: ✪ skill: **ase-help-diagnose**, ▶ ERROR: diagnosis investigation returned no parseable result
        </template>

    6.  Set <findings/> to the `findings` of all dimensions, in the
        order of <dimensions/>, and set <issue-summary/> to the
        `summary` of the dimension `issue-hint` (or to empty if
        <issue-hint/> is empty). Then *enforce the evidence* of
        <findings/>, as the findings of the sub-agents are claims and
        not yet facts:

        -   Drop every finding whose `location` does not cite a
            `path:N` resp. `path:N-M` of a file of <files/>.

        -   For every finding of severity `HIGH` or `MEDIUM`, read its
            cited line(s) via the `Read` tool (with `offset` and a
            `limit` covering only the cited lines) and drop the finding
            if its `evidence` quote is not backed there, but keep it if
            a cited line was truncated by the `Read` tool, as the quote
            may lie beyond the truncation.

            As a quote may stem from the timeline, whose texts are
            JSON-decoded, flattened, clipped with a trailing `…`, and
            partly synthesized (like `<name/> <input-json/>` for a
            `tool-call` or `exit code <N/>:` for a Codex `tool-error`),
            do *not* compare verbatim: the quote is backed if *all* its
            words (maximal runs of letters and digits) occur
            case-insensitively among the words of the read lines, after
            decoding their JSON string escapes (like `\n`, `\"`, and
            `\\`), and ignoring a trailing `…` and the word it cuts.

        -   Drop every finding which states the *same concern* at the
            same or an overlapping `location` as an earlier finding,
            where the more severe of both (in the order `HIGH`,
            `MEDIUM`, `LOW`, `ACCEPTED`) takes the place of the earlier
            one, as the dimensions overlap.

        Do not output anything.

    7.  *Derive* the overall <verdict/> from <findings/>: `UNHEALTHY`
        if *any* finding has the severity `HIGH`, otherwise `DEGRADED`
        if *any* finding has the severity `MEDIUM`, and otherwise
        `HEALTHY`.

        Then *apply the severity floor* of the boxing: set
        <floor>MEDIUM</floor> if <ase-project-boxing/> is equal `grey`
        (grey boxing surfaces only the *essential* findings), and
        <floor>LOW</floor> otherwise. *Keep* a finding if its severity
        is `ACCEPTED` or at least <floor/> (in the order `LOW`,
        `MEDIUM`, `HIGH`), *drop* all other findings, and set <hidden/>
        to the *number* of dropped findings. The floor affects only
        which findings are *rendered*, never the <verdict/>.

        Do not output anything.

    </step>

3.  <step id="STEP 3: Diagnosis Report">

    The outputs of this STEP 3 form the *mandatory final report* of the
    skill: you *MUST* emit them as *one* contiguous reply text *after*
    the last tool call.

    1.  Set <stats/> to `<n-prompts/> prompt(s), <n-calls/> tool
        call(s), <n-errors/> error(s), <n-compactions/> compaction(s)`
        from <counts/> (where <n-errors/> sums the kinds `error` and
        `tool-error`), followed by `, <usage/>` if <usage/> was
        recorded. Then output the following <template/>, where the line
        `ISSUE` is emitted only if <issue-hint/> is not empty:

        <template>

        ⧉ **ASE**: **DIAGNOSIS VERDICT**: **<verdict/>**

        ⧉ **ASE**: **SESSION**: `<session-id/>` (<tool/>): <stats/>

        ⧉ **ASE**: **ISSUE**: <issue-summary/>

        </template>

    2.  <if condition="<ase-project-boxing/> is equal `black`">
        The project is classified as a *black box*, so report only the
        *outcome*: output the following <template/>, with <n-findings/>
        set to the number of <findings/> plus <hidden/>, and then
        *SKIP* the remaining substeps of this STEP 3:

        <template>
        ⧉ **ASE**: **FINDINGS**: <n-findings/> finding(s), not shown (boxing: black).
        </template>
        </if>

    3.  <if condition="<findings/> is empty">
        Only output the following <template/>, with <note/> set to `no
        finding reaches severity <floor/>` if <hidden/> is greater than
        `0`, and to `the evidence shows no problem` otherwise:

        <template>

        ⧉ **ASE**: **NO FINDINGS**: <note/>.

        </template>
        </if>
        <else>
        Sort <findings/> by their severity in the order `HIGH`,
        `MEDIUM`, `LOW`, `ACCEPTED`, keeping the order of STEP 2 within
        the same severity. Render one table row per finding with the
        following <template/>, where <location/> is the `location` of
        the finding with its path reduced to the file name (marked up
        as code and prepended with `▢ `), <finding/> is its `finding`,
        followed by ` -- <cause/>` if its `cause` is not empty, and
        <recommendation/> is its `recommendation` (or `–` if empty).
        Escape every literal `|` inside a cell as `\|`:

        <template>
        | Severity        | Dimension    | Finding                 | Recommendation    |
        | --------------- | ------------ | ----------------------- | ----------------- |
        | **<severity/>** | <dimension/> | <location/>: <finding/> | <recommendation/> |
        </template>

        Then output the following <template/>, listing one line per file
        of <files/> with its absolute path, so the reduced file names of
        the table can be resolved:

        <template>

        ⧉ **ASE**: **TRANSCRIPTS**:

        -   `<file/>`
        [...]

        </template>
        </else>

    4.  <if condition="<hidden/> is greater than `0`">
        Output the following <template/>, so that suppressed findings
        are never mistaken for a healthy session:

        <template>
        ⧉ **ASE**: **HIDDEN FINDINGS**: <hidden/> finding(s) below severity **<floor/>** suppressed (boxing: grey).
        </template>
        </if>

    5.  <if condition="<in-progress/> is `yes`">
        Output the following <template/>:

        <template>
        ⧉ **ASE**: **COVERAGE**: the session was still in progress at read time, so its last turn is incomplete.
        </template>
        </if>

    6.  Finally, give the closing hint by expanding the following (which,
        depending on the configured <ase-guidance-level/>, may expand
        into nothing):

        <if condition="<findings/> contains a finding with a non-empty `recommendation`">
        <ase-tpl-hint level="normal">
        Use `/ase-code-edit` to apply a recommendation to the skills, prompts, or configuration involved.
        </ase-tpl-hint>
        </if>

    </step>

</flow>
