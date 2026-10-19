---
name: semantic-versioning
description: >
  Apply Semantic Versioning 2.0.0 (SemVer) principles to libraries, tools, and
  APIs. Use when determining version bumps (MAJOR, MINOR, PATCH), analyzing
  breaking changes in code or configuration, handling pre-releases and metadata,
  or setting dependency version ranges.
compatibility: >
  Agent Skills-compatible coding agents analyzing software releases,
  public APIs, package manifests, or version bump requests.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "versioning, semver, releases, api-compatibility, dependencies"
  topics: "version-control, devtools, software-development"
---

# Semantic Versioning (SemVer 2.0.0)

Semantic Versioning formalizes how software version numbers convey meaning about underlying code changes. Strict adherence to [SemVer 2.0.0](https://semver.org/spec/v2.0.0.html) enables automated dependency management, prevents unexpected runtime breakage, and clearly sets consumer expectations.

## Version Format: `X.Y.Z` (MAJOR.MINOR.PATCH)

1. **MAJOR (X)**: Incremented when making **incompatible API changes** (breaking changes).
   - Resets MINOR and PATCH to `0` (e.g., `1.4.2` -> `2.0.0`).
2. **MINOR (Y)**: Incremented when adding **backward-compatible functionality** or deprecating existing features.
   - Resets PATCH to `0` (e.g., `1.4.2` -> `1.5.0`).
3. **PATCH (Z)**: Incremented when making **backward-compatible bug fixes**.
   - (e.g., `1.4.2` -> `1.4.3`).

Additional qualifiers:
- **Pre-release**: Appended with a hyphen: `1.0.0-alpha.1`, `2.1.0-rc.3`. Pre-releases have lower precedence than the associated normal version (`1.0.0-rc.1 < 1.0.0`).
- **Build metadata**: Appended with a plus sign: `1.0.0+20261015`, `1.0.0-beta.1+exp.sha.5114f85`. Build metadata is ignored when determining version precedence.

---

## 1. Decision Flowchart for Version Bumps

```
Has public API or consumer contract changed?
│
├── YES ── Is the change backward-incompatible?
│           ├── YES ──> Increment MAJOR (reset MINOR & PATCH to 0)
│           │           (Note: in 0.y.z initial development, anything MAY change,
│           │            but 0.(y+1).0 is conventionally treated as breaking)
│           │
│           └── NO  ──> Was new functionality added or feature deprecated?
│                       ├── YES ──> Increment MINOR (reset PATCH to 0)
│                       └── NO  ──> Increment PATCH (backward-compatible fix)
│
└── NO  ── Is it an internal refactor, dependency update, or bug fix?
            ├── Internal refactor with identical behavior ──> PATCH (or no release)
            ├── Backward-compatible bug fix ─────────────> Increment PATCH
            └── Documentation or build-only change ───────> PATCH (if released)
```

---

## 2. What Constitutes a Breaking Change?

A breaking change occurs when consumers following the documented public API must modify their code, schema, or configuration to upgrade.

### Breaking (Requires MAJOR Bump)
- Removing or renaming an exported function, class, method, or public constant.
- Adding a new required parameter to an existing public function.
- Changing the return type or narrowing parameter types in public interfaces.
- Changing the ordering of positional arguments.
- Altering the behavior or side-effects of an existing function under normal inputs.
- Raising a new unchecked exception/error from an existing function where callers rely on specific error types.
- Removing support for a documented environment, CLI flag, or configuration option.
- Upgrading database schema without backward-compatible migrations.

### Non-Breaking / Compatible (Requires MINOR Bump)
- Adding new exported functions, classes, or types to the public API.
- Adding an **optional parameter** with a backward-compatible default value.
- Relaxing parameter types (accepting wider types without breaking existing callers).
- Marking an existing feature as `@deprecated` with clear migration paths (removal occurs in the next MAJOR).
- Exposing new CLI flags or configuration parameters with sensible defaults.

### Patch Fixes (Requires PATCH Bump)
- Fixing a bug without altering documented function signatures or API contracts.
- Fixing security vulnerabilities (CVEs) while preserving external contracts.
- Performance optimizations that produce identical results.
- Internal refactorings and code quality improvements.

---

## 3. The Special Status of Initial Development (`0.y.z`)

Under SemVer 2.0.0:
- Major version zero (`0.y.z`) is for initial development. Anything MAY change at any time. The public API SHOULD NOT be considered stable.
- **Ecosystem Convention**: In modern package ecosystems (Cargo, npm, uv), `0.Y.Z` treats increments of `Y` as breaking changes and increments of `Z` as compatible fixes.
- **Moving to `1.0.0`**: Once software is used in production or has defined a stable public API, release version `1.0.0`. Do not stay indefinitely on `0.x` when users depend on compatibility.

---

## 4. Common Mistakes and Anti-Patterns

| Anti-Pattern | Risk | Correct Practice |
| :--- | :--- | :--- |
| Releasing a breaking change as a PATCH | Upstream builds fail suddenly, breaking production systems | Always bump MAJOR for breaking changes |
| Removing a feature without a deprecation period | Disrupts consumers without notice | Deprecate in MINOR `N`, document migration, remove in MAJOR `N+1` |
| Changing defaults without warning | Silent behavioral change in user code | Treat default value changes as breaking if they alter outcome |
| Bumping MAJOR for purely internal refactors | Unnecessarily alerts consumers and complicates dependency resolutions | Bump PATCH if external behavior is identical |
| Using leading zeros: `1.02.3` | Invalid SemVer | Numerical identifiers MUST NOT contain leading zeroes (`1.2.3`) |

---

## 5. Examples

### Example 1: Evaluating a Python API Modification
```python
# Before (v1.3.0)
def fetch_user(user_id: int) -> User: ...

# Change proposal A:
def fetch_user(user_id: int, include_profile: bool = False) -> User: ...
# -> Result: Backward-compatible feature. Bump to v1.4.0 (MINOR).

# Change proposal B:
def fetch_user(user_id: str) -> User: ...
# -> Result: Incompatible parameter type change. Existing callers passing int break.
# -> Bump to v2.0.0 (MAJOR).
```

### Example 2: Evaluating a CLI Tool Flag Change
```bash
# Before:
tool export --format=json

# Change proposal:
# Renamed `--format` to `--output-format` and removed `--format`.
# Result: Breaking change! Any script calling `--format` fails.
# Correct approach:
# Keep `--format` as an alias, emit deprecation warning to stderr, add `--output-format`.
# Bump MINOR. When `--format` is finally removed in next major release, bump MAJOR.
```

---

## 6. Verification Checklist

- [ ] Identified all changed public interfaces, CLI arguments, and config schemas.
- [ ] Checked whether existing valid invocations continue to work without error.
- [ ] Confirmed version string matches SemVer regex: `^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$`.
- [ ] Updated version number consistently across project manifests (`pyproject.toml`, `Cargo.toml`, `package.json`, etc.).
