---
name: github-actions-android-first-green
description: "Use when an Android/Gradle GitHub Actions workflow is assumed working but every run is red, before claiming CI passes, after adding a workflow, or when local replays of CI are taken as proof. Symptoms: ./gradlew Permission denied (exit 126), a job that stops mid-Gradle with no ##[error] line, or android-emulator-runner reporting Task not found for a backslash continuation."
---

# Getting an Android CI workflow to its first real green

A workflow file that looks correct proves nothing. Replaying its commands
locally proves the commands, not the runner. **Ask the forge what happened.**

## 0. Never assume CI has run

```bash
gh auth status
gh run list --limit 10
```

A repo can go weeks with every run red and nobody noticing. If a
project doc claims CI "has never run" or "passes", verify it here first — that
claim is often stale or simply wrong, and correcting it is part of the work.

**Every run is dispatched by hand.** This account's zero-spend policy makes every
workflow `workflow_dispatch`-only, so a push starts nothing. Push the fix, then:

```bash
gh workflow run <workflow>.yml --ref <branch>     # prints the run URL when available
gh run list --workflow <workflow>.yml --limit 3   # or find the new run's ID here
```

`gh workflow run` fails on a workflow with no `workflow_dispatch:` trigger. If it
still has `push`/`pull_request` triggers, replace them rather than adding dispatch
beside them (`github-actions-cost-shutdown`, step 2). Never add a `push`,
`pull_request` or `schedule` trigger to get a run. Standard runners are free on
public repos; on a private repo every attempt draws on the plan's included minutes
and bills the overage, so get the owner's go-ahead and fix what you can check
locally first.

## 1. gradlew must be mode 100755

The single most common first failure, and it kills every job in ~13 seconds:

```
./gradlew: Permission denied     (exit code 126)
```

Cause: the wrapper was fetched with `curl`/`Invoke-WebRequest` on Windows and
committed as `100644`. Windows has no executable bit, so nothing locally can
show it.

```bash
git ls-files -s gradlew            # 100644 = broken
git update-index --chmod=+x gradlew
git commit -m "Make gradlew executable so CI can run it"
```

Check it in the index, not on disk — the on-disk mode is meaningless here.

## 2. A step that ends with no error line is an OOM kill

Signature: the log stops mid-Gradle (often just after `compileDebugKotlin`
warnings), there is **no `##[error]`**, `gh api .../annotations` returns
nothing, and the job is marked failed.

Do not theorise about memory. Measure it in the job:

```yaml
script: |
  free -h; df -h /
  ./gradlew :app:connectedDebugAndroidTest ...
  free -h
```

Real numbers from a standard `ubuntu-latest` runner on a private repo:

```
Mem:  7.8Gi total, 4.5Gi used, 164Mi free, 3.4Gi buff/cache
/dev/root  72G  65G used  6.7G avail  91%
```

**7.8 GiB, not 16.** GitHub documents the standard Linux runner as 2 CPU / 8 GB
on private repos and 4 CPU / 16 GB on public ones (verified 2026-09-24), so
measure on yours. On the 7.8 GiB runner the common defaults cannot fit together:

| component | typical default | fits? |
|---|---|---|
| emulator `ram-size` | 4096M | no |
| Gradle `org.gradle.jvmargs` | `-Xmx4g` | no |
| Kotlin daemon | inherits Gradle's `-Xmx` | no |

Working sizing, each number derived from the measurement:

```yaml
ram-size: 2048M
script: |
  ./gradlew :app:connectedDebugAndroidTest -Dorg.gradle.jvmargs="-Xmx2g -Dfile.encoding=UTF-8" -Pkotlin.daemon.jvmargs=-Xmx1g
```

Leave the `free -h`/`df -h` prints in permanently: the next failure then
arrives with evidence instead of needing the whole detour again.

## 3. reactivecircus/android-emulator-runner: one command per line

The action feeds `script:` to `sh -c`. A YAML block scalar with backslash
continuations arrives **literally**:

```
FAILURE: Build failed with an exception.
* What went wrong:
Selection failed
  Task '\' not found in root project 'X' and its subprojects.
```

Put each command on a single line, however long. Add a comment saying why, or
someone will "tidy" it back.

## 4. Noise that is NOT failure

During emulator boot these repeat and are harmless — boot polling:

```
adb: device offline
The process '.../adb' failed with exit code 1
WARNING | Failed to load snapshot 'default_boot'
```

Judge the job by its final `##[error]` / Gradle `FAILURE:` block, not by these.

## 5. Watching a run without burning the session

Runs take 10–30 minutes on a memory-starved runner. Poll in a loop inside one
command rather than issuing many short waits, and run it async or with a long
tool timeout (omp's bash tool defaults to 300 s):

```bash
for i in $(seq 1 20); do
  s=$(gh run view "$RUN_ID" --json status -q .status)
  [ "$s" = "completed" ] && break
  sleep 110
done
gh run view "$RUN_ID" --json conclusion,jobs \
  -q '.conclusion, (.jobs[] | .name + " -> " + (.conclusion // "?"))'
```

Getting logs:

```bash
gh run view --job "$JOB_ID" --log-failed > ci.log   # empty/short = killed, not failed
gh run view --job "$JOB_ID" --log > ci.log          # only after the job completes
```

`--log` refuses while a job is in progress ("logs will be available when it is
complete"). Save to a file and search the file; piping through a capped viewer
hides the error line.

## Order of work

1. `gh run list` — establish the real history before touching anything.
2. Fix the mode bit; push; dispatch; confirm jobs now get past `Set up`.
3. If a job dies with no error, add `free -h`/`df -h`; push; dispatch; read the numbers.
4. Size heaps and emulator from those numbers, one command per line.
5. Only claim green after `gh run view` reports every job `success`.
