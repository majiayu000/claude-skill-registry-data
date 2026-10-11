---
name: ase-task-integrate
argument-hint: "[--help|-h] [--next|-n <option>[,...]] [--worktree|-w <name>] [--changeset|-c <changeset>] [--draft|-d] [--target|-t <target>] [--mode|-m merge|rebase|squash] [--no-cleanup|-K] [--stateless|-S] [<id>]"
description: >
    Integrate the change set or implementation draft of the current or given
    task plan into its target. Use when the user calls to "deliver" or
    "apply" the change set or draft of the "task" or "plan". For merging
    a plain Git branch, use `ase-repo-merge` instead.
user-invocable: true
disable-model-invocation: false
effort: high
---

@${CLAUDE_SKILL_DIR}/../../meta/ase-control.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-skill.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-dialog.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-getopt.md

<purpose name="ase-task-integrate">
Integrate a Task Change Set
</purpose>

<expand name="getopt"
    arg1="ase-task-integrate"
    arg2="--next|-n=(none|DONE|DELETE)... --worktree|-w= --changeset|-c= --draft|-d --target|-t= --mode|-m=(merge|rebase|squash) --no-cleanup|-K --stateless|-S --int-reuse-task">
    $ARGUMENTS
</expand>

<objective>
*Integrate* the change set of the task plan from its *changeset*
location into its *target* through a Git merge.
</objective>

@${CLAUDE_SKILL_DIR}/../../meta/ase-format-task.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-common-task.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-common-changeset.md

<define name="integrate-temp-remove">
If <temp-dir/> is not empty, remove the temporary worktree and branch
by running the commands `git worktree remove --force "<temp-dir/>"`,
`git worktree prune`, and `git branch -D "<temp-branch/>"` (taken
exactly as given), ignoring any failure, and set <temp-dir></temp-dir>
(empty). Do not output anything.
</define>

Procedure
---------

1.  **Determine Task:**

    1.  Set <instruction><getopt-arguments/></instruction> initially, with any
        leading and trailing whitespace stripped, and set <temp-dir></temp-dir>
        (empty). Inherit the always existing <ase-task-id/> from the current
        context. Inherit the always existing <ase-session-id/> from the
        current context. Do not output anything.

    2.  React on task id:

        <expand name="task-react-id" arg1="ase-task-integrate"></expand>

    3.  Resolve the draft shorthand: if <getopt-option-draft/> is `true`
        and <getopt-option-changeset/> is not empty, only output the
        following <template/> and then immediately *STOP* processing the
        entire current skill:

        <template>
        ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ▶ ERROR: options `--draft` and `--changeset` are mutually exclusive
        </template>

        Otherwise, if <getopt-option-draft/> is `true`, set
        <getopt-option-changeset>attachment:draft</getopt-option-changeset>,
        so the *implementation draft* in the attachment `draft` of the
        plan is delivered. Do not output anything.

2.  **Determine Operation:**

    1.  Determine the current task plan content:

        <expand name="task-load-content"></expand>

    2.  If the <task-content/> is still empty, complain and tell the user to
        use the `ase-code-resolve`, `ase-code-refactor`, `ase-code-craft`,
        or `ase-task-edit` skills first to create a task plan, and
        `ase-task-implement` to create its change set. Then immediately
        stop processing this skill.

    3.  <if condition="<getopt-option-stateless/> is not equal `true`, the task lifecycle model <ase-project-task-lifecycle/> is `solo`, and the `Status:` frontmatter key of <task-content/> is present and not equal `OPEN`">
        Only an `OPEN` plan can be integrated in the `solo` model, as
        only `OPEN` transitions directly into `CLOSED`. Set <status/> to
        the value of this key. Only output the
        following <template/>, directly followed by the hint, and then
        immediately *STOP* processing the entire current skill, leaving
        the plan and the artifacts *untouched*:

        <template>
        ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ▶ ERROR: plan with status **<status/>** cannot be integrated (expected **OPEN**)
        </template>

        <ase-tpl-hint level="minimal">
        Run `/ase-task-status OPEN` first to re-open the plan.
        </ase-tpl-hint>
        </if>

3.  **Prepare Changeset and Target:**

    The *changeset* (location of the change set) and the *target*
    (place of integration) are controlled by the `Changeset:` and
    `Target:` frontmatter keys of the plan, which the `--changeset` and
    `--target` options override *ad-hoc* without changing the plan.
    The `worktree` value of the changeset refers to the *context
    worktree*, selected by the `--worktree` option, the `worktree` value
    of the target (and of the source it may refer to) to the *origin
    working copy* the skill was started in (both are the same without
    `--worktree`). An integration never creates a context worktree.

    1.  Set <task-changeset/> to <getopt-option-changeset/> if it is not
        empty, otherwise to the value of the `Changeset:` frontmatter key
        of <task-content/>, or to the configured default
        <ase-project-task-default-changeset/> if the key is absent, and
        parse it:

        <expand name="changeset-value"
            arg1="Changeset"
            arg2="<task-changeset/>"
            arg3="`worktree`, `branch`, `attachment`"
            arg4="◉ task: **<ase-task-id/>**"></expand>

        Set <changeset-type><value-type/></changeset-type> and
        <changeset-name><value-name/></changeset-name>.

    2.  <if condition="<getopt-option-worktree/> is not empty and <changeset-type/> is not `worktree`">
        The context worktree serves the `worktree` changeset only, so a
        `branch:` or `attachment:` changeset would leave it unused (e.g.
        on a mistyped option). Only output the following <template/> and
        then immediately *STOP* processing the entire current skill,
        leaving the working copy *untouched*:

        <template>
        ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ▶ ERROR: option `--worktree` requires a `worktree` changeset (got **<task-changeset/>**)
        </template>
        </if>

        Otherwise, prepare the context worktree:

        <expand name="changeset-context"
            arg1="<getopt-option-worktree/>"
            arg2="◉ task: **<ase-task-id/>**"
            arg3="false"
            arg4="false"></expand>

    3.  Set <task-target/> to <getopt-option-target/> if it is not
        empty, otherwise to the value of the `Target:` frontmatter key of
        <task-content/>, or to the configured default
        <ase-project-task-default-target/> if the key is absent, and parse
        it:

        <expand name="changeset-value"
            arg1="Target"
            arg2="<task-target/>"
            arg3="`worktree`, `branch`, `source`"
            arg4="◉ task: **<ase-task-id/>**"></expand>

        Set <target-type><value-type/></target-type> and
        <target-name><value-name/></target-name>. If <target-type/> is
        `source`, the target is whatever the `Source:` frontmatter key of
        <task-content/> refers to (or the configured default
        <ase-project-task-default-source/> if the key is absent):
        set <task-target/> to this value and parse it:

        <expand name="changeset-value"
            arg1="Source"
            arg2="<task-target/>"
            arg3="`worktree`, `branch`"
            arg4="◉ task: **<ase-task-id/>**"></expand>

        Set <target-type><value-type/></target-type> and
        <target-name><value-name/></target-name>.

    4.  Determine the *target branch* <target-branch/>: if <target-type/>
        is `worktree`, capture the output of the command
        `git -C "<origin-dir/>" branch --show-current`, otherwise set it
        to <target-name/>. If <target-branch/> is empty (detached `HEAD`)
        or the command
        `git rev-parse --verify --quiet "refs/heads/<target-branch/>"`
        fails, only output the following <template/> and then
        immediately *STOP* processing the entire current skill:

        <template>
        ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ▶ ERROR: target **<task-target/>** is no existing branch
        </template>

    5.  Determine the *merge source branch* <merge-source/> according to
        <changeset-type/>:

        -   `worktree`: Capture the output of the command
            `git -C "<context-dir/>" branch --show-current` into
            <merge-source/>. If it is empty (detached `HEAD`), only output
            the following <template/> and then immediately *STOP*
            processing the entire current skill:

            <template>
            ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ▶ ERROR: worktree **<context-label/>** has no checked-out branch
            </template>

        -   `branch`: Set <merge-source><changeset-name/></merge-source>.
            If the command
            `git rev-parse --verify --quiet "refs/heads/<merge-source/>"`
            fails, only output the following <template/> and then
            immediately *STOP* processing the entire current skill:

            <template>
            ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ▶ ERROR: changeset branch **<merge-source/>** does not exist
            </template>

        -   `attachment`: The change set is materialized on a *temporary*
            branch at the commit it is based on, so that the merge below
            can resolve any drift of the target semantically.

            1.  <if condition="the backmatter of <task-content/> contains NO attachment block with the `Type` key value `text/x-diff; charset=utf-8; kind="<changeset-name/>"`">
                Only output the following <template/>, directly followed
                by the hint, and then immediately *STOP* processing the
                entire current skill:

                <template>
                ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ▶ ERROR: no change set attachment **<changeset-name/>** exists
                </template>

                <ase-tpl-hint level="minimal">
                Run `/ase-task-implement --changeset <task-changeset/>` first to create the change set attachment.
                </ase-tpl-hint>
                </if>

            2.  <if condition="this attachment block is *stale* according to the plan <format/> (its `Modified` key is absent or older than the `Modified` key of the frontmatter)">
                The change set was created for an *earlier* version of
                the plan, so integrating it would deliver the wrong plan.
                Only output the following <template/>, directly followed
                by the hint, and then immediately *STOP* processing the
                entire current skill, leaving the plan and the artifacts
                *untouched*:

                <template>
                ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ▶ ERROR: change set attachment **<changeset-name/>** is **stale** (older than the plan)
                </template>

                <ase-tpl-hint level="minimal">
                Run `/ase-task-implement --changeset <task-changeset/>` again or remove the attachment.
                </ase-tpl-hint>
                </if>

            3.  <if condition="the `Desc` key of this attachment block carries a `merged <commit/>` value according to the plan <format/>">
                The change set was already *delivered* by an earlier
                integration, so integrating it again would replay it onto
                a target which already contains it. Set <merged-commit/>
                to this <commit/>, only output the following <template/>,
                directly followed by the hint, and then immediately *STOP*
                processing the entire current skill, leaving the plan and
                the artifacts *untouched*:

                <template>
                ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ▶ ERROR: change set attachment **<changeset-name/>** was already integrated (merged **<merged-commit/>**)
                </template>

                <ase-tpl-hint level="minimal">
                Run `/ase-task-implement --changeset <task-changeset/>` to create a new change set or remove the attachment.
                </ase-tpl-hint>
                </if>

            4.  Set <temp-base/> to the commit of the `base <commit/>`
                value of the `Desc:` key of this attachment block. If
                the key is absent or the command
                `git rev-parse --verify --quiet "<temp-base/>^{commit}"`
                fails, set <temp-base><target-branch/></temp-base>
                instead.

            5.  Set <temp-hash/> to the first 8 characters of the output
                of the `ase_mint(type: "sha1", hint:
                "<ase-task-id/>:<changeset-name/>:integrate")` tool of the
                `ase` MCP server, which keeps <temp-id/> *unique* per task
                and attachment. Set <temp-id/> to <ase-task-id/> with all
                characters other than `A-Z`, `a-z`, `0-9`, `_`, and `-`
                stripped, followed by
                `-<changeset-name/>-integrate-<temp-hash/>`, and set
                <temp-branch>ase-integrate/<temp-id/></temp-branch>.
                Determine <temp-dir/> by calling the `ase_worktree_path(id:
                "<temp-id/>", temp: true, create: true)` tool of the `ase`
                MCP server, which places it into the namespace of the
                *temporary* worktrees, disjoint from all other worktrees.
                You *MUST* *NEVER* assemble this path yourself.

                <if condition="<temp-dir/> exists and is *not* a worktree registered according to `git worktree list --porcelain` whose record carries the line `branch refs/heads/<temp-branch/>`">
                It is *not* owned by this skill, so set
                <temp-dir></temp-dir> (empty) to protect it from any
                removal, only output the following <template/>, and then
                immediately *STOP* processing the entire current skill,
                leaving the task plan *untouched*:

                <template>
                ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ▶ ERROR: directory **<temp-id/>** for attachment **<changeset-name/>** exists, but is no temporary worktree
                </template>
                </if>

                Otherwise, remove any *leftover* of an earlier run which
                stopped before its cleanup by expanding the following, and
                then determine <temp-dir/> once again the same way:

                <expand name="integrate-temp-remove"></expand>

            6.  Create the temporary worktree and branch by running the
                command
                `git worktree add -b "<temp-branch/>" "<temp-dir/>" "<temp-base/>"`
                (taken exactly as given), and apply the `Data` payload of
                the attachment block (with the 4-space indentation
                removed) inside it *verbatim*, e.g. via
                `git -C "<temp-dir/>" apply --3way`, re-applying hunks
                which no longer apply manually. You *MUST* *NEVER* modify
                anything *outside* of <temp-dir/>. Leave the change set
                *uncommitted*, as the merge below commits it. Set
                <merge-source><temp-branch/></merge-source>.

            If any of these sub-steps fails, expand the following:

            <expand name="integrate-temp-remove"></expand>

            Then only output the following <template/> and then
            immediately *STOP* processing the entire current skill,
            leaving the task plan *untouched*:

            <template>
            ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ▶ ERROR: change set attachment **<changeset-name/>** failed to materialize
            </template>

    6.  Check that the change set can be delivered at all. Determine the
        *change set directory* <merge-dir/>: for <changeset-type/>
        `worktree` it is <context-dir/>, for `attachment` it is
        <temp-dir/>, and for `branch` it is the directory of the
        registered worktree in which <merge-source/> is checked out
        according to `git worktree list --porcelain` (or empty if there
        is none). Do not output anything, except for the templates
        below.

        -   <if condition="<merge-source/> is equal <target-branch/> and (<changeset-type/> is not `worktree` or <context-dir/> differs from <origin-dir/>)">
            The change set and the target are the very same branch --
            either in a separate context worktree, so nothing would ever
            reach the origin working copy, or selected as `branch:`
            changeset, so a merge would just commit its uncommitted
            changes in place, which only the `worktree` changeset of the
            origin working copy documents. Expand the following, then only
            output the following <template/>, directly followed by the
            hint, and then immediately *STOP* processing the entire
            current skill, leaving the plan and the artifacts *untouched*:

            <expand name="integrate-temp-remove"></expand>

            <template>
            ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ▶ ERROR: change set and target are the same branch **<target-branch/>**
            </template>

            <ase-tpl-hint level="minimal">
            Use `--target branch:<name>` to select a different target branch.
            </ase-tpl-hint>
            </if>

        -   <elseif condition="the command `git rev-list --count "<target-branch/>..<merge-source/>"` reports `0` and either <merge-dir/> is empty or the command `git -C "<merge-dir/>" status --porcelain` reports no output">
            The change set carries neither commits beyond the target nor
            uncommitted changes, so an integration would report a
            success without delivering anything. Expand the following,
            then only output the following <template/> and then
            immediately *STOP* processing the entire current skill,
            leaving the plan and the artifacts *untouched*:

            <expand name="integrate-temp-remove"></expand>

            <template>
            ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ▶ ERROR: nothing to integrate -- change set **<task-changeset/>** carries no changes beyond target **<target-branch/>**
            </template>
            </elseif>

4.  **Integrate Change Set:**

    1.  <if condition="<getopt-option-stateless/> is not equal `true` and the task lifecycle model <ase-project-task-lifecycle/> defines the state `INTEGRATING` (i.e. `enterprise`)">
        Mark the plan as being integrated: set the `Status:` key of
        <task-content/> to `INTEGRATING` (*creating* the key at its
        position in the key order of the plan <format/> if absent), but
        *only* if `INTEGRATING` is reachable from the current state along
        the transitions of the task lifecycle model -- from `APPROVED`
        or `DEFERRED` (via `APPROVED`), or from `IMPLEMENTED` (via
        `APPROVING` and `APPROVED`, as the explicit integration request
        of the user counts as the approval) -- and persist this
        frontmatter-only change -- without refreshing the `Modified:` key
        -- by calling the `ase_task_save(id: "<ase-task-id/>", text:
        "<task-content/>")` tool of the `ase` MCP server. Do not output
        anything.
        </if>

    2.  Capture the outputs of the commands
        `git rev-parse "refs/heads/<target-branch/>"` and
        `git rev-parse "refs/heads/<target-branch/>^{tree}"` into
        <target-before/> and <target-tree-before/>, the target branch
        and its content *before* the merge. Do not output anything.

    3.  Set <merge-args>--target "<target-branch/>" --mode "<getopt-option-mode/>"</merge-args>,
        which passes the merge mode (`merge`, `rebase`, or `squash`)
        through. If <changeset-type/> is `attachment`, or
        <getopt-option-no-cleanup/> is not equal `true`, append
        ` --cleanup` to <merge-args/>, so the merged source branch (and
        its worktree) is removed afterwards. Then merge the change set by
        invoking the `ase-repo-merge` skill, which commits still
        uncommitted changes of the source branch, resolves merge
        conflicts semantically, and checks that the source branch landed:

        <skill name="ase:ase-repo-merge" args="<merge-args/> <merge-source/>" result="merge-result"/>

        Set <merge-verdict/> to the `MERGE VERDICT` reported by the
        `ase-repo-merge` skill in <merge-result/> (`MERGED`,
        `CONFLICT`, or `FAILED`), or to `FAILED` if it reported none.

    4.  <if condition="<merge-verdict/> is `MERGED` and the output of the command `git rev-parse "refs/heads/<target-branch/>^{tree}"` equals <target-tree-before/>">
        The merge succeeded, but the content of the target is unchanged,
        as the change set already landed earlier (e.g. on a repeated
        integration), so nothing was delivered: set
        <merge-verdict>NOOP</merge-verdict>. Capture the output of the
        command `git rev-parse "refs/heads/<target-branch/>"` into
        <target-after/>, and if it differs from <target-before/> and the
        output of the command
        `git rev-parse "refs/heads/<target-branch/>^1"` equals
        <target-before/>, drop the resulting empty commit by running
        the command
        `git update-ref "refs/heads/<target-branch/>" "<target-before/>" "<target-after/>"`
        (taken exactly as given), which leaves the index and working tree
        of the target intact, as their content is unchanged. Do not
        output anything.
        </if>

    5.  If <changeset-type/> is `attachment`, expand the following:

        <expand name="integrate-temp-remove"></expand>

    6.  Update the frontmatter and backmatter of <task-content/> as
        follows, but persist them *only* if anything changed:

        -   <if condition="<getopt-option-stateless/> is not equal `true`">
            If <merge-verdict/> is `MERGED`, set the `Status:` key to
            `CLOSED` for the `solo` model (traversing the transition from
            `OPEN`) or to `INTEGRATED` for the `enterprise` model (if it
            was set to `INTEGRATING` in step 1 above). Otherwise, keep
            the `Status:` key for the `solo` model (`OPEN`), and set it
            to `APPROVED` (for <merge-verdict/> `NOOP`) or `DEFERRED`
            (otherwise) for the `enterprise` model (if it was set to
            `INTEGRATING` in step 1 above). The `team` model defines no
            integration states, so its `Status:` key stays *untouched*.
            </if>

        -   <if condition="<changeset-type/> is `attachment` and <merge-verdict/> is `MERGED`">
            The delivered attachment block with the `Type` key value
            `text/x-diff; charset=utf-8; kind="<changeset-name/>"` must
            never be delivered again: if <getopt-option-no-cleanup/> is
            not equal `true`, remove it from the "backmatter". Otherwise,
            keep it, but capture the output of the command
            `git rev-parse "refs/heads/<target-branch/>"` into
            <merged-commit/> and append `, merged <merged-commit/>` to the
            value of its `Desc` key, which marks it as *delivered*
            according to the plan <format/>. Its `Modified` key stays
            *untouched*, as its `Data` payload is not changed.
            </if>

        The `Modified:` key stays *untouched*, as the "body" is not
        changed. Apart from the above, the plan *MUST* stay *exactly* as
        loaded. To persist the plan, call the `ase_task_save(id:
        "<ase-task-id/>", text: "<task-content/>")` tool of the `ase`
        MCP server. This `ase_task_save` MCP tool call is the *only*
        permitted way to persist the plan -- *NEVER* write the plan file
        via `Write`/`Edit` or by executing a shell command. Do not
        output anything in this sub-step.

    7.  <if condition="<merge-verdict/> is `MERGED`">
        Only output the following <template/>:

        <template>
        ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ⇢ changeset: **<task-changeset/>**, ⎇ target: **<target-branch/>**, ▶ status: **plan integrated**
        </template>
        </if>
        <elseif condition="<merge-verdict/> is `NOOP`">
        Only output the following <template/>, directly followed by the
        hint, and then immediately *STOP* processing the entire current
        skill:

        <template>
        ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ⇢ changeset: **<task-changeset/>**, ⎇ target: **<target-branch/>**, ▶ ERROR: nothing integrated -- change set is already contained in target
        </template>

        <ase-tpl-hint level="minimal">
        Run `/ase-task-implement` first to create a new change set, or select a different one via `--changeset`.
        </ase-tpl-hint>
        </elseif>
        <else>
        Only output the following <template/>, directly followed by the
        hint, and then immediately *STOP* processing the entire current
        skill:

        <template>
        ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ⇢ changeset: **<task-changeset/>**, ⎇ target: **<target-branch/>**, ▶ ERROR: integration failed with verdict **<merge-verdict/>**
        </template>

        <ase-tpl-hint level="minimal">
        Resolve the reported problem (e.g. commit or stash uncommitted changes of the target, or check out the target branch in a worktree) and run `/ase-task-integrate` again.
        </ase-tpl-hint>
        </else>

5.  **Decide Next Step:**

    1.  *Determine next step*:

        <expand name="task-next-select"
            arg1="ase-task-integrate"
            arg2="DONE|DELETE">
            Next Step: How would you like to proceed with the plan?
            DONE: Stop processing and PRESERVE task plan.
            DELETE: Stop processing and DELETE the task plan.
        </expand>

    2.  Check the tool <result/> and dispatch accordingly:

        -   If <result/> is `DONE` or `CANCEL`:
            Only output the following <template/> and then *STOP*.

            <template>
            ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ▶ status: **plan integrated -- done**
            </template>

        -   If <result/> is `DELETE`:
            Set <args></args> (empty). Do *not* forward any remaining
            `--next` list tokens, because the `ase:ase-task-delete`
            skill accepts only an optional `[<id>]` argument and no
            `--next` option; remaining tokens are intentionally discarded.
            Only output the following <template/> and then call the
            tool `Skill(skill: "ase:ase-task-delete", args: "<args/>")`
            to invoke the `ase:ase-task-delete` skill in order to
            *delete* the updated plan. Immediately stop processing the
            current skill once the `Skill` tool was used.

            <template>
            ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ▶ status: **plan integrated -- hand-off to delete task**
            </template>

