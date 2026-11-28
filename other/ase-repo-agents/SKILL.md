---
name: ase-repo-agents
argument-hint: "[--help|-h] [--file|-f <path>] [--section|-s (all|ABOUT|LAYOUT|BUILD|STYLE)...]"
description: >
    Generate a missing or update an existing AGENTS.md agent guidance file,
    by managing its sections About, Repository Layout, Build System, and
    Code Style along the read-only verified facts of the repository, while
    keeping all hand-written sections verbatim. Use when the user wants to
    "create", "generate", "update", "refresh", or "sync" the "AGENTS.md",
    the "agent guidance", or the "agent instructions" of a repository.
user-invocable: true
disable-model-invocation: false
effort: high
allowed-tools:
    - "Bash(git rev-parse *)"
    - "Bash(git -C * rev-parse *)"
    - "Bash(git -C * ls-files *)"
    - "Bash(git -C * log *)"
    - "Bash(git -C * diff *)"
    - "Read"
    - "Write"
    - "Edit"
---

@${CLAUDE_SKILL_DIR}/../../meta/ase-control.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-skill.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-getopt.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-format-agents.md

<purpose name="ase-repo-agents">
Update Agent Guidance
</purpose>

<expand name="getopt"
    arg1="ase-repo-agents"
    arg2="--file|-f= --section|-s=(all|ABOUT|LAYOUT|BUILD|STYLE)...">
    $ARGUMENTS
</expand>

<objective>
Generate a missing or update an existing *agent guidance file*
`AGENTS.md`, by composing resp. drift-updating its *managed sections*
along the read-only verified facts of the repository, while keeping all
hand-written sections verbatim.
</objective>

Format
------

The *managed sections* (`ABOUT`, `LAYOUT`, `BUILD`, and `STYLE`), their
*Section Detection*, and the *Content Quality* rules are defined by the
*Agent Guidance Format* above, which you *MUST* strictly honor. In the
following, a *fact* is a single statement of a managed section, like a
command, a build target, a path with its role, a tool, or a convention.

Processing
----------

<flow>

1.  <step id="STEP 1: Locate agent guidance file">

    Determine the repository root by running the command
    `git rev-parse --show-toplevel` and store its output in <root/>.

    <if condition="this command fails">
    Only output the following <template/> and then immediately *STOP*
    processing the entire current skill:

    <template>
    ⧉ **ASE**: ✪ skill: **ase-repo-agents**, ▶ ERROR: no Git repository
    </template>
    </if>

    Resolve the managed sections under focus: treat
    <getopt-option-section/> as a comma-separated list of tokens, trim
    every token, and expand the sentinel `all` (the default) to
    `ABOUT,LAYOUT,BUILD,STYLE`. Set <sections/> to the resulting list,
    in the *canonical order* of the managed sections. The option parser
    validates only the *first* token, so if any token is *empty*, *not*
    one of `all`, `ABOUT`, `LAYOUT`, `BUILD`, or `STYLE` (matched
    *case-sensitively*), given twice, or `all` combined with any other
    token, bind <token/> to it, then only
    output the following <template/> and immediately *STOP* processing
    the entire current skill:

    <template>
    ⧉ **ASE**: ✪ skill: **ase-repo-agents**, ▶ ERROR: invalid `--section` token: **<token/>**
    </template>

    <if condition="<getopt-option-file/> is not empty">
    The agent guidance file is explicitly given as
    <getopt-option-file/>, relative to the current directory: store it
    in <filename/>.

    <if condition="this file lies outside of <root/> (after resolving `..` segments and symbolic links), or its existing directory belongs to a nested repository or submodule (i.e., the command `git -C "<dir/>" rev-parse --show-toplevel`, with <dir/> the directory of <filename/>, does not yield <root/>)">
    Only output the following <template/> and then immediately *STOP*
    processing the entire current skill:

    <template>
    ⧉ **ASE**: ✪ skill: **ase-repo-agents**, ▶ ERROR: agent guidance file **<getopt-option-file/>** outside of the repository
    </template>
    </if>

    If this file exists, read it and set <state>existing</state>,
    otherwise set <state>new</state>.

    <if condition="this file exists but cannot be read, or its directory does not exist (i.e., the command `git -C "<dir/>" ls-files -- .` fails, with <dir/> the directory of <filename/>)">
    Only output the following <template/> and then immediately *STOP*
    processing the entire current skill:

    <template>
    ⧉ **ASE**: ✪ skill: **ase-repo-agents**, ▶ ERROR: agent guidance file **<getopt-option-file/>** not accessible
    </template>
    </if>
    </if>
    <else>
    The agent guidance file `AGENTS.md` is located in the *current*
    directory or one of its *parent* directories up to <root/>: locate
    and read the nearest one, store its relative path in <filename/>,
    and set <state>existing</state>. If there is none, store the path
    of `AGENTS.md` in <root/>, relative to the current directory, in
    <filename/>, and set <state>new</state>.

    <if condition="the nearest file exists but cannot be read">
    Only output the following <template/> and then immediately *STOP*
    processing the entire current skill:

    <template>
    ⧉ **ASE**: ✪ skill: **ase-repo-agents**, ▶ ERROR: agent guidance file **<filename/>** not accessible
    </template>
    </if>
    </else>

    Store the directory of <filename/>, relative to <root/> (and `.`
    for <root/> itself), in <base-dir/>: it is the *scope* of the agent
    guidance file, i.e., the entire repository for a root file, resp.
    just the sub-package of a nested file. Store the path of
    <filename/>, relative to <root/>, in <repo-path/>. All `git`
    commands below run via `git -C "<root/>"` and hence take and yield
    paths relative to <root/>.

    <if condition="<state/> is `existing`">
    Detect the sections of the file according to the *Section Detection*
    rules of the *Agent Guidance Format* above, and store the
    comma-separated ids of the found managed sections in <found/> (or
    `none` if there are none).
    </if>
    <else>
    Set <found>none</found>.
    </else>

    You *MUST* *NOT* output anything, except the result with the
    following <template/>:

    <template>
    ⧉ **ASE**: **AGENTS FILE:** `<filename/>` (<state/>), **SECTIONS:** <found/>, **FOCUS:** <sections/>
    </template>

    </step>

2.  <step id="STEP 2: Inventory repository">

    You *MUST* *NOT* output anything, except introduce the current
    operation with an output based on the following <template/>:

    <template>
    ⧉ **ASE**: **INVENTORY REPOSITORY:**
    </template>

    Gather the facts of the repository *below* <base-dir/> which the
    managed sections in <sections/> need, where for a nested file the
    CI workflows, shared configurations, and manifests of its parent
    directories up to <root/>, which drive its sub-package, are read as
    well:

    1.  Obtain the authoritative list of paths with the commands
        `git -C "<root/>" ls-files -- "<base-dir/>"` (tracked files) and
        `git -C "<root/>" ls-files --others --exclude-standard -- "<base-dir/>"`
        (untracked, but not ignored files), skipping every entry below
        `.ase/`, as it carries *ASE*'s own state. For a nested file,
        additionally list the files of its parent directories and the CI
        workflows with the command
        `git -C "<root/>" ls-files -- <pathspecs/>`, where <pathspecs/>
        is `":(glob)<dir/>/*"` for each parent directory <dir/> of
        <base-dir/> (resp. `":(glob)*"` for <root/>) plus
        `".github/workflows/"` and `".gitlab-ci.yml"`. For a large list
        (like thousands of paths), do not keep it in full, but verify
        single paths in STEP 3 with targeted commands
        `git -C "<root/>" ls-files -- "<path/>"`.

    2.  Read the existing manifests and build configurations, like
        `package.json` (`scripts`, `workspaces`, `engines`),
        `etc/stx.conf` resp. `stx.conf`, `Makefile`, `justfile`,
        `Taskfile.yml`, `pyproject.toml`, `setup.cfg`, `Cargo.toml`,
        `go.mod`, `pom.xml`, `build.gradle`, `CMakeLists.txt`, and
        container definitions, resp. their counterparts in the
        sub-packages.

    3.  Read the existing linter, formatter, and type-checker
        configurations (like `eslint`, `prettier`, `biome`,
        `.editorconfig`, `markdownlint`, `tsconfig`, `ruff`, `rustfmt`,
        or `golangci` ones), the CI workflows (like `.github/workflows/`
        or `.gitlab-ci.yml`) to learn which commands CI actually runs,
        and the `README.md`. For a *new* file, also read an existing
        `CLAUDE.md` resp. `.claude/CLAUDE.md` in <base-dir/>, whose
        guidance the new file must neither duplicate nor contradict.

    4.  For the `ABOUT`, `LAYOUT`, and `STYLE` sections, read the
        relevant parts of representative source files, to learn the
        roles of the notable directories and modules and the coding
        conventions which no linter or formatter enforces.

    5.  <if condition="<state/> is `existing`">
        Determine the last commit of the agent guidance file with the
        command `git -C "<root/>" log -1 --format=%h -- "<repo-path/>"`
        and store its output in <commit/> (empty if the command fails,
        as the repository has no commit yet, or the file is not yet
        committed).

        Store as the *candidates* of drifted facts the files changed
        since then with the command
        `git -C "<root/>" log --name-status --format= <commit/>..HEAD -- <scope/>`,
        plus the uncommitted changes with the command
        `git -C "<root/>" diff --name-status HEAD -- <scope/>` and
        the untracked files of item 1, where <scope/> is `"<base-dir/>"`
        plus, for a nested file, the <pathspecs/> of item 1 (as the
        parent files drive its sub-package), resp. *no* files at all if
        <commit/> is empty, as the omissions of a not yet committed file
        are as deliberate as long-standing ones. The candidates *limit*
        the `new` facts of STEP 3, while all existing facts of the
        focused managed sections are still verified there.
        </if>

    Run no other commands than the `git` commands above: the commands
    of the repository are *never* executed (*Read-Only Verification*).

    </step>

3.  <step id="STEP 3: Verify facts">

    You *MUST* *NOT* output anything, except introduce the current
    operation with an output based on the following <template/>:

    <template>
    ⧉ **ASE**: **VERIFY FACTS:**
    </template>

    Without modifying any file, verify the facts according to the
    *Grounding* and *Read-Only Verification* rules of the *Agent
    Guidance Format* above, and classify each:

    -   <if condition="<state/> is `existing`">
        Every fact of the managed sections in <sections/> of the file is
        `valid` if the repository confirms it, `stale` if the repository
        contradicts it (like a removed or renamed command, target, path,
        or tool), or `unverifiable` if the repository can neither
        confirm nor contradict it (which is kept, see *Preservation*).
        </if>

    -   Every notable fact of the inventory of STEP 2, which belongs to
        a managed section in <sections/> but is not yet stated in the
        file, is `new`, but *only* if the repository confirms it and,
        for an existing file, it stems from the *candidates* of STEP 2
        (as long-standing omissions are a deliberate level of detail) or
        belongs to a managed section missing in the file (which is
        hence composed in full).

    Set <drift/> to the number of `stale` and `new` facts.

    </step>

4.  <step id="STEP 4: Compose managed sections">

    You *MUST* *NOT* output anything, except introduce the current
    operation with an output based on the following <template/>:

    <template>
    ⧉ **ASE**: **COMPOSE SECTIONS:**
    </template>

    <if condition="<state/> is `new`">
    Without immediately writing the file, *compose* the managed sections
    in <sections/>, in their canonical order and with their canonical
    headings, out of the `new` facts, following the *Layout*,
    *Conciseness*, *Non-Duplication*, and *Privacy* rules of the *Agent
    Guidance Format* above, where a section without any facts is
    omitted.

    If *no* section receives any fact, only output the following
    <template/> and then immediately *STOP* processing the entire
    current skill, without creating the file:

    <template>
    ⧉ **ASE**: ✪ skill: **ase-repo-agents**, ▶ NOTICE: no facts for `<filename/>`
    </template>
    </if>
    <elseif condition="<drift/> is `0`">
    Only output the following <template/> and then immediately *STOP*
    processing the entire current skill, leaving the file untouched:

    <template>
    ⧉ **ASE**: ✪ skill: **ase-repo-agents**, ▶ NOTICE: no drift in `<filename/>`
    </template>
    </elseif>
    <else>
    Without immediately modifying the file, *drift-update* the managed
    sections in <sections/> only, following the *Surgical Drift*,
    *Preservation*, and *Layout* rules of the *Agent Guidance Format*
    above: correct every `stale` fact to its current state (or remove it
    if it no longer has any counterpart), add every `new` fact at its
    fitting position and in the style of its neighbor facts, and insert
    every missing managed section in <sections/> as defined by the
    *Section Detection* rules. All unmanaged sections, all managed
    sections not in <sections/>, and all `valid` and `unverifiable`
    facts stay *exactly* as they are.
    </else>

    </step>

5.  <step id="STEP 5: Write agent guidance file">

    You *MUST* *NOT* output anything, except introduce the current
    operation with an output based on the following <template/>:

    <template>
    ⧉ **ASE**: **UPDATING AGENTS FILE:**
    </template>

    Finally, write the result according to the *Editing* rule of the
    *Agent Guidance Format* above:

    -   <if condition="<state/> is `new`">
        Create the file <filename/> with the composed sections via the
        `Write` tool.
        </if>

    -   <if condition="<state/> is `existing`">
        You *MUST* use the `Edit` tool, replacing just the changed
        lines of each drift-updated managed section, resp. inserting a
        missing managed section, instead of re-writing the entire file
        with the `Write` tool, so that the resulting changes are shown
        to the user as a diff by the agent tool itself.
        </if>

    You *MUST* *NOT* output the resulting sections a second time, any
    further summary, or any further explanations.

    The file <filename/> is deliberately left *unstaged*, as it may
    carry further unrelated changes. Finally, give the closing hint by
    expanding the following (which, depending on the configured
    <ase-guidance-level/>, may expand into nothing and hence emit no
    output at all), with <import/> set to the file name of <filename/>
    (like `AGENTS.md`) and <claude-file/> set to the path, relative to
    the current directory, of an existing `CLAUDE.md` in <base-dir/>,
    else of an existing `.claude/CLAUDE.md` in <base-dir/> (with
    <import/> prefixed by `../`), else of a new `CLAUDE.md` next to
    <filename/>:

    <if condition="
        <state/> is `new`, <import/> is not `CLAUDE.md`, neither
        `CLAUDE.md` nor `.claude/CLAUDE.md` in <base-dir/> exists with a
        line importing the new file (like `@AGENTS.md` resp.
        `@../AGENTS.md`), and no `CLAUDE.md` resp. `.claude/CLAUDE.md`
        of a parent directory of <base-dir/> up to <root/> imports it by
        its relative path (like `@tool/AGENTS.md`)
    ">
    <ase-tpl-hint level="minimal">
    For *Claude Code*, add the line `@<import/>` to `<claude-file/>` (creating it if missing), so it imports the agent guidance file.
    </ase-tpl-hint>
    </if>

    </step>

</flow>

