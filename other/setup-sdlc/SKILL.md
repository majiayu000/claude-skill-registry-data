---
name: setup-sdlc
description: Adopt the agentic SDLC kit in this repository. Reads the codebase, proposes answers, asks the user to confirm, then fills in every CUSTOMISE block in the skills and AGENTS.md. Use after running install.sh, or when the user says "set this repo up with the kit", "configure the SDLC skills", or "fill in the review rules".
allowed-tools:
  - Bash(git:*)
  - Bash(gh:*)
  - Bash(rg:*)
  - Bash(ls:*)
  - Bash(cat:*)
  - Bash(lsof:*)
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - TodoWrite
---

# Set up the SDLC kit in this repo

The kit ships with blanks. This fills them in.

There are six `CUSTOMISE` blocks. The one that matters is **section B of
`skills/deep-review/SKILL.md`**, the project's own invariants. Without it the
reviewer is competent but generic. With it, it catches the bugs that are
specific to this product. Everything else here is housekeeping by comparison.

## The rule for this whole process

**Never ask what you can read. Come with a draft.**

Work out everything you can from the repo first, then put proposed answers in
front of the user to correct. A blank questionnaire gets abandoned; a wrong
guess gets fixed in ten seconds. Aim to ask about judgement and history, not
about facts sitting in `package.json`.

Ask in small batches, grouped by topic. Do not fire all of it at once.

## Step 1: read the repo before asking anything

Work these out on your own:

```bash
cat README.md AGENTS.md CLAUDE.md 2>/dev/null
cat package.json */package.json 2>/dev/null        # or the equivalent manifest
ls .github/workflows/
git log --oneline -30
git log --merges --oneline -10                     # merge commits or squash?
gh repo view --json isPrivate,mergeCommitAllowed,squashMergeAllowed
```

Then look for the shape of the product:

- **Ownership boundary.** Is there a tenant, org, workspace, account or user id
  that scopes most queries? Grep the ORM layer for it. This is the single most
  important thing to find, because it is usually where group B lives.
- **Where identity comes from.** Find the auth middleware. Does the scoping id
  come off a verified token, or out of the request?
- **The data layer.** ORM, raw SQL, or both. Any vector or full-text search.
- **Migrations.** How they run, and whether there is a command that is
  destructive.
- **Existing conventions.** Anything already written in `AGENTS.md` or a
  `CLAUDE.md` is a rule the user already cared enough to write down. Carry it
  over rather than asking again.

Also read the comments. A comment that says "do not change this without reading
X", or that explains why something counter-intuitive is the way it is, is
almost always a group B rule that nobody promoted to a document.

## Step 2: ask, in batches, with your draft attached

### Batch 1: invariants, the important one

Lead with this. If the user only answers one batch, it should be this one.

Frame the question by what you found, not abstractly:

> I can see most queries in `src/db/` filter by `orgId`, and `requireAuth`
> puts it on the request from a verified session. So my draft rule is: any
> query on an org-scoped table must constrain by the caller's `orgId`, taken
> from the session and never from the request body. Is that right, and is
> there anything else in the same category?

Then ask these, which you cannot work out from the code:

1. **What has actually broken in production?** The last incident, the last
   rollback, the last thing that woke someone up. Those are group B rules that
   have already been paid for once.
2. **What do you explain to every new engineer in their first week?** If you say
   it out loud repeatedly, it is not written down anywhere an agent can read.
3. **Is there anything that looks safe and is not?** A function whose name
   suggests it is scoped when it is not, a helper that bypasses a check, a
   setting that silently disables a control.
4. **Which of these apply here?** Offer the list, it prompts recall better than
   an open question:
   - money handled as floats rather than integer minor units
   - anything append-only, like an audit or ledger table
   - idempotency keys on a payment or webhook path
   - PII that must not cross a specific boundary
   - a migration that would lock a hot table
   - rate limits or quotas that are enforced in exactly one place
   - a cache that can serve one user's data to another

For each rule they give you, get the **consequence**, not just the rule. "Must
filter by org" is a style note. "A user of org A can read org B's documents" is
something a reviewer will block for. Write down the failure.

### Batch 2: environment and data safety

5. **Is the development database shared with anyone else? Is it production?**
   Ask directly. It is common and it is dangerous, and the answer changes the
   screenshot rules and the migration rules at the same time.
6. **Is there a command that must never be run against it?** A destructive
   schema sync is the usual answer.
7. **Which account is safe to log in as for testing and screenshots?** And does
   the data behind it belong to a real customer?
8. **Local ports**, per service. Confirm against what is actually listening.

### Batch 3: commands

9. **Install, typecheck, lint, test, build.** Propose them from the manifest and
   ask what you got wrong. Ask specifically whether any of them is broken or
   unused in this repo, since a command that prompts interactively or has never
   worked should be recorded as such rather than silently failing in CI.

### Batch 4: conventions and preferences

10. **Any writing or UI rules that keep getting broken?** Punctuation, casing,
    emoji, terminology, anything with a house style.
11. **Should an agent commit without being asked?** And push? And open PRs?
12. **Triage labels.** Read the existing ones with `gh label list`, map them to
    the roles in `skills/triage/SKILL.md` (`bug`, `enhancement`, `needs-triage`,
    `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`), and propose
    the mapping. Offer to create the missing ones.
13. **Does this repo squash or merge?** You can read this from the API, but
    confirm it, because it decides whether a screenshot committed on a branch
    ends up in the default branch's history forever.

## Step 3: fill everything in

Once the answers are in, write them. Do not leave a `CUSTOMISE` marker behind
with a "TODO" under it.

| File | What goes in |
|---|---|
| `skills/deep-review/SKILL.md` | Section B, replacing the worked example entirely |
| `AGENTS.md` | Project overview, review rules, commands, hard invariants |
| `skills/before-and-after/SKILL.md` | Test account, real-data warning, ports |
| `skills/evidence-driven-testing/SKILL.md` | The same data rule |
| `skills/new-feature/SKILL.md` | Shared resources: DB, ports, lockfiles, watchers |
| `skills/triage/SKILL.md` | The label mapping table |

Rules for writing section B:

- **One rule per bullet, with its consequence.** The reviewer quotes these back,
  so they have to stand alone.
- **Name real identifiers.** `orgId`, the actual table names, the actual
  middleware. A rule written in the abstract will not be matched against a diff.
- **Say which are blocking.** By default everything in B is P0. If something is
  really a P2, say so on the bullet.
- **Delete the worked example.** It is a multi-tenant SaaS sample and leaving it
  in means the reviewer checks rules that do not exist here.
- Keep `AGENTS.md`'s review list and section B consistent. They are read by
  different things and drifting apart is how one of them goes stale.

## Step 4: check your work

```bash
grep -rn "CUSTOMISE" skills/ AGENTS.md        # should return nothing
```

Then read section B back to the user as a list and ask one question: **"Would a
new engineer break any of these without realising?"** If the answer to a bullet
is no, it is a convention rather than an invariant, and it belongs in group E.

Finally, tell them one thing: nothing reviews a PR automatically. The review
runs on demand, via `deep-review` or the `/ship-pr` loop.

## If the user will not answer

Do not invent invariants. A made-up rule in group B is worse than an empty one,
because the reviewer will block real PRs for breaking a rule nobody agreed to.

Fill in what you verified from the code, write the rest as a short list of
open questions at the top of section B, and say in the summary that the
reviewer is running generic until those are answered. The skill already tells
the reviewer to disclose an unfilled section B rather than pretend it passed.
