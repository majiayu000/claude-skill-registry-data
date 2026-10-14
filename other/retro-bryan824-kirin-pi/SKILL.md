---
name: retro
description: "When the user asks to look back on a session — find where the agent struggled and propose environment fixes so the next run goes better."
disable-model-invocation: true
---

# Retro

Change the environment, not the code. For each struggle, ask what in the
repository allowed it, then propose the pointer, check, standard or access that
prevents it next time.

- Read the session's own record: the current conversation by default. Read another
  session's log only when the user names it; logs are private data. On a long
  session, run while the struggles are still in context.
- Tie every candidate to a specific moment: the search that took too long, the
  mistake, the fact the agent could not get. Drop any candidate you cannot trace;
  generic best practice filling a category is the main failure. A smooth session
  can honestly yield nothing.
- Route each fix to its existing owner:
  - Slow to find a file or fact: a navigation pointer from something the agent
    already reads.
  - A mistake a tool could catch: a deterministic check. Read the repository's own
    check commands, hooks and CI first; an unwired or broken check is the finding.
    A repository with no guardrail at all is a finding to report, not to install.
  - A judgment mistake review missed: a rule in the standards file the reviewer
    reads, created when the first such rule exists.
  - Steering that changes nothing, or a rule a check could enforce: delete or move
    it. Always-loaded instruction files hold pointers and essential rules.
  - A check that fired on good code: propose removing or narrowing it.
  - A tool call that cost more than it returned: a cheaper command or tool.
  - Information the agent could not reach: wider read access, such as a dev
    server log written to a file.
- Rank by cost to the next run, not by how loud the moment was.

Propose only. Edit nothing until the user picks a candidate; a chosen fix then goes
through normal implementation and verification. Retro changes the environment so
the mistake cannot recur; it is not a memory store.

Deliver: candidates most severe first, each with its session moment, owning file
and proposed change, or an explicit result that nothing traceable was found.
