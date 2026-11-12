---
name: crystal
description: Use when working on Crystal projects. Detected by the presence of a shard.yml file.
disable-model-invocation: false
user-invocable: false
allowed-tools: Bash
---

# Crystal Project Workflow

## Shard management

- Never manually edit `shard.lock` — run `shards install` to regenerate it after changing `shard.yml`.
- When pointing a shard at a GitHub repo without a published version tag, add `branch: master` to `shard.yml` so the resolver can find it.
- Local `path:` dependencies are for development only — always switch to `github:` before committing.

## Building and running

- `shards run --error-trace <target>` — compile and run a target listed in `shard.yml` in one step.
- `crystal tool format` — format all Crystal files in the project.
- `crystal spec spec/path/to/test_spec.cr:LINE_NUMBER --error-trace` — run a specific test with error traces.

## Testing patterns

- Tests use Minitest, not Crystal's built-in `spec` framework.
- To test private methods, add a public proxy method on the class that delegates to the private one (see existing specs for examples).
- Test files live in `spec/` mirroring the `src/` directory structure.
