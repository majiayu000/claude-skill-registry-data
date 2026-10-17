---
name: publish-artifacts
description: 'Publish HTML artifacts (mockups, demos, reports, prototypes) from a local folder tree to a Cloudflare-hosted site at ubuilt.dev, preserving the folder structure as URL paths, with per-folder access control — some folders public, others gated behind email one-time-PIN for named collaborators who need no Cloudflare account. Additive and multi-machine safe: every publish reconciles against live Cloudflare state (R2 objects + Access apps) and never clobbers what another machine pushed. Use when the user says "publish this artifact / mockup / prototype", "share this with <person>", "put this folder behind email auth", "publish to ubuilt.dev", "make this folder public / protected", "unpublish X", or otherwise wants to deploy an HTML tree to their Cloudflare artifacts site and control who can see each part.'
---

# publish-artifacts

Turn a local folder of HTML artifacts into a live site at your domain, where the folder tree *is* the URL structure and each top-level folder is either public or locked to specific people by email one-time-PIN. Driven by one declarative `manifest`, safe to run from any machine.

## Config — your specifics, in one place

Three values personalize this skill. They live in the **manifest** (the single source of truth). Nothing instance-specific is committed: the repo ships a generic `worker/wrangler.toml.template`, and **init generates `worker/wrangler.toml`** (gitignored) by substituting these values — wrangler can't read JSON, so this generation step is the bridge.

| Key | Example | Used for |
| --- | --- | --- |
| `site` | `ubuilt.dev` | the apex the Worker serves, and the host in every Access app `domain` |
| `bucket` | `artifacts` | the R2 bucket that holds the objects |
| `worker` | `ubuilt-artifacts` | the Worker name |

Throughout this doc `ubuilt.dev`, `artifacts`, and `ubuilt-artifacts` are **concrete examples** — read them as your Config values. To point the skill at a different domain: set these three in the manifest, then run setup (which regenerates `worker/wrangler.toml` from the template). The Worker code itself hardcodes nothing — it serves whatever the bound bucket holds.

## Mental model

- **The folder tree is the URL map.** `mockups/clientA/home.html` → `https://ubuilt.dev/clientA/home.html`; `clientA/index.html` → `https://ubuilt.dev/clientA/`. What you publish is exactly what the structure says.
- **Storage is additive.** Files live as objects in a private **R2** bucket. Publishing *adds or overwrites* the files you have locally; it never deletes what isn't in your tree. Removing something is an explicit `unpublish`.
- **The cloud is the source of truth — there is no local state file.** Every run *pulls* current Cloudflare state (R2 object list + Access apps) and reconciles your manifest against it. Run it from three machines; they converge, they don't fight.
- **Access is per top-level folder.** A folder is `public` (no gate) or `protected` (gated to an allow-list via a Cloudflare Access app scoped to `ubuilt.dev/<folder>/*`). Uncovered paths stay open; covered paths are deny-by-default.
- **Collaborators need no account.** Protected folders use the built-in **Email One-Time-PIN** IdP: the visitor enters their email, gets a code, and they're in if their address is on the folder's allow-list.
- **Placement = audience.** A top-level folder is at once the URL prefix *and* the access boundary, so **where you put a file decides who can see it.** Group by audience first: decide the destination folder (confirm with the user if not obvious) *before* generating artifacts; one audience per top-level folder (two allow-lists need two folders); keep cross-cutting assets in `public/` only if they're not sensitive.

## Architecture

Three moving parts, two of them set up once:

1. **A private R2 bucket** (`artifacts`) — the additive object store. *Stays private* — only the Worker reads it.
2. **One serving Worker** bound to the bucket, on the `ubuilt.dev` custom domain with `workers_dev = false` — maps request path → R2 key, handles `index.html`, content types, and 404. Deployed once; only changes if you edit serving logic.
3. **Per-folder Access apps** — created/updated on every publish to match the manifest.

Each request to a protected path hits Access *at the edge first* (gate), then the Worker (serve). A private bucket + `workers_dev = false` means there is no way to reach protected bytes except through the gated hostname.

### The serving Worker

Ships in `worker/` and is the source of truth: a generic `src/index.ts` + `wrangler.toml.template`. The Worker maps request path → R2 key, but **path normalization is a security boundary here, not a convenience** (see invariant 6): Access gates the *raw* request path against `/<folder>/*` while the Worker resolves the *decoded* path, so the Worker must never serve bytes for a non-canonical path. It 404s encoded separators (`%2F`/`%5C`) and `..` traversal, body-less-301s any non-canonical form (un-normalized `//`, `/.`, or a **bare directory path with no trailing slash**) to its canonical trailing-slash URL, and only then serves — trying `path`, then `path.html`, then the trailing-slash `index.html`. It sets the content-type plus `Cache-Control: no-store` and `X-Content-Type-Options: nosniff`, and 404s otherwise. **Read `worker/src/index.ts`** before changing serving logic — don't reproduce it from memory, and never "simplify" the normalization away (that reintroduces a gate bypass). Init generates the gitignored `wrangler.toml` from the template by substituting `__WORKER__`/`__SITE__`/`__BUCKET__` from the Config (this is where `workers_dev = false` and the custom-domain route live).

## One-time setup

On first use, detect whether setup exists; if not, run `init` — a *detect-then-generate* routine (the same pull-and-reconcile philosophy as publish). **No API token — everything authenticates via browser OAuth.** It probes the account, generates `worker/wrangler.toml` from the template, and deploys with:
```
npx wrangler deploy --cwd "<this-skill-dir>/worker"
```
A few steps are the human's (`wrangler login`, enabling R2, confirming OTP, installing Cloudflare's plugin); the agent runs the rest and **reports a status table** (each piece `✓ exists` / `created` / `needs you`).

Setup is done when: `wrangler whoami` succeeds, the `artifacts` bucket exists, the Worker responds on `https://ubuilt.dev/`, OTP is on, and the Cloudflare MCP (full-API, which is how Access is managed) is connected.

**The full walkthrough — probe table, R2 enablement, the plugin install, and the exact human-only gates — is in [`reference/setup.md`](reference/setup.md). Read it whenever setup is missing or incomplete.**

## The manifest — folder → access

A single file at the **root of the local artifacts tree**, named `artifacts.manifest.json`. It declares, per top-level folder, who can see it. Folders not listed inherit `default`.

```json
{
  "site": "ubuilt.dev",
  "bucket": "artifacts",
  "worker": "ubuilt-artifacts",
  "default": "public",
  "folders": {
    "public":  { "access": "public" },
    "landing": { "access": "public" },
    "clientA": { "access": "protected", "allow": ["jane@acme.com", "@acme.com"] },
    "clientB": { "access": "protected", "allow": ["bob@globex.com"] }
  }
}
```

The `site` / `bucket` / `worker` keys are the [Config](#config--your-specifics-in-one-place) — they must match `worker/wrangler.toml`. `default` + `folders` are the per-tree access map.

Rules for `allow` entries:
- A string **with a local part** (`jane@acme.com`) → exact email (`include: {email: {email: …}}`).
- A string **starting with `@`** (`@acme.com`) → anyone at that domain (`include: {email_domain: {domain: "acme.com"}}`).
- A `protected` folder with an **empty or missing `allow` is fail-closed** (nobody gets in). That's safe but pointless — **warn** the user and ask for emails before publishing it.

If there's no manifest yet, infer a draft from the tree (every top-level folder → `default`) and show it for confirmation before publishing. Never invent allow-lists; ask who each protected folder is for.

## Publish — the per-call operation

Inputs: a local artifacts directory (default: the cwd if it has a manifest, else ask). The operation is **idempotent** and **additive**.

1. **Resolve + validate.** Find the artifacts root and its `artifacts.manifest.json`. Validate every `protected` folder has a non-empty `allow`. Confirm the destination is `ubuilt.dev`.
2. **Auth + setup check.** Ensure `wrangler` has an OAuth session (`wrangler whoami`) and the Code Mode MCP is connected; confirm the bucket + Worker exist (run one-time setup if not). No token needed.
3. **Upload assets to R2 (additive).** For every file under the root, preserving relative path as the R2 key:
   ```bash
   wrangler r2 object put "artifacts/<relpath>" --file="<abspath>" --content-type="<type>" --remote
   ```
   The key (`clientA/home.html`) is exactly what the Worker resolves. This only *adds/overwrites* the local files — nothing else in the bucket is touched, so concurrent machines stay additive. For large trees, `rclone copy <dir> r2:artifacts` (against the R2 S3 endpoint) is a faster equivalent.
4. **Pull current Access state.** List existing Access apps and keep only the ones this skill manages — identify them by `domain` starting with `ubuilt.dev/` **and** name starting with `artifacts/`. Never read/modify apps outside that namespace (that's how we avoid clobbering anything else on the account). Code Mode MCP: `execute()` a `GET /accounts/{id}/access/apps`.
5. **Reconcile per top-level folder** (desired = manifest, actual = step 4):
   - **public** → ensure **no managed app** covers `ubuilt.dev/<folder>/*`. If one exists from a prior run, delete it. (No app = open, because we leave "Require Access protection" off.)
   - **protected** → ensure a policy with the folder's allow-rules exists, and an app `artifacts/<folder>` at `ubuilt.dev/<folder>/*` references it. Create if missing; update allow-list/policy if it drifted from the manifest. Keyed on the domain so re-runs update in place rather than duplicating.
   - Leave unmanaged apps and unrelated folders untouched.
6. **Report** (see Reporting style): each folder's URL, access, and who — plus exactly what changed this run.

### Access reconciliation — the API shapes

Token-free path: the Code Mode MCP `execute()` calling the Access endpoints. Create/update a **policy** (reusable), then reference it from the **app** — these are the shapes `execute()` sends:

- **policy** → `POST …/access/policies` with `{ name: "artifacts/<folder>", decision: "allow", include: [...] }`, where `include` is built from the folder's `allow`: an exact email is `{email:{email:"jane@acme.com"}}`, an `@domain` entry is `{email_domain:{domain:"acme.com"}}`.
- **app** → `POST …/access/apps` with `{ name: "artifacts/<folder>", type: "self_hosted", destinations: [ {type:"public", uri:"ubuilt.dev/<folder>"}, {type:"public", uri:"ubuilt.dev/<folder>/*"} ], session_duration: "24h", app_launcher_visible: false, allowed_idps: [], policies: ["<POLICY_ID>"] }`.
- **Scope to BOTH `ubuilt.dev/<folder>` and `ubuilt.dev/<folder>/*`.** The wildcard alone does **not** cover the bare folder path (`/<folder>` with no trailing slash), which the Worker still resolves to `<folder>/index.html` — gating only `/*` leaks the folder's index at the no-slash URL. Listing both seals it at the edge (defense-in-depth with the Worker's bare-path redirect and `%2F` rejection — neither layer alone is sufficient: Access can't see through `%2F`, and the Worker redirect still briefly reveals the folder's existence). Access resolves most-specific path first, so siblings stay open. `allowed_idps: []` = all configured login methods, which includes One-Time-PIN.
- Updates use `PUT …/access/apps/<id>` and `…/access/policies/<id>`, keyed on the domain so re-runs update in place rather than duplicating.

**Verbatim `curl` bodies, the `destinations` fallback shape, and the optional API-token (headless/CI) path are in [`reference/access-api.md`](reference/access-api.md).**

`unpublish <path>`: delete the matching R2 objects (`wrangler r2 object delete "artifacts/<relpath>"`) and, if a whole protected folder is removed, delete its managed Access app + policy. **Confirm before deleting** — deletion is the one non-additive action.

## Security invariants — never violate

1. **`workers_dev = false` stays in `wrangler.toml`.** A live `*.workers.dev` route serves the same Worker on an *ungated* hostname — a complete bypass of Access. If it's ever re-enabled (a dashboard toggle can silently flip it back on next deploy unless the config says false), protected content leaks. Verify after every Worker deploy.
2. **The R2 bucket stays private.** Never enable its `r2.dev` public URL or attach a public custom domain to the bucket — that exposes objects directly, around the gate. Only the Worker's binding reads it.
3. **Leave the account "Require Access protection" setting OFF.** With it off, uncovered paths are public (what we want for `public/` folders) and covered paths are gated. If it were on, every public folder would need an explicit Bypass policy — more moving parts, easy to get wrong.
4. **Protected = deny-by-default.** An app with no allow-policy lets nobody in; a protected folder with an empty `allow` is fail-closed. Safe, but warn rather than publish a folder no one can open.
5. **Only touch the `artifacts/` Access namespace.** Manage exactly the apps you created (name `artifacts/*`, domain `ubuilt.dev/*`). Pull-then-reconcile; never bulk-delete or assume local state is authoritative.
6. **Path normalization is part of the gate.** Access matches the *raw* request path against `/<folder>/*`; the Worker serves the *decoded* path. A mismatch leaks: `ubuilt.dev/<folder>` (no trailing slash) and `ubuilt.dev/<folder>%2F…` (encoded slash) both fall outside the `/*` rule yet resolve to `<folder>/index.html`. Close it on both layers — the Worker rejects `%2F`/`%5C`/`..` and body-less-redirects every non-canonical path to its canonical URL before serving, **and** every protected app is scoped to both `<folder>` and `<folder>/*`. Never weaken either. Verify the no-slash and `%2F` forms after every publish (see Reporting).

## Tools & auth

**Default auth is OAuth — no API token.** `wrangler login` (browser; all scopes incl. R2) covers Worker deploy + R2 uploads; the **Code Mode MCP** (`https://mcp.cloudflare.com/mcp`, OAuth) covers Access — `wrangler` can't manage Access. Both are per-machine browser logins — nothing secret to copy between machines.

| Job | Primary | Fallback |
| --- | --- | --- |
| Deploy/redeploy the Worker | `wrangler deploy` | Code Mode MCP `execute()` |
| Upload / delete R2 objects | `wrangler r2 object put/delete` (or `rclone` for bulk) | Code Mode MCP / S3 API |
| List current R2 / Worker state | `wrangler r2 object list`, `wrangler deployments` | connected Cloudflare MCP (read-only) |
| Create/update/list Access apps + policies | Code Mode MCP `execute()` | REST API `curl` + token |

The older connected Cloudflare MCP (`Cloudflare_Developer_Platform`) is read-only and can't write Access — use it only to *read* state. An API token is optional, only for headless/CI — see [`reference/access-api.md`](reference/access-api.md).

## Reporting style

After a publish, one compact table plus a one-line changelog. Example:

```
Published 3 folders to ubuilt.dev  (R2: +4 files, Access: 1 app updated)

  folder     URL                          access      who
  ───────    ─────────────────────────    ─────────   ─────────────────────
  public/    https://ubuilt.dev/public/   public      anyone
  clientA/   https://ubuilt.dev/clientA/  protected   jane@acme.com, @acme.com
  clientB/   https://ubuilt.dev/clientB/  protected   bob@globex.com

  Changed: clientA allow-list +@acme.com · uploaded clientA/home.html, clientA/flow.html, public/index.html, public/style.css
```

Always show the actual URLs (they're clickable and the point of the whole thing), the access state, and the allow-list for protected folders. When a protected folder is new, call out the first-visit flow: "clientA is gated — jane@acme.com will get a one-time PIN by email on first visit." Never print the API token. Never dump full R2 listings unless asked.

**Verify the gate, not just the happy path.** After publishing a `protected` folder, confirm it is sealed from *every* URL shape — not only the trailing-slash one. All of these must return a 302 to `*.cloudflareaccess.com` (or 404), never 200 with the content:
- `https://<site>/<folder>/` (trailing slash)
- `https://<site>/<folder>` (**bare, no slash** — the classic miss)
- `https://<site>/<folder>%2F` and `https://<site>/<folder>%2Findex.html` (**encoded slash** — bypasses path-scoped Access if the Worker decodes it)

A quick check: `curl -sI "https://<site>/<folder>" | grep -i location` should point at the Access login. A `public` folder instead serves 200 at `/<folder>/` and 301s the bare path to it. Treat any 200-with-content on a protected vector as a leak and fix before reporting success.

## Files

- `<artifacts-root>/artifacts.manifest.json` — the Config (`site`/`bucket`/`worker`) + per-folder access map (committed with the artifacts; it's the source of intent).
- `worker/` **inside this skill** — the serving Worker. Committed + generic: `src/index.ts`, `wrangler.toml.template`, `.gitignore`. **Not committed (gitignored), so not distributed:** `wrangler.toml` (generated from the template at init), `.wrangler/`, `node_modules/`.
- `reference/` — `setup.md` (one-time setup walkthrough) and `access-api.md` (verbatim Access API bodies + the CI token path). Read on demand, not on every publish.
- No machine-local state that matters. The current truth of what's published always lives in Cloudflare (R2 objects + Access apps) and is pulled fresh each run.
