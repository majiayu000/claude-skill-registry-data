---
name: ros2-development
description: "Implement or change ROS 2 Jazzy packages, nodes, interfaces, launch files and configuration in a colcon workspace. Use for building and validating a development change, including tests that report success without running. For a live QoS, TF, IMU or odometry fault, use ros2-troubleshooting."
---

# ROS 2 development

Work from the workspace's actual package graph and installed artifacts. This
skill supplies a development workflow, a check for empty test runs, and an
optional evidence tracking tool for task handoff. It does not prescribe a new
workspace layout or replace the project's build conventions.

## Build the affected package graph

Use `colcon list` to identify package names and build types. Build the changed
package and its workspace dependencies with `colcon build --packages-up-to
<package>`. `--packages-select` alone does not build its dependencies. For a
message or public API change, include affected consumers in the build and tests.
Preserve the project's existing build/install flags and dependency versions.

Build in a shell with the intended underlay, not the workspace's old overlay.
Use a separate shell to source the resulting `install/setup.bash` and inspect
`ros2 pkg prefix <package>`: otherwise an older installed copy can appear to
validate the source change.

## Require tests to have run

`colcon test` and `colcon test-result` can both succeed with zero tests. Use a
fresh result directory so a previous passing report cannot satisfy this run:

The variable `ROS2_SKILL_DIR` in the examples below represents the absolute path
to the loaded skill directory. The agent sets this path internally based on
where the skill was discovered and loaded; do not ask the user for this path.

```bash
# After building, in the workspace root. Replace my_package with actual names.
# For pytest packages; omit --python-testing pytest for other test frameworks.
ROS2_SKILL_DIR="/absolute/path/to/ros2-development" # Set by agent to loaded skill directory.
results="$(mktemp -d /tmp/ros2-test-results.XXXXXX)"
colcon test --packages-select my_package --return-code-on-test-failure \
  --python-testing pytest --test-result-base "$results" &&
python3 "${ROS2_SKILL_DIR}/scripts/check_test_results.py" "$results" \
  --packages my_package --require-test my_package::test_changed_behavior
```

Replace `test_changed_behavior` with the actual regression test for the change;
repeat `--require-test PACKAGE::ID` when more than one test is needed. It matches
a full JUnit `classname.name` or a dot-delimited suffix, or a CTest name. Omitting
a pytest `[parameter]` suffix selects that test's parameter group and requires
at least one non-skipped case. The output lists observed test IDs and states.
For ament CMake tests, the checker follows the current CTest wrapper's recorded
JUnit path and checks the inner cases, even if that path was configured in the
build directory. A passed wrapper cannot substitute for all-skipped inner tests.

The bundled check uses installed `colcon test-result` and requires at least one
non-skipped test in **each named package**, plus the requested tests. Exit **0**
means those reports contain executed, passing tests; **1** means a recorded test
or test-process failure/error; **2** means missing, empty or unparseable evidence.
An ament CTest crash/timeout is a recorded failure. Colcon's Python
`pytest.missing_result` placeholder alone is inconclusive: inspect the test log
to distinguish a runner problem from a crash before editing the implementation.
Without `--require-test`, even linters alone can satisfy the check. A test name
does not establish assertion quality: choose a regression that would reject the
reported defect, or exercise the changed behaviour with a runtime probe. Do not
describe style checks or a vacuous smoke test as functional verification.
It reads reports and sends no ROS commands. Keep the printed result directory
when reporting a failure. Inspect `colcon test`'s own exit status and diagnostics
as well; reports cannot clear an invocation error. A package intentionally without tests is not a failed
implementation; state the missing coverage and verify its changed behaviour.

For a Python package that uses pytest, pass `--python-testing pytest` to
`colcon test` (or use the workspace's explicit equivalent). Do not rely on
`setup.py`'s `tests_require` to select the runner: newer setuptools can ignore
that field and colcon can select a different framework, collecting no tests.

## Verify the installed behaviour

Choose the smallest runtime check that exercises the change. A successful build
does not prove that a launch file, parameter file or executable was installed.
Use [verification.md](references/verification.md) for the relevant artifact:
Python/C++ nodes, interfaces, launch/config, or lifecycle and sensor behaviour.
Check the observable result again after a correction; keep a failed probe
separate from a confirmed defect in the implementation.

## Optional evidence tracking and handoff

When handing off a task to another agent session or collaborator, the optional
`evidence.py` tool can record snapshots and verify whether the recorded context
remains unchanged at handoff time. See [references/handoff.md](references/handoff.md)
for instructions on `begin`, `finish`, and `inspect`.

This tool records artifact hashes and declared execution metadata; it does not
run user commands and does not guarantee that the generated code is correct.

## Evidence

The result checker is tested against passing, failing, empty and skipped
reports, including fresh-directory separation in real Python and CMake colcon fixtures.
This workflow provides diagnostic checks; an agent comparison has **not** established
a performance gain from its prose.
Official semantics: [package selection](https://colcon.readthedocs.io/en/released/reference/package-selection-arguments.html),
[test](https://colcon.readthedocs.io/en/released/reference/verb/test.html),
[test results](https://colcon.readthedocs.io/en/released/reference/verb/test-result.html).
