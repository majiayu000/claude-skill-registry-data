---
name: spec-investigate
description: >
  Deep, evidence-based technical investigation of a piece of work BEFORE any specification or
  implementation begins — starting from a ticket (Jira, GitHub Issues, Linear), a meeting/call
  transcript, a plain-text description, a doc/PRD file, a Slack/email thread, or an error log.
  Use when the user says "investigate STP-123", "spec-investigate", "look into this before we
  plan it", or hands over any of those inputs and wants the
  system understood (current behaviour, root cause, affected repos/files, risks, open
  questions) rather than fixed or built yet. This is the first stage of the
  investigate → create → (human approval) → implement → verify → ship pipeline — it hands off
  to the existing spec-create skill and does not replace, duplicate, or invoke spec-create,
  spec-implement, spec-verify, or spec-ship itself. Ticket-agnostic: works for bugs, features,
  refactors, security, performance, infra, or cross-repository tickets in any repo.
license: MIT
---

# spec-investigate

Discover and record the facts. Do not design the fix and do not write any code.

This skill is stage 1 of:

```
spec-investigate → spec-create → human approval → spec-implement → spec-verify → spec-ship
```

`spec-create`, `spec-implement`, `spec-verify`, and `spec-ship` already exist elsewhere (e.g. the
`ticket-to-pr` plugin, or whatever equivalent this host provides). **Never create, redesign,
duplicate, or invoke those skills from here.** Your only output is an investigation report plus a
ready-to-use work branch; a human decides when to run `spec-create` next.

## Project config (read first)

Load `.spec-driven.yml`: walk up from the current directory to the home folder, and the first one
found wins (a `multi-repo` config only applies inside the repos it lists). If none is found, check
`~/.spec-driven/workspaces.json`, which maps each multi-repo config to its repo paths. Use the config
whose repos contain the current directory, because a workspace's repos can live in unrelated folders. Its values beat anything
you would detect or assume. This skill uses `layout`/`repos` (where to look and what each repo does), `tracker`, `git.remote`, `git.base_branch`, `git.branch_name`, and `specs_dir`.

**Monorepo:** name the package(s) involved. **Multi-repo:** search every listed repo whose role fits the ticket, and create the work branch, with the same name, only in the repos the investigation shows need changes.

**No config?** If the `spec-setup` skill is available, run it first, then continue here. If it
isn't, detect what this skill needs from the repo, ask about anything ambiguous, and offer to save
the answers to `.spec-driven.yml` (keys: `layout`, `repos`, `tracker`, `git`, `commands`,
`specs_dir`).

## Invocation

```
spec-investigate STP-123
spec-investigate https://<org>.atlassian.net/browse/STP-123
spec-investigate STP-123 --context ./notes.md
spec-investigate #482                      # GitHub issue in the current repo
spec-investigate https://github.com/<owner>/<repo>/issues/482
spec-investigate https://linear.app/<team>/issue/ENG-91
spec-investigate ./call-transcript.txt          # transcript, notes, PRD, RFC, log — any file
spec-investigate "Checkout times out for EU users since Tuesday's deploy"   # plain text
spec-investigate                               # with the material pasted in the same message
```

The only required input is *something that describes the work* — a ticket ID/URL, a file, or text
pasted into the message. Below, "the ticket" means that primary input, whatever form it took. `--context` (a file path, or pasted text in the
same message) is optional supplementary evidence — a call transcript, meeting notes, a `.md`/`.txt`
file. Never block or stall waiting for context that doesn't exist; proceed without it.

Never hardcode a specific ticket ID into your behavior. Everything below must work identically for
any ticket key, tracker, or free-form input.

## The one rule everything else serves

**Do not guess when the answer can be discovered.** Every non-trivial claim in the final report
must be traceable to something you actually read — code, config, tests, git history, the
ticket, linked docs — not inferred from a plausible-sounding folder name or a guess at convention. Work
the loop:

```
Question → Search → Evidence → Trace → Cross-check → Concrete answer
```

"I haven't looked yet" is not the same as "unknown." Only write UNKNOWN after you've actually
searched and found nothing — and say what you searched.

Calibrate investigation depth to the ticket. A one-line copy change doesn't need an architecture
diagram; a cross-service auth or data-migration ticket does. Don't manufacture process for a
trivial ticket, and don't shortcut a genuinely risky one.

---

## Step 0 — Resolve the input and set up the branch safely

1. **Identify what kind of input this is and load all of it.** A tracker reference:
   - `*.atlassian.net/browse/KEY-123` → Jira (Atlassian MCP tool, `jira`/`acli` CLI, or REST).
   - `#482`, `owner/repo#482`, or a `github.com/.../issues/482` URL → GitHub Issues
     (`gh issue view 482 --comments --json title,body,labels,comments,...`).
   - `linear.app/.../issue/ENG-91` → Linear (Linear MCP tool or API).
   - A bare `KEY-123` → use `tracker` from `.spec-driven.yml`; without one, the tracker the project already uses (CLAUDE.md/AGENTS.md, branch
     names, PR links in `git log`); if that's ambiguous, try the trackers this host can reach and
     ask if none resolves. If you can't reach the tracker at all, ask the user to paste the ticket
     rather than guessing its contents.

   Anything else is free-form input — read it in full:
   - A file path (`.txt`/`.md`/`.vtt`/`.srt`/`.pdf`/`.docx`/log) → read the whole file.
   - Pasted text — a transcript, Slack/email thread, PRD excerpt, stack trace, or a one-line
     description → use it as-is.
   - A URL to a doc, PR, Sentry/Datadog issue, or design → fetch it with whatever access the host
     has; ask the user to paste it if you can't.
   Free-form input has no fields, so extract them: a working title, the type of work, the stated
   problem and desired outcome, any acceptance criteria actually stated, and who decided what.
   Apply Step 1's classification to it (requirement vs. proposal vs. question) — a transcript is
   not a spec. If it references a ticket, fetch that too and treat it as the scope of record.

   For a ticket, pull title, type,
   priority, labels, components, full description, comments, linked/parent/child issues, and
   attachments. Follow meaningful links (a linked ticket that defines the actual contract, a
   linked design doc) rather than stopping at the description.

2. **Determine the repository/repositories.** If you're already inside a git working directory
   that plausibly owns this ticket's area, use it. If the ticket is cross-repo (confirmed from its
   content, not assumed), identify every relevant repo and investigate each one — don't silently
   pick just the one you happen to be sitting in. If you can't tell which repo(s) are relevant
   from the ticket alone, say so and ask, rather than guessing.

3. **`git status` first, always.** If there are uncommitted changes unrelated to this ticket:
   **stop** — do not stash, reset, clean, discard, commit, or force anything on the user's behalf.
   Report exactly what you found and ask how to proceed.

4. **Determine the correct remote and base branch.** Run `git remote -v` — don't assume `origin`
   is the right remote if there's more than one. Pick the base branch in this order: `git.base_branch` in
   `.spec-driven.yml` → what `CLAUDE.md`/`AGENTS.md`/memory/prior project context says for this repo → the remote's default
   branch (`git remote show <remote>` or `gh repo view --json defaultBranchRef`). If the repo also
   has an integration branch (`staging`, `develop`) that recent work branches were cut from, and
   nothing says which to use, stop and ask rather than guessing. Fetch it and record its latest
   commit SHA.

5. **Name the branch by the repo's convention, then stick to it exactly.** Use, in order: `git.branch_name`
   in `.spec-driven.yml` → an explicit rule in `CLAUDE.md`/`AGENTS.md`/memory → the pattern recent branches already follow
   (`git branch -r --sort=-committerdate | head -20` — e.g. bare `STP-123`, or `fix/STP-123-…`) →
   default `<type>/<TICKET-ID>-<short-slug>` with the same prefixes `spec-ship` uses (`feat/`,
   `fix/`, `refactor/`, `chore/`, `docs/`). Don't invent a new pattern alongside an existing one.
   With no ticket ID (free-form input), use `<type>/<short-slug>` from the working title, and ask
   whether there's a ticket it should be linked to.

6. **If the branch already exists** (locally or remotely): do not delete, reset, rebase, or
   recreate it. Investigate first — what commit is it on, does it already have commits ahead of
   base, uncommitted changes, an existing `specs/` folder or investigation report, signs of
   started implementation? If continuing risks losing someone's work, **stop and report** instead
   of proceeding. If it's clean and simply behind the latest base, that's fine to note, not fix
   unprompted.

7. **If the branch doesn't exist:** create it directly from the fetched base commit. Never modify
   the base branch itself, never force-push.

8. Record for the report: source type (ticket / transcript / text / doc / log), ticket ID +
   tracker + URL or file path, working title, type of work, branch name, base branch, base commit
   SHA.

## Step 1 — Read the optional context, but don't crown it source of truth

If `--context` or pasted material was given, read it fully. It is **supplementary evidence**, not
automatically a requirement. For every substantive claim in it, classify what kind of statement it
actually is: a stated requirement, a business decision, a technical decision, a constraint, a
description of existing behaviour, a proposed (not decided) solution, a question, an assumption, or
just an example. A sentence like "maybe we should add another endpoint" is a proposed approach to
investigate against the existing API, not a requirement to build it.

Default evidence hierarchy when sources disagree — but actually evaluate conflicts, don't apply
this mechanically:

```
Repository / actual system behaviour
        ↓
Ticket scope and acceptance criteria
        ↓
User-provided context / meeting discussion
        ↓
Supporting documentation
```

When the context introduces something not in the ticket at all and it would materially affect scope,
architecture, data, APIs, security, or effort: don't fold it in silently. Flag it as Confirmed /
Likely / Proposed / Needs Clarification, and if sources genuinely conflict, document it as:

```
Ticket says: ...
Additional context says: ...
Repository currently does: ...
Impact: ...
Recommended clarification: ...
```

No context supplied is a completely normal case — proceed on ticket + repository evidence alone,
don't ask for a transcript that may not exist.

## Step 2 — Understand the ticket itself

From the ticket: problem statement, expected behaviour, acceptance criteria, type (bug / feature /
refactor / security / infra / perf / data / integration / UI / API / DB — whatever it actually is,
don't force it into a category it isn't). Pull in anything linked that actually defines scope.

## Step 3 — Map the relevant system before touching anything

For each relevant repo, briefly note why it's relevant and which app/service/module inside it
matters. Then trace the ACTUAL implementation — not what the folder names suggest — through
whichever of these layers are real for this stack:

```
Client/UI → Route/Controller → Service/Business logic → Data access → Database → External integration
```

Also check, wherever relevant to the ticket (skip what plainly doesn't apply): auth/authz,
validation, state management, feature flags, background jobs/queues/events, caching, retries,
idempotency, error handling, logging/observability, deployment behaviour.

For the specific behaviour the ticket is about, document the real execution flow with concrete
references — file paths, function/class/component names, route handlers, DB tables/migrations,
config keys, env vars. "The backend handles this" is not an answer; name the file and function.

## Step 4 — Root cause (bug/regression tickets)

Don't accept the ticket's stated cause at face value — verify it against the code. Classify your
conclusion as `CONFIRMED ROOT CAUSE`, `LIKELY ROOT CAUSE` (explain the gap), or
`ROOT CAUSE NOT YET CONFIRMED` (explain what more would nail it down). If the real cause differs
from what the ticket claims, say so plainly and show the evidence.

## Step 5 — Change surface, without scope-creeping it

Bucket every piece of work you can see coming into exactly one of:

- **Required** — needed to satisfy the ticket.
- **Supporting** — needed to safely enable the required change (a migration, a flag, a test seam).
- **Optional** — genuinely nice, not required; name it as optional, don't fold it into Required.
- **Out of scope** — things you noticed along the way that should explicitly NOT be touched now.

An investigation that quietly balloons into "and also we should refactor X" has failed this step.

## Step 6 — Dependencies, risks, security, performance (as relevant)

For each meaningful risk: what it is, why it exists, the potential impact, the evidence behind it,
and what mitigation it implies — don't list generic risk categories with nothing backing them.
Cover, where actually applicable to this ticket (don't manufacture relevance): internal/external
dependencies, API/DB/schema changes, backward compatibility, data migration, concurrency/race
conditions, retries/idempotency/duplicate processing, rollback, auth/authz/tenant isolation, input
validation, secrets/sensitive data handling, query performance/N+1/pagination, caching, rate
limits, timeouts. Tie every recommendation to evidence you actually found — not "this could
theoretically be slow."

## Step 7 — Testing landscape

Find what already tests this area (unit/integration/API/component/E2E, fixtures, mocks, CI config)
and what doesn't. Note existing patterns worth reusing and obvious regression risk if untested
paths change. **Do not write or implement any tests here** — this step only maps the landscape for
`spec-create` to plan against.

## Step 8 — Completion gate

Before writing the report, check you can actually answer (or have correctly marked UNKNOWN with
real justification, or flagged as a business decision) every one of:

what the ticket asks for · current vs. expected behaviour · where the current behaviour lives ·
how that flow actually works · why it behaves that way · confirmed root cause (if a bug) ·
affected repos/files · the real change surface · dependencies and risks · security considerations ·
performance/reliability considerations · existing test coverage · edge cases that matter ·
anything from optional context that changes scope · what's genuinely unknown · what needs a human
business decision.

If something on this list is still open and investigable, keep investigating — don't write the
report yet. If it's genuinely a product/business call, name the exact question that needs an
answer; don't invent one.

## Evidence labels

Tag non-obvious findings so `spec-create` knows how much weight to put on them:

- **VERIFIED** — confirmed directly in code, config, DB, tests, git history, the ticket, or official docs.
- **INFERRED** — well-supported by multiple signals but not directly confirmed; say why.
- **ASSUMPTION** — can't currently be proven; keep this list short, never hide one inside a
  recommendation as if it were fact.
- **UNKNOWN** — investigated and still open; say what you searched and why it didn't resolve.

## Step 9 — Write the report

Write it to `{specs_dir}/{feature-slug}/investigation.md` (`specs_dir` from config, default `specs`) in the repo (create the `specs/` folder if
needed — this mirrors where `spec-create` already keeps its own output, so the handoff reads
naturally from the same place; don't commit this folder if the repo's convention already
gitignores `specs/`, matching whatever this repo already does there). Use the structure in `references/report-template.md`.

Every section should be specific and evidence-backed, or explicitly say "None found" /
"Not applicable to this ticket" rather than being left looking like an oversight.

**Complexity Estimate** uses the same signals and tiers `spec-create` will apply per task: spread,
new design, data, concurrency, security, public contract, ambiguity, hard to verify. Security plus
data, or security plus concurrency, means `deep`. Say which model is worth planning this on, since a
deep ticket deserves the strongest model for `spec-create` too.

**Recommended Implementation Direction** describes the technically-supported direction the
evidence points to — reusing existing patterns the investigation actually found, not a novel
architecture invented on the spot. It is not permission to start building; flag any business
decision it depends on.

## Step 10 — Stop, hand off, don't bleed into the next stage

Report completion plainly:

```
Investigation complete.

Source: <ticket ID, or file / "pasted text">
Branch: <branch> (created from <base> @ <sha>)
Report: specs/<feature-slug>/investigation.md

Next step: run spec-create for <feature-slug> — it can read the investigation above directly rather than
re-discovering the system.
```

Do not run `spec-create` yourself unless the user explicitly asks you to chain into it in the same
turn. Never run `spec-implement` from here under any circumstance — that skips the human
review/approval step this workflow depends on.

## Hard boundaries (do not cross these)

- No implementation: no app code, API, schema, migration, UI, config, dependency, infra, or test
  changes. Finding an obvious one-line fix doesn't change this — document it, don't apply it.
- No code changes get committed or pushed from this skill — the only commit this skill produces,
  if any, is the empty ticket branch itself (creating a branch doesn't require a commit).
- Never touch the base branch.
- Never discard, stash, reset, or overwrite existing uncommitted work without being told to.
- Never force-push, never delete an existing branch without explicit approval.
- Never fabricate an answer to fill a gap — mark it UNKNOWN or as a business decision instead.
- Never silently expand scope based on optional context the ticket itself doesn't support.
