---
name: ase-meta-alias
argument-hint: "[--help|-h] [--scope|-s=(auto|user|project)] <operation> [<args>]"
description: >
    List, set, delete, or expand the skill command aliases of ASE: full
    aliases like `/foo-bar` for an arbitrary ASE skill command line, option
    aliases like `--custom` for a sequence of options of a skill, and the
    option defaults of a skill. Use when the user wants to "alias" a skill
    command, define an "option alias" or "default options" of a skill, or
    inspect or test the configured aliases.
user-invocable: true
disable-model-invocation: false
effort: high
allowed-tools:
    - "Bash(ase alias *)"
---

@${CLAUDE_SKILL_DIR}/../../meta/ase-control.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-skill.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-getopt.md

<purpose name="ase-meta-alias">
Skill Command Alias Management
</purpose>

<expand name="getopt"
    arg1="ase-meta-alias"
    arg2="--scope|-s=(auto|user|project)">
    $ARGUMENTS
</expand>

<objective>
*List*, *set*, *delete*, or *expand* the *skill command aliases* of
ASE, mirroring the `ase alias <operation>` CLI subcommands.
</objective>

Procedure
---------

1.  **Determine Operation:**

    1.  Set <arguments><getopt-arguments/></arguments>, with any leading
        and trailing whitespace stripped. Set <operation/> to its *first*
        whitespace-separated token, lower-cased, and <operands/> to the
        *verbatim* remainder of <arguments/> after this token, with any
        leading and trailing whitespace stripped. If <arguments/> is
        empty, set <operation>(none)</operation> and <operands/> to empty.
        Do not output anything.

    2.  Set <scope-args></scope-args> (empty) if <getopt-option-scope/>
        is `auto`, else set <scope-args>--scope <getopt-option-scope/></scope-args>.
        Do not output anything.

    3.  You *MUST* *NOT* use `Read`, `Write`, `Edit`, or any other
        filesystem-touching tool anywhere in this skill. *Every* access to
        the aliases is performed *exclusively* through the `ase alias` CLI
        command via the `Bash` tool, with every token of <operands/> passed
        *verbatim* (keeping the quoting of the user), and with nothing else
        appended to the command (especially no redirections and pipes).
        A `--tool` option is passed only where stated below.
        Do not output anything.

2.  **Dispatch Operation:**

    1.  <if condition="<operation/> is one of `list`, `set`, `delete`, or `expand`">
        Run the command `ase alias <operation/> <scope-args/> <operands/>`
        -- for `expand` *without* <scope-args/>, as it always considers
        both scopes, and for `set` and `delete` with an additional
        `--tool <ase-agent-tool/>` directly after <scope-args/>, as they
        write the shim skills for the current agent tool -- and set
        <output/> to its standard output and <error/> to its standard
        error.

        -   If the command failed, set <message/> to the message of the
            `[ERROR]:` line of <error/> and only output the following
            <template/>, and then immediately *STOP* processing the entire
            current skill:

            <template>
            ⧉ **ASE**: ☻ skill: **ase-meta-alias**, ▶ ERROR: **<message/>**
            </template>

        -   <if condition="<operation/> is `list` or `expand`">
            Only output the following <template/>:

            <template>
            ⧉ **ASE**: ⚙ alias: **<operation/>** <operands/>

            ```text
            <output/>
            ```

            </template>
            </if>

        -   <else>
            Set <changes/> to the messages of the `[INFO]:` lines of
            <error/> (the written and removed shim skills of the full
            aliases), one per line, or to `(no shim skills changed)` if
            there are none. Then run the command
            `ase alias list --tuned` and set
            <ase-getopt-tuned/> to its standard output, with any leading
            and trailing whitespace stripped, so that the changed option
            aliases and option defaults take effect immediately, still
            within the running session. Then only output the following
            <template/>:

            <template>
            ⧉ **ASE**: ⚙ alias: **<operation/>** <operands/> (*updated*)

            ```text
            <changes/>
            ```

            </template>

            Directly *after* this <template/>, give the corrective hint by
            expanding the following (which, depending on the configured
            <ase-guidance-level/>, may expand into nothing and hence emit
            no output at all):

            <ase-tpl-hint level="minimal">
            A newly set full alias may become available as a command only after restarting the agent tool session.
            </ase-tpl-hint>
            </else>
        </if>

    2.  <else>
        The <operation/> is either missing or unknown. Notice that the
        `edit` and `sync` subcommands of the `ase alias` CLI are
        deliberately *not* mirrored by this skill. Only output the
        following <template/> and then immediately *STOP* processing the
        entire current skill:

        <template>
        ⧉ **ASE**: ☻ skill: **ase-meta-alias**, ▶ ERROR: invalid operation: **<operation/>** (expected `list`, `set`, `delete`, or `expand`)
        </template>
        </else>
