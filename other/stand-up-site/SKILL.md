---
description: 'Stand a site up on its own custom domain, from a repository that already serves one: the receiving repository and its deploy key, the DNS records, the publish that proves it works before the merge, and settling GitHub Pages afterwards. Invoke as `/stand-up-site <domain>`. Use when a second site joins the repo, or when a site moves to a new domain.'
---

End state: `https://<domain>` serves the new site over an approved certificate,
`www` and plain HTTP redirect onto it, and every site already published from
this repository still serves its own content.

**A repository gets one Pages site**, so every site after the first is published
to a **receiving repository** of its own — `.claude/rules/deployment.md` carries
the arrangement that follows, and what this skill stands up is its receiving
end.

**The domain is bought by the operator; its records are written by whoever can
reach the registrar.** Step 2 splits on that, and either way the site is dark
until they land, whatever CI reports.

The code half — the site directory, its `next.config.ts`, the site's entry in
the shared config — is ordinary work on the branch and is not this skill's;
CLAUDE.md § "Repository layout" and `.claude/rules/deployment.md` own it. This
skill starts where the build already produces the site and ends where the domain
serves it.

## Step 1 — The receiving repository and its key

```bash
gh repo create <owner>/<domain> --public -d '<one line saying what it serves>'
```

**Public is not a preference.** Pages on a private repository is a paid-plan
feature, so a private receiving repository fails at publish time rather than at
creation.

The workflow's `GITHUB_TOKEN` is scoped to this repository, so pushing to
another one needs a credential of its own — a deploy key, whose private half
never leaves the secret it is written into:

```bash
ssh-keygen -t ed25519 -N '' -C '<domain> pages deploy' -f tmp/deploy-key
gh repo deploy-key add tmp/deploy-key.pub --repo <owner>/<domain> \
  --title 'pages deploy from <source repo>' --allow-write
gh secret set <SITE>_PAGES_DEPLOY_KEY --repo <owner>/<source repo> < tmp/deploy-key
rm tmp/deploy-key tmp/deploy-key.pub
```

**The web container has no `ssh-keygen`.** Python's `cryptography` writes the
same pair: `Ed25519PrivateKey.generate()`, its `private_bytes` in `Encoding.PEM`
/ `PrivateFormat.OpenSSH` / `NoEncryption()` to `tmp/deploy-key` under
`umask 077`, and its public key in `Encoding.OpenSSH` / `PublicFormat.OpenSSH`,
plus the comment, to `tmp/deploy-key.pub`.

Print nothing and keep nothing: once the private half is in the secret, rotation
is the only way back, and the publish script's own header carries that contract
(`scripts/publish-site.sh` takes the site id and maps it to its receiver).

Give the receiving repository a README saying what it is and where its content
comes from. It is the only thing a person landing on a source-less repository
has to read.

## Step 2 — The DNS records

GitHub's Pages addresses are the same for every site, so the table is the same
every time, whoever writes it:

- **A** on `@` — `185.199.108.153` `185.199.109.153` `185.199.110.153`
  `185.199.111.153`
- **AAAA** on `@` — `2606:50c0:8000::153` `2606:50c0:8001::153`
  `2606:50c0:8002::153` `2606:50c0:8003::153`
- **CNAME** on `www` — `<owner>.github.io`

One record per value — four A rows and four AAAA rows, not one row holding four
addresses. Which repository answers is decided by the `CNAME` file inside each
published branch, which is why that file is part of the build.

**Read the zone first and name the records that conflict.** The two that bite
are a registrar's parking page: an `ALIAS`, `ANAME` or `A` on the apex, which is
the slot the A records need, and a wildcard `CNAME`, which answers for `www` as
well and would send it to the parking page. Mail (`MX`, `v=spf1` `TXT`) and the
registrar's own `_acme-challenge` rows never enter a web request. Say all of
that explicitly, so what happens is two deletions rather than a cleared zone —
and note that an exact `www` record beats a wildcard by specificity, so a
wildcard survives the change untouched.

### Where the registrar has an API

These domains are registered at **Porkbun**, whose API the agent drives given
two things: `PORKBUN_API_KEY` and `PORKBUN_SECRET_API_KEY` in the environment,
and **API access switched on for that domain** in Porkbun's own domain list. The
keys are account-wide but the toggle is per domain, which is both the trap — a
call against a domain without it fails on the domain, not on the key, so the
keys look wrong — and the safety rail: only the domains the operator has
switched on are reachable from here.

Both halves ride in the JSON body of every request; the API has no header auth.
That is why nothing here echoes a request body — no `curl -v`, no `set -x`,
since either writes the secret into the session log.

```bash
porkbun() { # <endpoint path> [<extra JSON object>]
  jq -cn --arg k "$PORKBUN_API_KEY" --arg s "$PORKBUN_SECRET_API_KEY" \
    --argjson extra "${2:-null}" '{ apikey: $k, secretapikey: $s } + ($extra // {})' |
    curl -sS -X POST "https://api.porkbun.com/api/json/v3/$1" \
      -H 'Content-Type: application/json' -d @-
}

porkbun "dns/retrieve/<domain>" | jq '.records[] | { id, type, name, content }'
porkbun "dns/delete/<domain>/<record id>"
porkbun "dns/create/<domain>" \
  '{ "type": "A", "name": "", "content": "185.199.108.153", "ttl": "600" }'
```

An empty `name` is the apex; `www` is the host alone, never the full domain.
Every response carries `"status": "SUCCESS"` or `"ERROR"` with a `message` and a
`code`. An error is an HTTP 400 that `curl -sS` exits 0 on, so the body is what
says whether the call worked.

### Where it does not

Hand the table over and say which records to delete. The operator does it at the
registrar, and nothing else in this skill proceeds until they report back.

### Verify from here, on either route

**There is no `dig` or `nslookup` in the container**, and `dig +short` missing
returns empty rather than failing, which reads exactly like "DNS not set":

```bash
python3 - <<'PY'
import socket
for host in ('<domain>', 'www.<domain>'):
    print(host, sorted({a[4][0] for a in socket.getaddrinfo(host, None)}))
PY
```

The apex should answer with all eight GitHub addresses. **`www` lags behind it
by the wildcard's TTL**, because the wildcard was already answering for that
name and the new `CNAME` cannot invalidate what resolvers have cached — so the
first read-back shows the apex moved and `www` still on the parking page. That
is the expected shape, not a failed record; wait the TTL out and read again
rather than rewriting records that are already correct.

## Step 3 — Publish before the merge

A manual run is the only way to serve the site before the merge, and a dispatch
from an unmerged branch publishes whatever it is told to — including sites whose
pages the branch also changes.

**So the run names one site.** The gate reads a scope off the commit subject on
a push and off the **site** picker on a manual run
(`.claude/rules/deployment.md`); naming one site is what keeps an unmerged tree
from republishing the others.

```bash
gh workflow run deploy.yml --ref <branch> -f site=<site>
gh run watch "$(gh run list --workflow=deploy.yml --branch=<branch> \
  --limit 1 --json databaseId --jq '.[0].databaseId')"
```

Confirm in the run's own job list that the other sites' jobs were **skipped**,
not merely green. That is the assertion — the picker held — and it is the one
thing a failed reading of it costs a live site.

**Only receivers are in range of a branch dispatch.** The Pages-native site
deploys through the `github-pages` environment, whose protection rules admit the
default branch alone, so its deploy job **fails** on any other ref — after its
build has passed — with "not allowed to deploy to github-pages due to
environment protection rules". That is the guard rail holding, not a failure to
chase, and it caps what a pre-merge publish can disturb: a picker naming
everything still cannot touch the site served from this repository's own Pages.
Weigh a dispatch against the receivers alone.

## Step 4 — Settle Pages on the receiving repository

**The push usually does this by itself.** GitHub takes a pushed `gh-pages` as
the source, reads the domain off `CNAME` and has the certificate approved before
anything asks, so the first call below answers `409 already enabled` and only
the second is needed. Run both anyway: the first is there for a receiving
repository that does not self-enable, and a 409 is an answer rather than a
failure.

```bash
gh api -X POST repos/<owner>/<domain>/pages \
  -f 'source[branch]=gh-pages' -f 'source[path]=/'      # 409 when self-enabled
gh api -X PUT repos/<owner>/<domain>/pages -F https_enforced=true
```

Read the config back when either surprises you — `source.branch`, `cname` and
`https_certificate` say which of the two states you are in.

## Step 5 — Register it in Umami

Every site counts its visits in the self-hosted Umami at
`stats.vovazakharov.com`, and `SiteConfig.analyticsId` is required, so a site
without a website there does not type-check. The agent makes it: user `agent`,
password `UMAMI_AGENT_PASSWORD` from the environment, in the team `Sites`, where
every site's website lives — the user's own list is empty, which reads like
nothing having been set up.

```bash
umami_token() {
  jq -cn --arg p "$UMAMI_AGENT_PASSWORD" '{ username: "agent", password: $p }' |
    curl -sS -X POST https://stats.vovazakharov.com/api/auth/login \
      -H 'Content-Type: application/json' -d @- | jq -r .token
}
TOKEN=$(umami_token)
TEAM=$(curl -sS https://stats.vovazakharov.com/api/me/teams \
  -H "Authorization: Bearer $TOKEN" | jq -r '.data[] | select(.name == "Sites") | .id')
curl -sS "https://stats.vovazakharov.com/api/teams/$TEAM/websites" \
  -H "Authorization: Bearer $TOKEN" | jq -r '.data[] | "\(.id) \(.domain)"'
jq -cn --arg d '<domain>' --arg t "$TEAM" '{ name: $d, domain: $d, teamId: $t }' |
  curl -sS -X POST https://stats.vovazakharov.com/api/websites \
    -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' -d @- |
  jq -r .id
```

List first and create only when the domain is not there. The `id` the create
returns is the site's `analyticsId`, committed in its `SiteConfig` entry.

## Step 6 — Verify what is served

Against the live URL, never against the source: the build that produced the page
is the thing under test, so reading the tree only confirms the input.

- `https://<domain>` answers 200, `https://www.<domain>` and `http://<domain>`
  both 301 onto it.
- The served HTML carries **this** site's title, description and card image —
  the failure a shared `src/` makes possible is one site publishing under the
  other's domain, and it looks like a working site.
- The body copy reaches its last line, and anything the branch changed about how
  it renders is there in the markup.
- The `<head>`'s Umami `<script>` carries **this** site's `data-website-id`.
- Assets and the 404 page answer — `.nojekyll` missing strips Next's `_next/`
  directory, and the page comes up unstyled rather than broken.
- **Every site already published from here still serves its own content.**

## Traps

- **A 404 on the new domain is `CNAME` not reaching the branch**, or DNS that
  has not propagated. The publish script asserts on `CNAME` and `.nojekyll`
  before pushing, so propagation is the likelier of the two.
- **A publish that lands before its DNS leaves no certificate requested**:
  `https_certificate` stays absent however long you wait, and re-saving the same
  `cname` does nothing. Clear it and set it again —
  `gh api -X PUT repos/<owner>/<domain>/pages -F cname=null`, then
  `-f cname=<domain>` — and it is approved within a minute.
- **A subdomain of a domain already served** takes one `CNAME` on its host at
  `<owner>.github.io` in Step 2, not the apex table, and the zone's wildcard
  stays. Publish before writing it: a `CNAME` at `<owner>.github.io` that no
  Pages repository claims is one anyone's repository can take over.
- **The new domain serving an existing site** means the apex records point
  somewhere else entirely — that is DNS, not the build.
- **GitHub's run-workflow form reads its input list off the default branch.** A
  picker still only on the branch under test is not in the form, and an unset
  picker falls back to publishing everything. Dispatch from the CLI, where
  `-f site=` goes through whatever the form knows.
