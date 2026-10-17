---
name: manifestack-guard
description: Use before adding, removing or replacing an infrastructure dependency or vendor SDK - hosting, database, auth, email, storage, payments, monitoring, analytics, search, realtime, background jobs, queues, CMS, feature flags or AI APIs (for example "add Stripe", "set up Resend for emails", "install @supabase/supabase-js", "move auth to Clerk"), and when a hook reports that a new vendor was added. Checks the change against STACK.md requirements, the team's avoid list, budget, services already in the stack and revisit_when, and points to a full manifestack audit when limits need a look. Not for UI, styling, copy, tests or ordinary code changes.
license: MIT
compatibility: Node.js 22+ to run the bundled script. No network needed.
metadata:
  version: "0.5.1"
  homepage: https://manifestack.com
---

# Manifestack guard

A quick check before the stack changes. It reads `.manifestack/STACK.md` only; it does not run a full audit and does not read vendor pages.

`<skill-dir>` is the folder that contains this file.

## Steps

1. Run `node <skill-dir>/scripts/stack-md.mjs parse .manifestack/STACK.md` from the repository root.
   - `exists: false` → tell the user there is no `.manifestack/STACK.md` and suggest `/manifestack` (it records the stack and its limits). Then continue with their task.
2. Name the service being added, removed or changed, and its role (Hosting, Database, Auth, Email, Storage, Payments, Monitoring, Analytics, Search, Realtime, Jobs, CMS, Flags, AI, Other).
3. Check it against STACK.md:
   - **Requirements**: go through every item in `requires` one by one (data region, certifications such as SOC 2, SSO) and say for each whether this vendor meets it or needs checking. A payments, email or auth vendor holds customer data, so a data-region rule applies to it as much as to the database. Do not guess the answer; do not skip an item.
   - **Avoid**: does the vendor, its cloud or the setup it needs match anything in `avoid`? Quote the line.
   - **Budget**: quote the `budget` line and say the paid plan's price needs checking against it; the guard reads no prices.
   - **Limits**: name the plan limits that matter for how this service will be used, as things to check (by name, without numbers): daily and monthly send caps for email, billed users for auth, storage and egress for databases and files, API rate limits for payments or AI. A welcome email that works in testing and stops at the free daily cap on launch day is exactly what this check is for.
   - **Overlap**: is there already a section with the same role (a second auth provider, a second email sender)? Not for `Other`, which holds unrelated jobs, or for two services of one cloud (Lambda and CloudFront, both AWS).
   - **Priority**: if `priority` is set, does the change go against it? A service the team must run itself under `least ops`, a proprietary API at the core under `control`, a paid convenience add-on under `lowest cost`. One line, no verdict.
   - **revisit_when**: run `node <skill-dir>/scripts/stack-md.mjs check .manifestack/STACK.md`. A `triggered` section touched by this change is worth a full audit.
   - **decided**: does the change contradict a recorded decision? Quote it.
4. Report in two to four lines:
   - nothing to flag → say so in one line and continue;
   - a conflict or a new vendor → say what it is and suggest checking it before relying on it: `/manifestack audit` when STACK.md exists, `/manifestack` when it does not (it records the stack first). When the change replaces one vendor with another (auth from Clerk to Auth0), suggest `/manifestack compare clerk auth0` instead. Do not block the user's task.
5. If the user confirms the change, offer to add a section for the new service to STACK.md. Write it only on a yes, and only what is known without reading pages: `plan` as the user named it, `env` names, and `source: unverified`. Never `limit` or a price: those come from the audit, which reads the vendor's page. Write the JSON with your file tool to `.manifestack/tmp/set.json`, then run the script (the file works in every shell and nothing in it is expanded):
   ```json
   {"plan": {"value": "Free", "comment": "user 2026-10-08"}, "env": "ACME_API_KEY", "source": {"value": "unverified", "comment": "added by guard 2026-10-08; run /manifestack audit"}}
   ```
   ```bash
   node <skill-dir>/scripts/stack-md.mjs set --section "Email: Acme Mail" --json .manifestack/tmp/set.json
   node <skill-dir>/scripts/stack-md.mjs lint .manifestack/STACK.md
   ```

## Rules

- The check itself changes nothing. Afterwards the user's task goes on as usual: if they asked to add Stripe, adding the dependency, the code and the env var names is their request, not something the guard needs a second yes for. Only STACK.md waits for a yes.
- Never ask for API keys or read env values; env var names are enough.
- Do not state a vendor's prices, regions or certifications from memory. The guard reads no pages; say what needs checking and leave the facts to the audit.
- No vendor rankings or "use X instead". Point out the conflict; the choice stays with the user.
- Keep it short. The full rules are in `references/security.md`.
