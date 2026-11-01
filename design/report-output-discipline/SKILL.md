---
name: report-output-discipline
version: "1.0.1"
user-invocable: false
description: "Report artifact output-format contract: decide the format by who consumes the artifact, not by which skill produces it — human-read reports get a derived HTML beside their Markdown source, machine-consumed artifacts stay Markdown/JSON, dual-read artifacts keep their own format (Markdown or JSON) as the single source. Holds the one product registry the whole library routes through and the one shared renderer hosts call instead of hand-writing HTML. Triggers — 「报告格式」「产物格式」「报告输出契约」「给人看的报告」「报告写 HTML」「HTML 报告」「机器看的写 Markdown」 / report output format, report artifact format, report HTML, derived HTML view. Do NOT use as a general Markdown-to-HTML converter, for concept explanations (explain-clearly owns those pages), or for queue acceptance views (goal-driven-queue owns those)."
---

# Report Output Discipline

> Shared discipline. Hosts declare it in frontmatter `dependencies` and load it before writing a report artifact. It owns the product registry and the renderer contract; hosts own their own report content.

## 1. Classify by consumer

Every registered artifact gets exactly one class. Evaluate in this order and stop at the first match:

| Order | Class | Evidence the registry must hold |
|---|---|---|
| 0 | Existing HTML-contract entry | The registry row's evidence starts with `既有契约` and names its read point |
| 1 | `machine` | A non-agent consumer reads **fields or protocol** — give the read point as `path:line` plus the field or protocol |
| 2 | `dual` | A named agent consumption point — a downstream workflow stage, or the host loading it at session start — recorded as `path:line` |
| 3 | `human` | Nothing above matched; this is the only default |

A read that only feeds rendering (reading the whole file to display it) does not make an artifact `machine`. The default is `human` because guessing `machine` silently removes the HTML obligation, and nothing downstream would catch that mistake.

## 2. Apply the format contract

- `human` + `接入` + not an exception → write the Markdown source **and** a derived HTML beside it. Markdown is the only editing entry; a hand-edited HTML is not an accepted change.
- `machine` → Markdown or JSON only. No HTML sibling.
- `dual` → the source stays in its own format (Markdown or JSON). No forced derivation step in a workflow stage; on-demand derivation is allowed but never required.
- Conversation-level conclusions — stage results, verification verdicts, review outcomes — stay in the conversation and get no file.

## 3. Render through the shared renderer

Generate the HTML with `scripts/render-core.mjs`, resolved from the directory this skill was installed into:

```
node <skill-dir>/scripts/render-core.mjs <source.md> [--root <dir>] [--at <iso>]
```

When `<skill-dir>` is unknown, ask the user where the skill is installed. When Node or the renderer is unavailable, print the Markdown path and state why — never hand-write HTML as a fallback.

The renderer behavior contract (escaping, link normalization, inline CSS, footer provenance, determinism) is defined once in the `report-output-format` capability. Do not restate it in a host.

Mermaid `flowchart` fences are pre-rendered to inline SVG. Graphs outside the supported subset, and unsupported diagram types, render as a visible degradation marker with the original source kept — never as a silent plain code block.

## 4. Suppress the derived HTML from the change set

Derived HTML must not enter version control, otherwise a pure document change gets classified as a UI change. The host ensures this when it writes the file: append a single ignore rule in the artifact's repository, or write into an already-ignored directory. Append only; never overwrite an existing rule. When the rule cannot be written, say so, give the exact line to add, still generate the HTML, and state that the UI-verification obligation still applies.

## 5. Tell the reader where the page is

After deriving HTML, report both paths in the conversation. Opening a browser is the host's own capability choice.

## 6. Registry is the only decision point

[reference.md](reference.md) holds the product registry: product, producing skill, class, consumer evidence, source format, derived format, path, suppression method, and integration status. Read the row; do not re-derive the class in prose. A new artifact is registered before it is integrated.

## 7. Keep hosts thin

A host body names its registry row and points here. It does not copy the classification table, the format rules, or the renderer contract.
