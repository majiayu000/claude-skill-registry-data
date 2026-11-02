---
name: execute
description: Reactant router — read a document, interpret its <@skill> annotations in context, and execute every actionable tag sequentially from top to bottom, re-reading after each one. Use when the user asks to execute, run, or process Reactant tags in a file.
---

# Execute

Execute every actionable Reactant annotation in one document, one tag at a
time, in source order. The host agent is the parser: read and interpret the
document directly. Do not call or rely on a programmatic tag scanner, parser,
AST, or dispatch classifier.

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
/execute <file>
```

Resolve a relative file path against the current working directory.

## Annotation Interpretation

Reactant annotations normally look like `<@skill-name>` or
`<@skill-name: prompt>`. Natural-language prompts may wrap across lines. Use
the whole document, its structure, and surrounding prose to decide whether an
apparent tag is an actionable instruction.

- `<@comment: ...>` is human-readable data: preserve it and never dispatch it.
- A paired `<@chat-model name="..."> ... </@chat-model>` block is model-response
  data. Treat its payload as opaque conversation content even if it contains
  apparent tags.
- A `chat-user` already followed by its `chat-model` response is answered and
  remains as chat history; do not dispatch it again.
- Tags shown as documentation, quoted examples, or code samples are normally
  literal examples, not instructions. A leading backslash may explicitly mark
  an example, but examples do not require an escape character. Use context.
- `execute`, `execute-one`, and `skill-generator` are entry skills, not inline
  operations. Preserve and report an apparent annotation using any of those
  names; never dispatch it.
- Leave ambiguous or malformed-looking text unchanged and report it instead
  of guessing. Leave unknown skill tags unchanged and warn the user.

## Skill Discovery

For the selected annotation, find the matching Agent Skill in this order:

1. `<project-root>/.reactant/skills/<name>/SKILL.md`.
2. Skill roots listed in `<project-root>/.reactant/config.json`, in order.
3. The bundled Reactant skills available in the current host/install.

Project-local skills may shadow ordinary bundled skills. They may not shadow
the reserved names `execute`, `execute-one`, `skill-generator`, `chat-user`,
`resolve`, `chat-model`, or `comment`. If discovery is ambiguous, do not
dispatch; report the collision. Adding a valid project-local skill requires no
registry edit.

## Workflow

1. Read the entire current file.
2. Interpret the document and select the first actionable Reactant annotation
   in source order using the rules above. If none remains, report the summary
   and stop.
3. Discover and read the matching `SKILL.md`. This exact router selection is
   the only authorization to activate that tag-only worker. Follow its
   protocol for this one annotation only. Use an isolated subagent if the host
   provides one and doing so is appropriate; otherwise perform the protocol
   directly.
4. Give the selected skill the absolute document path, project root, exact raw
   annotation, interpreted skill name and prompt, surrounding authored block,
   relevant scope modifiers, ordered chat chain when applicable, context
   references, and full-file access for broader context.
5. Accept the skill result as produced. Do not add a second model pass, grade,
   fact-check, automatically retry, or semantically verify it.
6. If the skill succeeds, re-read and reinterpret the entire current file,
   then repeat from step 2. Earlier work may move, add, answer, or remove later
   annotations.
7. If the skill fails or a needed capability is unavailable, leave its tag in
   place, stop immediately, and do not execute later tags.
8. Report a brief summary of executed tags, any failure, unknown tags, and
   skipped comments/chat history/literal examples.

## Rules

- Always choose the next instruction from a fresh reading of the current file;
  never batch or reorder annotations.
- Preserve unrelated annotations, comments, chat-model blocks, answered chat
  turns, and literal examples byte-for-byte unless the selected skill is
  explicitly defined to consume that exact content.
- If several actionable annotations share a block, the first skill may edit
  the authored prose but must leave later annotations available for the next
  pass.
- One dispatched failure stops this run.
- Never re-dispatch an annotation that a completed dispatch left unchanged:
  if a worker reports success but the document is unchanged and the same
  annotation is still actionable (a no-op), stop and report it instead of
  selecting the same annotation again. This rule applies with and without
  transactional history.
- The router itself does not edit `.reactant/`; only a selected skill that is
  explicitly responsible for project-local skills, or the transaction kernel,
  may do so.

## Transactional History

A project may record authoring history. Before the first dispatch, look for
`.reactant/config.json` at or above the document's directory. If it exists
and contains a `"repository_id"` field, history is enabled and EVERY dispatch
must be wrapped in a kernel transaction as described below. If the file is
absent or has no `repository_id`, dispatch exactly as described above,
editing the real file directly — no history is recorded.

The kernel ships with the optional `reactant` Python developer package. When
history is enabled but `python3 -m reactant version` fails, do not dispatch:
report that this project has history enabled but the kernel is unavailable,
and let the user either install the package or decide to proceed without
history by saying so explicitly.

Wrap each selected annotation like this:

1. Open the transaction, passing your selection as JSON on stdin:

   ```
   python3 -m reactant tx-begin --project "<project-root>" --json-file - <<'EOF'
   {"invocation": "execute",
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

   Then stop this run as usual; the unresolved tag remains in the real file.

5. Act on the commit reply's `"status"` — there are three outcomes, not two:
   - `"success"`: the staged result is installed in the real project and
     recorded. Re-read the REAL file and continue with the next annotation.
   - `"no-op"`: the worker completed but produced NO staged change, so the
     selected annotation is still present and would be re-selected on the
     next pass. Stop this run immediately: report that the worker made no
     change, leave the tag in place, and do not retry it in this
     invocation. Never loop on a no-op.
   - `"failed"` (for example, the real project changed while the
     transaction was open): stop and show the user the error summary.

Open transactions are serialized: never begin a second transaction before the
first is committed or failed.
