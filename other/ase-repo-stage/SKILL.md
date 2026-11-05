---
name: ase-repo-stage
argument-hint: "[--help|-h] [--entry|-e] [--turn|-t] [--session|-s] [--merge|-m] [--no-verify|-V] [--worktree|-w] [--changelog|-c] [--commit|-C] [<topic>]"
description: >
    Stage only the part of the current Git working copy changes which
    belongs to a topic, to the last `CHANGELOG.md` entry, to the last
    turn, or to the entire session, by picking and, if necessary,
    splitting hunks, check that the staged state builds on its own,
    and optionally chain into ChangeLog updating and commit message
    crafting. Use when the user calls to "stage" only a part of the
    changes, like "the hunks related to" a topic or "the last turn".
user-invocable: true
disable-model-invocation: false
effort: high
allowed-tools:
    - "Bash(git *)"
    - "Bash(find *)"
    - "Bash(ln -s *)"
    - "Bash(rm -f *)"
    - "Write"
    - "Read"
    - "Skill"
---

@${CLAUDE_SKILL_DIR}/../../meta/ase-control.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-skill.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-getopt.md

<purpose name="ase-repo-stage">
Stage a Part of the Changes
</purpose>

<expand name="getopt"
    arg1="ase-repo-stage"
    arg2="--entry|-e --turn|-t --session|-s --merge|-m --no-verify|-V --worktree|-w --changelog|-c --commit|-C">
    $ARGUMENTS
</expand>

<objective>
*Stage* only the part of the current Git working copy changes which
belongs to a *selection* -- a topic, the last `CHANGELOG.md` entry, the
last turn, or the entire session -- by picking and, if necessary,
*splitting* hunks, and *check* that the staged state builds on its own.
</objective>

Procedure
---------

Throughout the entire skill, you *MUST* *NEVER* modify the *content* of
any working copy file yourself: only the Git *index* is changed, the
working copy is only *temporarily* stashed and restored by STEP 4, and
only the chained `ase-repo-changelog` skill of STEP 5 may edit a file.

Whenever this skill *stops early* after STEP 1.5, first *undo* the
intent-to-add marks of all files of <intent-files/> which carry no
staged content by running the corresponding command (taken exactly as
given) per file: `git reset -q -- "<file/>"`.

<flow>

1.  <step id="STEP 1: Determine Selection and Change Set">

    1.  Set <topic><getopt-arguments/></topic>, with any leading and
        trailing whitespace stripped. If *more than one* of
        <getopt-option-entry/>, <getopt-option-turn/>, and
        <getopt-option-session/> is equal `true`, only output the
        following <template/> and then immediately *STOP*:

        <template>
        ⧉ **ASE**: ✪ skill: **ase-repo-stage**, ▶ ERROR: options `--entry`, `--turn`, and `--session` are mutually exclusive
        </template>

    2.  Determine the *selection mode* <mode/>: set it to `entry`,
        `turn`, or `session` if the corresponding option is equal
        `true`. Otherwise, *infer* it from <topic/>: set it to `turn`
        if <topic/> refers to the changes of the last (or previous)
        turn, to `session` if it refers to all changes of the current
        session, to `entry` if it refers to the last ChangeLog entry,
        and in all these cases strip the referring words from <topic/>.
        Otherwise, set it to `topic`. An explicitly given option always
        *overrides* the inference, and a remaining non-empty <topic/>
        always *narrows* the modes `entry`, `turn`, and `session`.

        If <mode/> is `topic` and <topic/> is empty, only output the
        following <template/> and then immediately *STOP*:

        <template>
        ⧉ **ASE**: ✪ skill: **ase-repo-stage**, ▶ ERROR: no selection given -- neither a topic nor `--entry`, `--turn`, or `--session`
        </template>

        Otherwise, set <selection/> to a brief rendering of <mode/> and
        <topic/> (like `topic "<topic/>"`, `last ChangeLog entry`, `last
        turn`, or `session, narrowed to "<topic/>"`) and only output the
        following <template/>:

        <template>
        ⧉ **ASE**: ✪ skill: **ase-repo-stage**, ⇌ selection: **<selection/>**
        </template>

    3.  Determine the *repository root* by running the corresponding
        command (taken exactly as given) and capturing its output into
        <repo-root/>. If this command fails, only output the following
        <template/> and then immediately *STOP*:

        `git rev-parse --show-toplevel`

        <template>
        ⧉ **ASE**: ✪ skill: **ase-repo-stage**, ▶ ERROR: no Git repository
        </template>

    4.  <if condition="<getopt-option-merge/> is not equal `true`">
        The selection *replaces* the current index content. Determine
        the staged and the unstaged files by running the corresponding
        commands (taken exactly as given):

        `git -C "<repo-root/>" -c core.quotepath=off diff --cached --name-only`

        `git -C "<repo-root/>" -c core.quotepath=off diff --name-only`

        If a file occurs in *both* lists, its staged version exists
        *nowhere else* and would be lost by resetting the index, so only
        output the following <template/> and then immediately *STOP*,
        leaving everything untouched:

        <template>
        ⧉ **ASE**: ✪ skill: **ase-repo-stage**, ▶ ERROR: files with both staged and unstaged changes -- use `--merge` or commit the staged changes first
        </template>

        Otherwise, if the first list is not empty, *unstage* everything
        by running the corresponding command (taken exactly as given),
        which leaves the working copy untouched:

        `git -C "<repo-root/>" reset -q`
        </if>
        <else>
        The selection is staged *on top* of the current index content,
        which hence stays untouched. Do not output anything.
        </else>

    5.  Determine the *untracked files* by running the corresponding
        command (taken exactly as given), skipping every entry below the
        `.ase/` directory, as it carries *ASE*'s own state:

        `git -C "<repo-root/>" -c core.quotepath=off ls-files --others --exclude-standard`

        Set <intent-files/> to the remaining files and mark each of them
        as *intent-to-add* by running the corresponding command (taken
        exactly as given), so its content shows up as an ordinary,
        splittable creation diff:

        `git -C "<repo-root/>" add -N -- "<file/>"`

    6.  Determine the *diff details* and the *diff statistics* of the
        working copy against the index by running the corresponding
        commands (taken exactly as given) and capturing their full
        outputs into <diff/> and <stat/>:

        `git -C "<repo-root/>" diff --binary`

        `git -C "<repo-root/>" diff --numstat`

        <if condition="<diff/> is empty">
        Only output the following <template/> and then *STOP*:

        <template>
        ⧉ **ASE**: ✪ skill: **ase-repo-stage**, ▶ status: **no changes to stage**
        </template>
        </if>

    </step>

2.  <step id="STEP 2: Select Changes">

    1.  Determine the *selected changes* -- the changed *lines* of
        <diff/> which belong to the selection -- according to <mode/>:

        -   `topic`: the changes which semantically belong to <topic/>.

        -   `entry`: the changes which realize the *last* ChangeLog
            entry, i.e. the entry added or modified by the *uncommitted*
            change of the `CHANGELOG.md` file in <diff/> (if several,
            the one <topic/> names, else the last one in file order),
            *plus* the lines of this entry itself. If <diff/> adds or
            modifies no such entry, only output the following
            <template/> and then *STOP*:

            <template>
            ⧉ **ASE**: ✪ skill: **ase-repo-stage**, ▶ ERROR: no uncommitted `CHANGELOG.md` entry found
            </template>

        -   `turn` resp. `session`: the changes made by your *own*
            file-modifying tool calls (like `Edit` and `Write`) of the
            *last* turn before this skill invocation resp. of the
            *entire* current session, as carried by the conversation
            context. If the context carries no such modifications which
            are still part of <diff/>, only output the following
            <template/> and then *STOP*:

            <template>
            ⧉ **ASE**: ✪ skill: **ase-repo-stage**, ▶ ERROR: no changes of the <mode/> found in the conversation context
            </template>

        For the modes `entry`, `turn`, and `session`, a non-empty
        <topic/> additionally *narrows* the selected changes to those
        which semantically belong to <topic/>.

    2.  Keep *mutually dependent* changes together: if a selected
        change only builds together with an unselected one (like a use
        and its import or declaration), select the latter, too, and
        mention it in its file summary of STEP 3.

    3.  Set <n-files/>, <n-hunks/>, and <n-split/> to the number of
        files, hunks, and *partially* selected hunks with selected
        changes. A binary file diff is never split, so it is either
        selected entirely or not at all.

        <if condition="no changes were selected">
        Only output the following <template/> and then *STOP*:

        <template>
        ⧉ **ASE**: ✪ skill: **ase-repo-stage**, ▶ status: **nothing selected for staging**
        </template>
        </if>

    </step>

3.  <step id="STEP 3: Stage Changes">

    1.  Set <tmp-dir/> to the value of the `TMPDIR` environment variable
        if it is known in the current session context, and to `/tmp`
        otherwise. Do not output anything.

    2.  Assemble <patch/> from <diff/>: keep the complete `diff --git`
        file headers and the `@@` hunk headers of all files and hunks
        with selected changes, and drop all others. Keep an *entirely*
        selected hunk *verbatim*. Turn a *partially* selected hunk into
        a sub-hunk, exactly like an edited hunk of `git add -p`: keep
        its context lines and its selected `+` and `-` lines, turn every
        *unselected* `-` line into a context line by replacing its
        leading `-` by a space, and drop every *unselected* `+` line.
        Its `@@` header stays unchanged, as `--recount` fixes its counts.

        Besides these marker changes, <patch/> stays *byte-exact*: you
        *MUST* *NEVER* re-wrap, re-indent, or re-encode a line, normalize
        or strip trailing whitespace, omit the trailing newline, or
        re-render any part of it as Markdown.

    3.  Use the `Write` tool to write <patch/> to the patch file
        `<tmp-dir/>/ase-stage.patch`, and apply it to the *index only*
        by running the corresponding command (taken exactly as given):

        `git -C "<repo-root/>" apply --cached --recount --whitespace=nowarn "<tmp-dir/>/ase-stage.patch"`

        <if condition="this command fails">
        Keep the patch file for inspection, only output the following
        <template/>, and then *STOP*:

        <template>
        ⧉ **ASE**: ✪ skill: **ase-repo-stage**, ▶ ERROR: patch failed to apply -- kept as `<tmp-dir/>/ase-stage.patch`
        </template>
        </if>

    4.  Undo the intent-to-add mark of every file of <intent-files/>
        without selected changes by running the corresponding command
        (taken exactly as given) per file, and then remove the patch
        file by running the corresponding command (taken exactly as
        given):

        `git -C "<repo-root/>" reset -q -- "<file/>"`

        `rm -f "<tmp-dir/>/ase-stage.patch"`

    5.  Only output the following <template/>, with one `○` line per
        staged file and an ultra brief <summary/> of its staged changes:

        <template>
        ○   `<file/>`: <summary/>
        [...]
        ⧉ **ASE**: ✪ skill: **ase-repo-stage**, ✚ staged: **<n-files/>** files, **<n-hunks/>** hunks (**<n-split/>** split), ▶ status: **selection staged**
        </template>

    </step>

4.  <step id="STEP 4: Verify Staged State"
        condition="<getopt-option-no-verify/> is not equal `true`">

    1.  Determine the *build command* <build/> of the project: prefer
        the command the project-level AI guidance files (`AGENTS.md`,
        `CLAUDE.md`, or similar) name for building, else derive it from
        the build configuration (like the `build` script of
        `package.json`, the default target of a `Makefile`, or the
        native build command of the language). Prefer a *single*
        top-level command which builds and type-checks the *entire*
        project.

        <if condition="no build command can be determined">
        Only output the following <template/> and then *skip* the
        remaining sub-steps of this step:

        <template>
        ⧉ **ASE**: ✪ skill: **ase-repo-stage**, ▶ status: **no build command found -- check skipped**
        </template>
        </if>

    2.  Set <build-ok/> to the outcome of running <build/> on the
        *staged state alone*, determined by the *first* applicable
        case:

        -   <if condition="the working copy carries neither unstaged changes nor untracked files besides those below `.ase/`">
            The working copy already equals the staged state (check it
            via `git -C "<repo-root/>" diff --quiet` and a re-run of the
            untracked files command of STEP 1.5), so run <build/> with
            <repo-root/> as its working directory.
            </if>

        -   <elseif condition="<getopt-option-worktree/> is equal `true`">
            Build in a *temporary worktree*: determine <check-dir/> by
            calling the `ase_worktree_path(id: "ase-repo-stage", temp:
            true, create: true)` tool of the `ase` MCP server -- you
            *MUST* *NEVER* assemble this path yourself. If <check-dir/>
            is still a registered worktree of an earlier run, remove it
            first. Then run the corresponding commands (taken exactly as
            given), where the redirection captures the binary-safe
            staged diff:

            `git -C "<repo-root/>" worktree add --detach "<check-dir/>" HEAD`

            `git -C "<repo-root/>" diff --cached --binary > "<tmp-dir/>/ase-stage-check.patch"`

            `git -C "<check-dir/>" apply --whitespace=nowarn "<tmp-dir/>/ase-stage-check.patch"`

            Link every git-ignored *dependency* directory of the working
            copy (like each `node_modules` directory, found via `find
            "<repo-root/>" -name node_modules -type d -prune -not -path
            "*/.ase/*"`) into the same relative location of <check-dir/>
            via `ln -s "<dependency-dir/>" "<check-dir/>/<relative-dir/>"`,
            so <build/> runs without a fresh installation. Then run
            <build/> with <check-dir/> as its working directory, and
            finally clean up by running the corresponding commands
            (taken exactly as given):

            `git -C "<repo-root/>" worktree remove --force "<check-dir/>"`

            `rm -f "<tmp-dir/>/ase-stage-check.patch"`
            </elseif>

        -   <else>
            Build *in place*: run the corresponding commands (taken
            exactly as given) and compare the outputs of the first and
            the third command -- only if they *differ* was the stash
            really created:

            `git -C "<repo-root/>" rev-parse -q --verify refs/stash`

            `git -C "<repo-root/>" stash push -q --keep-index --include-untracked -m "ase-repo-stage"`

            `git -C "<repo-root/>" rev-parse -q --verify refs/stash`

            If the stash was not created, only output the following
            <template/> and then immediately *STOP*, as the working copy
            stays untouched:

            <template>
            ⧉ **ASE**: ✪ skill: **ase-repo-stage**, ▶ ERROR: stashing the unstaged changes failed -- staged state not checked
            </template>

            Otherwise, run <build/> with <repo-root/> as its working
            directory, and then *always* -- also on a failed build --
            restore the working copy by running the corresponding
            commands (taken exactly as given), where the reset is safe
            because the stash carries both the index and the working
            copy:

            `git -C "<repo-root/>" reset -q --hard`

            `git -C "<repo-root/>" stash pop -q --index`

            If the `git stash pop` command fails, only output the
            following <template/> and then immediately *STOP*:

            <template>
            ⧉ **ASE**: ✪ skill: **ase-repo-stage**, ▶ ERROR: restoring the working copy failed -- the changes are kept in `git stash list` as `ase-repo-stage`
            </template>

            <ase-tpl-hint level="minimal">
            Remove the conflicting files the build created and restore the changes via `git stash pop --index`.
            </ase-tpl-hint>
            </else>

    3.  <if condition="<build-ok/> indicates success">
        Only output the following <template/>:

        <template>
        ⧉ **ASE**: ✪ skill: **ase-repo-stage**, ⚙ build: `<build/>`, ▶ status: **staged state builds**
        </template>
        </if>
        <else>
        The staged selection stays as it is, and the chaining of STEP 5
        is *skipped*. Only output the following <template/>, where
        <errors/> are the *essential* error lines of the build output
        as a fenced code block:

        <template>
        <errors/>
        ⧉ **ASE**: ✪ skill: **ase-repo-stage**, ⚙ build: `<build/>`, ▶ ERROR: staged state does not build
        </template>

        <ase-tpl-hint level="minimal">
        The selection most likely lacks a dependent change -- re-run `/ase-repo-stage` with a refined topic.
        </ase-tpl-hint>
        </else>

    </step>

5.  <step id="STEP 5: Chain into ChangeLog and Commit"
        condition="(<getopt-option-changelog/> is equal `true` or <getopt-option-commit/> is equal `true`) and STEP 4 reported no build failure">

    1.  <if condition="<getopt-option-changelog/> is equal `true`">
        Capture the unstaged diff of the `CHANGELOG.md` file located by
        `ase-repo-changelog` (in the current directory or one of its
        parents) into <before/> via `git -C "<repo-root/>" diff --
        "<changelog/>"`. Then invoke the ChangeLog updating:

        <skill name="ase:ase-repo-changelog"/>

        Capture the same diff again into <after/>, and *stage* exactly
        the changes which <after/> carries beyond <before/> -- the
        entries just added or updated for the staged selection -- by
        assembling, writing, and applying them as in STEP 3.2 and 3.3.
        </if>

    2.  <if condition="<getopt-option-commit/> is equal `true`">
        Invoke the commit message crafting for the staged selection:

        <skill name="ase:ase-repo-commit"/>
        </if>

    </step>

6.  <step id="STEP 6: Report Result">

    Give the closing hints by expanding the following (which, depending
    on the configured <ase-guidance-level/>, may each expand into
    nothing and hence emit no output at all):

    <if condition="<getopt-option-commit/> is not equal `true`">
    <ase-tpl-hint level="normal">
    Use `/ase-repo-review` to review and `/ase-repo-commit` to craft the commit message of the staged selection.
    </ase-tpl-hint>
    </if>

    <ase-tpl-hint level="verbose">
    Use `--merge` to keep already staged changes, `--worktree` to check the build in a temporary worktree, `--no-verify` to skip the check, and `--changelog`/`--commit` to chain into the ChangeLog and commit message skills.
    </ase-tpl-hint>

    </step>

</flow>

