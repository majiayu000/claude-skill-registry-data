---
name: ase-spec-lint
argument-hint: "[--help|-h] [--auto|-a] [--severity|-S=(AUTO|LOW|MEDIUM|HIGH)] [--include|-i=<aspect>[,...]] [--exclude|-e=<aspect>[,...]] [--staged] [--unstaged] [<spec-reference>]"
description: >
    Lint the SpecBook-based specification (SPEC) for potential quality
    problems: its syntax, its formatting, its statements, the logical
    gaps of its model, and its completeness for an implementation.
    Use when the user wants to "lint" or "check" the "spec" or
    "specification".
user-invocable: true
disable-model-invocation: false
effort: high
allowed-tools:
    - "Bash(git rev-parse *)"
    - "Bash(git -C *)"
---

@${CLAUDE_SKILL_DIR}/../../meta/ase-control.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-skill.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-dialog.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-getopt.md

<purpose name="ase-spec-lint">
Lint Specification
</purpose>

<expand name="getopt"
    arg1="ase-spec-lint"
    arg2="--auto|-a --severity|-S=(AUTO|LOW|MEDIUM|HIGH) --include|-i=(none|S01|S02|S03|S04|S05|S06|S07|S08|S09|S10)... --exclude|-e=(none|S01|S02|S03|S04|S05|S06|S07|S08|S09|S10)... --staged --unstaged">
    $ARGUMENTS
</expand>

<objective>
*Analyze* the specification of `<getopt-arguments/>` for *potential
problems* related to a set of specification quality aspects.
</objective>

<flow>

1.  <step id="STEP 1: Investigation">

    <if condition="<ase-project-boxing/> is equal `black` and <getopt-option-severity/> is equal `AUTO`">

    The project source artifacts are classified as a *black box*, so
    the user does *not* want them inspected or their problems surfaced
    (an *explicitly* given severity floor lifts this skip).
    *Skip* the entire investigation and reporting: do *not* invoke any
    `Bash`, `Glob`, or `Agent` tool and do *not* read any source, only
    output the following <template/> and then *SKIP* the remaining steps
    STEP 2 and STEP 3:

    <template>
    <ase-tpl-bullet-normal/> **LINT**: *suppressed* (`project.boxing` is `black`)
    </template>

    </if>

    Set <condensed>true</condensed> if <ase-project-boxing/> is equal
    `grey` or `black` (the latter reached only under an explicitly given
    severity floor), and <condensed>false</condensed> otherwise: a
    *condensed* report suppresses the full unified diffs of STEP 3.

    First, determine the *effective aspect set* <aspects/>, i.e., the
    specification quality aspects which are checked at all. For this,
    parse <getopt-option-include/> and <getopt-option-exclude/> as
    comma-separated token lists, silently dropping the `none` sentinel
    and any empty token. If a token <token/> is *not* one of the aspect
    ids `S01`...`S10`, only output the following <template/> and then
    *STOP* the entire flow (do not perform any further steps):

    <template>
    ⧉ **ASE**: ✪ skill: **ase-spec-lint**, ▶ ERROR: invalid aspect id: **<token/>**
    </template>

    Otherwise set <aspects/> to *all* ten aspect ids `S01`...`S10` if
    both lists are empty, to the *include* list if only it is non-empty,
    to all ten *minus* the *exclude* list if only it is non-empty, and
    to the *include* list *minus* the *exclude* list if both are
    non-empty. If the resulting <aspects/> is *empty*, only output the
    following <template/> and then *STOP* the entire flow (do not
    perform any further steps):

    <template>
    ⧉ **ASE**: ✪ skill: **ase-spec-lint**, ▶ ERROR: options `--include` and `--exclude` cancel out to an empty aspect set
    </template>

    Then split <aspects/> into the *per-file* aspects <file-aspects/>
    (those of `S01`...`S06`) and the *model-wide* aspects
    <model-aspects/> (those of `S07`...`S10`), as the latter can be
    judged on the entire specification model only.

    Then, use the following <template/> to give a hint on this step:

    <template>
    <ase-tpl-bullet-secondary/> **LINT INVESTIGATION**
    </template>

    Dispatch the investigation to *sub-agents* via the `Agent`
    tool so that *no* investigation details leak into the user-visible
    transcript. The sub-agents perform the silent reading and checking;
    only their final structured return values are consumed here.

    For this, first *silently* resolve the `SPEC` artifacts by calling
    the `ase_artifact_list(kind: [ "spec" ])` tool of the `ase` MCP
    server *once* and set <corpus/> to the returned project-relative
    file list. If <corpus/> is empty, only output the following
    <template/> and then *STOP* the entire flow (do not perform any
    further steps):

    <template>
    ⧉ **ASE**: ✪ skill: **ase-spec-lint**, ▶ ERROR: no specification artifacts below `<ase-spec-basedir/>`
    </template>

    <if condition="<getopt-option-staged/> is equal `true` or <getopt-option-unstaged/> is equal `true`">

    Then *silently* restrict the linting to the *changed* files of the
    Git working copy. Set <changes>staged and unstaged</changes> if
    both <getopt-option-staged/> and <getopt-option-unstaged/> are equal
    `true`, set <changes>staged</changes> if only
    <getopt-option-staged/> is equal `true`, and set
    <changes>unstaged</changes> otherwise. Determine the *repository
    root* by running the command `git rev-parse --show-toplevel` (taken
    exactly as given) and capturing its output into <repo-root/>. Then
    determine the changed files by running the corresponding commands
    (taken exactly as given), each listing one path relative to
    <repo-root/> per line, and collect all listed paths, dropping
    duplicates:

    <if condition="<getopt-option-staged/> is equal `true`">
    `git -C "<repo-root/>" -c core.quotepath=off diff --cached --name-only --diff-filter=d`
    </if>

    <if condition="<getopt-option-unstaged/> is equal `true`">
    `git -C "<repo-root/>" -c core.quotepath=off diff --name-only --diff-filter=d`

    `git -C "<repo-root/>" -c core.quotepath=off ls-files --others --exclude-standard`
    </if>

    Keep only those listed paths which are contained in <corpus/>. If
    `<getopt-arguments/>` is not empty, keep only those files which lie
    within the specification referenced by it, expanding any directory
    or wildcard references with the `Glob` tool. Set <sources/> to the
    resulting list of individual specification files, preserving order.

    If <sources/> is empty, only output the following <template/>
    and then *SKIP* the rest of this STEP 1 and the remaining steps
    STEP 2 and STEP 3:

    <template>
    <ase-tpl-bullet-normal/> **LINT**: *no <changes/> specification files to lint*
    </template>

    </if>
    <elseif condition="`<getopt-arguments/>` is not empty">

    Then *silently* resolve `<getopt-arguments/>` to individual files,
    expanding any directory or wildcard references with the `Glob` tool,
    keep only those files which are contained in <corpus/>, and set
    <sources/> to the resulting list, preserving order.

    If <sources/> is empty (none of the *spec-reference* resolvable to a
    specification file), only output the following <template/> and then
    *STOP* the entire flow (do not perform any further steps):

    <template>
    ⧉ **ASE**: ✪ skill: **ase-spec-lint**, ▶ ERROR: no specification files to lint in: **<getopt-arguments/>**
    </template>

    </elseif>
    <else>

    Then set <sources/> to <corpus/>, i.e., lint the *entire*
    specification.

    </else>

    Then set <schema/> to the whitespace-separated entries of
    <ase-spec-schema/>, or to the single entry `std` if
    <ase-spec-schema/> is empty, where each entry `std` is replaced by
    the path of the bundled file `meta/ase-format-specbook.yaml`. Set
    <meta/> to the space-separated paths of the bundled files
    `meta/ase-format-specbook.md` and `meta/ase-tenets.md`. Form each
    bundled file path by joining <ase-plugin-root/> and the file name
    with exactly *one* `/` separator, as <ase-plugin-root/> may or may
    not carry a trailing `/`.

    <if condition="<aspects/> contains `S01`">
    Then call the `ase_specbook_lint(markdown: true)` tool of the `ase`
    MCP server *once*, which lints the *entire* specification against
    the schema via *SpecBook* and for its generic Markdown formatting
    via *markdownlint*, and set <diagnostics/> to those entries of its
    returned `diagnostics` array whose `file` is contained in
    <sources/>.
    </if>
    <else>
    Then set <diagnostics/> to empty.
    </else>

    Then dispatch the sub-agents by invoking the following tool once per
    *investigation*, emitting *all* invocations *in one single message*
    so they run in *parallel*:

    ```text
        Agent(
            description:       "Specification Lint Investigation (<index/>/<count/>)",
            subagent_type:     "ase:ase-spec-lint",
            prompt:            "ASPECTS: <investigation-aspects/>\nFILES: <investigation-files/>\nCORPUS: <corpus/>\nMETA: <meta/>\nSCHEMA: <schema/>\nDIAGNOSTICS:\n<investigation-diagnostics/>",
            run_in_background: false
        )
    ```

    The *investigations* are determined as follows:

    -   <if condition="<file-aspects/> is not empty">
        Partition <sources/>, preserving order, into at most *eight*
        batches of roughly equal size (a single file yields a single
        batch). Each batch is one *investigation* with
        <investigation-aspects/> set to <file-aspects/>,
        <investigation-files/> set to the files of the batch, and
        <investigation-diagnostics/> set to those entries of
        <diagnostics/> whose `file` is contained in the batch.
        </if>

    -   <if condition="<model-aspects/> is not empty">
        One additional *investigation* covers the entire model, with
        <investigation-aspects/> set to <model-aspects/>,
        <investigation-files/> set to *all* of <sources/>, and
        <investigation-diagnostics/> set to empty.
        </if>

    Here every aspect list is comma-separated (without any spaces),
    every file list is space-separated, <investigation-diagnostics/>
    carries one line `- <file/>:<line/>:<column/>: <severity/>:
    <message/>` per diagnostic (or the single line `(none)` if empty),
    <index/> is the 1-based index of the investigation, and <count/> is
    the total number of investigations, so that each parallel
    invocation is distinguishable in the progress display.

    Parse the result message of each `Agent` tool invocation as a JSON
    array and concatenate all those arrays. Determine the *anchor* of
    each problem as its `file` and `line` fields. Then *deduplicate* the
    combined list: when two problems share the same anchor and
    `aspect`, *silently drop* all but the first one (sub-agents may
    have read overlapping *related* files for comprehension). Finally
    sort the list by the anchor `file` and then numerically by the anchor
    `line`, and set <problems/> to that list.

    Then determine the *effective severity floor* <floor/>: define the
    ordinal rank `LOW`=1, `MEDIUM`=2, `HIGH`=3.

    <if condition="<getopt-option-severity/> is equal `AUTO`">
    Set <floor>MEDIUM</floor> if <ase-project-boxing/> is equal `grey`
    (grey boxing surfaces only *material* findings of severity `MEDIUM`
    and above), and <floor>LOW</floor> otherwise.
    </if>
    <else>
    Set <floor><getopt-option-severity/></floor>: an *explicitly* given
    severity floor always *wins* over the boxing, both over the `grey`
    floor and over the `black` skip.
    </else>

    Then *apply the effective severity floor* <floor/>: *Keep* a problem
    in <problems/> if and only if its `severity` field is `ACCEPTED` *or*
    `rank(severity)` is greater than or equal to `rank(<floor/>)`;
    *silently drop* all other problems. With the floor `LOW`, all
    problems are kept. `ACCEPTED` problems are *never* dropped.

    Finally, sort the surviving problems in <problems/> by their
    `severity` field from highest to lowest in the fixed order `HIGH`,
    `MEDIUM`, `LOW`, `ACCEPTED`, so the subsequent reporting starts with
    the most severe problem. Within the same severity, keep the
    `file`/`line` order established above.

    You *MUST* *NOT* output anything else in this STEP 1.

    </step>

2.  <step id="STEP 2: Summary">

    Use the following <template/> to output a summary of the detected
    problems in <problems/> (if any were found), in the original aspect
    ordering `S01 - XXX`...`S10 - XXX`.

    <template>
    <ase-tpl-bullet-secondary/> **LINT SUMMARY**:

    <ase-tpl-bullet-signal/> **SX - XXX**: N issues
    <ase-tpl-bullet-signal/> **SX - XXX**: N issues
    [...]
    </template>

    Else, if no problems were found, use the following <template/> to
    output the summary instead:

    <template>
    <ase-tpl-bullet-secondary/> **LINT SUMMARY**:

    *(no problems detected)*
    </template>

    You *MUST* *NOT* output anything else in this STEP 2.

    </step>

3.  <step id="STEP 3: Correction">

    1.  *Mark this skill as the active edit-capable skill* so that the
        ASE `pre-tool-use` hook auto-approves the subsequent `Edit`
        invocations on *any* invocation path (slash command *or* `Skill`
        tool). Call the `ase_state_set(key: "skill", val:
        "ase-spec-lint", session: "<ase-session-id/>")` tool
        from the `ase` MCP server. Then call the `ase_timestamp(format:
        "yyyy-LL-dd HH:mm")` tool of the `ase` MCP server *once* to find
        out the current time and store it in <timestamp-modified/>, and
        set <touched/> to empty (the list of files changed by an
        applied correction). Do not output anything in this substep.

        *Critical safety invariant*: the marker set here grants `Edit`
        auto-approval and *MUST* be cleared again (substep 4 below)
        *before* this skill yields control, *regardless* of how the
        iteration in substep 2 ends - whether it completes normally,
        is aborted early (e.g. an `Edit` failure, an unparseable value,
        or any other unexpected condition), or is otherwise interrupted.
        If you ever stop or bail out of substep 2 early, you *MUST*
        still perform substep 4 first. Never leave this marker active
        for a later, unrelated `Edit`.

    2.  Set <total/> to the number of problems in <problems/> and
        <index/> to `0`. Then iterate over all problems:

        <for items="<problems/>">

        1.  Increment <index/> by one (the 1-based position of the
            current <item/> within <problems/>).
            Set <aspect/>      to the `aspect`      field of <item/>.
            Set <severity/>    to the `severity`    field of <item/>.
            Set <description/> to the `description` field of <item/>.
            Set <anchor/>      to `` `<anchor-file/>`:<anchor-line/> ``, where
            <anchor-file/> is the `file` and <anchor-line/> the `line` field of <item/>.
            Set <change-set/>  to the `change-set`  field of <item/>.
            Set <gap/> to `true` if <aspect/> starts with `S09` or
            `S10` (a *gap-filling* best-guess correction), and to
            `false` otherwise.

        2.  Set <context></context> (set to empty).
            Set <diff></diff> (set to empty).
            Set <diff-condensed></diff-condensed> (set to empty).

        3.  Iterate over the change set:

            <for items="<change-set/>">

            1.  Set <file/>         to the `file`         field of <item/>.
                Set <change-hunks/> to the `change-hunks` field of <item/>.

                Unless <condensed/> is equal `true` (where the
                full unified diff is suppressed and no context lines are
                rendered at all), *silently* read the current content of
                <file/> with the `Read` tool - reusing the content read
                for the same <file/> earlier in this iteration, unless
                an `Edit` was applied to it in between - and set
                <file-lines/> to its lines, *stripped* of the
                line-number prefixes the tool adds. Set <file-lines/>
                to empty if the file cannot be read.

                This content is the *authoritative* source of the
                context lines of substep 2 below, so the rendered diff
                shows real context even when a sub-agent supplied none.

                Unless <condensed/> is equal `true` (where the
                full unified diff is suppressed and this per-file header is
                unused), set <diff-file/> to the following <template/>:

                <template>
                --- <file/> (original)
                +++ <file/> (corrected)
                </template>

            2.  Iterate over the change hunks.

                <for items="<change-hunks/>">

                1.  Set <line/>           to the `line`           field of <item/>.
                    Set <context-before/> to the `context_before` field of <item/>.
                    Set <old-text/>       to the `old_text`       field of <item/>.
                    Set <new-text/>       to the `new_text`       field of <item/>.
                    Set <context-after/>  to the `context_after`  field of <item/>.

                    Then *normalize* the hunk to its *minimal* form, so
                    that the proposed diff shows exactly the lines the
                    later `Edit` will actually change: while the *first*
                    line of <old-text/> is identical to the *first* line
                    of <new-text/>, *move* that line from both to the
                    end of <context-before/> and increment <line/> by
                    one; likewise, while the *last* line of <old-text/>
                    is identical to the *last* line of <new-text/>,
                    *move* that line from both to the front of
                    <context-after/>. Finally, *trim* <context-before/>
                    to its *last* two lines and <context-after/> to its
                    *first* two lines.

                    Then, whenever <file-lines/> is non-empty,
                    *re-derive* both context parts from it, *overriding*
                    the sub-agent supplied values: set <context-before/>
                    to the *up to two* lines of <file-lines/> directly
                    *before* line <line/> (empty if <line/> is `1`) and
                    <context-after/> to the *up to two* lines of
                    <file-lines/> starting at line (<line/> + <n/>),
                    where <n/> is the number of lines in <old-text/>
                    (empty if that line is beyond the end of the file).
                    Keep the sub-agent supplied values only when
                    <file-lines/> is empty.

                2.  *Skip* this substep entirely when <condensed/>
                    is equal `true` - the full unified diff is suppressed
                    there, so none of the <hunk-body/>, <old-count/>,
                    <new-count/>, <old-start/>, or <new-start/> values
                    below are consumed (substep 4 builds only the condensed
                    one-liner instead).

                    Otherwise, determine the hunk *body* as an ordered list
                    of lines, each carrying a one-character prefix (` ` for
                    context, `-` for old-side, `+` for new-side). Build it
                    by concatenating, in order and *skipping any part that
                    is empty*:

                    - one ` `-prefixed line for *each* line of
                      <context-before/> (if non-empty),
                    - one `-`-prefixed line for *each* line of <old-text/>
                      (if non-empty; split <old-text/> on newlines),
                    - one `+`-prefixed line for *each* line of <new-text/>
                      (if non-empty; split <new-text/> on newlines),
                    - one ` `-prefixed line for *each* line of
                      <context-after/> (if non-empty).

                    Set <hunk-body/> to those prefixed lines joined by
                    newlines.

                    Set <old-count/> to the number of old-side hunk lines,
                    i.e., the combined line count of <context-before/>,
                    <old-text/>, and <context-after/> (each empty part
                    counts as `0`).
                    Set <new-count/> to the number of new-side hunk lines,
                    i.e., the combined line count of <context-before/>,
                    <new-text/>, and <context-after/> (each empty part
                    counts as `0`).

                    Set <old-start/> to the 1-based line number of the
                    *first* old-side hunk line: if <context-before/> is
                    non-empty, that is the line of its *first* context
                    line, i.e. <line/> minus the number of lines in
                    <context-before/>; otherwise it is <line/> itself
                    (the first line of <old-text/>). For a hunk that
                    *only inserts* new lines (empty <old-text/> *and*
                    empty context), set it to the
                    line *before* which the insertion happens, clamped to a
                    minimum of `0`, so a top-of-file insertion yields
                    `@@ -0,0 ... @@`.
                    Set <new-start/> to the same value as <old-start/>, but
                    clamped to a minimum of `1` whenever <new-count/> is
                    greater than `0` (the corrected side then has a real
                    first line).

                3.  If <context/> is not empty, set
                    <context><context/>,</context> (append a comma).
                    Then append the following <template/> to <context/>:

                    <template>`<file/>`:<line/></template>

                4.  <if condition="<condensed/> is equal `true`">

                    The full unified diff is *suppressed* in a condensed
                    report (see substep 5 below), so *skip* the full-diff append
                    and instead build only a *condensed* one-line
                    representation of this hunk: determine <old-snippet/>
                    as the *single-line* collapse of <old-text/> (join its
                    lines with ` ⏎ `, or `∅` when <old-text/> is empty for
                    a pure insertion) and <new-snippet/> as the same
                    collapse of <new-text/> (or `∅` when empty for a pure
                    deletion). Then append the following <template/> to
                    <diff-condensed/> as a new line:

                    <template>
                    <ase-tpl-bullet-signal/> `<file/>`:<line/>: `<old-snippet/>` → `<new-snippet/>`
                    </template>

                    </if>
                    <else>

                    Append the following <template/> to <diff-file/>,
                    emitting <hunk-body/> verbatim (one already-prefixed
                    line per line, with no extra blank or space-only lines):

                    <template>
                    @@ -<old-start/>,<old-count/> +<new-start/>,<new-count/> @@
                    <hunk-body/>
                    </template>

                    </else>

                </for>

            3.  Unless <condensed/> is equal `true` (where
                <diff-file/> is unused), append <diff-file/> to <diff/>.

            </for>

            If <context/> is still empty (an empty <change-set/>), set
            <context><anchor/></context>.

        4.  Report the problem with the following <template/>:

            <template>
            <ase-tpl-bullet-signal/> [<index/>/<total/>]: **<aspect/> PROBLEM** (`<severity/>`): <context/>

            <description/>

            </template>

        5.  <if condition="<change-set/> is empty">

            No correction could be derived for this problem, so report
            it with the following <template/>, set <result>REJECT</result>,
            and *skip* the remaining substep 6:

            <template>
            <ase-tpl-bullet-normal/> **<aspect/> SOLUTION**:

            *(no correction derivable -- manual action required)*

            </template>

            </if>
            <elseif condition="<getopt-option-auto/> is not equal `true` or <gap/> is equal `true`">

            <if condition="<condensed/> is equal `true`">

            The project source artifacts are classified as a *grey box* (or
            *black box*), so the user does *not* want the full artifact
            internals surfaced:
            *suppress* the full unified diff and instead show only the
            *condensed* one-line-per-hunk representation. Report the
            solution with the following <template/>:

            <template>
            <ase-tpl-bullet-normal/> **<aspect/> SOLUTION**:

            <diff-condensed/>

            </template>

            </if>
            <else>

            Report the solution with the following <template/>:

            <template>
            <ase-tpl-bullet-normal/> **<aspect/> SOLUTION**:

            ```diff
            <diff/>
            ```

            </template>

            </else>

            </elseif>
            <else>

            Report the solution with the following <template/>:

            <template>
            <ase-tpl-bullet-normal/> **<aspect/> SOLUTION**:

            *(corresponding change automatically applied)*

            </template>

            </else>

        6.  <if condition="<getopt-option-auto/> is equal `true` and <gap/> is equal `true`">

            A *gap-filling* correction carries *best-guess* content,
            which is *never* applied unattended. Report this with the
            following <template/> and set <result>REJECT</result>:

            <template>
            *(best-guess correction not applied under `--auto` -- re-run without `--auto` to review it)*

            </template>

            </if>
            <elseif condition="<getopt-option-auto/> is not equal `true`">

            In the following, you *MUST* *NOT* use your built-in
            <user-dialog-tool/> tool! Instead, you *MUST* just show a
            custom dialog according to the expanded `custom-dialog`
            definition. You *MUST* closely follow this definition:

            <expand name="custom-dialog" arg1="--other">
                CORRECTION: How would you like to proceed with this proposed correction?
                ACCEPT: Apply this proposed correction.
                REJECT: Skip this proposed correction.
            </expand>

            </elseif>
            <else>

            Set <result>ACCEPT</result>.
            You *MUST* *NOT* output anything else in this sub-step 6.

            </else>

        7.  Check <result/> and dispatch accordingly:

            -   <if condition="<result/> is 'ACCEPT'">
                Invoke the `Edit` tool to apply the changes exactly
                as given by the hunks of the current <change-set/>
                (rendered as <diff/>, unless suppressed in a condensed
                report). The operation will be auto-approved by the ASE
                `pre-tool-use` hook (which tracks the active skill),
                so *no* interactive permission prompt will appear.
                After applying the changes, add every `file` of
                <change-set/> to <touched/> (dropping duplicates) and
                just continue with the next <item/>.
                </if>

            -   <if condition="<result/> starts with 'OTHER'">
                Generate a *new* proposal for the *same* <item/>
                (incorporating the user's free-text hint from <result/> if
                provided via the "OTHER" prefix). *Reassign* <description/>
                and <change-set/> to reflect this refined proposal (each
                change-hunk's `old_text` stays anchored to the existing
                text at its `file`:`line`; `new_text` carries the
                refinement), keeping the conformance to the **SpecBook**
                format contract and the schema, so that the substep 2/3
                rebuild renders the new <diff/> and any `Edit` applies the
                new proposal rather than the original. Then loop back to
                substep 2 of this iteration. There is *no* cap on
                refinement rounds - keep refining until the user picks
                `ACCEPT` or `REJECT`.
                </if>

            -   <if condition="
                    <result/> is 'REJECT' or
                    <result/> is 'CANCEL' or
                    <result/> starts with 'ERROR'
                ">
                Skip this <item/> without any `Edit` call and continue
                with the next <item/>.
                </if>

        </for>

    3.  For every file in <touched/> which carries a `Modified:
        <timestamp-modified-old/>` frontmatter line, invoke the `Edit`
        tool to replace <timestamp-modified-old/> with
        <timestamp-modified/>, keeping the spacing behind `Modified:`
        unchanged. Do not output anything in this substep.

    4.  *Clear the active edit-capable skill marker* now that all `Edit`
        invocations are done, so a later unrelated `Edit` is *not*
        auto-approved. Call the `ase_state_delete(key: "skill",
        session: "<ase-session-id/>")` tool from the `ase` MCP
        server. Do not output anything in this substep.

    5.  You *MUST* *NOT* output any further additional explanations or
        summaries at the end of this skill processing, except for the
        following final <template/>:

        <template>
        <ase-tpl-bullet-secondary/> **LINT FINISHED**
        </template>

    6.  Finally, give the closing hints by expanding the following
        (which, depending on the configured <ase-guidance-level/>, may
        each expand into nothing and hence emit no output at all):

        <if condition="at least one problem in <problems/> was left uncorrected">
        <ase-tpl-hint level="normal">
        For problems whose correction demands more than a local edit, use `/ase-spec-edit -g` to resolve them through a grilled one-shot specification edit.
        </ase-tpl-hint>
        </if>

        <if condition="<getopt-option-auto/> is not equal `true`">
        <ase-tpl-hint level="verbose">
        Use `/ase-spec-lint --auto` to apply all non-gap corrections unattended, `--severity` to raise the reporting floor, `--include`/`--exclude` to narrow the checked aspects, and `--staged`/`--unstaged` to lint only the changed specification files.
        </ase-tpl-hint>
        </if>

    </step>

</flow>

