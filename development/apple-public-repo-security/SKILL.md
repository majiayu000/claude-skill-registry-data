---
name: apple-public-repo-security
description: Use when a repo goes public or open-sources, when a CloudKit server-to-server PEM, ASC API `.p8`, APNs key, signing `.p12`, or provisioning profile first enters the pipeline, or when asked how to prevent or respond to a secret leak (gitleaks, lefthook, GitHub Secret Scanning, `git filter-repo`, rotate-first). Also for Apple upstream telemetry disclosure (MetricKit, Game Center, sysdiagnose). Repo-hygiene baseline only; ship-in-binary identifiers (AdMob IDs via xcconfig) and CLI keys in `secrets/.env` are build-time-secret-injection; ASC API usage is asc-api-automation.
---

# Apple Public Repo Security

## When to invoke

- The repo will be public from day 1.
- An existing private repo is planning to open-source.
- A new secret is being introduced (CloudKit server-to-server key, APNs key, ASC API key).
- User asks "how do I prevent secret leaks in a public repo", "how do I configure Xcode Cloud secrets", "what to do after a leak".

## Default decisions

### Public commitment from day 1

- No "private first, public later" transition — there's no escape hatch to "clean history later".
- No commit in the repo's history may contain secret values, PII, or identifiable player data.
- A violation, once it happens, is treated as **already leaked** and the secret is rotated.

### Secret classification

| Secret | Purpose | Storage |
|---|---|---|
| CloudKit server-to-server key (Key ID + PEM) | Backend API | Xcode Cloud Env Vars (Secret); locally in `secrets/` (chmod 600, gitignored) or Keychain |
| App Store Connect API Key (`.p8` + Key ID + Issuer ID) | TestFlight / submission automation | Xcode Cloud Env Vars (Secret); locally in `secrets/` (chmod 600, gitignored) or Keychain |
| APNs Auth Key (`.p8` + Key ID + Team ID) | Push notifications | Xcode Cloud Env Vars (Secret) |
| Signing certificate + private key (`.p12`) | Code signing | Xcode Cloud automatic signing, hosted by Apple |
| Provisioning profiles | Code signing | Xcode Cloud Apple-managed |
| Player identification data | Runtime debug | OSLog `.private` interpolation; **never** committed to git |

### Things that must not enter git

- The actual content of the secrets above (including base64-encoded forms)
- Real player aliases / displayNames / playerIDs (except after hashing)
- Apple Developer Team ID / DUNS / address (if they appear in entitlements / profile metadata)
- Build logs containing secrets (redact before viewing)
- Developers' local `secrets/` real files
- Personal notes / drafts

### Starter `.gitignore`

```
# Secrets / credentials
*.pem
*.p8
*.p12
*.mobileprovision
*.cer
.env
.env.*
!.env.example
secrets/

# Xcode / build
DerivedData/
build/
xcuserdata/
*.xcuserstate
.swiftpm/

# macOS
.DS_Store

# Personal notes
*.private.md

# Local development secrets directory is `secrets/` (chmod 600 PEMs / API keys
# live here; already ignored above via `secrets/`). Allow-list examples with a
# nested `secrets/.gitignore` (`* / !*.example / !README.md / !example/ /
# !example/**`) instead of a second top-level rule — see
# `build-time-secret-injection`. The last two lines are required: `*` also
# ignores the `example/` directory itself, and git does not descend into an
# ignored directory to apply `!README.md` to files inside it (verify with
# `git check-ignore -v secrets/example/README.md`).
```

### Three lines of defence

| Line | Tool | Scope |
|---|---|---|
| 1. Local pre-commit | `lefthook` + `gitleaks` (via `mise`) | Catches staged diffs; can be bypassed with `--no-verify` |
| 2. CI post-clone | Xcode Cloud `ci_post_clone.sh` runs `gitleaks` | Catches at PR time; fails the build; earliest stage is cheapest |
| 3. GitHub Secret Scanning Alerts | GitHub platform (free on public repos) | Passive detection; alerts a common private-key / generic API-key pattern — **only once Generic patterns is enabled** (Settings → Advanced Security → Secret Protection) — but does **not** auto-revoke it — Apple is not in GitHub's secret-scanning partner program, so any Apple-issued key (CloudKit, ASC, APNs) still needs a manual rotation |

`lefthook.yml` example:

```yaml
pre-commit:
  parallel: true
  commands:
    gitleaks:
      run: mise exec -- gitleaks git --pre-commit --staged --redact --verbose
```

`ci_post_clone.sh` example — Xcode Cloud runs custom build scripts with
`ci_scripts/` as the root directory, so the first line must `cd` back to the
repo root before anything else; Xcode Cloud also has no mise preinstalled (see
`xcode-cloud-single-track-ci`), so this goes through the committed `bin/mise`
wrapper, and scans the checked-out working directory rather than the staged
diff (a fresh clone has nothing staged, so `--staged` would scan zero lines
and leave this line of defence empty):

```bash
cd "$CI_PRIMARY_REPOSITORY_PATH"
./bin/mise trust
./bin/mise install
./bin/mise exec -- gitleaks dir . --redact --verbose
if [ $? -ne 0 ]; then
  echo "gitleaks detected potential secrets — failing build"
  exit 1
fi
```

### Leak SOP (rotate before cleaning history)

1. **Rotate first** (rotation is the real stop-bleed; after a force push, GitHub reflog / forks may still reach the secret until GitHub Support runs garbage collection on the repository (GitHub documents no time window), and **any fork retains it forever**):
   - CloudKit Dashboard: rotate the server-to-server key
   - Rotate the ASC API key
   - Rotate the APNs key
   - Signing cert leak: revoke + reissue in Apple Developer Center
2. Use [`git filter-repo`](https://github.com/newren/git-filter-repo) to clean history + force push (Git's own docs say `git filter-branch`'s use "is not recommended", not that it's deprecated — but `filter-repo` remains the practical choice; GitHub's own sensitive-data-removal workflow requires `filter-repo` ≥ 2.47 run with `--sensitive-data-removal`)
3. Notify GitHub support to purge forks / caches — **acknowledge that fork removal is not guaranteed**
4. Open an incident log + lessons learned in the project's incident-log location (`meetings/` for consumers of `collaboration-skills:spec-phase-orchestration`)
5. **Do not** continue other development until the four steps above are done

### Setup templates (shipped in the repo)

- `.env.example`: list all env var keys with placeholder values
- `secrets/example/README.md`: explain the local PEM directory layout (**do not include a `.pem.example` real file** — gitleaks's built-in `private-key` rule needs the full header + ≥64-character body + footer to fire, so a placeholder with only the header text won't trip it and isn't a safe substitute for keeping the real key out; if you must include a real example, explicitly allowlist it in `.gitleaks.toml`)
- `docs/setup.md`: first-clone steps for new developers

### Public commitment on Apple upstream channels

The App's commitment to users (aligned with `PrivacyInfo.xcprivacy`):

- **No PII collection**
- **No third-party tracking SDK**
- **The App does not upload events to "our" servers** (CloudKit / Game Center are provided by Apple)

Legitimate Apple upstream channels (users can disable in Settings):
- MetricKit `MXMetricPayload` / `MXDiagnosticPayload` — delivered **to the App itself**, not to Apple; this is in-app telemetry, not an upload channel
- ASC Power & Performance (*Settings → Privacy → Analytics & Improvements*, user opt-in device analytics) — a separate channel Apple collects independently of MetricKit
- Game Center scores / achievements (*Settings → Game Center*)
- ASC crash reports / TestFlight beta crashes (when the user enables Share Analytics)
- sysdiagnose (when the user actively shares via Feedback Assistant; OSLog `.private` is redacted here)

### Extra responsibilities for code reviewers

Every PR review additionally checks:
- No new secret pattern slipped through
- No secret values mentioned in docs / comments / commit messages / PR descriptions
- No identifiable info in screenshots / assets
- If privacy claims change → `PrivacyInfo.xcprivacy` + App Store metadata are updated in sync
- Any "temporarily log PII for debug" helper is removed before merging

## Rationale

- Three lines of defence are standard defence-in-depth, with complementary interception stages.
- The rotate-first SOP reflects the reality that "git history is permanently reachable in forks" — cleaning history is **not** stopping the bleed.
- GitHub's secret-scanning partner program auto-revokes tokens for its listed partners, but Apple is not one of them; the third line still catches a leaked Apple-issued key via GitHub's generic pattern alerts once Generic patterns is enabled (Settings → Advanced Security → Secret Protection), it just doesn't revoke it for you — it's a free, must-enable layer regardless.

## Deviation considerations

- **Private repo planning to go public later**: start with this skill, but allow some templates (e.g. `.pem.example`) to hold real files temporarily; clean up before going public.
- **No CI (pure local development)**: the first line of defence (local pre-commit hook) can be bypassed by `git commit --no-verify` — this cannot be technically blocked client-side. Educate contributors, and rely on the second line (CI gitleaks in `ci_post_clone.sh`) as the actual hard gate. Without CI, the second line is missing entirely; mitigations are social (code review, contributor education) rather than technical.
- **Internal corporate repo**: the third line (GitHub platform) can be skipped, but the first and second still apply.

## Verification checklist

- `.gitignore` covers the secret file extensions listed above.
- `.mise.toml` includes gitleaks + lefthook.
- `lefthook.yml` runs gitleaks pre-commit.
- `ci_post_clone.sh` runs gitleaks with fail-on-detect.
- GitHub Settings → Advanced Security → Secret Protection: Generic patterns enabled.
- `docs/setup.md` instructs `lefthook install` to activate hooks.
- `PrivacyInfo.xcprivacy` is consistent with the public commitments.

## Related skills

- `mise-tool-management`: gitleaks + lefthook installed via mise.
- `xcode-cloud-single-track-ci`: `ci_post_clone.sh` is where the second line lives.
- `oslog-logger-defaults`: `.private` interpolation matches the sysdiagnose redaction semantics.
- `apple-three-piece-analytics`: "no third-party SDK" is one of the public commitments.
- `build-time-secret-injection`: ship-in-binary identifiers (AdMob IDs via xcconfig) and CLI keys in `secrets/.env` — this skill only owns the leak-prevention lines of defence, not where those values live day to day.
- `asc-api-automation`: what the ASC API `.p8` is *used* for once it is stored safely.
- Official sources: when verifying or updating a factual or version-sensitive claim, read `references/official-docs.md`.
