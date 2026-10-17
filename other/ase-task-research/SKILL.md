---
name: ase-task-research
argument-hint: "[--help|-h] [--services|-s=(all|perplexity|brave|exa|websearch)...] [--refine|-r] [--dry-run|-d] [<id> | <id>: [<topic>] | <topic>]"
description: >
    Research a topic in depth for the current or given task plan, by
    combining Internet/Web search with a grounding in the source
    artifacts of the project, and append the resulting research report
    to the "research" attachment of the task, optionally refining the
    plan by its recommendations. Use when the user wants to "research",
    "investigate", or "look into" a topic for a "task" or "plan".
user-invocable: true
disable-model-invocation: false
effort: high
---

@${CLAUDE_SKILL_DIR}/../../meta/ase-control.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-skill.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-getopt.md

<purpose name="ase-task-research">
Research a Topic for a Task Plan
</purpose>

<expand name="getopt"
    arg1="ase-task-research"
    arg2="--services|-s=(all|perplexity|brave|exa|websearch)... --refine|-r --dry-run|-d --int-source-dir=">
    $ARGUMENTS
</expand>

<objective>
*Research* a topic in depth for a task plan, grounded in both the
*Internet*/*Web* and the *source artifacts* of the project.
</objective>

@${CLAUDE_SKILL_DIR}/../../meta/ase-format-task.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-format-meta.md

Procedure
---------

<define name="search-agent">
```text
    Agent(
        description:       "Query Web Search Service: <arg1/>",
        subagent_type:     "ase:ase-meta-search",
        prompt:            <content/>,
        run_in_background: false
    )
```
</define>

1.  **Determine Task and Topic:**

    1.  Set <topic><getopt-arguments/></topic> initially, with any
        leading and trailing whitespace stripped. Inherit the always
        existing <ase-task-id/>, <ase-session-id/>, and
        <ase-project-boxing/> from the current context. Do not output
        anything.

    2.  React on task and/or topic:

        -   If <topic/> matches the regexp `^[a-zA-Z0-9#][a-zA-Z0-9#_-]*$`,
            or has the format `<id/>:` or `<id/>: <text/>` where <id/>
            matches this regexp: set <ase-task-id><id/></ase-task-id> (or
            to <topic/> itself for the first form) and <topic/> to <text/>
            (or to empty for the first two forms), call the
            `ase_task_id(id: "<ase-task-id/>", session: "<ase-session-id/>")`
            tool of the `ase` MCP server to switch the task, and then only
            output the following <template/>:

            <template>
            ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ▶ status: **task given**
            </template>

        -   Otherwise, only output the following <template/>:

            <template>
            ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ▶ status: **task inherited**
            </template>

    3.  Treat <getopt-option-services/> as a comma-separated list of
        *backend tokens*. The getopt parser validates only the *first*
        token, so you *MUST* validate each remaining token yourself
        against the allowed set `all`, `perplexity`, `brave`, `exa`,
        `websearch`. If any token is *not* in this set, bind <token/> to
        that offending token, then only output the following <template/>
        and then immediately *STOP* processing the entire current skill:

        <template>
        ⧉ **ASE**: ☻ skill: **ase-task-research**, ▶ ERROR: invalid `--services` token: **<token/>**
        </template>

        A backend is *selected* if `all` is in <getopt-option-services/>
        *OR* that backend's own name is in <getopt-option-services/>.

    4.  *Load*: call the `ase_task_load(id: "<ase-task-id/>", tag: true)`
        tool of the `ase` MCP server -- with the `variant` argument
        defaulting to `source` and the `attachments` argument defaulting
        to `elided` -- and set <plan/> to its `text` output field without
        the trailing `<task-plan-tag>` delimiter line, and <tag/> to the
        content of that line. If <plan/> is empty or starts with `ERROR:`
        or `WARNING:`, only output the following <template/> and then
        immediately *STOP* processing the entire current skill:

        <template>
        ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ▶ ERROR: no task plan to research for
        </template>

    5.  <if condition="<topic/> is empty">
        Research the *task plan itself*: set <topic/> to a concise,
        self-contained summary of the `#   TASK:` title and the `DOM`
        bullet-points of <plan/> (skipping every bullet-point in the
        *inert* checkbox states `[-]` and `[>]`).
        </if>
        Then only output the following <template/>:

        <template>
        ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ⌕ topic: **<topic/>**, ▶ status: **topic given**
        </template>

2.  **Research the Web:**

    1.  Derive *two to four* focused, complementary search *queries*
        <queries/> from <topic/> -- like its established practices and
        standards, its typical solutions, libraries, or patterns, and its
        known pitfalls. Each query is a *self-contained* summary of an
        aspect of <topic/> and *MUST* *NEVER* carry confidential project
        internals: no file paths, no symbols or identifiers, and no
        other names taken from the project or from <plan/>, as the
        queries leave the project towards foreign search services. Do
        not output anything.

    2.  Invoke the following tool once per query <query/> of <queries/>
        and per *selected* backend, emitting *all* invocations *in one
        single message* so they run in *parallel*:

        If the `perplexity` backend is *selected* and the MCP tool
        `perplexity_search` from the MCP server `search-perplexity` is
        available:

        <expand name="search-agent" arg1="perplexity">
            Call the MCP tool `perplexity_search(query: "<query/>")`
            from the MCP server `search-perplexity`.
        </expand>

        If the `brave` backend is *selected* and the MCP tool
        `brave_web_search` from the MCP server `search-brave` is
        available:

        <expand name="search-agent" arg1="brave">
            Call the MCP tool `brave_web_search(query: "<query/>")`
            from the MCP server `search-brave`.
        </expand>

        If the `exa` backend is *selected* and the MCP tool
        `web_search_exa` from the MCP server `search-exa` is available:

        <expand name="search-agent" arg1="exa">
            Call the MCP tool `web_search_exa(query: "<query/>")`
            from the MCP server `search-exa`.
        </expand>

        If the `websearch` backend is *selected* and the tool `WebSearch`
        (or, if it is not available, the tool `web_search`) is available:

        <expand name="search-agent" arg1="websearch">
            Call the tool `WebSearch(query: "<query/>")`.
        </expand>

        If *none* of the selected backends could be invoked -- because no
        corresponding tool is available -- only output the following
        <template/> and then immediately *STOP* processing the entire
        current skill:

        <template>
        ⧉ **ASE**: ✪ skill: **ase-task-research**, ▶ ERROR: no search backend available: **<getopt-option-services/>**
        </template>

    3.  Consolidate all responses into the *Web facts* <web-facts/>:
        merge overlapping information, drop irrelevant and unsourced
        information, and keep *every* remaining fact together with its
        source URL. Do not output anything.

3.  **Ground in the Project:**

    1.  Resolve the artifact kinds `spec`, `code`, `docs`, and `infr` to
        their project-relative file lists:

        <if condition="<getopt-option-int-source-dir/> is not empty">
        The *code basis* of the task is the separate working copy
        <getopt-option-int-source-dir/> (e.g. a checkout of the branch of
        its `Source` key): run the command `ase artifact list` *once*
        with <getopt-option-int-source-dir/> as its working directory and
        parse its `# <kind/>:` and `- <file/>` output lines into the file
        lists, and read every file *exclusively* from there -- the
        `ase_artifact_list` tool always resolves against the *project*
        working copy and hence *MUST* *NOT* be used here.
        </if>
        <else>
        Call the `ase_artifact_list(kind: [ "spec", "code", "docs", "infr" ])`
        tool of the `ase` MCP server *once* and read the returned
        `artifacts` array of `{ kind, files }` objects into the file
        lists.
        </else>

    2.  From these file lists, determine the files (or their parts) which
        are relevant for <topic/> and <plan/> -- the specification parts,
        source code modules, interfaces, and symbols, the documentation,
        and the build, test, and deployment configuration the topic
        touches or depends on -- and *read* them, strictly *read-only*
        (never change, stage, or commit anything). Condense their
        relevant *project facts* -- the current state, existing
        decisions, conventions, constraints, and terminology -- each with
        its project-relative file path, into <project-facts/>. Do not
        output anything.

4.  **Synthesize the Research Report:**

    Call the `ase_timestamp(format: "yyyy-LL-dd HH:mm")` tool of the
    `ase` MCP server and set <timestamp/> to the `text` field of its
    response. Then set <section/> to the research *section* of this run
    with the following <format/>, *bounded* to about `300` lines and at
    most `10` findings (the most relevant ones), where every line of
    every part is broken after about 100 characters, and where a part
    without any content states `(none)`:

    <format>
    ##  RESEARCH: <topic/>

    *Researched: <timestamp/>*

    ### Findings

    1.  **<finding-summary/>**: <finding-text/> (<source-url/>)
    [...]

    ### Project Grounding

    -   `<project-file/>`: <project-fact/>
    [...]

    ### Assessment

    <assessment/>

    ### Recommendations

    -   **<recommendation-summary/>**: <recommendation-text/>
    [...]
    </format>

    Here the *Findings* are the most relevant Web facts of <web-facts/>,
    each with its source URL, the *Project Grounding* are the most
    relevant project facts of <project-facts/>, each with its
    project-relative file path, the *Assessment* states in 3-8 sentences
    how the findings apply to the project, including the *gaps* (what
    the project lacks) and the *conflicts* (where the project or <plan/>
    deviates from the findings), and the *Recommendations* are the
    concrete, actionable consequences for <plan/>. You *MUST* *NOT*
    invent any finding, source URL, or project fact which is not backed
    by <web-facts/> resp. <project-facts/>. The section *MUST* *NOT*
    contain a line consisting of just `---`. Do not output anything.

5.  **Attach the Research Report:**

    1.  <if condition="<getopt-option-dry-run/> is `true`">
        Set <status>researched (dry-run, not attached)</status> and
        continue with sub-step 3.
        </if>

    2.  *Persist*: update <plan/> as follows and save it, where a refused
        save restarts this sub-step:

        1.  If the backmatter of <plan/> contains an attachment block
            with the `Type` key value `text/markdown; charset=utf-8;
            kind="research"`, it carries the sections of *earlier*
            research runs: fetch its payload via the
            `ase_task_attachment(id: "<ase-task-id/>", type:
            "text/markdown; charset=utf-8; kind=\"research\"")` tool of
            the `ase` MCP server, whose `text` output field is the
            payload *verbatim*, and set <payload/> to it, followed by an
            empty line and <section/>, so the sections *accumulate* in
            chronological order. Otherwise, set <payload/> to <section/>
            and *append* a new attachment block to the backmatter of
            <plan/>.

        2.  Set the keys of this attachment block according to the plan
            <format/>: `Type` to `text/markdown; charset=utf-8;
            kind="research"`, `Desc` to <topic/> (truncated to at most 60
            characters, ending in `…` if truncated), `Created` to its
            already present value (or to <timestamp/> for a new block),
            `Modified` to <timestamp/>, and `Data` to <payload/> as a
            `|4+` literal block scalar, with *every* line -- including
            empty lines -- indented by *exactly* 4 spaces.

        3.  <if condition="<getopt-option-refine/> is `true`">
            Treat the *Recommendations* of <section/> as a *refinement
            instruction* for the plan and apply them *in-place* to the
            body of <plan/>, preserving the overall structure and the
            format of the plan <format/>: add new bullet-points in
            checkbox state `[ ]` or adjust the <text/> of existing ones,
            but *never* rewrite unrelated bullet-points and *never*
            change a bullet-point in checkbox state `[x]`, `[-]`, or
            `[>]`. Skip recommendations which the plan already reflects.
            If the body actually changed, set the `Modified:` frontmatter
            key to <timestamp/> -- the very same value as the `Modified`
            key of the research attachment, so the attachment does not
            fall behind the plan.
            </if>

        4.  Change *nothing else* of <plan/>: especially, do *not* change
            the `Status:` key, pass the `Effort:` key through *verbatim*
            (the task store drops it on its own if the body changed), and
            pass all other attachment blocks through *verbatim* (with
            their elided `Data` markers).

        5.  Call the `ase_task_save(id: "<ase-task-id/>", text: "<plan/>",
            base: "<tag/>")` tool of the `ase` MCP server, so the save is
            refused if the plan was changed meanwhile by anybody else.
            This `ase_task_save` MCP tool call is the *only* permitted way
            to persist the plan -- *NEVER* write the plan file via
            `Write`/`Edit` or by executing a shell command.

            -   On success, set <status>research attached</status>, or
                <status>research attached, plan refined</status> if the
                body was changed by sub-step 3 above.

            -   If the save is refused because the plan was *changed*
                meanwhile, *reload* <plan/> and <tag/> as in step 1.4
                and restart this sub-step 2 (keeping <section/>), at most
                *three* times in total, and afterwards set
                <status>failed: plan changed concurrently</status>.

            -   On any other error <info/>, set <status>failed:
                <info/></status>.

    3.  *Report*:

        -   <if condition="<status/> starts with `failed` or <ase-project-boxing/> is `black`">
            Only output the following <template/>:

            <template>
            ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ▶ status: **<status/>**
            </template>
            </if>

        -   <elseif condition="<ase-project-boxing/> is `grey`">
            Only output the following <template/>, where <condensed/> is
            the *Assessment* and the *Recommendations* of <section/>,
            condensed to their essentials:

            <template>
            <ase-tpl-boxed title="RESEARCH" subtitle="<ase-task-id/>">
            <condensed/>
            </ase-tpl-boxed>
            ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ▶ status: **<status/>**
            </template>
            </elseif>

        -   <else>
            Only output the following <template/>:

            <template>
            <ase-tpl-boxed title="RESEARCH" subtitle="<ase-task-id/>">
            <section/>
            </ase-tpl-boxed>
            ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ▶ status: **<status/>**
            </template>
            </else>

    4.  Finally, give the closing hint by expanding the following (which,
        depending on the configured <ase-guidance-level/>, may expand
        into nothing and hence emit no output at all), and then *STOP*
        processing the entire current skill:

        <if condition="<getopt-option-dry-run/> is `true`">
        <ase-tpl-hint level="normal">
        Run `/ase-task-research` again without `--dry-run` to append the research report to the `research` attachment of the task.
        </ase-tpl-hint>
        </if>
        <elseif condition="<getopt-option-refine/> is not `true` and <status/> starts with `research attached`">
        <ase-tpl-hint level="verbose">
        Use `/ase-task-research --refine` to additionally refine the plan by the recommendations, or `/ase-task-view --full` to view the research attachment.
        </ase-tpl-hint>
        </elseif>

