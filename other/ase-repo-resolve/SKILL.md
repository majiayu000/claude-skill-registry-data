---
name: ase-repo-resolve
argument-hint: "[--help|-h] [--dir|-d <dir>] [--safe|-s] [--interactive|-i] [<path> ...]"
description: >
    Resolve the Git merge conflicts of a working directory -- of an
    in-progress merge, rebase, cherry-pick, revert, stash apply, or of
    conflict markers left by patch -- carefully and semantically, never
    losing any change, escalate unresolvable hunks as-is, continue the
    in-progress operation, and emit a RESOLVED, PARTIAL, NONE, or FAILED
    verdict. Use when the user calls to "resolve" or "fix" merge
    conflicts.
user-invocable: true
disable-model-invocation: false
effort: high
allowed-tools:
    - "Bash(git *)"
    - "Bash(mkdir -p *)"
    - "Bash(cp -p *)"
    - "Bash(rm -rf *)"
    - "Read"
    - "Edit"
    - "Write"
---

@${CLAUDE_SKILL_DIR}/../../meta/ase-control.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-skill.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-dialog.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-getopt.md

<purpose name="ase-repo-resolve">
Resolve Merge Conflicts
</purpose>

<expand name="getopt"
    arg1="ase-repo-resolve"
    arg2="--dir|-d=. --safe|-s --interactive|-i">
    $ARGUMENTS
</expand>

<objective>
*Resolve* the merge conflicts of the working directory *semantically*,
*never* losing any change, *escalate* the unresolvable hunks as-is,
*continue* the in-progress operation, and report the *resolve verdict*.
</objective>

@${CLAUDE_SKILL_DIR}/../../meta/ase-common-resolve.md

Procedure
---------

<flow>

1.  <step id="STEP 1: Resolve Conflicts">

    1.  Set <paths/> to <getopt-arguments/> with any leading and
        trailing whitespace stripped. Do not output anything.

    2.  Resolve the conflicts by expanding the following:

        <expand name="resolve-conflicts"
            arg1="ase-repo-resolve"
            arg2="<getopt-option-dir/>"
            arg3="<getopt-option-interactive/>"
            arg4="<getopt-option-safe/>"
            arg5="<paths/>"></expand>

    3.  <if condition="<resolve-verdict/> is `FAILED`">
        Only output the following <template/> and then immediately
        *STOP* processing the entire current skill:

        <template>
        ⧉ **ASE**: ✪ skill: **ase-repo-resolve**, ▶ ERROR: **<getopt-option-dir/>** is no Git working directory, ▶ RESOLVE VERDICT: **FAILED**
        </template>
        </if>
        <elseif condition="<resolve-verdict/> is `NONE`">
        Only output the following <template/> and then immediately
        *STOP* processing the entire current skill:

        <template>
        ⧉ **ASE**: ✪ skill: **ase-repo-resolve**, ⎇ operation: **<resolve-operation/>**, ▶ RESOLVE VERDICT: **NONE**
        </template>
        </elseif>

    </step>

2.  <step id="STEP 2: Continue Operation">

    1.  If <resolve-verdict/> is not `RESOLVED` or <resolve-operation/>
        is `none`, skip this entire STEP 2, as either conflicts remain
        or there is no operation to continue (e.g., after
        `git stash apply` or `patch --merge`).

    2.  Run the command
        `git -C "<repo-root/>" diff --name-only --diff-filter=U`. If its
        output is *not* empty (unmerged files outside of <paths/>
        remain), only output the following <template/> and skip the
        remaining items of this STEP 2:

        <template>
        ⧉ **ASE**: ✪ skill: **ase-repo-resolve**, ⎇ operation: **<resolve-operation/>**, ▶ status: **not continued -- further conflicted files remain**
        </template>

    3.  Continue the operation by running the command
        `git -C "<repo-root/>" -c core.editor=true <resolve-operation/> --continue`,
        which keeps the prepared commit message without opening an
        editor.

        <if condition="the command stopped again with new conflicts (only possible for a `rebase`, `cherry-pick`, or `revert` of multiple commits)">
        Only output the following <template/> and then *START OVER* at
        STEP 1, item 2, to resolve the conflicts of the next commit:

        <template>
        ⧉ **ASE**: ✪ skill: **ase-repo-resolve**, ⎇ operation: **<resolve-operation/>**, ▶ status: **continued -- next conflicts**
        </template>
        </if>
        <elseif condition="the command failed for another reason">
        Only output the following <template/>, as the resolution itself
        is complete and staged:

        <template>
        ⧉ **ASE**: ✪ skill: **ase-repo-resolve**, ⎇ operation: **<resolve-operation/>**, ▶ WARNING: operation failed to continue
        </template>
        </elseif>
        <else>
        Only output the following <template/>:

        <template>
        ⧉ **ASE**: ✪ skill: **ase-repo-resolve**, ⎇ operation: **<resolve-operation/>**, ▶ status: **operation continued**
        </template>
        </else>

    </step>

3.  <step id="STEP 3: Report Verdict">

    1.  Report the escalations by expanding the following:

        <expand name="resolve-report" arg1="ase-repo-resolve"></expand>

    2.  Only output the following <template/>:

        <template>
        ⧉ **ASE**: ✪ skill: **ase-repo-resolve**, ⎇ operation: **<resolve-operation/>**, ▶ RESOLVE VERDICT: **<resolve-verdict/>**
        </template>

    3.  <if condition="<resolve-verdict/> is `PARTIAL`">
        Give the closing hint by expanding the following (which,
        depending on the configured <ase-guidance-level/>, may expand
        into nothing and hence emit no output at all):

        <ase-tpl-hint level="minimal">
        Resolve the escalated hunks manually (or re-run with `--interactive`), stage the files via `git add`, and continue the operation.
        </ase-tpl-hint>
        </if>

    </step>

</flow>
