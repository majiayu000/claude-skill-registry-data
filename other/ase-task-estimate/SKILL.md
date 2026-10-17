---
name: ase-task-estimate
argument-hint: "[--help|-h] [--force|-f] [--dry-run|-d] [--all|-a] [--calibrate|-c [--save|-s]] [<id> ...]"
description: >
    Estimate the effort of the current, given, or all unestimated task
    plans as T-shirt sizes (XS, S, M, L, XL) of expected human time, and
    store it in the "Effort:" frontmatter key, or calibrate the estimation
    against the actual human time of the finished tasks. Use when the user
    wants to "estimate", "size", or "gauge the effort" of a "task" or
    "plan", or to "calibrate" the effort estimation.
user-invocable: true
disable-model-invocation: false
effort: high
---

@${CLAUDE_SKILL_DIR}/../../meta/ase-control.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-skill.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-getopt.md

<purpose name="ase-task-estimate">
Estimate the Effort of a Task Plan
</purpose>

<expand name="getopt"
    arg1="ase-task-estimate"
    arg2="--force|-f --dry-run|-d --all|-a --calibrate|-c --save|-s">
    $ARGUMENTS
</expand>

<objective>
*Estimate* the effort of task plans as T-shirt sizes of expected human time.
</objective>

@${CLAUDE_SKILL_DIR}/../../meta/ase-format-task.md

Procedure
---------

<define name="effort-scores">

Derive the *scores* of the plan <plan/> (the body only, never the
frontmatter or backmatter), skipping every bullet-point in the *inert*
checkbox states `[-]` and `[>]` entirely, while all other checkbox
states (including `[x]`, as the effort covers the *entire* lifecycle of
the task) count alike. A bullet-point *without* a type (like in a
legacy plan) counts with the types following from its section: `DOM`
or `IFC` for a context or specification section (but *nothing* for a
pure rationale like a *why*), `ARC` or `IMP` for a changes or design
section, and `REG` or `CON` for a verification section. Do not output
anything.

1.  *Attention score*: set <attention/> to the sum of the weights of all
    counted bullet-points, with the weights `DOM` 5.0, `IFC` 4.0, `ARC`
    3.0, `IMP` 1.0, `REG` 0.5, and `CON` 1.0, each *multiplied* by the
    *item count* of the bullet-point: the number of *distinct*
    requirements, behaviors, or changes it states (at least `1`), like
    one per independent statement or per enumerated element, so a dense
    bullet-point stating ten key bindings counts ten times, while a
    bullet-point stating a single fact counts once. Set
    <minutes-attention/> to <attention/> times <factor/>.

2.  *Volume score*: *predict* the code impact of the counted `ARC` and
    `IMP` bullet-points *strictly read-only* from the plan and the code
    base (never change, stage, or commit anything), *disregarding* any
    already existing change set of the task (its uncommitted changes,
    its branch, or its change set attachment): *never* measure the
    volume from such a change set, so estimations before and after the
    implementation stay comparable. Set <files/> to the number of files
    they touch (or create) -- the files named by the bullet-points
    *plus* the files following from them, like call sites,
    documentation, manual pages, and generated catalogs -- and <lines/>
    to the estimated number of changed lines, sizing new files after
    comparable existing ones and changes after the code they touch, and
    <new-lines/> to the part of <lines/> in newly created files. Set
    <minutes-volume/> to <files/> times <file-minutes/> plus <lines/>
    plus twice <new-lines/> times <line-minutes/>, so a newly written
    line weighs *three* times a changed one. As a plan describes the
    straightforward path only, while the edge cases, the error
    handling, and the polishing of the realization regularly multiply
    its size, <line-minutes/> already covers this growth, hence do
    *not* inflate the predicted lines themselves.

3.  *Base size*: set <minutes/> to <minutes-attention/> plus
    <minutes-volume/>, and set <size/> to the *smallest* size of `XS`,
    `S`, `M`, and `L` whose upper band bound in <scale/> is greater than
    or equal to <minutes/>, or to `XL` if <minutes/> exceeds all bounds.

</define>

1.  **Determine Operation:**

    1.  Set <ids/> to the whitespace-separated tokens of
        <getopt-arguments/>, each with a trailing `:` removed. Inherit
        the always existing <ase-task-id/>, <ase-session-id/>,
        <ase-project-task-lifecycle/>, and <ase-project-boxing/> from the
        current context. Do not output anything.

    2.  Validate the arguments and options:

        -   If a token <token/> of <ids/> does *not* match the regexp
            `^[a-zA-Z0-9#][a-zA-Z0-9#_-]*$`, only output the following
            <template/> and then immediately *STOP* processing the entire
            current skill:

            <template>
            ⧉ **ASE**: ☻ skill: **ase-task-estimate**, ▶ ERROR: invalid task id: **<token/>**
            </template>

        -   If <getopt-option-all/> is `true` and <ids/> is *not* empty,
            only output the following <template/> and then immediately
            *STOP* processing the entire current skill:

            <template>
            ⧉ **ASE**: ☻ skill: **ase-task-estimate**, ▶ ERROR: option `--all` takes no task ids
            </template>

        -   If <getopt-option-calibrate/> is `true` and <ids/> is *not*
            empty or any of <getopt-option-all/>, <getopt-option-force/>,
            and <getopt-option-dry-run/> is `true`, only output the
            following <template/> and then immediately *STOP* processing
            the entire current skill:

            <template>
            ⧉ **ASE**: ☻ skill: **ase-task-estimate**, ▶ ERROR: option `--calibrate` takes no task ids and excludes `--all`, `--force`, and `--dry-run`
            </template>

        -   If <getopt-option-save/> is `true` and
            <getopt-option-calibrate/> is *not* `true`, only output the
            following <template/> and then immediately *STOP* processing
            the entire current skill:

            <template>
            ⧉ **ASE**: ☻ skill: **ase-task-estimate**, ▶ ERROR: option `--save` requires `--calibrate`
            </template>

    3.  Determine the *estimation configuration*: for each of the keys
        `project.task.effort.scale`, `project.task.effort.factor`,
        `project.task.effort.file`, `project.task.effort.line`, and
        `project.task.effort.iteration`, call the `ase_config_get(key:
        "<key/>", scope: "project")` tool of the `ase` MCP server and
        JSON-decode its `text` output field. Set <scale/> to the four
        comma-separated upper band bounds of `XS` to `L` (default:
        `15,60,240,960`), <factor/> to the human minutes per
        attention-score point (default: `1`), <file-minutes/> to the
        human review minutes per touched file (default: `1`),
        <line-minutes/> to the human minutes per predicted changed line
        (default: `0.025`), and <iteration-factor/> to the iteration
        multiplier of interactive user interfaces (default: `2.5`), each
        falling back to its default if empty or malformed. Do not
        output anything.

    4.  Determine the *finished states* <finished-states/> and the
        *successful finished state* <success-state/> of the task lifecycle
        model <ase-project-task-lifecycle/>: `CLOSED` and `CANCELLED`
        resp. `CLOSED` for `solo` (or absent), `IMPLEMENTED` and
        `CANCELLED` resp. `IMPLEMENTED` for `team`, and `INTEGRATED` and
        `CANCELLED` resp. `INTEGRATED` for `enterprise`. Do not output
        anything.

    5.  <if condition="<getopt-option-calibrate/> is `true`">
        Skip step 2 and continue with step 3.
        </if>

2.  **Estimate Task Plans:**

    1.  Determine the tasks <tasks/> to estimate:

        -   If <getopt-option-all/> is `true`: call the
            `ase_task_list(verbose: true)` tool of the `ase` MCP server and
            set <tasks/> to the `id` of every entry of its `tasks` array
            whose `status` is *not* in <finished-states/> and -- unless
            <getopt-option-force/> is `true` -- whose `effort` is empty.

        -   Else, if <ids/> is not empty: set <tasks><ids/></tasks>.

        -   Else: set <tasks><ase-task-id/></tasks>.

        <if condition="<tasks/> is empty">
        Only output the following <template/> and then *STOP* processing
        the entire current skill:

        <template>
        ⧉ **ASE**: ◉ tasks: *(none)*, ▶ status: **nothing to estimate**
        </template>
        </if>

    2.  Set <analogues/> to the *analogues* for cross-checking: call the
        `ase_task_list(verbose: true)` tool of the `ase` MCP server (or
        reuse its result of sub-step 1), take every entry whose `status`
        is <success-state/> and whose `effort` is *not* empty, and pick
        up to *five* of them whose title is most similar to the tasks of
        <tasks/>. For each picked one, call the `ase_task_attachment(id:
        "<id/>", type: "application/yaml; kind=\"usage\"")` tool of the
        `ase` MCP server, and keep it only if it carries a usage
        attachment (a `WARNING:` response means none), whose YAML payload
        `time: { ai, hr, real }` carries a `hr` of at least `5` minutes, together
        with its `effort` size and the size whose band covers its
        `time.hr` (its *actual* size). Do not output anything.

    3.  For each task id <id/> of <tasks/>, perform the following
        *per-task workflow*, where a failing task never stops the
        processing of the remaining tasks:

        1.  *Load*: call the `ase_task_load(id: "<id/>", tag: true)` tool
            of the `ase` MCP server -- with the `variant` argument
            defaulting to `source` and the `attachments` argument
            defaulting to `elided` -- and set <plan/> to its `text`
            output field without the trailing `<task-plan-tag>`
            delimiter line, and <tag/> to the content of that line.

            -   If <plan/> is empty, set <status>skipped: no plan</status>
                and continue with sub-step 5.

            -   If the `Group:` frontmatter key of <plan/> equals its
                `Id:` key (an *explicit epic*), set <status>skipped:
                epic</status> and continue with sub-step 5.

            -   If <plan/> carries an `Effort:` frontmatter key (which the
                task store only delivers if it is *valid*) and
                <getopt-option-force/> is *not* `true`, set <size/> to its
                size and <status>skipped: already estimated</status> and
                continue with sub-step 5.

        2.  *Score*: derive the scores of <plan/>:

            <expand name="effort-scores"></expand>

        3.  *Adjust*:

            -   *Risk surcharge*: determine which of the risks `dependency`
                (a new or upgraded third-party dependency or external
                service), `ambiguity` (bullet-points in state `[?]` or
                vague, underspecified wording), `untested` (changed code
                without an automated test procedure covering it),
                `concurrency` (parallelism, locking, or race conditions),
                `security` (authentication, authorization, secrets, or
                untrusted input), and `persistence` (data formats,
                migrations, or stored state) apply to <plan/>. There is
                *no* `architecture` risk, as the `ARC` weight already
                covers it, and a risk applying to virtually *every* task
                of the project (like `untested` in a project without any
                automated test procedure) does *not* count, as the
                calibrated rates already absorb it. Set <surcharge/> to
                `20` percent per applying risk, but at most `40` percent
                in total, and raise <minutes/> by <surcharge/> percent.

            -   *Iteration multiplier*: if the *main* deliverable of
                <plan/> is an *interactive* or *visual* user interface
                (like a terminal UI, a web UI, a layout, or a rendering
                with key or pointer handling) which is built or
                substantially reworked, set <iteration/> to
                <iteration-factor/>, as
                such work regularly needs many rounds of post-adjustment
                which no plan foresees; else set <iteration/> to `1`. A
                mere display detail of an existing interface (like an
                additional badge or column) does *not* count. Multiply
                <minutes/> by <iteration/> -- *outside* the cap of the
                risk surcharge -- and re-determine <size/> from the
                resulting <minutes/> like the base size.

            -   *Plausibility*: if the code base already contains a
                *comparable* realization of the planned functionality
                (but *never* the change set of the task itself, see the
                volume score), set <reference/> to its size in lines and
                consider the prediction *implausible* if <lines/> and
                <reference/> differ by a factor of at least `2`. A
                reference *never* changes <size/> itself.

            -   *Confidence*: set <confidence/> to `HIGH`. Lower it by
                one level (`HIGH` to `MEDIUM` to `LOW`) if the `ambiguity`
                risk applies, by one level if the prediction is
                implausible, and by one level if <analogues/> is empty or
                if the analogues of comparable scope disagree with <size/>
                (their actual size differs from <size/> by at least one
                band), and by two levels if they disagree by at least two
                bands, but never below `LOW`. The analogues *never*
                change <size/> itself.

            -   *Drivers*: set <drivers/> to the 2-4 main drivers of the
                estimation (like the dominant bullet-point types, the
                code volume, the applying risks, the iteration
                multiplier, an implausible prediction, or the analogues),
                each as an ultra brief phrase.

        4.  *Persist*: <if condition="<getopt-option-dry-run/> is `true`">
            set <status>estimated (dry-run, not stored)</status>.
            </if>
            <else>
            Set the `Effort:` frontmatter key of <plan/> to *just*
            <size/> -- *without* any content hash, as the task store
            stamps it on save -- replacing an already present `Effort:`
            key, or *creating* it at its position in the key order of the
            plan <format/> (directly after `Kind:` resp. before `Tags:`).
            Change *nothing else* of <plan/>: especially, do *not*
            refresh the `Modified:` key (an effort is no body change), do
            *not* change the `Status:` key, and pass the entire
            backmatter through *verbatim* (with its elided `Data`
            markers). Call the `ase_task_save(id: "<id/>", text:
            "<plan/>", base: "<tag/>")` tool of the `ase` MCP server, so
            the save is refused if the plan was changed meanwhile by
            anybody else. This `ase_task_save` MCP tool call is the
            *only* permitted way to persist the plan -- *NEVER* write the
            plan file via `Write`/`Edit` or by executing a shell command.

            -   On success, set <status>effort estimated</status>.

            -   If the save is refused because the plan was *changed*
                meanwhile, *reload* and *re-estimate* the task by
                restarting the per-task workflow at sub-step 1, at most
                *three* times in total, and afterwards set <status>failed:
                plan changed concurrently</status>.

            -   On any other error <info/>, set <status>failed:
                <info/></status>.
            </else>

        5.  *Report*: <if condition="<status/> starts with `skipped` or `failed`">
            only output the following <template/>:

            <template>
            ⧉ **ASE**: ◉ task: **<id/>**, ▶ status: **<status/>**
            </template>
            </if>
            <else>
            only output the following <template/>, where every driver of
            <drivers/> is rendered as its own `○` line -- but *without*
            any driver lines if <ase-project-boxing/> is `black`, and
            with an additional first `○` line `attention <attention/>
            (<minutes-attention/> min), volume <files/> files / <lines/>
            lines (<minutes-volume/> min), risk +<surcharge/>%, iteration
            x<iteration/> (<minutes/> min)` if <ase-project-boxing/> is
            `white`:

            <template>
            ⧉ **ASE**: ◉ task: **<id/>**, ⚖ effort: **<size/>** (confidence: **<confidence/>**), ▶ status: **<status/>**
            ○   [...]
            </template>

            <if condition="<size/> is `XL`">
            Directly *after* this <template/>, only output the following
            <template/>:

            <template>
            ⧉ **ASE**: ◉ task: **<id/>**, ▶ WARNING: effort **XL** is open-ended -- consider splitting the task via `/ase-task-dissect <id/>`
            </template>
            </if>
            </else>

    4.  <if condition="<tasks/> contains more than one task">
        Only output the following <template/>, where <n-estimated/>,
        <n-skipped/>, and <n-failed/> are the numbers of tasks whose
        <status/> was an estimation, a skip, resp. a failure:

        <template>
        ⧉ **ASE**: ⚖ estimated: **<n-estimated/>**, skipped: **<n-skipped/>**, failed: **<n-failed/>**
        </template>
        </if>

    5.  Finally, give the closing hint by expanding the following (which,
        depending on the configured <ase-guidance-level/>, may expand
        into nothing and hence emit no output at all), and then *STOP*
        processing the entire current skill:

        <if condition="<getopt-option-dry-run/> is `true`">
        <ase-tpl-hint level="normal">
        Run `/ase-task-estimate` again without `--dry-run` to store the estimated effort in the `Effort:` key.
        </ase-tpl-hint>
        </if>
        <elseif condition="a task was skipped as already estimated">
        <ase-tpl-hint level="verbose">
        Use `/ase-task-estimate --force` to re-estimate tasks already carrying a valid effort.
        </ase-tpl-hint>
        </elseif>

3.  **Calibrate Estimation:**

    1.  Call the `ase_task_list(verbose: true)` tool of the `ase` MCP
        server and take every entry whose `status` is <success-state/>
        (a task which reached its intended outcome, unlike a cancelled
        one) and whose `effort` is *not* empty. For each of them, call the
        `ase_task_attachment(id: "<id/>", type: "application/yaml;
        kind=\"usage\"")` tool of the `ase` MCP server and keep the task
        as a *sample* only if it carries a usage attachment (a `WARNING:`
        response means none), whose YAML payload `time: { ai, hr, real }`
        carries a `hr` (the `time.hr`) of at least `5` minutes, as agent-driven tasks book
        little human time. For each sample, set its *actual* size to the
        size whose band in <scale/> covers its `time.hr`. Do not output
        anything.

        Then *re-score* every sample with the *current* rates, as its
        stored `effort` was estimated with the rates in effect *at that
        time* (which nothing records), so calibrating against it would
        apply an already applied correction again on every repeated
        calibration: call the `ase_task_load(id: "<id/>")` tool of the
        `ase` MCP server, set <plan/> to its `text` output field, and --
        skipping the sample if <plan/> is empty or starts with `ERROR:`
        or `WARNING:` -- derive the scores of <plan/>:

        <expand name="effort-scores"></expand>

        Here, predict the volume as of *before* the realization of the
        task, i.e. *never* measure it from the realized code in the code
        base. Then apply the *risk surcharge* and the *iteration
        multiplier* of sub-step 2.3.3 (but not its plausibility,
        confidence, and drivers), and set the *re-scored minutes* of the
        sample to the resulting <minutes/> and its *estimated* size to
        the resulting <size/>. Do not output anything.

    2.  <if condition="there are fewer than *three* samples">
        Only output the following <template/> and then *STOP* processing
        the entire current skill, leaving the configuration *untouched*:

        <template>
        ⧉ **ASE**: ⚖ calibration: **<n/>** samples, ▶ WARNING: insufficient data (at least 3 finished tasks with an effort and at least 5 human minutes required)
        </template>
        </if>

    3.  Determine the calibration figures:

        -   *Band matrix*: the number of samples per pair of estimated
            size (rows `XS` to `XL`) and actual size (columns `XS` to
            `XL`).

        -   *Hit rate*: the percentage of samples whose estimated size
            equals their actual size.

        -   *Bias*: the mean of the band differences (estimated minus
            actual, in bands), where a positive value means
            *overestimation* and a negative one *underestimation*.

        -   *Correction*: <correction/> is the median of `time.hr`
            divided by the re-scored minutes over all samples.

        -   *Fitted rates*: <fitted-factor/>, <fitted-file/>, and
            <fitted-line/> are <factor/>, <file-minutes/>, resp.
            <line-minutes/>, each multiplied by <correction/> and rounded
            to two significant digits, as the best-fitting rates, which
            scale the *entire* estimation (attention and volume)
            proportionally. As the samples are re-scored with the current
            rates, a repeated calibration right after saving the fitted
            rates yields a <correction/> of about `1` and hence
            *converges* instead of compounding.

        -   *Suggested scale*: the bounds of <scale/>, each multiplied by
            <correction/>, rounded to integers -- an *alternative* to the
            fitted rates and a *suggestion* only, which is never stored.

        Do not output anything.

    4.  Only output the following <template/>, with the band matrix
        rendered as a Markdown table with aligned column edges:

        <template>
        <ase-tpl-head title="EFFORT CALIBRATION" subtitle="<n/> samples"/>

        **Band Matrix** (rows: estimated, columns: actual):

        | *Est.* | *XS*  | *S*   | *M*   | *L*   | *XL*  |
        | ------ | ----- | ----- | ----- | ----- | ----- |
        | **XS** | [...] | [...] | [...] | [...] | [...] |
        | [...]  | [...] | [...] | [...] | [...] | [...] |

        ●   **Hit Rate**: <hit-rate/>%
        ●   **Bias**: <bias/> bands
        ●   **Rates**: factor <factor/>, file <file-minutes/>, line <line-minutes/> (current) → factor **<fitted-factor/>**, file **<fitted-file/>**, line **<fitted-line/>** (fitted)
        ●   **Scale**: `<scale/>` (current) → `<suggested-scale/>` (suggested alternative)

        <ase-tpl-foot title="EFFORT CALIBRATION" subtitle="<n/> samples"/>
        </template>

    5.  <if condition="<getopt-option-save/> is `true`">
        Call the `ase_config_set(key: "<key/>", val: "<val/>", scope:
        "project")` tool of the `ase` MCP server for the <key/>/<val/>
        pairs `project.task.effort.factor`/<fitted-factor/>,
        `project.task.effort.file`/<fitted-file/>, and
        `project.task.effort.line`/<fitted-line/>, and then only output
        the following <template/>:

        <template>
        ⧉ **ASE**: ⚙ config: `project.task.effort.{factor,file,line}` (scope: `project`): **<fitted-factor/>**, **<fitted-file/>**, **<fitted-line/>**, ▶ status: **rates saved**
        </template>
        </if>
        <else>
        Give the closing hint by expanding the following (which,
        depending on the configured <ase-guidance-level/>, may expand
        into nothing and hence emit no output at all):

        <ase-tpl-hint level="normal">
        Use `/ase-task-estimate --calibrate --save` to store the fitted rates, or alternatively `/ase-meta-config --scope project set project.task.effort.scale <bounds>` to adopt the suggested scale.
        </ase-tpl-hint>
        </else>

