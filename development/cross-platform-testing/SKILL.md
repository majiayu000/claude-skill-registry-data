---
name: cross-platform-testing
description: >
  Design and debug test matrices across operating systems, CPU architectures, and language/runtime
  versions: what actually differs (paths, line endings, case sensitivity, file locking, permissions,
  encodings, locale, time zones, endianness, floating point, shell), how to write portable tests,
  and how to build a GitHub Actions matrix (include/exclude, fail-fast, experimental legs, pinned
  runner labels, arm64) that is informative without exploding in cost. Use when software must run
  on Linux, macOS, Windows or multiple Python/Node/Rust/Java versions, when CI passes on one OS
  but fails on another, or when adding a support matrix. Do NOT use for general CI authoring
  (ci-github-actions), CI security hardening (github-actions-security), browser/device test
  automation (playwright-testing), or benchmarking (performance-regression-testing).
compatibility: >
  Agent Skills-compatible coding agents. GitHub Actions hosted runners (labels verified against
  actions/runner-images README on 2026-10-15). Concepts apply to other CI systems.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "cross-platform, ci, github-actions, matrix, windows, macos, arm64, portability, testing"
  topics: "software-development, testing, ci"
---

# Cross-Platform Testing

Goal: learn about platform-specific failures before users do, at a cost you can sustain. That requires (1) knowing *which differences bite*, (2) tests that expose them, and (3) a matrix sized to your support promise.

Boundaries: general workflow writing is `ci-github-actions`; supply-chain hardening of workflows is `github-actions-security`; browser coverage is `playwright-testing`; slow-down detection is [performance-regression-testing](../performance-regression-testing/SKILL.md); contract compatibility between services is [contract-testing](../contract-testing/SKILL.md).

## Non-negotiable rules

1. The matrix mirrors the support policy. Test what you claim to support; do not claim what you do not test; document the rest as best-effort.
2. Never skip or mark platform tests as expected-failure to get green without an issue and a reason in the skip message (`skipif(sys.platform == "win32", reason="...")`).
3. CI jobs get least privilege and no production credentials; matrix legs run untrusted PR code on shared runners, so do not expose secrets to fork PRs and follow `github-actions-security` (pin actions, minimal `permissions`).
4. Do not paper over differences by loosening assertions. Normalize at the boundary (paths, newlines, encodings) in the code, or in a documented test helper.
5. Reproduce platform failures with the actual platform (CI re-run, VM, or container for Linux variants); do not guess at Windows or macOS behavior from Linux.

## What differs (the checklist that finds real bugs)

| Area | Typical break | Portable practice |
|---|---|---|
| Paths | `/` vs `\`, drive letters, UNC, 260-char legacy limit, case-insensitive default FS on macOS/Windows vs case-sensitive Linux | `pathlib`/`Path`/`path.join`; never string-concatenate; test with names differing only by case; avoid reserved Windows names (`CON`, `NUL`) |
| Line endings | CRLF checkouts; golden files differ | `.gitattributes` (`* text=auto`, `eol=lf` for fixtures); open files with explicit newline handling; compare normalized text |
| Encoding | default text encoding varies; console codepage | explicit `encoding="utf-8"`; test non-ASCII filenames and content; names may arrive as NFD from some macOS filesystems (HFS+ normalized; APFS preserves bytes), so compare normalized forms |
| Permissions & symlinks | exec bit and chmod meaningless on Windows; symlinks need privilege on Windows | gate tests by capability, not by OS name where possible |
| File locking | Windows refuses to delete/rename open files | close handles; retry-aware cleanup; avoid deleting a cwd or open temp file |
| Processes & shell | `bash` vs `cmd`/PowerShell quoting; `python` vs `python3`; signals unsupported on Windows | spawn with argument lists, `shell=False`; `sys.executable` for Python subprocesses |
| Time | time zones, DST, clock resolution (Windows coarser), locale date formats | inject clocks; test with fixed `TZ`; use UTC internally |
| Numeric | endianness, 32 vs 64-bit, x86 vs arm64 floating point (FMA, SIMD), `long` size, struct padding | tolerances for floats (`approx`), explicit-width types, `struct` with `<`/`>`; do not compare float hashes |
| Environment | env var case (Windows case-insensitive), `HOME` vs `USERPROFILE`, temp dir paths | use framework temp dirs; never hardcode `/tmp` |
| Dependencies | wheels/binaries missing for an arch; build tools absent | test installation from a clean environment on each leg |
| Filesystem semantics | atomic rename, `fsync`, sort order of directory listings | sort listings explicitly; do not rely on order |

## Workflow

### 1. Write the support statement first

Example: "Linux x64 and arm64, macOS (current and previous major, arm64), Windows x64; Python 3.11 to 3.14." Anything beyond is untested. Derive the matrix from this sentence, not from habit.

### 2. Design the matrix

Dimensions: OS x architecture x language-version (x optional dependency flavor). Full cross-product grows multiplicatively. Reduce with judgment:

- Full language-version sweep on **one fast OS** (Linux x64) to catch version issues cheaply.
- Latest stable language version on **every OS/arch** to catch platform issues.
- Oldest and newest supported versions on the slow/expensive OS only if you have platform-specific code in version-sensitive areas.
- Nightly/scheduled legs for pre-release language versions and "latest" runner images, marked non-blocking.

GitHub Actions example (matrix keys are free-form; `include` adds legs, `exclude` removes combinations; `fail-fast: false` lets all legs report):

```yaml
name: tests
on: [push, pull_request]
permissions:
  contents: read
jobs:
  test:
    name: ${{ matrix.os }} / py${{ matrix.python }}
    runs-on: ${{ matrix.os }}
    timeout-minutes: 20
    continue-on-error: ${{ matrix.experimental }}
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-24.04, ubuntu-24.04-arm, windows-2025, macos-26]
        python: ["3.11", "3.14"]
        experimental: [false]
        include:
          - { os: ubuntu-24.04, python: "3.12", experimental: false }
          - { os: ubuntu-24.04, python: "3.13", experimental: false }
          - { os: ubuntu-24.04, python: "3.15", experimental: true }
    steps:
      - uses: actions/checkout@v4   # pin to a full SHA (or at least the current major) per your policy
      - uses: actions/setup-python@v7
        with:
          python-version: ${{ matrix.python }}
          allow-prereleases: ${{ matrix.experimental }}
      - run: python -m pip install -e ".[test]"
      - run: python -m pytest -ra
```

Notes grounded in docs: the `include`/`exclude`/`fail-fast`/`continue-on-error: ${{ matrix.experimental }}` pattern is the documented way to run experimental legs without failing the workflow; `actions/setup-python` takes `python-version` (and an `architecture` input defaulting to the host); its README currently shows `@v7`. Pin third-party actions to a full commit SHA if your policy requires it (the `@v4`/`@v7` tags here are illustrative; use the current major or a SHA, consistently across all workflows). The version list is dated: the supported set moves each October, so re-check python.org release status when editing (here 3.14 gates, 3.15 is the pre-release experimental leg, and 3.10 is end-of-life). This YAML was not executed in a real repository; validate it with your CI before relying on it.

### 3. Pin runner labels deliberately

Verified labels (runner-images README, 2026-10-15): `ubuntu-latest` = Ubuntu 24.04 x64; `ubuntu-24.04-arm` and `ubuntu-22.04-arm` for arm64; `windows-latest` = Windows Server 2025 x64, `windows-11-arm` for Windows arm64; `macos-latest` = macOS 26 arm64, `macos-15` arm64, `macos-15-intel` and `macos-26-intel` for x64. The README notes `-latest` labels migrate gradually over one to two months, and some images are deprecated over time. Prefer explicit versions for gating legs (reproducible), and keep one non-blocking `*-latest` leg as an early warning. Labels change; re-check the runner-images page when editing the matrix.

### 4. Write portable tests

```python
from pathlib import Path

def test_roundtrip_unicode_filename(tmp_path: Path):
    p = tmp_path / "café ☃.txt"
    p.write_text("line1\nline2\n", encoding="utf-8")
    assert p.read_text(encoding="utf-8").splitlines() == ["line1", "line2"]
    assert [x.name for x in sorted(tmp_path.iterdir())] == [p.name]
```

Principles: temp dirs from the framework; explicit encodings and newline handling; sorted directory listings; capability-based skips over OS-name skips (for symlinks, `hasattr(os, "symlink")` is true on Windows even when creation is not permitted, so probe by actually trying, as below); assertions on normalized values (`Path` equality, `os.path.normcase` only when comparing for case-insensitive FS semantics).

```python
import functools, os, tempfile

@functools.lru_cache(maxsize=None)
def can_symlink() -> bool:
    with tempfile.TemporaryDirectory() as d:
        try:
            os.symlink(os.path.join(d, "target"), os.path.join(d, "link"))
            return True
        except (OSError, NotImplementedError):
            return False

# @pytest.mark.skipif(not can_symlink(), reason="symlink creation not permitted; see issue #123")
```

Add targeted tests for each platform-conditional branch in your code: if code says `if sys.platform == "win32"`, a Windows leg must run it. Check with coverage per leg (combine reports) to find platform branches never executed.

### 5. Triage a failure that appears on one leg

1. Read the failing leg's log first; do not assume Linux behavior.
2. Classify: environment (tool missing, encoding, line ending), code (path handling, locking), test (hardcoded separators), dependency (no wheel for arch), infra flake (network, runner).
3. Add the minimal reproducer as a test that fails on that leg only, then fix.
4. For a flake, rerun once; if it recurs on the same leg, treat as real. Track flakes; quarantine with an issue and an owner, not silently.
5. If you cannot access the platform locally, add targeted diagnostics (print `platform`, `sys.getdefaultencoding()`, file-system case sensitivity probe) in a temporary debugging branch, then remove them.

### 6. Keep cost and signal in balance

- Set `timeout-minutes` and use `concurrency` with `cancel-in-progress` for PRs to stop superseded runs.
- Cache dependencies via the setup action's cache option (`cache: pip`) or an explicit cache step, keyed on lockfiles.
- Split: fast core suite on all legs; slow/integration suite on one or two legs.
- `max-parallel` limits concurrent legs if you share a constrained runner pool.
- Required status checks must list stable job names (use explicit `name:` as above); changing matrix values changes check names, so update branch protection.

## Worked example: "passes on Linux, fails on Windows"

Symptom: `test_export_writes_report` fails on `windows-2025` with `PermissionError` when the test itself removes its output (an explicit `rmtree`/`unlink` in the test body; pytest does not delete `tmp_path` at teardown, it keeps recent base dirs), and a golden-file comparison differs by `\r\n`.

- Diagnosis 1: the code under test opens the report with `open(path)` and never closes it; Windows cannot delete open files. Fix: use a context manager.
- Diagnosis 2: the golden file was checked out with CRLF by autocrlf and the code writes with the platform newline. Fix: write explicit `newline="\n"` in the code (a real product decision: stable output across platforms) and add `*.golden text eol=lf` to `.gitattributes`.
- Add a regression test asserting bytes equal `b"a\nb\n"` rather than text-mode comparison.

## Anti-patterns

- Testing only on Linux then shipping a Windows installer.
- Growing the matrix by default with every new Python version on every OS.
- `fail-fast: true` (default) hiding the other legs' failures when diagnosing; or `continue-on-error` on everything so nothing gates.
- Using `windows-latest`/`macos-latest` as the only labels and being surprised by image upgrades.
- Skipping tests by OS name without reason or issue.
- Mocking `os.name`/`sys.platform` instead of running the real platform for filesystem behavior.
- Treating arm64 as "same as x64": native extensions, SIMD paths, and float results can differ.
- Secrets or deployment steps in matrix jobs triggered by fork PRs.

## Verification checklist

- [ ] Support statement written; matrix derived from it
- [ ] Gating legs pinned to explicit runner labels; one non-blocking latest/prerelease leg
- [ ] `fail-fast: false`, `timeout-minutes`, least-privilege `permissions` set
- [ ] Tests use framework temp dirs, explicit encodings, sorted listings, no hardcoded separators
- [ ] Every `sys.platform`/arch conditional in code is executed on a matching leg
- [ ] Skips carry a reason and an issue link
- [ ] Required status check names are stable and documented

## References

- [Platform difference deep dive and debugging recipes](references/platform-differences.md)
- [Scenarios for evaluating this skill](references/scenarios.md)
- [Sources and provenance](references/sources.md)
