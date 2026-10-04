---
name: ci-assessment
description: >-
  READ-ONLY CI/CD posture assessment. Use during SCOUT or ESCALATE when a build system is in
  scope and you must answer "what could an attacker do to this pipeline" without executing
  anything: identifying the CI platform, testing unauthenticated consoles and default
  credentials, auditing exposed logs and artefacts, hunting secrets in job output and
  variables, assessing runner-token exposure, and reporting it as an assessment.
---

# SKILL: CI/CD Posture Assessment

> **AI LOAD INSTRUCTION**: An assessment is not a weaker attack — it is a *different* product. The
> deliverable is a defensible inventory of exposure with reproducible evidence and a remediation
> order, not a shell. Everything here runs read-only and survives the client asking "prove it
> again". Where an active attack exists, this skill records the weakness and routes to
> [cicd-attacks](../cicd-attacks/SKILL.md) — it does not execute it.

## 1. RELATED ROUTING

- [cicd-attacks](../cicd-attacks/SKILL.md) — offensive counterpart; load only when RoE permits
- [recon-methodology](../recon-methodology/SKILL.md) — how a CI host enters the inventory
- [insecure-source-code-management](../insecure-source-code-management/SKILL.md) — VCS/backup exposure beside CI configs
- [dependency-confusion](../dependency-confusion/SKILL.md) — registry side of the supply chain
- [evidence-standard](../../core-subjects/evidence-standard.md) — what a finding carries

---

## 2. WHAT THIS ASSESSMENT ANSWERS

Six questions, in this order. Later ones are worthless if earlier ones are unanswered.

| # | Question | Evidence that answers it |
|---|---|---|
| 1 | **Which CI platforms exist?** | login-page fingerprints, hostnames (`jenkins.`, `ci.`), headers |
| 2 | **Who can reach them?** | internet vs VPN-only vs internal; anon endpoints |
| 3 | **What does an anonymous visitor see?** | console pages, job names, build logs, badge APIs |
| 4 | **What does a low-privilege user see?** | secret *names*, credential metadata, runner config |
| 5 | **Where do secrets live, and are they retrievable?** | variables store, log leakage, artefacts |
| 6 | **What is the blast radius?** | deploy keys, cloud roles, registry tokens, signing keys |

---

## 3. PLATFORM IDENTIFICATION

Fingerprint before you probe. The platform dictates endpoints, auth model, and which defaults are
even plausible — a Jenkins checklist run against GitLab wastes the window.

```bash
# Host naming is the cheapest signal in the estate inventory
cat inventory.txt | grep -Ei '(^|\.)(ci|cd|jenkins|gitlab|builder|build|drone|argo|tekton|teamcity)\.'

# Headers and titles for whatever survives
httpx -l ci_candidates.txt -sc -title -td -server -o ci_probe.txt

# GitHub Actions has no host to find: it lives inside repos
gh api /orgs/ORG/repos --paginate -q '.[] | .full_name' | \
  while read r; do gh api "/repos/$r/contents/.github/workflows" -q '.[].name' 2>/dev/null | sed "s|^|$r |"; done
```

| Platform | Tell | Auth surface | Default-credential reality |
|---|---|---|---|
| **Jenkins** | `X-Jenkins` header, `/login`, `/api/json`, cookie | `/script` (Groovy console), `/manage`, CLI 50000 | no default, but `admin:admin` in built/container instances |
| **GitLab** | `_gitlab_session` cookie, `/users/sign_in` | `/-/graphql-explorer`, `/api/v4`, runner registration | none; watch `/users/sign_up` |
| **GitHub Actions** | no host — repo `.github/workflows/*.yml` | workflow files, org/repo/env secrets, `GITHUB_TOKEN` | exposure lives in the YAML and org settings |
| **CircleCI** | `circleci.` host, v2 API | project settings, context env vars | long-lived API tokens |
| **Azure DevOps** | `dev.azure.com`, `X-VSS-*` headers, `_apis/` paths | variable groups, | over-scoped PATs, often committed |

---

## 4. UNAUTHENTICATED CONSOLE AND CREDENTIAL CHECKS

Read-only does not mean passive. Fetching a login page or a public badge is normal traffic; the line
you must not cross is submitting credentials you do not own beyond a documented, single,
non-destructive default-credential test the RoE permits.

```bash
# Which endpoints answer without a session? Status and size tell you what it is.
for p in /script /manage /api/json /api/xml /people /asynchPeople \
         /credentials /computer/ /env-vars.html /whoAmI/api/json; do
  printf '%-22s ' "$p"
  curl -s -o /dev/null -w '%{http_code} %{size_download}\n' "https://ci.example.com$p"
done

# GitLab: is self-registration left enabled?
curl -s -o /dev/null -w '%{http_code}\n' https://gitlab.example.com/users/sign_up

# GitHub Actions: is the workflow surface even visible?
gh api /repos/OWNER/REPO/actions/secrets -q '.total_count'   # names/count only, never values
```

**Interpretation, not just collection.** A `200` on the Jenkins `/api/json` index discloses job
names and often the version — record it. A `403` on `/api/json` with `200` on `/login` is a
*correctly locked* instance: record it as a control that works, because an assessment that only
lists problems is not credible. A session-less `200` on `/script` is Groovy execution — that finding
writes itself.

**Default-credential testing rules.** Only with explicit written authorisation, only against an
attributable account, one attempt per credential pair per platform, only where the RoE names it.
A lockout caused by your spray is an availability incident you will spend the rest of the assessment
explaining. Where the RoE is silent, do not test — report the *absence of a lockout policy* instead.

---

## 5. EXPOSED BUILD LOGS AND ARTEFACTS

Build output is the most under-rated disclosure channel in CI. Jobs echo environment variables for
debugging, print `docker inspect` output, `cat` manifests, and dump connection strings in failed
migration errors. Anyone who can read logs often needs no further vulnerability.

```bash
# Jenkins: jobs are discoverable from the JSON index, then logs per build
curl -s 'https://ci.example.com/api/json?tree=jobs[name,url]' | jq -r '.jobs[].name'
curl -s 'https://ci.example.com/job/JOBNAME/lastBuild/consoleText' | \
  grep -nEi 'password|token|secret|api[_-]?key|authorization:|aws_|BEGIN [A-Z ]*PRIVATE KEY'

# Artefact repositories: Nexus, Artifactory, GitLab registry
curl -s -o /dev/null -w '%{http_code}\n' https://nexus.example.com/service/rest/v1/repositories
curl -s 'https://artifactory.example.com/artifactory/api/repositories' | jq -r '.[].key'
```

| Artefact class | Where it leaks | Why it matters |
|---|---|---|
| Job console output | `consoleText`, GitLab trace, Actions log download | env dumps, tokens under `set -x` |
| Test/coverage reports | published HTML artefacts, workspace reports | internal hostnames, fixture records, stack traces |
| Build artefacts (`.jar`, `.war`, `.zip`) | `target/`, `dist/`, published packages | embedded config, keystores, credentials, source maps |
| Container images | registry tags, `latest` beside `prod-*` | secrets baked into layers, base age, topology |
| Caches | Actions cache, shared Maven/Gradle caches | dependency-confusion footholds, poisoning |

```bash
# Offline secret patterns across fetched logs/artefacts — no target traffic
gitleaks detect --no-git --source ./fetched_artefacts -r leaks.json
```

Record **which log line, in which build, at which URL** produced each hit. A secret reported without
its retrieval path is unverifiable and triaged as noise.

---

## 6. SECRET AND ENVIRONMENT-VARIABLE EXPOSURE

The question is never "does the tool store secrets" (all of them do) but "who can read them, and can
they be made to print". Separate the exposure modes, because the remediations differ.

| Exposure mode | Mechanism | Detection without retrieving the value |
|---|---|---|
| **Stored-secret read** | a job-config or admin user retrieves the value | credential metadata: names, types |
| **Log echo** | value reaches output via `set -x`, debug flags, `env` | grep fetched logs for markers, entropy |
| **Cross-scope read** | scope separation is weaker than assumed; a PR job reads prod secrets | which scopes attach which secrets to what |
| **Registry/deploy tokens** | keys with write access to production artefacts | key metadata; read/write |

```bash
# Jenkins credential metadata (names and types, read-only)
curl -s https://ci.example.com/credentials/store/system/domain/_/api/json | jq '.credentials'

# GitLab project variables: key names and protection flags, not values
curl -s -H "PRIVATE-TOKEN: $TOKEN" \
  'https://gitlab.example.com/api/v4/projects/PROJECT_ID/variables' | \
  jq -r '.[] | "\(.key)\tmasked=\(.masked)\tprotected=\(.protected)"'

# GitHub: secret names only; environment scoping and protection rules are the real finding
gh api /repos/OWNER/REPO/environments -q '.environments[].name'
gh api /repos/OWNER/REPO/actions/secrets -q '.secrets[].name'
```

**The high-value findings are structural, not value-based:** a secret attached to every job in a
project rather than the job that needs it; a production secret reachable from a branch, PR or fork
trigger; a secret marked **unmasked** (masking is best-effort, not a control); a long-lived static
token where short-lived OIDC federation is available; one credential shared by CI and a human. Never
place a retrieved value in the report — state identity, scope, retrieval path, and that rotation is
required regardless of whether you used it.

---

## 7. RUNNER AND AGENT EXPOSURE

Runners are the boundary between the pipeline and everything it can reach. Assess them as hosts,
not as CI objects.

```bash
# GitHub: are self-hosted runners attached, and at what scope?
gh api /repos/OWNER/REPO/actions/runners -q '.runners[] | "\(.name)\t\(.status)"'
gh api /orgs/ORG/actions/runners  -q '.runners[] | "\(.name)\t\(.status)"'

# Jenkins: node inventory reveals OS, labels, executors, remote FS roots
curl -s 'https://ci.example.com/computer/api/json?tree=computer[displayName,offline]' | jq .
```

| Finding | Why it is a posture problem | Record |
|---|---|---|
| Registration token readable by a non-admin | any holder attaches a runner and gets jobs — including secret-carrying ones | who can read it, its scope |
| Persistent vs ephemeral runners | persistent runners retain state, credentials, position | isolation claim vs reality |
| Runner network position | a runner inside a prod subnet turns a repo write into internal access | CIDRs it reaches |
| Label-based routing | `runs-on: self-hosted` in a public repo is an invitation; labels are attacker-chosen | which labels exist, who can target them |
| Runner as a secret store | instance profiles, mounts, `~/.aws`, `~/.docker/config.json` | host credentials |

**Registration-token exposure has the shortest path to impact** because it needs no exploit: obtain
the token, register, wait for a job, inherit its secrets and the runner's network position. Rate it
high even undemonstrated — the value is naming it first.

---

## 8. CHECKLIST, REPORTING, AND REMEDIATION ORDER

Copy this into the report as a scored table. `PASS` means present and effective; `FAIL` means
absent; `PARTIAL` means present but bypassable — always state the bypass.

```
IDENTIFICATION
[ ] CI platforms enumerated and fingerprinted (header-confirmed, not guessed)
[ ] Versions recorded; version exposure rated informational
[ ] Per-platform reachability charted (internet / VPN / internal)

AUTHENTICATION AND EXPOSURE
[ ] Unauthenticated endpoint surface mapped, with a status code per path
[ ] Unauthenticated console (/script, /manage, admin UIs) evaluated
[ ] Default-credential posture stated (tested only if RoE permits, else from lockout policy)
[ ] Self-registration / signup endpoints assessed
[ ] MFA enforced for admin and secret-access roles
[ ] Session lifetime, idle timeout and logout behaviour recorded

LOGS AND ARTEFACTS
[ ] Build logs readable by anonymous or broadly-permissioned users
[ ] Logs grepped for secret markers; every hit carries a URL and build ID
[ ] Artefact repositories enumerated; anonymous read assessed
[ ] Published artefacts inspected offline for embedded config and secrets
[ ] Container images checked for baked-in credentials and stale bases

SECRETS
[ ] Secret inventory taken by NAME and SCOPE only
[ ] Secrets scoped per job rather than per project/repository
[ ] Production secrets unreachable from PR / fork / untrusted-branch triggers
[ ] Masking enabled and documented as best-effort, not a control
[ ] Static long-lived tokens identified, with an OIDC migration note
[ ] Secret-in-repo history checked (routes to insecure-source-code-management)

RUNNERS
[ ] Self-hosted runners enumerated with scope, labels, status
[ ] Registration token read-access restricted; registration disabled where unused
[ ] Runner network position documented per runner
[ ] Runner credential inheritance (instance roles, mounts) documented
[ ] Job isolation between projects on shared runners assessed

PIPELINE INTEGRITY
[ ] Third-party actions/steps pinned to immutable SHAs, not tags
[ ] Branch protection: required reviews, required checks, force-push and deletion blocked
[ ] Workflow-file write rights separated from merge rights
[ ] Production deployment approvals exist and cannot be self-approved
[ ] Audit logging enabled and shipped off-platform
```

**Reporting rules.** Severity follows the reachability chain, not the category: "registration token
readable by any employee in an org of 4,000" outranks "unpinned action in a repo nobody deploys".
No secret values, ever — identifier, scope, retrieval path, rotation requirement; prove findings
through metadata (`masked`, `protected`, last-rotated), not content. One finding, one URL, one
timestamp, so the client can re-run it. Separate posture from exploitation. And name the compensating
controls you found — they shorten the argument about severity.

**Remediation order — this ranking, not alphabetical:**

| Order | Action | Why first |
|---|---|---|
| 1 | Rotate every credential reachable through a log, artefact, or broad scope | exposure already happened; rotation is the only remedy |
| 2 | Restrict runner registration; make runners ephemeral | shortest path to execution |
| 3 | Scope secrets per job and environment; remove prod secrets from PR/fork paths | removes the "CI read my secret" class |
| 4 | Enforce branch protection; separate workflow write from merge rights | stops pipeline-integrity attacks |
| 5 | Pin third-party actions/steps to immutable references | cheap, permanent |
| 6 | Tighten log and artefact visibility; scrub debug output | reduces future disclosure only |
| 7 | Enable and ship audit logs; alert on secret access and changes | detection for the rest |
| 8 | Move to short-lived federated credentials | removes standing privilege |

**Do not** present items 6–8 as substitutes for 1–3. Reordering this list is the most common way an
assessment quietly fails its purpose.

---

---

## 9. CONFIRMING THE FINDING

| Step | Question | What it proves |
|---|---|---|
| 1 | Did you **read the actual asset** (a log, a secret, a build artefact) rather than infer it? | an assessment needs a read, not a hypothesis |
| 2 | Was the read **unauthenticated or default-credentialed**, and is that stated? | the exposure's nature |
| 3 | Was there a **control** - the same request to a component that requires auth? | the endpoint is the outlier |
| 4 | Did the asset contain a **credential, a token, or internal architecture**? | the impact |
| 5 | Is the exposure **still live** at the time of writing the report? | a stale reference is not a finding |
| 6 | Did you **stay read-only**, with no job triggered and no artefact altered? | the assessment contract |
| 7 | Did you record the **platform, version, and URL** for each finding? | reproducibility |

**Read-only plus the asset plus the control is the bar.** An assessment that lists a reachable console
without reading anything behind it has produced a scan result, not a finding.

---

## 10. EXECUTION PRIMITIVES

The assessment is proven by **a read of the exposed asset, performed read-only, with the authenticated
control**. Every block ends at content, never at a status code.

### 11.1 Platform identification and the read-only rule

```bash
CI="https://ci.target.example"
# the platform, which determines every path that follows
curl -sS -D- -o /dev/null "$CI/" 2>&1 | grep -iE 'server|x-jenkins|x-gitlab|gitlab-lb|x-goog|atlassian|teamcity' | head -6
curl -sS "$CI/" 2>/dev/null | grep -oiE 'jenkins|gitlab|bamboo|teamcity|azure devops|argo|drone|circleci' | sort -u | head -5
# the version, which bounds the known issues
curl -sS "$CI/api/json" 2>/dev/null | head -c 200; echo
curl -sS "$CI/api/v4/version" 2>/dev/null | head -c 200; echo
# READ-ONLY RULE: record it, and never call a job-triggering endpoint
echo "READ-ONLY: no POST to /build, /job/*/build, /pipeline, /api/v4/projects/*/trigger"
```

**The read-only rule is part of the technique.** An assessment that triggers a build has executed
something, which changes the engagement's nature and must be agreed with the client in advance.

### 11.2 Unauthenticated consoles and default credentials

```bash
CI="https://ci.target.example"
# the unauthenticated surfaces, each read for content rather than status
for p in / /login /api/json /api/v4/projects /script /manage /computer/api/json /view/all/api/json; do
  printf '%-28s ' "$p"
  curl -sS -o /tmp/ci.out -w '%{http_code} %{size_download} ' "$CI$p" 2>/dev/null
  head -c 60 /tmp/ci.out | tr -d '\n'; echo
done
# THE CONTROL: a path that requires authentication, which must be 401 or a login redirect
curl -sS -o /dev/null -w 'control(auth) %{http_code}\n' "$CI/me" 2>/dev/null
# the default-credential check, which is a TEST and not a brute force - one attempt per known default
for cred in "admin:admin" "admin:password" "root:root" "jenkins:jenkins"; do
  U="${cred%%:*}"; P="${cred##*:}"
  printf '%-22s ' "$cred"
  curl -sS -o /dev/null -w '%{http_code}\n' -u "$U:$P" "$CI/api/json" 2>/dev/null
done
# and the anonymous API, which on Jenkins is the highest-yield read when the matrix is open
curl -sS "$CI/api/json?tree=jobs[name,url,color]" 2>/dev/null | head -c 500; echo
```

**One attempt per documented default, and no more.** The assessment's credibility depends on it never
looking like a brute force, and the client's rules of engagement will say so.

### 11.3 Build logs and artefacts, read for secrets

```bash
CI="https://ci.target.example"
# the job list, then the console text of the most recent build - read-only
curl -sS "$CI/api/json?tree=jobs[name,url,lastBuild[number,url]]" 2>/dev/null | head -c 800; echo
# the console log, which is where secrets leak
curl -sS "$CI/job/DEPLOY/lastBuild/consoleText" 2>/dev/null | head -c 2000; echo
# the secret patterns, which are the actual finding
curl -sS "$CI/job/DEPLOY/lastBuild/consoleText" 2>/dev/null | grep -inE \
  'AWS_(SECRET|ACCESS)|AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9]{36}|glpat-[A-Za-z0-9_-]{20}|xox[baprs]-|-----BEGIN [A-Z ]*PRIVATE KEY|password=|token=|NT_?HASH|connectionString' | head -20
# the artefact list, and one artefact's headers - the artefact is usually the credential container
curl -sS "$CI/job/DEPLOY/lastBuild/api/json?tree=artifacts[fileName,relativePath]" 2>/dev/null | head -c 600; echo
curl -sS -D- -o /dev/null "$CI/job/DEPLOY/lastBuild/artifact/.env" 2>&1 | grep -iE 'content-type|content-length|HTTP/' | head -4
# THE CONTROL: a job that does not exist, which must 404 - proves you are reading real resources
curl -sS -o /dev/null -w 'nonexistent %{http_code}\n' "$CI/job/NOPE/lastBuild/consoleText" 2>/dev/null
```

**The `grep` output with its surrounding context is the finding.** A build log that contains
`AWS_SECRET_ACCESS_KEY=` is a credential exposure; the log's URL and the build number are the evidence.

### 11.4 Environment variables and secret stores

```bash
CI="https://ci.target.example"
# the variables endpoint, which on Jenkins leaks values in some configurations
curl -sS "$CI/job/DEPLOY/lastBuild/injectedEnvVars/api/json" 2>/dev/null | head -c 1000; echo
curl -sS "$CI/env-vars.html/" 2>/dev/null | head -c 400; echo
# GitLab's variable endpoints, which require a token - the absence of a token IS the finding shape
curl -sS "$CI/api/v4/projects?visibility=public&per_page=5" 2>/dev/null | head -c 600; echo
curl -sS -o /dev/null -w 'ci-variables %{http_code}\n' "$CI/api/v4/projects/1/variables" 2>/dev/null
# the mask check: are secrets masked in the log, and can a build script unmask them
python3 - <<'PY'
print("Jenkins masks a secret in the log only where the exact string appears; a script can trivially")
print("mask-bypass it with base64. An assessment records the MASKING state that you OBSERVED in a log -")
print("it must not attempt to unmask a live secret, which requires triggering a build.")
PY
# and the config.xml, which frequently exposes credentials in cleartext or as an id reference
curl -sS "$CI/job/DEPLOY/config.xml" 2>/dev/null | grep -icE 'password|secret|token|credentialId' | sed 's/^/config.xml-secret-refs=/'
```

**The masking state you observed is the assessment's claim.** Do not attempt to unmask a live secret -
that requires triggering a build, and it is outside the read-only contract.

### 11.5 Runner, agent, and token exposure

```bash
CI="https://ci.target.example"
# the agents the controller exposes, and whether a job can be placed on them
curl -sS "$CI/computer/api/json?tree=computer[displayName,offline,executors[*]]" 2>/dev/null | head -c 800; echo
curl -sS "$CI/label/linux/api/json" 2>/dev/null | head -c 400; echo
# the runner registration state - a project-scoped runner token is the lateral primitive
curl -sS "$CI/api/v4/runners" 2>/dev/null | head -c 300; echo
# and the CI token exposure in a repository's config, which is where a shared runner token appears
curl -sS "https://git.target.example/target/repo/raw/main/.gitlab-ci.yml" 2>/dev/null | head -c 800; echo
curl -sS "https://git.target.example/target/repo/raw/main/.github/workflows/deploy.yml" 2>/dev/null | head -c 800; echo
# THE CONTROL: the same repository files without authentication, which must 404 on a private repo
curl -sS -o /dev/null -w 'private-control %{http_code}\n' "https://git.target.example/other/private/raw/main/.gitlab-ci.yml" 2>/dev/null
```

**A pipeline file readable without authentication is the finding.** It names the secrets, the runner, and
the deployment target, and it is frequently the single highest-yield read in a CI assessment.

### 11.6 The exposure inventory, generated for the report

```bash
python3 - <<'PY'
import requests
CI = "https://ci.target.example"
SURFACES = [
    ("console",            "/"),
    ("api-json",           "/api/json"),
    ("job-list",           "/api/json?tree=jobs[name]"),
    ("computer-list",      "/computer/api/json"),
    ("credentials-store",  "/credentials/"),
    ("script-console",     "/script"),
    ("env-vars",           "/env-vars.html/"),
    ("config-xml",         "/job/DEPLOY/config.xml"),
]
print("%-20s %-6s %-9s %-14s %s" % ("surface", "code", "bytes", "auth-needed", "note"))
for name, path in SURFACES:
    try:
        anon = requests.get(f"{CI}{path}", timeout=10)
        auth = requests.get(f"{CI}{path}", auth=("test", "test"), timeout=10)
        note = "READABLE ANONYMOUSLY" if anon.status_code == 200 else ("redirect to login" if anon.status_code in (302,303) else "")
        print("%-20s %-6s %-9s %-14s %s" % (name, anon.status_code, len(anon.content),
              "yes" if auth.status_code != anon.status_code else "no", note))
    except Exception as e:
        print("%-20s ERROR %s" % (name, type(e).__name__))
print()
print("Each READABLE ANONYMOUSLY row needs a CONTENT read in the report, not just the status code.")
print("A status code alone is a scan result; the content is the assessment.")
PY
```

**Content, not status codes.** Every row in the report should quote what was actually readable, with the
secret values redacted and their provenance named.

### 11.7 The end-to-end harness

```bash
python3 - <<'PY'
print("=== CI ASSESSMENT RECORD (read-only) ===")
for row in ["platform, version, and the URL you read",
            "the authentication state of each surface you read",
            "the control path that DID require authentication",
            "the content you read, quoted and redacted",
            "the secret patterns found, with the log URL and build number",
            "the runner and agent exposure, with the token's scope if visible",
            "the pipeline files readable without authentication",
            "the masking state you OBSERVED, without attempting an unmask",
            "the confirmation that no job was triggered and no artefact was altered",
            "the remediation order: which exposure to close first, and why"]:
    print("  -", row)
print()
print("An assessment is a product with a different bar: every claim reproducible, nothing executed.")
PY
```

**Reproducible, read-only, and ordered.** The remediation order is part of the deliverable, because the
client will ask which exposure to close first.

---

## 11. EVIDENCE STANDARD — ASSESSMENT ARTEFACTS

| Item | Why |
|---|---|
| The **platform, version, and exact URL** for each observation | reproducibility |
| The **authentication state** of each surface, tested anonymously | the exposure's nature |
| The **control path that required authentication** | proves the open surface is the outlier |
| The **content read**, quoted and redacted | the finding, not a status code |
| The **secret patterns found**, with the log URL and build number | the highest-impact rows |
| The **runner and agent exposure**, with any token's scope | the lateral primitive |
| The **pipeline files readable without authentication** | the architecture disclosure |
| The **masking state you observed** | an assessment claim, not an unmask attempt |
| The **confirmation that nothing was triggered or altered** | the read-only contract |
| The **remediation order**, with a rationale | the deliverable's second half |

Report the **surface and the content**: "the Jenkins controller at `https://ci.example` returns `200`
for `GET /api/json?tree=jobs[name]` with no authentication, listing 34 jobs including `DEPLOY-PROD` and
`ROTATE-KEYS`, where `GET /me` returns `403`, which is the authentication control. `GET
/job/DEPLOY-PROD/lastBuild/consoleText` with no authentication returns a 412 KB console log containing
`AWS_ACCESS_KEY_ID=AKIA...` and `AWS_SECRET_ACCESS_KEY=` with the value masked by the credentials plugin;
the log also names the internal registry `registry.internal:5000` and the deployment host
`prod-app-01.internal`. GitLab at `https://git.example` serves `.gitlab-ci.yml` for the `target/repo`
project without authentication, and that file names a project-scoped runner token variable. No build was
triggered and no job configuration was modified at any point", never "the CI server is exposed".

### False positives - do not report these

| Observation | Why it is not a finding |
|---|---|
| A reachable console **with no content read** | a scan result, not an assessment finding |
| A `200` on a **public health or status endpoint** | designed to be public |
| A login page returning `200` | that is what a login page does |
| A default-credential check **attempted more than a few times** | no longer an assessment, and a scope violation |
| A masked secret **inferred to be recoverable** without testing | a hypothesis; state it as one |
| A build log containing **only public repository information** | nothing sensitive |
| A runner or agent address **with no token exposure** | architecture information, low severity |
| A pipeline file from a **public open-source repository** | already public |
| An exposure on a **staging CI instance the client owns and knows about** | confirm the scope before reporting |
| A finding that required **triggering a build** | outside the read-only assessment |
| A secret value reproduced in full | a disclosure |

**Read-only, content-bearing, with the control.** The assessment's value is that every claim is
reproducible and nothing was executed - a single triggered build destroys that property.

---

## 12. REMEDIATION REFERENCE

1. **Require authentication on every controller endpoint, including the anonymous read API, and disable the anonymous read matrix entirely** - most of the exposures in this document are that one setting.
2. **Change every default credential and every vendor default path before the instance is reachable from a shared network** - the default-credential check is one attempt and it succeeds more often than it should.
3. **Mask secrets in build logs by construction: never echo them, and use the credential store's binding rather than a shell variable** - masking by pattern is defeated by base64 and by string manipulation.
4. **Restrict build-log and artefact read access to the project's members, and expire logs on a defined retention** - an old log with a credential is an exposure even after the credential is rotated.
5. **Rotate any credential that has ever appeared in a log, an artefact, or an environment listing, and confirm the rotation** - the exposure's history is longer than the finding's.
6. **Keep pipeline definition files private, and never put a token, a hostname, or a deployment target in one that can be read without authentication** - the pipeline file is the architecture disclosure.
7. **Scope runner and agent registration tokens to a single project, expire them, and rotate on a schedule** - a shared runner token is a path to every project on the runner.
8. **Isolate runners so that one project's job cannot read another's workspace or the host's filesystem** - the runner is where a CI pipeline crosses into infrastructure.
9. **Put the controller and the runners on a management network, and never expose either to the internet** - the exposure in most assessments is a firewall rule rather than a product setting.
10. **Log and alert on anonymous reads of the API, on default-credential attempts, and on log downloads outside the project's members** - all three are high-signal and cheap.
11. **Re-run this assessment after every platform upgrade and after any change to the authentication configuration** - the anonymous matrix and the default paths change between versions.

---

## 13. RELATED SIBLINGS - LOAD TOGETHER

- [cicd-attacks](../cicd-attacks/SKILL.md) - the active side, which turns these exposures into execution
- [insecure-source-code-management](../insecure-source-code-management/SKILL.md) - the repository-tier exposures
- [dependency-confusion](../dependency-confusion/SKILL.md) - the build-time supply-chain path
- [cloud-assessment](../cloud-assessment/SKILL.md) - where the credentials found in a log lead
- [security-reporting-and-documentation](../security-reporting-and-documentation/SKILL.md) - the reporting discipline this deliverable depends on

---

## SELF-VERIFY

Run from the workspace root; every check is read-only and should pass before this file is complete.

```bash
f=skills/impl/ci-assessment/SKILL.md
wc -c "$f"                                              # byte size within 12,000-15,000
grep -cE '^## [0-9]+\.' "$f"                            # numbered sections: 7-9
grep -oE '\]\(\.\./[^)]+\)' "$f" | sed -E 's/^\]\(\.\.\///; s/\)$//' | sort -u | \
  while read -r p; do [ -e "skills/impl/$p" ] || echo "BROKEN LINK: $p"; done
grep -q '^## 9\. SELF-VERIFY' "$f" && echo "self-verify present"
```
