---
name: init
description: Bring the current project under Groundworks - register it, record the owner's answers, and prove its gate. Run only when the user invokes /groundworks:init.
disable-model-invocation: true
---

# Bring a project under Groundworks

Work in the main session. Do not start other agents for this.

1. **Is it already registered?** Call `project_list`. If the current folder's project is there,
   call `project_show` for it, say so, and stop unless the user wants to change something.
2. **Ask the owner at most three questions**, in one message, in plain words:
   - What is this project for, and what state is it in (active, paused, archived)?
   - What command proves it works (its gate)? Offer the stack's gate from `stack_list` as a
     suggestion. Never run a command the owner has not confirmed.
   - Where does it belong: an existing workspace, a new workspace, private (nothing leaves it), or
     isolated (nothing comes in or leaves)?
   A skipped question is recorded as open, never guessed.
3. **Register it** with `project_register` (name, directory relative to the workspace, a one-line
   summary from the owner's answer, the stack if one fits). If the gate differs from the stack's,
   tell the owner the `gate = [...]` lines to add to its registry file.
4. **Record the answers** with `journal_add`, one entry per answer: kind `fact`, confidence
   `CONFIRMED`, source `owner statement, <today's date>`. Record the intended scope too; until the
   store enforces scopes, say that it is recorded, not yet enforced.
5. **Prove the gate** with `gate`, once, after the owner says go. Report the result exactly as it
   came back (which step, which machine). A red gate is reported red.
6. **Finish** with `project_show` for the project and a `journal_add` of kind `status`: what is
   registered, what the gate proved, what is still open.
