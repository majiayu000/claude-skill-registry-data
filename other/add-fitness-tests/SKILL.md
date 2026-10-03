---
name: add-fitness-tests
description: Create or synchronize architecture tests from the Architecture Profile. Manual command.
disable-model-invocation: true
---
Delegate to test-engineer with a pointer prompt: apply skill `architecture-fitness-tests`. The test-engineer copies `assets/ArchitectureTests.cs.template` into `tests/<Root>.ArchitectureTests/ArchitectureTests.cs` with a shell command, replaces `{Root}`, adds tests only for rules the template lacks, runs them. Existing violations are listed, not fixed. Relay its OUT block + `UNENFORCED:` list.
