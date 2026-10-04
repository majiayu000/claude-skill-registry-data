---
name: replication-package
description: Assemble a journal-ready replication archive for a quantitative-marketing paper, scanning for secrets, PII, and absolute local paths before the zip is built. TRIGGER on "/replication-package", "build a replication package", "data availability statement", "zip up the code and data for submission", a data-editor email asking what to send, or any "gather everything a replicator would need" request.
---

# Replication package

Build one sanitized zip a data editor can accept without follow-up. The archive is assembled from files that already exist. Nothing here re-runs the analysis or verifies that the numbers in the paper match the code; if that is what the user wants, say so and stop.

## Discovery (no config file)

Everything is resolved at runtime. There is no setup step and no state file to create.

| Value | How to get it |
| --- | --- |
| Local username | `whoami` |
| Paths to redact | `$HOME`, `/Users/$(whoami)/`, every `$HOME/Library/CloudStorage/Dropbox*/` mount (enumerate them with `ls -d "$HOME/Library/CloudStorage/"Dropbox*` rather than assuming a name), plus any cluster paths found in the code (`/gpfs/...`, `/home/<user>/`) |
| Author name, email | `git config user.name` / `git config user.email` inside the code repo, then `--global`. If both are empty, parse `\author{}` and `\thanks{}` from the main `.tex`. Ask only if still unknown. |
| Affiliation | Parse `\affiliation{}` / `\institute{}` / `\thanks{}` from the main `.tex`. Ask once, and only when actually writing the README author block. |
| Paper root | The path argument if given, else `ls -d "$HOME/Library/CloudStorage/Dropbox*/Apps/Overleaf"/*/` and ask the user to pick. |
| Code root | An argument, or ask. Never guessed from the paper root, which does not contain code. |
| Archive destination | An argument, or ask. Never defaulted. See "Staging and archive destination". |
| Paper slug | Directory name lowercased, spaces and punctuation to hyphens (`Algorithmic Pricing Manuscript` becomes `algorithmic-pricing-manuscript`). Confirm it with the user in the report. |

Batch whatever still has to be asked into one message instead of interrogating the user step by step. Never block on a value that only affects a cosmetic README field; write `[FILL IN]` and flag it. The two questions that do block are the code root and the archive destination.

PDFs turn up here as preregistrations, IRB approvals, and pasted data-editor letters. The Read tool cannot open them on this machine, since it needs `pdftoppm` (this setup assumes no Homebrew and no poppler; adjust to yours). Route every PDF through the helper:

```bash
~/.claude/assets/bin/pdfread.py text prereg.pdf
~/.claude/assets/bin/pdfread.py text prereg.pdf --pages 1-5
~/.claude/assets/bin/pdfread.py png prereg.pdf --pages 1 --dpi 150 --out /tmp/p   # then Read /tmp/p-1.png
```

Never call `pdftotext` or `pdftoppm`; neither is installed.

## Two roots, both given as input

A package needs two directories, and in this setup they are normally in different places.

Paper root is an Overleaf project, normally under `$HOME/Library/CloudStorage/Dropbox*/Apps/Overleaf/<project>/`, holding `main*.tex`, `.bib`, `Tables/`, and `Figures/`. These projects are for academic writing, so a paper root with nothing but `.tex`, `.bib`, and exhibit assets is the expected case and needs no comment. Read it for the exhibit list, the title, the abstract, and the author block; never copy the manuscript into the archive.

Code root is wherever the analysis lives, which is somewhere else entirely: a local git repo, a research folder elsewhere in Dropbox, or a directory on the HPC grid. It is a separate input: take it from the arguments when given, otherwise ask for it in the batched question message and wait for the answer.

The one genuine blocker is code that lives on an HPC cluster (`/gpfs/...`, `/home/<user>/`) and has not been synced down. Confirm the given path really exists locally before believing it:

```bash
if [ ! -d "$CODE_ROOT" ]; then
  echo "STOP: code root $CODE_ROOT is not present locally"
  case "$CODE_ROOT" in
    /gpfs/*|/home/*) echo "This looks like an HPC cluster path. Sync it down first, then rerun." ;;
  esac
  exit 1
fi
```

Never build an archive from a half-present tree. It looks complete in the manifest and breaks on the first file a replicator opens.

## Staging and archive destination

Stage under `$TMPDIR`. Every copy, rewrite, and check happens there, so a half-built package never appears in a synced folder.

The destination for the finished zip is the user's to name. Treat it as a required input with no default. Take it from the arguments if given. Otherwise ask once, before any copying starts, in the same batched message as the other open questions: where should the finished archive be written? State plainly that the location will not be guessed and that nothing gets written until there is an answer. It is usually a Dropbox folder the user keeps for this purpose, separate from the Overleaf project.

Hard rule: the archive is never written anywhere under `~/Library/CloudStorage/Dropbox*/Apps/Overleaf/` (equivalently `$HOME/Library/CloudStorage/Dropbox*/Apps/Overleaf/`). Those folders sync to Overleaf, so a large archive left there gets pushed into the manuscript project. Refuse the path, say why, and ask for another one. Staging follows the same rule.

Dropbox on this machine is mounted per account under `$HOME/Library/CloudStorage/`, with names like `Dropbox-Personal` and `Dropbox-YourUniversity`. In this layout there is no `$HOME/Dropbox` symlink, and the mount names change whenever an account is added or removed, so never hard-code one. Match the family with the glob `*/Dropbox*/`, and test the logical path, the physical path, and the string the user typed, since any one of them alone can let an Overleaf folder through:

```bash
case "$DEST/" in
  */Dropbox*/Apps/Overleaf/*) echo "REFUSE: $DEST syncs to Overleaf. Name another folder."; exit 1 ;;
esac
mkdir -p "$DEST" || { echo "STOP: cannot create $DEST"; exit 1; }
DEST_ABS=$(cd "$DEST" && pwd -P) || { echo "STOP: $DEST is not enterable"; exit 1; }
DEST_LOG=$(cd "$DEST" && pwd -L)
for d in "$DEST_LOG" "$DEST_ABS"; do
  case "$d/" in
    */Dropbox*/Apps/Overleaf/*) echo "REFUSE: $d syncs to Overleaf. Name another folder."; exit 1 ;;
  esac
done
[ -w "$DEST_ABS" ] || { echo "STOP: $DEST_ABS is not writable"; exit 1; }
```

The string the user typed is checked before the `mkdir -p`, so an Overleaf destination is refused before any directory gets created inside a synced folder; the logical and physical forms are checked once the path resolves.

Because the destination is very likely inside some other Dropbox folder, the archive starts uploading the moment it lands. Say this in the report. For a multi-gigabyte package, suggest pausing syncing while the file is written, or writing it to a folder excluded from selective sync. A long Dropbox upload is wasted work when the file is going to a journal.

## Layout

Stage `<slug>_replication_<YYYYMMDD>/` and zip that single directory. This layout is a superset that clears all four target journals.

```
<slug>_replication_<YYYYMMDD>/
├── README.md              # structured per the template below
├── code/                  # 00_master.R, 01_clean.R, 02_analysis.R, ...
├── data/
│   ├── raw/               # as obtained, or a pointer file if it cannot ship
│   ├── analysis/          # the cleaned data the estimation actually reads
│   └── dictionaries/      # one codebook per dataset, shipped or not
├── materials/             # Qualtrics .qsf, stimuli, instructions, preregistration
├── output/
│   ├── tables/
│   └── figures/
├── logs/                  # console logs from the cleaning run and the analysis run
└── meta/
    ├── exhibit_map.md     # table/figure -> script -> line -> output file
    ├── manifest.json      # every file with size and sha256
    ├── git_hash.txt
    └── checklist.md
```

Per-study subfolders under `code/` and `materials/` when the paper has numbered studies. JMR asks for study-level organization explicitly.

## Workflow

### 1. Inventory

- Code: glob `.R`, `.Rmd`, `.py`, `.ipynb`, `.do`, `.jl`. Sort by run order from numeric filename prefixes, else infer from `source()` / `import` / `%run` dependencies and note the guess in the README. Flag a missing master script; Management Science requires one.
- Data: glob `.csv`, `.rds`, `.RData`, `.parquet`, `.dta`, `.feather`, `.h5`, `.npz`, `.sav` under the code root. Record per-file and total size. Read every CSV header for the dictionary stub.
- Exhibits: everything under the paper root's `Tables/`, `Figures/`, `output/`.
- Materials: `.qsf`, `.crdf`, stimulus images, experimenter instructions, preregistration PDFs, IRB approval. All four journals want the instruments as participants saw them. Read any PDF with `pdfread.py`, not the Read tool.
- Bibliography: copy `*.bib` to `meta/`. Do not copy the manuscript `.tex`.

### 2. Exhibit map

The deliverable journals ask for most, and the one authors most often ship broken. Produce `meta/exhibit_map.md` as a real table.

Exhibits as printed: parse every `table`/`figure` float in the main `.tex` for its `\label`, `\caption`, and the asset it pulls in (`\input{Tables/X.tex}`, `\includegraphics{Figures/Y.png}`). Take the printed number from the `.aux` file when one exists, since `\newlabel{fig:x}{{3a}{7}}` gives number `3a` on page 7 and beats counting float order. Otherwise count order of appearance and mark the numbers inferred. Number the appendix separately (`Table A2`).

Producing script: for each asset filename, grep the code root for the output path, recording file and line. Catch the write calls that appear in marketing code: `ggsave`, `pdf(`, `png(`, `dev.copy`, `write.csv`, `fwrite`, `writeLines`, `cat(..., file=)`, `stargazer`, `texreg`, `modelsummary`, `kableExtra::save_kable`, `xtable`, `plt.savefig`, `fig.savefig`, `to_latex`, `esttab`, `estout`, `outreg2`.

Gaps: every exhibit with no producing script is a finding, as is every script writing an output the paper never uses. List both.

Emit the column set from the Social Science Data Editors template ("List of tables and programs"), a superset of what any of the four journals asks for:

| Figure/Table # | Program | Line | Output file | Note |
| --- | --- | --- | --- | --- |
| Table 3 | `code/03_estimate.R` | 214 | `output/tables/main_results.tex` | runs after `02_clean.R` |
| Figure 2 | `code/04_figures.py` | 88 | `output/figures/fig2_elasticity.pdf` | |
| Table A4 | UNMAPPED | | `output/tables/robust_iv.tex` | no writer found, confirm with user |

Copy the same table into the README under "List of tables and programs".

### 3. Safety scan (before anything is copied)

The scan is the reason to use this skill instead of zipping by hand. Run it over the whole code root plus every text-like data file. Report file and line for every hit. Do not auto-strip secrets: false positives like `api_key = Sys.getenv("KEY")` are common, and silent rewrites of the user's code are worse than a noisy report.

#### Secrets and credentials

Structural token patterns (Python `re`, applied line by line):

```
AWS access key ID     \bAKIA[0-9A-Z]{16}\b
AWS secret            (?i)aws_secret_access_key\s*[:=]\s*['"]?[A-Za-z0-9/+=]{40}
GitHub PAT classic    \bgh[pousr]_[A-Za-z0-9]{36}\b
GitHub PAT fine-grain \bgithub_pat_[A-Za-z0-9_]{82}\b
Anthropic             sk-ant-(?:api|oat|ort)[0-9]{0,2}-[A-Za-z0-9_-]{20,}
OpenAI                \bsk-(?:proj-)?[A-Za-z0-9_-]{32,}\b
Hugging Face          \bhf_[A-Za-z0-9]{34,}\b
Google API key        \bAIza[0-9A-Za-z_-]{35}\b
Slack                 \bxox[baprs]-[A-Za-z0-9-]{10,}\b
Notion                \b(?:ntn_|secret_)[A-Za-z0-9]{40,}\b
Private key block     -----BEGIN (?:RSA |EC |OPENSSH |PGP )?PRIVATE KEY-----
DB connection string  (?i)(?:postgres(?:ql)?|mysql|mongodb(?:\+srv)?)://[^\s'"]+:[^\s'"]+@
Generic assignment    (?i)(api[-_ ]?key|secret|token|passwd|password|bearer|access[-_]?key)\s*[:=]\s*['"][^'"]{8,}['"]
High-entropy blob     \b[0-9a-f]{32,}\b  and  \b[A-Za-z0-9+/]{40,}={0,2}\b     (noisy, report low confidence)
```

Credential files never enter the archive, match or no match: `.env`, `.env.*`, `.Renviron`, `.Rprofile`, `.netrc`, `.pgpass`, `.aws/credentials`, `kaggle.json`, `*service-account*.json`, `credentials.json`, `token.json`, `id_rsa*`, `*.pem`, `*.p12`, `.Rhistory`, `.bash_history`, `.ipynb_checkpoints/`. Exclude and list them.

Marketing-specific credential names to grep by name: `wrds_user`, `wrds_pass`, `Sys.setenv(WRDS_`, `X-API-TOKEN`, Qualtrics datacenter IDs.

A hardcoded live credential stops the run. Show the file and line, and ask whether to replace it with an environment-variable read, keep it (the user confirms it is a public test key), or abort.

#### Personal data

Shape-based patterns, run over every text-like file:

```
Email                 [\w.+-]+@[\w-]+\.[\w.-]+          (skip the author's own addresses)
US phone              \b\d{3}[-.\s]\d{3}[-.\s]\d{4}\b
SSN shape             \b\d{3}-\d{2}-\d{4}\b
MTurk worker ID       \bA[A-Z0-9]{12,14}\b
Prolific PID          \b[a-f0-9]{24}\b
IP address            \b(?:\d{1,3}\.){3}\d{1,3}\b
Qualtrics response ID \bR_[A-Za-z0-9]{15,17}\b
```

The Prolific PID pattern matches any 24-hex string, so a Mongo ObjectId or a truncated hash hits
it too; report these with the count and the column name and let the user judge, as with `ipv4`
and `phone`.

### 3a. Survey platform data (Qualtrics, MTurk, Prolific, CloudResearch, LUCID/Cint)

For a user who runs Qualtrics studies heavily, this scan does the most work in practice. A raw Qualtrics export is not de-identified data; it arrives with several direct identifiers turned on by default, and nobody remembers they are there. Run the scan over every `.csv`, `.tsv`, and `.xlsx` in the code root and in the staged tree, and again after any file is copied.

Split the findings into two lists and keep them separate in the report.

Must be removed before the archive ships. These are direct or near-direct identifiers, and no analysis needs them:

| Column | Why |
| --- | --- |
| `IPAddress` | identifies a household or an institution, and geolocates |
| `LocationLatitude`, `LocationLongitude`, `LocationAccuracy` | Qualtrics fills these from the IP at full precision, often street-level |
| `RecipientEmail`, `RecipientFirstName`, `RecipientLastName` | copied in from the contact list on any emailed distribution |
| `ExternalReference` | the contact-list or CRM key for that person |
| `WorkerId`, `AssignmentId`, `HITId` | MTurk; a WorkerId is a stable, searchable, cross-study identifier |
| `PROLIFIC_PID`, `PID`, `prolific_id`, `SESSION_ID`, `STUDY_ID` | Prolific; the PID resolves to a public-facing account |
| CloudResearch / TurkPrime ids (`psid`, `cr_id`, panelist id, TurkPrime assignment id) | vendor-side panelist keys that link across every study on the platform |
| LUCID / Cint respondent ids (`rid`, `RID`, `ttid`, transaction id, supplier id) | panel keys, the same problem as CloudResearch |
| Any embedded-data field carrying an email, name, phone, student id, roster key, or class section | embedded data is whatever the researcher piped in, so read the values before deciding |

Flag for the user to decide. These raise re-identification risk without naming anybody, so the right call depends on the sample size and on what the analysis needs:

| Column | The judgment call |
| --- | --- |
| `ResponseId` | not identifying by itself, and it is the join key back to the response record in the Qualtrics account, which still holds the IP and the contact fields. Ship it if a stable row id is useful, and say in the README that it does not resolve to a person without account access. |
| `StartDate`, `EndDate`, `RecordedDate` | second resolution plus coarse geography plus a small sample can single out one respondent. Truncate to the day or the hour when the analysis does not use seconds, and keep `Duration (in seconds)`, which is usually the variable that actually matters. |
| Coarse geography derived from lat/long (country, state, region, zip3) | normally keepable, and worth a second look when cell sizes get to a handful. |
| `UserLanguage`, `DistributionChannel` | low risk alone, informative in combination when N is small. |
| `Q_RelevantIDDuplicate`, `Q_RelevantIDDuplicateScore`, `Q_RelevantIDFraudScore`, `Q_RelevantIDLastStartDate`, `Q_RecaptchaScore` | device-fingerprint output. Usually fine to keep, worth naming so the user knows it is fingerprinting. |
| `UserAgent`, browser, OS, screen resolution when present | a device fingerprint spread across columns. |

Open-ended text is the case a column-name rule cannot catch. Respondents write their own names, their employer, their manager's name, their town, their diagnosis, and their email address into free-response boxes, including boxes that only asked what they thought of the ad. A clean regex sweep is not evidence that an open-text column is safe.

So: identify the open-text columns mechanically, then read a real sample of the values, then flag every one of them in the report for human review. Say in the report which columns were sampled and how many values were read, so the user knows what was actually looked at.

Qualtrics files that carry the researcher's own footprint:

- The `.qsf` survey definition is JSON and holds the survey id, the owner/account id, the datacenter and brand base URL, contact-list and mailing-list references, embedded-data defaults, end-of-survey redirect URLs that sometimes carry tokens, and notification email addresses. Journals want the instrument, so ship the `.qsf`, but grep it first and report what is in it.
- The Qualtrics CSV export has three header rows: column names, question text, and a JSON `ImportId` row that also records the account's `timeZone`. A header scan must read row 1 and must not treat rows 2 and 3 as data.
- Contact-list exports, distribution-history exports, and panel invitation files (anything matching `*contact*list*`, `*distribution*`, `*panel*invit*`) hold participant email addresses and single-use survey links. These never enter the archive, the same way credential files never do.

Runnable check, headers across every delimited and Excel file:

```bash
python3 ~/.claude/skills/replication-package/scripts/scan_headers.py "$SCAN_ROOT"
```

Runnable check, values, for the identifier sitting in a column with an innocuous name:

```bash
python3 ~/.claude/skills/replication-package/scripts/scan_values.py "$SCAN_ROOT"
```

An `ipv4` hit can be a version string and a `phone` hit can be an id or a price, so report these with the count and the column name and let the user judge. A hit in a column the header scan called clean is the finding that matters most, since it means an identifier is hiding under an innocuous name.

Then read a sample of each open-text column with your own eyes:

```bash
python3 ~/.claude/skills/replication-package/scripts/sample_open_text.py "$FILE" "$COLUMN"
```

A ragged file is a finding in its own right: a Qualtrics export is rectangular, so a row with the wrong field count means the file was hand-edited or re-saved by something, and every column-based conclusion about it is suspect.

Grep the `.qsf` before shipping it:

```bash
python3 ~/.claude/skills/replication-package/scripts/scan_qsf.py "$QSF"
```

The remedy, and it is the same one nearly every time: keep the raw platform export out of the archive, ship a de-identified analysis dataset next to the script that produces it from that raw export, and let the replicator verify every step after the drop. The de-identification script is the part that makes this credible, so it goes in `code/` with the rest and gets named in the README. Then write it into the data availability statement, in the form of route 4 in section 6: raw responses are withheld for human-subjects reasons, the de-identified analysis file is included, and the code that produced it from the raw export is included.

### 4. Path sanitization

Edit copies inside the staging directory. The source tree is read-only from this skill.

Rewrite, and count substitutions per file so the user can spot-check:

- `$HOME` and `/Users/<username>/` to a relative path when the target is inside the package, else `<DATA_DIR>/...` with `DATA_DIR` documented in the README.
- `$HOME/Library/CloudStorage/Dropbox*/Apps/Overleaf/<project>/` to `./`, and the same for every other `Dropbox*` mount on the machine. Code written by any tool that resolved a real path will carry the full `CloudStorage` spelling, so rewrite that form, not just a short one.
- Cluster paths (`/gpfs/scratch60/<user>/`, `/home/<user>/`) to `<DATA_DIR>/`.
- Drive-letter absolute paths from a co-author's machine (`^[A-Za-z]:[\\/]`) to the same placeholders. Flag these loudly: they usually mean the co-author's code was never run anywhere else.
- The local username anywhere it survives the above.

Then re-grep the staged copies for any remaining `^/` or `~/` absolute path and report leftovers. Management Science requires relative paths only, and this check is what proves it.

Notebooks: strip outputs on the copy. `jupyter` is not installed here, so use Python directly.

```bash
python3 - "$f" <<'PY'
import json, sys
p = sys.argv[1]
nb = json.load(open(p))
for c in nb.get("cells", []):
    if c.get("cell_type") == "code":
        c["outputs"] = []
        c["execution_count"] = None
json.dump(nb, open(p, "w"), indent=1)
PY
```

### 5. Environment capture

The journals want this stated in the README, so write it there and keep the raw captures in `meta/` as backup.

- R: `Rscript -e 'sessionInfo()'`. `sessionInfo()` records the current session and not what the scripts need, so also grep the code for `library()`, `require()`, and `pkg::` calls, then resolve each with `Rscript -e 'cat(as.character(packageVersion("pkg")))'`. That list is what belongs in the README.
- renv: if `renv.lock` exists, copy it and say the package was built under renv. If not, note that versions came from the packaging machine's library.
- Python with uv: `uv pip freeze` inside the project, plus copies of `uv.lock` and `pyproject.toml` when present. A `uv.lock` is the strongest environment evidence available and should be mentioned by name in the README.
- Python without uv: `pip freeze` only when a virtualenv is active. Otherwise fall back to a static import scan across `.py` and `.ipynb`, write bare names, and head the file with `# Unpinned, from a static import scan. Pin before shipping.`
- Versions and hardware: `R --version`, `python3 -V`, `sw_vers -productVersion`, `sysctl -n machdep.cpu.brand_string hw.memsize hw.ncpu`. JMR requires operating system, CPU, memory, and disk in the README.
- Seeds: grep for `set.seed`, `np.random.seed`, `random.seed`, `torch.manual_seed`, `set seed`. Report where the seed is set, or state that randomness is uncontrolled. The README template below has a line for it.
- Runtime: ask the user for wall-clock time per script when it is not in a log. Management Science wants runtime stated past a few minutes; JMR past five.
- `meta/git_hash.txt`: `git rev-parse HEAD` and `git status --short`, so a dirty tree is visible. If it is not a repo, write that plainly.

### 6. Data that cannot ship

Handle this as a documented access path. It is never a reason to fail.

Decide per dataset:

1. Ships as is. Default.
2. Too large. All four journals accept external hosting. Management Science caps the ScholarOne upload at 200 MB and asks for a Dropbox or Google Drive link, reachable without registration, above that. JMR deposits to the AMA's Harvard Dataverse collection. Build the archive without the file, write `data/raw/README.md` with the host, the URL or DOI, the file's sha256, and its size, and flag it.
3. Licensed or proprietary (Nielsen, Circana/IRI, comScore, WRDS, Compustat, a platform NDA). Ship the code, the full variable dictionary, and access instructions concrete enough to be actionable: vendor, contact, product name, date range, version, and the exact extract or query. Journals accept this only with an editor-approved alternative disclosure plan, so remind the user that the plan is raised at or near initial submission and not at acceptance.
4. Restricted for human-subjects reasons. Ship de-identified analysis data plus the de-identification script, and keep raw identifiers out entirely.

Where the data cannot ship, all four journals offer the same menu of substitutes, and the archive should carry whichever the user picked: disguised data (noise or a multiplier), summary and distributional statistics sufficient to repopulate the model, a random subset of rows, a synthetic dataset generated from the estimated model with evidence that it is a valid surrogate, or a dictionary complete enough for someone to rebuild a comparable dataset. Management Science alone also allows an embargo (one year for code, two for data).

Whichever route applies, `data/dictionaries/` still gets a codebook for the dataset, shipped or not, with every variable named as it appears in the code and a one-line description. Management Science requires this without exception.

Draft the matching data availability statement for the title page. JMR prescribes fixed wordings; the two that usually apply are "Restrictions apply to the availability of these data, which were used under license, and thus the data are not publicly available." and "An alternative disclosure plan was approved for this article."

### 7. Generate the meta files

`meta/manifest.json`: walk the staged tree and record `path`, `size_bytes`, `sha256` for every file, sorted by path.

```bash
python3 - "$STAGE" <<'PY'
import hashlib, json, os, sys
root = sys.argv[1]
out = []
for dp, _, fns in os.walk(root):
    for fn in sorted(fns):
        p = os.path.join(dp, fn)
        h = hashlib.sha256(open(p, "rb").read()).hexdigest()
        out.append({"path": os.path.relpath(p, root),
                    "size_bytes": os.path.getsize(p), "sha256": h})
out.sort(key=lambda r: r["path"])
json.dump(out, open(os.path.join(root, "meta", "manifest.json"), "w"), indent=2)
PY
```

`data/dictionaries/<name>.md`: one row per variable with name, type, and description. Prefill name and type from the CSV header and first rows; leave `[FILL IN]` for description.

`meta/checklist.md`: the template below, ticked against what was actually produced.

### 8. Zip

`$DEST_ABS` is the absolute destination resolved by the check in "Staging and archive destination", re-checked against the Overleaf rule immediately before the write. The zip runs after a `cd`, so a relative `$DEST` would resolve against the staging parent; use the absolute form.

```bash
cd "$(dirname "$STAGE")" && zip -r -X \
  "$DEST_ABS/<slug>_replication_<YYYYMMDD>.zip" "$(basename "$STAGE")" \
  -x '*.DS_Store' -x '*/__MACOSX/*' -x '*/.git/*' -x '*/.Rproj.user/*' \
  -x '*/__pycache__/*' -x '*/.ipynb_checkpoints/*' -x '*conflicted copy*'
```

`-X` drops macOS resource forks and uid/gid, which otherwise make the archive look strange to a Linux data editor. The conflicted-copy exclusion matters because these projects live in Dropbox. Verify with `unzip -l` and report the size; warn above 200 MB, and mention the Dropbox upload when the destination is inside a synced folder.

### 9. Report

1. Absolute path to the zip in the destination the user named, file count, total size, and whether that destination syncs.
2. Safety scan findings, with file and line, secrets separate from personal data, and "must remove" separate from "your call". Name every open-text column that was sampled and every one that still needs reading. The user reads this before shipping.
3. The exhibit map, including every unmapped exhibit and every orphan output.
4. Path rewrites per file, plus any absolute path that survived.
5. What is missing or unpinned, and what needs external hosting.
6. Next actions in the order the journal will want them.

## Journal requirements

| | Marketing Science | Management Science | JMR | JCR |
| --- | --- | --- | --- | --- |
| Due | acceptance, before publication | acceptance, before production | conditional acceptance | invited revision |
| Deposited to | journal website, keyed to article DOI | journal website, approved by the Data Editor | AMA Harvard Dataverse collection | OSF, Harvard Dataverse, QDR, or ResearchBox |
| README | required only in the substitute-data case | required, journal's own template | required, three specified elements | not required |
| Size cap | none stated | 200 MB on ScholarOne, link above it | none stated | none stated |
| Environment | not required | software and versions, runtime past a few minutes | software, versions, OS, CPU, memory, disk, runtime past 5 min | statistical packages and versions |
| Extra artifact | editorial checklist | 36-item replication checklist; AsCollected, a data-provenance and author-contribution disclosure due at initial submission, not at acceptance | data availability statement on the title page | data collection statement in ScholarOne |

Details worth carrying into the run:

- Marketing Science operates under the 2013 Desai replication and disclosure policy. It asks for data and estimation code plus a complete list and description of the variables. Exemptions go to the Editor-in-Chief at submission time.
- Management Science is the strictest and the most recently revised. Its checklist requires a master script, relative paths only, log files from both the cleaning run and the analysis run, code that runs clean on a different machine, and README instructions for reproducing every figure, table, and result. Build to this one and the rest follow.
- JMR requires a file list with descriptions, replication instructions, and a computing-resources description. File names and paths become public even when the file itself is restricted, so no confidential information in any filename.
- JCR requires an anonymized, reviewer-accessible link with no author or institution names in the URL or the files, and seven-year retention.
- None of the four mandates the Social Science Data Editors README template, but its structure is a superset of all four, so use it as the default and add the journal-specific pieces.

## README template

```
# Replication Package: [Title]

## Overview
[One paragraph: what the code does, what it reproduces, and roughly how long a full run takes.]
Author: [name] ([affiliation]). Contact: [email].
Git commit at packaging: [hash]

## Data availability and provenance
Rights: [I have legitimate access to and permission to use the data / permission to redistribute is
documented below.]
Summary of availability: [All data are publicly available / Some data cannot be made publicly
available / No data can be made publicly available]
### [Dataset name]
Source, date range, version, how obtained, license, and where it sits in this package. For anything
not shipped, the exact access path: vendor, contact, product, extract or query.

## Dataset list
| File | Source | Rows | Vars | Provided | Notes |

## Computational requirements
Software and exact versions, including every package the scripts call.
Hardware: OS, CPU, memory, disk.
Randomness: seed set at [file:line] / not controlled.
Runtime: [per script and total].

## Description of programs/code
Run order, what each script reads and writes, and which exhibit each one produces.

## Instructions to replicators
1. Place raw data in `data/raw/` (see data/dictionaries/).
2. Run `code/00_master.R` from the package root.
3. Tables land in `output/tables/`, figures in `output/figures/`, logs in `logs/`.

## List of tables and programs
| Figure/Table # | Program | Line | Output file | Note |

## Notes
All paths are relative to the package root unless prefixed `<DATA_DIR>`.
```

## Checklist template (`meta/checklist.md`)

```
Target journal: [Marketing Science | Management Science | JMR | JCR]

Code
- [ ] All code producing every table, figure, and in-text number in the main paper
- [ ] Code that builds analysis data from raw data
- [ ] A master script running everything in order
- [ ] Relative paths only, verified by re-grep of the staged tree
- [ ] Runs clean on a second machine

Data
- [ ] Raw data included, or an approved alternative disclosure plan documented
- [ ] Analysis data included
- [ ] A dictionary for every dataset, shipped or not
- [ ] Qualtrics IPAddress, Location*, Recipient*, and ExternalReference columns dropped
- [ ] Platform ids dropped: MTurk WorkerId/AssignmentId, Prolific PID, CloudResearch, LUCID/Cint
- [ ] Timestamp resolution decided; ResponseId keep-or-drop decided
- [ ] Every open-text column sampled and read by a human, not just regex-scanned
- [ ] Raw platform export withheld where needed, with the de-identification script shipped
- [ ] `.qsf` grepped for account, contact-list, and distribution details
- [ ] Data availability statement drafted for the title page

Materials
- [ ] Instruments and stimuli as participants saw them (.qsf, screenshots, scripts)
- [ ] Preregistration and any documented deviations
- [ ] Exclusions, screens, and recruitment waves reported

Environment
- [ ] Software and exact versions in the README; hardware, runtime, and seeds stated
- [ ] renv.lock or uv.lock included where one exists

Reproducibility and metadata
- [ ] Exhibit map complete, no UNMAPPED rows
- [ ] Log files from the cleaning run and the analysis run
- [ ] README complete, git hash recorded, manifest with sha256
- [ ] One zip, under the target journal's size cap
```

## Failure modes

- Code root not given: ask for it, once, in the batched question message. The paper root holding only `.tex` and exhibits is normal and is not a symptom of anything.
- Archive destination not given: ask for it, and say it will not be guessed. Nothing is written until there is an answer.
- Destination inside `$HOME/Library/CloudStorage/Dropbox*/Apps/Overleaf/`: refuse, say it syncs to Overleaf, ask for another folder.
- Code lives on the cluster: stop and have the user sync it locally first.
- A PDF needs reading: use `~/.claude/assets/bin/pdfread.py`. In this setup the Read tool fails on PDFs and `pdftotext` and `pdftoppm` do not exist.
- `Rscript` missing: write the placeholder, flag it, keep going.
- `pip freeze` with no active virtualenv: it lists the global environment and is misleading. Prefer `uv pip freeze` or the static import scan, and say which was used.
- Live credential found: stop before zipping, show file and line, ask for a decision.
- Data over 200 MB, or over the journal's cap: build without it, write the pointer file, flag it.
- Exhibits with no producing script: report them and never invent a mapping. This is the most common real defect, and only the user can resolve it.
- Not a git repo: `git_hash.txt` says so.

## Out of scope

Does not submit or upload anywhere, does not push to GitHub, does not edit the manuscript or the `.bib`, does not run the analysis to check that outputs reproduce, does not generate new tables or figures, and does not modify the source tree. All sanitization happens on copies in the staging directory.
