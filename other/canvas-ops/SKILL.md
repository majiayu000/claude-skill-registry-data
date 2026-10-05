---
name: canvas-ops
description: Drive the A3 canvas workbench through conversation — create nodes, write configs, wire ports, generate media, run jobs. Use when the user wants to build or edit a workflow board by talking to it. Covers lock discipline, the port-matching iron rule, quote-first submissions, and failure self-correction.
license: MIT
compatibility: Requires the skilyst runtime (>=0.1.0) with a skilyst credential (AK/SK or user/password), network access to beehive-api.verse4.pet, and an existing workflow board. The twelve canvas tools register only when this skill is active.
metadata:
  skilyst.skill_id: skilyst/canvas-ops
  skilyst.version: "1.0.0"
---

# Canvas operations (the conversation-driven board)

The board is the workflow; you are its writer. Every tool below lands a
structured change on the server-side blueprint and an action card in the
conversation — the user watches the board move as you speak.

## When to use

The user wants to build or edit a board by conversation: "add a script node
that writes a 15-second ghost-catcher patrol script", "wire the reference
image to the first frame", "generate a reference image", "run it".

**Start every session with `canvas_list_workflows` + `canvas_read_board`.**
If the user did not name a board, list them, pick the most recently updated
one, and *say which one you picked* before editing.

## The tools

| tool | what it does | key params | reach for it when |
| --- | --- | --- | --- |
| `canvas_list_workflows` | boards this account can see | limit | picking the board to operate on |
| `canvas_read_board` | full board state: nodes, edges (derived from `material_deps`/`depends_on`), media pool | workflow_id | before any edit; after a conflict |
| `canvas_create_node` | add a node to the blueprint (auto-key `{type}-{provider}-{n}`, auto-position) | workflow_id, node_type, provider, config? | "创建一个 script 节点" |
| `canvas_write_node_config` | deep-merge a config patch into one node | workflow_id, key, config | "把时长改成 15 秒" |
| `canvas_connect_ports` | wire an edge; a material source wires as `material_deps {key, input_port}` + depends_on | workflow_id, from_key, to_key, input_port? | "把参考图接到首帧" |
| `canvas_query_schema` | node definition + derived port analysis (enums, required, alternative input modes) | node_type+provider or node_id | **before every connect or submission** |
| `canvas_read_node_output` | newest job output for one node (async poll) | workflow_id, key | after submitting a generation |
| `canvas_submit_node_job` | submit ONE node as a job, quote-first | workflow_id, node_type, provider, config | running a single node |
| `canvas_run_workflow` | submit the whole board as one job, quote-first | workflow_id | "跑一下这个流程" |
| `canvas_generate_image` | submit a PAID gpt-image-2 image job | workflow_id, prompt, size? | "生成一张参考图" |
| `canvas_list_media` | the board's media pool entries (with `index` and `referenced_by`) | workflow_id | checking what is available; resolving "第 3 张"; before deleting |
| `canvas_add_media` | add an upload-origin pool entry by URL | workflow_id, url, name | bringing an external image onto the board |
| `canvas_rename_media` | rename one pool entry (locked, wholesale pool replace) | workflow_id, entry_id, name | "把参考图改名为钟馗立绘" |
| `canvas_delete_media` | remove one pool entry (409 if referenced) | workflow_id, entry_id | "删掉池里第 2 张" (check referenced_by first) |

Node types you will meet: `generate` is the workhorse — script/LLM text
generation is `generate:script` (NOT `process:script`), media generation is
`generate:minimax-h3` / `generate:gpt-image-2` / ...; `material` is a
media-pool reference (pure data input, never executed). `process` exists for
edit/postprocess providers.

## Single-node submission carries its own prompt (单节点提交自带提示词)

`canvas_submit_node_job` submits ONE node in node execution mode — the
platform does NOT merge upstream text into it. A generate node whose provider
needs a prompt (minimax-h3, gpt-image-2, ...) MUST carry the prompt itself:
write it into the node's config (`prompt` for video/image providers,
`instruction` for script) via `canvas_write_node_config` BEFORE submitting.
Wiring a script node upstream (`depends_on`) documents the flow but does
not inject its output — read the upstream script output with
`canvas_read_node_output` and put the distilled text into the consumer's
prompt config yourself.

## Lock discipline (写锁纪律)

Every blueprint write (`create_node` / `write_node_config` / `connect_ports`)
is **already wrapped** by the runtime in the server-side lock protocol:
lock → read → modify → PUT → unlock, with finally semantics (a failed PUT
still unlocks — a crash can never strand a lock; a dead holder's lock is
taken over by the next applicant server-side).

If a write raises `LockHeldError` (画板正被占用):

1. **Stop.** Tell the user the board is busy and *who* holds it (the error
   carries holder kind/id and since when).
2. **Do not retry in a loop.** The holder is alive and working; your calls
   do not preempt it.
3. Reads (`canvas_read_board`, `canvas_query_schema`) still work — you can
   keep planning, just not writing.

Your own API calls refresh the lock heartbeat implicitly while you hold it —
you never need to think about expiry.

## Port matching iron rule (端口匹配铁律)

**Before `canvas_connect_ports`, ALWAYS `canvas_query_schema` the TARGET
node.** The schema is the judge of which ports may receive what:

- **enum fields** — e.g. `image_roles` accepts exactly
  `reference_image` / `first_frame` / `last_frame`;
- **required fields** — what a submission will 400 without;
- **alternative input modes** — arrays that cannot be mixed.

**Canonical case — minimax-h3.** Its image inputs are *exclusive*:
`first_frame` and `reference_image` cannot coexist in one submission. Wiring
a reference image to `first_frame` when `reference_image` entries already
exist (or vice versa) is a 400 *at submit time* — expensive to discover
late. Query the schema, decide the port deliberately, then connect. Never
guess a port from the field name alone.

**`input_port` is never silently dropped.** A connect that passes
`input_port` with a NON-material source (a script or generate node) fails
with a structured error naming the source node — a plain `depends_on` edge
carries no port semantics, and a board that silently degrades the wiring is
worse than a refused one. If the error names a material node with no pool
reference, fix that node's `config.pool_entry_id` first, then connect.

## Quote-first (先报价)

Paid submissions (`canvas_submit_node_job`, `canvas_run_workflow`,
`canvas_generate_image`) fetch an estimate *before* the submission exists.
Quote amounts are integer micro-USD plus a USD display figure. When the
estimate is material, state the USD figure to the user and get the go-ahead
— the wallet is charged on submit (held at the quote's upper bound, settled
at measured usage).

When the caller started the run with `confirm_paid` (the desktop and web
workbenches do), a material quote PAUSES the tool: the shell shows a
confirmation card (estimate + wallet balance + confirm/cancel) and the tool
blocks until the user answers. A decline (or a timeout) raises
`PaidConfirmDeclined` — nothing was charged; ask the user what to change
instead of resubmitting. In that mode you do NOT need to ask in conversation
first — the card IS the question.

## Failure self-correction (失败自修正)

| failure | what to do |
| --- | --- |
| schema/validation 400 | read the **structured** error — the platform names the offending field and the allowed values. Fix that field, retry **once**. No blind retries, no fallback wrappers. |
| 409 workflow-modified | the runtime already retried once; `canvas_read_board` again before your next write — the board moved under you. |
| `LockHeldError` | report to the user, stop writing (see above). |
| 402 / 413 quota | report the number, do not retry. |

## Media pool flow (参考图上板)

Generation is async and the pool is where artifacts land:

1. `canvas_generate_image` **submits only** — a paid gpt-image-2 job.
2. Poll with `canvas_read_node_output` (or `beehive_get_job`) until
   `completed`.
3. On completion the server **auto-captures** the image into the board's
   media pool (`origin.kind=generated`) — no add needed.

For an external image the user supplied by URL: `canvas_add_media`, then
make it wireable as a material node, then connect:

```
canvas_add_media(workflow_id, url, name)          -> pool entry id
canvas_create_node(workflow_id, 'material', '',   -> material node
                   config={pool_entry_id: <id>})
canvas_query_schema(node_type='generate', provider='minimax-h3')
canvas_connect_ports(workflow_id, from_key=<material key>,
                     to_key=<consumer key>, input_port='first_frame')
```

Material nodes are identified by `config.pool_entry_id`; the runtime wires
them into the consumer's `material_deps` and `depends_on`, and the server
compiles that to `images[]` + `image_roles[]` (or `video_refs`/`audio_refs`)
at submit time. The pool pointer is read leniently (`pool_entry_id` or the
`entry_id` alias), but ALWAYS write `pool_entry_id` — it is the field the
server compiles, and a lenient read that has to normalize your spelling
reports the drift on the action card.

## Media pool lifecycle (池内资产管理)

The pool is the board's asset shelf — full lifecycle:

- **what is there**: `canvas_list_media` returns every entry with an `index`
  (its 1-based position), render fields, and `referenced_by` (the material
  node keys wiring it onto the board).
- **input references ("用池里第 3 张")**: list the media, resolve the ordinal
  to `entries[index-1]`, then wire it — create a material node pointing at
  that entry's `id` and connect it to the consumer:

  ```
  canvas_list_media(workflow_id)                    -> entries[2] = {id: mp-3, kind: image, ...}
  canvas_create_node(workflow_id, 'material', '',
                     config={pool_entry_id: 'mp-3'}) -> material node key
  canvas_connect_ports(workflow_id, from_key=<material key>,
                       to_key=<consumer key>, input_port=<port from query_schema>)
  ```

  Never guess an entry id from a name — names collide; list first, match on
  index or exact id.
- **rename**: `canvas_rename_media(workflow_id, entry_id, name)` — locked
  write, the platform's designed pool-replacement path.
- **delete**: `canvas_delete_media(workflow_id, entry_id)` — the platform
  refuses (409) an entry still referenced by a material node and names the
  referencing keys; offer to remove or rewire those nodes first. Always
  `canvas_list_media` and check `referenced_by` before deleting.

## Board delta awareness

Every successful canvas call lands an action row in the conversation with a
`board_delta` (added node, wired edge, pool entry, submitted job). The UI
renders these as cards the user can expand and click to locate on the board.
Keep your result summaries human-readable — the card's one-liner is what the
user reads first.
