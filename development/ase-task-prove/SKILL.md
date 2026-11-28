---
name: ase-task-prove
argument-hint: "[--help|-h] [--next|-n <option>[,...]] [--worktree|-w <name>] [--source|-s <source>] [--changeset|-c <changeset>] [--draft|-d] [<id>]"
description: >
    Prove the implementation of current or given task plan by executing
    the witness of each verification claim and empirically falsifying
    it, then emit a PROVEN / NOT PROVEN verdict. Use when the user wants
    the implementation "proven", the tests "verified", the evidence
    "delivered", or asks whether the change is "really correct".
user-invocable: true
disable-model-invocation: false
effort: xhigh
---

@${CLAUDE_SKILL_DIR}/../../meta/ase-control.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-skill.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-dialog.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-getopt.md

<purpose name="ase-task-prove">
Prove a Task Plan Implementation
</purpose>

<expand name="getopt"
    arg1="ase-task-prove"
    arg2="--next|-n=(none|DONE|EDIT|RESOLVE)... --worktree|-w= --source|-s= --changeset|-c= --draft|-d --int-reuse-task"
    arg3="colon-or-bare">
    $ARGUMENTS
</expand>

<objective>
*Prove* the implementation of a task plan: execute the witness of each
verification claim, *empirically falsify* it, and emit a `PROVEN` /
`NOT PROVEN` verdict backed by captured transcripts.
</objective>

@${CLAUDE_SKILL_DIR}/../../meta/ase-format-task.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-common-task.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-common-changeset.md

<define name="prove-temp-remove">
If <temp-dir/> is not empty, remove the temporary worktree by running
the commands `git worktree remove --force "<temp-dir/>"` and
`git worktree prune` (taken exactly as given), ignoring any failure,
and set <temp-dir></temp-dir> (empty). Do not output anything.
</define>

Rules
-----

A passing test shows only that the code did not contradict the test. A
*proof* additionally shows that the test *would have noticed* had the
code failed the claim. You *MUST* honor the following rules:

-   **Observe, never repair**: do *not* fix the implementation, rewrite
    or weaken a test, or relax an expected value. The *only* files you may
    modify are those a falsifier modifies and restores, the recovery files below
    `.ase/proof/` of <proof-dir/>, the temporary proof worktree, the dependency
    and build outputs a preparation or witness produces, and the task plan via
    `ase_task_save(...)`.

-   **Prove the change set**: run *every* witness and falsifier with the
    proof directory <proof-dir/> as its working directory, and resolve
    *every* file path relative to it, as only there the change set of
    the plan exists.

-   **Evidence over assertion**: every status traces to a command you
    actually ran, with its exit code and decisive output captured
    *verbatim*. Never paraphrase, reconstruct, or invent a transcript. A
    command you did not run yields `BLOCKED`.

-   **One falsifier at a time**: apply exactly one falsifier, run only
    its witness, restore, verify the restoration, and only then proceed.

-   **Targeted signal**: a falsified run counts only if the witness
    fails *for the reason the claim predicts*. A compile error or an
    unrelated cascade proves only that the falsifier was too coarse.

-   **Honest verdict**: `PROVEN` or `NOT PROVEN`, nothing in between. A
    `NOT PROVEN` verdict is a *successful* run of this skill; never
    soften it in prose.

Procedure
---------

1.  **Determine Task and Obligations:**

    1.  Set <instruction><getopt-arguments/></instruction> initially, with any
        leading and trailing whitespace stripped, and set <temp-dir></temp-dir>
        (empty).
        Inherit the always existing <ase-task-id/> from the current context.
        Inherit the always existing <ase-session-id/> from the current context.
        Do not output anything.

    2.  React on task id:

        <expand name="task-react-id" arg1="ase-task-prove"></expand>

    3.  Determine the current task plan content:

        <expand name="task-load-content"></expand>

    4.  If the <task-content/> is still empty, complain and tell the user to
        use the `ase-task-edit` skill first to create a task plan. Then
        immediately stop processing this skill.

    5.  Set <obligations/> to all `REG` and `CON` bullet-points of the
        `VERIFICATION (WHEN)` section, skipping the *inert* ones in
        state `[-]` or `[>]`. Give each one the <obligation-id/> of its
        bullet type plus its 1-based position among *all* bullet-points
        of that type, the inert ones included (e.g. `REG1`, `CON2`), so
        the id matches the plan, and set its <claim/> to its <text/>.
        Set <kind/> to the `Kind:` frontmatter key, or, if it is absent,
        to the kind inferred from the plan content, falling back to
        `CRAFTING`. Do not output anything.

    6.  <if condition="<obligations/> is empty">
        Deriving claims *now*, with the implementation in front of you,
        would only describe the code. Only output the following
        <template/>, directly followed by the hint, and then immediately
        *STOP* processing this skill:

        <template>
        ⧉ **ASE**: ☻ skill: **ase-task-prove**, ▶ ERROR: plan **<ase-task-id/>** has no active (non-inert) `REG` or `CON` verification claims
        </template>

        <ase-tpl-hint level="minimal">
        Use `/ase-task-grill --focus VERIFICATION` to fix the verification claims -- ideally *before* implementing.
        </ase-tpl-hint>
        </if>

    7.  Determine the *proof directory* <proof-dir/>, in which the change
        set of the plan exists, and which the `Changeset` key of the plan
        refers to:

        1.  If <getopt-option-draft/> is `true` and
            <getopt-option-changeset/> is not empty, only output the
            following <template/> and then immediately *STOP* processing
            the entire current skill:

            <template>
            ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ▶ ERROR: options `--draft` and `--changeset` are mutually exclusive
            </template>

            Otherwise, if <getopt-option-draft/> is `true`, set
            <getopt-option-changeset>attachment:draft</getopt-option-changeset>.

        2.  Set <task-changeset/> to <getopt-option-changeset/> if it is
            not empty, otherwise to the value of the `Changeset:`
            frontmatter key of <task-content/>, or to the configured
            default <ase-project-task-default-changeset/> if the key is
            absent, and parse it:

            <expand name="changeset-value"
                arg1="Changeset"
                arg2="<task-changeset/>"
                arg3="`worktree`, `branch`, `attachment`"
                arg4="◉ task: **<ase-task-id/>**"></expand>

            Set <changeset-type><value-type/></changeset-type> and
            <changeset-name><value-name/></changeset-name>.

        3.  <if condition="<getopt-option-worktree/> is not empty and <changeset-type/> is not `worktree`">
            Only output the following <template/> and then immediately
            *STOP* processing the entire current skill:

            <template>
            ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ▶ ERROR: option `--worktree` requires a `worktree` changeset (got **<task-changeset/>**)
            </template>
            </if>

            <if condition="<getopt-option-source/> is not empty and <changeset-type/> is not `branch`">
            Only output the following <template/> and then immediately
            *STOP* processing the entire current skill:

            <template>
            ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ▶ ERROR: option `--source` requires a `branch` changeset (got **<task-changeset/>**)
            </template>
            </if>

            Otherwise, prepare the context worktree, which a proof never
            creates:

            <expand name="changeset-context"
                arg1="<getopt-option-worktree/>"
                arg2="◉ task: **<ase-task-id/>**"
                arg3="false"
                arg4="false"></expand>

        4.  Determine <proof-dir/> according to <changeset-type/>:

            -   `worktree`: The change set is *uncommitted* in the context
                worktree: set <proof-dir><context-dir/></proof-dir> and
                <fix-diff/> to the output of the command
                `git -C "<proof-dir/>" diff HEAD` plus the untracked files
                of `git -C "<proof-dir/>" ls-files --others --exclude-standard`.

                <if condition="<getopt-option-worktree/> is empty">
                The falsifiers will temporarily break files of the
                *origin working copy*, which parallel sessions may share.
                Only output the following <template/>, directly followed
                by the hint, and then *continue* processing:

                <template>
                ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ▶ WARNING: falsifiers modify the **shared working copy** in place during the proof
                </template>

                <ase-tpl-hint level="minimal">
                Avoid parallel sessions in this working copy during the proof, or implement and prove in an own worktree via `--worktree <name>`.
                </ase-tpl-hint>
                </if>

            -   `branch`: The change set is *committed* onto the branch
                <changeset-name/>. If the command
                `git rev-parse --verify --quiet "refs/heads/<changeset-name/>"`
                fails, only output the following <template/> and then
                immediately *STOP* processing the entire current skill:

                <template>
                ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ▶ ERROR: changeset branch **<changeset-name/>** does not exist
                </template>

                Otherwise, set <task-source/> to <getopt-option-source/>
                if it is not empty, otherwise to the value of the
                `Source:` frontmatter key of <task-content/>, or to the
                configured default <ase-project-task-default-source/> if
                the key is absent, and parse it:

                <expand name="changeset-value"
                    arg1="Source"
                    arg2="<task-source/>"
                    arg3="`worktree`, `branch`"
                    arg4="◉ task: **<ase-task-id/>**"></expand>

                Set <source-ref/> to `refs/heads/<value-name/>` if
                <value-type/> is `branch`, resp. to `HEAD` otherwise. Set
                <temp-base>refs/heads/<changeset-name/></temp-base>, set
                <fork/> to the output of the command
                `git merge-base "<source-ref/>" "refs/heads/<changeset-name/>"`,
                and set <fix-diff/> to the output of the command
                `git diff "<fork/>..refs/heads/<changeset-name/>"`. If the
                `git merge-base` command fails (e.g., a missing source
                branch or no common ancestor), only output the following
                <template/> and then immediately *STOP* processing the
                entire current skill:

                <template>
                ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ▶ ERROR: no fork point of changeset branch **<changeset-name/>** from source **<task-source/>**
                </template>

            -   `attachment`: The change set is a unified diff in the
                attachment block of `Type` key value
                `text/x-diff; charset=utf-8; kind="<changeset-name/>"`. If
                no such block exists, only output the following
                <template/>, directly followed by the hint, and then
                immediately *STOP* processing the entire current skill:

                <template>
                ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ▶ ERROR: no change set attachment **<changeset-name/>** exists
                </template>

                <ase-tpl-hint level="minimal">
                Run `/ase-task-implement --changeset <task-changeset/>` first to create the change set attachment.
                </ase-tpl-hint>

                If it is *stale* according to the plan format, only
                output the following <template/>, directly followed by
                the hint, and then immediately *STOP* processing the
                entire current skill:

                <template>
                ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ▶ ERROR: change set attachment **<changeset-name/>** is **stale** (older than the plan)
                </template>

                <ase-tpl-hint level="minimal">
                Run `/ase-task-implement --changeset <task-changeset/>` again or remove the attachment.
                </ase-tpl-hint>

                Otherwise, set <temp-base/> to the commit of the
                `base <commit/>` value of its `Desc:` key, or to `HEAD`
                if it is absent or the command
                `git rev-parse --verify --quiet "<temp-base/>^{commit}"`
                fails, and set <fix-diff/> to its `Data` payload, fetched
                *verbatim* via the `ase_task_attachment(id:
                "<ase-task-id/>", type: "text/x-diff; charset=utf-8;
                kind=\"<changeset-name/>\"")` tool of the `ase` MCP server.

        5.  <if condition="<changeset-type/> is `branch` or `attachment`">
            Materialize the change set in a *temporary*, *detached*
            worktree, so the falsifiers never touch any other working
            copy: set <temp-name/> to <changeset-name/> with every
            character other than `A-Z`, `a-z`, `0-9`, `_`, and `-`
            replaced by `-`, then every run of multiple `-` reduced to a
            single `-` (e.g., `feature-x` for `feature/x`), as a branch
            name may contain `/` and `.`. Set <temp-id/> to
            <ase-task-id/> with all characters other than `A-Z`, `a-z`,
            `0-9`, `_`, and `-` stripped, followed by
            `-<temp-name/>-prove-<temp-hash/>`, where
            <temp-hash/> is the first 8 characters of the output of the
            `ase_mint(type: "sha1", hint:
            "<ase-task-id/>:<changeset-name/>:prove")` tool of the `ase`
            MCP server. Determine <temp-dir/> by calling the
            `ase_worktree_path(id: "<temp-id/>", temp: true, create: true)`
            tool of the `ase` MCP server -- you *MUST* *NEVER* assemble
            this path yourself. If <temp-dir/> exists and is a *registered*
            worktree according to `git worktree list --porcelain` whose
            record carries a `detached` line, it is a leftover of an
            earlier run, so remove it by expanding the
            following and then determine <temp-dir/> once again:

            <expand name="prove-temp-remove"></expand>

            If <temp-dir/> then still exists, set
            <temp-dir></temp-dir> (empty) to protect it from any removal,
            only output the following <template/>, and then immediately
            *STOP* processing the entire current skill:

            <template>
            ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ▶ ERROR: directory **<temp-id/>** exists, but is no temporary worktree
            </template>

            Otherwise, run the command
            `git worktree add --detach "<temp-dir/>" "<temp-base/>"`
            (taken exactly as given), and for `attachment` apply
            <fix-diff/> inside it via `git -C "<temp-dir/>" apply --3way`,
            leaving it *uncommitted*. If any of this fails, expand the
            following:

            <expand name="prove-temp-remove"></expand>

            Then only output the following <template/> and then
            immediately *STOP* processing the entire current skill:

            <template>
            ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ▶ ERROR: change set **<task-changeset/>** failed to materialize
            </template>

            Otherwise, set <proof-dir><temp-dir/></proof-dir>.
            </if>

            Do not output anything, except for the templates above.

2.  **Determine Witnesses and Falsifiers:**

    1.  Determine how tests are run in this project -- a command
        documented in the AI guidance files (`AGENTS.md`, `CLAUDE.md`,
        etc.) wins over one inferred from the build manifest -- and how
        a *single* test case is selected. A temporary proof worktree
        carries only the tracked files, so first prepare it like a fresh
        clone (e.g. install the dependencies and build, as documented).
        If no way to run tests exists,
        every obligation requiring a *test case* witness gets
        <status>BLOCKED</status> with the finding `no test runner
        determined`, while *command* and *spec* witnesses are still run.

    2.  For every obligation, determine its <witness/>: either the test
        case deciding its <claim/> (cited as `<file/>::<case/>`) plus
        the command running only that case, with the file and case
        selector passed *only* as single-quoted shell arguments (every
        `'` inside written as `'\''`), or -- for a claim that a
        project procedure like build, lint, or the whole suite succeeds
        -- that command itself. An obligation without a witness gets
        <status>BLOCKED</status> with the test case the implementation
        must add as its <finding/>. Obligations sharing the *same*
        command witness share its runs, so it is run only once.

        For <kind/> `SPECIFYING`, a claim about the *content* of the
        specification gets a *spec witness* instead of a test case: the command
        `ase spec query <selector/>` with an *ASTq* selector matching the
        specification node the claim is about, which *passes* only if its output
        carries the claimed statement or value (checked by an exact match in the
        command line, as the query alone succeeds even without any match). Pass
        the claimed statement and the selector *only* as single-quoted shell
        arguments, with every `'` inside written as `'\''`, so plan content can
        never break or inject into the command. A claim that the specification
        lints clean keeps the *command* witness `ase spec lint`.

    3.  For every obligation with a *test case* or *spec* witness,
        determine its <falsifier/> *automatically* from <kind/>, as a
        *precise*, executable edit and never as prose:

        -   `SPECIFYING`: `MUTATE` -- replace the verbatim
            `<old-text/>` at `<file/>:<line/>` of the *specification*
            artifact (never of production code) by a `<new-text/>`
            dropping or contradicting the specified statement or value
            the claim is about, so the spec witness has to notice it.
            The specification has to stay *syntactically* valid, so
            the witness fails on the claim, not on a parse error.
        -   `RESOLVING`: `REVERT` -- reverse-apply inside <proof-dir/>
            the fix hunks of <fix-diff/> in the production files which
            implement *this* plan (never of the witness, and never
            unrelated hunks). The fixed API still exists, so the witness
            fails on the reproduced defect. Without such fix hunks, fall
            back to `MUTATE`.
        -   otherwise (`CRAFTING`, `REFACTORING`): `MUTATE` -- replace
            the verbatim `<old-text/>` at `<file/>:<line/>` of the
            production code by a
            `<new-text/>` negating *the claim* (flip the comparison,
            boundary, sign, branch, or value the claim is about).
        -   only where neither applies: `PERTURB` -- substitute the
            input of the witness by one contradicting the claim.

        An obligation with a *command* witness gets the falsifier `n/a`:
        falsifying a build or linter proves nothing about the change.
        Set <falsifier-kind/> of every obligation to the kind of its
        falsifier (`REVERT`, `MUTATE`, `PERTURB`, or `n/a`).

3.  **Discharge Obligations:**

    First, output the following <template/>:

    <template>
    ⧉ **ASE**: **PROOF EXECUTION**
    </template>

    The recovery directory <proof-rec/> is `.ase/proof/<proof-key/>/`
    below <proof-dir/>, where <proof-key/> is <ase-task-id/> with all
    characters other than `A-Z`, `a-z`, `0-9`, `_`, and `-` stripped,
    so proofs of different tasks never share it. If
    `<proof-rec/>journal.json` already exists -- checked even if no
    falsifier is run -- it is the leftover of an interrupted proof,
    whose falsified files must neither become the new baseline nor be
    proven, so expand the following:

    <expand name="prove-temp-remove"></expand>

    Then only output the following <template/> and then immediately
    *STOP* processing the entire current skill:

    <template>
    ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ▶ ERROR: leftover proof journal **<proof-rec/>journal.json** -- recover and remove it first
    </template>

    <if condition="any obligation has a falsifier other than `n/a`">
    Capture a *restore anchor* before the first falsifier:
    verbatim copies of every file of <proof-dir/> a falsifier will touch
    below `<proof-rec/>baseline/`, each with an appended `.baseline`
    suffix so test runners and linters never pick them up as sources
    (as `git stash create` misses untracked files), plus their
    `git hash-object` resp. content hashes,
    and additionally the output of `git -C "<proof-dir/>" stash create`
    (a dangling commit of the tracked uncommitted state, or `HEAD` if
    its output is empty for a clean tree). Write <proof-dir/>, the
    anchor, and the file list to `<proof-rec/>journal.json`, so a manual
    recovery stays possible after an interruption.
    </if>

    Then process the obligations *strictly one at a time*, in order,
    performing only step 4 for those already `BLOCKED`:

    1.  **Positive run:** run the witness command twice (a *command*
        witness with the falsifier `n/a` only once, as no falsification
        depends on its stability), capturing
        each time its exit code, its decisive output line, and a
        verbatim <transcript/> (command line, head and tail of the
        output with `[...]` elided, and `exit=<code/>`). Set <positive/>
        to `exit=<code/>, <decisive-line/>` of the first run.

        -   If both runs differ in their exit code or pass/fail verdict
            (ignoring volatile output like timings), set
            <status>BLOCKED</status> with the instability and its
            suspected source as <finding/>.
        -   Else if the run failed for an *environmental* reason (like a
            missing dependency or build output), set
            <status>BLOCKED</status> with this reason as <finding/>.
        -   Else if the run failed, set <status>FAILED</status> with
            what the implementation does instead as <finding/>.
        -   Else if the falsifier is `n/a`, set <status>PROVEN</status>
            and <falsified>n/a</falsified>.

        Once a status is set, continue directly with step 4.

    2.  **Falsified run:** apply the falsifier. If it cannot be applied
        (e.g., the verbatim `<old-text/>` is not found, or the
        reverse-apply of the fix hunks is rejected), restore as below,
        set <status>BLOCKED</status> with the finding `falsifier not
        applicable: <reason/>`, as an unchallenged witness proves
        nothing, and continue directly with step 4. Otherwise, run the
        *same* witness command, capture it like above into <falsified/>
        and <transcript/>, and *always* restore afterwards -- even when
        the run errored -- from the copies of the restore anchor below
        `<proof-rec/>baseline/`.
        If the witness rebuilt artifacts from the falsified sources
        (like a `dst/` directory), re-run that build after the
        restoration, so no later run and no working copy keeps them.
        Verify the restoration against the recorded hashes resp.
        copies. If it does not match, set
        <baseline>DIRTY: <files/></baseline>, set <status>BLOCKED</status>
        with the finding `not run: working tree not restored` for the
        current and every remaining obligation without a status, output
        the step 4 <template/> for each of them, so the progress matches
        the ledger, then output the following <template/> (only if
        <temp-dir/> is empty, as a temporary proof worktree is removed
        anyway), skip the remaining obligations, and continue directly
        with the *Finally* paragraph below:

        <template>
        ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ▶ ERROR: working tree *NOT* restored: **<files/>** -- recover via `<proof-rec/>journal.json`
        </template>

    3.  **Judge:** if the witness failed for the reason the claim
        predicts, set <status>PROVEN</status>. If it *passed*, set
        <status>VACUOUS</status> with the precise insensitivity as
        <finding/> -- which assertion is missing, too weak, or watching
        the wrong value. If it failed for another reason, set
        <status>BLOCKED</status> with the narrower falsifier which
        would isolate the claim as <finding/>.

    4.  Output the following <template/>:

        <template>
        ○   **<obligation-id/>**: <status/>
        </template>

    Finally, set <baseline>restored</baseline> unless it was set to
    `DIRTY` above. If it is `restored`, remove the recovery directory
    <proof-rec/>, as it is no longer needed. In any case, remove the
    temporary proof worktree, as it only materialized the change set:

    <expand name="prove-temp-remove"></expand>

4.  **Report and Persist Ledger:**

    1.  Count <proven/>, <vacuous/>, <failed/>, and <blocked/>, and set
        <total/> to the number of obligations. Set
        <verdict>PROVEN</verdict> *if and only if* <proven/> equals
        <total/> and <baseline/> is `restored`, else set
        <verdict>NOT PROVEN</verdict>. Apply no other rule.

    2.  Render the <ledger/> with the following <template/>, with one
        table row per obligation and one evidence entry per obligation
        which is *not* `PROVEN` (for every obligation, if
        <ase-project-boxing/> is `white`), and output it framed by
        `<ase-tpl-head title="PROOF LEDGER"/>` and
        `<ase-tpl-foot title="PROOF LEDGER"/>`. If
        <ase-project-boxing/> is `black`, output only the verdict line.
        Render a <positive/>, <falsified/>, <falsifier-kind/>, or
        <witness/> never set (e.g. for an obligation `BLOCKED` before any
        run or without a witness, or settled in its positive run) as
        `-`, and omit the transcript code block of an obligation
        without any run. Escape every `|` inside a table cell as `\|`,
        so it cannot break the table. Replace every secret-like value in
        a <transcript/> (a token, password, key, or credential in a URL)
        by `[REDACTED]`, as the ledger is persisted into the plan and
        possibly into an issue tracker. If
        a <transcript/> contains a run of 3 or more backticks, lengthen
        its fence beyond the longest such run, so it cannot break.

        <template>
        ⚖ **VERDICT**: **<verdict/>** -- <proven/>/<total/> proven, <vacuous/> vacuous, <failed/> failed, <blocked/> blocked, changeset <task-changeset/>, baseline <baseline/>

        | ID | FALSIFIER | POSITIVE | FALSIFIED | STATUS |
        | -- | --------- | -------- | --------- | ------ |
        | <obligation-id/> | <falsifier-kind/> | <positive/> | <falsified/> | <status/> |

        -   **<obligation-id/>** ⟨<status/>⟩: <witness/>: <finding/>

            ```text
            <transcript/>
            ```

        </template>

    3.  Determine <timestamp-modified/> by calling the
        `ase_timestamp(format: "yyyy-LL-dd HH:mm")` tool of the `ase`
        MCP server and using the `text` field of its response. It stamps
        the attachment below *only*; the `Modified:` frontmatter key
        stays *untouched*.

    4.  Append <ledger/> as an attachment block to the "backmatter" of
        <task-content/> with the following <template/>, where <payload/>
        is <ledger/> with *every* line indented by *exactly* 4 spaces. If
        an attachment block of type `text/markdown; charset=utf-8;
        kind="proof"` exists, *replace* it in place and keep its
        `Created` value as <timestamp-attachment-created/>, else use
        <timestamp-modified/>:

        <template>
        ---
        Type:      text/markdown; charset=utf-8; kind="proof"
        Desc:      Proof Ledger
        Created:   <timestamp-attachment-created/>
        Modified:  <timestamp-modified/>
        Data:      |4+
        <payload/>
        </template>

    5.  Call the `ase_task_save(id: "<ase-task-id/>", text:
        "<task-content/>", tag: true)` tool of the `ase` MCP server to
        save the plan -- if <task-tag/> is not empty, additionally with
        the argument `base: "<task-tag/>"`, so a change of the plan made
        meanwhile by anybody else is merged instead of silently
        overwritten. If the save is refused because the plan was
        *changed* meanwhile, reload <task-content/> and <task-tag/> as in
        step 1.3, re-apply sub-step 4, and save again, at most *three*
        times in total, so the outcome of a long proof is not lost. On
        any other refusal, output the error message and stop the skill.
        This is the *only* permitted way to persist
        it -- *NEVER* write the plan file via `Write`/`Edit` or a shell
        command. Do not output anything related to this call except the
        following <template/>:

        <template>
        ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ⚖ verdict: **<verdict/>**, ▶ status: **proof ledger persisted**
        </template>

5.  **Decide Next Step:**

    1.  *Determine next step*:

        <expand name="task-next-select"
            arg1="ase-task-prove"
            arg2="DONE|EDIT|RESOLVE">
            Next Step: How would you like to proceed with the proof result?
            DONE: Stop processing.
            EDIT: Hand processing off to editing the plan.
            RESOLVE: Hand processing off to resolving the strongest finding.
        </expand>

    2.  Check the tool <result/> and dispatch accordingly:

        -   If <result/> is `DONE` or `CANCEL`, or if <result/> is
            `RESOLVE` while <verdict/> is `PROVEN`:
            Only output the following <template/> and then *STOP*.

            <template>
            ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ⚖ verdict: **<verdict/>**, ▶ status: **proof completed -- done**
            </template>

        -   If <result/> is `EDIT`:
            <expand name="task-next-handoff" arg1="ase-task-edit"
                arg2="proof completed -- hand-off to edit"></expand>

        -   If <result/> is `RESOLVE` while <changeset-type/> is `branch`
            or `attachment`, or <baseline/> starts with `DIRTY`:
            A resolution cannot safely edit the proven change set here --
            for `branch` and `attachment` it was proven only in the removed
            temporary worktree, and with a `DIRTY` baseline its files still
            carry a falsifier -- so it has to go through the plan:
            <expand name="task-next-handoff" arg1="ase-task-edit"
                arg2="proof completed -- hand-off to edit"></expand>

        -   If <result/> is `RESOLVE`:
            Set <problem/> to the *strongest* finding, in this order: the
            first `FAILED` obligation, else the first `VACUOUS` one, else
            the first `BLOCKED` one, phrased as the concrete defect plus
            its cited location, with every `"` replaced by `'`, enclosed
            in double quotes, so the option parser of `ase-code-edit`
            takes it as a single argument and never as an option. Set
            <resolve-args>--mode resolve</resolve-args>,
            and append ` --worktree <getopt-option-worktree/>` if
            <getopt-option-worktree/> is not empty, so the fix lands in
            the proven change set. As `ase-code-edit` has no `--next`
            option, the remaining tokens of <getopt-option-next/> cannot
            be forwarded: if it is not `none`, first output the following
            <template/>:

            <template>
            ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ▶ WARNING: remaining `--next` tokens **<getopt-option-next/>** ignored by `ase-code-edit`
            </template>

            Only output the following <template/> and then call the tool
            `Skill(skill: "ase:ase-code-edit", args: "<resolve-args/> <problem/>")`.
            Immediately stop processing the current skill once the
            `Skill` tool was used.

            <template>
            ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ⚖ verdict: **<verdict/>**, ▶ status: **proof completed -- hand-off to resolve**
            </template>

