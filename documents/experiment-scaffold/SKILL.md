---
name: experiment-scaffold
description: "Create a new experiment workspace directory: initialize git, write an AGENTS.md goal doc, and create references/ with index.md + notes/links markdown plus local repo copies under references/repos (gitignored). Prefer canonical GRM clones when available, otherwise seed from a shared experiment cache. Use when the user asks to spin up a scratch/research/experiment folder and provides repos, links, and/or notes to collect."
---

# Experiment Scaffold

Create a workspace for a scratch, research, or experiment project when the user
provides a name and goal, with any repos, URLs, or notes they want collected.

## 1. Gather the inputs

Collect:

- A directory name that is one path segment, with no `/`.
- A one to three sentence goal describing what the user wants to learn, build,
  or test.
- Zero or more GitHub repos, as `owner/repo` or a URL.
- Optional sparse-checkout paths for large repos, using `repo=path[,path...]`.
- Zero or more reference URLs and notes.
- An optional parent directory. Use the current directory when none is given.

## 2. Create the workspace

Run the sibling helper `scripts/create_experiment.py` with the gathered inputs.
For example:

```bash
python3 scripts/create_experiment.py \
  --root ~/experiments \
  --name vector-search \
  --goal "Evaluate hybrid search with embeddings vs BM25." \
  --repo langchain-ai/langchain \
  --repo-sparse langchain-ai/langchain=libs/langchain,cookbook \
  --repo facebookresearch/faiss \
  --url https://python.langchain.com/docs/concepts/retrievers/ \
  --note "Measure latency/recall across configs"
```

The helper creates:

- `<root>/<name>/.gitignore`, which ignores `references/repos/`.
- `<root>/<name>/AGENTS.md`, with the goal and a pointer to `references/index.md`.
- `references/index.md`, an inventory with repository clone status.
- `references/notes.md` and `references/links.md`.
- `references/repos/<owner>/<repo>` copies for repositories that can be cloned.

## 3. Fetch linked articles when URLs were supplied

The helper records URLs in `references/links.md`. After it finishes, save each
URL as clean, complete Markdown in `references/articles/`:

1. Create `references/articles/`.
2. Fetch each URL with the available native web-fetch or browsing tool. Preserve
   headings, code snippets, and technical details; include the title, author,
   and date when available. For GitHub issue or pull request URLs, use `gh issue
   view` or `gh pr view` through Bash.
3. Write each result to a descriptive filename such as
   `wkwebview-headless-mode-devto.md`, with this frontmatter:

   ```yaml
   ---
   source_url: <original URL>
   fetched_date: <today's date>
   topic: <short topic label>
   ---
   ```

4. If a URL cannot be fetched because of an auth wall, timeout, or empty
   response, skip it and record the failure under `Fetch failures` in
   `references/index.md`.

Fetch URLs in parallel when the environment supports it; otherwise fetch them
sequentially.

## Repository cloning

The helper prefers a canonical GRM clone at
`~/code/github.com/<owner>/<repo>` when GRM is available. Otherwise it reuses a
shared cache at `~/code/experiments/reference-cache/<host>/<owner>/<repo>`,
cloning there on first use. It then creates the experiment-local copy under
`references/repos/` with `fastcp` when available, and normalizes it to a clean
default-branch checkout.

Sparse requests copy only the listed repo-relative paths. If a canonical or
cached source exists, the helper creates a sparse shared clone from it. Without
a source, it makes a direct sparse partial clone instead of filling the full
shared cache. Repositories that cannot be parsed as `owner/repo` or URL form
use a direct clone into `references/repos/`.

Cache population tries `gh repo clone` with SSH first, then falls back if SSH or
authentication fails. If cache population fails while using multiple GitHub
accounts, check `gh auth status` and switch accounts with
`gh auth switch -u <user>`. To make `gh` prefer SSH, run
`gh config set git_protocol ssh`.

## Helper options

Pass these options when the experiment needs them:

- `--depth N` creates a shallow clone. The default `0` keeps complete history.
- `--repo-sparse REPO=PATH[,PATH...]` limits one repo to listed paths. Repeat
  the option for additional paths or repos.
- `--no-clone` creates the structure without cloning repos.
- `--strict` stops at the first clone failure. By default, failures are recorded
  in `references/index.md` and processing continues.
- `--canonical-root PATH` overrides the canonical clone root.
- `--cache-root PATH` overrides the shared experiment cache root.
- `--grm-mode auto|on|off` controls whether canonical reuse requires GRM.
