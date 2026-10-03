---
name: dependency-supply-chain
description: Audit and defend against malicious dependencies in npm, pnpm, PyPI, and similar ecosystems. Covers lockfile hygiene, the limits of npm audit, behavior-level scanning with socket.dev, postinstall script review, typosquat and slopsquat detection, and minimum-permission CI runs. Invoke when adding a new dependency, after a supply-chain incident, or as periodic audit.
---

# Dependency / Supply-Chain Security

The supply chain is the part of your stack you trust by default and rarely review. npm, PyPI, RubyGems, Maven, Go modules — they have all hosted malicious packages, typosquats, and compromised maintainer accounts at scale.

This skill is the working developer's defense — pragmatic checks that fit in a normal workflow, not a software bill-of-materials regulatory program.

## When to invoke

- Adding a new dependency to a project (especially a small / new / single-maintainer one)
- After a publicized supply-chain incident affecting your ecosystem
- Quarterly audit of `package.json` / `requirements.txt` / `go.mod`
- Inheriting a project with a large `node_modules` and no obvious hygiene
- CI/CD just leaked a secret — start here to find which dep grabbed it

## The threat model

What can a malicious dependency actually do?

- **Read environment variables / files during install** (postinstall script)
- **Read environment variables / files at runtime** (any code path)
- **Exfiltrate via outbound HTTPS** to any host
- **Modify other dependencies** (link-stage tampering, build-script monkey-patching)
- **Hide payloads in transitive deps** so your `package.json` looks clean

You cannot inspect every line of every dependency. You can raise the cost of attacks and detect them when they happen.

## Lockfile hygiene

A lockfile is the only thing standing between "I added one dep" and "my install grabbed 1,200 transitive deps any of which can be swapped tomorrow".

- **Commit the lockfile.** Always: `package-lock.json`, `pnpm-lock.yaml`, `yarn.lock`, `poetry.lock`, `Pipfile.lock`, `go.sum`. No exceptions.
- **`npm ci` (or `pnpm install --frozen-lockfile`) in CI**, not `npm install`. `install` can mutate the lockfile silently; `ci` errors if the lockfile and `package.json` disagree.
- **Lockfile drift alerts.** A PR that touches `package-lock.json` but not `package.json`, or vice versa, deserves a review comment. Add a CI check.
- **Pin direct dependencies tightly** when the dep is small / new / sketchy. `"left-pad": "1.3.0"` rather than `"left-pad": "^1.3.0"`. The caret invites unattended updates.

For high-stakes apps consider `npm install --omit=dev` in production builds — dev deps are a huge attack surface that production runtime does not need.

## Built-in audit — useful, limited

```bash
npm audit --omit=dev --audit-level=high
pnpm audit --audit-level=high
yarn npm audit
pip-audit
```

What `npm audit` does well:

- Catches known CVEs against installed versions
- Fast, no extra tooling
- Good signal-to-noise at `--audit-level=high` or `critical`

What it misses:

- **Malicious-by-design** packages (the package is doing what it's "supposed to do", which happens to be evil)
- **Unreported issues** — many compromised packages are not in any CVE feed
- **Behavior-level analysis** — `audit` doesn't know that this package suddenly started making outbound HTTPS calls

Treat `npm audit` as the first line of defense, not the only one.

## Behavior-level scanning

Tools that look at *what a package does*, not just *which CVE it has*:

- **socket.dev** — flags new packages, packages that gained network/install-script behavior, typosquat-shaped names. GitHub integration that comments on PRs. Free tier covers most personal use.
- **deps.dev** (Google) — package metadata, transitive graph, advisory feed
- **OSV-Scanner** — open-source scanner against the OSV database, broader than npm audit
- **Snyk / GitHub Dependabot security alerts** — overlap with audit but include curated advisories

A reasonable stack: GitHub Dependabot (free, native) + socket.dev (free, behavior-aware) + `npm audit` in CI.

## Reviewing a new dependency before `npm install`

When adding a new dep, especially a small or unfamiliar one, take 60 seconds first.

```bash
# What is this package, who maintains it, what's the install footprint?
npm view <pkg>
npm view <pkg> dependencies         # transitive count
npm view <pkg> repository.url        # is there a public repo?
npm view <pkg> maintainers           # who can publish a new version?
npm view <pkg> time                  # when was each version published?

# How popular is it? (huge install counts don't prove safety, but obscure single-digit downloads warrant scrutiny)
curl -s "https://api.npmjs.org/downloads/point/last-week/<pkg>" | jq

# Red flags in the publish history
npm view <pkg> time --json | jq 'to_entries | sort_by(.value) | reverse | .[0:5]'
```

Red flags:

- **Single maintainer with no other notable packages** + the package handles auth/crypto/payments
- **Recently transferred ownership** (new maintainer's other packages look unrelated)
- **Sudden version jump** with a vague changelog (`"bug fixes"` and a 1k-line diff)
- **No public repo**, no homepage, no README
- **Typosquat-shaped name** — `lodash-utils` vs `lodash`, `colors-js` vs `colors`
- **Postinstall script** (see next section)
- **Network calls during install** (you can sandbox install to detect — see CI section)

## Postinstall scripts

`postinstall`, `preinstall`, `install`, `prepare` scripts run on `npm install`. They are the most common malware delivery vector.

```bash
# Enumerate every package with an install-time script
find node_modules -name package.json -not -path '*/node_modules/*/node_modules/*' \
  -exec grep -l '"postinstall"\|"preinstall"\|"prepare"' {} \; \
  | xargs -I {} dirname {} | sed 's|node_modules/||'

# Block ALL install scripts globally — most packages do not need them
npm config set ignore-scripts true
# Or per-install
npm install --ignore-scripts
```

`--ignore-scripts` breaks some legitimate native-module builds (`node-sass`, `sharp`, `better-sqlite3`). Allow scripts only for the specific packages that need them — yarn 2+ and pnpm have allowlists.

In `pnpm`:

```yaml
# .npmrc
ignore-scripts=true

# package.json
"pnpm": {
  "onlyBuiltDependencies": ["sharp", "better-sqlite3"]
}
```

## Typosquat detection

Common substitutions: `i` ↔ `l` ↔ `1`, `0` ↔ `o`, missing/extra dashes, plural/singular. Run:

```bash
# Cheap typosquat heuristic — flag packages with very similar names to well-known ones
npm ls --depth=0 --json | jq -r '.dependencies | keys[]' | while read p; do
  echo "$p"  # human review or feed to socket.dev
done
```

socket.dev / npq do this systematically; for a manual pass, just eyeball your direct deps with `cat package.json | jq '.dependencies | keys'`.

## CI / build sandbox

Don't let your install run with prod credentials sitting in env.

```yaml
# GitHub Actions
- name: Install dependencies
  run: npm ci --ignore-scripts
  env: {}                 # no env vars passed in
# Then run the few allowed install scripts intentionally
- name: Run build scripts for native deps
  run: npm rebuild sharp better-sqlite3
```

See [`github-actions-security`](../github-actions-security/SKILL.md) for the broader CI story (pinned action SHAs, OIDC, secret scoping).

## Audit `node_modules` for an inherited project

```bash
# How many packages did this single npm install actually install?
find node_modules -name package.json -not -path '*/node_modules/*/node_modules/*' | wc -l

# Largest packages — these are where you'd hide a payload
du -sh node_modules/*/  | sort -h | tail -20

# Packages with install scripts (as above)

# Packages with .bin executables
find node_modules/.bin -type l -o -type f | head -30
```

Cross-check against `package.json` direct deps. Anything in `node_modules` you cannot trace back to a direct or expected-transitive dep is worth investigating.

## What to do when a dependency is compromised

You wake up to "package X version 2.4.5 was compromised, contains a credential stealer".

1. **Determine if you shipped it.**
   ```bash
   # Did you have it installed at the bad version?
   git log --all -p -- package-lock.json | grep -A2 -B2 'package-x.*2\.4\.5'
   ```
2. **Assume credentials accessed during install/run are burned.** That includes `.env` files readable by the user that ran `npm install`, plus anything in process env at runtime.
3. **Rotate every credential that was in scope.** Order per [`secret-hygiene`](../secret-hygiene/SKILL.md).
4. **Pin to a known-clean version**, or remove the package entirely if no clean version exists.
5. **Audit `package-lock.json` for the transitive surface** — the compromised package may be a transitive dep you didn't add directly.
6. **Check CI logs** for unexplained outbound traffic during recent builds.
7. **Add the package + version range to a permanent denylist** in your CI (whatever scanner you use) so you don't accidentally re-add it.

## Periodic audit checklist

Once a quarter:

- [ ] Lockfile present and committed for every project
- [ ] CI uses `npm ci` / `--frozen-lockfile`, not loose install
- [ ] Dependabot (or equivalent) enabled, PRs reviewed not auto-merged for major versions
- [ ] `npm audit --audit-level=high` passes; exceptions documented
- [ ] socket.dev or equivalent reviews new dependency PRs
- [ ] Install scripts allowlisted; defaults to ignore
- [ ] No env vars passed to `npm ci` step in CI
- [ ] Direct dependencies you don't recognize have been investigated
- [ ] A known-vulnerable package list is maintained for the project's ecosystem

## What this skill will not do

- Replace a formal Software Bill of Materials (SBOM) program for regulated environments
- Provide payloads or attack patterns to publish malicious packages
- Recommend installing packages without lockfiles "for now"
