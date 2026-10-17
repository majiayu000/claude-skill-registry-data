---
name: ase-task-assign
argument-hint: "[--help|-h] [<id>:] <assignee>"
description: >
    Assign the current or given task plan to oneself or to somebody else,
    with assigning it to oneself tracking the AI usage (time, tokens, and
    costs) of the session until the task is given back, which adds the
    accumulated usage to the usage attachment of the task. Use when the user
    wants to "assign", "take", "pick up", "give back", "hand over", or
    "unassign" the "task" or "plan".
user-invocable: true
disable-model-invocation: false
effort: high
---

@${CLAUDE_SKILL_DIR}/../../meta/ase-control.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-skill.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-getopt.md

<purpose name="ase-task-assign">
Assign a Task Plan
</purpose>

<expand name="getopt" arg1="ase-task-assign">
    $ARGUMENTS
</expand>

<objective>
*Assign* the task plan and *account* the AI usage of the session onto it.
</objective>

Procedure
---------

1.  **Determine Task and Assignee:**

    1.  Parse <arguments><getopt-arguments/></arguments> (with any
        leading and trailing whitespace stripped) into a
        whitespace-separated list of tokens. Inherit the always
        existing <ase-task-id/>, <ase-session-id/>, <ase-user-id/>, and
        <ase-agent-tool/> from the current context. Set
        <id><ase-task-id/></id> and <assignee></assignee> (empty).
        Do not output anything.

    2.  <if condition="<arguments/> contains two tokens and the first token ends with `:`">
        Set <id/> to the first token with the trailing `:` removed and
        <assignee/> to the second token. Do not output anything.
        </if>

    3.  <elseif condition="<arguments/> contains exactly one token which does NOT end with `:`">
        Set <assignee/> to the token. Do not output anything.
        </elseif>

    4.  <else>
        Only output the following <template/> and then immediately
        *STOP* processing the entire current skill:

        <template>
        ⧉ **ASE**: ☻ skill: **ase-task-assign**, ▶ ERROR: expected `[<id>:] <assignee>` arguments (use `none` to unassign)
        </template>
        </else>

    5.  <if condition="<id/> does NOT match the regexp `^[a-zA-Z0-9#][a-zA-Z0-9#_-]*$`">
        Only output the following <template/> and then immediately
        *STOP* processing the entire current skill:

        <template>
        ⧉ **ASE**: ☻ skill: **ase-task-assign**, ▶ ERROR: invalid task id `<id/>` (expected `^[a-zA-Z0-9#][a-zA-Z0-9#_-]*$`)
        </template>
        </if>

2.  **Perform Assignment:**

    1.  Call the `ase_task_assign(id: "<id/>", assignee: "<assignee/>",
        session: "<ase-session-id/>", tool: "<ase-agent-tool/>")` tool
        of the `ase` MCP server and set <text/> to the `text` output
        field of this tool call. As giving a task back waits for late
        telemetry, this call takes about 10 seconds then. Do not output
        anything related to this MCP tool call.

    2.  -   If <text/> starts with `ERROR:`:
            Only output the following <template/>:

            <template>
            ⧉ **ASE**: ◉ task: **<id/>**, ▶ status: **<text/>**
            </template>

        -   If <text/> starts NOT with `ERROR:`:
            <if condition="<assignee/> is equal `me` or <ase-user-id/>, and <id/> is NOT equal <ase-task-id/>">
            Call the `ase_task_id(id: "<id/>", session: "<ase-session-id/>")`
            tool of the `ase` MCP server to switch the task, so the usage
            window of the task observes assignee changes made elsewhere, and
            set <ase-task-id><id/></ase-task-id>. Do not output anything
            related to this MCP tool call.
            </if>

            Set <result/> to the first line of <text/> with the leading
            `OK: ` prefix stripped and only output the following
            <template/>:

            <template>
            ⧉ **ASE**: ◉ task: **<id/>**, ☺ assignee: **<assignee/>** (*updated*), ▶ <result/>
            </template>

            If <text/> carries a line `NOTICE: <info/>`, additionally
            output:

            <template>
            ⧉ **ASE**: ◉ task: **<id/>**, ▶ NOTICE: <info/>
            </template>

