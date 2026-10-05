---
name: codexqa-code-wiki
description: >
  Builds a local architecture wiki for a repository from the CodexQA symbol
  graph (no model needed): modules, who calls whom and how often, reading
  paths, and one self-contained HTML page. Use when the user mentions
  codexqa-code-wiki, code-wiki, wiki, knowledge graph, architecture wiki,
  module map, reading guide, 代码知识图谱, 架构 Wiki, 模块地图, 阅读导览,
  wiki inputs, --no-llm, community detection, 社区检测, HTML 报告, or asks
  to map modules / generate a repo wiki without an LLM. Not change review
  (that is codexqa-code-analyzer), not CodexQA evidence-pack HTML review
  (that is codexqa-code-reviewer), and not SAST+agent code-risk scan reports
  (that is codexqa-defect-analyzer). Former skill name: code-wiki.
license: Apache-2.0
compatibility: >
  Requires Node.js >= 18 and the `codexqa` CLI
  (`npm i -g @openqa-cn/codexqa`) on PATH. Index and `wiki inputs` need no
  LLM. Data lives in ~/.codexqa/.
metadata:
  author: open-source
  version: "2.0.0"
  open-standard: agentskills
---

# Code Wiki

Three commands, one file to write:

```text
node <skill>/scripts/wiki.mjs brief <repo>   # index + export facts + print the brief
  → you write .codexqa-wiki/<repo>/notes.json  # names and sentences only
node <skill>/scripts/wiki.mjs build <repo>   # validate + render one HTML file
```

The script owns every fact on the page: modules, sizes, call counts, groups,
the architecture diagram, public symbols, files, links, search. You own the
words: what the repo is, what each module does, and which reading path fits
which task. You never edit HTML, CSS, or diagrams.

`<skill>` is this skill's directory. `<repo>` is a local checkout (preferred).
`README.md` / `README.zh-CN.md` are for humans; do not load them.

## Documents (load on demand)

| File | Load when |
|---|---|
| `SKILL.md` (this file) | always |
| [references/notes.md](references/notes.md) | before writing `notes.json` |
| [references/playbook.md](references/playbook.md) | one module only, index problems, persisting for the Web UI |
| [references/cli.md](references/cli.md) | `codexqa` missing, PATH, repo ids, maintenance |

## Default flow

1. **Brief.** Run `node <skill>/scripts/wiki.mjs brief <repo>`. It indexes
   incrementally, exports `codexqa wiki inputs`, and writes
   `.codexqa-wiki/<repo>/` with `inputs.json`, `meta.json`, `brief.md`, and a
   `notes.json` scaffold (kept if it already exists). Read the printed brief:
   groups, suggested paths, and per module its files, calls, callers, public
   symbols, and key flows.
2. **Notes.** Read [references/notes.md](references/notes.md), then fill
   `notes.json`. Every `P01`-style id and group id in it must exist in the
   brief. Write 简体中文 unless the user asked for English (`"lang": "en"`).
3. **Build.** Run `node <skill>/scripts/wiki.mjs build <repo>`. If it prints
   `error:` lines, fix those fields and rerun; they name the field and the fix.
   `check <repo>` validates without writing HTML.
4. **Deliver.** Tell the user the printed file path plus two or three lines on
   what the wiki says. Do not paste the HTML or open it in chat.

The user only wants a quick look → `build <repo> --draft` right after
`brief`. The page uses rule-based names and says it is a draft. Offer to
write the notes afterwards.

Useful flags: `brief --limit 8` (large repos), `brief --lang en`,
`brief --skip-index` (index is fresh), `build --out FILE`,
`build --source-url 'https://host/repo/blob/{commit}/{path}'` (file links
when the remote is not GitHub / GitLab / Gitee / Bitbucket).

## Scenario routing

| User is asking… | Do |
|---|---|
| What is this repo / module map / architecture wiki / knowledge graph | Default flow |
| Where should I start reading / onboarding path | Default flow; put the effort into `guides` |
| What does module X do / who does it talk to | Answer from `brief.md`; deeper digest in [playbook](references/playbook.md) **Explain one module** |
| Store a rule-only wiki for the CodexQA Web UI | [playbook](references/playbook.md) **Persist rule-only wiki** |
| `brief` failed / empty export / wrong branch | [playbook](references/playbook.md) **Index health** |

Change review, callers of a symbol, test gaps, and stack traces belong to
`codexqa-code-analyzer`.

## Rules

- Facts come only from this run's export. Do not add modules, calls, or
  responsibilities that the brief does not support; do not use the README or
  a website as evidence for a module's role.
- A reading path follows real calls: each step must call or be called by the
  next. `build` rejects anything else and lists the valid neighbours.
- Standalone modules (no calls to or from other modules) get a name and a
  role, never a layer.
- Write for someone who just cloned the repo. No internal field names
  (`deps`, `cross_community`, `called_by`, `wiki inputs`); `build` rejects
  them.
- Do not run `codexqa wiki` without `--no-llm`, `wiki embed`, or `query wiki`.
  Those call a model or need model-written pages.
- Do not hand-edit the generated HTML. Change `notes.json` and rebuild.
