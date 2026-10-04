---
name: triage-work-item
description: >
  Triages a tracker work item, which is a bug, a task, or a story, end-to-end against the codebase.
  It reads the item with its full comment thread, links, and parent epic, cross-references related
  items, investigates the codebases behind the affected feature, corroborates with attached evidence
  and observability data, then posts a verified analysis comment back to the item. That comment gives
  the root cause for a bug, or the current behavior, the approach, and the effort for a change
  request. Ships with Jira and GitHub Issues tracker adapters, plus Grafana and CloudWatch
  observability adapters, and degrades to any reachable platform. Use when the user gives a
  work-item URL or key, on Jira (`…atlassian.net/browse/KEY`) or GitHub
  (`github.com/<o>/<r>/issues/<n>`), and asks to triage, investigate, diagnose, or root-cause it,
  even without the word "triage", as in "look into TICKET-123 and post what you find". Do not use it
  to read or summarize a work item with no code investigation, or to write new work items.
argument-hint: "<work-item URL or key> [--dry-run]"
allowed-tools: [Read, Grep, Bash, Agent, ToolSearch, AskUserQuestion, Write]
---

# Triage a tracker work item against the codebase and observability data

In this skill, "work item" is the generic term for whatever the tracker holds, which is a bug, a task, or a story. Jira and GitHub both call the object an "issue". The steps below keep that word when they name the concrete object, an API call, or a CLI call.

This is an investigation workflow, not a lookup. Its value over a plain read of the work item is a verified conclusion that a future engineer can act on immediately. Evidence that you checked backs that conclusion, and not a plausible-sounding guess. For a bug, that conclusion is a specific code path, configuration value, or data condition. For a change request, it is a validated approach and an effort estimate. Every step below exists either to gather that evidence, or to guard against reporting something that sounds right and is not.

The workflow is tool-agnostic. The tracker-specific and observability-specific mechanics live in adapter files under `references/`, and each one loads only when you reach the step that needs it. That keeps the always-loaded body focused on judgment. The judgment stays the same wherever the work item lives, and wherever the telemetry lives.

By default, post the comment once you have verified your findings. Do not pause for a separate approval step. Step 9 verifies the findings, and that verification is the safety gate rather than a human checkpoint. The one exception is `--dry-run`. When the user passes that flag, write the finished comment to a file and show it. Do the same when the user clearly wants to see the analysis before anything goes out.

## Inputs

- **Required**: an issue URL or key. With a bare key such as `PROJ-123`, you also need enough to identify the tracker and the instance. Ask when the context does not make it obvious. The context can be a prior message, a hostname already visible, or the repo you are standing in.
- **Optional**: which repos or codebases to investigate. When the user names none, see Step 5.
- **Optional**: `--dry-run`, which drafts the comment and never posts it.

## Step 1: Identify the tracker and load its adapter

Determine which tracker holds the issue, mainly from the shape of the URL:

- A `…atlassian.net/browse/<KEY>` URL, or a bare `PROJ-123` key, is Jira. Read `references/trackers/jira.md`.
- A `github.com/<owner>/<repo>/issues/<n>` URL is GitHub Issues. Read `references/trackers/github.md`.

The adapter file is the authority for the mechanics of that tracker. It covers how to load or authenticate its tools, and the exact call that fetches an issue with its full comment thread. It covers how to search related issues, and how to post a comment. It also covers the comment markup dialect and the known gotchas of that tracker. Read it now, and follow it wherever a later step says "per the tracker adapter".

When no adapter file exists for the tracker in front of you, degrade instead of stopping. Discover the relevant tools with a keyword `ToolSearch`, or with the platform's CLI or API. Make sure that the fetch, search, and comment operations you need exist, then proceed. Tell the user that you are running without a dedicated adapter, so they know that any citation of tool-specific behavior is best-effort. A run that goes well is a signal that the tracker earns its own adapter file.

## Step 2: Fetch the target issue in full

Use the fetch call from the tracker adapter. Retrieve the issue with its **entire** comment or discussion thread, in order, and not the description alone. A later comment frequently changes the picture. An issue gets reassigned between teams. A refinement discussion narrows down a fix approach. A "let us investigate X" comment is superseded a few comments later by "actually it is Y". The most recent comments carry the most current understanding, so do not anchor only on the original report.

Note the parent epic or tracking issue, and any linked issue, which can be a duplicate, a relates-to link, or a blocks link. You check these in Step 6, so do not chase them yet.

**List the attachments in the same pass**, even when nothing in the thread points at one. Capture the filename, the type, the size, and the upload date. An attachment is a first-party capture of the actual incident. It can be a HAR file, a log export, a crash dump, a screen recording, or a failing input file. Such a file routinely settles in one read what a code investigation can only narrow down. A default fetch often leaves attachments out. Some trackers hold them in a field that you have to request by name, and others hold them only as links inside the body text. So a response with no attachment data is not evidence that the issue has none. The tracker adapter covers how to list and download them.

**Trust the file list over what the thread says about it.** Prose goes stale, and the attachment list does not. A description that reads "waiting on the HAR file" describes the day someone wrote it. The file can have landed an hour later, with no edit to the description and no comment that announces it. Read the upload dates against the dates in the thread, instead of believing either one alone. An attachment that predates the discussion still asking for it is a common case, not a contradiction.

## Step 3: Classify the item and establish the comment template

Determine whether this item is a **bug** or a **change request**. In a bug, the actual behavior deviates from what the system is intended or documented to do. In a change request, the system does what it was built to do, and the desired behavior itself is changing. A change request also covers non-behavioral work, where no behavior is at stake either way. That work can be a refactor, a chore, tech debt, or a spike.

Use two signals together, and never the tracker's issue-type field alone:

- **The tracker issue type**, which is Bug against Story, Task, or Feature. Take it as a starting signal.
- **The content-level test.** Ask what the description and the comments say. They can say that the system fails to do what it is supposed to do, which is a promise that it breaks. They can instead say that the system must now do something different from what it was built to do. The first is a bug, and the second is a change request.

When the two signals disagree, **the content wins**. For example, the issue type reads "Story" or "Task", and the content describes broken existing behavior. Teams routinely misuse issue-type fields for workflow reasons. A team can file a regression as a "Task", and a "Story" can really mean "fix this". Treat the field as a hint, and not as the source of truth. Mention the override in the comment only when it is material to how you framed the investigation. Do not call out a trivial mismatch.

A non-behavioral task defaults to the change-request template. Effort and approach are exactly what such an item needs. Neither "root cause" nor "how it works today against what is wrong" fits a pure refactor cleanly enough to force the bug shape.

Some items are too sparse to classify with confidence, such as a one-line title with no description and no comments. Ask the user through `AskUserQuestion` instead of guessing. A wrong template choice compounds through the rest of the workflow.

Once you classify the item:

- For a **bug**, use `references/bug-template.md`.
- For a **change request**, including a non-behavioral task, use `references/change-request-template.md`.

Open the comment with an attribution line: `Triaged with 🤖 using <model> (<effort> effort)`. That line flags the comment as AI-assisted, so readers calibrate their trust and their scrutiny. Keep it, and never drop it to make the comment look more human. Always fill in `<model>`, because you know your own model name from your environment context, such as `Sonnet 5`. Fill in `(<effort> effort)` only when you have a concretely known effort or thinking-level setting for this session. Never guess one to fill the field. With no known setting, drop the whole parenthetical instead of writing a placeholder, which gives `Triaged with 🤖 using Sonnet 5:`. Use the literal Unicode 🤖, and not a `:robot:` shortcode. Some trackers do not expand shortcodes, as `references/trackers/jira.md` records for Jira, so a shortcode renders as literal text instead of an emoji.

## Step 4: Note the tracker's comment markup dialect

Different trackers render comments differently. Jira renders its own wiki and ADF markup, and its comment API accepts Markdown and converts it. GitHub renders GitHub-flavored Markdown. The tracker adapter states which dialect to write in, and how the post call expects it. Keep the dialect in mind while you draft in Step 10, so that code fences, headings, and links render instead of showing as literal characters.

## Step 5: Scope the codebases to investigate

When the user already named the repos, use them. Otherwise work out what is in scope before you guess blindly:

- Find out whether you are already working inside a relevant repo. Check the current directory, and check a workspace documented in a top-level `CLAUDE.md` or `README` that maps products and teams to repos.
- When the product area of the issue suggests a codebase that you can identify with reasonable confidence, say so and proceed. When the choice is genuinely ambiguous, ask the user. That happens in a multi-repo organization with no strong signal about which service owns this behavior. A question costs less than a long investigation on the wrong repo.

This step investigates a **local checkout**, through Read, Grep, and git. It calls no API of the git host, so it works the same whether the repo lives on GitHub, GitLab, or Bitbucket.

**Before you investigate, make sure that each repo is current.** These are local working copies that drift behind their remote in silence. A stale checkout does not fail loudly. It produces a *confidently wrong negative*: a subagent that searches a checkout missing the commit that implements the feature reports "no such code exists anywhere". That report reads exactly like a genuine gap, and it can send the whole investigation toward the wrong repo. For each repo in scope, do this before you dispatch the Step 7 agents against it:

- Run `git fetch origin && git log HEAD..origin/<default-branch> --oneline` to find out whether the checkout is behind.
- When the checkout is behind and `git status` shows a clean working tree, fast-forward it with `git pull --ff-only`.
- When local uncommitted changes exist that you do not want to disturb, leave the existing checkout alone. Investigate against a worktree of the fresh default branch instead. Use `git worktree add`, or the `EnterWorktree` tool when it is available. Do not stash someone else's work in progress.

## Step 6: Cross-reference related issues

Search for issues that can carry extra context. Search the siblings under the same parent epic or tracking issue, and run a keyword search on the summary. The exact search call, and the quirks of handling its results, live in the tracker adapter. Some trackers return a large result set that spills to a file and needs `jq` rather than a direct `Read`. Watch for two things, whatever the tracker:

- **A shared epic or a matching keyword is a lead, not a conclusion.** Read anything you find before you cite it. An issue commonly lives under the same epic as your target purely through product-area grouping, with no bearing on this specific bug. Treating it as related without reading it wastes the reader's time, and it can misdirect the fix.
- **Keep a large search payload out of your context.** When a search spills to a file, extract only `key`, `summary`, and `status`, through `jq` or a subagent. Scan those for candidates before you fetch anything in full.

This step and Step 7 do not depend on each other, so run them concurrently rather than back to back.

## Step 7: Investigate the codebase

Delegate this step to one or more background `Agent` calls, either Explore or general-purpose. Do not dig through the repo yourself inline. Delegation keeps your context focused on synthesis, and it lets you run this step in parallel with Step 6. See `references/investigation-subagent-prompt.md` for a full example of a prompt that gets good results. That prompt does three things. It briefs the agent on the user-visible symptom in plain terms. It names specific classes and patterns to look for, when you already hold hints, such as the service ownership of a related issue. It asks explicitly for file paths, line numbers, and actual code or configuration snippets, rather than summaries.

Here is what you want back, concretely:
- The full call path for the affected behavior, such as controller to service to data-access layer.
- Any configuration value that bounds the behavior, such as a timeout, a batch size, or a feature flag.
- **For a bug**: whether the current implementation has an evident gap that explains the symptom. The gap can be a missing check, a missing index, an unbounded query, or a race condition. Ask for more than "here is the relevant code". Ask for a stated hypothesis about *why* the code produces the reported symptom.
- **For a change request**: how the current implementation works today, which is the mechanism that the change must modify or extend, plus a candidate approach for making the change. The approach names what has to move, and it names any complicating factor, such as a data migration, backward compatibility, or affected callers.
- The git history and blame for recent, relevant changes. An issue number referenced in a commit message near the affected code is often the single best clue for why the current behavior exists.

When the feature spans a backend and a frontend, or several services, run one agent per codebase in parallel. Give each agent enough of the user-facing symptom to search usefully. Do not hand an agent a file path alone and hope.

## Step 8: Corroborate with runtime evidence

There are two sources, and they age in opposite ways: the files attached to the issue, and whatever the observability platform still retains.

**Take the attachments first.** Anything that Step 2 listed is a recording of the incident as it happened. Unlike a log backend, it never ages out. For an issue reported months ago, an attachment is often the only runtime evidence left. It frequently answers the question that a code read can only narrow. Mine it before Step 7, or alongside it, and not after. A decisive attachment reshapes the hypothesis that the code investigation is meant to test. Read it late, and you redo work that you already reasoned your way around. `references/attached-evidence.md` covers how to get these files without blowing up your context, and which fields carry the answer in the common formats.

### Observability data, when it will actually help

When no observability platform is configured or reachable, skip this part. The code investigation stands on its own. When a platform is available, its mechanics live in an observability adapter. That adapter covers the tools or CLI, how to pick a datasource, and the query languages for logs, metrics, and traces. Read `references/observability/grafana.md`, `references/observability/cloudwatch.md`, or the file that matches your platform. When no adapter exists for your platform, discover the tools with `ToolSearch` and proceed best-effort, the same way as in Step 1.

Before you query anything, check the age of the issue against your log and trace retention window. A hosted logging or tracing backend commonly retains 14 to 30 days. The adapter notes the platform's own default when that default is known. When the reported incident is older than the window, a log lookup almost certainly comes back empty, so skip it and save the round trip. The query is worth running only for a still-relevant or recurring issue, where current data can confirm or refute a hypothesis. Examples are an ongoing elevated error rate, and a currently slow endpoint that you can trace.

Treat this data as corroboration for a hypothesis that the code already gave you, and not as a starting point. You must already know what you are looking for before you query. For a change request, this data can also serve as baseline evidence for the "How it works today" section. It then confirms no failure hypothesis. The current latency and error-rate numbers are that kind of baseline.

## Step 9: Verify before you trust the investigation

This step keeps the analysis honest. A subagent's report is a *claim*, not a fact. It can misstate a line number or paraphrase code loosely. It can also miss that a configuration value it found is not the one wired up to this code path. Before you draft anything, do four things:

- Take the two or three highest-confidence claims that hold up your conclusion, and check each one yourself with `Read` or `grep` on the actual file. For a bug, those claims are the root cause, plus any configuration value that you cite. The root cause is the specific code that is missing or wrong. For a change request, they are your description of how the current behavior works, plus any claim about what the proposed approach requires. Confirm the line number, and confirm that the surrounding logic says what the report said.
- Give extra scrutiny to a *negative* claim, such as "this repo has no code related to X" or "no caller of this endpoint exists". The freshness check in Step 5 is exactly what guards against a false negative. When you skipped that check for this repo, run it now, before you accept the conclusion.
- When a claim does not hold up under inspection, do not drop it. Work out what is actually true, and adjust the conclusion. A confidently wrong root cause is worse than one that admits it is incomplete.
- Quote a code snippet, or cite a `file:line` reference, in the final comment only when you confirmed it in this step. Never relay an unverified snippet from a subagent.

## Step 10: Draft the analysis

Structure the comment per the template chosen in Step 3, which is `references/bug-template.md` or `references/change-request-template.md`, in the tracker's markup dialect from Step 4. The template is the authority for which sections the comment carries and what belongs in each one, so read it before you draft. Whatever headers you end up using, cover every section that the template marks as required.

### Keep it tight

A thorough investigation and a long comment are not the same thing. The lists above say what each section covers, and they do not say how much to write. It is easy to let the length of a section track how much you found instead of how much the reader needs. A few habits keep the comment proportional:

- **Cite the strongest evidence for a point once.** Sometimes git history, a doc, and a code comment all confirm one fact. An example is "this gap is deliberate, not a regression". Pick whichever one makes the point most directly, and leave the rest out. Three citations for one claim read as padding rather than rigor.
- **Name each file and line once.** Root cause, and How it works today, already name the files involved. A closing list of "files touched" then tells the reader something they already have.
- **Match depth to merit, not to symmetry.** When one option is clearly the pick, give it the fuller explanation. Dispatch a weaker alternative in one clause. Do not mirror the depth of the winner because the alternative is "Option B".
- **Show one snippet for a repeated gap.** The same issue sometimes shows up in more than one file. One missing check can sit in both a backend and a frontend. Verify and quote one of them, and cite the other by `file:line`. The reader can open it themselves.
- **Quote the shortest excerpt that carries the argument.** Trim a log trace, a request timeline, or a payload to the fields that do the work. Drop the rows that take no part. Six annotated lines that show a duplicated call and a dead redirect prove the point. The raw capture pasted in leaves the reader to re-derive it.
- **Describe an artifact or show it, and not both.** One sentence states what the error payload contains and how the code classifies it. The payload pasted underneath then adds length rather than proof. Include the artifact only when its shape is what the reader needs. That happens when they have to recognize it, match on it, or act on its exact contents.

A section can run long when the substance genuinely needs it. A root cause with several interacting factors needs the room, and so does a proposed approach with a real architectural fork. Even then, keep it to one tight paragraph, and do not break it into a bulleted sub-structure.

**The test before you post**: read the draft as the single message that you send to one colleague who has to act on this today. Cut every sentence that will not change what they do. The summary that you are about to give the user in the conversation is a good calibration. You write that version for someone who wants the point, and it is usually the right length and the right shape. When the ticket comment runs markedly longer than that summary, the excess is nearly always transcript rather than substance: evidence quoted twice, a conclusion restated as its own section, or the reasoning that got you there instead of the finding itself. Post the version that you want to read six months from now, and not the one that shows how much work it took.

**Posting a follow-up comment**: link or name the earlier comment, and give only what changed. That is the new evidence, plus which of your earlier conclusions it confirms, sharpens, or kills. Re-explaining the parts that still hold makes anyone who read the first comment pay twice, and it makes the delta harder to find. This differs from a correction, where the point *is* to be explicit about what was wrong, as Step 11 describes.

### Write it in plain English

The reader of this comment is often not the person who wrote the code, and sometimes not an engineer at all. Write short sentences in the active voice, define a term that such a reader can miss at its first use, and cut filler.

Keep every verified `file:line` citation, code snippet, and quoted log line exactly as it is. A reworded quote of an artifact is no longer evidence.

When you cite a commit, make it reachable. Derive the base URL of the repo from `git remote get-url origin`, and write the citation as a markdown link whose text a human can read, such as "the batch-size cap raised in abc1234". When the remote resolves to no web URL, write the short SHA plus the subject line of the commit, because the subject is the part that a human can act on. A tracker does not always turn a SHA into a link, and the tracker adapter records what this one does.

Where this pulls against the length test above, the length test wins. When a plain-English writing skill such as `simple-english` is available, invoke it and apply its rules to the draft, before Step 11 posts anything.

## Step 11: Post the comment, or hold it for a dry run

When the user requested `--dry-run`, write the finished comment to a file and report the path. Show the comment in the conversation instead of posting it. Call no post-comment operation.

Otherwise, post the comment now, through the comment call from the tracker adapter, in the markup that the tracker expects. Do not add a separate "must I post this?" checkpoint. Step 9 is what earns the right to post automatically.

**If you later discover that a comment you already posted was wrong**, post a new comment. That happens when the comment was built on a stale checkout, or when a claim did not survive re-verification. Say explicitly that it supersedes the previous one, and explain what changed and why. Never edit or delete the earlier comment in silence. Readers who already saw it need the correction to be visible. The trail of "here is what I thought, here is what was actually true" is itself useful signal.
