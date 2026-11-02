---
name: execute-one
description: Reactant router — read a document, interpret its annotations in context, and execute only the first actionable <@skill> tag. Use when the user wants to step through Reactant tags one at a time.
---

# Execute One

Execute exactly one Reactant annotation: the first actionable tag in source
order. The host agent is the parser. Do not call or rely on a programmatic tag
scanner, parser, AST, or dispatch classifier.

## Entry and Dispatch Boundary

Reactant has three direct entry skills: `execute`, `execute-one`, and
`skill-generator`. The first two are document routers. `skill-generator` is a
direct project-authoring utility, has no inline tag form, and is never
dispatched by a router. All remaining Reactant skills are tag-only workers.
Invoke a worker only after this router has selected its exact actionable
annotation from the target document. Never invoke a worker because ordinary
chat, authored prose, or another skill merely resembles its capability.

## Usage

```
/execute-one <file>
```

Resolve a relative file path against the current working directory.

## Annotation Interpretation

Read the whole document and use its structure and meaning to interpret
`<@skill-name>` / `<@skill-name: prompt>` annotations. Prompts may wrap across
lines.

- Skip `<@comment: ...>` and paired `<@chat-model>` response data.
- Skip a `chat-user` turn already followed by its model response.
- Do not execute tags that are being shown as documentation, quoted examples,
  or code samples. A leading backslash is an optional explicit hint, not a
  required escape grammar.
- Leave ambiguous, malformed-looking, and unknown tags unchanged; report them
  instead of guessing.
- `execute`, `execute-one`, and `skill-generator` are entry skills, not inline
  operations. Preserve and report an apparent annotation using any of those
  names; never dispatch it.

## Skill Discovery

For the selected annotation, look for the matching `SKILL.md` in project-local
`.reactant/skills/`, configured `skill_roots` in order, and then the bundled
Reactant skills available in the current host/install. Project-local skills
may not shadow `execute`, `execute-one`, `skill-generator`, `chat-user`,
`resolve`, `chat-model`, or `comment`. Report ambiguous collisions and do not
dispatch them.

## Workflow

1. Read the entire current file.
2. Interpret it and select the first actionable Reactant annotation in source
   order. If none remains, report that and stop.
3. Discover and read the matching `SKILL.md`. This exact router selection is
   the only authorization to activate that tag-only worker. Follow it for this
   one tag only. Use an isolated subagent if the host provides one and it is
   appropriate; otherwise perform the protocol directly.
4. Supply the absolute document path, project root, exact raw annotation,
   interpreted name/prompt, surrounding authored block, modifiers, relevant
   chat chain and context references, plus full-file access.
5. Accept the result as produced without a second model pass, grading,
   fact-checking, automatic retry, or semantic verification.
6. Report the result. On failure, leave the tag in place. In every case stop
   after this one dispatch; never attempt a second tag.

## Rules

- Exactly one dispatch per invocation. Repeated `/execute-one` calls advance
  through the document one annotation at a time.
- Preserve unrelated annotations, comments, chat-model blocks, answered chat
  turns, and literal examples byte-for-byte unless the selected skill is
  explicitly defined to consume that exact content.
- The router itself does not edit `.reactant/`; only a selected skill that is
  explicitly responsible for project-local skills, or the transaction kernel,
  may do so.

## Transactional History

A project may record authoring history. Before dispatching, look for
`.reactant/config.json` at or above the document's directory. If it exists
and contains a `"repository_id"` field, history is enabled and the single
dispatch must be wrapped in a kernel transaction. If the file is absent or
has no `repository_id`, dispatch exactly as described above, editing the real
file directly — no history is recorded.

The kernel ships with the optional `reactant` Python developer package. When
history is enabled but `python3 -m reactant version` fails, do not dispatch:
report that this project has history enabled but the kernel is unavailable,
and let the user either install the package or decide to proceed without
history by saying so explicitly.

Wrap the one selected annotation like this:

1. Open the transaction, passing your selection as JSON on stdin:

   ```
   python3 -m reactant tx-begin --project "<project-root>" --json-file - <<'EOF'
   {"invocation": "execute-one",
    "document": "<target document path>",
    "tag": {"raw": "<annotation text copied exactly from the document>",
            "name": "<interpreted skill name>",
            "prompt": "<interpreted prompt, or omit>"},
    "skill": {"name": "<skill name>", "path": "<selected skill directory>"},
    "agent": {"host": "<host product name>", "model_name": "<exact model id, or omit>"},
    "context_inputs": ["<double-backtick input paths, if any>"],
    "observed_annotations": [{"kind": "comment", "name": "comment",
                              "raw": "<@comment: copied exactly>"}]}
   EOF
   ```

   `tag.raw` must be an exact copy of the selected annotation text. If that
   exact text occurs more than once in the document, add
   `"char_start": <0-based character offset>` so the range is unambiguous.
   `observed_annotations` is optional but valuable: report the
   annotation-layer content you noticed while interpreting the document —
   `<@comment: ...>` tags and other non-executable data — copied exactly,
   so provenance can exclude those words from authored text. The same
   more-than-once rule applies (`char_start` per entry). Relative
   `context_inputs` paths resolve from the document's directory. The kernel
   only verifies mechanically that each range matches your raw text;
   selecting and interpreting annotations remains your judgment. If
   tx-begin reports an error (for example another transaction is still
   open), resolve it as the message directs before dispatching.

2. The reply contains `staged_project_root` and `staged_document_path`. Give
   the worker skill the STAGED document path and STAGED project root instead
   of the real ones. During the transaction, neither you nor the worker may
   modify the real project — a real-project change is detected at commit and
   fails the transaction.

3. When the worker completes successfully:

   ```
   python3 -m reactant tx-commit <transaction-id> --project "<project-root>"
   ```

   If the worker added new annotation-layer content — for example the
   `<@chat-model>` response block appended by `chat-user` — report it in the
   commit so provenance can exclude it from authored prose: pass
   `--json-file -` with
   `{"produced_annotations": [{"kind": "chat-model", "name": "chat-model",
   "raw": "<inserted block text copied exactly>", "path": "<file it is in>"}]}`.
   The `path` is relative to the staged project root and must name a file
   this transaction changed. If the exact raw text occurs more than once in
   that file, add `"char_start"` for the entry, as with the tag.

4. When the worker fails or a needed capability is unavailable:

   ```
   python3 -m reactant tx-fail <transaction-id> --project "<project-root>" --error "<short summary>"
   ```

   The unresolved tag remains in the real file; report the failure and stop.

5. Act on the commit reply's `"status"` — there are three outcomes, not two:
   - `"success"`: the staged result is installed in the real project and
     recorded; report the consumed annotation.
   - `"no-op"`: the worker completed but produced NO staged change; report
     explicitly that the annotation was dispatched but not consumed and
     remains in the document — never describe a no-op as a successful
     consumption.
   - `"failed"`: show the user the error summary.
   In every case stop after this one dispatch — never attempt a second tag.

Open transactions are serialized: never begin a transaction while another one
is open.
