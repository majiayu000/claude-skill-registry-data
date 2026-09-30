---
name: ase-repo-changelog
argument-hint: "[--help|-h]"
description: >
    Update ChangeLog entries in CHANGELOG.md files
user-invocable: true
disable-model-invocation: false
model: sonnet
effort: high
allowed-tools:
    - "Bash(git log *)"
    - "Bash(git diff *)"
    - "Bash(git show *)"
    - "Bash(git tag --list *)"
    - "Read"
    - "Write"
    - "Edit"
---

@${CLAUDE_SKILL_DIR}/../../meta/ase-control.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-skill.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-getopt.md

<purpose name="ase-repo-changelog">
Update ChangeLog Entries
</purpose>

<expand name="getopt" arg1="ase-repo-changelog">
    $ARGUMENTS
</expand>

<objective>
Help to complete, consolidate and sort *ChangeLog* entries of the most
recent *ChangeLog* section, based on underlying *Git* commits and staged
changes.
</objective>

Format
------

The *ChangeLog* file is a Markdown formatted file named `CHANGELOG.md`,
and contains sections with headers in the style `N.M.K (YYYY-MM-DD)`.

Each *ChangeLog* entry is always formatted as...

    `<change-type/> [<artifact-kind/>]: <summary/>`

...where the <change-type/> is one of the following tags and their usual
related changes:

    -   `FEATURE`:     new        functionality or configuration
    -   `IMPROVEMENT`: improved   functionality or configuration
    -   `BUGFIX`:      corrected  functionality or configuration
    -   `UPDATE`:      updated    functionality or configuration
    -   `CLEANUP`:     cleaned up functionality or configuration
    -   `REFACTOR`:    refactored functionality or configuration

The <artifact-kind/> is one or more of the following *artifact* tags,
classifying which kind of artifact the change primarily touches. If
multiple artifact kinds apply, comma-separate them
(e.g. `[arch, code]`):

    -   `spec`:  requirement/specification artifacts
    -   `arch`:  architecture/design artifacts
    -   `code`:  source code artifacts
    -   `docs`:  documentation artifacts
    -   `infr`:  infrastructure/build/tooling artifacts
    -   `othr`:  any other artifacts

The <summary/> is not longer than about 60-80 characters. The
*ChangeLog* entries for a single product release version are also always
grouped and sorted according to the above <change-type/> list.

Processing
----------

<flow>

1.  <step id="STEP 1: Locate and read ChangeLog entries">

    The *ChangeLog* file `CHANGELOG.md` is located in the *current*
    directory or one of the *parent* directories of the current project.
    Locate and read this file. Store its relative path in <filename/>.

    You *MUST* *NOT* output anything, except the result with the
    following <template/>:

    <template>
    <ase-tpl-bullet-normal/> **CHANGELOG FILE:** `<filename/>`
    </template>

    </step>

2.  <step id="STEP 2: Determine artifact changes">

    You *MUST* *NOT* output anything, except introduce the current
    operation with an output based on the following <template/>:

    <template>
    <ase-tpl-bullet-normal/> **DETERMINE ARTIFACT CHANGES:**
    </template>

    To update the entries of the most recent *ChangeLog* section, consult
    the Git *commits* plus the currently already staged changes in the Git
    *index*, but *ignore* the Git *stash* and still unstaged changes.

    For finding the corresponding Git *commits*, first determine the
    correct baseline Git tag. Take the `N.M.K` from the *first* (most
    recent) level-2 header in the *ChangeLog* file and check whether a
    corresponding Git tag already exists with the command `git tag --list
    N.M.K`. If this command *does* produce output, the first section is
    already released/tagged, so use the `N.M.K` from the *first* level-2
    header as the baseline tag and *insert* a new, still-unreleased
    level-2 section (next patch version, current date) *above* it, which
    then becomes the *first* (most recent) section all subsequent steps
    operate on - the already released section *MUST* *NOT* be modified.
    If this command produces *no* output, the
    first section is still in-progress/untagged, so use the `N.M.K` from
    the *second* level-2 header as the baseline tag instead. If *no*
    second level-2 header exists (very first, still untagged release),
    skip the baseline tag and check *all* Git commits with the command
    `git log HEAD --numstat --pretty=format:'%h: %s'` instead. Then
    check all Git commits between `HEAD` and this baseline tag with the
    command `git log N.M.K..HEAD --numstat --pretty=format:'%h: %s'`.

    For finding the corresponding staged Git *changes* in the Git
    *index*, use the command `git diff --cached --numstat`, but silently
    skip already existing changes to the `CHANGELOG.md` file itself. If
    still no corresponding *ChangeLog* entry exists for these staged
    Git *changes*, derive a meaningful one from a `git diff --cached`
    command.

    </step>

3.  <step id="STEP 3: Complete ChangeLog entries">

    You *MUST* *NOT* output anything, except introduce the current
    operation with an output based on the following <template/>:

    <template>
    <ase-tpl-bullet-normal/> **COMPLETE ENTRIES:**
    </template>

    Without immediately modifying the `CHANGELOG.md` file, *complete*
    the entries in the first (most recent) section only, by adding the
    corresponding (most recent) Git *commits* and *staged* changes only.

    For each Git commit, reduce the Git commit messages to a single
    short <summary/> sentence, not longer than 60-80 characters.

    For each entry, also determine the <artifact-kind/> *artifact kind*
    tag(s) from the paths of the changed files. To classify a changed
    file to its artifact class, call the `ase_artifact_list(kind: [
    ... ])` tool of the `ase` MCP server *once*, passing the `kind`
    tokens (`spec`, `arch`, `code`, `docs`, `infr`, `othr`), and read
    the returned `artifacts` array of `{ kind, files }` objects to match
    each changed file to its kind. Use the matched lower-cased kind
    directly as its <artifact-kind/> tag, and comma-separate multiple
    tags when more than one artifact class applies.

    If a <summary/> is too short or especially is not comprehensible
    enough because of too little context information, add some essential
    context, especially references to the class/module/package, etc.
    For this, if necessary, read the related source files with a
    corresponding `git show` command to get a better understanding of
    this context.

    </step>

4.  <step id="STEP 4: Consolidate and sort ChangeLog entries">

    You *MUST* *NOT* output anything, except introduce the current
    operation with an output based on the following <template/>:

    <template>
    <ase-tpl-bullet-normal/> **CONSOLIDATE ENTRIES:**
    </template>

    Without immediately modifying the `CHANGELOG.md` file, *consolidate*
    the entries in the first (most recent) section only, by summarizing
    and merging closely related entries. Perform the entry consolidation
    per <change-type/> group only.

    Without immediately modifying the `CHANGELOG.md` file, *sort* the
    entries in the first (most recent) section only. Instead of the
    chronological commit order, group the entries by the <change-type/>s.

    </step>

5.  <step id="STEP 5: Write modified ChangeLog entries">

    You *MUST* *NOT* output anything, except introduce the current
    operation with an output based on the following <template/>:

    <template>
    <ase-tpl-bullet-signal/> **UPDATING CHANGELOG:**
    </template>

    Finally, *update* the `CHANGELOG.md` file with the completed,
    consolidated and sorted *ChangeLog* entries. Also, update the date
    `YYYY-MM-DD` in the `N.M.K (YYYY-MM-DD)` header of the *first* (most
    recent) section.

    You *MUST* *NOT* output any further summary or give any further
    explanations.

    </step>

</flow>

