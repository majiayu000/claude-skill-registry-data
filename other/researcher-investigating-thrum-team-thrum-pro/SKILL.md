---
name: researcher-investigating
description: "Use when investigating, exploring code, working on a research task, when asked to find me X, or to investigate Y. Loads researcher-specific discipline for running an investigation cleanly."
---

# Researcher: Investigating

## Reconcile your queue first

Lift this query into a bundle (`thrum queue add --from-message <msg-id>`),
then `thrum queue start <bundle-id>`; drop/close finished bundles. Full
lifecycle: `using-the-queue`. Without a Pro licence (`not entitled` / `requires a license`), skip this write and track
it in the message thread instead.

## Use Explore sub-agents for breadth-first searches

**Why:** Reading 10 files into your main context to "understand the
architecture" is the Context Hog trap. Sub-agents partition the search across
multiple conversations that each report a focused finding back — the
investigation gets done without polluting your context with raw file contents.

**How to apply:** When the question is "how does X work" or "what calls Y",
spawn an `Explore` sub-agent with a clear partition: a specific directory, a
specific symbol, or a specific question. Get a focused report back. For research
across N > 6 items, invoke `efficient-multi-agent-research` instead of bespoke
dispatch — it handles partition + parallelization + consolidation.

> **Model tiers:** pass an explicit `model:` on every dispatch; choose model and effort per the
> `choosing-subagent-models` skill (read `runtime.role_models` at the moment of use). Never let a sub-agent inherit your
> own model.

### Prefer `efficient-multi-agent-research` for multi-part research

When a research or investigation task has independent parts, reach for the
`efficient-multi-agent-research` skill FIRST — it partitions the work across
many cheap parallel subagents (cheap gatherers, judgment-tier synthesizers) instead of
one expensive serial subagent. It is the preferred research path: cheaper,
faster, and it keeps each subagent's context tight.

## Verify the actual state — don't answer from recall

**Why:** Reporting from memory of past panes, files, or commits produces
over-claimed findings. The preamble carries the invariant; this rule carries the
operational depth — the specific commands to run before trusting any state
claim.

**How to apply:**

- **Pane state.** Run `tmux capture-pane -p -t <pane>` (or the runtime
  equivalent) before reporting "the pane shows X" / "the prompt fired".
- **Code state.** Use the Read tool or `git show HEAD:<path>` before reporting
  "function Y is at line Z" or "file X handles case W".
- **Beads state.** Run `bd show <id>` before reporting "task is in_progress" /
  "issue is closed" — your remembered idea of the state may be stale.

If you can't verify, say so explicitly: "I believe X based on <evidence>; I have
not verified Y."

## Scope queries before deep-diving — return early when unclear

**Why:** A vague request ("investigate the auth flow") burns hours investigating
dimensions the requester didn't actually care about. Returning early with a
clarifying question is faster overall — even if it adds five minutes of
round-trip latency, it prevents three hours of wrong-direction work.

**How to apply:** Read the dispatch and the linked spec/plan first. If the scope
is ambiguous (multiple plausible interpretations, contradictory documents, no
clear acceptance signal), reply with NEEDS_CONTEXT and one specific narrowing
question. Don't guess. Don't investigate "what they probably meant" in parallel.

## Persist findings via `thrum memory create` with a verification footer

**Why:** A finding sent only as a Thrum message is ephemeral — the coordinator
may acknowledge and move on, and the next session has to re-investigate.
Persisting as a `research_note` memory makes findings recoverable across
sessions and re-readable by other agents.

**How to apply:** After reporting to the requester, write the finding as a
`research_note` memory with cited file:line refs and a verification footer. Tag
it with `--tag <slug>` so other agents can find it later via
`thrum memory search --tag <slug>`:

```bash
cat > /tmp/research-note-body.md <<EOF
<prose explanation with cited file:line refs>

Verified: $(date +%Y-%m-%d) @ $(git rev-parse HEAD)
EOF
thrum memory create --kind research_note --scope role \
  --title "<finding prose, ~80 char soft limit>" \
  --tag <slug> \
  --oneline "<one-line summary>" \
  --full "@/tmp/research-note-body.md"
```

`--full` here is multi-line prose — compose via heredoc or a captured
variable, never double-quoted inline like this; see the heredoc-or-file rule in your role preamble.

Then add one line to `.thrum/context/research.md` under Tracked Topics (note: `thrum queue` now supersedes free-text
Open Questions tracking):

```markdown
- `<slug>` — <one-line description, ≤ 80 chars>
```

The full index format and staleness-check protocol live in
the Memory section of your role preamble.

## Never implement findings — return them to the requester

**Why:** Your job ends when you have a finding. Implementing the fix expands
scope, dirties the worktree, and conflicts with the role boundary that keeps the
team coherent.

**How to apply:** When investigation surfaces a bug:

1. Reproduce + cite the file:line evidence
2. File a beads issue with title, description, repro steps
3. Send a one-paragraph summary to the coordinator with the bd ID
4. Stop. Do not write the fix unless the coordinator explicitly asks.

The same applies for refactor opportunities, missing tests, or documentation
gaps — you surface them, the implementer ships them.

## Project-specific rules (already loaded)

Load the /thrum:project-rules-protocol skill and follow it.

If you accumulate a new rule mid-session (the user corrects you), capture it via
the Memory section of your role preamble — it references the
`thrum-memory` skill for the canonical `thrum memory create` shape.

## Pattern D self-write — set `agent_status=working` on dispatch ACK

Immediately after sending the dispatch ACK for a research request, run
`thrum agent set-status working`. This is the same Pattern D
self-write used by the implementer's dispatch-ACK protocol (sibling skill
`implementer-receiving-dispatch`).

```bash
# Step 1: ACK within 2 minutes of receiving a research dispatch
thrum reply <MSG_ID> --stdin <<'EOF'
Received. Starting <scope>. ETA <rough>.
EOF

# Step 2: Mark yourself working (RPC-preferred; local-write fallback if daemon is unreachable)
thrum agent set-status working
```

The companion `set-status idle` call lives in `researcher-answering-queries` for
the response/DONE side.
