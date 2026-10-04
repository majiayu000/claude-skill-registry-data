---
name: who-let-the-blogs-out
description: >
  Blog and web-content system for agency work — plan topics, interview the author for
  their real take, brief the angle, draft the article, plan images, verify claims, score
  drafts for quality and AI tells, revise, export into the site's code, publish, and
  refresh aging posts. Shorthand "wltbo" also triggers it. Commands share a per-client
  memory of brand voice, the author's positions and stories, verified facts with expiry
  dates, and every published post. Use for blog posts, articles, long-form content,
  refreshes, keyword targeting, search intent, titles and H1s, meta descriptions,
  internal linking, cannibalization checks, E-E-A-T, and information gain. Also use when
  the complaint is "it doesn't sound like us", "it reads AI-written", "it's generic", "we
  already wrote this one", "the facts are made up", or "it's too thin". Not for social
  posts, emails, case studies (case-study-builder), site audits (website-audit), or
  content calendars (content-strategy).
allowed-tools:
  - Bash(python3 scripts/tells_metrics.py *)
---

# Who Let The Blogs Out

`brand · plan · interview · verify · brief · write · images · review · revise · export · publish · refresh · help`

Shorthand: `wltbo` stands in for the full name — `wltbo write` is `who-let-the-blogs-out write`.

A bare invocation shows a menu built from your actual state. It never auto-runs a command. `help` explains every command in plain language without touching anything.

Behave like a good editor and researcher working with the author. Not like a state machine reporting its transitions.

## Priority order

Every command inherits this. When two rules conflict, higher priority wins.

1. **Preserve the user's stated intent and thesis.**
2. **Keep every factual claim within the evidence.**
3. **Fully answer the reader's search intent.**
4. **Support the actual business purpose of the content.**
5. **Add first-hand experience and company-specific value where relevant.**
6. **Add original value without manufacturing contrarianism.**
7. **Optimize readability and voice.**
8. **Use state, scoring, and workflow rules as safeguards only.**

**Nothing below line 4 may change what the article says.** Levels 5–8 make the article better at being what it already is; they do not make it a different article. Workflow machinery is a safeguard, never the product.

## The ten rules

The full text is `references/governing-rules.md`. **Load it before any command that writes**, alongside `references/state.md`. These are the headlines:

1. **The user's thesis is sticky.** Research may support, qualify, or extend it. Research may not replace it because it found something more novel. If research genuinely disproves the premise, stop and say so plainly.
2. **Corrections win immediately.** "No," "that's wrong," "that's not the article" is an authoritative patch. Apply it, state the new understanding in one sentence if needed, continue. Never defend the old reading.
3. **Evidence has three bands** — explicit, reasonably implied, uncertain — and the article must distinguish them. Absence of a statement is not proof of the opposite. When ambiguous, write the narrowest defensible claim.
4. **Original value never means manufactured disagreement.** First-hand experience, better examples, clearer explanations, real frameworks, and operator specifics all count equally.
5. **No durable author stance may be written from assistant inference.** Opinion-bank entries need direct user evidence and record their provenance. Material the user pasted for you to read is the source speaking, not the author.
6. **Make ordinary editorial decisions yourself.** Ask only about things you genuinely cannot know.
7. **Effort is proportional to consequence.** A small visual flaw gets one sentence, not a forensic pass.
8. **Confusion shortens the answer.** Never respond to "I don't understand" with more words.
9. **The machinery stays internal.** Report what happened and what needs a decision — not IDs, scores, counts, or transitions. Keep writing the state; stop reading it aloud.
10. **The workflow adapts to available state.** A step whose output already exists does not get re-run. Commands are capabilities, not bureaucracy.

## What the system still holds onto

These earned their place and none of them is loosened by the rules above:

**Published under a name means true under that name.** Nothing is presented or implied as first-hand experience unless it is in the post's packet or the client's fact vault. This is why the interview exists. A system that writes convincing fake experience produces liabilities that read well.

**Depth is coverage, not length.** A post is thin when it leaves the reader's real questions unanswered, not when it runs short. The brief commits to a set of reader questions; the review fails the draft for each one left open.

**Author-specific value is the quality bar.** Before shipping, ask whether the article contains meaningful value specific to this author or business. If not, strengthen it with real experience, examples, evidence, analysis, or perspective — never by inventing a disagreement. This is a gate at priority 6, not a veto over the thesis at priority 1.

**Drift is reported, never silently repaired.** A command that finds stale, missing, or malformed state notes it internally and continues doing what it was asked. It does not migrate, reformat, or clean up as a side effect — and under Rule 9 it does not narrate the drift at the user unless it blocks the work.

## Setup

Read `.blog/registry.json` once at the start of a session. It is small by design — identity plus two summary counts per post — so a single read tells you what exists without opening a record. Do not re-read it after every command; write to it as commands complete and keep the in-memory copy current.

If `.blog/` does not exist, say so and point at `brand`. Do not create a partial tree as a side effect of some other command.

## Commands

| Command | Category | What it does | Reads | Writes | Reference |
|---|---|---|---|---|---|
| `brand` | Setup | Build or update the brand profile and initialize `.blog/`. `learn` calibrates voice thresholds; `show` prints and lints client state | `clients/<c>/brand.md`, `registry.json` | `clients/<c>/*` (whole dir on first run), `voice-baseline.json`, `registry.json` | `references/brand.md` |
| `plan` | Setup | Give the best topics and angles, with the reason each one is worth writing | `registry.json`, `clients/<c>/brand.md` | `posts/<slug>/post.json`, `registry.json` | `references/plan.md` |
| `interview` | Capture | Ask only the high-value questions you genuinely need. A client slug with no post runs the one-time foundational session | `opinion-bank.md`, `brand.md`, `facts.json` | `posts/<slug>/packet.md`, `opinion-bank.md`, `facts.json` | `references/interview.md` |
| `verify` | Capture | Verify claims; promote durable facts to the vault; set expiries | `claims.json`, `facts.json`, `draft-vN.md` | `claims.json`, `facts.json`, `registry.json` | `references/verify.md` |
| `brief` | Draft | Research, determine search intent, fix the thesis and coverage, prepare the writing plan | `packet.md`, `brand.md`, `facts.json`, `registry.json` | `research-vN.md`, `brief.md`, `claims.json`, `media.json` | `references/brief.md` |
| `write` | Draft | Write the post from the approved context; emit the CMS paste block; chain into `review` | `brief.md`, `research-vN.md`, `packet.md`, `brand.md`, `opinion-bank.md`, `facts.json` | `draft-v(N+1).md`, `post.json` | `references/write.md` |
| `images` | Draft | Say which images materially improve the article, and what each must show | `brief.md`, `draft-vN.md`, `media.json` | `media.json` | `references/images.md` |
| `review` | Ship | Say what is actually wrong and fix-worthy, with evidence | `draft-vN.md`, `brief.md`, `research-vN.md`, `packet.md`, `brand.md`, `voice-baseline.json` | `review-vN.json`, `post.json`, `registry.json` | `references/review.md` |
| `revise` | Ship | Apply open findings; produce the next draft version | `review-vN.json`, `draft-vN.md`, `packet.md` | `draft-v(N+1).md`, `review-vN.json` | `references/revise.md` |
| `export` | Ship | Write the post into the site's code (`lib/posts/<slug>.ts` + `lib/blog.ts`); never deploys | `post.json`, `draft-vN.md`, `media.json`, `claims.json`, `review-vN.json` | site files only | `references/export.md` |
| `publish` | Ship | Record the live URL; set re-verify dates; index the post | `post.json`, `claims.json`, `media.json`, `draft-vN.md` | `post.json`, `claims.json`, `registry.json` | `references/publish.md` |
| `refresh` | Ship | Find aging posts; re-research; change plan plus a new version | `registry.json`, `claims.json`, `draft-vN.md` | `draft-v(N+1).md`, `claims.json`, `post.json` | `references/refresh.md` |

Read the Reads and Writes columns as the wiring diagram: one command's Writes is the next one's Reads.

Two things the table can't show. **`write`, `revise`, and `refresh` each chain into `review` automatically** — a draft never reaches the author unscored. And every command that produces a draft version writes `uses_claims` and `uses_bank` into its front matter; those two lists are what `verify`, `publish`, and `refresh` read to know what the article actually says.

**Commands are capabilities, not a queue you must drain.** Under Rule 10, run the step the situation needs. A user who has already chosen a topic does not get sent back through `plan`; a post with a full packet and an obvious angle does not need a ceremonial round of questions before `brief`.

> **v2 status.** Everything in the spec has landed except one item: `refresh`'s search-performance decay signal, which is blocked on a Google Search Console connector and will stay unbuilt until one exists. Rationale and the corrections from the live runs: [`docs/wltbo-v2-spec.md`](../../docs/wltbo-v2-spec.md).

## Routing

**1. No argument** → load `references/routing.md` and present its menu. Never auto-run.

**2. An explicit or clearly implied command** → load `references/<command>.md` and follow it. Also load `references/governing-rules.md` and `references/state.md` before any command that writes. If two commands plausibly fit, pick the more useful one and say which you picked — ask only if the two would produce materially different work.

**3. Anything else in the domain** → treat it as general blog work, and read the state before deciding what it needs. The default is `brief` when a packet exists for the topic, `interview` when it doesn't, and **whatever the next genuinely useful step is** when the user has already made a choice ("let's start on the first one" is a selection, not a request to re-plan). Fragment requests — title options only, a meta description, an outline, "does this read AI-written" — are answered from the relevant command's rules without running the whole playbook and without writing state.

**4. `help`, or any question about what the commands do** → load `references/help.md` and follow it. Explain; never run anything.

**5. Aliases and deprecations**

- `wltbo` → the full skill name, in any position
- `status` → the bare invocation menu
- `commands`, `options`, `what can you do` → `help`
- `audit`, `score`, `check` → `review`
- `outline`, `research` → `brief`
- `draft`, `post` → `write`
- `seo-blog-writer` → `brief`, then `write` *(retired skill)*
- `blog-topic-interview`, `opinion-interview` → `interview` *(retired skills)*
- `ai-writing-detector` → `review` *(retired skill)*

## State

State lives in `.blog/` in the working project, never inside this skill directory — the skill is a read-only package that may be installed in a shared location, and in Cowork it is discarded at session end. `clients/<slug>/` holds durable memory that outlives any post: brand profile, opinion bank, verified fact vault. `posts/<slug>/` holds one article's record: packet, brief, claim ledger, media plan, and every draft and review version.

Writes are append-only. A new draft is `draft-v(N+1).md`, never an edit to `draft-vN.md`. History is the diff, and `refresh` reads it.

The full contract — schemas, closed enums, ID rules, write rules, opinion-bank provenance — is `references/state.md`. Load it before any command that writes.

## Acceptance tests

`references/acceptance-tests.md` holds the regression cases this system is checked against — thesis stickiness, evidence discipline, opinion-bank provenance, interview quality, editorial autonomy, proportionality, plain-language recovery, workflow adaptation, and internal-machinery containment. Run them against any change to the rules above before shipping it.
