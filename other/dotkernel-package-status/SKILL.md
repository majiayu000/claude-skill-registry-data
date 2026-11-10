---
name: dotkernel-package-status
description: 'Choose, justify and verify PHP/Composer dependencies in Dotkernel projects, and answer whether a Dotkernel package is still maintained. Use this skill ANY time you are about to suggest, add, evaluate or replace a package, edit composer.json, run `composer require`/`composer remove`, or answer "what should I use for X" — including when the user only asks how to implement something a library could solve (mail, queues, caching, logging, validation, pagination, auth, CLI, fixtures, uploads, GeoIP, error handling, HTTP client). Also use when asked whether a Dotkernel package is still maintained, what a package does, which PHP versions it supports, whether it is safe for a new project, or what the state of the Dotkernel open-source portfolio is. Enforces this order — already installed, then dotkernel/*, then laminas & mezzio, then a vetted community package, then hand-rolled code — and answers from the published dotkernel.com listing rather than from memory. Also use whenever you catch yourself naming a package from memory.'
---

# Dotkernel package status and dependency policy

```text
Applies to
  Projects:  - all
  Packages:  - all
```

Dotkernel is a Mezzio/Laminas ecosystem with its own first-party `dot-*` layer. Most "I need a
library for this" moments are already solved inside the stack. Reaching outside it is a governance
decision, not a convenience.

## Source of truth

Dotkernel publishes the support status of its open-source packages as a machine-readable listing,
rebuilt daily from the GitHub organization. It is the only source this skill uses for `dotkernel/*`
packages. Prefer it over recollection: names drift, lifecycle states change, and a package that was
active at training time may be security-only now.

- Data: <https://www.dotkernel.com/dotkernel-packages.json>
- Human-readable page: <https://www.dotkernel.com/dotkernel-packages-oss-lifecycle/>
- Site that publishes both, and the code that generates them:
  <https://github.com/dotkernel/dotkernel.com>

The listing is a product of the dotkernel.com site rather than of any single package, so nothing
needs to be installed or generated to use it and it works from any repository. Fetch it fresh for
each question; do not save a copy into the project. Report a wrong or stale entry against
`dotkernel/dotkernel.com`, and a wrong lifecycle value against the package's own repository, which
is where the `OSSMETADATA` file that declares it lives.

### Shape

```json
{
    "generated_at": "2026-08-05T10:14:45+00:00",
    "org": "dotkernel",
    "packages": [
        {
            "name": "dot-cache",
            "url": "https://github.com/dotkernel/dot-cache",
            "description": "Dotkernel cache component",
            "lifecycle": "active",
            "php": "~8.3.0 || ~8.4.0",
            "archived": false
        }
    ]
}
```

- `name` - the bare repository name. The Composer package is `dotkernel/<name>`.
- `description` - the GitHub repository description; `null` when the repository has none.
- `lifecycle` - see below. Values outside the four listed are possible and mean the repository
  declared something unrecognized; report it as undeclared rather than guessing.
- `php` - the `require.php` constraint from the package's `composer.json`, or `null` when it
  declares none or the file could not be read. A `null` is missing data, not "any PHP version."
- `archived` - GitHub's own archived flag, which is independent of `lifecycle`. A repository can be
  archived on GitHub while still declaring an older lifecycle, and the page surfaces that as a
  separate "Archived on GitHub" note.

The listing carries no keywords, release dates, download counts or successor field. Do not present
any of those as coming from it.

### What each lifecycle means for a consumer

| Value | What to tell someone | As a new dependency |
| --- | --- | --- |
| `active` | Actively developed, new features and fixes. Safe for a new project. | Yes |
| `maintenance` | Still supported, receiving fixes but no new features. Safe to stay on; expect no new capabilities. | Yes, and say so |
| `security-only` | Only security fixes are released. Plan an upgrade or replacement now. | No — red flag, ask first |
| `archived` | No longer maintained. Do not use in new projects; migrate existing ones. | No |

Treat `archived: true` the same as the `archived` lifecycle, whatever `lifecycle` says.

### Querying it

```bash
curl -fsSL https://www.dotkernel.com/dotkernel-packages.json \
  | jq -r --arg q 'cache' '.generated_at, (.packages[]
      | select(((.name // "") + " " + (.description // "")) | ascii_downcase | contains($q))
      | "\(.name)  \(.lifecycle)  php=\(.php // "unknown")  archived=\(.archived)  \(.description // "")")'
```

Match on `name` and `description`, not on a guessed name. If the shell cannot reach the site, load
the human-readable page instead.

## The ladder — walk it in order, stop at the first hit

**0. Already installed.** Read `composer.json` and grep `composer.lock` before anything else.
Dotkernel API ships a large transitive tree (laminas-*, mezzio-*, doctrine/*, league/oauth2-server,
symfony components, psr/*). If a package is already in the lock file, use it — no new dependency.

```bash
jq -r '.require, .["require-dev"] | keys[]' composer.json | sort
jq -r '.packages[].name, .["packages-dev"][].name' composer.lock | sort   # full transitive tree
composer show | grep -i <keyword>                                         # installed packages only
```

**1. A `dotkernel/*` package.** Search the listing (see *Source of truth*). Prefer it even if a more
popular community package exists — consistency with the ecosystem and the maintainers' expectations
outweighs raw feature count. Only `active` or `maintenance`, not archived on GitHub, and a `php`
constraint that covers every PHP version this project's `composer.json` `require.php` allows.

**2. `laminas/*` or `mezzio/*`.** These are effectively first-party-adjacent: Dotkernel is built on
them, they are usually already in the tree, and `dot-*` packages are thin wrappers over them.

**3. A vetted community package.** Only when 0–2 genuinely cannot cover the need. Prefer
`symfony/*`, `doctrine/*`, `psr/*` and `league/*` — the stack already depends on them, so you are
widening an existing surface rather than opening a new one. It must be actively maintained,
installable on every PHP version this project's `require.php` allows, not abandoned, carry a real
license, and not duplicate something already in the tree. "Actively maintained" means a release in
the last 12 months — the rule of thumb the user applies when confirming the package; this skill has
no release dates to check it against itself.

**4. Write it yourself.** For a small, well-understood need (a value object, a 40-line helper, a
single middleware), in-tree code beats a dependency. Say so explicitly instead of silently picking a
package.

## Verifying a name

Never name a package from memory. A name is **verified** only when you read it in one of:

- this project's `composer.lock` (any vendor), or
- the dotkernel.com listing (`dotkernel/*` only).

Anything else — a `laminas/*`, `mezzio/*` or community package that is not already installed — is
**unverified**. Say so in those words, and hand its maintenance status, PHP support and license to
the user to confirm; this skill has no source for them.

If the listing cannot be fetched, say so and call every `dotkernel/*` name that is not in
`composer.lock` unverified. Do not fall back to remembered status, which is exactly what the listing
exists to replace.

## Answering status questions

- Cite `generated_at`. The listing is a daily snapshot, so say what it was current as of.
- Absence is not non-existence. A repository is only listed when it carries an `OSSMETADATA` file
  declaring its lifecycle, and the site excludes non-package repositories (documentation, skeleton
  projects, the site itself). If a name is missing, say it is not in the published package listing
  and check <https://github.com/orgs/dotkernel/repositories> - do not say it does not exist.
- For "is X maintained?", lead with the lifecycle sentence above, then the PHP constraint if the
  question is about upgrading.
- For "what should I use instead?", the listing gives no successor field. Say the package is
  archived or security-only, walk the ladder for the underlying need, and point at the GitHub `url`
  and the lifecycle page rather than inventing a replacement.

The JSON is served from the document root of dotkernel.com, so its URL tracks the deployed file
name. If the request 404s, load the human-readable page above and read the "View as JSON" link from
it, or check the `dataFile` setting in `config/autoload/packages.global.php` in
<https://github.com/dotkernel/dotkernel.com>.

## Contributing to dotkernel/api specifically

This is someone else's repository. Adding a dependency changes the dependency surface of every
downstream Dotkernel project.

- **Do not run `composer require` on a contribution branch.** Solve the problem with what is
  installed. If that is impossible, produce a proposal (below) and let the maintainers decide — the
  right first step is an issue or discussion on the repo, not a commit.
- A new dependency in a PR that was not agreed in advance is the most common reason a Dotkernel PR
  stalls. Flag this to the user before writing any code that assumes a new package.
- `require-dev` is not a free pass — CI runs it.

## Output format when a dependency is genuinely needed

Always show the work. Never present a single option as if it were the only one.

```text
Dependency proposal
Need:        <one line — the capability, not the package>
Installed?   <what you grepped, and why it does not cover the need>
Dotkernel:   <candidate — lifecycle, php, listing generated_at> or "none — searched: x, y, z"
Laminas:     <candidate, installed or unverified> or "none"
Community:   <candidate> — unverified: confirm a release in the last 12 months, PHP support and license
Recommend:   <choice> + one-sentence why
Alternative: <hand-rolled sketch, ~n lines>
Decision:    yours — I have not modified composer.json
```

## Where to look first, by need

Verify each against the listing and `composer.lock` — treat this as a search hint, not a source of
truth.

| Need | Look at |
| --- | --- |
| DI / factories via attributes | `dot-dependency-injection` |
| Routing, route groups | `dot-router` + `mezzio-router` |
| Errors, logging, error middleware | `dot-errorhandler`, `dot-log` |
| Mail | `dot-mail` (wraps symfony/mailer) |
| Caching | `dot-cache` |
| CLI commands | `dot-cli` + `laminas-cli` |
| Pagination / collections | `dot-paginator` |
| Input validation & filtering | `dot-inputfilter`, `dot-filter`, `dot-validator`, `laminas-inputfilter` |
| Authorization / RBAC / guards | `dot-authorization*`, `dot-rbac-guard` |
| API authentication | `league/oauth2-server` via `mezzio-authentication-oauth2` (already in API) |
| Doctrine fixtures | `dot-data-fixtures` |
| GeoIP | `dot-geoip` |
| Response headers | `dot-response-header` |
| Queues / async | `symfony/messenger`, wired the way stock Queue does it: `netglue/laminas-messenger` plus a transport such as `symfony/redis-messenger`. `dotkernel/queue` is a project skeleton to start a worker from — never `composer require` it |
| Scaffolding new code | `dot-maker` (generate, do not hand-write boilerplate) |
| HTTP client | whatever is in the lock file already — do not add guzzle if `symfony/http-client` is present |

## Red flags — stop and ask

- You are about to write a package name you did not read out of the listing or the lock file.
- The package solves a problem you have not confirmed exists in this codebase.
- It duplicates something already in `composer.lock` under a different vendor.
- Its PHP constraint excludes a version this project's `require.php` allows, or the listing's `php`
  is `null`.
- It is `security-only` or `archived` in the listing, or `archived: true` on GitHub.
- You are adding it to make a test pass.
