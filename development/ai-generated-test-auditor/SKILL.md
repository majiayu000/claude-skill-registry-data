---
name: ai-generated-test-auditor
description: 当 AI 写完测试、要决定信不信这份测试时使用。查三类假信心：断言与实现是否同源复制、有没有边界与异常用例、失败信号够不够强；再规划 2–5 个突变抽样，能执行时再实跑，看把被测代码改坏之后测试会不会变红，没实跑就不声称测试抓得住错。测试全绿不等于代码对，也可能是测试根本抓不住错。要决定整份 diff 能不能合并时走 ai-diff-review-protocol。
category: ai-usage/code-review
version: 0.1.1
status: draft
priority: P1
compatible_agents:
  - claude-code
  - codex
  - cursor
  - codebuddy
  - nestudy
  - generic-llm-agent
display_name: AI 测试体检
outputs:
  - chat
max_rounds: 20
suggest_hint: 用「AI 测试体检」查这份 AI 写的测试是不是照抄实现、缺不缺边界，并规划 2–5 个突变抽样，能执行时再实跑
---

# ai-generated-test-auditor

Use this skill when an AI has already proposed or written tests and you need to decide whether those tests are actually protecting behavior, or just producing a reassuring green checkmark.

This skill audits **test quality**, not product correctness. Its job is to find weak assertions, implementation mirroring, missing boundary/error cases, and evidence that the suite would stay green even after a meaningful bug.

## What this skill does

- Separates the **behavioral contract** from the AI-generated test code.
- Checks whether tests rely on an **independent oracle** or merely replay implementation logic.
- Audits coverage shape:
  - happy path;
  - boundary values;
  - invalid input / failure paths;
  - state transitions / side effects;
  - regressions for previously known bugs.
- Plans 2–5 **reversible sample mutations** that should make good tests fail, and runs them only when the tests can be executed, the user agrees, and the code can be restored (Step 5). Otherwise the plan is the deliverable and runtime evidence is marked missing.
- Produces a verdict: **usable / usable with gaps / weak / misleading**.

## Good fits

Use it for:

- reviewing tests created by Copilot, ChatGPT, Claude, Cursor, Aider, or similar tools;
- checking whether a generated suite only tests the obvious path;
- spotting tautological assertions like “expected = same helper as production code”;
- deciding what a human reviewer must strengthen before merging;
- preparing a focused test-review handoff for another engineer or agent.

## Not for

Do **not** use this skill to:

- claim the underlying implementation is correct;
- replace real test execution;
- generate a full production-ready test suite from scratch;
- approve risky refactors without runtime evidence;
- decide whether a whole diff can be merged. Use `ai-diff-review-protocol` for that; it sends the tests inside the diff back here.

If the user actually wants new tests written, a test-authoring skill should do that first. Come back to this skill once there is a candidate suite to inspect.

## Required inputs

Ask for the smallest set that makes an audit meaningful:

1. **Behavioral target**
   - what function, module, endpoint, workflow, or bugfix the tests are supposed to protect;
2. **AI-generated tests**
   - pasted code, file content, or a precise summary of key assertions;
3. **Implementation summary**
   - enough to see whether tests copy internal logic instead of checking behavior;
4. **How tests would be run**
   - command, framework, or at least the expected environment;
5. **Any known edge cases or failure modes**
   - if already known by the user or issue tracker.

If these are missing, say exactly what is missing. Do not pretend to certify tests you cannot inspect.

## Core workflow

### Step 1: restate the contract under test

Before reading assertions, write down:

- what external behavior should be true;
- what inputs matter;
- what outputs, state changes, or side effects matter;
- what should fail, reject, or stay unchanged.

Prefer contract language such as:

- accepts / rejects;
- returns / raises / logs / persists;
- preserves ordering / idempotence / monotonicity;
- does not mutate unrelated state.

### Step 2: classify each test by evidence strength

For each test or cluster of similar tests, classify the oracle:

- **independent oracle** — compares against a hard requirement, fixture, known output, invariant, or manually reasoned expectation;
- **derived oracle** — expected value computed by a simpler but still independent method;
- **mirrored logic** — expected value built by repeating the production algorithm or the same branch conditions;
- **weak signal** — only checks “did not crash”, status 200, non-null, truthy, or snapshot noise without semantic assertions.

Anything in the last two categories is high-risk when AI wrote it.

### Step 3: audit coverage shape

Check whether the suite includes, skips, or hand-waves:

1. **happy path**;
2. **boundary cases**
   - empty input, zero, one, min/max, exact threshold, off-by-one neighbors;
3. **error / invalid input cases**;
4. **stateful or side-effect cases**
   - retries, duplicate calls, persistence, ordering, cleanup;
5. **regression hooks**
   - tests tied to a known bug or failure mode.

If a category is absent, name the missing risk explicitly.

### Step 4: look for AI-specific failure patterns

Treat these as red flags:

- assertions copied from implementation formulas or helper functions;
- mocks so aggressive that real behavior disappears;
- snapshot tests with no focused semantic assertions;
- exact string assertions on unstable text without checking the real contract;
- tests that only verify the current implementation, not intended behavior;
- “parameterized” cases that are all the same shape;
- boundary values mentioned in comments but not asserted;
- TODO/FIXME placeholders left in test code;
- tests for private helpers while public behavior stays untested.

### Step 5: plan reversible sample mutations

Pick 2–5 small mutations that a decent suite should catch.

Prefer mutations like:

- flip `>` to `>=` or `<` to `<=` at a threshold;
- remove validation or an early return;
- replace a computed value with a constant;
- swap sort order;
- skip persistence / callback / emitted event;
- change one branch’s sign, key, or unit conversion.

For each mutation, record:

- target behavior being challenged;
- likely file/function or logic point;
- what test should fail;
- what it means if no test would fail.

If you cannot run mutations in the current environment, still provide the **plan** and label runtime evidence as missing.

Run the plan only when all of these hold: you can execute the tests, the user has agreed, and every file can be restored exactly. Then:

1. Work where nothing can be lost: a clean working tree (`git status --porcelain` prints nothing) or a separate worktree or copy of the project. Never mutate files that have uncommitted changes you cannot restore.
2. Run the tests the plan names once without changes. They must pass; otherwise the mutation results mean nothing.
3. Apply one mutation, run the named tests, record red or green.
4. Restore the file (`git checkout -- <file>`, `git restore <file>`, or copy the saved original back) and confirm the tree is clean before the next mutation.
5. Report each mutation as `killed` (a named test turned red), `survived` (the suite stayed green) or `not run`, with the command you used.

If any condition fails, deliver the plan only.

### Step 6: produce a verdict

Use one of:

- **usable** — covers core behavior with mostly independent oracles and meaningful failure signals;
- **usable with gaps** — main path is protected, but specific missing edges or weak assertions remain;
- **weak** — many tests are shallow, mirrored, or leave important behavior unprotected;
- **misleading** — a green suite would create false confidence because the assertions barely test the contract.

## Output format

Use this structure:

### 1. Audit target
- what the tests claim to protect;
- what evidence was actually available.

### 2. Contract summary
- key behaviors;
- failure modes that should matter.

### 3. Evidence audit
A compact table with:
- test or cluster;
- oracle type;
- strength;
- concern.

### 4. Coverage gaps
- missing boundary cases;
- missing error cases;
- missing side-effect or regression coverage.

### 5. Sample mutation plan
For each mutation:
- mutation idea;
- behavior it probes;
- test expected to fail;
- interpretation if suite stays green.

### 6. Verdict
- usable / usable with gaps / weak / misleading;
- what to strengthen next.

### 7. Evidence status
Tag statements when useful:
- `given`;
- `observed in test code`;
- `inferred from implementation summary`;
- `should be verified by execution`;
- `missing evidence`.

## Boundary rules

- Do not claim coverage percentages you did not measure.
- Do not claim mutation resistance unless mutations were actually executed.
- Do not rewrite the whole suite unless the user explicitly asks for authoring help.
- Do not confuse “tests pass” with “tests are meaningful”.
- If only a prose summary is available, downgrade confidence and say so.

## Deterministic helper

This skill includes a dependency-free helper script:

- `scripts/check_test_audit_manifest.py`

It validates whether a planned audit packet is structurally complete enough to review consistently:

- required fields present;
- implementation file paths unique;
- test case IDs unique;
- mutation sample IDs unique;
- every mutation points to declared implementation files and named test cases;
- warns when happy path, boundary, error, or side-effect coverage is missing from the audit packet;
- warns about keys it does not know instead of ignoring them silently.

Allowed values, with the Step 2 and Step 3 wording the script also accepts:

| Field | Canonical value | Also accepted |
|---|---|---|
| `oracle` | `independent` | independent oracle |
| `oracle` | `derived` | derived oracle |
| `oracle` | `mirrored` | mirrored logic |
| `oracle` | `weak-signal` | weak signal |
| `kind` (test case) | `happy-path` | happy path |
| `kind` (test case) | `boundary` | boundary cases |
| `kind` (test case) | `error-path` | error / invalid input cases |
| `kind` (test case) | `side-effect` | stateful or side-effect cases |
| `kind` (test case) | `state-transition` | state transition |
| `kind` (test case) | `regression` | regression hooks |

A mutation's `kind` is free text (for example `remove-validation`, `boundary-flip`).

Example manifest shape:

```json
{
  "target": "Validate AI-generated tests for create_user",
  "implementationFiles": ["src/user_service.py"],
  "testCases": [
    {
      "id": "accepts_valid_name",
      "kind": "happy-path",
      "oracle": "independent",
      "summary": "Creates a user when name and email are valid"
    },
    {
      "id": "rejects_blank_name",
      "kind": "error-path",
      "oracle": "independent",
      "summary": "Raises ValueError for blank name"
    }
  ],
  "mutationSamples": [
    {
      "id": "skip_blank_name_validation",
      "targetFile": "src/user_service.py",
      "kind": "remove-validation",
      "expectedFailingTests": ["rejects_blank_name"],
      "why": "A real guard should be observable through the public API"
    }
  ]
}
```

Run it with any Python 3 environment:

```bash
python3 scripts/check_test_audit_manifest.py path/to/test-audit-manifest.json
python3 scripts/check_test_audit_manifest.py --selftest
```

Exit codes: 0 means the manifest is valid (warnings may remain), 1 means it has problems (missing fields, unknown values, a mutation naming a test that is not in the packet), 2 means the file cannot be read as JSON or the arguments are wrong.

## Heuristics this skill should apply

Prefer these questions when deciding whether AI-generated tests are trustworthy:

- Would the test still pass if the implementation returned a constant or cached default?
- Does the expected value come from an independent requirement, or from reusing production logic?
- Are there threshold neighbors, invalid shapes, and empty cases?
- Does any test prove an important side effect happened, not merely that the function returned?
- Is there at least one mutation per major behavioral promise that should clearly turn the suite red?

## Mini examples

- If the production code sorts ascending and the test builds `sorted(input)` as its expected value, that is often mirrored logic, not a strong oracle.
- If an API test only checks status `200` and “response is not null”, it does not prove the payload contract.
- If deleting an input-validation branch would leave the suite green, the suite is giving false confidence exactly where users are likely to get hurt.

## Success criterion

The skill has done its job when the user can say:

1. which tests genuinely protect behavior;
2. which tests only mirror implementation or check noise;
3. which edge and failure cases are still unprotected;
4. which 2–5 sample mutations should be tried next;
5. and how much trust the current suite has earned.

## 变更记录 / Changelog

| 版本 | 日期 | 变更 | 类型 |
|---|---|---|---|
| 0.1.1 | 2026-09-26 | description 与 suggest_hint 不再承诺"验证测试真会变红"，改成"规划 2–5 个突变抽样，能执行时再实跑"，Step 5 补上实跑的安全步骤（干净工作区或副本、先征得同意、逐个突变、逐个恢复）；脚本接受正文用语（mirrored logic、weak signal 等）并在正文列出枚举，改用 argparse（--help 不再被当成文件名），传入目录、非 UTF-8、坏 JSON 时报错退出 2，不认识的键给警告，补 --selftest；示例命令改为 python3；与 ai-diff-review-protocol 互相点名 | patch |
| 0.1.0 | 2026-09-05 | 初始版本 | minor |
