---
name: local-docs-lookup
description: Ground agent answers in local library documentation (pydoc, go doc, vendored READMEs, help() in REPLs) rather than routing queries through a third-party.
---

# Local Documentation Lookup

Ground agent answers in locally-available documentation before considering any external lookup service. Under the MCP Registry Policy in `AGENTS.md`, documentation-lookup-as-service MCPs route library names and query text to a third party - this skill is the policy-compliant replacement.

## When to Use This Skill

Use this skill when:

- The agent needs API / library details to answer a question correctly.
- The user asks "how do I use X in library Y?" or "what's the signature of foo?"
- You notice the agent hallucinating API calls, method names, or argument orderings.
- A failing test or stack trace references a library function whose real signature the agent should verify rather than guess.

**When NOT to use**:

- The question is about the user's own code - use direct file reads or `devai-code-search` instead.
- The question is about a runtime error in the user's code - use `bug-localization` or `error-explanation-generator`.
- The documentation you need is genuinely online-only and the user has explicitly approved fetching a specific public URL - fetch it via `devai-web-fetch` with the one URL (policy-compliant per the decision tree in `AGENTS.md`).

## Instructions

Walk this lookup sequence **in order** and stop at the first source that answers the question.

### Step 1: Introspect the installed package

Python, Ruby, Node, Go all ship REPL introspection. Use it first.

```bash
# Python
python -c "import requests; help(requests.get)"
python -m pydoc requests.get
python -c "import inspect, requests; print(inspect.signature(requests.get))"

# Node (REPL)
node -e "console.log(require.resolve('axios'))"
# Then Read the resolved path's README / index.d.ts

# Go (from a module directory)
go doc encoding/json.Marshal
go doc -all encoding/json.Marshaler

# Ruby (irb)
ruby -rjson -e "puts JSON.method(:parse).source_location"
```

This is the highest-fidelity source because the docstring / signature comes from the exact version installed.

### Step 2: Read the vendored package README

Every installed package ships its README on disk.

```bash
# Python
find "$(python -c 'import sys; print(sys.prefix)')"/lib/*/site-packages/<package-name> -name "README*" -print

# Node
ls node_modules/<package>/README*

# Ruby
gem contents <gem-name> | grep -i readme
```

Read the README with the `Read` tool. This usually answers "what does this library do and how do I use its main entry points."

### Step 3: Read the package's shipped .md / .txt / .rst docs

Many packages ship a `docs/` directory, a `CHANGELOG.md`, or inline code comments that contain usage examples.

```bash
# Python
ls "$(python -c 'import sys; print(sys.prefix)')"/lib/*/site-packages/<package>/docs 2>/dev/null
find "$(python -c 'import sys; print(sys.prefix)')"/lib/*/site-packages/<package> -name "*.md" -maxdepth 3

# Node
find node_modules/<package> -name "*.md" -maxdepth 3
```

### Step 4: Read the package's type stubs or source

TypeScript `.d.ts` files, Python type stubs (`*.pyi`), and plain source are authoritative for signatures.

```bash
# Node / TypeScript
cat node_modules/<package>/dist/index.d.ts
cat node_modules/<package>/dist/<submodule>.d.ts

# Python - go straight to the source
python -c "import <package>; print(<package>.__file__)"
# Then Read the printed path.
```

### Step 5: Check the project's own shipped docs

Many well-organized projects ship a `docs/` tree in their own repo at `<repo-root>/docs/` with guides, ADRs, and references. Always grep this tree before reaching for external sources.

```bash
find docs/ -name "*.md" -print
grep -r "<symbol-or-phrase>" docs/
```

### Step 6: Local man pages

For CLI tools and system libraries:

```bash
man <command>
<command> --help
```

### Step 7 (last resort, with user approval): `devai-web-fetch` a single URL

If the prior steps did not answer the question AND the official documentation is online, ask the user:

> "The information is not in any local source I can find. Would you like me to fetch the official docs page at `<URL>` via `devai-web-fetch`? This makes one outbound HTTPS call to the URL you approve; no third-party intermediary is involved."

If the user approves, call `devai-web-fetch` with the single URL. Do not perform follow-up fetches without re-asking.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "grep-ing the repo is slower than just asking the MCP" | The initial lookup via pydoc / README is 5-10 seconds. The ongoing cost of the MCP is every query leaking library names, plus a new dependency on an external service's uptime. |
| "The MCP has more up-to-date docs than what's installed locally" | Your code runs against the installed version - that's the version whose docs actually matter. An MCP returning the bleeding-edge docs may describe features that don't exist in your installed version, which is worse than nothing. |
| "I don't know where the package is installed" | `python -c "import X; print(X.__file__)"` or `node -e "console.log(require.resolve('X'))"` solves this in one line. Take the one line. |
| "The package has no README" | If a package ships with no README and no source comments, its maintainability is the real problem. Do not paper over that with a remote lookup - flag the package for replacement. |

## Verification

- [ ] The answer cites at least one local source (file path or introspection command output).
- [ ] If `devai-web-fetch` was used, the user explicitly approved the URL.
- [ ] The answer matches the installed version of the package (not a newer API the user does not have).
- [ ] No documentation-as-service MCP was invoked.
- [ ] Library names and query text did not leave the local machine except to the user-approved URL (if any).

## Related Skills

- `rag-implementation` - general RAG over arbitrary document corpora; this skill is the specialized flow for library documentation.
- `context-manager` - for shaping what context the agent loads; feed local doc extracts via this skill.
- `code-semantic-search` - for searching the user's own code (not library docs).
- `error-explanation-generator` - when the library question is triggered by a specific runtime error.

## Notes on the Gap

This skill covers **cached / installed-version** documentation. It does NOT recreate a continuously-updated library index such as a search-engine-style lookup over every package version on PyPI / npm / crates.io. That gap is real; under the MCP Registry Policy, closing it requires either (a) running a local mirror of the documentation corpus, which is large and infrequently needed, or (b) accepting the single-URL user-approved fetch via `devai-web-fetch` for the rare case where the locally-installed version is genuinely insufficient. Document both as a known limitation rather than papering over it with a third-party service.
