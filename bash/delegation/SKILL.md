---
name: delegation
description: Use when handing work to another agent or model (an explorer, implementer, reviewer or critic) on any vendor, to choose its model, brief it, dispatch it and check its result. Work you do yourself needs none of this.
---

# Delegation

Every handoff to another agent or model goes through this skill. It decides who
works (role), on which model (roster) and through which vendor; the vendor's own
tools do the dispatching. Whether to delegate at all is shared policy and the
calling workflow's choice.

## Roles

| Role | Job | Access | Contract |
|---|---|---|---|
| explorer | finds and reports facts | read-only except its report file | `roles/explorer.md` |
| implementer | changes owned paths and runs the checks | owned paths; commits only if the brief grants it | `roles/implementer.md` |
| reviewer | checks work against its brief and acceptance | read-only except its report file | `roles/reviewer.md` |
| critic | challenges a plan, design or result independently | read-only except its report file | `roles/critic.md` |

The coordinator, the session that delegates, writes briefs, integrates results,
rules on findings and commits. Put the role's contract in the brief: a worker may
not load this skill.

## Roster

`.delegation/roster.toml` at the repository root (untracked) maps each role to a
vendor, model and settings; start from `roster.example.toml`. A model the owner
names in the conversation overrides the roster for that dispatch. A role with no
entry and no named model: ask the owner, never pick one yourself.

A reviewer or critic should come from a different model family than the
implementer whose work it judges. When the roster or a request puts them in the
same family, ask the owner to approve that explicitly before dispatching.

## Dispatch

1. Read the role's contract, its roster entry and `vendors/<vendor>/dispatch.md`.
2. Check the model and settings against the vendor's current list as its file
   says. A value not on the list stops the dispatch: report it, never substitute
   a nearby one.
3. Brief: the role contract, outcome, owned paths or read-only, constraints,
   acceptance checks, context pointers and report format. Writers in a shared
   checkout preserve others' edits.
4. Dispatch through the vendor.
5. Collect: record the model and settings the vendor reports actually ran, mark
   any it does not report as requested-but-unverified, and verify consequential
   claims against primary evidence before relying on them.

If your harness has its own subagent tool that can run the roster's model with
its settings, you may use it instead; it needs no vendor file.

## Vendors

| Vendor | Model list | File |
|---|---|---|
| T3 Code | T3's live catalog | `vendors/t3/dispatch.md` |
| Codex CLI | `python3 scripts/models.py refresh codex-cli` | `vendors/codex-cli/dispatch.md` |
| Claude CLI | `python3 scripts/models.py refresh claude-cli`, else a reviewed seed | `vendors/claude-cli/dispatch.md` |

`python3 scripts/models.py roster` checks every roster row: CLI rows against
their lists, T3 rows for shape. A new vendor gets a folder whose `dispatch.md`
says how to list models, launch, follow up, keep a role read-only and read what
ran, plus a lister in `scripts/models.py` when the vendor has a machine-readable
list.
