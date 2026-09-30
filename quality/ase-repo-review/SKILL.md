---
name: ase-repo-review
argument-hint: "[--help|-h] [--severity|-S=(LOW|MEDIUM|HIGH)]"
description: >
    Perform a holistic, human-reviewer-style critique of the currently
    staged Git changes and emit an approve/reject verdict with
    prioritized, severity-tagged, line-cited findings. Use when the user
    wants the staged diff "reviewed", "critiqued", or "code-reviewed"
    before committing.
user-invocable: true
disable-model-invocation: false
effort: high
allowed-tools:
    - "Bash(git diff *)"
    - "Agent"
---

@${CLAUDE_SKILL_DIR}/../../meta/ase-control.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-skill.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-getopt.md

<purpose name="ase-repo-review">
Review Staged Changes
</purpose>

<expand name="getopt"
    arg1="ase-repo-review"
    arg2="--severity|-S=(LOW|MEDIUM|HIGH)">
    $ARGUMENTS
</expand>

<objective>
Review the currently staged Git changes the way an *experienced human
reviewer* would - judging them *holistically* against the change's *own
intent* and against *correctness*, *design fit*, *clarity*, *robustness*,
and *project-convention conformance* - and emit a single *approve /
request-changes verdict* backed by *prioritized*, *severity-tagged*,
*line-cited* findings. This is a *synthesizing critique*, not a mechanical
scan: it complements `ase-code-lint` (mechanical quality), `ase-code-analyze`
(logic/semantics), and `ase-repo-diff` (intent narrative and risk).
</objective>

Procedure
---------

<flow>

1.  <step id="STEP 1: Determine Change Set">

    1.  Determine *whether there are staged changes at all* by running the
        corresponding command (taken exactly as given) and capturing its
        output - the bare *list of staged file names* - into <diff/>. This
        is a lightweight gate; the full diff is fetched by the sub-agent
        in STEP 2, so capturing only the file-name list here is sufficient:

        `git diff --cached --name-only HEAD`

    2.  <if condition="<diff/> is empty">
        Only output the following <template/> and then *STOP* immediately:

        <template>
        ⧉ **ASE**: ✪ skill: **ase-repo-review**, ▶ status: **no changes to review**
        </template>
        </if>

    </step>

2.  <step id="STEP 2: Review Investigation">

    <if condition="<ase-project-boxing/> is equal `black`">

    The project source artifacts are classified as a *black box*, so
    the user does *not* want the staged changes scrutinized or their
    findings surfaced. *Skip* the entire review investigation: do
    *not* invoke the `Agent` tool and do *not* read any change, set
    <findings/> to the *empty* list, set <verdict/> to `SKIPPED (boxing:
    black)`, set <summary/> to a *one-line* neutral restatement of the
    change intent derived solely from STEP 1, and proceed *directly* to
    STEP 3.

    </if>

    First, use the following <template/> to give a hint on this step:

    <template>
    <ase-tpl-bullet-secondary/> **REVIEW INVESTIGATION**
    </template>

    Dispatch the review investigation to a *sub-agent* via the `Agent`
    tool so that *no* investigation details leak into the user-visible
    transcript. The sub-agent performs the silent reading, the read-only
    repository probing, and the critique; only its final structured return
    value is consumed here.

    For this, invoke *exactly once* the tool:

    ```text
        Agent(
            description:       "Review Investigation",
            subagent_type:     "ase:ase-repo-review",
            prompt:            "Review the staged changes.",
            run_in_background: false
        )
    ```

    Parse the single result message of the `Agent` tool as a JSON object,
    set <summary/> to its `summary` field (a single crisp sentence
    reconstructing the change's intent), and set <findings/> to its
    `findings` field (a list).

    Then *derive* the overall <verdict/> from <findings/>: set
    <verdict/> to `REJECT - DEMANDS CHANGES` if *any* finding in
    <findings/> has a `severity` field of `HIGH`; otherwise set
    <verdict/> to `APPROVE`. The verdict is derived *before* the
    severity floor below, so the floor only affects which findings are
    *rendered*, never the verdict.

    Then determine the *effective severity floor* <floor/>: define the
    ordinal rank `LOW`=1, `MEDIUM`=2, `HIGH`=3, start from
    <floor><getopt-option-severity/></floor> (default `LOW`), and - if
    <ase-project-boxing/> is equal `grey` - raise <floor/> to `MEDIUM`
    whenever its current rank is below `rank(MEDIUM)` (grey boxing
    surfaces only *material* findings of severity `MEDIUM` and above).
    The floor affects only which findings are *rendered*, never the
    <verdict/> derived above.

    Then *apply the effective severity floor* <floor/>: *Keep* a finding
    in <findings/> if and only if its `severity` field is `ACCEPTED` *or*
    `rank(severity)` is greater than or equal to `rank(<floor/>)`;
    *silently drop* all other findings. With the default floor `LOW`, all
    findings are kept. `ACCEPTED` findings are *never* dropped.

    You *MUST* *NOT* output anything else in this STEP 2.

    </step>

3.  <step id="STEP 3: Verdict and Findings">

    1.  Use the following <template/> to output the overall review in
        <verdict/> and the reconstructed intent <summary/>:

        <template>

        <ase-tpl-bullet-signal/> **REVIEW VERDICT**: **<verdict/>**

        <ase-tpl-bullet-normal/> **CHANGE INTENT**: <summary/>

        </template>

        You *MUST* *NOT* output anything else in this STEP 3.1.

    2.  <if condition="<findings/> is empty">
        Only output the following <template/> - with <note/> set to `the
        change was not reviewed` if <verdict/> starts with `SKIPPED` and
        to `the change is clean` otherwise - and then *SKIP* the
        remainder of this STEP 3 (an empty finding list never yields the
        `REJECT` verdict, so the closing hint of substep 4 would expand
        into nothing anyway):

        <template>

        <ase-tpl-bullet-normal/> **NO FINDINGS**: <note/>, nothing to flag.

        </template>
        </if>

    3.  <if condition="<findings/> is NOT empty">
        Sort the findings by <severity/> from highest to lowest in the
        fixed order `HIGH`, `MEDIUM`, `LOW`, `ACCEPTED`. Within the same
        severity, keep the order returned by the sub-agent.

        Then render a *three-column table* with one row per finding by
        using the following output <template/>. For each finding, repeat
        the third line, set <severity/> to its `severity` field, set
        <dimension/> to its `dimension` field, set <location/> to its
        `location` field, and set <finding/> to its `finding` field.

        In the <location/> column, mark up the `file:line` reference
        as code (with backticks) and prepend it with `▢ ` - keep the
        sub-agent's own `:N` / `:N-M` line citation intact and do *not*
        append any further line-count decoration.

        Because the <finding/> text is free-form Markdown, *before*
        emitting any row you *MUST* escape every literal `|` pipe
        character inside <location/> and <finding/> as `\|` so it cannot
        break the table column structure.

        <template>
        | Severity        | Dimension    | Finding                 |
        | --------------- | ------------ | ----------------------- |
        | **<severity/>** | <dimension/> | <location/>: <finding/> |
        </template>

        Keep the overall report *concise* and *brief*.
        Do *not* output any further explanation.
        </if>

    4.  Finally, give the closing hint by expanding the following
        (which, depending on the configured <ase-guidance-level/>, may
        expand into nothing and hence emit no output at all):

        <if condition="<verdict/> starts with `REJECT`">
        <ase-tpl-hint level="normal">
        Use `/ase-code-resolve` to derive and apply a solution approach for the findings which demand changes.
        </ase-tpl-hint>
        </if>

    </step>

</flow>
