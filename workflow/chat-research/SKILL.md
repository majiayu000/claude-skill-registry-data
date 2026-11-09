---
name: chat-research
description: Use when a web chat UI must answer research over CDP.
version: 1.0.0
author: TimeLine
license: MIT
platforms: [macos, linux]
metadata:
    hermes:
        tags: [cdp, research, chat-ui, composer, automation]
---

# Chat Research

Ask a web chat product a research question and read the answer back, from a browser this process
launched, with no human approving each submit. There is no API to call: the product is a UI, so the
workflow is a composer, a submit and a text read - and every step of it fails silently when it
fails.

This is not the way to act in a tab a person is using. Two debugger clients cannot share one tab, so
attaching detaches theirs, and a submit in their tab is approval-gated by design. This skill covers
the other case: a browser this process launched, or a tab it opened itself.

## When to use

- A research question must be answered by a web chat product and the answer read back as text,
  without a person approving each submit.
- The question is long-running and belongs in a background tab while other work continues.
- The answer is one input to a larger task and only its text is wanted.

Not for: acting in a person's attached tab, or reading a page that asks nothing of it - a plain page
read is a different procedure, and the browser transport skill covers the connection.

## The four steps

1. **Open** a background tab and keep its handle: `node .../cdp-open.mjs <url>`.
2. **Send**: `node .../cdp-send.mjs <ws-url> "<text>"`.
3. **Wait and read**: `node .../cdp-read.mjs <ws-url> --tail 3000`.
4. **Click a control** that has no label: `node .../cdp-click.mjs <ws-url> "css:<selector>"`.

Every command runs from the repository root, and `...` stands for
`Documentation/Skill/Chat-Research/Reference/`.

`cdp-open.mjs` creates the target with `background: true` and prints its `ws` handle beside the
page's title and the head of its text, so the handle a later step needs is the one the first step
reports. Every script takes that `webSocketDebuggerUrl` from `GET /json/list`, prints what it did,
and exits `2` with one `blocker:` line when it could not run.

The endpoint is `CDP`, default `http://127.0.0.1:9222`. Node 22 or newer: the scripts use the global
`WebSocket` and `fetch` and install nothing.

## Where a deep link replaces the composer

Where a site accepts the prompt in the URL, `Page.navigate` submits with no composer, no focus and
no editor events - the cheapest and the most reliable send there is:

```
https://<product>/search?q=<encodeURIComponent(prompt)>
```

One worked example, not the rule: `https://www.perplexity.ai/search?q=...` starts a new thread and
answers.

Whether a site does this is a fact about that site, not a CDP guarantee, so verify the outcome
rather than the navigation: a submitted prompt produces a thread URL and a new assistant turn, while
a prefilled one produces neither. Use the deep link for a fresh question; use the composer when the
question must land inside an existing thread or a project.

## Why a composer send needs three checks

`cdp-send.mjs` runs the sequence in the order that survives a real editor, and each step exists
because the step before it fails silently:

1. **Click the composer with real pointer input.** `el.click()` is ignored by an editor that listens
   on the pointer pipeline, so the script measures the element and dispatches `mousePressed` and
   `mouseReleased` through the `Input` domain.
2. **Select all, then `Input.insertText`.** `insertText` types at the caret, so a leftover draft is
   concatenated rather than replaced, and the question that gets sent is two questions.
3. **Click Submit, then check that the composer emptied.** A click that lands on a wrapper does
   nothing and reports nothing. When the text is still there, the script dispatches `Enter` - the
   submit path every chat composer implements - and checks again.

The report is `sent: true` only when the composer is empty. A submit that is believed rather than
checked is how one prompt gets sent twice.

The visible composer is not the first one in DOM order: a panel or a dialog leaves a hidden editor
earlier in the tree, and a send that types into it reports `typed: ""` and reads as a dead page. The
script filters on a non-zero rect for that reason.

Submit is found by its accessible name, `submit`. A product that names the control differently needs
that line changed, and until it is, the run stops on a `blocker:` naming the disabled control rather
than clicking a dead button and reporting success.

## The output contract the prompt must carry

The question is asked in full, and the model structures its own reply. The reasoning, the caveats
and the part it could not establish are what make a research answer worth having, and a shape
demanded up front discards them first: a model told to answer in a fixed number of short lines drops
the qualifier before it drops the finding. Constrain only what the reader cannot consume, and leave
the rest to the model.

Two exceptions, each with a reason of its own:

- **Status extraction** - a verdict the caller acts on mechanically (triage, pass/fail per item, one
  row per issue) may name the shape, because that answer is meant to be parsed rather than read.
- **Wide markdown tables** - the answer arrives as `document.body.innerText` or an accessibility
  tree, and a five-column table flattens into fragments that cannot be reassembled. The constraint
  is on the table, not on the length: rule out the wide table and leave the answer as long as it
  needs to be.

A terminal marker is worth asking for only when the answer streams and completion must be known.
`cdp-read.mjs --stable 3` already polls `document.body.innerText` until it stops changing, which
costs the model nothing; a marker asked on top of that costs it a line and buys nothing. Never sleep
a fixed time in either case: a fixed sleep returns whatever the network happened to deliver, which
is a partial answer that reads as a whole one.

## Mode and model are part of the question

A research product usually offers a search mode and an agent mode, and the two answer differently:
search reads sources and quotes them, an agent browses and acts. The mode is therefore part of the
question, not a preference.

A session started from a project can inherit the project's default mode, which silently overrides
the toggle that was set before typing. Assert the composer's own controls before sending:

```js
[...document.querySelectorAll("[aria-pressed]")].map((Control) => ({
	label: Control.getAttribute("aria-label"),
	pressed: Control.getAttribute("aria-pressed"),
}));
```

`aria-pressed` is the mode the composer will actually use; the label is the model that will answer.
Read both, assert both, and name them in the report - an answer from the wrong mode is a different
answer, and a reader who is not told which one produced it cannot tell. A product that scopes its
composer controls behind an attribute of its own needs the query scoped to the composer element; the
attribute a toggle carries is `aria-pressed` everywhere, the wrapper is not.

A project's defaults live behind its own settings route, so the composer can show one mode before
typing and the session use another. Check both, and report the mode that answered rather than the
mode that was asked for.

## Reading a project-scoped thread

A session started from a project page's composer is filed in that project even though the thread's
own URL is the ordinary `/search/<id>` form. The project URL and the thread URL therefore disagree,
and neither is wrong: the project owns membership and instructions, the thread owns the transcript.
Read the thread URL when the text is wanted, and the project URL when the next question must land in
the same place.

## The scripts' failure discipline

Each of the four scripts exits `2` with one `blocker:` line when it cannot run - no endpoint, a dead
tab, no composer, a submit control that never enabled, no text, no control with that label - and
exits `1` only when it ran to the end and its claim did not hold (the composer still held the text
after both submit paths). Never a stack trace: the caller reads an exit code and one reason, and a
trace is a wall between the two.

A `blocker:` line names what stopped the run, and where there is one the command that fixes it,
because a missing browser is not the site's fault. It never reports a defect in the page that the
page did not commit, and it is never a silent no-op: a click that found nothing prints the label it
searched for and the reason it found nothing.

## Beyond the answer text

Two things a capture needs that are not the answer's prose.

**The trace.** An answer renders its work as nested collapsible steps, and that nesting is how the
answer was reached - it is not in the text, so a capture that keeps only the prose loses the
argument. `cdp-trace.mjs` reads the nesting the DOM states and writes one JSON line per step with
`id` and `parent`, plus one line per source; depth is a consequence of nesting, never an input to
it. A collapsed step has no rendered children, so `--expand` clicks the closed headers and repeats
until a pass opens nothing - a click is not an opening, and the count of headers still shut is the
only progress signal. `--selftest` parses the page-side scripts without a browser, and
`--fixture <file.json>` feeds the shape the page returns through the serialiser, which is how the
tree is tested off-page.

**The feed.** A question about a body of code is answered better with the code attached than pasted,
and the composer takes files through an `<input type="file" multiple>` that is usually hidden.
`bundle.mjs` turns a directory into deterministic batches with a manifest, `attach.mjs` sets them on
the input with `DOM.setFileInputFiles` - a click cannot, because the input is hidden and the page's
handler is a React `onChange` - and `observe.mjs` reports what changed afterwards, so the run knows
the page settled instead of sleeping a fixed time. Each one reports what the page actually took:
attaching fewer files than were named is exit `1`, not a success.

## Pitfalls

- **Never click a suggestion chip that carries a mode badge.** Under an answer a product offers
  follow-ups it will run itself, and the ones badged with an agent or a computer-use badge start
  that mode: a browsing agent that acts instead of a search that reads. The badge is the tell. Type
  the follow-up into the composer with the mode asserted, and click only a plain suggestion whose
  mode is the one wanted.
- **A settings dialog is a route, not a modal.** Saving navigates the URL and can leave the panel
  open over the composer, where a click lands on the panel. Close it by its own control
  (`Close settings`) before typing.
- **A menu opened by `el.click()` may not open.** Some menus need a real pointer press: use
  `cdp-click.mjs` with the accessible label. The converse also holds - a switch toggles with
  `el.click()` and ignores a coordinate click that lands on its knob - so try the labelled click,
  then the synthetic one, and read the state back after each.
- **A streaming thread re-renders the tab.** A target id survives a navigation inside the page but
  not a new document: re-list `/json/list` and take the new `webSocketDebuggerUrl` instead of
  reusing a dead one.
- **A control with no accessible label needs a selector.** `css:<selector>` is the path for a
  switch, a canvas or a row that no label match reaches; a zero rect is reported rather than
  clicked.
- **Never attach to a tab a person is using.** Two debugger clients cannot share one tab, and
  attaching detaches theirs.

## Claim → test

| Claim                                       | Test                                                                                                   |
| ------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| A background tab can be opened and read     | `node .../cdp-open.mjs <url>` prints a `ws` handle and `chars > 0`                                     |
| A composer send is verified, not assumed    | `node .../cdp-send.mjs <ws> "probe"` prints `sent: true` and exits 0                                   |
| A leftover draft is replaced, not appended  | send twice with different text: the second read shows only the second text                             |
| A dead tab is a blocker, not a stack trace  | `node .../cdp-send.mjs ws://127.0.0.1:9/x "probe"` exits 2 with `blocker:`                             |
| The prompt is the question, not a shape     | the prompt text names no line count and rules out only a wide table                                    |
| The read waits for the answer to finish     | `node .../cdp-read.mjs <ws> --stable 3` returns once the text stops changing, with no marker asked for |
| The mode and model are known before sending | the composer's `aria-pressed` mode and model label are read and reported                               |
| A control with no label is clickable        | `node .../cdp-click.mjs <ws> "css:<selector>"` prints `clicked` with a point                           |
| TeX survives the capture                    | `node .../cdp-extract.mjs <ws>` on a page with maths prints `formulas: N` and `$…$` in the body        |
| A stub is refused, not returned             | `node .../cdp-extract.mjs <ws> --min-chars 5000` exits 1 with `refusing a stub`                        |
| The trace keeps the tree, not a depth       | `node .../cdp-trace.mjs --fixture <file>` prints `id`/`parent` on every line, exit 0                   |
| A batch is deterministic                    | `node .../bundle.mjs <root> --out <dir>` twice leaves `batch-NN.txt` byte-identical                    |

## References

| File              | Covers                                                               |
| ----------------- | -------------------------------------------------------------------- |
| `cdp-open.mjs`    | Create a background target, navigate, report handle, title and text  |
| `cdp-send.mjs`    | Click the visible composer, replace its text, submit, verify emptied |
| `cdp-click.mjs`   | Click by accessible label or `css:` selector with pointer events     |
| `cdp-read.mjs`    | Poll `innerText` until it stops changing, then print a tail          |
| `cdp-extract.mjs` | Serialise the rendered answer to Markdown, TeX and code intact       |
| `research.mjs`    | Resolve a thread id to its page target, then capture it              |
| `cdp-trace.mjs`   | Read the step tree as JSON lines with `id`/`parent`                  |
| `observe.mjs`     | Watch the page after a send and print each change                    |
| `bundle.mjs`      | Turn a directory into deterministic batches a composer takes         |
| `attach.mjs`      | Set files on the composer hidden input and verify                    |
