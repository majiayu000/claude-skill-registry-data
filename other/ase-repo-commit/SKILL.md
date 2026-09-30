---
name: ase-repo-commit
argument-hint: "[--help|-h]"
description: >
    Determine commit message for staged Git changes.
user-invocable: true
disable-model-invocation: false
effort: medium
allowed-tools:
    - "Bash(git diff *)"
    - "Bash(git ls-files *)"
---

@${CLAUDE_SKILL_DIR}/../../meta/ase-control.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-skill.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-getopt.md

<purpose name="ase-repo-commit">
Git Commit
</purpose>

<expand name="getopt" arg1="ase-repo-commit">
    $ARGUMENTS
</expand>

<objective>
Help to *craft* a *concise commit message* for the
currently staged Git changes.
</objective>

<flow>

1.  <step id="STEP 1: Find out staged changes">

    Run the following command to find out details of what changes are
    currently staged in the Git *index* for commit, capturing its output
    into <diff/>:

    `git diff --cached`

    <if condition="<diff/> is empty">
    Only output the following <template/> and then *STOP* immediately:

    <template>
    ⧉ **ASE**: ✪ skill: **ase-repo-commit**, ▶ status: **no changes to commit**
    </template>
    </if>

    </step>

2.  <step id="STEP 2: Craft a consolidated commit message">

    Craft a commit <message/> in the following format:

    `<type/>: <summary/>`

    The known <type/>s (kept deliberately in sync with the intent groups
    of the `ase-repo-diff` and `ase-repo-changelog` skills) and their
    usual corresponding kind of change are:

    -   `FEATURE`:     new        functionality or configuration
    -   `IMPROVEMENT`: improved   functionality or configuration
    -   `BUGFIX`:      corrected  functionality or configuration
    -   `UPDATE`:      updated    functionality or configuration
    -   `CLEANUP`:     cleaned up functionality or configuration
    -   `REFACTOR`:    refactored functionality or configuration

    The rules for generating <summary/> are:

    -   Use a maximum of 60-80 characters
    -   Use imperative mood ("add" not "added")
    -   Use *no* period at the end
    -   Use *no* Markdown formatting

    Output this crafted commit message with the following <template/>:

    <template>
    Commit Message:
    **<message/>**
    </template>

    Do *not* output any further explanation.

    Finally, give the closing hint by expanding the following (which,
    depending on the configured <ase-guidance-level/>, may expand into
    nothing and hence emit no output at all):

    <if condition="
        a `CHANGELOG.md` file exists in the project (or in any affected
        sub-package) and is *not* itself part of the staged changes
    ">
    <ase-tpl-hint level="normal">
    The staged changes do not touch `CHANGELOG.md` -- use `/ase-repo-changelog` to update its entries before committing.
    </ase-tpl-hint>
    </if>

    </step>

</flow>

