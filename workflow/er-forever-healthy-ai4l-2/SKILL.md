---
name: er
description: AI4L - Main Skill for Evidence Review Creation and Auditing using @AGENTS
version: 2.0.2
---

# AI4L - Main Skill for Evidence Review Creation and Auditing using @AGENTS

## General Rules

* Parse the user's input to determine which sub-command to execute
* Set [args] to $ARGUMENTS

* Note the [start_time] when beginning any command, and report the [time_taken] when done

* All generated results go in [creation_dir] as .md files
* Do not edit or modify any files outside [creation_dir]


* Full lines formatted as `line` comments must be ignored when processing commands.


## Resolving the target ER

* If no [args] are given, set [target_er] to the newest _ER.md file in [creation_dir]
* Otherwise, if [args] names an existing _ER.md file in [creation_dir] (with or without the directory), set [target_er] to that file's bare filename, without any directory
* Otherwise treat [args] as an intervention: list the _ER.md files in [creation_dir] whose filename starts with [args] converted the way 6.25 of [er_prompt] converts short_topic (lowercase, spaces and dashes to underscores, other characters removed), and set [target_er] to the newest of them by the date in the filename
* If nothing matches, report `No ER found for: [args]` and exit


## COMMAND: create {topic}

`Create an evidence review (ER) using the @er-creator agent.`

* If no [args] are given {
  * Report: `usage: /er create {topic}`
  * exit
} otherwise {
  set [topic] to [args]
}

* Report: `create: [topic]`

* @er-creator: `[topic]`
* Wait until the agent finishes

* Report: `filename: [filename]`


## COMMAND: audit {er}

`Audit an ER using the @er-auditor agent.`

* Resolve [target_er] from [args] (see "Resolving the target ER")

* Report: `audit: [target_er]`

* @er-auditor: `[target_er]`
* Wait until the agent finishes and returns the result

* Report: `target_er: [target_er]`
* Report: `pass_rate: [pass_rate]`
* Report: `audit_filename: [audit_filename]`


## COMMAND: fix {er}

`Audit and fix an ER using the @er-fixer agent.`

* Resolve [target_er] from [args] (see "Resolving the target ER")

* Report: `fix: [target_er]`

* @er-fixer: `[target_er]`
* Wait until the agent finishes and returns the result

* Report: `target_er: [target_er]`
* Report: `pass_rate: [pass_rate]`
* Report: `audit_filename: [audit_filename]`


## COMMAND: combine {er}

`Create a final _ER_QA.md file from all audits`

* Resolve [target_er] from [args] (see "Resolving the target ER")

* Report: `combine: [target_er]`

* @er-combiner: `[target_er]`
* Wait until the agent finishes and returns the result
* Set [new_qa_filename] to the filename the agent returns in its `QA file:` line

* Report `QA file: [new_qa_filename]`

## COMMAND: iterate {er}

`Loops audit/fix cycles up to [max_audits] times until [needed_passes] show 100% pass rate.`

* Resolve [target_er] from [args] (see "Resolving the target ER")

* Report: `iterate: [target_er]`

Initialize {
  * Set [iteration] = 0, [consecutive_passes] = 0
}

Loop while [iteration] < [max_audits] and [consecutive_passes] < [needed_passes]
{
  * @er-fixer: `[target_er]`
  * Wait until the agent finishes and returns the result

  * If the [pass_rate] is 100%, increment [consecutive_passes]; otherwise reset to 0
  * Increment [iteration]

  * Report: "Iteration [iteration]: Pass rate = [pass_rate] ([consecutive_passes]/[needed_passes] consecutive passes needed)"
}

* @er-combiner: `[target_er]`
* Wait until the agent finishes and returns the result
* Set [new_qa_filename] to the filename the agent returns in its `QA file:` line

* Report `QA file: [new_qa_filename]`

If [consecutive_passes] >= [needed_passes] {
  * Return: `status: success`
} else {
  * Return: `status: failed`
}

* Return: `target_er:  [target_er]`
* Return: `iterations: [iteration]`


## COMMAND: full {topic}

`A create and multi-pass audit workflow.`

* If no [args] are given {
  * Report: `usage: /er full {topic}`
  * exit
}

* Execute the "create" command
* Execute the "iterate" command with [filename] returned by "create" as [args]

## COMMAND: compare {intervention}

`Compares all ERs for a given intervention, typically from different AI models or versions, to determine which is strongest based on content quality and the latest QA audit results.`

* If no [args] are given {
  * Set [intervention] to intervention in the frontmatter of the newest ER in [creation_dir]
} else {
  * Set [intervention] to [args]
}

* Report: `compare: [intervention]`

* Compare all ERs in [creation_dir] with a similar [intervention] in their frontmatter
  * Compare the quality of the content
  * Be detailed
  * Take into account the latest "_ER_QA.md" for each.

* Present a clear recommendation of which ER is strongest and why.
