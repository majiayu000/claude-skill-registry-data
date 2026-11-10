---
name: repo-execution-context
description: Identify the working directory, execution environment, and repository-supported command for tests, builds, setup, or local services when that path is unclear. Use for unfamiliar repositories or unresolved host, container, devcontainer, and task-runner workflows; reuse an already established path for the same task.
---

# Repository Execution Context

Resolve where and how the requested repository command should run. This skill
selects an execution path; the original task determines whether to execute it.

## Choose the path

1. Identify the requested operation, checkout, and package or service. Follow
   applicable repository instructions. Reuse a user-supplied repository command
   or a path established earlier in this task unless relevant files, scope, or
   evidence have changed; repeated README discovery adds no value.
2. When the path is unclear, start with available target-package documentation
   or the root README and follow relevant pointers. Inspect only the wrappers,
   scripts, manifests, container configuration, or CI needed for the operation.
   Check referenced commands exist. If sources disagree, trace the relevant
   wrapper and compare current scripts and CI; explain the discrepancy rather
   than treating a README command as unconditional authority. Surface unresolved
   choices that affect correctness or risk before execution.
3. Select the documented entry point for this operation. Preserve its working
   directory, arguments, environment, and required setup. Prefer a maintained
   wrapper such as `make test`, `just test`, or a project script over rebuilding
   its sequence by hand. Use raw language commands when the repository supports
   that path or inspection finds no wrapper or container requirement.
4. Confirm the execution boundary for this operation:
   - A documented container command, dedicated test service, or devcontainer
     workflow establishes a container path. Keep its setup and commands there;
     a missing container runtime is a blocker, not evidence for host execution.
   - A production Dockerfile, database-only Compose stack, or generic bind mount
     alone does not place application tests in a container. Host tests may use
     containerized dependencies; distinguish those processes.
   - Use the repository's actual service names and configuration. Adjust a
     wrapper only when needed for the requested subset or diagnosis, after
     checking its argument forwarding and setup behavior.
5. Check prerequisites and side effects before executing. Identify missing tools
   or access and keep the selected execution environment. Restore dependencies
   or install tools only within existing authorization and repository rules;
   documentation alone does not authorize migrations or external mutations.
   For service startup, use available runtime-isolation guidance when ports or
   shared state can collide.

## Result

Return the working directory, entry-point command, execution environment, and
the relevant source for the choice. Mention unresolved prerequisites or source
conflicts. Distinguish a selected or proposed command from one actually run;
report execution results only when observed within the original task's scope.
