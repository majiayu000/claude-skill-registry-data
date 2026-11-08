---
name: ase-repo-import
argument-hint: "[--help|-h] [--safe|-s] [--interactive|-i] <url>|#<number>|<patch-file>"
description: >
    Import a change set -- a pull/merge request or commit of GitHub,
    GitLab, or Gitea, given by its URL or by its number `#<number>`, or
    a diff/patch file -- into the current Git working copy as unstaged
    and untracked files, merging it with local changes, resolving
    conflicts semantically, keeping the conflict markers of unresolvable
    hunks, reporting them as a TODO, and emitting an IMPORTED, CONFLICT,
    or FAILED verdict. Use when the user calls to "import", "fetch", or
    "apply" a pull request, merge request, commit, diff, or patch.
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

<purpose name="ase-repo-import">
Import a Change Set
</purpose>

<expand name="getopt"
    arg1="ase-repo-import"
    arg2="--safe|-s --interactive|-i">
    $ARGUMENTS
</expand>

<objective>
*Import* a change set into the working copy as *unstaged* and
*untracked* files, *merge* it with local changes, *resolve* its
conflicts *semantically*, and report the remaining conflicts as the
*TODO* and the *import verdict*.
</objective>

@${CLAUDE_SKILL_DIR}/../../meta/ase-common-resolve.md

<define name="import-fail">
If <fetched-patch/> is not empty, remove it by running the command
`rm -rf "<fetched-patch/>"`. Then only output the following <template/>
and then immediately *STOP* processing the entire current skill, as the
working copy is still *untouched*:

<template>
⧉ **ASE**: ✪ skill: **ase-repo-import**, ▶ ERROR: <arg1/>, ▶ IMPORT VERDICT: **FAILED**
</template>
</define>

Procedure
---------

<flow>

1.  <step id="STEP 1: Determine Source">

    1.  Set <fetched-patch></fetched-patch> (empty) and
        <import-escalations></import-escalations> (empty). Set <source/>
        to <getopt-arguments/> with any leading and trailing whitespace
        and any surrounding quotes stripped. If <source/> is empty,
        expand the following:

        <expand name="import-fail" arg1="exactly one source required"></expand>

    2.  Capture the outputs of the commands
        `git rev-parse --show-toplevel` and
        `git rev-parse --absolute-git-dir` (taken exactly as given) into
        <repo-root/> and <git-dir/>. If a command fails, expand the
        following:

        <expand name="import-fail" arg1="no Git repository"></expand>

    3.  Run the command `git -C "<repo-root/>" ls-files --unmerged`. If
        its output is *not* empty, expand the following, as the conflicts
        of the import could not be told apart from the existing ones:

        <expand name="import-fail" arg1="working copy has unresolved conflicts"></expand>

    4.  Classify <source/> into <source-kind/> by the *first* matching
        form:

        -   `#<number/>` (only digits after the `#`): set <source-kind/>
            to `request`. The form *always* references the number of the
            forge and *never* a task id of ASE. Determine the remotes by
            running the command `git -C "<repo-root/>" remote` and set
            <remote/> to `upstream` if it exists, else to `origin` if it
            exists. Otherwise, expand the following:

            <expand name="import-fail" arg1="neither remote `upstream` nor `origin` exists"></expand>

        -   A value starting with `http://` or `https://`: remove any
            `?...` and `#...` suffix and match the remainder as
            `<repo-url/>/<path/>`, where <path/> is one of:

            -   `commit/<sha/>` or `-/commit/<sha/>`, or
                `pull/<number/>/commits/<sha/>` or
                `pulls/<number/>/commits/<sha/>`: set <source-kind/> to
                `commit`.

            -   `pull/<number/>`, `pulls/<number/>`, or
                `-/merge_requests/<number/>`, optionally followed by
                `.diff`, `.patch`, or `/<anything/>`: set <source-kind/>
                to `request`.

            The URL is *valid* only if <repo-url/> matches the regexp
            `^https?://[A-Za-z0-9.:-]+(/[A-Za-z0-9._~-]+)+$`, <number/>
            consists of digits only, and <sha/> consists of 7 to 64
            hexadecimal digits, which keeps it safe for being passed
            quoted to the `git` commands. If it is not valid or no form
            matches, expand the following:

            <expand name="import-fail" arg1="unsupported URL: **<source/>**"></expand>

            Determine the remotes by running the command
            `git -C "<repo-root/>" remote -v` and set <remote/> to the
            first remote whose fetch URL denotes the same host and
            repository path as <repo-url/> (ignoring the scheme, the
            user, and a trailing `.git`), so its access credentials are
            used, or to <repo-url/> otherwise.

        -   Anything else: set <source-kind/> to `file` and <patch/> to
            the absolute path of <source/>, resolved against the current
            working directory. If this is no readable regular file,
            expand the following:

            <expand name="import-fail" arg1="**<source/>** is neither a supported reference nor a patch file"></expand>

    </step>

2.  <step id="STEP 2: Prepare Patch">

    1.  <if condition="<source-kind/> is `request`">

        1.  Capture the *default branch* of the remote by running the
            command `git -C "<repo-root/>" fetch --quiet --no-tags "<remote/>" HEAD`
            and then the output of the command
            `git -C "<repo-root/>" rev-parse FETCH_HEAD` into
            <default-commit/>. If a command fails, expand the following:

            <expand name="import-fail" arg1="remote **<remote/>** cannot be fetched"></expand>

        2.  Fetch the *head* by running the command
            `git -C "<repo-root/>" fetch --quiet --no-tags "<remote/>" "<ref/>"`,
            with <ref/> being `refs/pull/<number/>/head` (GitHub and
            Gitea) and, if this fails, `refs/merge-requests/<number/>/head`
            (GitLab). If both fail, expand the following:

            <expand name="import-fail" arg1="**<source/>** is no pull or merge request of **<remote/>**"></expand>

            Capture the output of the command
            `git -C "<repo-root/>" rev-parse FETCH_HEAD` into <head-commit/>.

        3.  Capture the output of the command
            `git -C "<repo-root/>" merge-base "<default-commit/>" "<head-commit/>"`
            into <base-commit/>. This is the *fork point* from the
            default branch, as the fork point from `HEAD` would import
            all foreign commits a lagging `HEAD` is missing. If the
            command fails, expand the following:

            <expand name="import-fail" arg1="no common base with the default branch of **<remote/>**"></expand>

        </if>
        <elseif condition="<source-kind/> is `commit`">

        Run the command
        `git -C "<repo-root/>" rev-parse --verify --quiet "<sha/>^{commit}"`.
        If it fails, the commit has to be fetched first: run the command
        `git -C "<repo-root/>" fetch --quiet --no-tags "<remote/>" "<sha/>"`
        and, if this fails as well (e.g., an abbreviated <sha/>, which
        can only be resolved locally), the command
        `git -C "<repo-root/>" fetch --quiet --no-tags "<remote/>" HEAD`,
        and then re-run the verification. Capture its output into
        <head-commit/> and the output of the command
        `git -C "<repo-root/>" rev-parse --verify --quiet "<head-commit/>^"`
        into <base-commit/>. If a verification fails, expand the
        following:

        <expand name="import-fail" arg1="commit **<sha/>** or its parent is not available"></expand>

        </elseif>

    2.  <if condition="<source-kind/> is not `file`">

        Set <patch><git-dir/>/ase-import.patch</patch> and
        <fetched-patch><patch/></fetched-patch>. Create the *flattened*
        patch by running the command
        `git -C "<repo-root/>" diff --no-color --no-ext-diff --src-prefix=a/ --dst-prefix=b/ --binary --full-index -M --output="<patch/>" "<base-commit/>" "<head-commit/>"`,
        which is independent of the `diff.*` configuration of the user,
        and set <strip>-p1</strip>. Capture the output of the command
        `git -C "<repo-root/>" log --oneline "<base-commit/>..<head-commit/>"`
        into <import-intent/>. Keep in mind that the fetch made the
        blobs of the patch available for the 3-way merge.

        </if>
        <else>

        Set <strip>-p1</strip>. Read the header of the patch and set
        <import-intent/> to its commit subjects or descriptive text (or
        to empty if there is none).

        </else>

    3.  Run the command
        `git -C "<repo-root/>" apply <strip/> --numstat -z "<patch/>"`.
        If it fails (no valid patch) or reports nothing (an empty change
        set, e.g., of an already merged pull request), expand the
        following:

        <expand name="import-fail" arg1="**<source/>** carries no applicable change set"></expand>

        If <source-kind/> is `file`, none of the reported paths exists
        below <repo-root/>, and at least one of them does when running
        the command with `-p0` instead, set <strip>-p0</strip> and
        re-run the command.

    4.  Only output the following <template/>:

        <template>
        ⧉ **ASE**: ✪ skill: **ase-repo-import**, ⇌ source: **<source/>**, ▶ status: **change set prepared**
        </template>

    </step>

3.  <step id="STEP 3: Apply Change Set">

    1.  Determine the *affected files* of the patch: set <touched/> to
        the paths reported by the `--numstat` command above and
        <multi-files/> to those reported more than once (a multi-commit
        patch). Run the command
        `git -C "<repo-root/>" apply <strip/> --summary "<patch/>"` and set
        <renames/> to the mapping of the *source* to the *destination*
        path of its `rename` lines (expanding the compact form
        `dir/{old => new}/file`), as `--numstat -z` reports only the
        destination. Set <created/> to the paths of its `create mode`
        lines plus the destinations of its `copy` lines, and <removed/>
        to the paths of its `delete mode` lines. Do not output anything.

    2.  Determine the *local changes* of the affected files by running
        the command
        `git -C "<repo-root/>" -c core.quotepath=off status --porcelain=v1 -- <files/>`,
        with <files/> being the quoted paths of <touched/> and the
        rename sources of <renames/>. Set <excluded/> to <multi-files/>
        plus every reported path, with a rename source replaced by its
        destination. These files bypass the 3-way merge below: it either
        refuses a file with unstaged changes or merges into its staged
        state, which the final unstaging would lose, and it nests the
        conflict markers of a file touched more than once.

    3.  Apply all other files with a 3-way merge by running the command
        `git -C "<repo-root/>" apply <strip/> --3way --exclude="<file/>" [...] "<patch/>"`,
        with one `--exclude` per file of <excluded/>, and inspect the
        result. The command is *atomic*:

        -   If it succeeded or reported `U <file/>` lines (conflict
            markers written), continue with the next item.

        -   Otherwise *nothing* was applied: add every file of an
            `error: <file/>: <reason/>` line to <excluded/>, with a
            rename source replaced by its destination, and re-run the
            command. If no line names a further file, expand the
            following:

            <expand name="import-fail" arg1="patch failed to apply"></expand>

    4.  Set <merged-files/> to the paths of <touched/> and the rename
        sources of <renames/>, without the files of <excluded/> and
        their rename sources. Only these got staged by the command
        above. Do not output anything.

    5.  <if condition="<excluded/> is not empty">

        1.  Apply the hunks of the excluded files directly onto the
            working directory, leaving their staged state alone, by
            running the command
            `git -C "<repo-root/>" apply <strip/> --reject --include="<file/>" [...] "<patch/>"`,
            with one `--include` per file of <excluded/>. Applicable
            hunks are applied, also on top of local changes, and the
            others are rejected.

        2.  Turn every *rejected* hunk into a conflict in the file, as
            no base of the 3-way merge exists for it: take the hunks from
            `<file/>.rej`, but for a file of <multi-files/> from the
            rejected sections of the patch, as `<file/>.rej` holds only
            the rejects of the last section. Locate the region of the
            hunk in the current file via its removed and context lines
            and replace this region by the following, with the labels
            of a 3-way merge, which you *MUST* write via `Edit` without
            changing anything else of the file:

            ```text
            <<<<<<< ours
            [lines of the current region]
            ||||||| base
            [removed and context lines of the hunk]
            =======
            [added and context lines of the hunk]
            >>>>>>> theirs
            ```

            Afterwards, remove `<file/>.rej`. If the region of a hunk
            cannot be located, *keep* the hunk in `<file/>.rej`, so it
            gets escalated below.

        3.  Handle every file which was reported by an
            `error: <file/>: <reason/>` line without any rejected hunk:

            -   A *new* file colliding with an existing one
                (`already exists in working directory`): if the existing
                content equals the content of the patch, nothing has to
                be done. For different text content, write the existing
                content and the content of the patch as *one* conflict
                spanning the entire file, without a `base` section.

            -   Everything else (e.g., a missing file, the removal of a
                locally changed file, a binary patch): leave the file
                *untouched* and record it in <import-escalations/> with
                its conflict kind, a one-line intent of each side, and a
                one-line reason.

        </if>

    6.  Only output the following <template/>:

        <template>
        ⧉ **ASE**: ✪ skill: **ase-repo-import**, ⇌ source: **<source/>**, ▶ status: **change set applied**
        </template>

    </step>

4.  <step id="STEP 4: Resolve Conflicts">

    1.  Set <import-paths/> to the paths of <touched/>, the rename
        sources of <renames/>, and all existing `<file/>.rej` of them.
        Do not output anything.

    2.  Resolve the conflicts by expanding the following, where *ours*
        are `HEAD` and the local changes and *theirs* is the imported
        change set with the intent <import-intent/>:

        <expand name="resolve-conflicts"
            arg1="ase-repo-import"
            arg2="<repo-root/>"
            arg3="<getopt-option-interactive/>"
            arg4="<getopt-option-safe/>"
            arg5="<import-paths/>"></expand>

    </step>

5.  <step id="STEP 5: Unstage Changes">

    1.  <if condition="<merged-files/> is not empty">
        Unstage the merged files, which also drops the unmerged state of
        their remaining conflicts, while their conflict markers stay in
        the files, by running the command
        `git -C "<repo-root/>" reset --quiet -- <files/>`, with <files/>
        being the quoted paths of <merged-files/>. You *MUST* *NOT* reset
        any other path, as the staged state of the user stays as it is.
        </if>

    </step>

6.  <step id="STEP 6: Report Verdict">

    1.  Set <import-summary/> to one to three sentences stating what the
        change set does, derived from the actual changes in <patch/>
        (for a large patch, at least from its significant hunks) and not
        only from the claims of <import-intent/>. For every path of
        <touched/>, which is relative to <repo-root/>, set <change/> to
        `added` if it is in <created/>, `removed` if it is in <removed/>,
        `renamed` if it is a destination of <renames/>, or `modified`
        otherwise, followed by `, not applied` if <import-escalations/>
        left the file untouched. Set <file/> to the path, for `renamed`
        prefixed with its rename source and ` → `, and <file-summary/> to
        a short phrase stating what the patch changes in this file. Do
        not output anything.

    2.  If <fetched-patch/> is not empty, remove it by running the
        command `rm -rf "<fetched-patch/>"`. Do not output anything.

    3.  Only output the following <template/>, with one table row per
        path of <touched/>, grouped in the order `added`, `modified`,
        `renamed`, and `removed`:

        <template>
        <ase-tpl-head title="IMPORT SUMMARY"/>

        <import-summary/>

        | Change    | File      | Summary         |
        |-----------|-----------|-----------------|
        | <change/> | `<file/>` | <file-summary/> |
        | [...]     | [...]     | [...]           |

        <ase-tpl-foot title="IMPORT SUMMARY"/>
        </template>

    4.  Set <import-todo/> to <import-escalations/> plus
        <resolve-escalations/>. Set <import-verdict>IMPORTED</import-verdict>
        if <import-todo/> is empty, or
        <import-verdict>CONFLICT</import-verdict> otherwise. Do not
        output anything.

    5.  <if condition="<import-todo/> is not empty">
        Set <backups/> to the text `⊚ backups:`, followed by a blank and
        <resolve-backup-dir/> rendered as a code span, if
        <resolve-backup-dir/> is not empty, or to empty otherwise. Then
        only output the following <template/>, with one entry per
        conflict in <import-todo/>:

        <template>
        <ase-tpl-head title="IMPORT TODO"/>

        <ase-tpl-bullet-signal/> `<file/>:<lines/>` (<kind/>): <reason/>
            ◦ ours:   <ours-intent/>
            ◦ theirs: <theirs-intent/>
        [...]

        <backups/>

        <ase-tpl-foot title="IMPORT TODO"/>
        </template>
        </if>

    6.  Only output the following <template/>:

        <template>
        ⧉ **ASE**: ✪ skill: **ase-repo-import**, ⇌ source: **<source/>**, ▶ IMPORT VERDICT: **<import-verdict/>**
        </template>

    7.  Give the closing hint by expanding the following (which,
        depending on the configured <ase-guidance-level/>, may expand
        into nothing and hence emit no output at all):

        <if condition="<import-verdict/> is `CONFLICT`">
        <ase-tpl-hint level="minimal">
        Resolve the listed conflicts manually: their conflict markers are still in the files.
        </ase-tpl-hint>
        </if>
        <else>
        <ase-tpl-hint level="normal">
        Run `/ase-repo-review --unstaged` to review the imported changes.
        </ase-tpl-hint>
        </else>

    </step>

</flow>

