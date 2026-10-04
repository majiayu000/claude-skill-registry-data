---
name: release-note
description: Changelog and release notes.
disable-model-invocation: true
---

# Semantic Versioning (SemVer) Release Notes Guideline

This document defines the standard steps and rules for writing Release Notes for the project, based on [Semantic Versioning 2.0.0 (semver.org)](https://semver.org/).

## 1. Core Rules of SemVer (X.Y.Z)

Every release version must follow the **MAJOR.MINOR.PATCH** format (e.g., `1.4.2`). You must increment the respective element based on the scope of changes:

*   **MAJOR (X):** Increment when you make **incompatible API changes** (Breaking changes). When MAJOR is incremented, MINOR and PATCH must be reset to `0` (e.g., `1.4.2` $\rightarrow$ `2.0.0`).
*   **MINOR (Y):** Increment when you **add functionality** in a backward-compatible manner. When MINOR is incremented, PATCH must be reset to `0` (e.g., `1.4.2` $\rightarrow$ `1.5.0`).
*   **PATCH (Z):** Increment when you make backward-compatible **bug fixes** without adding new features or breaking existing APIs (e.g., `1.4.2` $\rightarrow$ `1.4.3`).

> **Note:** Major version zero (`0.x.x`) is for initial development. Anything MAY change at any time. The public API should not be considered stable.

### 1.1. Additional Labels (Pre-release & Build Metadata)
SemVer allows appending labels to define the lifecycle of a release more precisely:
*   **Pre-release:** Denoted by a hyphen `-` immediately following the PATCH version. These versions have a lower precedence than the associated normal version and are used for drafts or testing phases.
    *   *Examples:* `1.0.0-alpha`, `1.0.0-beta.1`, `1.0.0-rc.1` (Release Candidate).
    *   *Precedence:* `1.0.0-alpha` < `1.0.0-beta` < `1.0.0-rc.1` < `1.0.0`.
*   **Build Metadata:** Denoted by a plus sign `+` at the very end. Used to store commit hashes, build IDs, or timestamps. This metadata **does not** affect version precedence.
    *   *Examples:* `1.0.0-beta.1+exp.sha.5114f85`, `1.2.3+20260601`.

---

## 2. Step-by-Step: Writing Release Notes

When preparing a new release, follow these steps:

### Step 1: Categorization
List all merged tickets/PRs. Group them into clear categories (following Keep a Changelog standards):
*   `Added`: For new features.
*   `Changed`: For changes in existing functionality.
*   `Deprecated`: For once-stable features removed in upcoming releases.
*   `Removed`: For deprecated features removed in this release.
*   `Fixed`: For any bug fixes.
*   `Security`: To invite users to upgrade in case of vulnerabilities.

### Step 2: Determine the Version
*   If there are any breaking changes or removed APIs $\rightarrow$ **Increment MAJOR**.
*   If there are no breaking changes, but new features (`Added`) or APIs are introduced $\rightarrow$ **Increment MINOR**.
*   If the list only contains `Fixed` or `Security` updates $\rightarrow$ **Increment PATCH**.

### Step 3: Draft the Release Note
Use Markdown. Always specify the **[Version] - Release Date (YYYY-MM-DD)**. Write concise and clear descriptions targeting end-users or API integrators. Avoid blindly copy-pasting cryptic git commit messages.

---

## 3. Concrete Examples

Below are 3 scenarios for creating release notes based on project changes.

### Example 1: Patch Release (Bug Fixes)
*Current version is `1.2.3`. The team just fixed a server crash caused by empty payloads and patched a token security vulnerability.*
$\rightarrow$ **Decision:** Only bug fixes and security patches, increment PATCH to `1.2.4`.

```markdown
## [1.2.4] - 2026-06-01

### Fixed
- **API Reliability:** Handled HTTP 500 crash when an empty body (`undefined`) is sent to the Feature Flag API. The system now correctly returns a 400 Bad Request.
- **Swagger UI:** Updated the DTO to correctly render the input field in Swagger UI, resolving the fake 400 error upon execution.

### Security
- **Auth Guard:** Patched a vulnerability that allowed bypassing authentication with old cookies when the header token was expired.
```

### Example 2: Minor Release (New Features)
*Current version is `1.2.4`. The team just added a configuration sync system via Redis and an API to toggle On-chain mode. Existing APIs are unaffected.*
$\rightarrow$ **Decision:** Backward-compatible new features, increment MINOR to `1.3.0`.

```markdown
## [1.3.0] - 2026-06-15

### Added
- **Config Sync Service:** Implemented dual-storage (MongoDB + Redis) to synchronize system configuration in real-time without requiring server restarts.
- **Feature Flag API:** Added a new endpoint `PUT /api/v1/system/admin/feature-flag/onchain-mode` allowing Admins to toggle the system into On-chain mode.
- **Telemetry:** Agents now automatically emit metrics logs every 10 minutes.

### Changed
- **Logs Format:** Changed console log output format to JSON for easier extraction into the ELK stack (API responses remain unaffected).
```

### Example 3: Major Release (Breaking Changes)
*Current version is `1.3.0`. The team decided to overhaul the authentication architecture from JWT to OAuth2, removed the old `/auth/login` endpoint, and changed the response wrapper of all APIs from `{ data: ... }` to `{ payload: ... }`.*
$\rightarrow$ **Decision:** Breaking changes that will disrupt existing integrated clients, increment MAJOR to `2.0.0`.

```markdown
## [2.0.0] - 2026-07-01

> **⚠️ WARNING:** This release contains breaking changes. Please review the Migration Guide before upgrading.

### Changed
- **[BREAKING] Standard Response:** All APIs now return the `{ payload: ... }` wrapper instead of `{ data: ... }`. Client SDKs must update their parsers.
- **[BREAKING] Authentication:** Migrated the core authentication mechanism to the OAuth2 standard.

### Removed
- **[BREAKING] Legacy Auth:** The endpoints `/api/v1/auth/login` and `/api/v1/auth/refresh` have been officially removed from the system.
- **Legacy Transactions API:** Removed the Off-chain v1 processing module, which was deprecated in version 1.1.0.
```

---

## 4. Best Practices: Leveraging Conventional Commits
To ensure accurate version bumping and enable **automation (CI/CD)**, the team should adopt the [Conventional Commits](https://www.conventionalcommits.org/) specification:
*   Commits starting with `fix: ...` $\rightarrow$ Automatically resolve to a **PATCH**.
*   Commits starting with `feat: ...` $\rightarrow$ Automatically resolve to a **MINOR**.
*   Commits containing `BREAKING CHANGE:` in the footer, or an exclamation mark `!` (e.g., `feat!: ...`) $\rightarrow$ Automatically resolve to a **MAJOR**.

By doing so, determining the version (Step 2 above) is no longer subjective and can be fully automated using tools (like Semantic-release or Standard-version).
