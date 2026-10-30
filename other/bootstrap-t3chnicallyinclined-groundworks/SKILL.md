---
name: bootstrap
description: Start a new project from one of the Groundworks stacks and prove it builds. Run only when the user invokes /groundworks:bootstrap.
disable-model-invocation: true
---

# Start a new project from a stack

Work in the main session. Do not start other agents for this.

1. Call `stack_list`, and `stack_show` for the likely candidates. Recommend one stack in a sentence
   and say why; ask the owner for the project name if they have not given it.
2. Call `bootstrap` with the stack and name. It refuses a directory that exists and is not empty;
   if it does, report that and stop.
3. Call `gate` on the new project straight away, before anything is added, to prove the scaffold
   builds. Report the result exactly as it came back.
4. Record a `journal_add` of kind `status` for the new project: the stack, the gate result and its
   machine, and what the owner said the project is for. Ask for a one-line summary if there is
   none, and tell the owner the summary line to put in its registry file.
