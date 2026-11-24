---
name: file-server
description: Must invoke when presenting a file to the user. The CharlieBot server has a built-in file browser that serves any file on the host filesystem.
version: 1.1.0
---

# File Server

Share files and directories with the user by generating links to the CharlieBot file server. The
server serves any file on the host filesystem.

## URL Format

```
<base_url>/absolute_filepath/<absolute-path>
```

Where `<base_url>` is the CharlieBot URL resolved from HOST MEMORY (look for the **CharlieBot URL**
entry).

The path after `/absolute_filepath/` is the absolute filesystem path with its leading `/` removed.
The prefix names what has to follow it, so a path that dropped its leading segments reads as wrong
where it is written. This is the sole canonical prefix: the legacy `/files` and `/file` spellings
are unmounted and answer 404, so never write or repair a link onto them. The file server sits
behind the access key — an unauthenticated browser navigation gets the unlock form, not the file.

Examples:

| Filesystem path | URL |
|---|---|
| `/path/to/trace.json` | `<base_url>/absolute_filepath/path/to/trace.json` |
| `/path/to/results/` | `<base_url>/absolute_filepath/path/to/results/` |

## Publish Lane

Links that reach readers beyond the operator come from `charliebot publish <artifact-path>`: the
command copies the file to `<publish.dir>/<token>/<basename>` and prints the published URL,
`<publish.public_base_url>/<token>/<basename>`. The token is 22 random URL-safe characters, fresh
per publish, so publishing the same file twice gives two links and overwrites nothing. The host
serves the publish directory publicly, so anyone holding a link opens it, and a link cannot be
guessed from the page name. Publishing refuses unless `<publish.dir>/index.html` exists: without
it the host's static server would list the directory, and that listing would expose every link.

A host can publish through an external program in place of the publish directory. `publish.command` holds the program's argv. `charliebot publish <artifact-path> [-- <lane options>]` runs that argv with the artifact's absolute path and the lane options appended. The program prints the reader URL as its one line of stdout and exits 0. `charliebot publish` prints that URL. When the program exits non-zero, `charliebot publish` exits 1 and shows the program's stderr. The host skill that installs the program documents its lane options. A host configures one lane: `publish.command`, or the pair `publish.dir` and `publish.public_base_url`.

Share external reader links only through `charliebot publish`. Slack, Discord, and Feishu replies with a file-server
URL are refused with HTTP 422 naming the URL and publish command; those URLs remain for operator review and chat embeds.

## Behavior

- **File path**: returns the file for download (auto-detected MIME type)
- **Directory path**: returns an HTML directory listing with clickable entries

## When to Use

Whenever you need to present a file to the user (logs, traces, checkpoints, images, configs, and so
on), generate the URL instead of dumping file contents into chat. This is especially useful for:

- Large files (traces, logs, pickles)
- Binary files (images, model checkpoints)
- Directories the user may want to browse

## Rules

1. Share a generated file link only after `charliebot files probe` confirms HTTP 200 for that exact URL.
2. Present the link in markdown format: `[descriptive text](url)`
3. **If the file is a Perfetto/Chrome trace** (`.json` trace from training/profiling, or a directory
   of rank traces), ALWAYS also include a Perfetto viewer link alongside the file link. Read the
   `perfetto` skill for how to construct the viewer URL.

   Trace indicators: filename matches `trace_rank*.json` / `*trace*.json`, lives under a `trace/` or
   `profile/` dir, or the user called it a "trace"/"profile"/"perf capture".
4. Write a raw filesystem path as plain text, `path:line`, since the CharlieBot UI renders a markdown
   link around a raw local path as a dead link. The form to wrap in `[descriptive text](url)` is a
   file-server URL.
5. An artifact shared beyond the operator (a Slack post, a group report) ships comment-disabled: the
   comment tray belongs to the operator's own review flow.

## HTML Artifacts

Generated HTML artifacts (reports, plans, dashboards) must satisfy:

- Full document with doctype, html, body tags.
- Self-contained: inline CSS/JS. External resources from `cdn.jsdelivr.net` or
  `unpkg.com` only.
- Self-explanatory: a reader with no prior conversation or project background understands the page
  on its own, first read. The page's language follows the user's artifact-language preference; the
  templates stay English.
- Sandboxing: chat embeds render via srcdoc + sandbox attribute (no access to parent
  window, cookies, or storage). The plan panel viewer runs same-origin without sandbox
  because its in-frame comment tray requires same-origin; plan artifact content is
  trusted master-authored output.
- Aim for well-organized, visually polished pages that present information more densely
  than markdown allows. Multiple artifacts per response are supported.

### Cold-Read Gate

Pages of every genre pass the cold-read gate.
The gate has two parts: the genre's mechanical assertions and one cold read.
The PII scan keeps paths in workspace form and names people by role.

A waiting page (`prompts/web_reply.md`, Form) has the genre `waiting`.

- When you want a page's failures before the status set, run `charliebot artifact check <page-file> --genre <genre> --assertions-only`.
  A broken page then stops before the user opens it.
- The status set that links a page runs the fork assertions of its genre and refuses a broken page.
- The cold read of `charliebot web status set` reads the item together with its page.
- Count that cold read as the page's cold read, and start no second cold read for the page.
  Each Waiting on you item then takes one cold read.

Before you share a page or register a plan version, run the assertions:

    charliebot artifact check <page-file> --genre <genre> --assertions-only

When an assertion fails, fix the page and run the assertions again.
Plan registration runs the same assertions.
`charliebot artifact check` reports page height against the target in `prompts/master.md` under
"Explaining to the user" → "Length". An overage names folding as the fix, and an unmeasured result reports why.
Page height and measurement availability never block page sharing, plan registration, or `web status set`.
Apply the canonical Length contract when a gloss contributes to an overage.

The cold read is one model pass without context. It reads only the page and answers the eight questions in
`prompts/cold_read.md`.

Use the chat message that triggered the page. For a plan, use the understanding page's goal sentence verbatim; when
there is no understanding page, use the originating request.

Run a cold read after the Improve round and after every later `charliebot plan amend`. Run it in the same turn as verify
for a plan version. For other genres, finish it before or in the same turn as sharing.

A manager's cold read runs in a child session. After the child returns its result, end the turn; its report wakes the
manager. A worker's cold read runs in the foreground and prints the report. The report names the page path and SHA-256
of the page bytes read, each failed model attempt, the answering model, and the eight answers verbatim.

When a cold read fails, say so in the reply. When the page changes after the read starts, check every answer against
the current page.

Revise the page when any signal below appears:

- Answers 1, 2, or 3 differ from intent; answer 2 also signals when its epistemic state conflicts with page labels.
- Answer 4 names a section other than the first content section, or answer 6 answers no to any part of the trigger.
- Answer 7 lists terms, or answer 8 says `NOT STATED` for any part of a page reporting a run.
- On a plan or understanding page, answer 3 omits a decision requested from the reader.
- Answer 3 contains `FOLDED` or `NO DEMO`, or omits an option shown on a visible option line.
- An answer 5 re-read point names a `div.fork` decision fork in section 1, a jump between a fork and another section,
  a run, its variables, or a difference between compared legs.

Revise each genuine clarity gap and skip false positives on established project or domain terms. Revise the page in
place. For a plan, register the revision with `charliebot plan amend`. When verify runs, combine the cold-read revisions
and verify findings in one amend. Leave term-count tallies out of chat replies. A cold-read revision closes the gate and
gets no cold read.

The cold-reader instructions and the eight questions live in `prompts/cold_read.md`.

### Source Check

The Source Check covers every factual claim the user may rely on, including:
- a cause;
- a mechanism;
- a derived number, a sum, a ratio, or a difference that the page computes;
- a current system value, a count, a time, or a status that a system holds now.

It also checks the proposal premises in `source_check_spec.md` for every option and acceptance criterion.

The cold read judges readability, and the source check judges the facts.

- A plan page takes the verify round of the plan-approval skill in place of this check.
- An understanding page, a page with an open fork, or a page with a proposed option or acceptance criterion is shared
  only after a separate read-only fact-check worker checks it and the page author folds the findings into the page.
  Correct each claim or label it Open.
  When a premise fails, drop or rewrite the option or acceptance criterion and check the rewritten premises
  before sharing.
- Any other page is shared at once; the same worker starts its check in the turn that shares it, and the author corrects
  the page in place.
- `source_check_spec.md` in this skill's directory is the task spec for the fact-check worker.
