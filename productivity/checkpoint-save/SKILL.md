---
name: checkpoint-save
description: "Saves session progress to a state file, naming it automatically from the session's work. Usage: /checkpoint-save [optional_name]"
---

# Save Session State

1. **Determine the project**: the basename of the git repository root (`git rev-parse --show-toplevel`), or of the working directory outside a repo, so subfolders of one repo share state (e.g. working in `/Users/me/projects/my-app/src` → project is `my-app`). Two repos with the same folder name share one cabinet. State files live in `~/.claude_states/<project>/`.

2. **Determine the `<session_name>`. Do NOT ask for one; derive it.**
   - If a name was passed after `/checkpoint-save`, use it verbatim (slugified: lowercase, kebab-case).
   - Otherwise generate one, matching **this project's existing convention**, which you must observe rather than assume: run `ls ~/.claude_states/<project>/ | tail -30` and copy the dominant shape.
   - Absent any existing files, default to `<topic-slug>-MM-DD-YY`.
   - Rules for the topic slug:
     - **Lead with the identifier the work is tracked under** if one exists: a ticket ID (`auth142`, `ops58`), else the subsystem (`billing`, `catalog`, `dashboard`). That prefix is what makes a checkpoint findable months later.
     - Follow with **2–4 words naming the outcome, not the activity**: `shipped`, `closed`, `live`, `retired`, `half-done`, `plan-ready`. `auth142-shipped` beats `working-on-auth142`.
     - Prefer the state the session *ended* in. A session that shipped one ticket and left a migration half-applied is `auth142-shipped-migration-half-done`, not `auth142`.
     - Never use content-free names: `before-we-start`, `checkpoint`, `session`, `wip`, `latest`, `update`, `notes`.
     - Keep the whole filename under ~50 chars.
   - Use today's date in the project's existing date format (`MM-DD-YY` if that dominates, `YYYY-MM-DD` if that does).
   - **Collision**: if that exact file exists and belongs to a *different* session, append a short distinguishing word rather than overwriting (`auth142-shipped-2-07-30-26`). Re-checkpointing the *same* session should overwrite, and should note in the body which earlier checkpoints it supersedes.
   - The `sendit-` prefix is reserved for runtime views; reject it for manual checkpoint names. Do not overwrite or migrate existing files with that prefix.
   - State the chosen name in the reply so it can be corrected.

3. **Review all actions, file changes, and decisions made during this session.**

4. Create or overwrite `~/.claude_states/<project>/<session_name>.md` with a highly compressed summary. First line is `# Checkpoint: <session_name>`. Sections:
   - **Domain/Goal:** what this specific session is responsible for.
   - **Working Directory:** the full path to the project.
   - **Completed Steps:** what was just finished in this exact session.
   - **Key Files Modified:** files changed or created.
   - **Open Blockers:** unresolved errors or logic gaps.
   - **Next Actions:** exact instructions for the next step, as a numbered list with one action per line. Keep the action itself on that line and put any detail it needs on indented sub-lines beneath it: `/checkpoint-load` echoes these back as single-line sub-bullets, so an action whose first line runs into rationale reads as noise there. When the session states the next actions, keep exactly that list in that order; add no steps of your own.

   **Lead with any state that is unsafe to forget** (halted daemons, disabled flags, live production state, open migrations, money or data at risk) in its own section above Completed Steps, including the exact command to reverse it. A checkpoint's worst failure mode is a fresh session resuming without knowing the system was left in a non-default state.

   **Record what was measured, not only what was concluded**, and explicitly flag any conclusion a later step invalidated. Numbers and falsified assumptions are exactly the parts a fresh context cannot re-derive.

   **Active controller-owned Send It task:** preserve its runtime authority. Follow `/checkpoint-load`'s sealed-bridge validation procedure for the exact `sendit-<run-uuid>` using the recorded platform's installed runtime. Only after successful authoritative JSON readback, reference its run, platform, snapshot sequence and sealed hash in this manual document, preserving all nine semantic fields and retained limits. Save these notes under an ordinary name; the seal remains authoritative and must be revalidated on a later sealed load. Do not overwrite the Git-local generated view, invent a replacement binding, or use operator `recover` to reset its limits. If no valid seal exists or validation fails, label this manual document as session notes, record the missing seal or validation error, and do not present it as an automatic worker recovery receipt; the bound controller must save/reconcile its current phase before automatic continuation. Saving or reading notes does not rebind, reset limits or authorize a restart.

5. Create the directory if it does not already exist.

6. Once the file is written, remind me to run `/clear` to free up the terminal context window.
