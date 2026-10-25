---
name: remote-hosts
description: "Run commands or do file operations on a remote ssh host through the hermes-remote-tools plugin."
version: 1.1.1
author: Alaister LJ Leung
tags: [ssh, remote, cloud, terminal, files]
---

# Remote hosts via hermes-remote-tools

## When to use

Use this plugin's tools for anything that must run or read on a host other than the one Hermes runs on. The builtin terminal, read_file, write_file, patch and execute_code are host-local: a remote path given to them reads the wrong machine's filesystem or dies with a not-found error. The local machine is served by the builtins; every other configured host goes through the six remote tools.

The six tools:

- `terminal_remote` - shell on a configured remote host, with the same approval stack as the builtin terminal. `background=true` registers the process for notifications and standard process management.
- `read_remote_file` / `search_remote_files` - reads and regex/glob searches.
- `write_remote_file` / `patch_remote_file` - mutations, snapshotted before the edit (undoable) and verified by a read-back hash.
- `undo_remote_file` - restores the previous content of a file, one step at a time.

## Call shape

The tools are local deferred tools behind the tool_search bridge, so every parameter sits INSIDE the inner call's `arguments` object:

```
{"calls": [{"name": "terminal_remote", "arguments": {"target": "devbox", "command": "uname -a"}}]}
```

Both failure shapes are verified: omitting `target` from `arguments`, and placing `target` as a sibling of `arguments`. One entry per tool_call: batching two invocations is rejected outright, so a batched call returns nothing and wastes a round-trip. On a schema refusal, tool_describe the tool once, verify the shape, retry once, then report the blocker instead of looping.

## Configuration

Targets live in config.yaml under the plugin's settings:

```yaml
plugins:
  entries:
    hermes-remote-tools:
      settings:
        targets:
          devbox:
            host: 203.0.113.10
            user: alaister
            port: 22
            key: ~/.ssh/devbox
            cwd: "~"
```

A machine reachable on more than one network takes a list of addresses in `host`, tried in order, the first that connects wins; the pooled session is probed before every reuse, so a machine that moved networks re-dials automatically. Connection-relevant fields are fingerprinted, so a config edit rotates the pooled session on next use. Plugin code loads once per process: after a config edit restart the gateway (and the dashboard when desktop sessions use the plugin), then prove reachability with ONE live call. A green `hermes plugins doctor hermes-remote-tools` proves registration, not reachability.

## Execution semantics

- Remote commands run under `bash -c` even when the remote login shell is fish, csh or tcsh: the plugin probes `$SHELL` once per session and, on a non-POSIX login shell, base64-wraps the script through the command line so the login shell never parses it. Write POSIX/bash chains inside the script.
- `cd` inline (`cd ~/path && ...`), not through the workdir parameter: a failing `cd` short-circuits the chain, so nothing runs in the wrong directory.
- Results carry `failed: true` only on a nonzero exit; success omits the key.
- Keep `timeout` well under the background-promotion cap: an over-cap timeout promotes the command to a tracked background process.
- Never put secrets in a command string: the approval layer redacts credential-shaped substrings. Write any credential-touching script with `write_remote_file` and execute the written file.

## Verification discipline

- After every remote write, prove the bytes on the target: `ls -la <path>` plus `sha256sum` through `terminal_remote`. A write can report success and a matching read-back hash while landing on the wrong host or nowhere at all.
- `terminal_remote` is the ground truth for remote file state; cross-check any `read_remote_file` result against it before building on the read.
- Never use `scp`. Ship bytes through `write_remote_file` (new or whole-file rewrite, absolute path, never `~`) or the base64 heredoc through `terminal_remote`, which no shell on any hop parses. For a whole-file rewrite of an existing file, write `<path>.new`, `sha256sum` and `diff -u` it against the target, then `mv` only after the hash matches. `diff` exits 1 on differences, so `failed: true` on a successful diff is expected.
- Build patch payloads as a local file first with anchor assertions, then ship them: hand-inlining multi-line replacement text into a tool_call body trips the control-character schema check.

## Pitfall: never leave shell tracing on inside a remote command

`set -x` (or `bash -x`) in the command body poisons the pooled session's working directory. The env's per-command wrapper emits its CWD marker with `printf '<marker>%s<marker>' "$(pwd -P)"`, xtrace echoes that printf line, and the marker parser picks the traced FORMAT STRING (the `%s` sitting between two marker occurrences), so `self.cwd` becomes the literal `%s`. Every later call on that target then dies before the command runs: `bash: line 3: cd: %s: No such file or directory` with exit 126 from the wrapper's own `cd ... || exit 126`, and the file tools answer `working directory '%s' does not exist on the active terminal backend`. The real marker line survives in the output unstripped, which is the tell. A long `set -x` command also returns visibly mangled output for the same reason (the strip span eats the traced line and glues its neighbours).

Recovery needs no restart and no config edit: pass an explicit absolute `workdir` on the next call. It overrides the stored cwd (`effective_cwd = cwd or self.cwd`), so the command runs and the wrapper's trailing marker re-parses to the real path. Verified 2026-10-18 on ljair (macOS, git 2.54): poisoning reproduced on demand, one-call recovery after it.

Trace a nested shell instead (`bash -x ./script.sh`), and print debug lines plainly rather than turning on `set -x` in the remote command body.

## Classifying failures

Two layers, do not conflate: a wrapper refusal (`missing required argument(s): target`, or a batched call) is call-shape and fires before any shell sees the command; mangled output or a nonzero exit is execution (shell semantics or quoting). Classify before retrying anything.
