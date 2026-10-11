---
name: survey-remote-repo-layout
description: "Use when asked to use real data from a repo too large to clone or check out (SVN/Perforce/git): capture its layout as a committed manifest, or validate indexing or grouping rules on real paths without file contents."
---

# Survey a repository too large to clone

When someone says *"use real data from `<repo-url>`, we can't clone it"*, the answer is
almost never a partial checkout. Metadata listings return everything a catalogue/indexer
derives — path, size, revision, author, timestamp — in one request, for free.

## 1. Confirm reach and scale first

```bash
svn info <url>            # revision, UUID, last author
svn ls <url>              # top level only — find the real root
```

Do **not** recurse until you know the top-level shape. The art/source root is often
several levels down (`trunk/source`), and siblings (`trunk/intermediate`) are cooked
output you must exclude.

## 2. One recursive metadata call

```bash
svn ls -R --xml <url>     # path + size + commit{revision,author,date} per entry
git ls-tree -r -l HEAD    # git equivalent (no author; use git log --name-only if needed)
p4 files //depot/...      # perforce
```

Budget: ~90s and ~16 MB XML for ~50k files. Nothing is fetched.

## 3. The encoding trap — this WILL bite on Windows

PowerShell decodes a child process's stdout with `[Console]::OutputEncoding` (OEM 437),
not UTF-8. Non-ASCII paths become mojibake (`César` → `C├⌐sar`) while the command
**exits zero and reports the correct file count**. Nothing downstream notices.

Fix: redirect to a file and let the XML parser honour the declaration.

```powershell
$tmp = [System.IO.Path]::GetTempFileName()
Start-Process svn -Wait -NoNewWindow -PassThru `
  -ArgumentList @("ls","--recursive","--xml","--revision",$Rev,$Url) `
  -RedirectStandardOutput $tmp
$xml = New-Object System.Xml.XmlDocument
$xml.Load($tmp)
```

Always verify the capture against an independent parse (Python `xml.etree`) before
trusting the script. Compare line-by-line, not counts — counts matched while 233 paths
were corrupt.

## 4. Manifest format

Tab-separated, sorted by path (ordinal), gzipped, UTF-8 no BOM:

```
path <TAB> size <TAB> revision <TAB> author <TAB> 2026-09-08T09:26:35Z
```

Validate TSV is safe first: check no path contains a tab or newline. ~7.7 MB of text
gzips to ~0.6 MB — small enough to commit, which is the whole point: real-scale tests
then run in CI instead of skipping outside one machine.

Loader must **throw on a short row**, never skip. A manifest that silently drops rows
gives a catalogue short by an unknown amount, indistinguishable from a smaller repo.

## 5. Feed it through the existing seam

Find the interface the indexer already enumerates through. Usually a test fake already
accepts a list — reuse it rather than writing a second client.

```csharp
public static ILoreClient ClientFor(string path) => new FakeLoreClient(Load(path));
```

Add an explicit config option (`Indexer:ManifestPath`), not magic path-sniffing. Validate
its existence in the host's **options validation**, not in a runtime pre-flight check —
DI resolves the client before any startup check runs, so a missing file throws a stack
trace several frames before your friendly message.

Say plainly what a layout cannot do: no file contents, so dependency scanning, hashing,
locking and restore are all empty.

## 6. Run it — do not model it

Model in Python to explore; **prove with the real binary against a real database**. The
gaps are large and instructive. Guard against these:

- **Config override.** A settings row in the DB may silently override env vars. Check the
  target/settings table before believing your `RootPrefix` took effect.
- **Use a throwaway database.** Crawling into the shared dev DB mutates it — main-branch
  crawls *delete* assets not seen. Create a fresh DB, migrate with whichever service owns
  migrations, then crawl. If you do pollute one, repair by re-crawling the original
  source and diff **paths**, not counts.
- **Verify in the UI**, not just SQL. Category counts in the sidebar are the cheapest
  end-to-end proof.

## 7. Expect the rules to be wrong

Rules derived from *cooked/exported* output rarely survive contact with *authored source*:

| Cooked tree | Source tree |
|---|---|
| `.dae`, `.fbx` | `.mb`, `.ma`, `.spp`, `.sbs`, `.psd` |
| filed by asset | filed by craft (`models/`, `painter/`, `textures/`) |
| variants encoded in filenames | one authoring master; variants generated downstream |

**A healthy-looking collapse ratio does not mean the rules matched.** Supporting-file
attachment inflates files-per-entry independently of grouping. Read the entry count and
the per-category breakdown too.

Depth varies *twice*: the craft folder sits at different depths per category, and below it
a subcategory may precede the asset. The rule that survives both:

> The asset is the **deepest folder below the craft that is not itself a craft name**;
> no folder at all means the file is the asset.

Taking the shallowest collapses unrelated assets together; taking the literal deepest
splits an asset's own `resources/` folder off from it.

## 8. Honesty checks before finishing

- Every name in a hand-written vocabulary list (craft folders, exclusions) must be
  **counted in the capture**. A zero-occurrence entry is wrong with no symptom whatsoever.
  Put the counts in the comment so they can be re-audited.
- Pin the capture in tests: exact row count, column order via one known row, and the
  non-ASCII round-trip.
- Pre-existing test failures: prove with `git worktree add /tmp/baseline HEAD` and rerun
  there. Never write them off from diff scope alone.
- Committing real employee names and unreleased-title layouts is a data-sensitivity call —
  **surface it to the user**, don't decide silently.
