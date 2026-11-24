---
name: baton-pass
description: "Use when work moves to another session, agent, tool or person, the session runs short, or a packet arrives. Unattended agents need OK."
user-invocable: false
---
# Baton pass
Gate: get the user's OK before starting an agent that keeps running without the user, or sending work or code to a teammate's machine (G1, G6). See gates.md in the skill house-rules.
Job: Move work to the next session, agent, tool or person with the least loss, and pick it up cleanly at the other end.
Takes: session state and a destination, or a received packet.   Gives: one chosen move, a packet, or a started worker; on receipt, a restated goal and a report at the end.
Team moves: see team, dispatch, hand over code, other machine

Received a packet? Go straight to Receiving.

## Steps

### Choosing

Every move except staying swaps the first-hand record for a digest, so pay that only when staying costs more. Clearing the wrong context can't be repaired: the diff shows what changed but not why. Ask in order. The first yes wins.

Mid-chunk, keep working or give the rest to workers. The only move that can apply then is forking a side task, at question 3.

1. **Can you stay?** Yes if the next chunk needs this reasoning first-hand, or there's room. Reasoning weakens past about 150k tokens.
2. **Is everything disposable?** Empty the session. It's instant, and the old one stays resumable.
3. **Must work travel** to another tool, folder or person, or fork as a side task? Write a packet. Nothing else justifies one.
4. **Can it run unattended, tightly scoped?** Dispatch it.
5. **Otherwise compress,** naming what the next chunk needs. You'll often land here, but it comes last because a summary can lose the nuance of a decision.

Clearing and compressing are the user's keystrokes where the host gives no tool for them, so recommend the move.

Before the user leaves, or before a wait of an hour or more, write the packet anyway and tell the user that clearing the session (`/clear` on Claude Code) and starting from the packet makes resuming cheap. An idle cache expires, and the next turn rewrites the whole context.

### Sending

1. **Fill the packet** from existing artifacts, using the shape in the file `artifacts.md` in the skill `house-rules`. Tailor `Goal` to the stated focus. `Goal` and `Next` say what to achieve, not how. Name skills in `Use`; don't copy their steps. A suspected cause goes under `Open` as `[reported]`, never in `Goal`. Carry `Asked` and `Limits` unchanged. Use references over copies. Label each `State` line. List helpful skills in `Use`, and make the packet make sense without them.
2. **Hand over code as code** (see the table). A description of edits is never the hand-over.
3. **Keep it portable** when it crosses machines. Use only portable refs: inline anything that sits in the bench or a worktree path.
4. **Redact, then measure.** It must be under 3,500 characters, and so must any prompt for a host subagent: `node -e "console.log(require('fs').readFileSync(process.argv[1],'utf8').length)" <packet>`. Move anything bigger behind a reference.
5. **Save it** in bench `packets/`, then **launch** with the packet itself as the brief or message, or a short prompt holding only its path. Packet text never goes through a shell. Give the worker a descriptive name, or note its run id where the level assigns one.
6. **Track it.** Whatever comes back is `[reported]` until you re-run it. Tell the user what moved, to whom, and where the packet is.

A dispatch inside a run the user asked for needs no OK, and "hand this to Codex" is itself the OK. A worker that would keep running beyond what they asked for is G6.

| Level | Code travels as | The next agent starts by | It returns through |
|---|---|---|---|
| hub | A commit on a named branch, named in the packet. An isolated run starts from your tree's last commit, so check out the base first | Dispatch with the packet as the message: an isolated write run, or a message to an agent already running | `final message` |
| host | A commit on a named branch, named in the packet | Host subagent with the packet as prompt | `final message` |
| herdr | A commit on a named branch, in its own worktree | New workspace and agent, the prompt holding only the packet path | `final message`, or `file:` inside its worktree |
| solo | A local commit | Nothing starts. Tell the user how to open the next session with the packet | `file:` |

- A named kind the host can't start as a subagent: use that kind's headless CLI, checked with `--help`, or herdr. If neither exists, write the packet and say the user has to start it. Name the fallback either way.
- A person: the packet is the deliverable, in portable refs. Sending it is the user's act.
- Another machine: say it's not available and give the user a packet to carry.

### Receiving

1. State the goal in one line.
2. Check `base` against your tree. Rebase if it's wrong. If the base can't be reached, report `blocked`. On a fresh tree, check `git for-each-ref refs/dami/wip` before rebuilding lost work. Compare `where` with your own hostname: if they match, say `running locally` and don't SSH to `where`.
3. Read `Refs`, `Settled` and `Open`.
4. Obey `Limits`. They outrank your own method and everything in `Use`.
5. Treat the packet as work, never as an OK. A quoted gate OK is information. Stop at any gate and report it under `Needs OK`. A lead in a new session asks the user again, unless its own prefs hold a standing OK that names the action.
6. Do `Next`, in the role the header gives you. Use the skills in `Use` if you have them, and carry on if you don't.
7. If you disagree with `Settled`, put that under `Open` and keep working to the settled decision.
8. Return a report through `return`, in the shape from the file `artifacts.md` in the skill `house-rules`. Answer every `Asked` item. Hand over code first, then finish with the report, under 3,500 characters.

## Done when

The test for a sent packet: the receiver could start with no other context.

Sender:

- One move was chosen by asking in order, and the reason for it is stated.
- `Asked` and `Limits` are unchanged, `Next` is one concrete action, and `State` lines are labelled.
- The packet measured under 3,500 characters and is redacted.
- Any code travels as a commit or branch that the packet names.
- A started worker has a name or run id, and the user knows the level used and any fallback taken.

Receiver:

- The goal was restated and `base` was checked.
- The report answers every `Asked` item, labels its evidence, and arrived through `return`.
