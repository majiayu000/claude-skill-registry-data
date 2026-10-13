---
name: multi-tenancy
description: This skill should be used when several customers, organizations, teams or workspaces share one application and their data must stay apart — and especially when a person can belong to more than one of them. Trigger phrases (English) include "multi-tenant", "organizations and members", "workspaces", "teams", "invite users to an org", "a user in two companies", "switch workspace", "agency with several clients", "tenant isolation", "demo account", "white label". Trigger phrases (Spanish) include "multi-tenant", "varias empresas en la misma app", "organizaciones y miembros", "invitar usuarios", "un usuario en dos empresas", "cambiar de espacio", "cuenta demo", "que un cliente no vea los datos de otro". It decides the membership model before the schema hardens, puts the tenant rule in one place, and covers the edges that leak — server functions, deletion, invitations and the shared demo. Use `data-modeling` for the schema itself and `rls-audit` to verify the policies.
---

# Multi-tenancy

Tenant isolation is one rule — "you only touch what belongs to an organization you are in" — that must hold in every query, every server function and every screen. This skill is about writing that rule **once** and about the places it is forgotten.

Analogy: an office building with several companies. The lobby is shared, each floor is private. The security model isn't a guard on every desk — it's one badge system that every door consults. The failures are never the front doors; they are the service elevator, the cleaning contractor with a master key, and the show floor left open for visitors.

## Discovery (max 3 questions, only if unknown)

1. Can one person ever belong to two organizations — a freelancer, an agency, a consultant, a founder with two companies?
2. Who creates an organization — anyone who signs up, or only you?
3. Is there a shared demo or sample account that strangers can enter?

## Step 1 — Decide the membership model now

| Model | Shape | Choose when |
| --- | --- | --- |
| **Single-org** | `users.org_id` | The answer to question 1 is a certain, permanent no |
| **Memberships** | `memberships(user_id, org_id, role)` + an active-org selection | Any doubt at all |

**Default to memberships.** The single-org shortcut saves a table today. Converting later, in one production app, meant touching 39 of 56 policies, 21 functions and 33 files — and exposed the side effects in Step 4.

## Step 2 — One choke point

Every policy and query asks **one function** for the caller's tenant — `current_org_id()` — instead of reading a column directly.

- With memberships it returns the **active** organization, after checking the caller is really a member of it.
- Because everything goes through it, changing the model later changes one function.
- The role check lives beside it and **filters by the caller's id**. Never ask "is there an admin row?" — the first row returned belongs to someone.

## Step 3 — "What I can see" is not "who is on the team"

These are two different questions, and conflating them is the commonest bug after a membership migration.

- *What I see* follows my active organization.
- *Who is on the team* is everyone with a membership in this organization, whatever they have open right now.

List teams from the memberships (a `team` view), never from a per-user "current org" field — otherwise a person working in their other company vanishes from user lists, assignment rules and public booking pages.

## Step 4 — Shared people: decide each of these explicitly

Once a person can be in two organizations, each of these has a wrong default:

- **Deleting an organization** must not delete its people. Check the `ON DELETE` of every foreign key between org and person.
- **"Remove user"** removes a membership. The account is deleted only when the last one goes.
- **Profile fields** (name, working hours, avatar) — can the admin of A edit them for someone shared with B? Usually: per-membership settings belong to the membership, identity belongs to the person.
- **Per-person integrations** (a connected calendar, a personal API key): which organization's data do they sync into?
- **Revoked access**: is the login disabled, or only the membership? Leaving the auth user alive keeps the password valid; re-inviting then collides with "email already exists".
- **Invitations**: a link opened while signed in as someone else should say so, not bounce to the dashboard. And a failed read while accepting is an error — never "this user has no organization", which can move a person out of the one they had.

## Step 5 — The service elevator: code that bypasses RLS

Anything running with a service key or as `SECURITY DEFINER` skips the policies. That code must apply the tenant rule itself:

- Take the tenant from the **verified session**, never from the request body or a function parameter.
- Add the tenant to **every** join and lookup inside it. A background job with the admin key that forgets one filter writes to another customer's client.
- Enforce "same tenant" in the schema with **composite foreign keys** — `(tenant_id, id)` referenced as a pair — so a row cannot point at a parent in another tenant even when code forgets.
- Use **one server-side gate** for "may this caller act here?" (active user, valid membership, current subscription). Then test that the server gate and the screen's own check agree for every role — two gates drift.

## Step 6 — The front door: who can create a tenant

Closing the sign-up page does not close sign-up. If a function creates an organization, it can be called directly — in one app, three strangers created organizations the same day through social login after the registration screen had been removed.

- Protect the **function that creates the tenant**, not the page that calls it.
- Get notified on every new organization.

## Step 7 — The show floor: a shared demo is a hostile tenant

A demo that visitors enter is an account controlled by strangers. Assume they will try every button and every API call.

- **Block spend**: no paid AI calls, emails or messages from the demo.
- **Block writes that persist**: no changing or disconnecting keys, no inserting or deleting shared records.
- **Enforce in the server and in the policies** ("the organization is not the demo"), not by hiding buttons.
- **Fail closed**: if the code cannot tell whether this is the demo, refuse.
- **No shared password in the bundle.** Issue a personal link that expires.
- **Demo data ages.** Seeded dates drift into the past; re-date them on a schedule, including derived columns the dashboards filter by.

## Step 8 — Tenant settings that are easy to forget

- **Time zone is tenant (or user) data, and something must write it.** A default nobody sets puts everyone in UTC: slots offered at five in the morning, two people seeing different times for the same appointment, day boundaries that cut off the evening.
- **Rate limits and quotas per tenant**, especially on public endpoints where you cannot rely on the visitor's IP.

## Handoff

Pass the membership model and the choke-point function to `data-modeling` (schema and indexes led by `tenant_id`), `auth` (roles), and `rls-audit` (verification from outside). Run `rls-audit` after any change to this model.

## Output

Deliver: the membership decision with its reason, the tables, the `current_org_id()` function and role check, the team view, the explicit answer to each item in Step 4, the server gate, the tenant-creation guard, the demo restrictions if there is one, and the cross-tenant tests (user of A acting on B, through the API and through each server function).

## Field notes

`references/field-notes.md` — the migration and the leaks these steps came from.

## Reference

PostgreSQL docs (Row Security Policies, composite foreign keys), AWS "Multi-tenant data isolation with PostgreSQL Row Level Security", the multi-tenancy sections of your BaaS's documentation. Pairs with `data-modeling`, `auth`, `rls-audit` and `secure-coding`.
