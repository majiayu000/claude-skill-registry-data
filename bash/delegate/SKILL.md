---
name: delegate
description: Hand ordinary implementation work to the Gemini CLI headless, then review what it actually wrote against the code graph. Use before launching gemini or judging its output.
---

# /delegate

Ordinary implementation work may be handed to the Gemini CLI on
`gemini-3.1-flash-lite` and reviewed afterwards. The loop is fixed.

For exploration, running builds or test you can also use gemini or
Sonet 5 sub-agent.

## Running it

1. **Clean tree first.** `git status --short` must be empty, on `main`. What
   `git diff` shows afterwards is then exactly what the delegate wrote.
2. **Run it headless**, task in a file to avoid quoting problems, and always
   with the workspace-trust variable exported:

   ```bash
   GEMINI_CLI_TRUST_WORKSPACE=true gemini -m gemini-3.1-flash-lite \
       --approval-mode yolo -p "$(cat task.txt)"
   ```

   `yolo` is required - a headless run has nobody to answer a prompt, and
   `auto_edit` stalls on the first shell command.

3. **The env var is not optional.** Without it the CLI first downgrades the mode
   ("Approval mode overridden to \"default\" because the current folder is not
   trusted") and then refuses to run at all: "Gemini CLI is not running in a
   trusted directory". Every headless run in an untrusted checkout dies there,
   before reading the task. `--skip-trust` is the flag-shaped equivalent;
   trusting the folder interactively does not carry into a headless run.
4. **The workspace is the only writable root.** An output path outside the repo
   - a session scratchpad under `/tmp`, for instance - is refused with "Path not
     in workspace" and the delegate quietly retargets the write to
     `~/.gemini/tmp/<project>/<name>`, reporting success. So either name an output
     file inside the repo, or read the result back from that fallback directory
     instead of concluding the run produced nothing.
5. **Re-index** from the dashboard, so the review reads a graph
   that matches the tree rather than the one from before the edit.

## What the task file must always carry

Do not commit or run any writing git command; the repository's language and
encoding policy; edits must pass `pre-commit run --files <paths>`; an
acceptance test the delegate has to check itself; and the name of any tree that
is off limits.

Give the delegate the facts already established rather than letting it
rediscover them - the free tier throttles by requests per minute, and every
wasted turn costs a minute of backoff.

Two failure modes seen repeatedly, worth pre-empting in the prompt:

- **A test that measured nothing.** Where the thing being changed runs from a
  container image, the source is baked in by `COPY`, so the edit does nothing
  until the image is rebuilt - in this repository, a change under
  `graphify/src/` needs `make -C graphify build`. A delegate that skips the
  rebuild is measuring the previous version.
- **A substituted acceptance criterion.** Asked for nodes in the graph, it
  answers with a file count, a log line, or a promise that they "should
  persist". Ask for the node list, and query it yourself regardless.

## Reviewing what it wrote

Opus 5 reviews, and it reviews the **actual changes** - never the delegate's own
summary, which is a claim rather than a result.

1. Take the real changes from `git diff`: the files, classes, defines, functions
   and parameters that actually moved.
2. For every changed entity, query the graph (`search_code_nodes`,
   `get_code_graph_neighbors`) for everything attached to it - callers, imports,
   includes, templates, data keys, whatever relations that language has - and
   check whether the change breaks any of them. Re-index first, or the sweep
   reads the tree as it was before the edit.
3. That impact sweep is exploration, so it runs on Sonnet 5. Sonnet gathers
   evidence; it does not rule.
4. The verdict - accept, fix on top, or revert - is Opus 5's alone, taken on the
   evidence gathered.

Then fix on top and commit with the `commit` skill. Local commit only; pushing
is the user's call.

## Recap

Say what was handed over, inside the recap the `enggraph` skill defines -
counts, not adjectives.

- **Delegations** - one line each: which model ran, what it was asked for,
  what came back.
- **Verdict** - accepted, fixed on top, or reverted, and on which evidence.
  The delegate's own summary is a claim, so cite the diff or the graph.
