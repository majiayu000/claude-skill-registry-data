---
name: genotoxic-current
description: Triage surviving production mutants and test-statement removals with reproducible result accounting, explicit mapping uncertainty and graph context.
license: CC-BY-SA-4.0
metadata:
  status: experimental-unbenchmarked
---

# Mutation finding triage

Use for an existing mutation campaign or a requested test-gap investigation.
Select the tool for the project's actual language and framework. Review its
current stable release, runtime requirements, license and output schema. Install
into a separate qualified environment; do not install every ecosystem or alter
the project's dependencies merely to follow a generic recipe.

Freeze source, test, dependency, tool and configuration hashes. Record the
baseline command, selected tests, timeouts, worker limits and exclusions. Run the
unmodified tests successfully first. Infrastructure errors, unavailable parsers,
timeouts and interrupted campaigns need their own outcomes and diagnostics.

Retain every generated mutant ID, exact source edit and tool outcome. Report
generated, excluded, attempted, completed, killed, survived, untested, timed-out
and failed counts. Declare denominators; a tool's tested-only score can conceal
untested code. Recompute counts from raw records and reject missing/duplicate
IDs. Preserve invalid or equivalent mutants with their exclusion evidence.

For the qualified Python mutmut 3.8.0 path, use a project configuration:

```toml
[tool.mutmut]
source_paths = ["src/"]
pytest_add_cli_args_test_selection = ["tests/"]
```

Run `mutmut run --max-children 1`, then `mutmut results --all true` and
`mutmut export-cicd-stats`. The JSON aggregate is
`mutants/mutmut-cicd-stats.json`; retain per-mutant metadata and source edits too.
The old `--paths-to-mutate`, `--runner` and `junitxml` commands are unavailable.
The project must be recognizable even for help commands. POSIX fork support is
required; native Windows needs a qualified WSL/container environment. Qualify
process isolation with actual setup rather than disabling fork safety. A
container campaign needs bounded private semaphore storage as well as writable
scratch space. Do not reuse cached results after result-affecting input changes.

Use graph analysis for context, with its exact source scope and language/parser
inventory. Trailmark 0.5.0's Python path was exercised with a separately pinned
offline grammar. Other languages require their own parser qualification. Keep
CLI and Python API imports in the same qualified environment; installing a tool
does not make it importable from an unrelated project environment.

Call `QueryEngine.from_directory(..., language=...)`, run `preanalysis()` and
retain `to_json()`. Resolve source paths and line spans against the same frozen
source version. Match function/method identities, including qualified names and
nested scopes. A diff hunk header is not necessarily the changed line. Preserve
multiple candidates and unresolved locations instead of choosing by order.

Use callers, entrypoint paths, ancestors and complexity as prioritization
evidence. Zero callers can mean an exported API, dynamic callback or incomplete
graph. An unmapped finding is unresolved. Neither condition establishes dead
code, equivalence or a false positive. Inspect the actual call boundary and
contract before recommending removal or dismissal.

For each survivor, inspect its exact edit and rerun the relevant test against
that mutant. Distinguish a reproducible behavior gap, a proven equivalent edit,
an excluded API/input domain, inadequate test selection, and unresolved or
infrastructure outcomes. Equivalence needs type, input and side-effect evidence;
logging, errors and cleanup may be externally observable contracts. Complexity
thresholds are heuristics, not severity assessments.

For Necessist removals, retain the test identity and removed span separately
from any inferred production call. Respect actual test-directory boundaries;
the substring `test` also occurs in production paths such as `contest.py`.
Resolve aliases, receiver types and overloads when possible. Otherwise retain
all candidates. A passing removal does not establish that cleanup or an
assertion is unnecessary under the full test/resource contract.

Group evidence by resolved production identity without consuming it after the
first mutant. Preserve every mutation and removal ID and the many-to-many
relationships. Same-function observations help prioritize investigation; they
do not prove both tools discovered the same missing assertion.

Add a minimal regression that distinguishes the real contract from the mutant.
Use properties and fuzzing where their generators and oracle fit the gap, and
retain the reproducing regression. Re-run fixed mutant identities under the
same budgets, plus relevant unmodified integration tests. Keep remaining
untested, excluded, failed and unresolved cases visible in the final report.

See [qualification and scope](references/qualification.md). Tool controls and
source-example reproductions do not establish coding-agent improvement.
