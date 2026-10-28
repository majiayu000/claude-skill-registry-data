---
name: github-repo-repair-audit
description: Repair and audit an existing GitHub repository — verify what is actually on the remote before acting, compare local vs remote at byte level, fix real bugs with a reproducible setup, and sync every place that quotes the number you changed. Use when a task says "the repo is still on the old version" or "fix X", or when auditing several repos for stale descriptions and broken claims. Not for launching a new repo (use github-repo-launch-polish).
version: 1.0.0
---

# GitHub Repo Repair Audit

Auditing an existing repo. The dominant failure mode is not a hard bug — it is **acting on a
description that has already gone stale**, producing a no-op commit or redoing finished work.

Distinct from `github-repo-launch-polish` (README/badges/topics for a *new* repo)
and `portfolio-github-workflow` (publishing one portfolio site).

## Rule 0 — Verify the remote before you touch anything

Task lists, memory notes, and handoff summaries go stale. The remote is the only source of truth.

```bash
# 1. What is actually on main, and when?
GET /repos/{owner}/{repo}/commits/main        → sha + message + committer date
# 2. Full file list with blob shas and sizes
GET /repos/{owner}/{repo}/git/trees/main?recursive=1
```

> **Real case (2026-10-21):** a task said "daypilot main is still on old commit 81b639a, push the
> local fix". Remote HEAD was `22b18167`, v1.0.1/v1.1.0 — **the fix had been pushed three days
> earlier**. Pushing again would have produced an empty commit and a false "done" report.
> A second task said "og:image is a malformed base64 splice" — remote was already a correct URL.

**If the described gap does not exist, say so and stop.** Do not push just to have pushed.

## Rule 1 — Comparing local vs remote

### Never trust size alone, and never trust the sha alone either

```python
# local
git hash-object path/to/file
# remote
GET /repos/{owner}/{repo}/git/trees/main?recursive=1   → tree[i].sha
```

These **can disagree even when the bytes are identical** (GitHub's blob sha notation differs from
what `git hash-object` computes locally). A mismatch is not proof of a content difference.

> **Real case:** `_selftest_eval.js` showed remote sha `61460c20` vs local `82b6498e`, both 5751
> bytes. `diff` said identical, CRLF counts matched, and re-downloading produced `82b6498e` again.
> The content was byte-identical; only the recorded sha differed. **Download and compare bytes
> before concluding anything.**

### Files over 1 MB: contents API silently returns no content

`GET /repos/{o}/{r}/contents/{path}` returns `"content": ""` for large files. You must:

```python
sha = [e['sha'] for e in tree['tree'] if e['path']==PATH][0]
raw = base64.b64decode(api(f"/repos/{o}/{r}/git/blobs/{sha}")['content'])
```

A script that silently writes an empty file looks like "successful download, empty file" and will
send you chasing a bug that does not exist.

### Batch comparison recipe

```python
remote = {e['path']: e['sha'] for e in tree['tree'] if e['type']=='blob'}
for path, sha in sorted(remote.items()):
    local_hash = subprocess.run(['git','hash-object',local],capture_output=True,text=True).stdout.strip()
    if local_hash != sha:
        # do NOT report yet — download and diff the bytes
        ...
```

## Rule 2 — Fix a bug: reproduce it first

Do not fix from a static read. Build a minimal local copy of the repo, then **make the failure
actually happen**, then fix, then re-run the repro.

```python
# stub the external dependency instead of calling it for real
fake = types.ModuleType('requests')
fake.post = lambda *a, **k: FakeResponse()
sys.modules['requests'] = fake
```

> **Real case (2026-10-21):** `ecom-script-agent`'s `llm.py` called `_build_system_prompt()` and
> `_build_user_prompt()`, neither of which **existed anywhere in the repo**. A static read looked
> plausible; the repro printed `NameError: name '_build_system_prompt' is not defined` immediately.
> The repo's 27 tests all passed — because **not one of them imported `agent.llm`**.
> Green tests covered a path nobody walked. Fix came with 8 new tests for exactly that path.

**When you fix a covered-by-nothing path, add tests for that path.** Otherwise the same bug
returns, still invisible.

## Rule 3 — Changing a number means changing every place that quotes it

After any fix that changes a countable fact, grep the whole deliverable set for the old number.

> **Real case:** unit-test count went 27 → 35. The number appeared in `README.md` (3 places),
> `CHANGELOG.md`, and — written two hours earlier — **4 places inside an HTML planning page I had
> generated myself**. The HTML was the deliverable the user was actively using.
> Cheap habit: after bumping a number, `grep -n "<old>"` across every artifact produced today.

Also distinguish two numbers that happen to look alike. In that repo `27` meant both
"auto_fix replacement rules" and "unit tests" — unrelated facts sharing a value. When you change
one, say explicitly which one changed and which did not.

## Rule 4 — Pushing without a working git

`git push` over a proxy fails for private repos. Use the Git Data API in four steps:

```
POST /git/blobs            → sha per file
POST /git/trees            → {base_tree, tree:[{path,mode,type,sha}]}
POST /git/commits          → {message, tree, parents:[parent_sha]}
PATCH /git/refs/heads/main → {sha}
```

Get a PAT without hardcoding it:

```bash
printf "protocol=https\nhost=github.com\n\n" | git credential fill | grep '^password='
```

Write it to a temp file, use it, **delete it before you finish the turn**.

Unauthenticated API calls hit a shared rate limit and return 403 — audit scripts that "work"
locally will fail mysteriously without a token.

## Rule 5 — Verify after pushing

```bash
curl -s -o /dev/null -w "%{http_code}" -L <page-url>     # 200?
GET /repos/{o}/{r}/pages                                  # status == built
curl -s -L <page-url> | grep 'og:title'                   # actually live?
```

Pages rebuilds take a minute. Asserting on stale CDN output produces false negatives — retry once
before concluding the deploy failed.

## Checklist

- [ ] Remote HEAD + date checked before any edit
- [ ] Local/remote diffs confirmed by **bytes**, not sha or size
- [ ] Bug reproduced in a local sandbox before fixing
- [ ] Tests added for the previously uncovered path
- [ ] Every place quoting a changed number is updated
- [ ] Push via Git Data API; PAT deleted afterward
- [ ] Post-push verified over HTTP

## Example

> 帮我检修这几个仓库：daypilot 说 main 还是旧版，ecom 说 llm.py 有未定义函数，作品集说 og:image 畸形。

daypilot: HEAD is v1.1.0, 19 files compared, 17 identical, 2 sha-mismatches that are byte-equal →
**already done, do not push**. ecom: repro `NameError`, fix, +8 tests (27→35), update README +
CHANGELOG + my own HTML page, push. Portfolio: og:image already correct, but **9 pages have no og
tags at all** → patch those, verify 200 + `built`.
