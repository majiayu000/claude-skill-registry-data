---
name: thrum-memory
description: "Use when capturing, reading or querying structured memories (session summaries, architectural decisions, restart snapshots, agent rules) via the thrum memory CLI - writing a role-rule, looking up rules at session start, recalling a topic, or checking what a memory should say before you write it."
allowed-tools: "Bash(thrum memory:*)"
version: "0.11.0"
license: "Apache-2.0"
---

# thrum memory — capture, read and query structured memories

> **Before writing or editing any memory or state entry, apply "A memory states the current rule" below:** a memory
  states only the CURRENT rule (exceptions allowed), never a timeline of rulings, corrections or reversals, and every
  touch re-examines the whole memory.

## When to use thrum memory vs. other stores

Learned something future work should respect? → `thrum memory create` (pick a kind below).

Transient task state (in-progress work, current session context)? → your task tracker's notes, not memory.

Long-form project narrative (architecture decisions, release status)? → kind `arch_decision` or `session_summary`.

Code documentation (CLAUDE.md, READMEs, in-file comments)? → edit the file directly. Memory is for structured records,
not docs.

## Kind taxonomy

- `session_summary` — what shipped in a session
- `arch_decision` — long-lived architectural decision; can be superseded later
- `current_state` — point-in-time state snapshot; expires fast
- `epic_status` — one row of open epics or active work
- `worktree_status` — one worktree-table row; expires per session
- `stable_infra` — long-lived infrastructure entry
- `resume_snapshot` — per-agent restart blob (scope=agent)
- `agent_rule` — rule or preference for future sessions (scope=role or scope=project)
- `research_note` — a verified research finding (see the cite-stamp rule below)
- `comment` — comment on a parent memory (`child_of: <parent-id>`)

## Reading

### Canonical read flow — 3 zoom steps

Never jump straight to `--zoom full` or `--format body`. Escalate in order:

1. **Scan the index** — onelines only, no body content loaded:

   ```bash
   thrum memory index [--scope <scope>] [--kind <kind>]
   thrum memory list --zoom oneline [--scope <scope>] [--kind <kind>]
   ```

2. **Triage with short** — for records that look promising:

   ```bash
   thrum memory show <id> --zoom short
   ```

3. **Fetch full only when confirmed** — `thrum memory show <id> --zoom full` (default zoom is full).

The index and short tiers exist to save context. Multi-record output from `list` and `search` prints `body_oneline`
only.

### Session-start enumeration of role-rules

```bash
thrum memory list --zoom oneline --kind agent_rule --scope role
```

`--scope role` infers your role from the daemon identity binding; no qualifier is needed. To narrow by tag, use `search`
(`list` has no tag filter):

```bash
thrum memory search --kind agent_rule --scope role --tag <slug>
```

### Topic-driven recall

```bash
thrum memory search "<topic keywords>"                 # ranked, oneline
thrum memory show <id> --zoom short                    # triage
thrum memory show <id> --zoom full                     # fetch
thrum memory search "<topic>" --kind research_note     # filter by kind
thrum memory search "<topic>" --tag <slug>             # filter by tag
thrum memory search "<topic>" --since 30d              # filter by recency
```

`search` runs full-text search and, when configured, embedding search. For `--near` queries, complex predicates and hint
codes, use `memory-search-advanced`.

### Pulling a known entry

```bash
thrum memory show <id> --zoom full
thrum memory show <id> --format json | jq -r '.body_full'
```

Default text output shows ID, Kind, Status, Scope, Agent, Created, Updated, Tags, Parent, then every zoom level present.

### Cross-scope reads

Omitting `--scope` returns every scope the caller can access. The CLI does not filter on another role's name; query the
broader scope and narrow with `--tag`:

```bash
thrum memory list --zoom oneline --kind agent_rule --scope role     # your role
thrum memory list --zoom oneline --kind agent_rule --scope project  # project-wide
thrum memory list --zoom oneline --kind agent_rule                  # all visible scopes
```

## Writing

### Canonical write command

Compose real prose in a file or heredoc, never double-quoted inline:

```bash
cat > /tmp/memory-body.md <<'EOF'
<body — rule + Why + How to apply, or finding + cites>
EOF
thrum memory create --kind <K> --scope <S> \
  --title "<short prose title — what this entry says>" \
  --oneline "<one-line summary, ≤280 bytes>" \
  --short "@/tmp/memory-body.md" \
  --tag <slug-or-keyword> [--tag <additional-tag>]
```

`--kind`, `--title` and `--oneline` are required (the daemon rejects a create without them). `--short` and `--full` are
strongly encouraged; omitting both raises the MEM-010 hint and weakens retrieval. Populate all three zoom levels when
authoring:

| Field          | Length budget | Purpose                                                       |
| -------------- | ------------- | ------------------------------------------------------------- |
| `body_oneline` | ≤280 bytes    | Default search and list render — conveys the gist in one line |
| `body_short`   | ≤4 KB         | Mid-zoom — default `show <id>` render                         |
| `body_full`    | ≤256 KB       | Deep zoom — full body via `show <id> --format body`           |

For role-rules: `oneline` is the rule in one line, `short` is the rule plus Why and How to apply, and `full` is omitted
unless `short` is not enough.

Without a Pro license (`not entitled` / `requires a license`), skip the write and track the item in the message thread
instead. `create`, `edit` and `link` need the memory.substrate entitlement; reads, `delete`, `purge` and `unlink` do
not.

### Body shape

**Role-rules (`--kind agent_rule`):**

```text
<rule statement — one sentence>

Why: <reason — past incident, project policy, or strong preference>
How to apply: <when/where this kicks in>
```

Lead with the rule. The `Why:` line is what a future reader needs to judge edge cases the rule does not literally cover.

**Research notes (`--kind research_note`):**

```text
<finding statement>

Evidence: <file:line citations or external links>
Verified: YYYY-MM-DD @ <commit-sha>
```

The `Verified:` stamp is `git rev-parse HEAD` at verification time. It drives the staleness check in
`memory-maintenance`. When you re-verify, edit the entry to replace the stamp:

```bash
cat > /tmp/memory-verify-body.md <<'EOF'
<verified body with updated 'Verified: ... @ <new-sha>' footer>
EOF
thrum memory edit <id> --full "@/tmp/memory-verify-body.md"
```

**Other kinds:** free-form body matching the kind. Lead with the decision or observation, then its context.

### Title

Free-form prose, about 80 characters. The title appears in every `list` output:

- GOOD: `"Coordinator must verify implementer findings before forwarding"`
- GOOD: `"safecmd.Bd 2-return signature mirrors safecmd.Tmux"`
- AVOID slug-style or role-prefixed titles such as `"coord-verify-findings"`. The slug belongs in `--tag`.

### Tags as the slug handle

The per-entry slug is kebab-case keywords in `--tag`. Repeat `--tag` for each tag. `thrum memory search --tag <slug>`
finds the entry by its concept key:

```bash
thrum memory create --kind agent_rule --scope role \
  --title "Implementer must use safecmd.Bd not raw exec for bd calls" \
  --oneline "Daemon-adjacent bd invocations must use safecmd.Bd helper" \
  --short "..." \
  --tag safecmd-bd --tag daemon-discipline
```

Feature-scoped queries use a `feature-<name>` tag by convention (no code enforces it):

```bash
thrum memory create --kind session_summary --tag feature-watcher-substrate,substrate ...
thrum memory search --tag feature-watcher-substrate --limit 10
```

Module installs use `--tag mod-<module-name> --tag <slug>` so they do not overwrite user entries that share a slug.

### Scope

`--scope` takes `project | agent | role`. The CLI infers identity from the caller's daemon binding; there is no
`:role:<name>` shape.

| Scope     | Use for                                           | Visibility                                                              |
| --------- | ------------------------------------------------- | ----------------------------------------------------------------------- |
| `role`    | Role-rules, role-specific guidance                | All agents sharing this role; preferred default for `agent_rule` writes |
| `agent`   | Private rules or notes for this agent instance    | Only this agent (by agent_id)                                           |
| `project` | Shared knowledge across all agents in the project | Every agent in the project                                              |

For role-rules, always use `--scope role`.

## A memory states the current rule

A memory written as a timeline ("X; later corrected to Y; exception Z; Z reversed") is worse than no memory. Exceptions
are fine. Reversals and layers of revisions are not.

This applies to every store: `thrum memory`, `thrum state`, file-based memories and their indexes, and restart
snapshots.

**Every touch re-examines the whole memory.** Whenever you create, edit, append to or merge a memory, read all of it,
not just your change. If any part is a timeline, a stale version of a rule, or a summary that disagrees with the body,
rewrite the whole memory to the current rule in the same edit.

**Shape:**

```text
<Rule, present tense, one or two sentences, with its full scope:
 which roles, runtimes, repos, peers, boxes or paths it covers.>
<Exceptions as part of the rule: "except X, where Y". An exception that ends on
 a condition says so: "until <event>; check it before applying".>
Owner, date and one short quote of the CURRENT ruling (optional).

Why: <the reason, short>
How to apply: <every still-current precondition, command, control and bound>
```

A memory with several independent rules keeps each as its own headed section in this shape, or splits into linked
memories. Never collapse independent rules into one sentence, and never drop a rule because it is not the title's rule.

**Stays:** the current rule and its full scope words; its current exceptions; the current ruling's owner, date and
quote; the reason (a past incident only when the Why is empty without it, kept to two lines); every still-current
precondition, command, control and bound.

**Goes:** replaced statements, their quotes and dates; "first X, then Y" narratives; exceptions that no longer apply;
evidence that only supported a replaced statement; markers such as "UPDATE", "CORRECTED", "SUPERSEDED", "REVERSED",
"STRICKEN", "later", "(late)" and strikethrough.

**Scope is part of the rule.** Never shorten scope words (which repo, role, runtime, peer, box, path). For anything
about authorization, peering, capability or access, read the project's security model first and keep every scope
qualifier word for word.

**Every summary agrees with the body.** A memory can have several summaries; make each match the rewritten body:

- File memory: its front-matter `description:`, its line in the main index (e.g. MEMORY.md), and its line in any
  secondary index. Grep the file name in every index.
- `thrum memory`: its `--title` and `--oneline`. Find related entries with `thrum memory search <topic>`; rewrite with
  `thrum memory edit <id>`.
- `thrum state`: the value of every key that restates the rule. Keep a file memory and the state key it names identical.

**Rewriting a memory:**

1. Read the memory, every memory it links to, and every memory on the same topic (search by topic, not only title). If
   it names a live source (a config key, skill, template, bead), read that too. When the live source is newer, the
   memory says "read X at the moment of use" instead of restating X.
2. List every distinct statement it makes, with its date or position.
3. Decide the current rule point by point. For each point, the latest owner statement on that point governs. A later
   statement replaces an earlier one only when it covers the same scope; a narrower later statement is an exception, and
   the earlier statement still governs everywhere else. If two statements have the same scope and no clear order, mark
   the memory AMBIGUOUS, change nothing, and put the exact question to the owner.
4. Rewrite in the shape above, one section per independent rule.
5. Rewrite every summary to match.
6. If another memory states the same rule, move every still-current point into the memory you keep, then reduce the
   other to a one-line body ("Merged into <name>.") and re-point or remove its index entries. Never reduce a memory to a
   pointer before its current points have moved.
7. Self-check (all must be yes): a reader can act correctly after the first section alone; each rule is stated once,
   with no earlier version beside it; every summary matches the body; no other memory states a different version; no
   scope word, current exception, precondition or reason was lost.
8. Report each memory as REWRITTEN, MERGED INTO x, AMBIGUOUS (question) or UNCHANGED (why), and say in one line which
   rules were kept, dropped (and why) or moved (and where).

**Index entries.** An index entry is one `[text](file.md)` link. Rewrite only that link's text; leave the other entries
on its line alone. Follow any format contract the index states about itself (caps, demotion). An index entry that marks
a memory as superseded or corrected is itself a timeline: rewrite it to the current rule or remove it.

**Auditing a store.** Grep the store for the markers above and for topics that more than one memory covers, then follow
the steps for each hit. A grep finds only marked memories, so also read the memories that share a topic with a hit.

Never invent a rule. When unsure whether a statement is still current, ask.

## Top operations

```bash
thrum memory search --tag substrate --kind arch_decision   # one tag per query
thrum memory show thrum-mem-01EXAMPLE00000000000000000
thrum memory edit <id> --short @newshort.md                # changed-zoom embeddings re-queue
thrum memory edit <id> --add-tag v0.11 --rm-tag draft
thrum memory link <new-id> supersedes <old-id>
thrum memory link <child-id> child_of <parent-id>
```

Edits, supersedes, deletes, edge changes and history walks are covered in `memory-maintenance`.

## Default-safe behaviors

- `--limit 10` by default for search. Memory bodies are much larger than messages; `--limit 25` or higher is an explicit
  opt-in.
- `status=active` is the default filter. Use `--status all` to include superseded and purged entries.
- Scope is an assembly filter, not access control. `memory.search` returns matches in every scope unless `--scope` is
  passed. Scope only decides which memories the default assembler folds into an agent's prime context.

## When you need more

- RAG, `--near` queries, complex predicate stacks, pagination, and MEM-001..010 hint codes: `memory-search-advanced`.
- Edit, delete, supersede, edges, hierarchy, comments, history, undelete and hard delete: `memory-maintenance`.
- Moving a MEMORY.md entry's full text into a memory record: `memory-to-thrum-pointer`.

## First-time setup

Embedding is opt-in. The default config disables RAG; full-text search (`--grep`) works without it. To enable RAG:

```bash
thrum config set llm.embedding.enabled true
thrum config set llm.embedding.provider ollama --force
thrum config set llm.embedding.base_url http://localhost:11434 --force
thrum config set llm.embedding.model "granite-embedding:30m-english"
```

For non-English projects use `granite-embedding-multilingual-97m`.

Memory IDs take their prefix from the repo (git remote URL, then the main worktree basename, then the working-directory
basename, normalized). To override:

```bash
thrum config set id_prefix "my-repo"
```

Rate limit and backfill knobs: `embedding.max_per_minute` (default 60) and `embedding.backfill_on_boot` (default true).
