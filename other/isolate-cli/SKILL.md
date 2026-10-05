---
name: isolate-cli
description: "Run a third-party CLI as a subprocess without leaking into it or leaving state on the host, and prove both. Use when a script or skill shells out to an external tool, when a run must leave no trace outside the repository, when private input (a diff, a prompt, a credential) must not reach the tool's session log, when a policy or deny-list handed to the tool must actually be in force, when a claim about the tool's own behaviour (which paths it searches, which config file wins) must be settled against the shipped binary or bundle rather than its documentation, or before a measurement series whose runs must be comparable. Covers behaviour and state roots read out of the installed binary or bundle, a snapshot-diff-prune harness proven able to go red, and policy rules validated offline. Do NOT use to investigate an external system in general (that is research-it, which delegates here for artifacts on disk) or to judge whether a green result counts as evidence (that is prove-checks)."
metadata:
  author: Serghei Iakovlev
  version: "1.1"
  category: security
---

# Confine an External CLI

A CLI invoked as a subprocess is not a function call. It reads the operator's global configuration, writes per-run state under the home directory keyed to the directory it ran in, and treats a config file it cannot compile as advice rather than as an instruction. None of those three shows up in an exit code: the private content piped in lands in a plaintext log outside the repository, the host accumulates state nobody audits, and the confinement believed to be in force is absent.

This skill is the mechanics of running such a tool and being able to say afterwards what it read, what it wrote, and what it left behind. Whether the run's *result* is evidence is a separate question and belongs to `prove-checks`.

## Trigger

- A script or skill invokes a third-party CLI as a subprocess: an agent CLI, a linter with a cache, a package manager, a formatter, anything with a state store outside the working directory.
- A second tool or provider branch is added to a script that already does this.
- The tool is handed a policy, deny-list, allow-list or sandbox configuration.
- The content piped in is private: an unmerged diff, a prompt, a credential, customer data.
- A measurement or benchmark series will invoke the tool repeatedly and the runs have to be comparable to each other.

Not this skill: reading the tool's behavior to answer a general question, which is `research-it`, or deciding whether the green that came out counts as proof, which is `prove-checks`.

## Procedure

### 1. Read the state roots out of the installed artifact

The copy on disk is the one that runs. Release notes, the project README and the upstream default branch each describe a different one, and two versions of the same CLI commonly sit side by side under different runtime or package managers. Resolve and record the version and the real path before reading anything: `command -v tool`, then `readlink -f` on the result, then the package manifest or lockfile that installed it. This is `research-it`'s source-priority rule narrowed to a single copy on disk (OPTIONAL when the question widens past this run into how the tool behaves in general).

Resolve the artifact from the directory the run will happen in, not from the shell you are typing in. A version manager picks the interpreter by walking up from the current directory, so the same command name resolves to different installations depending on where it is invoked, and a wrapper that runs from a throwaway directory is answering a different question than your prompt is. Three separate investigations on one host each read the wrong copy this way before noticing; two of them noticed only from an unrelated stack trace. Print the resolved path from inside the run's own directory, record it beside the results, and when the reading turns out to have come from the wrong copy, re-verify every claim already made from it rather than assuming the versions agree.

Determining which credential channel a tool actually uses costs nothing if you point it at a proxy you control and read the hostnames it tries to reach. Different auth paths talk to different endpoints, so one intercepted connection attempt distinguishes them without spending a single call against the real service.

Where the authoritative behavior is readable depends on how the tool ships:

| Delivery shape | What is readable | How to enter it |
|---|---|---|
| Shim or wrapper script | The script and whatever it exec's | Follow the shebang or the exec line to the real entry point; `readlink -f` stops at a version-manager shim, so ask the manager from the run's directory |
| Loader or self-updater | An entry that spawns a platform package or a copy from its own versioned cache | Follow each spawn, read the copy it selects, and record that version rather than the manifest's |
| Interpreted package tree (site-packages, gems, node_modules, vendored sources) | Full sources, unminified | Grep the installed tree for a distinctive literal, then read the module that defines it |
| Single-file bundle (bundled JS, PEX, self-extracting archive) | Usually plain text; build banners with upstream file paths often survive | Locate the chunk with `grep -rlc`, then slice by byte offset, never by line |
| Split bundle (a directory of generated chunks beside one entry file) | The same as a single-file bundle, but only for the reachable subset | Resolve the import graph from the entry the package manifest names, then locate within that set only |
| Archive (JAR, WAR, wheel, container layer) | Contents after unpacking | Unpack first, then treat the result as one of the rows above; class files need `javap -c` or a decompiler |
| Statically linked binary (Go, Rust, C or C++) | Literals and embedded metadata only | `strings -n 6` for path fragments and marker names, `go version -m` for module metadata, then confirm by observation |

Two rules hold across all of them. Enter on a **distinctive literal** (a marker filename, an error string, a config key), never on a common word. And read the declaration that **owns** the paths, the single list the tool itself iterates, not a call site that happens to build one: a call site is a partial view that stays correct until the tool adds a root.

A third rule holds wherever the build emits more than one file: **a hit is not evidence the code runs**. A packager that splits its output writes many generated files into one directory and re-emits the same module into several of them, and only the ones reachable from the entry the manifest names are ever loaded. The unreachable copies carry the same literals as the live one, so a filename search cannot rank them and returns a dead copy as readily as the real one. Walk the static imports from the entry, keep the reachable set, and re-derive any citation that falls outside it. Measured once on a bundle of 72 generated files, 40 were reachable, and a search for one distinctive method name returned three files of which two never execute. Minifiers make this worse in a way that hides it: the live copy may hold a symbolic reference where a dead copy inlined the literal, so searching for the literal finds only the dead ones and the reachable set looks empty.

Never `grep`, `grep -o` or `sed -n` on a bundle to read a match. A single line can be a megabyte wide and one hit floods the context. Slice around the match instead:

```python
import re, sys
data = open(sys.argv[1], encoding="utf-8", errors="replace").read()
for m in list(re.finditer(sys.argv[2], data))[:3]:
    print(data[max(0, m.start() - 400) : m.end() + 800])
```

**When the artifact yields nothing** (a stripped binary, an encrypted bundle), derive the roots by observation instead: point `HOME` and the XDG base-directory variables at a scratch tree, run the tool once, and list what appeared; where available, trace file-creating syscalls (`strace -f -e trace=file`, `dtruss`, `fs_usage`). An observed set is a lower bound for one input on one platform, not the tool's list, so keep the harness in step 2 watching whole directories rather than a set of named paths, and re-derive it after every upgrade.

### 2. Snapshot, then prove the snapshot can go red

Take the baseline before the first run: a sorted listing of every root, plus a hash of any registry or index file the tool maintains. Keep it outside the repository and outside the tool's own roots.

Then plant a decoy, an empty entry of the right shape inside a root, and re-run the diff. If the decoy does not appear, the detector is blind and every clean diff afterwards means nothing. Remove the decoy and confirm the diff goes quiet again.

Only then: run, diff, prune, diff again. The second diff must be empty.

This is `prove-checks`'s negative control aimed at the audit instrument rather than at the check (REQUIRED reading when the run's own result will also be reported as evidence), and that skill's ordering rule carries over intact: any control asserting the *absence* of something runs before the run that would create it.

### 3. Attribute entries by content, never by name

The tool derives its entry name from the working directory through a transform it owns (lowercasing, slugging, hashing, a numeric suffix on collision), so a name reconstructed from the path will miss. Worse, every other entry in those roots belongs to somebody else's session, possibly one running concurrently.

Read the marker file *inside* each candidate, compare it to the path this run used, and delete only exact matches. Never sweep a whole state root. Giving the run its own throwaway working directory makes that marker unique and keeps private input out of any real project's history.

Leave alone anything shared and rewritten in place, such as a registry keyed by path or a global index: a read-modify-write against a file every concurrent process also writes trades litter for a lost update. Record that omission as a decision in a comment, or the next reader will "fix" it.

### 4. Run the tool's own validator offline before spending a live call

Confinement has two halves: what the tool may reach, and what it may keep. The policy decides the first, so enumerate the reachable surfaces before writing a rule - the directory the tool runs in, the operator's global configuration, and every plugin, extension or MCP server still enabled in a headless run, which loads whether or not it is ever called and, for a model-driven tool, puts its own instructions into the context.

A configuration the tool cannot compile is frequently dropped, noted on stderr, and ignored. The run continues under whatever rules survived and still exits 0, so the rule believed to be providing the confinement is simply absent while the run looks like a success.

- Get the acceptance predicate from the artifact when step 1 could read it (the schema, the parser, the safety check on each rule) together with whatever produces its input, such as the argument serializer or the path normalizer. Copy it; do not reimplement it from its observed behavior. When the artifact is unreadable, use the tool's own validate, lint or dry-run subcommand offline, and failing that, a probe run whose only job is to confirm the rule fires.
- Build two tables: inputs the rule must catch, and legitimate inputs it must not. Write the attack table in the spelling the rule actually sees. A pattern matched against serialized arguments is applied *before* the tool percent-decodes, expands a glob, resolves a relative traversal, or expands `~` and environment variables, so those spellings, plus case variants and alternate home roots, all reach the rule unchanged.
- Iterate offline until a candidate passes both tables. Only then spend a live run, and confirm there that the rule is in force by attempting the denied action with a sentinel that is fresh for this run.
- Keep the stderr check in the wrapper regardless: treat the tool's own "rule dropped", "config error" or "falling back to defaults" line as a hard failure of the run, never as a warning.
- Anchor that check to the tool's own diagnostics, not to the whole stream. For an agentic CLI the second stream carries the transcript, so text the tool merely read and echoed will trip a substring match: a guard scanning everything once fired on a sentence of prose out of the repository under review. Match on the tool's diagnostic prefix, or read its structured log, and prove the guard still fires by feeding it a genuinely broken configuration.

### 5. Give every run its own state root, and know what that buys and costs

`HOME` alone is not a state root. An XDG-aware tool prefers `XDG_CONFIG_HOME`, `XDG_DATA_HOME`, `XDG_STATE_HOME`, and `XDG_CACHE_HOME` when they are exported, so a run under a swapped `HOME` still writes to the operator's real directories. Point all four into the root, keep the real roots in the step 2 snapshot so a leak reaches the diff, and re-resolve the version afterward: moving the cache can change which copy a self-updater runs.

The throwaway root that keeps a run from leaving state behind is also what makes a series comparable, and the mechanism is worth stating because it is easy to optimise away. A per-run directory changes the absolute paths the tool stamps into the front of its own request - the working directory, its temporary directory - and a prefix that never repeats defeats any implicit prompt cache the provider runs. Runs in the series are therefore independent of each other by construction rather than by discipline: verify it by reading the provider's own per-request accounting and confirming the cached-token count on the first request of every run is zero.

The price of that independence is the entire first request, every run, at full rate. Measure it once against a deliberately fixed root to learn what the cache would have saved, then keep the per-run root anyway: a series whose runs warm each other is not a series, it is one run reported several times. Publish the spread rather than an average when the cost is driven by how many turns the tool decides to take, because that distribution has no useful mean.

### 6. Pin what the run inherits, and fail loudly when it moves

A throwaway state root closes the outbound direction only. Inbound is still wide open: the credential, the account selection, the default model and the endpoint are read out of a file in the operator's home that any deploy, any parallel session and any configuration sync may rewrite between one run and the next. A series whose runs disagree about which account they used is not a series, and the disagreement is invisible because nothing errors.

Derive each inherited value from an artifact rather than copying the operator's current choice: the format of a credential store states which authentication type it can serve, so the store on disk answers the question that the settings file only records an opinion about. Where a value cannot be derived, assert it at the start of the run with both the expected and the found value in the failure message, and record every inherited value beside the results. A wrapper that copies the operator's selection inherits their next mistake.

Supplying a credential to a confined run reopens the outbound direction unless the credential is copied rather than shared. Pointing the run at the operator's real credential store makes that store writable: the tool refreshes a rotating token, rewrites the selected account, or appends to a usage ledger, and the one file worth protecting is the one the throwaway root never covered. Copy the minimum the authentication type needs into the run's own root, assert it arrived before spending anything, and destroy the copy with the root. The copy is an artifact too, so scrub the session store and any export taken from it before a figure read out of them leaves the machine.

### 7. Reconcile against the baseline and publish the counts

At the end, re-diff every root against the opening snapshot and state the numbers. "root A: 41 entries before, 41 after; root B: 12 before, 12 after; index hash unchanged" is a report; "cleanup ran" is not. Anything deliberately left behind is named and justified in the same breath.

## Worked example

One tool, one version, as an illustration of the shape above, worked through Gemini CLI 0.40.x on Linux: see [references/worked-example.md](references/worked-example.md).

## Validation

- [ ] The state roots came from a list read in the installed artifact, or from an observation run whose limits are recorded, and the resolved version and path were recorded alongside them.
- [ ] The decoy made the diff go red before any measured run.
- [ ] Every deletion matched a marker read from inside the entry, not a name derived from the path.
- [ ] The run had its own disposable working directory, and the private input reached no store that outlives it.
- [ ] Each policy rule passed the tool's own validator offline, and the wrapper fails the run on the tool's rule-dropped output.
- [ ] The closing diff against the opening snapshot is empty, or every remaining difference is named and explained.

## Anti-patterns

- **Taking the state paths from the documentation.** Docs describe the version their author had. The artifact on disk describes the version that will run tonight.
- **Grepping a bundle for content.** One match prints one megabyte-wide line. Locate with `grep -rlc`, read with a byte-offset slice.
- **Citing a generated file without proving the entry reaches it.** Duplicate copies of one module across split output are near-identical and a filename search cannot rank them, so a citation can describe code the tool never loads and nothing in the output says so.
- **Reconstructing the entry name from the working directory.** The tool's own transform owns that name; guessing it deletes somebody else's session, or nothing at all.
- **Sweeping the whole state directory.** Every entry that is not this run's belongs to another operator, another project, or a process running right now.
- **Reading a stderr note as noise.** "Policy file error", "rule ignored" or "falling back to defaults" alongside exit 0 is the tool announcing that the confinement is off.
- **Measuring before the harness is proven.** A snapshot diff that has never gone red reports "no change" for a blind detector and for a clean host identically.
