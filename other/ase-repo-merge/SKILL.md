---
name: ase-repo-merge
argument-hint: "[--help|-h] [--target|-t <target-branch>] [--mode|-m merge|rebase|squash] [--cleanup|-c] <source-branch>"
description: >
    Merge a Git source branch, including its still uncommitted changes,
    into a target branch through a regular merge, a rebase with
    fast-forward, or a squash merge, resolving merge conflicts semantically, check
    that the source branch landed, and emit a MERGED, CONFLICT, or FAILED
    verdict. Use when the user calls to "merge", "integrate", or "land" a
    branch.
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
@${CLAUDE_SKILL_DIR}/../../meta/ase-getopt.md

<purpose name="ase-repo-merge">
Merge a Branch
</purpose>

<expand name="getopt"
    arg1="ase-repo-merge"
    arg2="--target|-t=current --mode|-m=(merge|rebase|squash) --cleanup|-c">
    $ARGUMENTS
</expand>

<objective>
*Merge* the source branch, including its still *uncommitted* changes,
into the target branch, *resolve* all merge conflicts *semantically*,
*check* that the source branch landed, and report the *merge verdict*.
</objective>

@${CLAUDE_SKILL_DIR}/../../meta/ase-common-resolve.md

<define name="source-rollback">
If <source-commit/> is not empty and <merged/> is not equal `true`,
undo the commit of the pending source changes of STEP 2, so they are
uncommitted again: run the command `git -C "<source-dir/>" rev-parse HEAD`
and, only if its output equals <source-commit/>, run the command
`git -C "<source-dir/>" reset --quiet --mixed "<source-commit/>~1"`.
</define>

<define name="merge-fail">
First expand the following:

<expand name="source-rollback"></expand>

Then only output the following <template/> and then immediately *STOP*
processing the entire current skill:

<template>
⧉ **ASE**: ✪ skill: **ase-repo-merge**, ▶ ERROR: <arg1/>, ▶ MERGE VERDICT: **FAILED**
</template>
</define>

<flow>

1.  <step id="STEP 1: Determine Branches">

    1.  Set <source-commit/> to empty, <merged/> to `false`, and
        <squashed/> to `false`.

    2.  Set <source/> to <getopt-arguments/> with any leading and
        trailing whitespace stripped. If <source/> is empty or contains
        whitespace, expand the following:

        <expand name="merge-fail" arg1="exactly one source branch required"></expand>

    3.  Determine the *checked-out branch* by running the command
        `git branch --show-current` (taken exactly as given) and
        capturing its output into <current-branch/>. If
        <getopt-option-target/> is `current`, set
        <target><current-branch/></target>, otherwise set
        <target><getopt-option-target/></target>. If <target/> is empty
        (detached `HEAD`), expand the following:

        <expand name="merge-fail" arg1="no target branch determinable"></expand>

    4.  For each of the branches <source/> and <target/>, run the command
        `git rev-parse --verify --quiet "refs/heads/<branch/>"` (with
        <branch/> substituted). If it fails for a branch, expand the
        following:

        <expand name="merge-fail" arg1="branch **<branch/>** does not exist"></expand>

    5.  Determine the *worktrees* by running the command
        `git worktree list --porcelain` (taken exactly as given). Set
        <source-dir/> to the `worktree` path of the entry whose `branch`
        line is `refs/heads/<source/>` (or to empty if there is none),
        and set <target-dir/> to the `worktree` path of the entry whose
        `branch` line is `refs/heads/<target/>` (or to empty if there is
        none). Do not output anything.

    </step>

2.  <step id="STEP 2: Commit Pending Source Changes">

    1.  If <source-dir/> is empty, skip this entire STEP 2, as a branch
        not checked out anywhere carries no uncommitted changes.

    2.  Run the command `git -C "<source-dir/>" status --porcelain`. If
        its output is empty, skip the remaining items of this STEP 2.

    3.  Stage all changes by running the command
        `git -C "<source-dir/>" add --all`, inspect them by running the
        command `git -C "<source-dir/>" diff --cached`, and craft a
        commit <message/> in the format `<type/>: <summary/>`, where
        <type/> is one of `FEATURE`, `IMPROVEMENT`, `BUGFIX`, `UPDATE`,
        `CLEANUP`, or `REFACTOR` and <summary/> is a 60-80 character,
        imperative-mood summary without a trailing period, without
        Markdown formatting, and without any double-quote (`"`),
        backtick (`` ` ``), dollar (`$`), or backslash (`\`) characters.

    4.  Commit the changes by running the command
        `git -C "<source-dir/>" commit -m "<message/>"`. If it fails,
        unstage the changes again by running the command
        `git -C "<source-dir/>" reset --quiet` and expand the following:

        <expand name="merge-fail" arg1="pending changes of branch **<source/>** failed to commit"></expand>

    5.  Capture the output of the command
        `git -C "<source-dir/>" rev-parse HEAD` into <source-commit/>.
        If <source/> equals <target/>, set <merged/> to `true`, as the
        committed changes already landed on the target branch.

    6.  Only output the following <template/>:

        <template>
        ⧉ **ASE**: ✪ skill: **ase-repo-merge**, ⎇ branch: **<source/>**, ▶ status: **pending changes committed**
        </template>

    </step>

3.  <step id="STEP 3: Merge Source into Target">

    1.  If <source/> equals <target/>, skip this entire STEP 3, as the
        committed changes already landed on the target branch.

    2.  If <target-dir/> is empty, expand the following:

        <expand name="merge-fail" arg1="target branch **<target/>** is not checked out in any worktree"></expand>

    3.  Run the command `git -C "<target-dir/>" status --porcelain`. If
        its output is *not* empty, expand the following, leaving the
        uncommitted changes of the target *untouched*:

        <expand name="merge-fail" arg1="target branch **<target/>** has uncommitted changes"></expand>

    4.  Capture the output of the command
        `git -C "<target-dir/>" rev-parse HEAD` into <target-commit/>,
        the target branch *before* the merge. Then set <op-dir/>, the
        worktree in which the operation runs, and <abort-cmd/>, the
        command which undoes the in-progress operation, according to
        <getopt-option-mode/>:

        -   `merge`: set <op-dir><target-dir/></op-dir> and
            <abort-cmd>git -C "<target-dir/>" merge --abort</abort-cmd>.

        -   `squash`: set <op-dir><target-dir/></op-dir> and
            <abort-cmd>git -C "<target-dir/>" reset --hard --quiet HEAD</abort-cmd>,
            as a squash merge records no `MERGE_HEAD` and hence cannot
            be aborted via `git merge --abort` (the reset is safe, as
            the target worktree was free of uncommitted changes before).

        -   `rebase`: the source branch has to be *checked out* for
            being rebased. If <source-dir/> is not empty, set
            <op-dir><source-dir/></op-dir>, and, if the command
            `git -C "<source-dir/>" status --porcelain` reports any
            output, expand the following:

            <expand name="merge-fail" arg1="source branch **<source/>** has uncommitted changes"></expand>

            Otherwise, set <op-dir><target-dir/></op-dir>, where the
            rebase temporarily checks out the source branch. In both
            cases set <abort-cmd>git -C "<op-dir/>" rebase --abort</abort-cmd>,
            which also restores the original checkout of <op-dir/>.

    5.  Start the operation according to <getopt-option-mode/> by
        running the command:

        -   `merge`:  `git -C "<target-dir/>" merge --no-ff --no-edit "<source/>"`
        -   `squash`: `git -C "<target-dir/>" merge --squash "<source/>"`
        -   `rebase`: `git -C "<op-dir/>" rebase "<target/>" "<source/>"`

        If it succeeds, continue with item 9 below.

    6.  Determine the *conflicted files* by running the command
        `git -C "<op-dir/>" diff --name-only --diff-filter=U`. If there
        are none, the operation failed for another reason: run the
        command <abort-cmd/> and expand the following:

        <expand name="merge-fail" arg1="<getopt-option-mode/> of **<source/>** into **<target/>** failed"></expand>

    7.  Resolve the conflicts semantically, never losing any change, by
        expanding the following:

        <expand name="resolve-conflicts"
            arg1="ase-repo-merge"
            arg2="<op-dir/>"
            arg3="false"
            arg4="false"
            arg5=""></expand>

        <if condition="<resolve-verdict/> is not `RESOLVED`">
        Run the command <abort-cmd/>, so the target and source branches
        are left exactly as before, and, if <resolve-backup-dir/> is not
        empty, remove the now obsolete backups by running the command
        `rm -rf "<resolve-backup-dir/>"` and set
        <resolve-backup-dir></resolve-backup-dir> (empty). Then report
        the escalations by expanding the following:

        <expand name="resolve-report" arg1="ase-repo-merge"></expand>

        Then expand the following:

        <expand name="source-rollback"></expand>

        Finally, only output the following <template/> and then immediately
        *STOP* processing the entire current skill:

        <template>
        ⧉ **ASE**: ✪ skill: **ase-repo-merge**, ⎇ source: **<source/>**, ⎇ target: **<target/>**, ▶ MERGE VERDICT: **CONFLICT**
        </template>
        </if>

    8.  Conclude the conflict resolution according to
        <getopt-option-mode/> by running the command:

        -   `merge`:  `git -C "<target-dir/>" commit --no-edit`
        -   `squash`: skip this item, as item 9 below commits.
        -   `rebase`: `git -C "<op-dir/>" -c core.editor=true rebase --continue`

        If the `rebase --continue` stopped again with new conflicts of
        a further source commit, *START OVER* at item 7 above. If the
        command failed for another reason, run the command <abort-cmd/>
        and expand the following:

        <expand name="merge-fail" arg1="<getopt-option-mode/> of **<source/>** into **<target/>** failed to conclude"></expand>

        Otherwise, only output the following <template/>:

        <template>
        ⧉ **ASE**: ✪ skill: **ase-repo-merge**, ⎇ source: **<source/>**, ⎇ target: **<target/>**, ▶ status: **merge conflicts resolved**
        </template>

    9.  Land the operation according to <getopt-option-mode/>:

        -   `merge`: nothing to do, as the merge commit already exists.

        -   `squash`: if the command `git -C "<target-dir/>" diff --cached --quiet`
            succeeds, nothing was staged, as the changes of the source
            branch already are contained in the target branch, so
            nothing is to be committed. Otherwise, commit the squashed
            changes with the prepared message, listing all squashed
            commits, by running the command
            `git -C "<target-dir/>" commit --no-edit`. If it fails, run
            the command <abort-cmd/> and expand the following:

            <expand name="merge-fail" arg1="squash of **<source/>** into **<target/>** failed to commit"></expand>

            Otherwise, set <squashed/> to `true`.

        -   `rebase`: if <op-dir/> equals <target-dir/>, switch it back
            to the target branch by running the command
            `git -C "<target-dir/>" switch "<target/>"`. Then
            fast-forward the target branch onto the rebased source
            branch by running the command
            `git -C "<target-dir/>" merge --ff-only "<source/>"`. If a
            command fails, expand the following, as the source branch
            is already rebased, but the target branch is unchanged:

            <expand name="merge-fail" arg1="fast-forward of **<target/>** to rebased **<source/>** failed"></expand>

        Set <merged/> to `true`.

    </step>

4.  <step id="STEP 4: Check Merge">

    1.  If <source/> equals <target/>, skip this entire STEP 4.

    2.  <if condition="<getopt-option-mode/> is `squash`">
        A squash merge does not record the source branch as an
        ancestor, so check that the squash commit landed instead: if
        <squashed/> is `true`, run the command
        `git -C "<target-dir/>" rev-parse "<target/>~1"`, and if its
        output does not equal <target-commit/> (the squash commit is
        not the direct successor of the previous target), expand the
        following:

        <expand name="merge-fail" arg1="changes of branch **<source/>** not contained in branch **<target/>** after squash"></expand>
        </if>
        <else>
        Run the command `git merge-base --is-ancestor "<source/>" "<target/>"`.
        If it fails, the source branch did not land on the target
        branch, so expand the following:

        <expand name="merge-fail" arg1="branch **<source/>** not contained in branch **<target/>** after <getopt-option-mode/>"></expand>
        </else>

    </step>

5.  <step id="STEP 5: Clean Up Source" condition="<getopt-option-cleanup/> is equal `true` and <source/> is not equal <target/>">

    1.  If <source-dir/> is not empty and differs from <target-dir/>,
        remove the worktree of the source branch by running the command
        `git worktree remove "<source-dir/>"`.

    2.  Delete the merged source branch by running the command
        `git -C "<target-dir/>" branch -d "<source/>"`, or, for
        <getopt-option-mode/> `squash`, whose source branch Git never
        considers merged, by running the command
        `git -C "<target-dir/>" branch -D "<source/>"`.

    3.  If a command fails, only output the following <template/> and
        continue, as the merge itself succeeded:

        <template>
        ⧉ **ASE**: ✪ skill: **ase-repo-merge**, ⎇ branch: **<source/>**, ▶ WARNING: cleanup of source branch failed
        </template>

    </step>

6.  <step id="STEP 6: Report Verdict">

    Only output the following <template/>:

    <template>
    ⧉ **ASE**: ✪ skill: **ase-repo-merge**, ⎇ source: **<source/>**, ⎇ target: **<target/>**, ▶ MERGE VERDICT: **MERGED**
    </template>

    </step>

</flow>

