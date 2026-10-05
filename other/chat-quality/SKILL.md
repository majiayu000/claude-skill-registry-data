---
name: chat-quality
description: "Biweekly loop that turns real chat feedback into eval coverage. Read the thumbs verdicts from the live Redis, join them to the logged exchanges, grow the golden set from actual failures, run the answer-quality eval, and land the fixes on a local branch for approval. Use when asked to run the chat quality loop. Never pushes, merges, or deploys."
icon: reviews
displayDescription: "Reads the site chat's own report card: every thumbs verdict a visitor left, joined back to the logged exchange it rates. Disliked answers become golden-set regression cases, the answer-quality eval runs against the updated set, and the fixes land on a branch with a plain-English report for approval. One of the loops described on the Loops page."
invoke: ["run the chat quality loop","/chat-quality"]
---

# chat-quality

Biweekly loop closing the site chat's feedback cycle. The widget's thumbs verdicts land in Redis and, until this loop, nothing ever read them. Each run joins the verdicts to the exchange log, turns real failures into golden-set regression cases (the standing rule in `evals/chat/README.md`), runs the eval, and hands the fixes over on a local branch. **Never push, merge, or deploy — the user approves every change.**

## When invoked

Run when asked to "run the chat quality loop" (`/chat-quality`), or by a scheduled task once one is created.

## Scope guardrails (read first)

- **Read-only on the live Redis.** `SCAN`, `GET`, `LRANGE`, `LLEN` against `chat:*` keys only — never `SET`, `DEL`, `EXPIRE`, or anything that writes. The logs are production evidence with a 30-day TTL; this loop observes them.
- **Visitor privacy.** Logged questions are visitors' own words and may carry personal details. They may appear verbatim in the local report, never in the committed diff: a golden-set case gets a paraphrase that preserves the failure, not the visitor's sentence. Visitor hashes never leave the report.
- **One eval run per loop.** `npm run eval:chat` spends real API budget (golden set × 3 repeats). Run it once, after the golden-set changes, not iteratively.
- **Fixes stay inside the chat's answer pipeline**: `evals/chat/golden-set.json`, corpus sources (page prose, `corpus-facts()` blocks, the generator's exclusions), the persona in `website/src/app/api/chat/persona.ts`, and the chat's lookup-tool layer — the `CHAT_TOOLS` definitions in `website/src/app/api/chat/route.ts` and their shared implementations in `website/src/lib/site-tools.ts` (a disliked prop or token answer can be a tool-description or lookup bug, and `site-tools.ts` also serves `/api/mcp`, so a fix there changes both surfaces). No UI, no components, no guardrail-cap changes (spend caps are the user's call — propose, don't edit).
- **Local branch only.** Never push or touch the user's working tree — follow the temporary-worktree recipe in `.claude/skills/growth-loop/SKILL.md` (step 4), branch name `chat/YYYY-MM-DD-<slug>`. Skip the worktree entirely when there is nothing to encode.

## The loop

### 0. Close the previous loop

Read the newest report in `evals/chat/loop-reports/` (git-ignored, local-only). Note whether its branch was merged; don't re-propose a case a previous run already encoded. First run ever: say so and move on.

### 1. Pull the verdicts and the log

Credentials are `KV_REST_API_URL` / `KV_REST_API_TOKEN` in `website/.env.local`. They are often **commented out** there so local dev fails open — read the values from the file either way; never uncomment them or export them into a dev server. If the file has no values at all, stop and ask the user for read access; there is no loop without the data.

Query the Upstash REST API directly (plain `curl`): `SCAN` for `chat:feedback:*` and `GET` each verdict; `LRANGE` the day lists for the window since the last report (key format and entry shape are owned by `website/src/app/api/chat/guardrails.ts` — read `logKey`/`ExchangeLog` there rather than trusting a remembered shape). Join verdicts to log lines by exchange `id`.

### 2. Triage

Every **down** verdict is a golden-set candidate: read the question, the answer, and the page it was asked from. Also skim the unrated exchanges for silent failures — invented paths, guardrail notices where a real answer was possible, questions the corpus plainly couldn't answer. **An empty or all-up window is a valid outcome**: write the short report and stop. Don't manufacture cases from answers that were actually fine.

### 3. Encode the failures

Apply the standing rule from `evals/chat/README.md`: each real failure becomes a golden-set case **before** it is fixed — paraphrased question, its `requiredFacts`, and the cheapest assertion that would have caught it, with the case's `description` citing the rule ids it covers per `evals/chat/SPEC.md` (a failure no rule covers means the spec gains the rule in the same change). If a required fact is missing from the corpus, that's the actual bug: fix the source (page prose or a `corpus-facts()` block), and `scripts/validate-chat-coverage.mjs` will hold the new case to the regenerated corpus. The one exception: a failure whose facts live in the generated prop or token data is answered by the chat's lookup tools, not the corpus — its case is marked `source: tools` and carries empty `requiredFacts` (the standing-rule section in `evals/chat/README.md` and rule T4 in `evals/chat/SPEC.md` own the convention); never fix one by stuffing a prop fact into page prose.

### 4. Run the eval

Follow `evals/chat/README.md` exactly — it owns the procedure (the `website-eval` launch entry / `npm run dev:eval -w website`, the port-3000 gotcha, `npm run eval:chat`) and how to read the transcripts (seat by seat; the aggregate score is noise). The question being answered: do the new cases fail before the fix and pass after, and did nothing that previously passed regress?

### 5. Fix on a branch

Worktree recipe from the growth-loop skill, branch `chat/YYYY-MM-DD-<slug>`. One coherent batch: the new golden-set cases plus the corpus/persona fixes they demanded. A persona or tool-definition edit updates its matching rule row in `evals/chat/SPEC.md` in the same commit, and a new rule ships with either a tripwire or an explicit unenforced entry there. Verify the website build in the worktree; commit the regenerated corpus when page prose changed (the commit-scope rule in the growth-loop recipe).

### 6. Report and hand off

Save to `evals/chat/loop-reports/YYYY-MM-DD.md` **and** repeat in full in the final message: the window, verdict counts (up/down/total exchanges), each disliked answer and the diagnosis, what was encoded, the eval result, and the branch name. Plain English. End with the approval step: merging the branch (or saying `ship`) approves it; deleting it rejects it. Nothing is pushed or deployed.
